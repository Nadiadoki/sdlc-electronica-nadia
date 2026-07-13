Fecha: 13/07/2026 (Día 1 · Lunes)

* Prompt: "Ayúdame a desarrollar la bitácora AI\_LOG.md y a hacer el ejercicio del día 1: 5 funciones puras sobre una clase Reading (conversión de unidades, detección de umbral, serialización) con type hints completos, verificadas con mypy y ruff."
* Qué produjo la IA: Un módulo lectura.py con las clases base (SensorType, Reading, Transport), un módulo funciones\_puras.py con 5 funciones (conversión C→F, detección de umbral, validación de rango, serialización a texto y comparación entre lecturas), y sus tests en test\_funciones\_puras.py.
* Decisión: Acepté las 5 funciones tal cual, los 6 tests pasaron a la primera corrida (pytest) y mypy no encontró errores de tipos. Sin embargo, ruff detectó que en funciones\_puras.py había un import sin usar (SensorType, importado pero nunca referenciado directamente en el archivo). Lo corregí eliminando ese import de la línea 6. No fue un error grave, pero muestra que hay que revisar el código generado en vez de asumir que todo lo que trae es necesario.

