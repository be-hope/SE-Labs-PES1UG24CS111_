"""Fuzz arbitrary input and verify useful behavior on valid input."""

import math

import pytest
from hypothesis import example, given, settings, strategies as st

from processor import parse_booking, stay_average, payable_fee


# Include the original text/None strategy and other unexpected input types.
inputs = st.one_of(
    st.text(), st.none(), st.integers(), st.floats(), st.binary(),
    st.lists(st.integers(), max_size=5),
    st.dictionaries(st.text(max_size=5), st.integers(), max_size=3),
)


@settings(max_examples=300)
@given(inputs)
@example(":")
@example("dog:nan")
@example("dog:inf")
@example("dog")
@example("abc")
@example("dog:abc")
@example('dog:"abc "')
def test_parse_booking_no_crash(s):
    result = parse_booking(s)
    if isinstance(s, str) and s in {"dog", "abc", "dog:abc", 'dog:"abc "'}:
        assert result is None
    if result is not None:
        pet, days = result
        assert pet and pet == pet.strip()
        assert math.isfinite(days) and days >= 0


@settings(max_examples=300)
@given(inputs)
@example("")
@example("2,,7")
@example("9" * 5000)
def test_stay_average_no_crash(s):
    result = stay_average(s)
    assert result is None or (math.isfinite(result) and result >= 0)


@settings(max_examples=300)
@given(inputs)
@example("|")
@example("nan|0")
@example("1.7e308|0")
def test_payable_fee_no_crash(s):
    result = payable_fee(s)
    assert result is None or (math.isfinite(result) and result >= 0)


@given(st.sampled_from(["dog", "cat", "rabbit"]),
       st.integers(min_value=0, max_value=10000))
def test_valid_booking(pet, days):
    assert parse_booking(f" {pet} : {days} ") == (pet.title(), float(days))


@given(st.lists(st.integers(min_value=0, max_value=1000000),
                min_size=1, max_size=30))
def test_valid_average(values):
    text = ",".join(str(value) for value in values)
    assert stay_average(text) == pytest.approx(sum(values) / len(values))


@given(st.integers(min_value=0, max_value=1000000),
       st.integers(min_value=0, max_value=1000000))
def test_valid_fee(fee, discount):
    assert payable_fee(f"{fee}|{discount}") == pytest.approx(
        max(fee * 1.18 - discount, 0.0)
    )


@pytest.mark.parametrize("function, text", [
    (parse_booking, ""), (parse_booking, ":"),
    (parse_booking, "dog:1:2"), (parse_booking, " :5"),
    (parse_booking, "dog:-1"), (parse_booking, "dog:nan"),
    (parse_booking, "dog:inf"), (stay_average, ""),
    (stay_average, "2,,7"), (stay_average, "-1,2"),
    (stay_average, "2.5,3"), (payable_fee, "|"),
    (payable_fee, "1|2|3"), (payable_fee, "-1|0"),
    (payable_fee, "1|-2"), (payable_fee, "nan|0"),
    (payable_fee, "0|inf"), (payable_fee, "1.7e308|0"),
])
def test_invalid_values_are_rejected(function, text):
    assert function(text) is None


def test_fractional_average_is_not_truncated():
    assert stay_average("2,3") == 2.5


def test_discount_cannot_make_fee_negative():
    assert payable_fee("100|200") == 0.0
