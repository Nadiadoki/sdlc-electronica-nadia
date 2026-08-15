# Code Review con IA - SQLAlchemySensorRepository

Archivo revisado: app/repositories/sqlalchemy_sensor_repository.py

## Hallazgo 1 (seguridad/confiabilidad) - CORREGIDO
add() no manejaba sensor_id duplicado: SQLAlchemy lanza IntegrityError sin capturar por el unique=True del modelo, exponiendo un error crudo de base de datos hasta el cliente. Ya existia SensorAlreadyExistsError en exceptions.py pero no se usaba aqui.
Correccion: capturar IntegrityError, hacer rollback, y lanzar SensorAlreadyExistsError.

## Hallazgo 2 (rendimiento) - CORREGIDO
list(limit, offset) no validaba valores: un limit gigante o un offset negativo podia forzar consultas costosas o comportamiento raro en SQL.
Correccion: limite maximo de 500 y minimo de 0 para offset.

## Hallazgo 3 (SOLID) - RECHAZADO
Propuesta: validar sensor_type dentro de update().
Justificacion del rechazo: ya se valida en la capa de arriba con el Literal de Pydantic en SensorUpdate (app/schemas/sensor.py). Duplicar la validacion en el repositorio viola SRP (el repositorio solo deberia persistir, no validar reglas de negocio) y es codigo redundante, porque nada mas en el proyecto llama a este repositorio sin pasar antes por el schema.

## Hallazgo 4 (acoplamiento) - RECHAZADO POR AHORA
Propuesta: mover el manejo de transacciones (commit) fuera del repositorio a un patron Unit of Work, para permitir operaciones atomicas entre varios repositorios.
Justificacion del rechazo: critica arquitectonica valida, pero corregirla implica refactorizar todos los services y tests que dependen del comportamiento actual (93 porciento de cobertura). Fuera del alcance de este checkpoint. Queda documentado como mejora futura.
