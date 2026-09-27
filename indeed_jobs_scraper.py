#!/usr/bin/env python3
"""Salaries, descriptions and apply links from Indeed, no login. Python, Node.js and cURL clients for the Indeed Jobs Scraper on Apify, pay per result.

Command-line client for the themineworks/indeed-scraper actor on Apify: runs it, waits for it
to finish and saves every result as JSON and CSV. Flags map 1:1 to the actor's input.
Free Apify account and API token: https://console.apify.com/sign-up
Docs and pricing: https://themineworks.com/actors/indeed-scraper/
"""
import argparse, csv, json, os, sys
from apify_client import ApifyClient

ACTOR = "themineworks/indeed-scraper"


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--token", default=os.environ.get("APIFY_TOKEN"), help="Apify API token (or set APIFY_TOKEN)")
    ap.add_argument("--out", default="results", help="Output basename, writes .json and .csv")
    ap.add_argument("--query", help="Job title, skill, or keyword to search for (Indeed's 'what' field), for example 'software…")
    ap.add_argument("--location", help="City, state, ZIP, or 'Remote' (Indeed's 'where' field), for example 'Austin, TX' or…")
    ap.add_argument("--country", help="Which Indeed country site (ccTLD) to search, for example uk.indeed.com for GB")
    ap.add_argument("--max-results", type=int, help="Maximum number of job listings to return")
    a = ap.parse_args()
    if not a.token:
        sys.exit("Provide --token or set APIFY_TOKEN. Free token: https://console.apify.com/sign-up")

    run_input = {}
    if a.query is not None: run_input["query"] = a.query
    if a.location is not None: run_input["location"] = a.location
    if a.country is not None: run_input["country"] = a.country
    if a.max_results is not None: run_input["maxResults"] = a.max_results

    client = ApifyClient(a.token)
    print(f"Running {ACTOR} ...")
    run = client.actor(ACTOR).call(run_input=run_input)
    items = list(client.dataset(run["defaultDatasetId"]).iterate_items())

    with open(a.out + ".json", "w", encoding="utf-8") as f:
        json.dump(items, f, indent=2, ensure_ascii=False)
    keys = []
    for it in items:
        keys += [k for k in it if k not in keys]
    if items:
        with open(a.out + ".csv", "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=keys, extrasaction="ignore")
            w.writeheader()
            for it in items:
                w.writerow({k: json.dumps(v, ensure_ascii=False) if isinstance(v, (list, dict)) else v for k, v in it.items()})
    print(f"Done: {len(items)} results saved to {a.out}.json and {a.out}.csv")


if __name__ == "__main__":
    main()
