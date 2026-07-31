from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.dependencies import get_reading_service
from app.exceptions import ReadingAlreadyInactiveError, ReadingNotFoundError, SensorNotFoundError
from app.schemas.reading import ReadingCreate, ReadingOut, ReadingUpdate
from app.services.reading_service import ReadingService

router = APIRouter()

ServiceDep = Annotated[ReadingService, Depends(get_reading_service)]


@router.get("/sensors/{sensor_id}/readings", response_model=list[ReadingOut])
def list_readings(
    sensor_id: str,
    service: ServiceDep,
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    from_: datetime | None = Query(default=None, alias="from"),  # noqa: B008
    to: datetime | None = Query(default=None),  # noqa: B008
) -> list[ReadingOut]:
    try:
        lecturas = service.list_for_sensor(sensor_id, limit, offset, from_, to)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    return [ReadingOut.model_validate(r) for r in lecturas]


@router.post(
    "/sensors/{sensor_id}/readings", response_model=ReadingOut, status_code=status.HTTP_201_CREATED
)
def create_reading(sensor_id: str, body: ReadingCreate, service: ServiceDep) -> ReadingOut:
    try:
        reading = service.record(sensor_id=sensor_id, value=body.value, unit=body.unit)
    except SensorNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(exc)
        ) from exc
    return ReadingOut.model_validate(reading)


@router.get("/readings/{reading_id}", response_model=ReadingOut)
def get_reading(reading_id: int, service: ServiceDep) -> ReadingOut:
    try:
        reading = service.get_reading(reading_id)
    except ReadingNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    return ReadingOut.model_validate(reading)


@router.patch("/readings/{reading_id}", response_model=ReadingOut)
def update_reading(reading_id: int, body: ReadingUpdate, service: ServiceDep) -> ReadingOut:
    try:
        reading = service.update_reading(reading_id, value=body.value, unit=body.unit)
    except ReadingNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except SensorNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(exc)
        ) from exc
    return ReadingOut.model_validate(reading)


@router.delete("/readings/{reading_id}", status_code=status.HTTP_204_NO_CONTENT)
def deactivate_reading(reading_id: int, service: ServiceDep) -> None:
    try:
        service.deactivate_reading(reading_id)
    except ReadingNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except ReadingAlreadyInactiveError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc
