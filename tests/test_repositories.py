import pytest
import tempfile
from pathlib import Path
from datetime import date
import database
from repositories import ExpenseRepository
from models import Expense

@pytest.fixture
def temp_db():
    """Временная БД для изолированного тестирования репозиториев."""
    original_name = database.DB_NAME
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp:
        tmp_path = tmp.name
    database.DB_NAME = tmp_path
    database.init_db()  # создаём таблицы
    yield tmp_path
    # закрываем соединения (если они ещё открыты)
    try:
        Path(tmp_path).unlink()
    except PermissionError:
        pass
    finally:
        database.DB_NAME = original_name

def test_expense_repository_add_and_get_all(temp_db):
    """Проверка добавления и получения всех расходов."""
    expense = Expense(id=None, amount=42.0, category="Тест", date=date(2025,4,28))
    expense_id = ExpenseRepository.add(expense)
    all_expenses = ExpenseRepository.get_all()
    assert expense_id is not None
    assert len(all_expenses) == 1
    assert all_expenses[0].amount == 42.0
    assert all_expenses[0].category == "Тест"