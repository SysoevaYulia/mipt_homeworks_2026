#!/usr/bin/env python

UNKNOWN_COMMAND_MSG = "Unknown command!"
NONPOSITIVE_VALUE_MSG = "Value must be grater than zero!"
INCORRECT_DATE_MSG = "Invalid date!"
OP_SUCCESS_MSG = "Added"


def is_leap_year(year: int) -> bool:
    is_leap = False
    if year % 400 == 0 or (year % 4 == 0 and year % 100 != 0):
        is_leap = True
    return is_leap


def extract_date(maybe_dt: str) -> tuple[int, int, int] | None:
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


def income_handler(_amount: float, _income_date: str) -> str:
    return OP_SUCCESS_MSG


def cost_handler(_category_name: str, _amount: float, _income_date: str) -> str:
    return OP_SUCCESS_MSG


def stats_handler(report_date: str) -> str:
    return f"Statistic for {report_date}"


def get_amount(amount: str) -> float:
    amount = amount.replace(",", ".")
    return float(amount)


def is_correct_amount(amount: str) -> bool:
    return not get_amount(amount) <= 0


def add_income(incomes: list[tuple[float, tuple[int, int, int]]], parts: list[str]) -> str:
    right_length = 3
    if len(parts) != right_length:
        return UNKNOWN_COMMAND_MSG
    amount = parts[1]
    date = parts[2]
    if not is_correct_amount(amount):
        return NONPOSITIVE_VALUE_MSG

    parsed_date = extract_date(date)
    if not parsed_date:
        return INCORRECT_DATE_MSG

    incomes.append((get_amount(amount), parsed_date))
    return income_handler(get_amount(amount), date)


def add_cost(costs: list[tuple[str, float, tuple[int, int, int]]], parts: list[str]) -> str:
    right_length = 4
    if len(parts) != right_length:
        return UNKNOWN_COMMAND_MSG
    category = parts[1]
    amount = parts[2]
    date = parts[3]
    if not is_correct_amount(amount):
        return NONPOSITIVE_VALUE_MSG

    parsed_date = extract_date(date)
    if not parsed_date:
        return INCORRECT_DATE_MSG

    costs.append((category, get_amount(amount), parsed_date))
    return cost_handler(category, get_amount(amount), date)


def less_or_equal(date_first: tuple[int, int, int], date_second: tuple[int, int, int]) -> bool:
    if date_first[2] < date_second[2]:
        return True
    if date_first[2] == date_second[2]:
        if date_first[1] < date_second[1]:
            return True
        if date_first[1] == date_second[1] and date_first[0] <= date_second[0]:
            return True
    return False


def calculate_income(
    incomes: list[tuple[float, tuple[int, int, int]]], start_date: tuple[int, int, int], end_date: tuple[int, int, int]
) -> float:
    total_income = 0.0
    for i in range(len(incomes)):
        income = incomes[i][0]
        date = incomes[i][1]
        if less_or_equal(start_date, date) and less_or_equal(date, end_date):
            total_income += income
    return total_income


def calculate_cost(
    costs: list[tuple[str, float, tuple[int, int, int]]],
    details: dict[str, float],
    start_date: tuple[int, int, int],
    end_date: tuple[int, int, int],
) -> float:
    total_cost = 0.0
    for i in range(len(costs)):
        category = costs[i][0]
        cost = costs[i][1]
        date = costs[i][2]
        if less_or_equal(start_date, date) and less_or_equal(date, end_date):
            total_cost += cost
            if category in details:
                details[category] += cost
            else:
                details[category] = cost
    return total_cost


def calculate_capital(
    incomes: list[tuple[float, tuple[int, int, int]]],
    costs: list[tuple[str, float, tuple[int, int, int]]],
    end_date: tuple[int, int, int],
) -> float:
    capital = 0.0
    for i in range(len(incomes)):
        income = incomes[i][0]
        date = incomes[i][1]
        if less_or_equal(date, end_date):
            capital += income
    for i in range(len(costs)):
        cost = costs[i][1]
        date = costs[i][2]
        if less_or_equal(date, end_date):
            capital -= cost
    return capital


def calculate_stat(
    incomes: list[tuple[float, tuple[int, int, int]]],
    costs: list[tuple[str, float, tuple[int, int, int]]],
    parts: list[str],
) -> None:
    right_length = 2
    if len(parts) != right_length:
        print(UNKNOWN_COMMAND_MSG)
        return
    parsed_date = extract_date(parts[1])
    if not parsed_date:
        print(INCORRECT_DATE_MSG)
        return

    stats_handler(parts[1])
    start_date = extract_date("01" + parts[1][2:])
    end_date = parsed_date

    if not start_date or not end_date:
        return

    details: dict[str, float] = {}
    capital = 0
    total_income = calculate_income(incomes, start_date, end_date)
    total_cost = calculate_cost(costs, details, start_date, end_date)
    print(f"Total capital: {capital:.2f} rubles")
    if total_income >= total_cost:
        print(f"In this month the profit was {(total_income - total_cost):.2f} rubles")
    else:
        print(f"In this month the loss was {(total_cost - total_income):.2f} rubles")
    print(f"Income: {total_income:.2f} rubles")
    print(f"Cost: {total_cost:.2f} rubles")
    print()
    print("Details (category: sum):")
    count = 1
    for key in sorted(details):
        print(f"{count}. {key}: {details[key]}")
        count += 1


def main() -> None:
    incomes: list[tuple[float, tuple[int, int, int]]] = []
    costs: list[tuple[str, float, tuple[int, int, int]]] = []
    with open(0) as file:
        for line in file:
            parts = line.split()
            if not parts:
                continue
            if parts[0] == "income":
                print(add_income(incomes, parts))
            elif parts[0] == "cost":
                print(add_cost(costs, parts))
            elif parts[0] == "stats":
                calculate_stat(incomes, costs, parts)
            else:
                print(UNKNOWN_COMMAND_MSG)


if __name__ == "__main__":
    main()
