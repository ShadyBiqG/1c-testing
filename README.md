# 1c-testing skill package

Project-local skill для Codex, который добавляет к `comol/ai_rules_1c` единый workflow автоматизированного тестирования 1С.

Версия пакета: **1.5 — runtime-aware testing + QA/TestClient**.

```text
1c-testing/
├── SKILL.md
├── references/
│   ├── ai-rules-integration.md
│   ├── architecture.md
│   ├── regression-workflow.md
│   ├── test-strategy.md
│   ├── test-data.md
│   ├── v8-runner.md
│   ├── vanessa.md
│   └── yaxunit.md
├── vendor/
│   └── va-ai/                  # offline-каталог шагов и валидатор
├── scripts/
│   └── check_vanessa_quality.py # эвристический quality-check feature
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
- YAxUnit — быстрые BSL/интеграционные тесты серверной логики;
- OneRPA QA MCP / TestClient — быстрый runtime/UI smoke и проверка изменённого пользовательского поведения;
- v8-runner MCP — основной AI-интерфейс build/test;
- v8-runner CLI — fallback для `extensions`, `--no-build` и ручной диагностики;
- Vanessa — сохраняемые acceptance/regression/E2E-сценарии, когда долговечное покрытие действительно нужно;
- Vanessa MCP — необязательная точечная диагностика неизвестного шага или элемента формы;
- встроенный снимок va-ai — offline fallback для базы шагов и валидации Vanessa; отдельная установка не нужна.
- встроенный quality-check — поиск хрупких ссылок/путей/пауз и сценариев без явного результата;
- runtime-aware стратегия отделяет ширину проверки L1–L4 от риска изменения и не раздувает локальный high-risk fix до полного регресса без доказанного широкого влияния.

Для локального Codex рекомендуется v8-runner MCP по **stdio**, привязанный к `v8project.yaml` конкретного проекта.

Канонический исходник хранится в этом Git-репозитории. Инструкции глобальной и project-local установки: [INSTALL.md](INSTALL.md).
