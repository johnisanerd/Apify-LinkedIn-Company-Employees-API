"""LinkedIn Company Employees API: a quick-start example.

Get a company employee list from LinkedIn as JSON. Give the API company names or
LinkedIn company URLs and it returns the people who work there, one row per
person: name, job title, headline, location and public profile URL. By default
it opens each person's public profile and keeps only the people who show a
current role at the company. There is no LinkedIn login, cookie or seat: the
data is what LinkedIn shows signed-out visitors, and no emails or phone numbers
are collected.

Get a free Apify API token: https://apify.com?fpr=9n7kx3
Actor: https://apify.com/johnvc/linkedin-company-employees-api?fpr=9n7kx3
Input schema: https://apify.com/johnvc/linkedin-company-employees-api/input-schema?fpr=9n7kx3

Run it:
    uv sync
    cp .env.example .env      # then paste your token into .env
    uv run python linkedin-company-employees-api-example.py

A fresh verified run takes about 3 to 10 minutes per company, so this script
starts the run, prints its id, waits for it to finish and then reads the
dataset. Apify's synchronous run endpoints stop waiting after 300 seconds,
which is too short for a verified run, so do not use them for this API.
"""

from __future__ import annotations

import os
import sys
from typing import Any

from apify_client import ApifyClient
from dotenv import load_dotenv

load_dotenv()

ACTOR_ID = "johnvc/linkedin-company-employees-api"

# Inputs are kept small (one small company, three people) to keep this first
# run quick and inexpensive. At the time of writing every billable event costs
# $0.00001: one Actor start per run, one dataset item per stored row, and one
# employee charge per person (found or verified, never both). Three verified
# people come to 7 events, or $0.00007. Raise maxResultsPerCompany or add
# companies once you know what you need, and uncomment any optional knob below.
RUN_INPUT: dict[str, Any] = {
    "companies": ["https://www.linkedin.com/company/firecrawl"],
    "maxResultsPerCompany": 3,
    # Optional knobs (see the Input Parameters table in the README):
    # "titleKeywords": ["engineer", "head of"],  # narrow by job title; each keyword is also its own search
    # "locations": ["San Francisco"],            # keep only people in these cities, regions or countries
    # "verifyEmployment": False,                 # default True; False is a faster search-level list
    # "maxSearchQueriesPerCompany": 20,          # default 40; fewer search slices is quicker but finds fewer people
    # "maxAgeDays": 0,                           # 0 always fetches fresh; leave it out for the cache defaults
}


def get_client() -> ApifyClient:
    """Build an Apify client from APIFY_API_TOKEN (read from .env or the shell)."""
    token = os.getenv("APIFY_API_TOKEN")
    if not token or token == "your_apify_api_token_here":
        sys.exit(
            "Set APIFY_API_TOKEN first: copy .env.example to .env and paste your token, "
            "or export APIFY_API_TOKEN in your shell.\n"
            "Get one free: https://apify.com?fpr=9n7kx3"
        )
    return ApifyClient(token)


def start_and_wait(client: ApifyClient, run_input: dict[str, Any]) -> tuple[str, str]:
    """Start a run, wait until it finishes, and return its storage ids.

    apify-client 3.x returns typed Run objects, so the ids are attributes
    (run.default_dataset_id), not dictionary keys. To cap spend, pass
    max_total_charge_usd=Decimal("0.50") to start(): the run stops cleanly at
    the cap, and a very small cap also means fewer searches per company.

    Returns:
        The run's default dataset id and default key-value store id.
    """
    run = client.actor(ACTOR_ID).start(run_input=run_input)
    print(
        f"Started run {run.id}. A fresh verified run takes about 3 to 10 minutes "
        "per company; cached results come back sooner. Waiting..."
    )
    finished = client.run(run.id).wait_for_finish()
    if finished is None:
        sys.exit(f"Run {run.id} could not be read back.")
    if finished.status != "SUCCEEDED":
        sys.exit(f"Run {run.id} ended with status {finished.status}: {finished.status_message}")
    return finished.default_dataset_id, finished.default_key_value_store_id


def print_employee(row: dict[str, Any]) -> None:
    """Print one employee row: who, which role, where, and how it was checked."""
    status = "verified" if row.get("verified") else "found, profile not checked"
    print(f"\n{row.get('fullName')}  [{status}: {row.get('matchReason')}]")
    print(f"  title:    {row.get('currentTitle') or 'not shown'}")
    print(f"  headline: {row.get('headline') or 'not shown'}")
    print(f"  location: {row.get('location') or 'not shown'}")
    print(f"  company:  {row.get('companyName')}")
    print(f"  profile:  {row.get('profileUrl')}")
    cached = "  (served from the shared cache)" if row.get("fromCache") else ""
    print(f"  found by: {row.get('foundBy')}{cached}")

    # Verified rows can also carry the public profile's extra fields. Work
    # history (positions) appears only when LinkedIn shows it to signed-out
    # visitors, which is rare, so treat every one of these as optional.
    extras = []
    if row.get("about"):
        extras.append("about text")
    if row.get("positions"):
        extras.append(f"{len(row['positions'])} position(s)")
    if row.get("education"):
        extras.append(f"{len(row['education'])} school(s)")
    if row.get("followers") is not None:
        extras.append(f"{row['followers']:,} followers")
    if extras:
        print(f"  extras:   {', '.join(extras)}")


def print_error(row: dict[str, Any]) -> None:
    """Print an error row (a company that could not be matched or searched)."""
    print(
        f"\nNo people for {row.get('requestedCompany')!r}: "
        f"{row.get('error_type')}: {row.get('error_message')}"
    )


def print_coverage(summary: dict[str, Any]) -> None:
    """Print each company's coverage from the run's RUN_SUMMARY record."""
    print("\nCoverage per company (RUN_SUMMARY):")
    for company in summary.get("companies") or []:
        if company.get("error_type"):
            print(f"  {company.get('requestedCompany')}: {company['error_type']}")
            continue
        listed = company.get("employeesInLinkedin")
        coverage = company.get("coverage")
        listed_text = f"{listed:,} employees listed on LinkedIn" if listed else "no employee count on LinkedIn"
        share = f", coverage {coverage:.1%}" if coverage is not None else ""
        print(
            f"  {company.get('companyName')}: {company.get('found')} found, "
            f"{company.get('verified')} verified, {listed_text}{share} "
            f"(stopped: {company.get('stoppedReason')})"
        )


def main() -> None:
    """Run the quick-start and print the company employee list it returns."""
    client = get_client()
    dataset_id, store_id = start_and_wait(client, RUN_INPUT)

    rows = list(client.dataset(dataset_id).iterate_items())
    employees = [row for row in rows if row.get("result_type") == "employee"]
    errors = [row for row in rows if row.get("result_type") == "error"]
    print(f"\nReturned {len(employees)} employee row(s) and {len(errors)} error row(s).")
    for row in employees:
        print_employee(row)
    for row in errors:
        print_error(row)

    record = client.key_value_store(store_id).get_record("RUN_SUMMARY")
    if record and isinstance(record.get("value"), dict):
        print_coverage(record["value"])


if __name__ == "__main__":
    main()
