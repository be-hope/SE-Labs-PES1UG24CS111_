"""Independent branch and boundary tests for the pet boarding module."""
import pytest

from pet_boarding import admission_ok, boarding_fee, checkout_status


@pytest.mark.parametrize("pet,days,premium,expected", [
    ("cat", 0, False, 0),
    ("cat", 3, False, 0), ("cat", 4, False, 20),
    ("dog", 2, False, 0), ("dog", 3, False, 30),
    ("dog", 3, True, 0), ("dog", 4, True, 30),
    ("cat", 4, True, 0), ("cat", 5, True, 20),
    ("rabbit", 4, True, 0), ("rabbit", 5, True, 20),
    ("rabbit", 5, False, 20),
    ("dog", 12, False, 300), ("dog", 13, False, 495),
    ("cat", 13, False, 200), ("cat", 14, False, 330),
    ("rabbit", 15, True, 330),
])
def test_fee_branches_and_boundaries(pet, days, premium, expected):
    assert boarding_fee(pet, days, premium) == expected


@pytest.mark.parametrize("pet,days,message", [
    ("bird", 1, "unknown pet type"),
    ("dog", -1, "invalid days"),
])
def test_rejected_bookings(pet, days, message):
    with pytest.raises(ValueError, match=message):
        boarding_fee(pet, days, False)


@pytest.mark.parametrize("age,vaccinations,senior,expected", [
    (12, 2, True, False), (12, 3, True, True),
    (0.99, 3, False, False), (1, 1, False, False),
    (1, 2, False, True), (4, 3, False, True),
])
def test_admission_branches(age, vaccinations, senior, expected):
    assert admission_ok(age, vaccinations, senior) is expected


@pytest.mark.parametrize("long_stay,weekend,cutoff", [
    (False, False, 15), (False, True, 35),
    (True, False, 30), (True, True, 50),
])
def test_checkout_boundaries(long_stay, weekend, cutoff):
    assert checkout_status(cutoff, long_stay, weekend) == "open"
    assert checkout_status(cutoff - 1, long_stay, weekend) == "late"
    assert checkout_status(cutoff - 15, long_stay, weekend) == "late"
    assert checkout_status(cutoff - 16, long_stay, weekend) == "closed"
