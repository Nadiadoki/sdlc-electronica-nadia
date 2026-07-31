from fastapi import FastAPI

from app.routers import readings, sensors

app = FastAPI(title="SensorHub API", version="0.3.0")

app.include_router(sensors.router)
app.include_router(readings.router)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
