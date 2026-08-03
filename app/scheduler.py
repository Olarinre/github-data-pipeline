from apscheduler.schedulers.blocking import BlockingScheduler

from app.etl.pipeline import GitHubPipeline
from app.logger import logger

pipeline = GitHubPipeline()

scheduler = BlockingScheduler()


@scheduler.scheduled_job(
    "interval",
    hours=1, # Run the pipeline every hour. could be changed to minutes or seconds.
)
def run_pipeline():

    logger.info("Scheduled pipeline started.")

    pipeline.run()


if __name__ == "__main__":

    logger.info("Scheduler started.")

    scheduler.start()