from dataclasses import dataclass
from typing import Any, Dict, Optional

from pydantic import BaseModel


@dataclass(slots=True)
class BaseAppException(Exception):
    code: str
    message: str
    status_code: int = 400
    details: Optional[Dict[str, Any]] = None
    headers: Optional[Dict[str, str]] = None

    def __str__(self) -> str:
        return f"{self.code}: {self.message}"
    
class ApiError(BaseModel):
    code: str
    message: str
    details: Optional[Dict[str, Any]] = None


