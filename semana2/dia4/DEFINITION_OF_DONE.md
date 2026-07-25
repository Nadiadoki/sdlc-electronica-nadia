# Definition of Done

Un cambio se considera "terminado" cuando cumple TODOS los criterios siguientes, expresados como escenarios verificables.

```
Feature: Definition of Done del proyecto

  Scenario: Cobertura de tests suficiente
    Given un Pull Request con cambios de código
    When se ejecuta pytest con reporte de cobertura
    Then la cobertura total es mayor o igual a 80%

  Scenario: Sin errores de estilo
    Given un Pull Request con cambios de código
    When se ejecuta ruff check sobre el proyecto
    Then no se reportan errores

  Scenario: Sin errores de tipos
    Given un Pull Request con cambios de código
    When se ejecuta mypy sobre el proyecto
    Then no se reportan errores
    And toda función pública tiene sus tipos anotados

  Scenario: Auto-revisión antes del merge
    Given un Pull Request listo para revisión
    When el autor lee su propio diff línea por línea
    Then puede explicar cada línea sin mirar notas
    And no queda código de depuración (prints sueltos, comentarios "TODO" sin resolver, etc.)

  Scenario: Documentación actualizada
    Given un cambio que afecta comportamiento público o estructura del proyecto
    When se abre el Pull Request
    Then el README y/o el AI_LOG reflejan ese cambio
```

## Notas

- **Cobertura ≥80%:** se verifica con `pytest --cov=<paquete> --cov-fail-under=80`. El build falla automáticamente si no se cumple.
- **ruff limpio:** `ruff check` debe salir con `All checks passed!`, sin excepciones silenciadas salvo con un comentario explícito que justifique el porqué (ej. `# noqa: E501 - ...`).
- **mypy limpio:** `mypy` no debe reportar errores, y las funciones públicas nuevas deben tener anotaciones de tipo completas (regla `disallow_untyped_defs`).
- **Auto-revisión:** antes de pedir merge, el autor revisa su propio diff como si fuera el revisor — esto es lo que permite responder "muéstrame la línea X y explícame por qué la escribiste así" sin dudar.
- **Documentación:** cualquier cambio de comportamiento (nueva función pública, cambio de API, decisión de diseño) debe quedar reflejado en README.md o en AI_LOG.md, para que el estado del proyecto sea siempre reconstruible leyendo esos dos archivos.
