# Интеграция с comol/ai_rules_1c

## Принцип

`1c-testing` — project-local дополнительный skill.

Не изменяй upstream-файлы `AGENTS.md` и `.codex/rules/*` для его подключения: `AGENTS.md` управляется `ai_rules_1c`, а пользовательские постоянные требования предназначены для `USER-RULES.md`.

## Приоритет

`ai_rules_1c` читает `USER-RULES.md` раньше базовых правил. Поэтому там фиксируется политика: тесты наблюдаемого BSL-поведения являются частью Definition of Done.

Это уточняет базовый принцип `AGENTS.md` не добавлять speculative tests: тест, требуемый проектным Definition of Done, не является speculative.

## MCP-first согласован с ai_rules_1c

`ai_rules_1c` уже требует предпочитать подходящие MCP-инструменты. Поэтому `1c-testing` не вводит отдельную конкурирующую дисциплину, а конкретизирует её для build/test:

1. если в сессии доступен MCP `v8_runner`, build/test выполняется через него;
2. для YAxUnit-модуля используется `run_module_tests`;
3. для полного прогона используется `run_all_tests`;
4. CLI применяется только для недоступных в MCP операций (`extensions`, `--no-build`, help/transport diagnostics) либо если MCP недоступен;
5. не дублируй один и тот же тест MCP-вызовом и CLI-командой без причины.

## Что остаётся у ai_rules_1c

`1c-testing` не дублирует и не отменяет coding standards, MCP-first поиск, правила метаданных, vendor support, repository locks, validation gates, memory и subagents.

Если для нового тестового общего модуля нужно изменить метаданные, используй `1c-metadata-manage`.

## Что принадлежит 1c-testing

- выбор YAxUnit/Vanessa;
- структура тестов;
- тестовые данные;
- регрессионный workflow;
- v8-runner MCP/CLI build+test;
- диагностика YAxUnit;
- Definition of Done для тестирования.

## Обновление ai_rules_1c

Продолжай обновлять upstream штатно через `install.ps1 update` или существующий workflow проекта.

Не копируй `1c-testing` в исходный клон `comol/ai_rules_1c/content/skills`, если не поддерживаешь собственный fork.

Храни skill в `.codex/skills/1c-testing/`, а проектную политику в `USER-RULES.md`.

Если `.codex/config.toml` содержит project-local `mcp_servers.v8_runner`, после обновления `ai_rules_1c` проверь, что пользовательская MCP-секция сохранилась. Не заменяй рабочий stdio-конфиг на HTTP без явной причины.

## 114 и 115

Skill должен оставаться одинаковым. Не зашивай в него `ТестыУТ114`, `ТестыУТ115`, путь базы, путь `v8project.yaml` или версию конфигурации. Эти значения читаются из `v8project.yaml`, структуры проекта и project-local `.codex/config.toml`.
