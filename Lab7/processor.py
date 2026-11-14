"""Lab 7: validate user input; return None for invalid values."""

import math


def parse_booking(text):
    """Return (normalized pet name, nonnegative finite days), or None."""
    if not isinstance(text, str) or text.count(":") != 1:
        return None
    pet, days_text = text.split(":")
    pet = pet.strip()
    if not pet:
        return None
    try:
        days = float(days_text)
    except (ValueError, OverflowError):
        return None
    if not math.isfinite(days) or days < 0:
        return None
    return pet.title(), days


def stay_average(days_csv):
    """Return the arithmetic mean of nonnegative integer stays, or None."""
    if not isinstance(days_csv, str):
        return None
    try:
        values = [int(item.strip()) for item in days_csv.split(",")]
    except ValueError:
        return None
    if any(value < 0 for value in values):
        return None
    try:
        average = sum(values) / len(values)
    except OverflowError:
        return None
    return average if math.isfinite(average) else None


def payable_fee(text):
    """Apply 18 percent tax, then discount; reject invalid amounts."""
    if not isinstance(text, str) or text.count("|") != 1:
        return None
    try:
        fee, discount = (float(item) for item in text.split("|"))
    except (ValueError, OverflowError):
        return None
    if not all(math.isfinite(value) and value >= 0 for value in (fee, discount)):
        return None
    total = fee * 1.18 - discount
    if not math.isfinite(total):
        return None
    return max(total, 0.0)


def main():
    print("==== Running parse_booking ====")
    result = parse_booking(input("Enter pet:days (e.g. dog:5): "))
    print("Pet and Days:", result if result is not None else "Invalid booking")

    print("\n==== Running stay_average ====")
    result = stay_average(input("Enter stay lengths in days as CSV (e.g. 2,5,7): "))
    print("Average Stay:", result if result is not None else "Invalid stay lengths")

    print("\n==== Running payable_fee ====")
    result = payable_fee(input("Enter fee|discount (e.g. 1500|100): "))
    print("Payable Fee:", result if result is not None else "Invalid fee or discount")


if __name__ == "__main__":
    main()
