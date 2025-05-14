"""
JSON parser for stat service
"""

import argparse
import json
import sys
import threading
import time
from datetime import datetime, timedelta

from flask import Flask, send_file

import gig_client

app = Flask(__name__)


@app.route("/stats", methods=["GET"])
def get_stats():
    """
    Endpoint to get the statistics.
    """
    return send_file(
        args.output_file, mimetype="application/json"
    )  # pylint: disable=E0606


def produce_statistics_gigs(json_data):
    """
    Produce statistics from the given JSON data.
    """
    total_completed = 0
    completed_last_24h = 0
    gigs_by_user = {}
    now = datetime.now()

    for gig in json_data.get("items", []):
        if gig.get("status") == "completed":
            total_completed += 1

            owner_id = gig.get("owner", {}).get("id")
            if owner_id:
                gigs_by_user[owner_id] = gigs_by_user.get(owner_id, 0) + 1

            end_date = datetime.fromisoformat(gig.get("end_date"))
            if now - end_date <= timedelta(days=1):
                completed_last_24h += 1

    statistics = {
        "total_completed": total_completed,
        "completed_last_24h": completed_last_24h,
        "gigs_by_user": gigs_by_user,
    }

    return json.dumps(statistics, indent=4)


def produce_statistics_postings(json_data):
    """
    Produce statistics from the given JSON data.
    """
    total_postings = 0
    open_postings = 0
    expired_postings = 0
    postings_by_user = {}
    now = datetime.now()

    for posting in json_data.get("items", []):
        total_postings += 1

        owner_id = posting.get("owner", {}).get("id")
        if owner_id:
            postings_by_user[owner_id] = postings_by_user.get(owner_id, 0) + 1

        expires_at = posting.get("expires_at")
        if expires_at:
            expires_at = datetime.fromisoformat(expires_at)
        if expires_at and expires_at > now:
            open_postings += 1
        else:
            expired_postings += 1

    statistics = {
        "total_postings": total_postings,
        "open_postings": open_postings,
        "expired_postings": expired_postings,
        "postings_by_user": postings_by_user,
    }

    return json.dumps(statistics, indent=4)


def combine_statistics(gigs_stats, postings_stats):
    """
    Combine the statistics from gigs and postings into a single JSON object.
    """
    combined_stats = {
        "gigs_statistics": json.loads(gigs_stats),
        "postings_statistics": json.loads(postings_stats),
    }

    return json.dumps(combined_stats, indent=4)


def poll_with_cli_and_build_stats():
    """
    Poll the server for gigs and postings data and build statistics.
    """
    while True:

        print("Polling for gigs and postings...")
        original_argv = sys.argv.copy()
        sys.argv = [
            "gig_client.py",
            args.server_ip,
            "gigs",
            "list",
            "--json_to_file=gigs.json",
        ]
        gig_client.main()
        sys.argv = [
            "gig_client.py",
            args.server_ip,
            "postings",
            "list",
            "--json_to_file=postings.json",
        ]
        gig_client.main()
        sys.argv = original_argv
        print("Gigs and postings data saved to gigs.json and postings.json")

        print("Building statistics...")

        with open("gigs.json", "r", encoding="utf-8") as f:
            gigs_data = json.load(f)

        with open("postings.json", "r", encoding="utf-8") as f:
            postings_data = json.load(f)

        gig_stats = produce_statistics_gigs(gigs_data)
        posting_stats = produce_statistics_postings(postings_data)
        combined_stats = combine_statistics(gig_stats, posting_stats)
        with open(args.output_file, "w", encoding="utf-8") as f:
            f.write(combined_stats)
        print(f"Statistics written to {args.output_file}")
        time.sleep(120)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Stat Service JSON Parser")
    parser.add_argument("server_ip", type=str, help="IP to the server to connect to")
    parser.add_argument("output_file", type=str, help="Path to output JSON file")
    args = parser.parse_args()

    threading.Thread(
        target=poll_with_cli_and_build_stats,
        daemon=True,
    ).start()
    app.run(host="0.0.0.0", port=5000)
