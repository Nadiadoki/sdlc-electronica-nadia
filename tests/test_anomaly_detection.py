 
from app.strategies import AnomalyDetector, ThresholdExceededStrategy


def test_threshold_exceeded_strategy_triggers_when_value_above_threshold(): 
    strategy = ThresholdExceededStrategy() 
    assert strategy.evaluate(value=50.0, threshold=40.0) is True 
 
 
def test_threshold_exceeded_strategy_does_not_trigger_when_value_at_or_below_threshold(): 
    strategy = ThresholdExceededStrategy() 
    assert strategy.evaluate(value=40.0, threshold=40.0) is False 
    assert strategy.evaluate(value=30.0, threshold=40.0) is False 
 
 
def test_anomaly_detector_uses_injected_strategy(): 
    detector = AnomalyDetector(strategy=ThresholdExceededStrategy()) 
    assert detector.is_anomaly(value=99.0, threshold=10.0) is True 
    assert detector.is_anomaly(value=5.0, threshold=10.0) is False 
