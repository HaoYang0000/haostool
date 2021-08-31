from datetime import datetime
import logging
import os
import shutil
from backend.services.backup_restore.tasks.base_task import Task, TaskStatus
from backend.engine import BACKUP_DIR, UPLOAD_ROOT, USER_PROFILE_DIR
logger = logging.getLogger(__name__)


class BackupUserProfileTask(Task):

    def __init__(self) -> None:
        Task.__init__(
            self,
            name=self.__class__.__name__,
            backup_id=f'{datetime.now().strftime("%Y-%m-%d")}',
            timestamp=datetime.now().isoformat()
        )

    def _pre_check(self):
        if not os.path.exists(f"{UPLOAD_ROOT}/{BACKUP_DIR}/{self.backup_id}/{USER_PROFILE_DIR}"):
            logger.info(
                f"folder: {UPLOAD_ROOT}/{BACKUP_DIR}/{self.backup_id}/{USER_PROFILE_DIR} does not exist. Creating folder")
            os.makedirs(
                f"{UPLOAD_ROOT}/{BACKUP_DIR}/{self.backup_id}/{USER_PROFILE_DIR}")

    def run(self):
        try:
            logger.info(f"Running job: {self.name}")
            self.status = TaskStatus.RUNNING
            self._pre_check()
            backup_result = self._backup_user_profile_content()
            self.result.update(backup_result)
            self.status = TaskStatus.SUCCESS
        except Exception as e:
            self.status = TaskStatus.FAILED
            self.result.update({"error": str(e)})

        return self.to_dict()

    def _backup_user_profile_content(self):
        logger.info(f"Back up user profile content...")
        source_dir = f'{UPLOAD_ROOT}/{USER_PROFILE_DIR}/'
        target_dir = f'{UPLOAD_ROOT}/{BACKUP_DIR}/{self.backup_id}/{USER_PROFILE_DIR}/'
        sre_files = os.listdir(source_dir)
        for file_name in sre_files:
            full_file_name = os.path.join(source_dir, file_name)
            target_file_name = os.path.join(target_dir, file_name)
            if os.path.isdir(full_file_name):
                logger.info(f"Skipping {full_file_name} because it's a dir")
                continue
            logger.info(f"copy {full_file_name} to {target_file_name}")
            shutil.copy2(full_file_name, target_file_name)

        return {
            "_backup_user_profile_content": "success"
        }
