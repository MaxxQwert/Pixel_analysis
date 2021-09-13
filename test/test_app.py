import pytest
from app import color_check


@pytest.fixture(scope="function", params=[
    ('testcolor1.bmp', '#ff00ff', (7100, 2000, 900)),
    ('testcolor2.bmp', '#00ff00', (2000, 7100, 900))
])
def param_test(request):
    return request.param


def test_color_check(param_test):
    (file, color, check) = param_test
    assert color_check(file, color) == check
