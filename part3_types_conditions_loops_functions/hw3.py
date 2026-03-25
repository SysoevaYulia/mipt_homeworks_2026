#!/usr/bin/env python

from typing import Any

UNKNOWN_COMMAND_MSG = "Unknown command!"
NONPOSITIVE_VALUE_MSG = "Value must be grater than zero!"
INCORRECT_DATE_MSG = "Invalid date!"
NOT_EXISTS_CATEGORY = "Category not exists!"
OP_SUCCESS_MSG = "Added"

KEY_AMOUNT = "amount"
KEY_DATE = "date"
KEY_CATEGORY = "category"
DateTuple = tuple[int, int, int]

EXPENSE_CATEGORIES = {
    "Food": ("Supermarket", "Restaurants", "FastFood", "Coffee", "Delivery"),
    "Transport": ("Taxi", "Public transport", "Gas", "Car service"),
    "Housing": ("Rent", "Utilities", "Repairs", "Furniture"),
    "Health": ("Pharmacy", "Doctors", "Dentist", "Lab tests"),
    "Entertainment": ("Movies", "Concerts", "Games", "Subscriptions"),
    "Clothing": ("Outerwear", "Casual", "Shoes", "Accessories"),
    "Education": ("Courses", "Books", "Tutors"),
    "Communications": ("Mobile", "Internet", "Subscriptions"),
    "Other": ("SomeCategory", "SomeOtherCategory"),
}

financial_transactions_storage: list[dict[str, Any]] = []


def is_leap_year(year: int) -> bool:
    if year % 400 == 0:
        return True
    return year % 4 == 0 and year % 100 != 0


def extract_date(maybe_dt: str) -> DateTuple | None:
    if not maybe_dt.replace("-", "").isdigit():
        return None
    day = int(maybe_dt[:2])
    month = int(maybe_dt[3:5])
    year = int(maybe_dt[6:])
    months_amount = 12
    days = [
        31,
        28,
        31,
        30,
        31,
        30,
        31,
        31,
        30,
        31,
        30,
        31,
    ]
    if year < 0:
        return None
    if is_leap_year(year):
        days[1] += 1
    if not (1 <= month <= months_amount):
        return None
    if not (1 <= day <= days[month - 1]):
        return None
    return day, month, year


def get_amount(amount: str) -> float:
    cleaned_amount = amount.replace(",", ".")
    if cleaned_amount.startswith("-"):
        return -float(cleaned_amount[1:])
    return float(cleaned_amount)


def income_handler(amount: float, income_date: str) -> str:
    parsed_date = extract_date(income_date)
    if not parsed_date:
        financial_transactions_storage.append({})
        return INCORRECT_DATE_MSG
    if amount < 0:
        financial_transactions_storage.append({})
        return NONPOSITIVE_VALUE_MSG
    financial_transactions_storage.append(
        {
            KEY_AMOUNT: amount,
            KEY_DATE: parsed_date,
        }
    )
    return OP_SUCCESS_MSG


def is_category_exists(category_name: str) -> bool:
    for cat, value_tuple in EXPENSE_CATEGORIES.items():
        for sub in value_tuple:
            if category_name == f"{cat}::{sub}":
                return True
    return False


def cost_handler(category_name: str, amount: float, cost_date: str) -> str:
    parsed_date = extract_date(cost_date)
    if not parsed_date:
        financial_transactions_storage.append({})
        return INCORRECT_DATE_MSG
    if amount < 0:
        financial_transactions_storage.append({})
        return NONPOSITIVE_VALUE_MSG
    category_exists = is_category_exists(category_name)
    if not category_exists:
        financial_transactions_storage.append({})
        return NOT_EXISTS_CATEGORY
    financial_transactions_storage.append(
        {
            KEY_CATEGORY: category_name,
            KEY_AMOUNT: amount,
            KEY_DATE: parsed_date,
        }
    )
    return OP_SUCCESS_MSG


def cost_categories_handler() -> str:
    lines: list[str] = []
    for cat, subs in EXPENSE_CATEGORIES.items():
        lines.extend(f"{cat}::{sub}" for sub in subs)
    return "\n".join(lines)


def stats_handler(report_date: str) -> str:
    return f"Statistic for {report_date}"


