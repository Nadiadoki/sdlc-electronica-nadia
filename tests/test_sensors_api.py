import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.db import Base
from app.dependencies import get_db
from app.main import app


@pytest.fixture()
def client():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestingSessionLocal = sessionmaker(bind=engine, expire_on_commit=False)
    Base.metadata.create_all(engine)

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


def test_crear_sensor_devuelve_201(client):
    response = client.post("/sensors", json={"sensor_id": "TEMP-01", "sensor_type": "temperature"})
    assert response.status_code == 201
    body = response.json()
    assert body["sensor_id"] == "TEMP-01"
    assert body["sensor_type"] == "temperature"
    assert body["active"] is True


def test_crear_sensor_duplicado_devuelve_409(client):
    client.post("/sensors", json={"sensor_id": "TEMP-01", "sensor_type": "temperature"})
    response = client.post("/sensors", json={"sensor_id": "TEMP-01", "sensor_type": "temperature"})
    assert response.status_code == 409


def test_crear_sensor_con_tipo_invalido_devuelve_422(client):
    response = client.post("/sensors", json={"sensor_id": "PRES-01", "sensor_type": "pressure"})
    assert response.status_code == 422


def test_listar_sensores_devuelve_200(client):
    client.post("/sensors", json={"sensor_id": "TEMP-01", "sensor_type": "temperature"})
    client.post("/sensors", json={"sensor_id": "HUM-01", "sensor_type": "humidity"})
    response = client.get("/sensors")
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_obtener_sensor_existente_devuelve_200(client):
    client.post("/sensors", json={"sensor_id": "TEMP-01", "sensor_type": "temperature"})
    response = client.get("/sensors/TEMP-01")
    assert response.status_code == 200
    assert response.json()["sensor_id"] == "TEMP-01"


def test_obtener_sensor_inexistente_devuelve_404(client):
    response = client.get("/sensors/GHOST-99")
    assert response.status_code == 404


def test_actualizar_sensor_devuelve_200(client):
    client.post("/sensors", json={"sensor_id": "TEMP-01", "sensor_type": "temperature"})
    response = client.patch("/sensors/TEMP-01", json={"sensor_type": "humidity"})
    assert response.status_code == 200
    assert response.json()["sensor_type"] == "humidity"


def test_actualizar_sensor_inexistente_devuelve_404(client):
    response = client.patch("/sensors/GHOST-99", json={"sensor_type": "humidity"})
    assert response.status_code == 404


def test_borrar_sensor_devuelve_204(client):
    client.post("/sensors", json={"sensor_id": "TEMP-01", "sensor_type": "temperature"})
    response = client.delete("/sensors/TEMP-01")
    assert response.status_code == 204


def test_borrar_sensor_ya_inactivo_devuelve_409(client):
    client.post("/sensors", json={"sensor_id": "TEMP-01", "sensor_type": "temperature"})
    client.delete("/sensors/TEMP-01")
    response = client.delete("/sensors/TEMP-01")
    assert response.status_code == 409
