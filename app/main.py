from fastapi import FastAPI

from app.routers import readings

app = FastAPI(title="SensorHub API", version="0.2.0")

app.include_router(readings.router)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
