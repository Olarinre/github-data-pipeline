import time

from app.etl.extract import GitHubExtractor
from app.etl.transform import GitHubTransformer
from app.etl.load import GitHubLoader
from app.logger import logger


class GitHubPipeline:

    def __init__(self):

        self.extractor = GitHubExtractor()
        self.transformer = GitHubTransformer()
        self.loader = GitHubLoader()

    def run(self):

        logger.info("=" * 60)
        logger.info("Starting GitHub ETL Pipeline")

        start_time = time.perf_counter()

        # ---------------- Extract ----------------

        extract_start = time.perf_counter()

        raw_data = self.extractor.search_repositories()

        extract_time = time.perf_counter() - extract_start

        repository_count = len(raw_data.get("items", []))

        logger.info(
            f"Extracted {repository_count} repositories "
            f"in {extract_time:.2f} seconds."
        )

        # Save raw JSON
        self.extractor.save_raw_data(
            raw_data,
            "repositories.json"
        )

        # ---------------- Transform ----------------

        transform_start = time.perf_counter()

        df = self.transformer.transform(raw_data)

        transform_time = time.perf_counter() - transform_start

        logger.info(
            f"Transformed {len(df)} repositories "
            f"in {transform_time:.2f} seconds."
        )

        # ---------------- Load ----------------

        load_start = time.perf_counter()

        self.loader.load(df)

        load_time = time.perf_counter() - load_start

        logger.info(
            f"Loaded {len(df)} repositories "
            f"in {load_time:.2f} seconds."
        )

        total_time = time.perf_counter() - start_time

        logger.info(
            f"Pipeline completed successfully "
            f"in {total_time:.2f} seconds."
        )

        logger.info("=" * 60)


if __name__ == "__main__":

    pipeline = GitHubPipeline()

    pipeline.run()