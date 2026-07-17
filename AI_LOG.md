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



##### Fecha: 15/07/2026 (Día 3 · Miércoles)

* Prompt: "Ayúdame con la actividad del día 3: implementar SRP, OCP y LSP con el dominio de sensores en solid\_srp\_ocp\_lsp.py, con ejemplo 'mal' y 'bien' de cada principio, más 2 tests por principio."
* Qué produjo la IA: semana1/dia3/solid\_srp\_ocp\_lsp.py con los 3 principios (SRP: SensorHandlerMal vs SensorReader/DataLogger; OCP: enviar\_alerta\_mal vs AlertStrategy/AnomalyDetector; LSP: HumiditySensorMal vs TemperatureSensor/HumiditySensor con process\_sensor), y test\_solid.py con 6 tests (2 por principio).
* Decisión: Acepté la estructura tal cual, los 16 tests pasaron y ruff no marcó nada. Pero mypy sí detectó que HumiditySensorMal.read() tenía una firma incompatible con BaseSensor (error \[override]) — que era justo el punto del ejemplo "mal" de LSP. En vez de "arreglarlo" (lo que anularía el ejemplo), agregué un comentario # type: ignore\[override] para documentar que la violación era intencional.



##### Fecha: 16/07/2026 (Día 4 · Jueves)

* Prompt: "Ayúdame con la actividad del día 4: completar SOLID con ISP y DIP en solid\_isp\_dip.py — dividir una interfaz gorda en Readable/Writable/Calibratable, y usar Protocol para que DataProcessor dependa de una abstracción DataRepository."
* Qué produjo la IA: semana1/dia4/solid\_isp\_dip.py con ISP (SensorDeviceMal vs. Readable/Writable/Calibratable, usadas por SimpleSensor y AdvancedSensor) y DIP (DataProcessorMal acoplado a PostgreSQLRepositoryMal vs. DataProcessor que recibe cualquier DataRepository por inyección de dependencias), y test\_solid\_isp\_dip.py con 4 tests.
* Decisión: Acepté la estructura tal cual. Los tests, mypy y ruff pasaron sin errores a la primera. Lo que más me quedó claro fue el DIP: en el test test\_data\_processor\_no\_conoce\_implementacion\_concreta uso un repositorio inventado en el momento (OtroRepoFake) y DataProcessor funciona igual sin cambiar nada — eso es la inyección de dependencias funcionando de verdad.



##### Fecha: 17/07/2026 (Día 5 · Viernes)

* Prompt: "Ayúdame con el ejercicio integrador del día 5: reimplementar un driver UART de C (buffers globales, parsing mezclado, no testeable) en Python moderno aplicando SOLID completo, en semana1/uart\_driver/ con config.py, parsers.py, device.py, recorder.py y tests/ con al menos 3 tests por clase."
* Qué produjo la IA: UartConfig (dataclass frozen con validación), MessageParser (ABC) con ModbusParser y NMEAParser, UartDevice (recibe config y parser por inyección de dependencias) y DataRecorder (persiste como JSON-lines), más 13 tests en tests/ (incluyendo un conftest.py para que los tests puedan importar los módulos desde la subcarpeta).
* Decisión: Acepté la estructura completa. Los 33 tests de la semana pasaron, mypy no encontró errores en los 4 módulos y ruff no marcó nada. Lo que más valoro de este diseño es que UartDevice no conoce ningún puerto real: en los tests uso un FakePort inventado, y en producción sería un puerto serial de verdad — el driver original en C no permitía esto porque todo dependía de buffers globales.

