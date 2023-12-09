import pytest
import tkinter as tk
from tkinter import messagebox
from unittest.mock import patch
from project import AccountingProgram


@pytest.fixture
def accounting_program():
    root = tk.Tk()
    app = AccountingProgram(root)
    yield app
    root.destroy()


def test_initialization(accounting_program):
    assert accounting_program.transactions == []


def test_submit_transaction_valid(accounting_program):
    with patch.object(tk.Toplevel, "destroy"):
        with patch.object(messagebox, "showinfo") as mock_showinfo:
            accounting_program.submit_transaction(
                "Test Description", "100.0", "Revenue", tk.Toplevel()
            )
            assert len(accounting_program.transactions) == 1
            mock_showinfo.assert_called_once_with(
                "Record Transaction", "Transaction recorded successfully."
            )


def test_submit_transaction_invalid(accounting_program):
    with patch.object(tk.Toplevel, "destroy"):
        with patch.object(messagebox, "showerror") as mock_showerror:
            accounting_program.submit_transaction(
                "Test Description", "invalid_amount", "Revenue", tk.Toplevel()
            )
            assert len(accounting_program.transactions) == 0
            mock_showerror.assert_called_once_with(
                title="input data error", message="amount must be numeric"
            )


def test_update_treeview(accounting_program):
    with patch.object(accounting_program.tree, "delete") as mock_delete:
        with patch.object(accounting_program.tree, "insert") as mock_insert:
            accounting_program.transactions = [
                {"Description": "Sale", "Amount": 500.0, "Type": "Revenue"},
                {"Description": "Expense", "Amount": 200.0, "Type": "Expense"},
            ]
            accounting_program.update_treeview()
            mock_delete.assert_called_once()
            assert mock_insert.call_count == 2  # One call for each transaction


if __name__ == "__main__":
    pytest.main()
