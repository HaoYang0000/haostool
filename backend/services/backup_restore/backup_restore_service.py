import json
import shutil
import os
from datetime import datetime
from backend.models.backups.backup import BackupModel
from backend.services.base import BaseService
from sqlalchemy import asc
from backend.engine import session_scope, UPLOAD_ROOT, BACKUP_DIR
from backend.services.backup_restore.tasks import (
    BackupBlogTask,
    BackupVideoTask,
    BackupUserProfileTask,
    BackupDatabaseTask,
    RestoreBlogTask,
    RestoreVideoTask,
    RestoreUserProfileTask,
    RestoreDatabaseTask
)
from backend.logs.logger import logger


class BackupRestoreService(BaseService):
    model = BackupModel

    def get_backup_records(self, name: str = ""):
        try:
            with session_scope() as session:
                if name:
                    return session.query(self.model).filter(self.model.name == name).all()
                return session.query(self.model).all()
        except Exception:
            return []

    def get_backup_files(self):
        target_dir = f'{UPLOAD_ROOT}/{BACKUP_DIR}/'
        files = []
        for file in os.listdir(target_dir):
            if not os.path.isdir(f'{UPLOAD_ROOT}/{BACKUP_DIR}/{file}'):
                files.append(file)
        return files

    def get_backup_file_path(self, file_name: str) -> str:
        return f'{UPLOAD_ROOT}/{BACKUP_DIR}', f'{file_name}.zip'

    def create_backup(self):
        job_status = {}
        jobs = [
            BackupBlogTask,
            BackupVideoTask,
            BackupUserProfileTask,
            BackupDatabaseTask
        ]
        for job in jobs:
            result = job().run()
            job_status[job.__name__] = result
        logger.info("All backup jobs done.")
        logger.info("Start packing...")
        name = f'{datetime.now().strftime("%Y-%m-%d")}'
        shutil.make_archive(
            base_name=f'{UPLOAD_ROOT}/{BACKUP_DIR}/{name}',
            format='zip',
            root_dir=f'{UPLOAD_ROOT}/{BACKUP_DIR}/{name}'
        )
        shutil.rmtree(f'{UPLOAD_ROOT}/{BACKUP_DIR}/{name}')
        logger.info("Packing done.")
        with session_scope() as session:
            logger.info("Creating db record.")
            new_backup = BackupModel(
                name=name,
                job_status=json.dumps(job_status, indent=4)
            )
            session.add(new_backup)
            session.commit()
            logger.info("Creating db record done.")
        return "Create backup success"

    def delete_backup_record(self, backup_id: str = "", name: str = "", with_file: bool = False):
        with session_scope() as session:
            if with_file is True:
                os.remove(f'{UPLOAD_ROOT}/{BACKUP_DIR}/{name}.zip')
                session.query(self.model).filter(
                    self.model.name == name).delete()
                session.commit()
                if os.path.isdir(f'{UPLOAD_ROOT}/{BACKUP_DIR}/{name}'):
                    shutil.rmtree(f'{UPLOAD_ROOT}/{BACKUP_DIR}/{name}')
            else:
                record = session.query(self.model).filter(
                    self.model.id == backup_id).one()
                session.delete(record)
                session.commit()
            return "Delete backup record success"

    def restore_record_and_files(self, file_name: str):
        dir_name = file_name.split('.')[0]
        shutil.unpack_archive(
            filename=f'{UPLOAD_ROOT}/{BACKUP_DIR}/{file_name}',
            extract_dir=f'{UPLOAD_ROOT}/{BACKUP_DIR}/{dir_name}',
            format='zip'
        )
        job_status = {}
        jobs = [
            RestoreBlogTask,
            RestoreVideoTask,
            RestoreUserProfileTask,
            RestoreDatabaseTask
        ]
        for job in jobs:
            result = job().run()
            job_status[job.__name__] = result
        shutil.rmtree(f'{UPLOAD_ROOT}/{BACKUP_DIR}/{dir_name}')
        return "Restore backup success"
