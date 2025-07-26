import argparse
import sys
# The InsightLogAnalyzer class is imported from the lib.py
from insightlog.lib import InsightLogAnalyzer


def main():
    parser = argparse.ArgumentParser(description="Analyze server log files (nginx, apache2, auth)")
    parser.add_argument('--service', required=True, choices=['nginx', 'apache2', 'auth'], help='Type of log to analyze')
    parser.add_argument('--logfile', required=True, help='Path to the log file')
    parser.add_argument('--filter', required=False, default=None, help='String to filter log lines')
    parser.add_argument('--level', required=False, default=None, help='Filter by log level (e.g., ERROR, WARNING)')
    args = parser.parse_args()

    # BUG FIX: Added a try...except block to handle errors from the analyzer library.
    #
    # THE BUG: The provided library code has multiple issues.
    # 1. The `filter_data` function explicitly notes a bug where it returns `None` on
    #    a file error instead of raising an exception.
    # 2. The `filter_all` method, which is called by `get_requests`, does not handle
    #    file errors at all and will crash with a FileNotFoundError or PermissionError.
    #
    # If `get_requests` were to return `None` (like `filter_data` does), the original
    # code would crash on the line `for req in requests:` with a `TypeError`.
    #
    # THE FIX: This `try...except` block makes the script robust against these bugs.
    # - It catches `FileNotFoundError` and `PermissionError` directly.
    # - It catches the `TypeError`, which specifically handles the case where the
    #   analyzer returns `None`.
    # This prevents the program from crashing and provides a clear error message,
    # improving usability and making debugging much easier.
    try:
        analyzer = InsightLogAnalyzer(args.service, filepath=args.logfile)
        if args.filter:
            analyzer.add_filter(args.filter)
        if args.level:
            analyzer.add_log_level_filter(args.level)

        requests = analyzer.get_requests()

        # This check is crucial for handling the "returns None on error" bug.
        if requests is None:
            # This handles the case where get_requests returns None, as seen in other
            # parts of the library, preventing a TypeError in the loop below.
            raise TypeError("Analyzer returned None.")

        for req in requests:
            print(req)

    except FileNotFoundError:
        sys.stderr.write(f"Error: The file '{args.logfile}' was not found.\n")
        sys.exit(1)
    except PermissionError:
        sys.stderr.write(f"Error: Permission denied to read the file '{args.logfile}'.\n")
        sys.exit(1)
    except TypeError:
        # This directly handles the symptom of the bug where the analyzer returns None.
        sys.stderr.write("Error: The log analyzer returned an invalid result (None).\n")
        sys.stderr.write("This is likely due to an error reading or parsing the log file.\n")
        sys.exit(1)
    except Exception as e:
        # Catch any other unexpected errors from the analyzer.
        sys.stderr.write(f"An unexpected error occurred: {e}\n")
        sys.exit(1)


if __name__ == '__main__':
    main()