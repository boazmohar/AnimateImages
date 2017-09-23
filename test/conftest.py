import pytest
import matplotlib.pyplot as plt


@pytest.yield_fixture(autouse=True)
def run_around_tests():
    yield
    plt.close('all')
