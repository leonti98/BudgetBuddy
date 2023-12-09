import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import locale
import csv


class AccountingProgram:
    def __init__(self, root):
        """
        Initialize the AccountingProgram.

        :param root: The Tkinter root window.
        :type root: Tkinter.Tk
        """
        self.root = root
        self.root.title("Accounting Program")

        # Initialize variables
        self.transactions = []

        # GUI components
        self.label = tk.Label(root, text="Accounting Program", font=("Helvetica", 16))
        self.label.pack(pady=10)

        # Buttons
        self.record_button = tk.Button(
            root, text="Record Transaction", command=self.record_transaction
        )
        self.record_button.pack(pady=5)

        self.financial_button = tk.Button(
            root,
            text="Generate Financial Reports and File Taxes",
            command=self.generate_reports_and_taxes,
        )
        self.financial_button.pack(pady=5)

        # Add a new button to trigger the export
        self.export_button = tk.Button(
            root, text="Export to CSV", command=self.export_to_csv
        )
        self.export_button.pack(pady=5)

        # Treeview for displaying transactions in the main window
        self.tree = ttk.Treeview(
            root,
            columns=("Description", "Amount", "Type"),
            show="headings",
        )
        self.tree.heading("Description", text="Description")
        self.tree.heading("Amount", text="Amount")
        self.tree.heading("Type", text="Type")
        self.tree.pack(pady=10)

    def export_to_csv(self):
        """
        Export transactions to a CSV file.

        This method prompts the user for a file name and exports the recorded transactions to a CSV file.

        :return: None
        """
        # Ask the user for the file name to save the CSV
        file_name = simpledialog.askstring(
            "Export to CSV", "Enter the file name (without extension):"
        )

        if file_name:
            # Add .csv extension if not provided
            file_name = (
                f"{file_name}.csv" if not file_name.endswith(".csv") else file_name
            )

            # Write transactions to CSV file
            with open(file_name, mode="w", newline="") as file:
                writer = csv.writer(file)
                # Write header
                writer.writerow(["Description", "Amount", "Type"])
                # Write transactions
                for transaction in self.transactions:
                    writer.writerow(
                        [
                            transaction["Description"],
                            transaction["Amount"],
                            transaction["Type"],
                        ]
                    )

            messagebox.showinfo(
                "Export to CSV", f"Transactions exported to {file_name}."
            )

    def record_transaction(self):
        """
        Open a window to record a new expense transaction.

        This method creates a new toplevel window for recording an expense transaction.
        It includes entry fields for the description, amount, and transaction category.
        The user can submit the transaction, and it will be added to the list of transactions.

        :return: None
        """
        # Create a Toplevel window for the transaction input
        transaction_window = tk.Toplevel(self.root)
        transaction_window.title("Record Transaction")

        # Label and Entry for Description
        tk.Label(transaction_window, text="Description:").pack(pady=5)
        description_entry = tk.Entry(transaction_window)
        description_entry.pack(pady=5)

        # Label and Entry for Amount
        tk.Label(transaction_window, text="Amount:").pack(pady=5)
        amount_entry = tk.Entry(transaction_window)
        amount_entry.pack(pady=5)

        # Label and Dropdown for Transaction Type
        tk.Label(transaction_window, text="Transaction Type:").pack(pady=5)
        transaction_types = ["Income", "Expense"]
        type_var = tk.StringVar(transaction_window)
        type_var.set(transaction_types[0])  # Set the default value
        type_dropdown = tk.OptionMenu(transaction_window, type_var, *transaction_types)
        type_dropdown.pack(pady=5)

        # Button to submit the transaction
        submit_button = tk.Button(
            transaction_window,
            text="Submit",
            command=lambda: self.submit_transaction(
                description_entry.get(),
                amount_entry.get(),
                type_var.get(),
                transaction_window,
            ),
        )

        submit_button.pack(pady=10)

    def submit_transaction(self, description, amount, transaction_type, window):
        """
        This method records the submitted transaction, updates the treeview, and notifies the user.

        :param description: The description of the transaction.
        :type description: str

        :param amount: The amount of the transaction.
        :type amount: float
        :raise ValueError: if amount is not numeric error messagebox.

        :param transaction_type: The type of the transaction (Income or Expense).
        :type transaction_type: str

        :param window: The Tkinter window to be destroyed after submitting.
        :type window: Tkinter.Toplevel

        :return: None
        """
        try:
            amount = float(amount)
            transaction = {
                "Description": description,
                "Amount": amount,
                "Type": transaction_type,
            }
            self.transactions.append(transaction)
            messagebox.showinfo(
                "Record Transaction", "Transaction recorded successfully."
            )
            window.destroy()
            self.update_treeview()

        except ValueError:
            messagebox.showerror(
                title="input data error", message="amount must be numeric"
            )
            pass

    def generate_reports_and_taxes(self):
        """
        Generate financial reports and file taxes.

        This method calculates and displays financial reports, including total Income, total expense, net income, and profit after tax.
        It also calculates and displays taxes based on total sales.

        :return: None
        """
        try:
            # Calculate and display financial reports
            total_Income = sum(
                transaction["Amount"]
                for transaction in self.transactions
                if transaction["Type"] == "Income"
            )
            total_expense = sum(
                transaction["Amount"]
                for transaction in self.transactions
                if transaction["Type"] == "Expense"
            )
            net_income = total_Income - total_expense

            # Calculate and display taxes
            total_sales = total_Income
            sales_tax_rate = 0.1  # 10% sales tax rate for demonstration
            sales_tax = total_sales * sales_tax_rate

            # Calculate profit after tax
            profit_after_tax = net_income - sales_tax

            reports_text = f"Financial Reports:\n\nTotal Income: {total_Income}\nTotal Expense: {total_expense}\nNet Income: {net_income}"

            reports_text += (
                f"\n\nTotal Sales: {total_sales}\nSales Tax (10%): {sales_tax}"
            )

            reports_text += f"\nProfit After Tax: {profit_after_tax}"
            messagebox.showinfo("Generate Reports and File Taxes", reports_text)

        except Exception as e:
            messagebox.showerror(
                "Error", f"Error generating reports and taxes: {str(e)}"
            )

    def update_treeview(self):
        """
        Update the Treeview in the main window with updated transactions.

        This method clears the Treeview in the main window and repopulates it with the latest transactions.

        :return: None
        """
        # Clear the Treeview in the main window and repopulate it with updated transactions
        self.tree.delete(*self.tree.get_children())
        for idx, transaction in enumerate(self.transactions):
            formatted_amount = locale.currency(transaction["Amount"], grouping=True)
            self.tree.insert(
                "",
                idx,
                values=(
                    transaction["Description"],
                    formatted_amount,
                    transaction["Type"],
                ),
            )

    locale.setlocale(locale.LC_ALL, "")


def main():
    root = tk.Tk()
    app = AccountingProgram(root)
    root.mainloop()
    # Set the locale for currency formatting


if __name__ == "__main__":
    main()
