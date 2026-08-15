import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db import Base
from app.exceptions import SensorAlreadyExistsError
from app.repositories.sqlalchemy_sensor_repository import SQLAlchemySensorRepository


@pytest.fixture 
def db_session(): 
    engine = create_engine("sqlite:///:memory:") 
    Base.metadata.create_all(engine) 
    session_factory = sessionmaker(bind=engine) 
    session = session_factory() 
    yield session 
    session.close() 
 
 
def test_add_duplicate_sensor_id_raises_domain_error(db_session): 
    repo = SQLAlchemySensorRepository(db_session) 
    repo.add(sensor_id="TEMP-01", sensor_type="temperature") 
    with pytest.raises(SensorAlreadyExistsError): 
        repo.add(sensor_id="TEMP-01", sensor_type="humidity") 
 
 
def test_list_with_zero_limit_returns_at_least_one(db_session): 
    repo = SQLAlchemySensorRepository(db_session) 
    repo.add(sensor_id="TEMP-01", sensor_type="temperature") 
    result = repo.list(limit=0) 
    assert len(result) == 1 
 
 
def test_list_with_huge_limit_is_capped_at_500(db_session): 
    repo = SQLAlchemySensorRepository(db_session) 
    repo.add(sensor_id="TEMP-01", sensor_type="temperature") 
    result = repo.list(limit=999999) 
    assert len(result) == 1 
 
 
def test_list_with_negative_offset_is_clamped_to_zero(db_session): 
    repo = SQLAlchemySensorRepository(db_session) 
    repo.add(sensor_id="TEMP-01", sensor_type="temperature") 
    result = repo.list(offset=-10) 
    assert len(result) == 1 
 
 
def test_deactivate_twice_returns_false_second_time(db_session): 
    repo = SQLAlchemySensorRepository(db_session) 
    repo.add(sensor_id="TEMP-01", sensor_type="temperature") 
    assert repo.deactivate("TEMP-01") is True 
    assert repo.deactivate("TEMP-01") is False 
