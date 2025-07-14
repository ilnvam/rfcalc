import pytest

from UnitConverter.rf_converter import FieldStrengthConverter, FSUNIT

conv = FieldStrengthConverter()

@pytest.fixture
def con():
    return FieldStrengthConverter()

@pytest.mark.parametrize("value, unit_in, unit_out, expected", [
    # FROM other units to dBuV/m
    (10, FSUNIT.V_PER_M, FSUNIT.DBUV_PER_M, pytest.approx(140.00, rel=1e-2)),
    (10, FSUNIT.UV_PER_M, FSUNIT.DBUV_PER_M, pytest.approx(20.00, rel=1e-2)),
    (10, FSUNIT.DBUA_PER_M, FSUNIT.DBUV_PER_M, pytest.approx(61.50, rel=1e-2)),
    (10e6, FSUNIT.UA_PER_M, FSUNIT.DBUV_PER_M, pytest.approx(191.50, rel=1e-2)),
    (10, FSUNIT.A_PER_M, FSUNIT.DBUV_PER_M, pytest.approx(191.50, rel=1e-2)),
    (10, FSUNIT.DBPT, FSUNIT.DBUV_PER_M, pytest.approx(59.50, rel=1e-2)),
    (10, FSUNIT.PT, FSUNIT.DBUV_PER_M, pytest.approx(69.50, rel=1e-2)),
    (1000, FSUNIT.Tesla, FSUNIT.DBUV_PER_M, pytest.approx(349.5, rel=1e-2)),
    (1000, FSUNIT.Gauss, FSUNIT.DBUV_PER_M, pytest.approx(269.50, rel=1e-2)),
    (1000, FSUNIT.MW_PER_CM_SQ, FSUNIT.DBUV_PER_M, pytest.approx(185.76, rel=1e-2)),
    (1000, FSUNIT.W_PER_M_SQ, FSUNIT.DBUV_PER_M, pytest.approx(175.76, rel=1e-2)),

    # TO other units from dBuV/m
    (100, FSUNIT.DBUV_PER_M, FSUNIT.V_PER_M, pytest.approx(0.10, rel=1e-2)),
    (100, FSUNIT.DBUV_PER_M, FSUNIT.UV_PER_M, pytest.approx(100000.00, rel=1e-2)),
    (100, FSUNIT.DBUV_PER_M, FSUNIT.DBUA_PER_M, pytest.approx(48.50, rel=1e-2)),
    (191.5, FSUNIT.DBUV_PER_M, FSUNIT.A_PER_M, pytest.approx(10.00, rel=1e-2)),
    (191.5, FSUNIT.DBUV_PER_M, FSUNIT.UA_PER_M, pytest.approx(10000000.00, rel=1e-2)),
    (100, FSUNIT.DBUV_PER_M, FSUNIT.DBPT, pytest.approx(50.50, rel=1e-2)),
    (100, FSUNIT.DBUV_PER_M, FSUNIT.PT, pytest.approx(334.97, rel=1e-2)),
    (289.5, FSUNIT.DBUV_PER_M, FSUNIT.Tesla, pytest.approx(1.00, rel=1e-2)),
    (289.5, FSUNIT.DBUV_PER_M, FSUNIT.Gauss, pytest.approx(10000, rel=1e-2)),
    (185.76, FSUNIT.DBUV_PER_M, FSUNIT.MW_PER_CM_SQ, pytest.approx(999.21, rel=1e-2)),
    (185.76, FSUNIT.DBUV_PER_M, FSUNIT.W_PER_M_SQ, pytest.approx(9992.14, rel=1e-2)),
])
def test_field_strength_conversions(con, value, unit_in, unit_out, expected):
    assert con.convert(value, unit_in, unit_out) == expected

def test_invalid_unit(con):
    with pytest.raises(TypeError) as e_info:
        con.convert(10, 'sd', FSUNIT.DBUV_PER_M)
    assert str(e_info.value) == 'Invalid source unit.'

def test_invalid_value(con):
    with pytest.raises(TypeError) as e_info:
        con.convert('sa', FSUNIT.DBUV_PER_M, FSUNIT.DBUV_PER_M)
    assert str(e_info.value) == 'Value must be a number.'