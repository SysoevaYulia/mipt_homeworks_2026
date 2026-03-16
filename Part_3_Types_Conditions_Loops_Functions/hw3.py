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
    if date[2] < 0:
        return None
    if is_leap_year(date[2]):
        days[1] = 29
    if not (date[1] >= 1 and date[1] <= 12):
        return None 
    if not (date[0] >= 1 and date[0] <= days[date[1] - 1]):
        return None
    return date


def income_handler(amount: float, income_date: str) -> str:
    return f"{OP_SUCCESS_MSG} {amount=} {income_date=}"


def cost_handler(category_name: str, amount: float, income_date: str) -> str:
    return f"{OP_SUCCESS_MSG} {category_name} {amount=} {income_date=}"

def stats_handler(report_date: str) -> str:
    return f"Statistic for {report_date}"

def get_amount(amount: str) -> int:
    amount = amount.replace(',', '.')
    amount = float(amount)
    return amount


def is_correct_amount(amount: str) -> bool:
    if get_amount(amount) <= 0:
        return False 
    return True


def add_income(incomes, amount: str, date: str):
    incomes.append((get_amount(amount), extract_date(date)))


def add_cost(costs, parts):
    costs.append((parts[1], get_amount(parts[2]), extract_date(parts[3])))


def less_or_equal(date_first, date_second) -> bool:
    if date_first[2] < date_second[2]:
        return True
    elif date_first[2] == date_second[2]:
        if date_first[1] < date_second[1]:
            return True
        elif date_first[1] == date_second[1]:
            if date_first[0] <= date_second[0]:
                return True
    return False


def calculate_stat(incomes, costs, end_date: str):
    total_income = 0
    total_cost = 0
    start_date = extract_date("01" + end_date[2:])
    end_date = extract_date(end_date)
    details = {}
    capital = 0
    for i in range(len(incomes)):
        income = incomes[i][0]
        date = incomes[i][1]
        if less_or_equal(start_date, date) and less_or_equal(date, end_date):
            total_income += income
        if less_or_equal(date, end_date):
            capital += income

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
        if less_or_equal(date, end_date):
            capital -= cost

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
    incomes = []
    costs = []
    for line in open(0):
        parts = line.split()
        if not parts:
            continue
        if parts[0] == "income":
            if len(parts) != 3:
                print(UNKNOWN_COMMAND_MSG)
                continue 
            if not is_correct_amount(parts[1]):
                print(NONPOSITIVE_VALUE_MSG)
                continue
            if not extract_date(parts[2]):
                print(INCORRECT_DATE_MSG)
                continue
            add_income(incomes, parts[1], parts[2])
            income_handler(get_amount(parts[1]), parts[2])
        elif parts[0] == "cost":
            if len(parts) != 4:
                print(UNKNOWN_COMMAND_MSG)
                continue 
            if not is_correct_amount(parts[2]):
                print(NONPOSITIVE_VALUE_MSG)
                continue
            if not extract_date(parts[3]):
                print(INCORRECT_DATE_MSG)
                continue
            add_cost(costs, parts)
            cost_handler(parts[1], get_amount(parts[2]), parts[3])
        elif parts[0] == "stats":
            if len(parts) != 2:
                print(UNKNOWN_COMMAND_MSG)
                continue 
            if not extract_date(parts[1]):
                print(INCORRECT_DATE_MSG)
                continue
            stats_handler(parts[1])
            calculate_stat(incomes, costs, parts[1])
        else:
            print(UNKNOWN_COMMAND_MSG)


if __name__ == "__main__":
    main()
