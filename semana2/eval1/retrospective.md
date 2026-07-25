# Sprint 1 Retrospective

## ¿Qué salió bien?

- El núcleo completo del Sprint Goal (registrar lecturas, detectar anomalías de temperatura y humedad, umbrales inyectados, alertas por consola y archivo) quedó implementado con TDD estricto: cada historia tiene su ciclo Red→Green documentado en el historial de commits.
- La decisión de inyectar el `threshold` en `AnomalyDetector` en vez de hardcodearlo permitió reutilizar la misma clase para temperatura y humedad sin duplicar lógica — los tests de US-03 (humedad) pasaron sin tener que tocar el código, solo agregando un umbral distinto.
- `AlertManager` quedó desacoplado de una implementación concreta de alerta (depende de cualquier objeto con `.send()`), lo que permitió probarlo con una alerta falsa creada dentro del propio test, sin depender de `ConsoleAlert` ni `FileAlert` reales.
- La cobertura final (98.4%) superó ampliamente el mínimo exigido (80%) sin haber escrito tests solo para inflar el número — cada test corresponde a un escenario Gherkin ya definido en el backlog.

## ¿Qué mejorar?

- Varias veces el código se pegó en el archivo equivocado (un test terminó dentro de `alerts.py` en vez de `test_alert_manager.py`), lo que causó errores confusos de `git diff` y tuvo que revisarse con calma. Falta más cuidado al copiar/pegar entre Notepad y la terminal, verificando el archivo activo antes de pegar.
- El primer intento de excluir los tests de `disallow_untyped_defs` en `mypy` (día 4) usó un patrón de módulo que `mypy` rechazó; se resolvió con `exclude` por ruta, pero muestra que conviene probar la configuración con un caso simple antes de asumir que la sintaxis es correcta.
- Los mensajes de commit de RED podrían ser más consistentes: algunos usan `- us-01`, otros `- us-05-us-06`. Estandarizar el formato ayudaría a que el historial sea más fácil de leer para alguien externo.

## Acción concreta para el próximo Sprint

**Antes de pegar cualquier bloque de código, confirmar en voz alta (o por escrito en el chat) qué archivo está activo en Notepad**, para evitar que el código termine en el archivo equivocado como pasó con `alerts.py`/`test_alert_manager.py` en este Sprint. Esto es una causa raíz identificable y corregible, no un problema de la herramienta.
