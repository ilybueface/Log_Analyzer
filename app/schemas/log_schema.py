from pydantic import BaseModel


class PerformanceCheckResponse(BaseModel):
    status: str
    execution_time_seconds: float
    results: list[str]
