# Источники и принятые решения

Пакет подготовлен 10.09.2026. Обновление 1.5: runtime-aware testing, QA/TestClient и разделение breadth/risk.

## comol/ai_rules_1c

- https://github.com/comol/ai_rules_1c
- `adapters/codex.yaml`
- `AGENTS.md`
- `USER-RULES.md`

Решение: project-local `.codex/skills/1c-testing` + политика в `USER-RULES.md`; `AGENTS.md` не модифицируется. Для Codex skills размещаются под `.codex/skills/{name}`. MCP-first тестирование согласуется с общим MCP-first подходом `ai_rules_1c`.

## YAxUnit

- https://github.com/bia-technologies/yaxunit
- `documentation/docs/getting-started/structure.md`
- `documentation/docs/features/test-registration.md`
- `.cursor/rules/tests/testing_guidelines.mdc`
- `.cursor/rules/tests/yaxunit-test-data.mdc`
- `.cursor/rules/tests/yaxunit-asserions.mdc`
- `.cursor/rules/tests/yaxunit_test_writer_prompt.mdc`

Решение: общие модули, `ИсполняемыеСценарии() Экспорт`, fluent registration, Arrange/Act/Assert, `ЮТест.ОжидаетЧто`, фабрики через `ЮТест.Данные()`.

## v8-runner-rust

- https://github.com/alkoleft/v8-runner-rust
- `SKILL/references/testing.md`
- `SKILL/references/project-workflows.md`
- `src/mcp/request.rs`
- `src/mcp/service.rs`
- `docs/CAPABILITIES.md`

Решение:

- Codex → `v8_runner` MCP по stdio — предпочтительный путь;
- `run_module_tests` — build+YAxUnit для конкретного модуля;
- `run_all_tests` — полный YAxUnit либо Vanessa (`runner=vanessa`);
- `build_project` — отдельная сборка;
- MCP публикует 8 операций и намеренно не зеркалит весь CLI;
- `extensions` и `--no-build` остаются CLI fallback;
- `run_module_tests` использует BuildFirst.

## va-ai

- https://github.com/Nikolay-Shirokov/va-ai
- закреплённая ревизия: `df127cf31055c6cf03e7a2b76a4d3acaf954e442`
- `docs/project-structure-guide.md`
- `docs/AI-WORKFLOW-SUMMARY.md`

Решение: минимальный автономный снимок размещён в `1c-testing/vendor/va-ai`: `data/library-full.json`, поиск шагов, валидатор, руководство и шаблоны. Снимок используется при недоступном Vanessa MCP и не является критичной зависимостью YAxUnit workflow. MIT-лицензия источника сохранена в `vendor/va-ai/LICENSE`; состав и ревизия описаны в `vendor/va-ai/SOURCE.md`.

## Vanessa Automation MCP

- https://github.com/Pr-Mex/vanessa-automation/blob/develop/docs/AI/index.md
- https://github.com/Pr-Mex/vanessa-automation/blob/develop/docs/index.md
- https://pr-mex.github.io/vanessa-automation/dev/JsonParams/JsonParamsEN/

Решение: выполнение и повторная проверка `.feature` всегда идут через `v8_runner`. Vanessa MCP не является runner и используется только точечно для поиска неизвестного шага, проверки неоднозначного синтаксиса или инспекции конкретного элемента формы после доказанного падения.

Руководство skill отдельно фиксирует требования к бизнес-проверкам, независимости данных, устойчивым локаторам, ожиданиям вместо фиксированных пауз и подтверждению фактического выполнения. Учебные примеры `va-ai` не считаются стандартом архитектуры сценариев.

## SteelMorgan/1c-agent-based-dev-framework — methodological reference

- https://github.com/SteelMorgan/1c-agent-based-dev-framework
- `framework/workflows/full-cycle/SKILL.md`
- `framework/rules/tdd-policy/SKILL.md`
- `framework/rules/vanessa-scenario-policy/SKILL.md`
- `framework/rules/vanessa-test-isolation-policy/SKILL.md`
- `framework/subagents/developer-tests.md`
- `framework/subagents/tester.md`

Использованные методические идеи: разделение runtime-слоёв тестирования, distinction unit/integration, проверка пользовательского контекста прав/RLS, исследование фактического UI перед новым Vanessa-сценарием и классификация падения теста до изменения production-кода.

Код, тексты prompts/rules и структура SteelMorgan не копировались. Репозиторий использует PolyForm Small Business License 1.0.0; этот пакет сохраняет собственные формулировки и архитектуру.

## OneRPA QA MCP / TestClient

Решение: QA/TestClient используется как быстрый developer runtime/UI smoke и для подтверждения фактического контракта формы. Vanessa остаётся слоем сохраняемых acceptance/regression/E2E-сценариев. Точные tool names и execution semantics принадлежат установленному `ai_rules_1c`/OneRPA tooling и не дублируются здесь.
