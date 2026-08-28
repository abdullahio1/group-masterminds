from datetime import timedelta


def get_week_range(given_date):
    monday = given_date - timedelta(days=given_date.weekday())
    sunday = monday + timedelta(days=6)
    return monday, sunday


def write_report(*list_args, filename: str, method: str = "a") -> None:
    """Write variable number of lists to file"""
    try:
        with open(filename, method) as f:
            for current_list in list_args:
                f.writelines(f"{line}\n" for line in current_list)
    except IOError as e:
        raise IOError(
            f"Could not write report to {filename}. Check permissions/disk space. Error: {e}"
        )
