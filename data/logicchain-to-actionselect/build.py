#!/usr/bin/env python3
"""Project seed LogicChain rows into no-think ActionSelect weak labels.

The projection intentionally keeps only the itemic tokens named by
``logic_chain.events[*].action``. It is core-evidence supervision rather than
FullRecall ActionSelect gold.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any


ITEMIC_TOKEN_RE = re.compile(
    r"<\|(?:video|ad|prod|living)_begin\|><s_a_\d+><s_b_\d+><s_c_\d+>"
)
TASK_MARKER_RE = re.compile(r"\n角色任务[：:]")
TOPIC_RE = re.compile(r"\n主题[：:]\s*([^\n]+)")


def load_rows(path: Path) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line_no, line in enumerate(handle, start=1):
            value = json.loads(line)
            if not isinstance(value, list) or len(value) != 1:
                raise ValueError(f"{path}:{line_no}: expected one wrapped row")
            row = value[0]
            if not isinstance(row, dict):
                raise ValueError(f"{path}:{line_no}: row is not an object")
            if not all(isinstance(row.get(key), str) for key in ("system", "prompt", "response")):
                raise ValueError(f"{path}:{line_no}: invalid SFT fields")
            rows.append({key: row[key] for key in ("system", "prompt", "response")})
    return rows


def response_value(response: str) -> Any:
    text = response.strip()
    if text.startswith("<think>") and "</think>" in text:
        text = text.split("</think>", 1)[1].strip()
    return json.loads(text)


def split_history_topic(prompt: str) -> tuple[str, str]:
    markers = list(TASK_MARKER_RE.finditer(prompt))
    if not markers:
        raise ValueError("prompt has no role-task marker")
    history = prompt[: markers[-1].start()].rstrip()
    topic_matches = TOPIC_RE.findall(prompt[markers[-1].start() :])
    if not topic_matches:
        raise ValueError("prompt has no topic")
    return history, topic_matches[-1].strip()


def stable_unique(values: list[str]) -> list[str]:
    return list(dict.fromkeys(values))


def render_prompt(history: str, topic: str) -> str:
    return (
        history.rstrip()
        + "\n\n"
        + "角色任务：你需要以极端严苛的用户行为数据挖掘专家及数据格式化专家的身份，"
        + "基于以上交互历史，针对给定主题筛选并提取出全部相关的历史交互行为。\n\n"
        + f"主题：{topic}\n\n"
        + "输出格式要求：请仅以包含 SID 的 JSON 数组形式返回结果，"
        + "切勿输出任何额外的解释说明或无关字符。/no_think"
    )


def render_response(labels: list[str]) -> str:
    value = json.dumps(labels, ensure_ascii=False, separators=(",", ":"))
    return f"<think>\n</think>\n{value}"


def project(row: dict[str, str]) -> list[dict[str, str]] | None:
    value = response_value(row["response"])
    if not isinstance(value, dict) or not isinstance(value.get("logic_chain"), dict):
        return None

    chain = value["logic_chain"]
    history, prompt_topic = split_history_topic(row["prompt"])
    topic = str(chain.get("name", "")).strip()
    if not topic or topic != prompt_topic:
        raise ValueError("prompt topic and logic_chain.name disagree")

    events = chain.get("events")
    if not isinstance(events, list):
        raise ValueError("logic_chain.events is not a list")
    raw_labels: list[str] = []
    for event in events:
        if not isinstance(event, dict):
            raise ValueError("logic event is not an object")
        raw_labels.extend(ITEMIC_TOKEN_RE.findall(str(event.get("action", ""))))

    labels = stable_unique(raw_labels)
    if not labels:
        return []
    if any(token not in history for token in labels):
        raise ValueError("projected token is missing from visible history")

    return [
        {
            "system": row["system"],
            "prompt": render_prompt(history, topic),
            "response": render_response(labels),
        }
    ]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path, help="seed 懂用户.jsonl")
    parser.add_argument("output", type=Path, help="projected ActionSelect JSONL")
    args = parser.parse_args()

    counts: Counter[str] = Counter()
    output_lines: list[str] = []
    for row in load_rows(args.source):
        projected = project(row)
        if projected is None:
            counts["source_actionselect"] += 1
            continue
        counts["source_logicchain"] += 1
        if not projected:
            counts["rejected_without_itemic_token"] += 1
            continue
        counts["output_rows"] += 1
        output_lines.append(
            json.dumps(projected, ensure_ascii=False, separators=(",", ":")) + "\n"
        )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    payload = "".join(output_lines)
    args.output.write_text(payload, encoding="utf-8")
    summary = {
        **counts,
        "sha256": hashlib.sha256(payload.encode("utf-8")).hexdigest(),
        "output": str(args.output),
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
