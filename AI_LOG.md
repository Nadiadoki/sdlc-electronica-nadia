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

##### 

##### Fecha: 18/07/2026 (Día 6 · Sábado — cierre de sesión)





## Semana 2

##### Fecha: 21/07/2026 (Semana 2 · Día 2 · Martes)

\*Prompt: "Ayúdame con el ejercicio del día 2: escribir el Product Backlog como user stories con escenarios Gherkin y story points Fibonacci en semana2/backlog.md, y después úsate como crítica auditando cada historia: ¿es verificable? ¿es ambigua? ¿qué caso borde falta?"

\*Qué produjo la IA: semana2/dia2/backlog.md con 5 historias de usuario (registrar lectura, consultar historial, configurar umbral, notificación por umbral, soporte multi-protocolo Modbus/NMEA), cada una con escenarios Gherkin y story points. Después, una auditoría crítica de las 5 historias.

\*Decisión: Acepté las 5 historias tal cual para el backlog. La auditoría fue el episodio más valioso: la IA detectó que varias historias (US-01, US-03, US-04) asumían reglas de negocio nunca definidas — por ejemplo, qué rango de valores es físicamente válido para un sensor, si configurar un umbral también cubre actualizarlo, y si "superar" un umbral es > o >=. No modifiqué el backlog todavía (decidí dejarlo así por ahora y documentar los huecos encontrados), pero esto muestra que Gherkin bien auditado expone ambigüedades de negocio que no se ven a simple vista al escribir la historia.

* Prompt: "Ayúdame a hacer el cierre del día 6: correr cobertura, ruff, mypy y revisar el historial de commits."
* Qué produjo la IA: Los comandos exactos a correr (pytest --cov, ruff check, mypy --ignore-missing-imports, git log --oneline) y ayuda para armar la nota de entrega con el mapeo de rutas del portafolio.
* Decisión: No hubo código nuevo que aceptar o rechazar hoy — fue verificación. Resultados: 95% de cobertura, ruff limpio, mypy sin errores en 18 archivos, 9 commits descriptivos. Todo pasó sin necesidad de ajustes.

##### 

##### Fecha: 22/07/2026 (Semana 2 · Día 3 · Miércoles)



* Prompt: "Guíame paso a paso en TDD estricto para implementar SensorRegistry: cada commit de test debe preceder al commit del código, siguiendo el ciclo RED-GREEN-REFACTOR."
* Qué produjo la IA: El código para 3 ciclos completos de TDD (verificar sensor inexistente, registrar y recuperar una lectura, validar que el sensor\_id no esté vacío) y el refactor final que extrae la validación a un método privado.
* Decisión: Seguí el flujo tal cual, con una corrección propia en el camino: al escribir record() a mano dejé mal la indentación (quedó fuera de la clase) y pytest lo detectó de inmediato como IndentationError. Tuve que reescribir el archivo completo para corregirlo. Fue un buen recordatorio de que en TDD el test no solo verifica la lógica — también atrapa errores básicos de sintaxis antes de que lleguen a producción.

##### 

##### Fecha: 23/07/2026 (Semana 2 · Día 4 · Jueves)



* Prompt: "Ayúdame con el día 4: escribir la Definition of Done en Gherkin, configurar pyproject.toml con ruff/pytest-cov/mypy estrictos, y trabajar con ramas y PR."
* Qué produjo la IA: DEFINITION\_OF\_DONE.md con 5 escenarios Gherkin, pyproject.toml con reglas de ruff, cobertura ≥80% y mypy con disallow\_untyped\_defs, y el flujo completo de rama + PR + merge.
* Decisión: Al activar disallow\_untyped\_defs, mypy marcó 33 errores en todos mis archivos de test. Decidí no anotar cada función de test a mano (no es práctica común exigir tipos tan estrictos en tests) y en su lugar configuré una exclusión. El primer intento con module = "test\_\*" falló porque mypy no acepta asteriscos parciales en nombres de módulo; funcionó al cambiar a exclude con una expresión regular sobre la ruta del archivo ('(^|/)test\_.\*\\.py$'). También tuve que corregir una sección \[tool.mypy] duplicada en el archivo. Al final: mypy limpio en 10 archivos de código real, tests sin exigencia de tipos.



##### 

##### Fecha: 25/07/2026 (Semana 2 · Día 5/Sábado · Evaluación 1)



