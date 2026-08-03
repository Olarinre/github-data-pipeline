import datetime
import time

from app.etl.extract import GitHubExtractor
from app.etl.transform import GitHubTransformer
from app.etl.load import GitHubLoader
from app.logger import logger
from app.quality.validation import DataValidator
from app.etl.metadata import PipelineMetadata




class GitHubPipeline:

    def __init__(self):

        self.extractor = GitHubExtractor()
        self.transformer = GitHubTransformer()
        self.loader = GitHubLoader()
        self.validator = DataValidator()
        self.metadata = PipelineMetadata()

    def run(self):

        logger.info("=" * 60)
        logger.info("Starting GitHub ETL Pipeline")

        start_datetime = datetime.utcnow()
        start_time = time.perf_counter()

        # Initialize variables so they always exist
        rows_loaded = 0
        repository_count = 0
        error_message = None
        status = "SUCCESS"

        try:

            # ---------------- Extract ----------------

            raw_data = self.extractor.search_repositories()

            repository_count = len(raw_data.get("items", []))

            self.extractor.save_raw_data(
                raw_data,
            "repositories.json"
            )

            # ---------------- Transform ----------------

            df = self.transformer.transform(raw_data)

            # ---------------- Validate ----------------

            self.validator.validate(df)

            # ---------------- Load ----------------

            self.loader.load(df)

            rows_loaded = len(df)

        except Exception as e:

            status = "FAILED"

            error_message = str(e)

            logger.exception("Pipeline failed.")

            raise

        finally:

            end_datetime = datetime.utcnow()

            total_runtime = time.perf_counter() - start_time

            logger.info(
            f"Pipeline finished in {total_runtime:.2f} seconds."
            )

            self.metadata.record_run(
                pipeline_name="GitHub ETL",
                start_time=start_datetime,
                end_time=end_datetime,
                status=status,
                rows_extracted=repository_count,
                rows_loaded=rows_loaded,
                error_message=error_message,
            )

            logger.info("=" * 60)

if __name__ == "__main__":

    pipeline = GitHubPipeline()

    pipeline.run()