# Bitacora AI\_LOG.md

## Semana 1

##### Fecha: 13/07/2026 (Día 1 · Lunes)

* Prompt: "Ayúdame a desarrollar la bitácora AI\_LOG.md y a hacer el ejercicio del día 1: 5 funciones puras sobre una clase Reading (conversión de unidades, detección de umbral, serialización) con type hints completos, verificadas con mypy y ruff."
* Qué produjo la IA: Un módulo lectura.py con las clases base (SensorType, Reading, Transport), un módulo funciones\_puras.py con 5 funciones (conversión C→F, detección de umbral, validación de rango, serialización a texto y comparación entre lecturas), y sus tests en test\_funciones\_puras.py.
* Decisión: Acepté las 5 funciones tal cual, los 6 tests pasaron a la primera corrida (pytest) y mypy no encontró errores de tipos. Sin embargo, ruff detectó que en funciones\_puras.py había un import sin usar (SensorType, importado pero nunca referenciado directamente en el archivo). Lo corregí eliminando ese import de la línea 6. No fue un error grave, pero muestra que hay que revisar el código generado en vez de asumir que todo lo que trae es necesario.



##### Fecha: 14/07/2026 (Día 2 · Martes)

* Prompt: "Ayúdame a hacer la actividad del día 2: reimplementar una FSM de semáforo en estilo orientado a objetos (TrafficLightFSM con estado interno y método transition), y escribir 4 tests: estado inicial, transición RED→GREEN, ciclo completo de vuelta a RED, y conteo de ciclos."
* Qué produjo la IA: semana1/fsm\_demo.py con TrafficLightState (Enum) y TrafficLightFSM (propiedades state y cycle\_count, método transition), y semana1/test\_fsm.py con los 4 tests pedidos.
* Decisión: Acepté la lógica de la FSM y los 4 tests tal cual, pasaron a la primera corrida. Pero ruff marcó el Enum (RED = auto(); YELLOW = auto(); GREEN = auto()) como mala práctica por tener múltiples statements en una sola línea con punto y coma — lo separé en tres líneas independientes. También noté que el código original no exponía \_cycle\_count hacia afuera, así que agregué una propiedad cycle\_count para poder verificarlo desde los tests.

