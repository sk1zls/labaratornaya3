import pytest
from datetime import date
from unittest.mock import Mock, patch
from services import ExpenseService, BudgetService
from models import Expense

def test_add_expense_success():
    mock_exp_repo = Mock()
    mock_budget_repo = Mock()
    mock_budget_repo.get_limit.return_value = None
    
    with patch('services.ExpenseRepository', mock_exp_repo), \
         patch('services.BudgetLimitRepository', mock_budget_repo):
        service = ExpenseService()
        amount, category, exp_date = 100.0, "Еда", date(2025, 4, 28)
        
        # Act
        result = service.add_expense(amount, category, exp_date)
        
        # Assert
        assert result is True
        mock_exp_repo.add.assert_called_once()
        added_expense = mock_exp_repo.add.call_args[0][0]
        assert added_expense.amount == amount
        assert added_expense.category == category

def test_add_expense_negative_amount_raises():
    """AAA: добавление расхода с отрицательной суммой вызывает ValueError."""
    service = ExpenseService()
    
    with pytest.raises(ValueError, match="Сумма должна быть положительной"):
        service.add_expense(-50.0, "Транспорт", date.today())