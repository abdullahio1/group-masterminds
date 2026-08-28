from flask import Flask, request, jsonify
import subprocess
import sys

app = Flask(__name__)


@app.route("/api/generate-report", methods=["POST"])
def generate_report():
    data = request.get_json()

    # 1. Validate incoming JSON
    if not data or "weekdate" not in data:
        return jsonify(
            {"error": "Missing required parameter: 'weekdate' (YYYY-MM-DD)"}
        ), 400

    weekdate = data["weekdate"]
    output_target = data.get("output", "both")  # Defaults to 'both'

    # Terminal command
    # list instead of a single string to prevent command injection attacks.
    command = [
        sys.executable,
        "-m",
        "apps.report.main",
        "-wd",
        weekdate,
        "-ot",
        output_target,
    ]

    try:
        # Execute the CLI script and wait for it to finish
        result = subprocess.run(
            command,
            capture_output=True,  # Captures terminal print()
            text=True,  # Returns output as strings
            check=True,  # Raises an error if the script crashes exit code != 0
        )

        # If successful, return the terminal output
        return jsonify(
            {"status": "success", "terminal_output": result.stdout.strip()}
        ), 200

    except subprocess.CalledProcessError as e:
        # If the CLI script crashed (e.g., database error, bad date format)
        return jsonify(
            {
                "error": "CLI script failed",
                "exit_code": e.returncode,
                "stdout": e.stdout.strip(),
                "stderr": e.stderr.strip(),
            }
        ), 500

    except Exception as e:
        # If Flask itself fails to launch the script
        return jsonify({"error": "Failed to execute process", "details": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
