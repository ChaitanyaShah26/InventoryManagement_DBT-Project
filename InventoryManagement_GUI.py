import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

# Database connection function
def create_connection():
    try:
        conn = mysql.connector.connect(
            host="localhost",        
            user="root",             
            password="pass@123",     
            database="InventoryManagement"  
        )
        return conn
    except mysql.connector.Error as e:
        messagebox.showerror("Connection Error", f"Error connecting to database: {e}")
        return None

# Main application class
class InventoryManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Inventory Management System")
        self.root.geometry("800x600")

        # Label and buttons for each table
        tk.Label(self.root, text="Select a Table to Manage", font=("Arial", 18)).pack(pady=10)

        # Buttons to manage tables
        self.manage_buttons = {
            "Employees": self.manage_employees,
            "Customer Care": self.manage_customer_care,
            "Warehouse": self.manage_warehouse,
            "Providers": self.manage_providers,
            "Products": self.manage_products,
            "Offers": self.manage_offers,
            "Customers": self.manage_customers,
            "Payments": self.manage_payments,
            "Online Payments": self.manage_online,
            "Offline Payments": self.manage_offline
        }

        for table_name, action in self.manage_buttons.items():
            tk.Button(self.root, text=f"Manage {table_name}", command=action, width=20).pack(pady=5)

    def manage_employees(self):
        self.manage_table("employee", ["e_id", "e_name", "e_age", "e_experience"])

    def manage_customer_care(self):
        self.manage_table("customer_care", ["cc_id", "cc_contact", "cc_location", "e_id"])

    def manage_warehouse(self):
        self.manage_table("warehouse", ["w_no", "w_capacity", "w_location"])

    def manage_providers(self):
        self.manage_table("provider", ["pr_id", "pr_type", "pr_address"])

    def manage_products(self):
        self.manage_table("products", ["p_id", "p_price", "p_expiry"])

    def manage_offers(self):
        self.manage_table("offers", ["o_no", "o_name", "o_type"])

    def manage_customers(self):
        self.manage_table("customer", ["c_id", "c_name", "c_contact", "c_age"])

    def manage_payments(self):
        self.manage_table("payment", ["py_id", "py_time", "py_date", "py_mode"])

    def manage_online(self):
        self.manage_table("online", ["on_upi", "on_credit", "on_debit"])

    def manage_offline(self):
        self.manage_table("offline", ["off_cod"])

    def manage_table(self, table_name, columns):
        # Create a new window for managing the table
        table_window = tk.Toplevel(self.root)
        table_window.title(f"Manage {table_name}")

        # Display all data in a Treeview above the action buttons
        tree_frame = tk.Frame(table_window)
        tree_frame.pack(pady=10)

        tree = ttk.Treeview(tree_frame, columns=columns, show="headings")
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120)
        tree.pack(fill=tk.BOTH, expand=True)

        # Action buttons (Insert, Update, Delete, Retrieve)
        action_frame = tk.Frame(table_window)
        action_frame.pack(pady=10)

        tk.Button(action_frame, text="Insert", command=lambda: self.show_insert_fields(table_window, table_name, columns, tree)).pack(side=tk.LEFT, padx=10)
        tk.Button(action_frame, text="Update", command=lambda: self.show_update_fields(table_window, table_name, columns, tree)).pack(side=tk.LEFT, padx=10)
        tk.Button(action_frame, text="Delete", command=lambda: self.show_delete_fields(table_window, table_name, columns, tree)).pack(side=tk.LEFT, padx=10)
        tk.Button(action_frame, text="Retrieve", command=lambda: self.show_retrieve_fields(table_window, table_name, columns, tree)).pack(side=tk.LEFT, padx=10)

        # Load data when window is opened
        self.view_all_data(tree, table_name)

    def show_insert_fields(self, table_window, table_name, columns, tree):
        self.clear_fields(table_window)  # Clear previous fields if any

        insert_frame = tk.Frame(table_window)
        insert_frame.pack(pady=10)

        entries = []
        for col in columns:
            tk.Label(insert_frame, text=col).pack(side=tk.LEFT, padx=5)
            entry = tk.Entry(insert_frame)
            entry.pack(side=tk.LEFT, padx=5)
            entries.append(entry)

        def add_record():
            values = [entry.get() for entry in entries]
            conn = create_connection()
            if conn:
                try:
                    cursor = conn.cursor()
                    cursor.execute(f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({', '.join(['%s'] * len(columns))})", values)
                    conn.commit()
                    conn.close()
                    messagebox.showinfo("Success", "Record added successfully.")
                    self.view_all_data(tree, table_name)  # Refresh data
                    self.clear_fields(table_window)  # Clear fields after insertion
                    insert_frame.destroy()  # Remove insert fields after operation
                except mysql.connector.IntegrityError as err:
                    messagebox.showerror("Error", f"Duplicate entry or integrity error: {err}")
                except Exception as e:
                    messagebox.showerror("Error", f"An error occurred: {e}")

        tk.Button(insert_frame, text="Add", command=add_record).pack(side=tk.LEFT, padx=5)

    def show_update_fields(self, table_window, table_name, columns, tree):
        self.clear_fields(table_window)  # Clear previous fields if any

        update_frame = tk.Frame(table_window)
        update_frame.pack(pady=10)

        entries = []
        for col in columns:
            tk.Label(update_frame, text=col).pack(side=tk.LEFT, padx=5)
            entry = tk.Entry(update_frame)
            entry.pack(side=tk.LEFT, padx=5)
            entries.append(entry)

        def update_record():
            values = [entry.get() for entry in entries]
            conn = create_connection()
            if conn:
                try:
                    update_stmt = f"UPDATE {table_name} SET " + ", ".join([f"{col} = %s" for col in columns[1:]]) + f" WHERE {columns[0]} = %s"
                    cursor = conn.cursor()
                    cursor.execute(update_stmt, values[1:] + [values[0]])
                    conn.commit()
                    conn.close()
                    messagebox.showinfo("Success", "Record updated successfully.")
                    self.view_all_data(tree, table_name)  # Refresh data
                    self.clear_fields(table_window)  # Clear fields after update
                    update_frame.destroy()  # Remove update fields after operation
                except Exception as e:
                    messagebox.showerror("Error", f"An error occurred: {e}")

        tk.Button(update_frame, text="Update", command=update_record).pack(side=tk.LEFT, padx=5)

    def show_delete_fields(self, table_window, table_name, columns, tree):
        self.clear_fields(table_window)  # Clear previous fields if any

        delete_frame = tk.Frame(table_window)
        delete_frame.pack(pady=10)

        tk.Label(delete_frame, text=f"Enter {columns[0]} to Delete").pack(pady=5)
        delete_entry = tk.Entry(delete_frame)
        delete_entry.pack(pady=5)

        def delete_record():
            record_id = delete_entry.get()
            if not record_id:
                messagebox.showerror("Error", "Please enter an ID to delete.")
                return

            conn = create_connection()
            if conn:
                try:
                    cursor = conn.cursor()
                    cursor.execute(f"DELETE FROM {table_name} WHERE {columns[0]} = %s", (record_id,))
                    conn.commit()

                    if cursor.rowcount == 0:
                        messagebox.showinfo("Not Found", "No record found with the provided ID.")
                    else:
                        messagebox.showinfo("Success", f"Record with {columns[0]} = {record_id} deleted successfully.")
                    conn.close()
                    self.view_all_data(tree, table_name)  # Refresh data
                    self.clear_fields(table_window)  # Clear fields after deletion
                    delete_frame.destroy()  # Remove delete fields after operation
                except Exception as e:
                    messagebox.showerror("Error", f"An error occurred: {e}")

        tk.Button(delete_frame, text="Delete", command=delete_record).pack(pady=5)

    def show_retrieve_fields(self, table_window, table_name, columns, tree):
        self.clear_fields(table_window)  # Clear previous fields if any

        retrieve_frame = tk.Frame(table_window)
        retrieve_frame.pack(pady=10)

        tk.Label(retrieve_frame, text=f"Enter {columns[0]} to Retrieve").pack(pady=5)
        retrieve_entry = tk.Entry(retrieve_frame)
        retrieve_entry.pack(pady=5)

        def retrieve_record():
            record_id = retrieve_entry.get()
            if not record_id:
                messagebox.showerror("Error", "Please enter an ID to retrieve.")
                return

            conn = create_connection()
            if conn:
                try:
                    cursor = conn.cursor()
                    cursor.execute(f"SELECT * FROM {table_name} WHERE {columns[0]} = %s", (record_id,))
                    record = cursor.fetchone()

                    if record:
                        record_str = "\n".join([f"{col}: {val}" for col, val in zip(columns, record)])
                        messagebox.showinfo("Record Found", f"Record:\n{record_str}")
                    else:
                        messagebox.showinfo("Not Found", "No record found with the provided ID.")
                    conn.close()
                    self.clear_fields(table_window)  # Clear fields after retrieve
                    retrieve_frame.destroy()  # Remove retrieve fields after operation
                except Exception as e:
                    messagebox.showerror("Error", f"An error occurred: {e}")

        tk.Button(retrieve_frame, text="Retrieve", command=retrieve_record).pack(pady=5)

    def view_all_data(self, tree, table_name):
        conn = create_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute(f"SELECT * FROM {table_name}")
                records = cursor.fetchall()
                for row in tree.get_children():
                    tree.delete(row)
                for record in records:
                    tree.insert("", "end", values=record)
                conn.close()
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {e}")

    def clear_fields(self, table_window):
        for widget in table_window.winfo_children():
            if isinstance(widget, tk.Entry):
                widget.delete(0, tk.END)

# Run the application
root = tk.Tk()
app = InventoryManagementApp(root)
root.mainloop()
