def parse_enrolment(text):
    try:
        if not isinstance(text, str):
            return None

        parts = text.split(':')
        if len(parts) != 2:
            return None

        age_group, hours = parts

        if not age_group.strip():
            return None

        hours = float(hours)

        if hours < 0:
            return None

        return age_group.strip().title(), hours

    except (ValueError, TypeError):
        return None


def hours_average(hours_csv):
    try:
        if not isinstance(hours_csv, str):
            return None

        if not hours_csv.strip():
            return None

        values = [int(r.strip()) for r in hours_csv.split(',')]

        if not values:
            return None

        if any(value < 0 for value in values):
            return None

        return sum(values) // len(values)

    except (ValueError, TypeError, ZeroDivisionError):
        return None


def payable_fee(text):
    try:
        if not isinstance(text, str):
            return None

        parts = text.split('|')

        if len(parts) != 2:
            return None

        fee, discount = parts

        fee = float(fee)
        discount = float(discount)

        if fee < 0 or discount < 0:
            return None

        total = fee * 1.18 - discount

        return max(total, 0)

    except (ValueError, TypeError):
        return None


def main():
    print("==== Running parse_enrolment ====")
    user_input = input("Enter age group:hours (e.g. toddler:25): ")
    result = parse_enrolment(user_input)
    print("Age Group and Hours:", result)

    print("\n==== Running hours_average ====")
    user_input = input("Enter weekly hours as CSV (e.g. 20,25,30): ")
    result = hours_average(user_input)
    print("Average Hours:", result)

    print("\n==== Running payable_fee ====")
    user_input = input("Enter fee|discount (e.g. 3000|250): ")
    result = payable_fee(user_input)
    print("Payable Fee:", result)


if __name__ == "__main__":
    main()