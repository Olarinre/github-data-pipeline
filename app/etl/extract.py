import json
from pathlib import Path

from requests import Session
from tenacity import retry, stop_after_attempt, wait_exponential

from app.config import GITHUB_API_URL, GITHUB_TOKEN
from app.logger import logger

RAW_DIR = Path("data/raw")
RAW_DIR.mkdir(parents=True, exist_ok=True)


class GitHubExtractor:

    def __init__(self):

        self.base_url = GITHUB_API_URL

        self.session = Session()

        self.session.headers.update({
            "Accept": "application/vnd.github+json",
            "User-Agent": "github-data-pipeline"
        })

        if GITHUB_TOKEN:
            self.session.headers.update({
                "Authorization": f"Bearer {GITHUB_TOKEN}"
            })

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10)
    )
    def search_repositories(
        self,
        language="Python",
        page=1,
        per_page=100
    ):

        logger.info("Fetching repositories...")

        response = self.session.get(
            f"{self.base_url}/search/repositories",
            params={
                "q": f"language:{language}",
                "sort": "stars",
                "page": page,
                "per_page": per_page
            },
            timeout=30
        )

        response.raise_for_status()

        logger.info("GitHub request successful.")

        return response.json()

    def save_raw_data(
        self,
        data,
        filename
    ):

        filepath = RAW_DIR / filename

        with open(filepath, "w", encoding="utf-8") as file:
            json.dump(
                data,
                file,
                indent=2
            )

        logger.info(f"Saved raw file -> {filepath}")

        return filepath


if __name__ == "__main__":

    extractor = GitHubExtractor()

    data = extractor.search_repositories()

    extractor.save_raw_data(
        data,
        "repositories.json"
    )

    print(len(data["items"]))