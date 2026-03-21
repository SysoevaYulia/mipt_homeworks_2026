#!/usr/bin/env python

from typing import Any

UNKNOWN_COMMAND_MSG = "Unknown command!"
NONPOSITIVE_VALUE_MSG = "Value must be grater than zero!"
INCORRECT_DATE_MSG = "Invalid date!"
NOT_EXISTS_CATEGORY = "Category not exists!"
OP_SUCCESS_MSG = "Added"


EXPENSE_CATEGORIES = {
    "Food": ("Supermarket", "Restaurants", "FastFood", "Coffee", "Delivery"),
    "Transport": ("Taxi", "Public transport", "Gas", "Car service"),
    "Housing": ("Rent", "Utilities", "Repairs", "Furniture"),
    "Health": ("Pharmacy", "Doctors", "Dentist", "Lab tests"),
    "Entertainment": ("Movies", "Concerts", "Games", "Subscriptions"),
    "Clothing": ("Outerwear", "Casual", "Shoes", "Accessories"),
    "Education": ("Courses", "Books", "Tutors"),
    "Communications": ("Mobile", "Internet", "Subscriptions"),
    "Other": ("Music"),
}


financial_transactions_storage: list[dict[str, Any]] = []


def is_leap_year(year: int) -> bool:
    is_leap = False
    if year % 400 == 0 or (year % 4 == 0 and year % 100 != 0):
        is_leap = True
    return is_leap


def extract_date(maybe_dt: str) -> tuple[int, int, int] | None:
    check_date = maybe_dt.replace("-", "")
    for symb in check_date:
        if symb not in "0123456789":
            return None
    date = int(maybe_dt[:2]), int(maybe_dt[3:5]), int(maybe_dt[6:])
    days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    months_amount = 12
    if date[2] < 0:
        return None
    if is_leap_year(date[2]):
        days[1] += 1
    if not (date[1] >= 1 and date[1] <= months_amount):
        return None
    if not (date[0] >= 1 and date[0] <= days[date[1] - 1]):
        return None
    return date


def get_amount(amount: str) -> float:
    amount = amount.replace(",", ".")
    answer = 1
    if amount[0] == "-":
        answer = -1
        amount = amount[1:]
    return answer * float(amount)


def income_handler(amount: float, income_date: str) -> str:
    if not extract_date(income_date):
        financial_transactions_storage.append({})
        return INCORRECT_DATE_MSG
    if amount < 0:
        financial_transactions_storage.append({})
        return NONPOSITIVE_VALUE_MSG

    financial_transactions_storage.append({"amount": amount, "date": extract_date(income_date)})
    return OP_SUCCESS_MSG


def cost_handler(category_name: str, amount: float, cost_date: str) -> str:
    if not extract_date(cost_date):
        financial_transactions_storage.append({})
        return INCORRECT_DATE_MSG
    if amount < 0:
        financial_transactions_storage.append({})
        return NONPOSITIVE_VALUE_MSG
    category_exists = False
    for cat, value_tuple in EXPENSE_CATEGORIES.items():
        for sub in value_tuple:
            if category_name == f"{cat}::{sub}":
                category_exists = True
                break
    if not category_exists:
        financial_transactions_storage.append({})
        return NOT_EXISTS_CATEGORY
    financial_transactions_storage.append(
        {"category": category_name, "amount": amount, "date": extract_date(cost_date)}
    )
    return OP_SUCCESS_MSG


def cost_categories_handler() -> str:
    return "\n".join(f"{cat}::{sub}" for cat, subs in EXPENSE_CATEGORIES.items() for sub in subs)


def stats_handler(report_date: str) -> str:
    return f"Statistic for {report_date}"


def less_or_equal(date_first: tuple[int, int, int], date_second: tuple[int, int, int]) -> bool:
    if date_first[2] < date_second[2]:
        return True
    if date_first[2] == date_second[2]:
        if date_first[1] < date_second[1]:
            return True
        if date_first[1] == date_second[1] and date_first[0] <= date_second[0]:
            return True
    return False


def calculate_income(start_date: tuple[int, int, int], end_date: tuple[int, int, int]) -> float:
    total_income = 0.0
    right_length = 2
    for i in range(len(financial_transactions_storage)):
        if len(financial_transactions_storage[i]) == right_length:
            date = extract_date(financial_transactions_storage[i]["date"])
            if date and less_or_equal(start_date, date) and less_or_equal(date, end_date):
                total_income += financial_transactions_storage[i]["amount"]
    return total_income


def calculate_cost(
    details: dict[str, float],
    start_date: tuple[int, int, int],
    end_date: tuple[int, int, int],
) -> float:
    total_cost = 0.0
    right_length = 3
    for i in range(len(financial_transactions_storage)):
        if len(financial_transactions_storage[i]) == right_length:
            date = extract_date(financial_transactions_storage[i]["date"])
            category = financial_transactions_storage[i]["category"]
            if date and less_or_equal(start_date, date) and less_or_equal(date, end_date):
                total_cost += financial_transactions_storage[i]["amount"]
                if category in details:
                    details[category] += financial_transactions_storage[i]["amount"]
                else:
                    details[category] = financial_transactions_storage[i]["amount"]
    return total_cost


def calculate_capital(
    end_date: tuple[int, int, int],
) -> float:
    capital = 0.0
    income_length = 2
    cost_length = 3
    for i in range(len(financial_transactions_storage)):
        if len(financial_transactions_storage[i]) == income_length:
            date = extract_date(financial_transactions_storage[i]["date"])
            if date and less_or_equal(date, end_date):
                capital += financial_transactions_storage[i]["amount"]
        if len(financial_transactions_storage[i]) == cost_length:
            date = extract_date(financial_transactions_storage[i]["date"])
            if date and less_or_equal(date, end_date):
                capital -= financial_transactions_storage[i]["amount"]
    return capital


def calculate_stat(stat_date: str) -> None:
    parsed_date = extract_date(stat_date)
    if not parsed_date:
        print(INCORRECT_DATE_MSG)
        return

    stats_handler(stat_date)
    start_date = extract_date("01" + stat_date[2:])
    end_date = parsed_date
    if not start_date or not end_date:
        return

    details: dict[str, float] = {}
    capital = calculate_capital(end_date)
    total_income = calculate_income(start_date, end_date)
    total_cost = calculate_cost(details, start_date, end_date)
    print(f"Total capital: {capital:.2f} rubles")
    if total_income >= total_cost:
        print(f"In this month the profit amounted to {(total_income - total_cost):.2f} rubles")
    else:
        print(f"In this month the loss amounted to {(total_cost - total_income):.2f} rubles")
    print(f"Income: {total_income:.2f} rubles")
    print(f"Expenses: {total_cost:.2f} rubles")
    print()
    print("Details (category: amount):")
    count = 1
    for key in sorted(details):
        print(f"{count}. {key}: {details[key]}")
        count += 1


def main() -> None:
    with open(0) as file:
        for line in file:
            parts = line.split()
            if not parts:
                continue
            if line == "cost categories":
                cost_categories_handler()
            elif parts[0] == "income":
                print(income_handler(get_amount(parts[1]), parts[2]))
            elif parts[0] == "cost":
                print(cost_handler(parts[1], get_amount(parts[2]), parts[3]))
            elif parts[0] == "stats":
                calculate_stat(parts[1])
            else:
                print(UNKNOWN_COMMAND_MSG)


if __name__ == "__main__":
    main()
