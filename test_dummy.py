"""test module"""

def test_dummy() -> None:
    """dummy test"""
    assert True


def test_dummy2() -> None:
    "assert test"
    try:
        assert False
    except AssertionError:
        pass
