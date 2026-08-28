from itertools import groupby
from collections import defaultdict
from datetime import datetime


def generate_weekly_report(data: list[tuple], week: int, sample_date: datetime) -> list:
    result = []
    result.append(f"=== Time Report — Week {week} ({sample_date.date()}) ===")

    for c_id, consultant_rows in groupby(data, key=lambda row: row[0]):
        customer_hours = []
        total_consult_hours = 0
        c_name = None

        for _, _, name, cust_name, net_hours, _ in consultant_rows:
            if not c_name:
                c_name = name
            customer_hours.append(f"{cust_name} {net_hours}")
            total_consult_hours += net_hours

        customer_string = ", ".join(customer_hours)
        result.append(
            f"{c_name:<20} {total_consult_hours:>10.1f} h    {customer_string}"
        )
    return result


def generate_customer_report(data: list[tuple]) -> list:
    result = []
    client_hours = defaultdict(float)

    for c_id, cust_id, c_name, cust_name, net_hours, days_worked in data:
        client_hours[cust_name] += net_hours

    result.append("\nConsultant Hours per Customer:")
    total_customer_hours = 0
    for cust_name, total_h_per_cust in client_hours.items():
        total_customer_hours += total_h_per_cust
        result.append(f"{cust_name:<25} {total_h_per_cust:>10.1f} h")

    result.append(f"\nTotal: {total_customer_hours:.1f} h")
    return result
