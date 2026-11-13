from hypothesis import given, strategies as st
from daycare_fees import parse_enrolment, hours_average, payable_fee


@given(st.text() | st.none())
def test_parse_enrolment_no_crash(s):
    try:
        parse_enrolment(s)
    except Exception as e:
        assert False, f"parse_enrolment crashed with: {e}"


@given(st.text() | st.none())
def test_hours_average_no_crash(s):
    try:
        hours_average(s)
    except Exception as e:
        assert False, f"hours_average crashed with: {e}"


@given(st.text() | st.none())
def test_payable_fee_no_crash(s):
    try:
        payable_fee(s)
    except Exception as e:
        assert False, f"payable_fee crashed with: {e}"