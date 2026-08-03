from apscheduler.schedulers.blocking import BlockingScheduler

from app.etl.pipeline import GitHubPipeline
from app.logger import logger
from app.etl.metadata import PipelineMetadata

pipeline = GitHubPipeline()
metadata = PipelineMetadata()
scheduler = BlockingScheduler()


@scheduler.scheduled_job(
    "interval",
    hours=1, # Run the pipeline every hour. could be changed to minutes or seconds.
    max_instances=1, #prevent overlapping runs
    coalesce=True, #if a run is missed, run it immediately.
)

def run_pipeline():

    logger.info("Scheduled pipeline started.")

    pipeline.run()


if __name__ == "__main__":

    logger.info("Scheduler started.")

    try:

        scheduler.start()

    except (KeyboardInterrupt, SystemExit):

        logger.info("Scheduler stopped.")