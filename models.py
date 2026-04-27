from dataclasses import dataclass
from datetime import date
from typing import Optional

@dataclass
class Expense:
    id: Optional[int]
    amount: float
    category: str
    date: date
    description: str = ""

@dataclass
class BudgetLimit:
    category: str
    limit_amount: float
    month: int   # 1-12
    year: int