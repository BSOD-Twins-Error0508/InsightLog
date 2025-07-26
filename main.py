import argparse
import csv
from insightlog.lib import InsightLogAnalyzer


def main():
    parser = argparse.ArgumentParser(description="Analyze server log files (nginx, apache2, auth)")
    parser.add_argument('--service', required=True, choices=['nginx', 'apache2', 'auth'], help='Type of log to analyze')
    parser.add_argument('--logfile', required=True, help='Path to the log file')
    parser.add_argument('--filter', required=False, default=None, help='String to filter log lines')
    parser.add_argument('--export', required=False, help='Path to export CSV file')
    parser.add_argument('--export_json', required=False, help='Path to export JSON file')  # neu
    args = parser.parse_args()
    analyzer = InsightLogAnalyzer(args.service, filepath=args.logfile)

    # Add and Remove filter
    # analyzer.add_filter('a')
    # analyzer.add_filter('b')
    # analyzer.add_filter('c')
    # print(analyzer.get_all_filters())
    # analyzer.remove_filter(1)
    # print(analyzer.get_all_filters())

    if args.filter:
        analyzer.add_filter(args.filter)
    requests = analyzer.get_requests()
    for req in requests:
        print(req)
    
    # === Export CSV ===
    if args.export:
        analyzer.export_to_csv(args.export)
        print(f"Ergebnisse wurden exportiert nach: {args.export}")

    # JSON Export
    if args.export_json:
        analyzer.export_to_json(args.export_json)
        print(f"Ergebnisse wurden exportiert nach: {args.export_json}")

if __name__ == '__main__':
    main() 