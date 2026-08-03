from app.logger import logger


class DataValidator:

    REQUIRED_COLUMNS = [
        "repo_name",
        "owner",
        "stars",
        "created_at",
        "updated_at",
    ]

    def validate(self, df):

        logger.info("Running data quality checks...")

        if df.empty:
            raise ValueError("DataFrame is empty.")

        # Check required columns
        missing_columns = [
            col for col in self.REQUIRED_COLUMNS
            if col not in df.columns
        ]

        if missing_columns:
            raise ValueError(
                f"Missing columns: {missing_columns}"
            )

        # Check nulls
        for column in self.REQUIRED_COLUMNS:

            if df[column].isnull().any():

                raise ValueError(
                    f"Column '{column}' contains null values."
                )

        # Duplicate repositories

        duplicates = df["repo_name"].duplicated().sum()

        if duplicates > 0:

            raise ValueError(
                f"{duplicates} duplicate repositories found."
            )

        # Negative values

        numeric_columns = [
            "stars",
            "forks",
            "open_issues",
        ]

        for column in numeric_columns:

            if (df[column] < 0).any():

                raise ValueError(
                    f"{column} contains negative values."
                )

        logger.info("Data quality checks passed.")

        return True