* Prompt 1: "Ayúdame a construir el Product Backlog y el Sprint 1 Planning para el sistema de monitoreo IoT, con 10+ historias en Gherkin, MoSCoW y tareas ≤4h."

Qué produjo la IA: 13 historias con Gherkin y story points, priorizadas MoSCoW, y la selección justificada de las 6 Must para el Sprint 1 con su desglose en tareas.

Decisión: Acepté la estructura completa. Antes de avanzar, la leí con calma para poder justificar cada priorización si me preguntan en la sesión de evaluación.

* Prompt 2: "Guíame en TDD estricto (Red→Green) para implementar SensorReading, AnomalyDetector con umbral inyectado, y AlertManager con estrategia abstracta."

Qué produjo la IA: El código de cada ciclo, paso a paso, exigiendo confirmar el fallo (RED) antes de dar la implementación (GREEN).

Decisión: Seguí el flujo completo, con dos correcciones propias en el camino: un test que terminó pegado por error dentro de alerts.py (lo tuve que mover a su archivo correcto), y un ajuste de tipos en AlertManager que pedía mypy. Ambos quedan documentados en la Retrospective.

* Prompt 3: "Escribe la Sprint Retrospective con hallazgos reales de esta sesión, no genéricos."

Qué produjo la IA: Una retrospectiva que documenta específicamente los errores de esta sesión (código en archivo equivocado, ajuste de configuración de mypy) con una acción concreta para el próximo sprint.

Decisión: La acepté tal cual — preferí que reflejara los tropiezos reales en vez de una retrospectiva "bonita" sin sustancia, ya que la rúbrica valora el uso reflexivo de la IA, no solo el resultado final.



### Semana 3

##### Fecha: 27/07/2026 (Semana 3 · Día 1 · Lunes)



* Prompt: "Ayúdame con el día 1 de la semana 3: crear app/main.py con FastAPI, endpoints /health y POST /readings, y requirements.txt curado."
* Qué produjo la IA: app/main.py con SensorReadingIn/SensorReadingOut (Pydantic) y los dos endpoints, más requirements.txt con las 10 dependencias específicas del proyecto.
* Decisión: Acepté el código tal cual, lo probé en Swagger (/docs) y ambos endpoints funcionaron a la primera. Este día marcó el cambio de trabajar por carpetas de semana a trabajar directamente sobre el producto (app/) en la raíz del repo.

##### 

##### Fecha: 29/07/2026 (Semana 3 · Día 2 · Martes)

* Prompt: "Ayúdame con el día 2: crear app/db.py con SQLAlchemy 2.x (API tipada con Mapped), replicando el Quick Start pero con mi modelo ReadingModel."
* Qué produjo la IA: app/db.py con engine, SessionLocal, Base(DeclarativeBase) y ReadingModel (tabla readings con id, sensor\_id indexado, value, unit, created\_at).
* Decisión: Acepté el código tal cual y lo verifiqué creando las tablas con Base.metadata.create\_all(engine) — se generó correctamente sensorhub.db. Presté atención especial a usar Mapped\[...] en vez de la sintaxis vieja Column(...) de SQLAlchemy 1.x, como advertía la guía sobre tutoriales desactualizados.



##### Fecha: 29/07/2026 (Semana 3 · Día 3 · Miércoles)



* Prompt: "Ayúdame con el día 3: crear el patrón repositorio (ReadingRepository como Protocol) y ReadingService, y escribir tests con un repositorio fake en memoria sin base de datos real."
* Qué produjo la IA: app/repositories/reading\_repository.py (Protocol), app/services/reading\_service.py (lógica de negocio dependiente de la abstracción), y 3 tests con un FakeReadingRepository definido dentro del propio archivo de test.
* Decisión: Acepté el diseño tal cual — es exactamente el mismo patrón DIP que ya había practicado en la semana 1 con DataProcessor/InMemoryRepository, así que reconocí la estructura de inmediato y pude verificar que el fake cumple el Protocol sin heredar de él explícitamente (duck typing de Python).



##### Fecha: 30/07/2026 (Semana 3 · Día 4 · Jueves)

