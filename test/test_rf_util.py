import pytest
import UnitConverter.rf_util as rf_util

@pytest.mark.parametrize("beamwidth, eut_height, expected",
                         [(11.4, 0.3, pytest.approx(1.50, rel=1e-2)),
                          (30, 10, pytest.approx(18.66, rel=1e-2)),])
def test_antenna_eut_distance(beamwidth, eut_height, expected):
    assert rf_util.antenna_eut_distance(beamwidth, eut_height) == expected