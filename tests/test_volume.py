import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from src.volume import Volume

@pytest.fixture
def volume_instance():
    return Volume()

def test_gain(volume_instance):
    assert volume_instance.gain(0.1, 0) == pytest.approx(1.03514216668)
    assert volume_instance.gain(0.5, 0) == pytest.approx(1.18850222744)
    assert volume_instance.gain(0.01, 0) == pytest.approx(0)
    assert volume_instance.gain(9, 0) == pytest.approx(22.3872113857)
    assert volume_instance.gain(0.01, 3) == pytest.approx(0)

def test_volume_initialization(volume_instance):
    assert volume_instance._setting == 9
    assert volume_instance._offset == 0
    assert volume_instance._volume == pytest.approx(22.3872113857)

