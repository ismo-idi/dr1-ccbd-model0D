from src.sunsun_algorithm2 import _primary
def test_failure_precedence_is_deterministic(): assert _primary(['MAX_OUTER_ITERATIONS','TCC_NOT_ACCEPTED','PHYSICAL_VIOLATION_DETECTED'])=='PHYSICAL_VIOLATION_DETECTED'