* Prompt: "Ayúdame con el día 4: conectar las capas con el sistema de dependencias de FastAPI (Depends) y diseñar los 5 endpoints REST de la tabla, con paginación, filtros de fecha y códigos de error correctos."
* Qué produjo la IA: app/dependencies.py (cadena de Depends: get\_db → get\_reading\_repository → get\_reading\_service), SQLAlchemyReadingRepository (implementación real del Protocol), ReadingService ampliado con excepciones de dominio propias, y app/routers/readings.py con los 5 endpoints traduciendo esas excepciones a códigos HTTP (400/404/409/422).
* Decisión: Acepté el diseño de excepciones de dominio (ReadingNotFoundError, ReadingAlreadyInactiveError) en vez de que el servicio lance HTTPException directamente — así el servicio no depende de FastAPI, y es el router quien decide el código HTTP. Verifiqué los 11 tests de integración, todos en verde, cubriendo cada código de estado de la tabla.



##### Fecha: 31/07/2026 (Semana 3 · Día 5 · Viernes)

* Prompt: "Ayúdame con el ejercicio integrador del día 5: CRUD completo de sensores y lecturas siguiendo las convenciones REST, validación Pydantic con física real (rechazar unidades desconocidas y valores fuera de rango físico por tipo de sensor), y arquitectura en 4 capas."
* Qué produjo la IA: SensorModel nuevo en db.py, el Protocol SensorRepository + su implementación SQLAlchemy, SensorService con sus propias excepciones de dominio, el router de sensores (CRUD completo), y una reescritura de ReadingService para que la validación de unidad y rango dependa del tipo de sensor realmente registrado en la base de datos (no de un valor fijo pasado a mano). Además, 32 tests en total, con 93.47% de cobertura.
* Decisión: Acepté el diseño de que ReadingService ahora dependa también de SensorRepository (no solo de ReadingRepository), porque sin eso la validación física no tenía forma de saber si un sensor mide temperatura o humedad. Tuve que resolver 20 errores de ruff en el código nuevo: la mayoría eran imports desordenados que arregló --fix automáticamente, pero corregí a mano 2 líneas largas y un falso positivo de ruff con Query() de FastAPI en los valores por defecto (silenciado con noqa: B008, porque es el patrón oficial recomendado por FastAPI).



##### Fecha: 01/08/2026 (Semana 3 · Día 6 · Sábado)

* Prompt: "Ayúdame con la ronda de peer review: corregir los warnings de obsolescencia en una rama nueva para tener algo real que revisar, abrir el PR con descripción clara, revisar el PR de mi compañero con la checklist (2 observaciones específicas + 1 pregunta), y responder las preguntas que me hizo sobre mi código."
* Qué produjo la IA: La corrección de datetime.utcnow() → datetime.now(UTC) y HTTP\_422\_UNPROCESSABLE\_ENTITY → HTTP\_422\_UNPROCESSABLE\_CONTENT en una rama fix/deprecation-warnings; ayuda para redactar las observaciones al PR de Antonio (nota de trabajo pegada por accidente en el README, archivo .txt con contenido Markdown mal ubicado) y para responder sus 3 preguntas técnicas sobre mi código (Protocol/DIP con repositorios fake, el order\_by explícito antes de paginar, y el borrado lógico en deactivate\_reading).
* Decisión: Acepté las correcciones de warnings tal cual, verificado con pytest (bajó de 29 a 1 warning, la única restante ajena a mi código). Para las respuestas a Antonio, no usé texto genérico: expliqué el porqué real de cada decisión de diseño (ej. el order\_by lo agregué a propósito por consistencia en la paginación, no como parche de un bug encontrado después). Este ejercicio de defender decisiones ante preguntas externas fue el punto central del día — no bastaba con que el código funcionara, tenía que poder justificarlo.



#### Semana 4

##### Fecha: 10/08/2026 (Semana 4 · Día 1 · Lunes)



* Prompt: "Ayúdame a realizar la actividad del día lunes: contenerizar mi app con Docker desde cero, siguiendo la escalera de la semana (app local → corre en Docker)."
* Qué produjo la IA: Un Dockerfile de 7 líneas para la app FastAPI (imagen base python:3.12-slim, WORKDIR /app, copia de requirements.txt e instalación de dependencias antes de copiar el resto del código para aprovechar la cache de capas de Docker, EXPOSE 8000 y CMD apuntando a uvicorn app.main:app). Además, guía paso a paso para instalar Docker Desktop y WSL2 (no los tenía instalados), y para diagnosticar y corregir dos problemas de entorno específicos de Windows/CMD.
* Decisión: Tuve que resolver tres problemas de entorno antes de poder construir la imagen: (1) el Bloc de notas guardó el archivo como Dockerfile.txt en vez de Dockerfile, lo renombré con ren; (2) al pegar el contenido en Notepad todas las instrucciones quedaron en una sola línea, lo cual invalida el Dockerfile (FROM requires either one or three arguments) — lo resolví recreando el archivo línea por línea desde la terminal con una serie de comandos echo ... >> Dockerfile, evitando el pegado múltiple; (3) después de instalar Docker Desktop y WSL, el comando docker seguía sin reconocerse porque la ventana de CMD tenía cargado el PATH de antes de la instalación — se resolvió abriendo una terminal nueva. Con eso, docker build corrió limpio (11/11 pasos) y docker run -p 8000:8000 sirvió correctamente en /health, confirmando que la app funciona igual dentro del contenedor que corriendo local con uvicorn.



