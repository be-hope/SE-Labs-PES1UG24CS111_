"""Independent statement coverage tests for the pet boarding module."""
import pytest

from pet_boarding import admission_ok, boarding_fee, checkout_status


@pytest.mark.parametrize("pet,days,premium,expected", [
    ("cat", 3, False, 0),
    ("dog", 4, False, 60),
    ("cat", 5, True, 20),
    ("rabbit", 6, True, 40),
    ("dog", 13, False, 495),
    ("cat", 14, False, 330),
])
def test_boarding_fee(pet, days, premium, expected):
    assert boarding_fee(pet, days, premium) == expected


@pytest.mark.parametrize("pet,days,message", [
    ("bird", 2, "unknown pet type"),
    ("cat", -1, "invalid days"),
])
def test_invalid_booking(pet, days, message):
    with pytest.raises(ValueError, match=message):
        boarding_fee(pet, days, False)


@pytest.mark.parametrize("age,vaccinations,senior,expected", [
    (10, 3, True, True), (10, 2, True, False),
    (0.5, 3, False, False), (1, 2, False, True),
    (4, 1, False, False),
])
def test_admission(age, vaccinations, senior, expected):
    assert admission_ok(age, vaccinations, senior) is expected


@pytest.mark.parametrize("minutes,long_stay,weekend,expected", [
    (30, True, False, "open"),
    (20, True, False, "late"),
    (14, True, False, "closed"),
    (35, False, True, "open"),
    (0, False, False, "late"),
])
def test_checkout(minutes, long_stay, weekend, expected):
    assert checkout_status(minutes, long_stay, weekend) == expected
