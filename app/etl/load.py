from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.exc import SQLAlchemyError

from app.database import SessionLocal
from app.logger import logger
from app.models import Repository


class GitHubLoader:

    def __init__(self):
        self.session = SessionLocal()

    def load(self, df):

        if df.empty:
            logger.warning("DataFrame is empty. Nothing to load.")
            return

        records = df.to_dict(orient="records")

        try:

            stmt = insert(Repository).values(records)

            stmt = stmt.on_conflict_do_update(
                index_elements=["repo_name"],

                set_={

                    "owner": stmt.excluded.owner,

                    "language": stmt.excluded.language,

                    "stars": stmt.excluded.stars,

                    "forks": stmt.excluded.forks,

                    "open_issues": stmt.excluded.open_issues,

                    "created_at": stmt.excluded.created_at,

                    "updated_at": stmt.excluded.updated_at,

                    "scraped_at": stmt.excluded.scraped_at,
                }
            )

            self.session.execute(stmt)

            self.session.commit()

            logger.info(f"Upserted {len(records)} repositories.")

        except SQLAlchemyError as e:

            self.session.rollback()

            logger.exception("Database error occurred.")

            raise

        finally:

            self.session.close()


if __name__ == "__main__":

    from app.etl.extract import GitHubExtractor
    from app.etl.transform import GitHubTransformer

    extractor = GitHubExtractor()
    transformer = GitHubTransformer()
    loader = GitHubLoader()

    raw = extractor.search_repositories()

    df = transformer.transform(raw)

    loader.load(df)

    print("Pipeline completed successfully.")