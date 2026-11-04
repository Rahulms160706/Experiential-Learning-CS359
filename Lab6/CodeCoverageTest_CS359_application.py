
import pytest

from daycare_fees import (
    extra_hours_fee,
    enrolment_allowed,
    pickup_status
)

# EXTRA HOURS FEE TESTS
def test_invalid_age_group():
    with pytest.raises(ValueError):
        extra_hours_fee("school", 10, False)

def test_negative_hours():
    with pytest.raises(ValueError):
        extra_hours_fee("toddler", -1, False)

def test_included_hours_without_sibling():
    assert extra_hours_fee("toddler", 25, False) == 0

def test_sibling_increases_included_hours():
    assert extra_hours_fee("toddler", 30, True) == 0

def test_infant_extra_hours():
    assert extra_hours_fee("infant", 21, False) == 14

def test_preschool_extra_hours():
    assert extra_hours_fee("preschool", 31, False) == 9

def test_infant_extra_hours_above_20():
    assert extra_hours_fee("infant", 41, False) == 462

def test_toddler_extra_hours_above_20():
    assert extra_hours_fee("toddler", 46, False) == 294


# ENROLMENT TESTS
def test_immunisation_pending():
    assert enrolment_allowed(12, 0, True) is True

def test_child_below_six_months():
    assert enrolment_allowed(5, 2, False) is False

def test_enrolment_with_vacancy():
    assert enrolment_allowed(6, 1, False) is True


# PICKUP STATUS TESTS
def test_pickup_on_time():
    assert pickup_status(20, True, False) == "on_time"

def test_pickup_late():
    assert pickup_status(10, True, False) == "late"

def test_pickup_overdue():
    assert pickup_status(4, True, False) == "overdue"

def test_friday_pickup():
    assert pickup_status(20, False, True) == "on_time"