def less_or_equal(date_first: DateTuple, date_second: DateTuple) -> bool:
    if date_first[2] < date_second[2]:
        return True
    if date_first[2] == date_second[2]:
        if date_first[1] < date_second[1]:
            return True
        same_month = date_first[1] == date_second[1]
        less_day = date_first[0] <= date_second[0]
        if same_month and less_day:
            return True
    return False


def calculate_income(start_date: DateTuple, end_date: DateTuple) -> float:
    total_income: float = 0
    right_length = 2
    for transaction in financial_transactions_storage:
        if len(transaction) == right_length:
            date = transaction.get(KEY_DATE)
            if date and less_or_equal(start_date, date) and less_or_equal(date, end_date):
                total_income += transaction[KEY_AMOUNT]
    return total_income


def check_date(start_date: DateTuple | Any, date: DateTuple | Any, end_date: DateTuple | Any) -> bool:
    if not date or not start_date or not end_date:
        return False
    return less_or_equal(start_date, date) and less_or_equal(date, end_date)


def calculate_cost(
    details: dict[str, float],
    start_date: DateTuple,
    end_date: DateTuple,
) -> float:
    total_cost: float = 0
    right_length = 3
    for transaction in financial_transactions_storage:
        if len(transaction) != right_length:
            continue
        date = transaction.get(KEY_DATE)
        if not check_date(start_date, date, end_date):
            continue
        category = transaction[KEY_CATEGORY]
        total_cost += transaction[KEY_AMOUNT]
        details[category] = details.get(category, 0) + transaction[KEY_AMOUNT]
    return total_cost


def calculate_capital(end_date: DateTuple) -> float:
    capital: float = 0
    income_length = 2
    cost_length = 3
    for transaction in financial_transactions_storage:
        date = transaction.get(KEY_DATE)
        if not date or not less_or_equal(date, end_date):
            continue
        if len(transaction) == income_length:
            capital += transaction[KEY_AMOUNT]
        elif len(transaction) == cost_length:
            capital -= transaction[KEY_AMOUNT]
    return capital


def print_stat_result(
    capital: float,
    total_income: float,
    total_cost: float,
    details: dict[str, float],
) -> None:
    print(f"Total capital: {capital:.2f} rubles")
    if total_income >= total_cost:
        profit = total_income - total_cost
        print(f"In this month the profit amounted to {profit:.2f} rubles")
    else:
        loss = total_cost - total_income
        print(f"In this month the loss amounted to {loss:.2f} rubles")
    print(f"Income: {total_income:.2f} rubles")
    print(f"Expenses: {total_cost:.2f} rubles")
    print()
    print("Details (category: amount):")
    count = 1
    for key in sorted(details):
        print(f"{count}. {key}: {details[key]}")
        count += 1


def calculate_stat(start_date: DateTuple, end_date: DateTuple) -> None:
    details: dict[str, float] = {}
    capital = calculate_capital(end_date)
    total_income = calculate_income(start_date, end_date)
    total_cost = calculate_cost(details, start_date, end_date)
    print_stat_result(capital, total_income, total_cost, details)


def print_stat(stat_date: str) -> None:
    end_date = extract_date(stat_date)
    if not end_date:
        print(INCORRECT_DATE_MSG)
        return
    stats_handler(stat_date)
    start_date = (1, end_date[1], end_date[2])
    if not start_date or not end_date:
        return
    calculate_stat(start_date, end_date)


def process_command(parts: list[str]) -> None:
    cmd_full = " ".join(parts)
    if cmd_full == "cost categories":
        cost_categories_handler()
        return
    cmd = parts[0]
    if cmd == "income":
        amount_inc = get_amount(parts[1])
        print(income_handler(amount_inc, parts[2]))
    elif cmd == "cost":
        amount_cost = get_amount(parts[2])
        print(cost_handler(parts[1], amount_cost, parts[3]))
    elif cmd == "stats":
        print_stat(parts[1])
    else:
        print(UNKNOWN_COMMAND_MSG)


def main() -> None:
    with open(0) as file:
        for line in file:
            parts = line.split()
            if parts:
                process_command(parts)


if __name__ == "__main__":
    main()
