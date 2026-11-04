
import pytest

from daycare_fees import (
    extra_hours_fee,
    enrolment_allowed,
    pickup_status
)

# 1. AGE GROUP VALIDATION
def test_valid_infant_age_group():
    assert extra_hours_fee("infant", 20, False) == 0

def test_valid_toddler_age_group():
    assert extra_hours_fee("toddler", 25, False) == 0

def test_valid_preschool_age_group():
    assert extra_hours_fee("preschool", 30, False) == 0

def test_invalid_age_group():
    with pytest.raises(ValueError):
        extra_hours_fee("school", 10, False)


# 2. NEGATIVE HOURS CONDITION
def test_negative_hours_rejected():
    with pytest.raises(ValueError):
        extra_hours_fee("toddler", -1, False)

def test_zero_hours_accepted():
    assert extra_hours_fee("toddler", 0, False) == 0


# 3. SIBLING DISCOUNT CONDITION
def test_sibling_discount_applied_to_toddler():
    assert extra_hours_fee("toddler", 30, True) == 0

def test_sibling_discount_not_applied_to_infant():
    assert extra_hours_fee("infant", 21, True) == 14

def test_sibling_discount_not_applied_when_no_sibling():
    assert extra_hours_fee("toddler", 26, False) == 9


# 4. INCLUDED HOURS CONDITION
def test_hours_within_included_limit():
    assert extra_hours_fee("preschool", 30, False) == 0

def test_hours_exceed_included_limit():
    assert extra_hours_fee("preschool", 31, False) == 9


# 5. HIGHER EXTRA-HOUR RATE CONDITION
def test_infant_extra_hours_above_twenty():
    assert extra_hours_fee("infant", 41, False) == 462

def test_toddler_extra_hours_above_twenty():
    assert extra_hours_fee("toddler", 46, False) == 294


# 6. IMMUNISATION CONDITION
def test_immunisation_pending_age_twelve():
    assert enrolment_allowed(12, 0, True) is True

def test_immunisation_pending_below_twelve():
    assert enrolment_allowed(11, 5, True) is False

def test_immunisation_not_pending():
    assert enrolment_allowed(6, 1, False) is True


# 7. MINIMUM AGE CONDITION
def test_age_below_six_months():
    assert enrolment_allowed(5, 2, False) is False

def test_age_exactly_six_months():
    assert enrolment_allowed(6, 1, False) is True


# 8. VACANCY CONDITION
def test_vacancy_available():
    assert enrolment_allowed(12, 1, False) is True

def test_no_vacancy_available():
    assert enrolment_allowed(12, 0, False) is False


# 9. AFTERCARE CONDITION
def test_pickup_with_aftercare():
    assert pickup_status(20, True, False) == "on_time"


def test_pickup_without_aftercare():
    assert pickup_status(20, False, False) == "on_time"


# 10. FRIDAY CONDITION
def test_friday_pickup():
    assert pickup_status(20, False, True) == "on_time"

def test_non_friday_pickup():
    assert pickup_status(20, False, False) == "on_time"


# 11. PICKUP STATUS CONDITIONS
def test_pickup_on_time():
    assert pickup_status(20, True, False) == "on_time"

def test_pickup_late():
    assert pickup_status(5, True, False) == "late"


def test_pickup_overdue():
    assert pickup_status(4, True, False) == "overdue"
