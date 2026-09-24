#!/usr/bin/env python3
"""Быстрая эвристическая проверка качества Vanessa Automation feature-файлов."""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path


SCENARIO_RE = re.compile(r"^\s*(Сценарий|Структура сценария):\s*(.+?)\s*$", re.IGNORECASE)
STEP_RE = re.compile(r"^\s*(Дано|Когда|Тогда|И|Но|Также|Затем)\s+(.+?)\s*$", re.IGNORECASE)
ASSERTION_RE = re.compile(
    r"\b(равен|равна|равно|содержит|не содержит|видим|видима|доступен|доступна|"
    r"отсутствует|появил|открылось окно|закрылось окно|существует|не существует|"
    r"проверяю|ожидаю что|вижу|не вижу)\b",
    re.IGNORECASE,
)


@dataclass(frozen=True)
class Finding:
    severity: str
    code: str
    path: Path
    line: int
    message: str


def feature_files(paths: list[Path]) -> list[Path]:
    result: list[Path] = []
    for path in paths:
        if not path.exists():
            raise ValueError(f"Путь не найден: {path}")
        if path.is_dir():
            result.extend(sorted(path.rglob("*.feature")))
        elif path.suffix.lower() == ".feature":
            result.append(path)
        else:
            raise ValueError(f"Ожидался .feature или каталог: {path}")
    return list(dict.fromkeys(result))


def inspect(path: Path) -> list[Finding]:
    lines = path.read_text(encoding="utf-8-sig").splitlines()
    findings: list[Finding] = []
    scenarios: list[tuple[int, str, list[tuple[int, str, str]]]] = []
    current: tuple[int, str, list[tuple[int, str, str]]] | None = None

    for number, line in enumerate(lines, 1):
        scenario = SCENARIO_RE.match(line)
        if scenario:
            current = (number, scenario.group(2), [])
            scenarios.append(current)
            continue

        step = STEP_RE.match(line)
        if step and current is not None:
            current[2].append((number, step.group(1).lower(), step.group(2)))

        stripped = line.strip()
        is_comment = stripped.startswith("#")
        if not is_comment and re.search(r"e1cib/data/.+\?ref=[0-9a-f]+", line, re.IGNORECASE):
            findings.append(Finding("ERROR", "VA101", path, number,
                                    "Зафиксирована ссылка объекта с ref; объект должен находиться или создаваться сценарием."))
        if not is_comment and re.search(r"(?<![\w$])(?:[A-Za-z]:\\|/home/|/Users/)", line):
            findings.append(Finding("ERROR", "VA102", path, number,
                                    "Абсолютный локальный путь делает сценарий непереносимым."))
        if not is_comment and re.match(r"^\s*(Дано|Когда|Тогда|И|Но|Также|Затем)\s+пауза\b", line, re.IGNORECASE):
            findings.append(Finding("WARN", "VA201", path, number,
                                    "Фиксированная пауза: замени ожиданием наблюдаемого состояния или обоснуй комментарием."))
        if not is_comment and re.search(r"\b(строк[аеу]|строку)\s+номер\s+[\"']?\d+", line, re.IGNORECASE):
            findings.append(Finding("WARN", "VA202", path, number,
                                    "Адресация по номеру строки хрупкая; предпочти бизнес-ключ или явно созданный набор данных."))
        if re.search(r"@(Draft|Ignore\w*)\b", stripped, re.IGNORECASE):
            findings.append(Finding("WARN", "VA203", path, number,
                                    "Сценарий исключён или помечен черновиком; проверь, что test gate действительно его запускает."))
        if re.search(r"TODO|FIXME|<[^>]+>|\.\.\.", line, re.IGNORECASE):
            findings.append(Finding("ERROR", "VA103", path, number,
                                    "В сценарии остался плейсхолдер или незавершённый фрагмент."))

    if not scenarios:
        findings.append(Finding("ERROR", "VA001", path, 1, "Не найден ни один сценарий."))

    for line, name, steps in scenarios:
        if not steps:
            findings.append(Finding("ERROR", "VA002", path, line, f"Сценарий «{name}» не содержит шагов."))
            continue
        has_assertion = any(ASSERTION_RE.search(text) for _, _, text in steps)
        if not has_assertion:
            findings.append(Finding("ERROR", "VA003", path, line,
                                    f"Сценарий «{name}» не содержит явной проверки результата."))
        if len(steps) > 35:
            findings.append(Finding("WARN", "VA204", path, line,
                                    f"В сценарии «{name}» {len(steps)} шагов; проверь, нельзя ли разделить его по бизнес-результатам."))

    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="+", type=Path, help="Файлы .feature или каталоги")
    parser.add_argument("--strict", action="store_true", help="Считать предупреждения ошибкой")
    args = parser.parse_args()

    try:
        files = feature_files(args.paths)
    except ValueError as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 2
    if not files:
        print("ERROR: .feature-файлы не найдены", file=sys.stderr)
        return 2

    try:
        findings = [finding for path in files for finding in inspect(path)]
    except (OSError, UnicodeError) as error:
        print(f"ERROR: не удалось прочитать feature: {error}", file=sys.stderr)
        return 2
    for finding in findings:
        print(f"{finding.path}:{finding.line}: {finding.severity} {finding.code}: {finding.message}")

    errors = sum(item.severity == "ERROR" for item in findings)
    warnings = sum(item.severity == "WARN" for item in findings)
    print(f"Проверено файлов: {len(files)}; ошибок: {errors}; предупреждений: {warnings}")
    return 1 if errors or (args.strict and warnings) else 0


if __name__ == "__main__":
    raise SystemExit(main())
