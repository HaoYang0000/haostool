from typing import Dict
from enum import Enum


class TaskStatus(str, Enum):
    INIT = "INIT"
    RUNNING = "RUNNING"
    FAILED = "FAILED"
    SUCCESS = "SUCCESS"


class Task(object):
    name: str
    backup_id: str
    timestamp: str
    status: str
    result: Dict

    def __init__(self, name: str, backup_id: str, timestamp: str) -> None:
        self.name = name
        self.backup_id = backup_id
        self.timestamp = timestamp
        self.status = TaskStatus.INIT
        self.result = dict()

    def run(self):
        raise NotImplementedError(self.__class__)

    def to_dict(self) -> Dict:
        return vars(self)
