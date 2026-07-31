from datetime import datetime

import pandas as pd

from app.logger import logger


class GitHubTransformer:
    """
    Transforms raw GitHub API responses into a clean DataFrame.
    """

    def transform(self, raw_data) -> pd.DataFrame:
        """
        Transform the raw GitHub API response into a pandas DataFrame.
        """

        # Safely get the list of repositories
        items = raw_data.get("items", [])

        if not items:
            logger.warning("No repositories found in the API response.")
            return pd.DataFrame()

        repositories = []

        for repo in items:

            record = {
                "repo_name": repo.get("full_name"),
                "owner": repo.get("owner", {}).get("login"),
                "language": repo.get("language"),
                "stars": repo.get("stargazers_count", 0),
                "forks": repo.get("forks_count", 0),
                "open_issues": repo.get("open_issues_count", 0),
                "created_at": repo.get("created_at"),
                "updated_at": repo.get("updated_at"),
                "scraped_at": datetime.utcnow(),
            }

            repositories.append(record)

        # Convert to DataFrame
        df = pd.DataFrame(repositories)

        # Convert date columns
        date_columns = ["created_at", "updated_at"]

        for column in date_columns:
            df[column] = pd.to_datetime(df[column])

        # Fill missing languages
        df["language"] = df["language"].fillna("Unknown")

        # Remove duplicate repositories
        df = df.drop_duplicates(subset=["repo_name"])

        # Validate required columns
        required_columns = [
            "repo_name",
            "owner",
            "stars",
        ]

        for column in required_columns:
            if df[column].isnull().any():
                raise ValueError(f"Column '{column}' contains null values.")

        logger.info(f"Successfully transformed {len(df)} repositories.")

        return df


if __name__ == "__main__":

    from app.etl.extract import GitHubExtractor

    extractor = GitHubExtractor()

    raw_data = extractor.search_repositories()

    transformer = GitHubTransformer()

    df = transformer.transform(raw_data)

    print(df.head())

    print(f"\nTotal repositories: {len(df)}")