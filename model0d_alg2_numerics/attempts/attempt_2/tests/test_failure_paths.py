from src.sunsun_algorithm2 import _primary


def test_failure_precedence_is_deterministic():
    causes = ['MAX_OUTER_ITERATIONS', 'TCC_NOT_ACCEPTED', 'PHYSICAL_VIOLATION_DETECTED']
    assert _primary(causes) == 'PHYSICAL_VIOLATION_DETECTED'
