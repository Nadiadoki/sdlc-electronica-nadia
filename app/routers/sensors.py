from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.dependencies import get_sensor_service
from app.exceptions import SensorAlreadyExistsError, SensorAlreadyInactiveError, SensorNotFoundError
from app.schemas.sensor import SensorCreate, SensorOut, SensorUpdate
from app.services.sensor_service import SensorService

router = APIRouter()

ServiceDep = Annotated[SensorService, Depends(get_sensor_service)]


@router.get("/sensors", response_model=list[SensorOut])
def list_sensors(
    service: ServiceDep,
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
) -> list[SensorOut]:
    return [SensorOut.model_validate(s) for s in service.list(limit, offset)]


@router.post("/sensors", response_model=SensorOut, status_code=status.HTTP_201_CREATED)
def create_sensor(body: SensorCreate, service: ServiceDep) -> SensorOut:
    try:
        sensor = service.create(body.sensor_id, body.sensor_type)
    except SensorAlreadyExistsError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_CONTENT, detail=str(exc)
        ) from exc
    return SensorOut.model_validate(sensor)


@router.get("/sensors/{sensor_id}", response_model=SensorOut)
def get_sensor(sensor_id: str, service: ServiceDep) -> SensorOut:
    try:
        sensor = service.get(sensor_id)
    except SensorNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    return SensorOut.model_validate(sensor)


@router.patch("/sensors/{sensor_id}", response_model=SensorOut)
def update_sensor(sensor_id: str, body: SensorUpdate, service: ServiceDep) -> SensorOut:
    try:
        sensor = service.update(sensor_id, sensor_type=body.sensor_type)
    except SensorNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_CONTENT, detail=str(exc)
        ) from exc
    return SensorOut.model_validate(sensor)


@router.delete("/sensors/{sensor_id}", status_code=status.HTTP_204_NO_CONTENT)
def deactivate_sensor(sensor_id: str, service: ServiceDep) -> None:
    try:
        service.deactivate(sensor_id)
    except SensorNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except SensorAlreadyInactiveError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc
