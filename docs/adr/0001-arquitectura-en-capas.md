# ADR 0001: Arquitectura en capas para SensorHub 
 
## Estado 
Aceptado 
 
## Contexto 
SensorHub necesitaba poder cambiar de base de datos (de SQLite local a PostgreSQL en produccion) y probar la logica de negocio sin depender de infraestructura real. Tambien necesitabamos que la validacion fisica de las lecturas dependiera del tipo de sensor realmente registrado, no de un valor fijo pasado a mano. 
 
## Decision 
Organizamos el codigo en 4 capas: routers -> services -> repositories -> models. Los repositorios se definen primero como Protocol (SensorRepository, ReadingRepository) y despues se implementan con SQLAlchemy (SQLAlchemySensorRepository), aplicando DIP: los services dependen de la abstraccion, no de la implementacion concreta. 
 
## Consecuencias 
+ Se pueden testear los services con un repositorio falso (fake), sin necesitar base de datos real, como ya hacemos con SQLite en memoria en los tests. 
+ Cambiar de SQLite a PostgreSQL (como hicimos en la semana 4) no toco nada de la logica de negocio en services ni en routers, solo la implementacion del repositorio y la configuracion de conexion. 
+ Agregar validacion fisica dependiente del tipo de sensor fue posible sin romper nada, porque ReadingService ya recibia SensorRepository como dependencia explicita. 
- Mas archivos y algo mas de ceremonia para features pequenas: agregar un campo simple implica tocar el modelo, el schema, el repositorio y el service. 
- Curva de aprendizaje mayor al inicio del proyecto comparado con poner todo en un solo archivo. 
