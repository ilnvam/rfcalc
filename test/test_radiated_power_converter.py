import pytest
from UnitConverter.eirp_converter import EIRP, EIRPConverter

@pytest.fixture
def rf():
    return EIRPConverter()

@pytest.mark.parametrize("value, unit_in, unit_out, kwargs, expected", [

    # Convert from available unit to EIRP in dBm
    (1000, EIRP.EIRP_mW, EIRP.EIRP_dBm, {}, 30.0),
    (30, EIRP.ERP_dBm, EIRP.EIRP_dBm, {}, 32.15),
    (10, EIRP.ERP_mW, EIRP.EIRP_dBm, {}, pytest.approx(12.15, rel=1e-2)),
    (60, EIRP.dbuv_per_m, EIRP.EIRP_dBm, {'distance':3.0, 'slope': 20.0}, pytest.approx(-35.23, rel=1e-2)),
    (60, EIRP.dbuv_per_m, EIRP.EIRP_dBm, {'distance':10.0, 'slope': 20.0}, pytest.approx(-24.77, rel=1e-2)),
    (87, EIRP.dbuv, EIRP.EIRP_dBm, {}, -20),

    #EIRP in dBm to other unit
    (30, EIRP.EIRP_dBm, EIRP.EIRP_mW, {}, pytest.approx(1000, rel=1e-2)),
    (30, EIRP.EIRP_dBm, EIRP.ERP_dBm, {}, pytest.approx(27.85, rel=1e-2)),
    (30, EIRP.EIRP_dBm, EIRP.ERP_mW, {}, pytest.approx(609.54, rel=1e-2)),
    (30, EIRP.EIRP_dBm, EIRP.dbuv_per_m, {'distance': 3.0, 'slope': 20.0}, pytest.approx(125.26, rel=1e-2)),
    (30, EIRP.EIRP_dBm, EIRP.dbuv_per_m, {'distance': 10.0, 'slope': 20.0}, pytest.approx(114.8, rel=1e-2)),
    (30, EIRP.EIRP_dBm, EIRP.dbuv, {}, pytest.approx(137.0, rel=1e-2)),
    (30, EIRP.EIRP_dBm, EIRP.W_m_sq, {'distance': 0.2}, pytest.approx(1.99, rel=1e-2)),
])

def test_eirp_conversions(rf, value, unit_in, unit_out, kwargs, expected):
    result = rf.convert(value, unit_in, unit_out, **kwargs)
    assert result == expected
