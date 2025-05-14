import json
from datetime import datetime, timedelta

import pytest
from main import (combine_statistics, produce_statistics_gigs,
                  produce_statistics_postings)


@pytest.fixture
def sample_gigs_data():
    """Fixture for sample gigs JSON data."""
    now = datetime.now()
    return {
        "items": [
            {
                "id": 1,
                "owner": {"id": 3, "first_name": "Clark", "last_name": "Kent"},
                "posting": 1,
                "start_date": (now - timedelta(days=10)).isoformat(),
                "end_date": (now - timedelta(days=1)).isoformat(),
                "status": "completed",
            },
            {
                "id": 2,
                "owner": {"id": 4, "first_name": "Diana", "last_name": "Prince"},
                "posting": 2,
                "start_date": (now - timedelta(days=5)).isoformat(),
                "end_date": now.isoformat(),
                "status": "in_progress",
            },
        ]
    }


@pytest.fixture
def sample_postings_data():
    """Fixture for sample postings JSON data."""
    now = datetime.now()
    return {
        "items": [
            {
                "id": 1,
                "owner": {"id": 3, "first_name": "Clark", "last_name": "Kent"},
                "title": "Yard Work",
                "expires_at": (now + timedelta(days=5)).isoformat(),
                "price": 100.00,
                "status": "open",
            },
            {
                "id": 2,
                "owner": {"id": 4, "first_name": "Diana", "last_name": "Prince"},
                "title": "Furniture Assembly",
                "expires_at": (now - timedelta(days=1)).isoformat(),
                "price": 200.00,
                "status": "expired",
            },
        ]
    }


def test_produce_statistics_gigs(sample_gigs_data):
    """Test the produce_statistics_gigs function."""
    stats = json.loads(produce_statistics_gigs(sample_gigs_data))
    assert stats["total_completed"] == 1
    assert stats["completed_last_24h"] == 0
    assert stats["gigs_by_user"] == {"3": 1}


def test_produce_statistics_postings(sample_postings_data):
    """Test the produce_statistics_postings function."""
    stats = json.loads(produce_statistics_postings(sample_postings_data))
    assert stats["total_postings"] == 2
    assert stats["open_postings"] == 1
    assert stats["expired_postings"] == 1
    assert stats["postings_by_user"] == {"3": 1, "4": 1}


def test_combine_statistics(sample_gigs_data, sample_postings_data):
    """Test the combine_statistics function."""
    gigs_stats = produce_statistics_gigs(sample_gigs_data)
    postings_stats = produce_statistics_postings(sample_postings_data)
    combined_stats = json.loads(combine_statistics(gigs_stats, postings_stats))

    assert "gigs_statistics" in combined_stats
    assert "postings_statistics" in combined_stats

    assert combined_stats["gigs_statistics"]["total_completed"] == 1
    assert combined_stats["postings_statistics"]["total_postings"] == 2
