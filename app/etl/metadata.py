from datetime import datetime

from app.database import SessionLocal
from app.models import PipelineRun


class PipelineMetadata:

    def __init__(self):
        self.session = SessionLocal()

    def record_run(
        self,
        pipeline_name,
        start_time,
        end_time,
        status,
        rows_extracted,
        rows_loaded,
        error_message=None,
    ):

        run = PipelineRun(
            pipeline_name=pipeline_name,
            start_time=start_time,
            end_time=end_time,
            duration_seconds=int(
                (end_time - start_time).total_seconds()
            ),
            status=status,
            rows_extracted=rows_extracted,
            rows_loaded=rows_loaded,
            error_message=error_message,
        )

        self.session.add(run)
        self.session.commit()
        self.session.close()