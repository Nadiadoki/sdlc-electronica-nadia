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


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_crear_lectura_devuelve_201(client):
    response = client.post("/sensors/TEMP-01/readings", json={"value": 24.5, "unit": "C"})
    assert response.status_code == 201
    body = response.json()
    assert body["sensor_id"] == "TEMP-01"
    assert body["value"] == 24.5
    assert body["active"] is True


def test_crear_lectura_bajo_cero_absoluto_devuelve_422(client):
    response = client.post("/sensors/TEMP-01/readings", json={"value": -300.0, "unit": "C"})
    assert response.status_code == 422


def test_listar_lecturas_con_paginacion_devuelve_200(client):
    for valor in (20.0, 21.0, 22.0):
        client.post("/sensors/TEMP-01/readings", json={"value": valor, "unit": "C"})

    response = client.get("/sensors/TEMP-01/readings?limit=2&offset=0")
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_listar_lecturas_con_rango_de_fechas_invalido_devuelve_400(client):
    response = client.get(
        "/sensors/TEMP-01/readings?from=2026-01-02T00:00:00&to=2026-01-01T00:00:00"
    )
    assert response.status_code == 400


def test_obtener_lectura_existente_devuelve_200(client):
    creada = client.post("/sensors/TEMP-01/readings", json={"value": 24.5, "unit": "C"}).json()
    response = client.get(f"/readings/{creada['id']}")
    assert response.status_code == 200
    assert response.json()["id"] == creada["id"]


def test_obtener_lectura_inexistente_devuelve_404(client):
    response = client.get("/readings/9999")
    assert response.status_code == 404


def test_actualizar_lectura_parcialmente_devuelve_200(client):
    creada = client.post("/sensors/TEMP-01/readings", json={"value": 24.5, "unit": "C"}).json()
    response = client.patch(f"/readings/{creada['id']}", json={"value": 30.0})
    assert response.status_code == 200
    assert response.json()["value"] == 30.0
    assert response.json()["unit"] == "C"


def test_actualizar_lectura_inexistente_devuelve_404(client):
    response = client.patch("/readings/9999", json={"value": 30.0})
    assert response.status_code == 404


def test_borrar_lectura_devuelve_204(client):
    creada = client.post("/sensors/TEMP-01/readings", json={"value": 24.5, "unit": "C"}).json()
    response = client.delete(f"/readings/{creada['id']}")
    assert response.status_code == 204


def test_borrar_lectura_ya_inactiva_devuelve_409(client):
    creada = client.post("/sensors/TEMP-01/readings", json={"value": 24.5, "unit": "C"}).json()
    client.delete(f"/readings/{creada['id']}")
    response = client.delete(f"/readings/{creada['id']}")
    assert response.status_code == 409
