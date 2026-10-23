import argparse
import html
import logging
import os
import re
import time

from datetime import datetime
from urllib.parse import quote_plus

import pandas as pd
import requests

from bs4 import BeautifulSoup
import urllib3

urllib3.disable_warnings(
    urllib3.exceptions.InsecureRequestWarning
)

# ============================================================================
# Logging
# ============================================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)


# ============================================================================
# Session
# ============================================================================

def create_session():

    session = requests.Session()

    session.headers.update(
        {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/136.0 Safari/537.36"
            )
        }
    )

    return session


# ============================================================================
# URL Builder
# ============================================================================

def build_url(
    query: str,
    start: int = 0,
    size: int = 200
):

    query = quote_plus(query)

    return (
        "https://arxiv.org/search/"
        f"?query={query}"
        "&searchtype=all"
        "&abstracts=show"
        "&order=-announced_date_first"
        f"&size={size}"
        f"&start={start}"
    )


# ============================================================================
# Parse Date
# ============================================================================

def extract_published_date(result_item):

    meta = result_item.select_one("p.is-size-7")

    if meta is None:
        return None

    text = meta.get_text(" ", strip=True)

    match = re.search(
        r"Submitted\s+(\d+)\s+([A-Za-z]+)\s*,?\s*(\d{4})",
        text
    )

    if not match:
        return None

    try:

        return datetime.strptime(
            f"{match.group(1)} {match.group(2)} {match.group(3)}",
            "%d %B %Y"
        )

    except ValueError:

        try:

            return datetime.strptime(
                f"{match.group(1)} {match.group(2)} {match.group(3)}",
                "%d %b %Y"
            )

        except Exception:

            return None


# ============================================================================
# Parse Search Result
# ============================================================================

def parse_page(
    html_text,
    date_from,
    date_to
):

    soup = BeautifulSoup(
        html_text,
        "html.parser"
    )

    results = soup.select(
        "li.arxiv-result"
    )

    papers = []

    for item in results:

        try:

            published = extract_published_date(item)

            if published is None:
                continue

            if not (
                date_from <= published <= date_to
            ):
                continue

            title_el = item.select_one(
                "p.title"
            )

            title = title_el.get_text(
                " ",
                strip=True
            )

            authors = ", ".join(
                a.get_text(strip=True)
                for a in item.select(
                    "p.authors a"
                )
            )

            abstract_el = item.select_one(
                "span.abstract-full"
            )

            abstract = abstract_el.get_text(
                " ",
                strip=True
            )

            link_el = item.select_one(
                "p.list-title a"
            )

            url = link_el["href"]

            arxiv_id = url.split("/")[-1]

            papers.append(
                {
                    "arxiv_id": arxiv_id,
                    "title": html.unescape(title),
                    "authors": authors,
                    "published": published.strftime(
                        "%Y-%m-%d"
                    ),
                    "url": url,
                    "abstract": html.unescape(
                        abstract
                    )
                }
            )

        except Exception as e:

            logger.warning(
                f"Failed to parse paper: {e}"
            )

    return papers


# ============================================================================
# Crawl
# ============================================================================

def fetch_page(session, url, attempts=4):

    # arXiv search answers 500 intermittently, so retry with a growing pause
    for attempt in range(1, attempts + 1):

        try:

            # arXiv sets an 'arxiv-search-parameters' cookie on the first page and
            # answers 500 when it is sent back with a different start offset
            session.cookies.clear()

            response = session.get(
                url,
                timeout=60,
                verify=False
            )

            response.raise_for_status()

            return response

        except Exception as e:

            logger.warning(
                f"Attempt {attempt}/{attempts} failed: {e}"
            )

            if attempt < attempts:

                time.sleep(10 * attempt)

    return None


def crawl_arxiv(
    query,
    date_from,
    date_to,
    page_size=200
):

    session = create_session()

    start = 0

    all_papers = []

    seen_dense = False

    sparse_pages = 0

    logger.info(
        f"Searching query='{query}'"
    )

    while True:

        url = build_url(
            query=query,
            start=start,
            size=page_size
        )

        logger.info(
            f"Fetching start={start}"
        )

        response = fetch_page(
            session,
            url
        )

        if response is None:

            logger.error(
                f"Giving up at start={start}; "
                f"keeping the {len(all_papers)} papers collected so far"
            )

            break

        papers = parse_page(
            response.text,
            date_from,
            date_to
        )

        if len(papers) == 0:

            logger.info(
                "No papers found on page."
            )

        all_papers.extend(
            papers
        )

        results = BeautifulSoup(
            response.text,
            "html.parser"
        ).select(
            "li.arxiv-result"
        )

        result_count = len(
            results
        )

        # The range shows up as a dense block of pages (dates are noisy, so a single
        # old or recent paper proves nothing). Stop after that block, once two pages
        # in a row hold almost nothing from the range.
        density = (
            len(papers) / result_count
            if result_count else 0
        )

        if density >= 0.3:

            seen_dense = True
            sparse_pages = 0

        elif seen_dense and density < 0.1:

            sparse_pages += 1

        else:

            sparse_pages = 0

        logger.info(
            f"Collected={len(all_papers)}"
        )

        if sparse_pages >= 2:

            logger.info(
                "Past the requested range; stopping."
            )

            break

        if result_count < page_size:
            break

        start += page_size

        time.sleep(5)

    return all_papers


# ============================================================================
# Save
# ============================================================================

def save_result(
    papers,
    query,
    date_from,
    date_to
):

    if len(papers) == 0:

        logger.warning(
            "No papers found."
        )

        return

    df = pd.DataFrame(
        papers
    )

    df.drop_duplicates(
        subset=["arxiv_id"],
        inplace=True
    )

    df.sort_values(
        by="published",
        ascending=False,
        inplace=True
    )

    query_safe = query.replace(
        " ",
        "_"
    )

    output_dir = (
        f"./{query_safe}/crawling"
    )

    os.makedirs(
        output_dir,
        exist_ok=True
    )

    filename = (
        f"{output_dir}/"
        f"{date_from.strftime('%Y%m%d')}_"
        f"{date_to.strftime('%Y%m%d')}.csv"
    )

    df.to_csv(
        filename,
        index=False,
        encoding="utf-8-sig"
    )

    logger.info(
        f"Saved {len(df)} papers"
    )

    logger.info(
        filename
    )


# ============================================================================
# Main
# ============================================================================

def main():

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--query",
        required=True
    )

    parser.add_argument(
        "--date-from",
        required=True
    )

    parser.add_argument(
        "--date-to",
        required=True
    )

    args = parser.parse_args()

    date_from = datetime.strptime(
        args.date_from,
        "%Y-%m-%d"
    )

    date_to = datetime.strptime(
        args.date_to,
        "%Y-%m-%d"
    )

    logger.info(
        "Starting Web Crawl..."
    )

    papers = crawl_arxiv(
        query=args.query,
        date_from=date_from,
        date_to=date_to
    )

    save_result(
        papers,
        args.query,
        date_from,
        date_to
    )

    logger.info(
        "Finished."
    )


if __name__ == "__main__":
    main()