import requests
from typing import Dict, Any
import json
from pathlib import Path

from app.config import GITHUB_API_URL, GITHUB_TOKEN


def create_session() -> requests.Session:
    """
    Creates a reusable HTTP session.
    """

    session = requests.Session()

    session.headers.update({
        "Accept": "application/vnd.github+json",
        "User-Agent": "github-data-pipeline"
    })

    if GITHUB_TOKEN:
        session.headers["Authorization"] = f"Bearer {GITHUB_TOKEN}"

    return session





def fetch_repositories(
    language: str = "Python",
    sort: str = "stars",
    per_page: int = 100,
    page: int = 1
) -> Dict[str, Any]:
    """
    Fetch repositories from GitHub.
    """

    session = create_session()

    response = session.get(
        f"{GITHUB_API_URL}/search/repositories",
        params={
            "q": f"language:{language}",
            "sort": sort,
            "per_page": per_page,
            "page": page
        },
        timeout=30
    )

    response.raise_for_status()

    return response.json()


RAW_DIR = Path("data/raw")
RAW_DIR.mkdir(parents=True, exist_ok=True)

def save_raw_json(data, filename):

    filepath = RAW_DIR / filename

    with open(filepath, "w", encoding="utf-8") as file:
        json.dump(
            data,
            file,
            indent=2
        )

    return filepath




if __name__ == "__main__":

    data = fetch_repositories()

    path = save_raw_json(
        data,
        "repositories.json"
    )

    print(path)