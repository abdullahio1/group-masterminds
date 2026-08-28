import argparse
import os
import sys
from datetime import datetime

# Import local modules
from apps.report.utils import get_week_range, write_report
from apps.report.database import get_time_entries
from apps.report.reporter import generate_weekly_report, generate_customer_report
from apps.report.azure_storage import upload_report_blob
from shared.credentials import get_storage_credentials


def valid_date(date_str: str) -> datetime:
    try:
        return datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        raise argparse.ArgumentTypeError(
            f"Invalid date: '{date_str}'. Expected: YYYY-MM-DD"
        )


def main():
    parser = argparse.ArgumentParser(
        prog="Time Management Reporter",
        description="Generates consultant reports and routes them to disk or Azure.",
    )
    parser.add_argument(
        "-wd", "--weekdate", type=valid_date, required=True, help="Format: YYYY-MM-DD"
    )
    parser.add_argument(
        "-ot",
        "--output",
        choices=["disk", "remote", "both"],
        default="both",
        help="Output target",
    )
    args = parser.parse_args()

    # 1. Calculate dates
    monday, sunday = get_week_range(args.weekdate)
    iso_year, week_num, _ = args.weekdate.isocalendar()
    filename = f"report-{iso_year}-w{week_num}.txt"

    try:
        print(f"Fetching data from {monday.date()} to {sunday.date()}...")

        # 2. Fetch Data & Generate Report Arrays
        raw_data = get_time_entries(monday, sunday)
        weekly_report = generate_weekly_report(raw_data, week_num, args.weekdate)
        customer_report = generate_customer_report(raw_data)

        # 3. Write to disk initially (needed for Azure upload anyway)
        write_report(weekly_report, customer_report, filename=filename, method="w")

        # 4. Handle Routing Logic
        if args.output in ["disk", "both"]:
            print(f"Report saved locally to: {filename}")

        if args.output in ["remote", "both"]:
            print("Uploading to Azure Storage...")
            conn_string = get_storage_credentials()
            upload_report_blob(conn_string, filename, f"reports/{iso_year}")
            print("Upload complete.")

            # Cleanup local file if they ONLY wanted remote
            if args.output == "remote":
                try:
                    os.remove(filename)
                    print("Local temporary file removed.")
                except OSError as e:
                    print(f"Warning: Could not delete local temp file {filename}: {e}")
    except EnvironmentError as e:
        print(f"\n[CONFIGURATION ERROR] {e}", file=sys.stderr)
        sys.exit(1)
    except (ConnectionError, RuntimeError, IOError) as e:
        print(f"\n[SYSTEM ERROR] {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"\n[UNEXPECTED ERROR] {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
