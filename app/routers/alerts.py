from typing import Annotated

from fastapi import APIRouter, Depends, Query

from app.dependencies import get_alert_repository
from app.repositories.alert_repository import AlertRepository
from app.schemas.alert import AlertOut

router = APIRouter() 
RepoDep = Annotated[AlertRepository, Depends(get_alert_repository)] 
@router.get("/sensors/{sensor_id}/alerts", response_model=list[AlertOut]) 
def list_alerts( 
    sensor_id: str, 
    repo: RepoDep, 
    limit: int = Query(default=50, ge=1, le=500), 
    offset: int = Query(default=0, ge=0), 
) -> list[AlertOut]: 
    alertas = repo.list_for_sensor(sensor_id, limit, offset) 
    return [AlertOut.model_validate(a) for a in alertas] 