##### Fecha: 11/08/2026 (Semana 4 · Día 2 · Martes)

* Prompt: "Ayúdame a hacer la actividad del día martes: Docker Compose + PostgreSQL."
* Qué produjo la IA: El docker-compose.yml con dos servicios (api construido desde el Dockerfile local, y db con imagen postgres:16 y volumen persistente); la línea psycopg\[binary] para requirements.txt; y la reescritura de app/db.py con una función get\_database\_url() que lee DATABASE\_URL del entorno (con SQLite como respaldo local) y normaliza los prefijos postgres:// / postgresql:// al formato postgresql+psycopg:// que necesita el driver.
* Decisión: Tuve que resolver dos problemas más de entorno en mi máquina: (1) ni pip ni alembic estaban reconocidos directo en CMD porque la carpeta Scripts de Python no está en el PATH — los resolví usando py -m pip install alembic y py -m alembic init migrations en su lugar; (2) seguí usando el método de crear archivos línea por línea con echo >> archivo en vez de Notepad, esta vez con más cuidado porque en YAML la indentación es significativa (verifiqué con type antes de continuar cada vez). Con docker compose up --build levanté ambos contenedores juntos y confirmé con docker compose ps y /health que la API quedó conectada a PostgreSQL real, no a SQLite. Dejé pendiente correr alembic revision --autogenerate y alembic upgrade head — según la guía del día, hoy solo tocaba inicializar las migraciones (alembic init migrations), y eso ya quedó hecho; configurar la URL de conexión en alembic.ini y generar la primera revisión lo dejo para retomarlo antes de la semana 6.



###### Fecha: 11/08/2026 (Semana 4 · Día 3 · Miércoles)

* Prompt: "Ayúdame con el día 3: pipeline de CI con GitHub Actions."
* Qué produjo la IA: El archivo .github/workflows/ci.yml con un job que instala dependencias, corre lint (ruff), revisión de tipos (mypy) y tests con cobertura mínima del 80%, activado en cada push y pull\_request a main.
* Decisión: El primer push del pipeline falló en el paso de Lint con 16 errores de ruff en código de semanas anteriores que nunca se había revisado con esta regla activa (14 eran imports desordenados, arreglables con --fix; los otros dos —una variable ambigua l y un import fuera de lugar— los corregí a mano). Después de ese fix, el pipeline volvió a fallar, esta vez en Tests con ModuleNotFoundError: No module named 'app': el ci.yml corría pytest directo, pero localmente yo uso python -m pytest, y esa diferencia importa porque -m agrega la raíz del proyecto a la ruta de búsqueda de módulos — sin eso, GitHub Actions no encontraba mi paquete app. Corregí la línea del workflow a python -m pytest --cov=app --cov-fail-under=80 y con eso el pipeline pasó en verde (CI #4). En total fueron 4 ejecuciones antes de tener un CI limpio, lo cual terminó siendo el ejercicio real de "romper algo a propósito" que pedía la guía, solo que sin querer.



###### Fecha: 11/08/2026 (Semana 4 · Día 4 · Jueves)

* Prompt: "Ayúdame con el día 4: despliegue continuo en Render."
* Qué produjo la IA: El archivo render.yaml con dos servicios (web sensorhub-api corriendo como Docker, y base de datos sensorhub-db, ambos en plan free, conectados automáticamente vía fromDatabase), y la actualización del Dockerfile para que el CMD corra alembic upgrade head \&\& uvicorn app.main:app antes de aceptar tráfico.
* Decisión: El primer deploy en Render falló con NoSuchModuleError / error de conexión en Alembic porque migrations/env.py seguía usando la URL de ejemplo con la que Alembic se inicializa por defecto, en vez de la URL real de PostgreSQL de producción. Lo corregí importando la misma función get\_database\_url() que ya tenía en app/db.py y forzando config.set\_main\_option("sqlalchemy.url", get\_database\_url()) al inicio de env.py — así ambos (la app y las migraciones) leen la conexión de la misma forma, sin duplicar lógica. Probé el fix local con alembic upgrade head (usó SQLite sin problema) antes de subirlo. Después de subir el commit, Render lanzó el deploy solo (Auto-Deploy detectó el push), y esta vez quedó "Live" — confirmé con /health respondiendo desde la URL pública https://sensorhub-api-n5is.onrender.com. Esto fue exactamente el riesgo de "deploy verde, API muerta porque no existe la tabla" que advertía la guía del día, solo que en mi caso ni siquiera llegó a "verde" la primera vez porque Alembic truena antes de que el servidor arranque — lo cual en retrospectiva es mejor que fallar silenciosamente después.



###### Fecha: 11/08/2026 (Semana 4 · Día 5 · Viernes — Evaluación 2)

* Prompt: "Ayúdame con el día 5: Evaluación 2, pipeline de producción."
* Qué produjo la IA: Una revisión de la rúbrica contra lo ya construido durante la semana, identificando que Dockerfile, docker-compose.yml, pipeline de CI en verde y despliegue continuo ya estaban cumplidos desde días anteriores; y el bloque final agregado al README.md con el badge del pipeline de CI y la sección de despliegue en producción (URL pública, link a /health y a /docs).
* Decisión: Antes de dar por cerrado el criterio de "seguridad de configuración", revisé el historial de git buscando la palabra secret en docker-compose.yml y render.yaml con git log --all -p, y encontré POSTGRES\_PASSWORD: secret y la URL con sensor:secret@db. Decidí que esto no es una filtración real: es una contraseña de desarrollo local que solo vive dentro de la red interna de Docker en mi propia máquina, nunca sale a internet ni se usa en producción — la base de datos real de Render usa una contraseña generada por el proveedor que llega a mi app vía fromDatabase en render.yaml, sin quedar escrita en ningún archivo del repo. Con eso confirmé que sí cumplo el criterio de "configuración por variables de entorno" tal como lo pide la rúbrica, sin necesidad de rotar ni limpiar nada del historial.





##### semana 5

###### Fecha: 15/08/2026 (Semana 5 · Día 2 · Martes)

* Prompt: "Ayúdame con el día 2: Aider, IA con trazabilidad Git."
* Qué produjo la IA: Guía para instalar Aider (pip install aider-install \&\& aider-install), y como se detectó que Aider requiere una API key de pago de un proveedor externo (OpenAI, Anthropic, etc.), guía paso a paso para instalar y usar GitHub Copilot Chat en VS Code por primera vez como alternativa contemplada en la propia guía. Con Copilot Chat generé la función fahrenheit\_to\_celsius(f: float) -> float en semana5/conversions.py, con el mismo estilo que celsius\_to\_fahrenheit.
* Decisión: Decidí no crear una cuenta de pago solo para probar Aider en este ejercicio, y documenté el intento real en semana5/aider.md: sí logré instalarlo (versión 0.86.2, resolviendo en el camino que aider-install es un ejecutable y no un módulo de Python, y que hacía falta abrir una terminal nueva para que reconociera el comando por el PATH), pero me detuve justo antes de necesitar la API key. Completé el ejercicio equivalente con Copilot Chat, que nunca había usado antes. La diferencia clave que documenté: Aider hace commit automático y separado por cada cambio que hace la IA, dejando un git log donde se distingue con precisión qué hizo la IA de qué hice yo; con Copilot Chat el cambio queda mezclado en mi propio commit manual, sin esa separación automática — la trazabilidad ahí depende de que yo la documente a mano, como en este mismo registro.



###### Fecha: 14/08/2026 (Semana 5 · Día 3 · Miércoles)

* Prompt: "Ayúdame con el día 3: code review y tests con IA."
* Qué produjo la IA: Un code review completo de SQLAlchemySensorRepository con 4 hallazgos: (1) add() no manejaba sensor\_id duplicado, dejando escapar un IntegrityError crudo de SQLAlchemy hasta el cliente; (2) list() no validaba limit/offset, permitiendo consultas costosas o comportamiento indebido con valores extremos; (3) propuesta de validar sensor\_type dentro de update(); (4) propuesta de mover el manejo de transacciones fuera del repositorio (patrón Unit of Work).
* Decisión: Implementé las correcciones 1 y 2 (captura de IntegrityError con rollback y re-lanzamiento como SensorAlreadyExistsError; límites seguros de limit máximo 500 y offset mínimo 0 en list()), y rechacé las propuestas 3 y 4 con justificación por escrito en AI\_CODE\_REVIEW.md: la validación de sensor\_type ya ocurre en la capa de schemas de Pydantic antes de llegar al repositorio, así que duplicarla ahí violaría SRP sin beneficio real; y el patrón Unit of Work es una mejora arquitectónica válida pero fuera del alcance de este checkpoint, dado que tocaría todos los services y el 93% de cobertura existente — quedó documentado como mejora futura, no aplicado. Agregué 5 tests nuevos cubriendo los casos borde (duplicado, límites de list(), doble desactivación), y terminé con 89 tests pasando y 100% de cobertura en el archivo revisado. La parte más pesada del día no fue el código en sí sino pelear con la terminal de Windows: varios símbolos especiales (>, <, |, y hasta un 2 pegado a un >> que CMD interpretó como redirección de errores) rompieron los comandos echo repetidamente, obligándome a reconstruir el archivo del repositorio en bloques pequeños y verificar cada uno con type antes de seguir.



###### Fecha: 15/08/2026 (Semana 5 · Día 4 · Jueves)

* Prompt: "Ayúdame con el día 4: documentación asistida y mi primer ADR."
* Qué produjo la IA: El ADR docs/adr/0001-arquitectura-en-capas.md, adaptado con contexto y consecuencias reales de mi proyecto SensorHub (no el texto genérico del ejemplo de la guía): la razón real de organizar el código en 4 capas (routers → services → repositories → models) con Protocol para aplicar DIP, y consecuencias concretas que ya viví — el cambio de SQLite a PostgreSQL en la semana 4 sin tocar lógica de negocio, y la validación física dependiente del tipo de sensor sin romper nada porque ReadingService ya dependía de SensorRepository como abstracción.
* Decisión: Decidí no usar el ejemplo genérico de la guía tal cual, y en su lugar documentar decisiones y consecuencias que efectivamente ocurrieron en mi propio código durante el curso, citando los cambios reales de semanas anteriores como evidencia de las ventajas y desventajas de la arquitectura en capas, en vez de inventar ejemplos hipotéticos.



###### Fecha: 15/08/2026 (Semana 5 · Día 5 · Viernes — Ejercicio integrador)

* Prompt: "Ayúdame con el ejercicio integrador del día 5: detección y notificación de anomalías, con TDD estricto y estrategia de alerta intercambiable."
* Qué produjo la IA: La feature completa de detección de anomalías, integrada de punta a punta: AlertStrategy (Protocol) y ThresholdExceededStrategy como implementación intercambiable (OCP), AnomalyDetector como orquestador puro sin dependencias de base de datos; el campo alert\_threshold en SensorModel y la tabla nueva AlertModel, con su migración de Alembic generada por --autogenerate; AlertRepository (protocolo + implementación SQLAlchemy); la integración en ReadingService.record() para que cada lectura nueva se evalúe automáticamente contra el umbral del sensor y, si lo supera, se persista una alerta; y el endpoint GET /sensors/{sensor\_id}/alerts.
* Decisión: Seguí TDD estricto para la parte pura (AlertStrategy/AnomalyDetector): primero el test que falla por ModuleNotFoundError, después el código mínimo que lo hace pasar, sin necesitar refactor por lo simple del resultado. Para la integración con ReadingService, decidí que alert\_repo y detector fueran parámetros opcionales con default None en vez de obligatorios, precisamente para no romper ninguno de los tests existentes que ya instanciaban ReadingService con solo dos argumentos — así la feature nueva es aditiva, no invasiva. Tuve que corregir dos problemas en migrations/env.py: primero, target\_metadata seguía en None desde que lo configuré el martes (nunca había usado --autogenerate de verdad hasta hoy), y al corregirlo con Notepad quedó con un espacio de indentación de más que rompió el import con un IndentationError. Terminé con 92 tests pasando y 91.38% de cobertura total. Construir 8 archivos nuevos y modificar 3 existentes solo con echo en CMD, sin acceso directo a editar archivos, fue la parte más lenta del día — tuve que dividir cada archivo grande en 2 o 3 bloques para evitar que la terminal cortara el pegado a la mitad.

