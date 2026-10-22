import subprocess
import argparse
from datetime import datetime

parser = argparse.ArgumentParser(description="Crawling data and select the relavant papers")
parser.add_argument('--query', type=str, default='Quantum Computing', help='Search query (Quantum Computing | LLM)')
parser.add_argument('--date-from', type=str, help='Start date (YYYY-MM-DD)')
parser.add_argument('--date-to', type=str, help='End date (YYYY-MM-DD)')
parser.add_argument('--num-papers', type=int, default=15, help='Number of papers to be selected, will be devided by 5 (weekdays) (Default = 15)')
parser.add_argument('--curated', action='store_true', help='Build the themed weekly issue (one thread + AI written take) instead of selecting random papers')
parser.add_argument('--planned-date', type=str, help='Upload planned Monday date (YYYY-MM-DD), required with --curated')
args = parser.parse_args()

UTILS_DIR = "./utils"

# Run the crawling command
subprocess.run(["python", f"{UTILS_DIR}/arxiv_web_crawler.py", "--query", args.query, "--date-from", args.date_from, "--date-to", args.date_to])

# Once the crawling command finishes, run to select the selected papers
query_safe = args.query.replace(' ', '_')
date_from = datetime.strptime(args.date_from, '%Y-%m-%d').strftime('%Y%m%d')
date_to = datetime.strptime(args.date_to, '%Y-%m-%d').strftime('%Y%m%d')
num_papers = str(args.num_papers)
input_file = f'{date_from}_{date_to}.csv'

if args.curated:
    if not args.planned_date:
        raise SystemExit('--planned-date is required with --curated')
    result = subprocess.run(["python", "curated_newsletter.py", "--query", args.query, "--input-file", input_file, "--planned-date", args.planned_date])
    if result.returncode != 3:  # 3 = no Claude subscription or API key available
        raise SystemExit(result.returncode)
    print('No Claude subscription or API key available - falling back to the keyword-based selection.')

subprocess.run(["python", f"{UTILS_DIR}/rank_parser.py", "--query", args.query, '--input-file', input_file, '--num-papers', num_papers])
