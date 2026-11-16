from pydantic import BaseModel
from enum import Enum


class CheckStatus(str, Enum):
    ALL_SUCCESS = "all_success"
    PARTIAL_SUCCESS = "partial_success"
    ALL_FAILED = "all_failed"


class SingleStatusCheck(str, Enum):
    SUCCESS = "success"
    FAILED = "failed"


class PerformanceCheckResponse(BaseModel):
    status: CheckStatus
    execution_time_seconds: float
    results: list[str]


class PerformanceCheckSingleResponse(BaseModel):
    status: SingleStatusCheck
    execution_time_seconds: float
    results: list[str]
