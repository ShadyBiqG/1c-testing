# 1c-testing skill package

Project-local skill для Codex, который добавляет к `comol/ai_rules_1c` единый workflow автоматизированного тестирования 1С.

Версия пакета: **1.2 — MCP-first + offline Vanessa**.

```text
1c-testing/
├── SKILL.md
├── references/
│   ├── ai-rules-integration.md
│   ├── architecture.md
│   ├── regression-workflow.md
│   ├── test-data.md
│   ├── v8-runner.md
│   ├── vanessa.md
│   └── yaxunit.md
├── vendor/
│   └── va-ai/                  # offline-каталог шагов и валидатор
└── templates/
    ├── TestDataModule.bsl
    └── TestModule.bsl

USER-RULES.fragment.md
install-or-update.ps1
INSTALL.md
SOURCES.md
```

Архитектура:

- `ai_rules_1c` — общие правила разработки 1С;
- `1c-testing` — тестовая дисциплина;
- YAxUnit — быстрые BSL/регрессионные тесты;
- v8-runner MCP — основной AI-интерфейс build/test;
- v8-runner CLI — fallback для `extensions`, `--no-build` и ручной диагностики;
- Vanessa — UI/E2E;
- Vanessa MCP — поиск шагов, проверка Gherkin и интерактивная отладка;
- встроенный снимок va-ai — offline fallback для базы шагов и валидации Vanessa; отдельная установка не нужна.

Для локального Codex рекомендуется v8-runner MCP по **stdio**, привязанный к `v8project.yaml` конкретного проекта.

Канонический исходник хранится в этом Git-репозитории. Инструкции глобальной и project-local установки: [INSTALL.md](INSTALL.md).
