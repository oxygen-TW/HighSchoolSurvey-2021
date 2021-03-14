from pydantic import BaseModel, Field
from typing import Optional

class frontData(BaseModel):
    stuId: str
    school: str
    sex: int
    grade: int
    department: str
    Q1: int
    Q2: Optional[str] = ""
    Q3: int
    Q4: int
    Q5: int
    Q6: Optional[str] = ""
    Q7: int

