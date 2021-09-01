import os
from datetime import datetime
from backend.services.backup_restore.tasks.base_task import Task, TaskStatus
from backend.engine import BACKUP_DIR, UPLOAD_ROOT, DB_BACKUP_DIR
from backend.config.config import get_config_file
from backend.logs.logger import logger


class BackupDatabaseTask(Task):

    def __init__(self) -> None:
        Task.__init__(
            self,
            name=self.__class__.__name__,
            backup_id=f'{datetime.now().strftime("%Y-%m-%d")}',
            timestamp=datetime.now().isoformat()
        )

    def _pre_check(self):
        if not os.path.exists(f"{UPLOAD_ROOT}/{BACKUP_DIR}/{self.backup_id}/{DB_BACKUP_DIR}"):
            logger.info(
                f"folder: {UPLOAD_ROOT}/{BACKUP_DIR}/{self.backup_id}/{DB_BACKUP_DIR} does not exist. Creating folder")
            os.makedirs(
                f"{UPLOAD_ROOT}/{BACKUP_DIR}/{self.backup_id}/{DB_BACKUP_DIR}")

    def run(self):
        try:
            logger.info(f"Running job: {self.name}")
            self.status = TaskStatus.RUNNING
            self._pre_check()
            backup_result = self._backup_database()
            self.result.update(backup_result)
            self.status = TaskStatus.SUCCESS
        except Exception as e:
            self.status = TaskStatus.FAILED
            self.result.update({"error": str(e)})

        return self.to_dict()

    def _backup_database(self):
        logger.info(f"Back up database content...")
        db_dict = get_config_file().get("database_info")
        file_dir = f"{UPLOAD_ROOT}/{BACKUP_DIR}/{self.backup_id}/{DB_BACKUP_DIR}/backup.sql"
        dump_cmd = f'mysqldump -h {db_dict.get("address")} -u {db_dict.get("user")} -p{db_dict.get("password")} --databases {db_dict.get("database")} > {file_dir}'
        os.system(dump_cmd)
        return {
            "_backup_database": "success"
        }
