import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from pymongo import MongoClient

class EmployeeDatabaseApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Employee Database Management")

        # Connect to MongoDB
        self.client = MongoClient("mongodb://localhost:27017")
        self.db = self.client["employee_database"]  # Replace with your actual database name
        self.collection = self.db["employees"]

        self.create_widgets()

    def create_widgets(self):
        # Entry Widgets
        self.idLable = ttk.Label(self.root , text="Employee ID :")
        self.idLable.grid(row=0, column=0, padx=5, pady=3)
        self.employee_id_entry = ttk.Entry(self.root, width=30)
        self.employee_id_entry.grid(row=0, column=1, padx=5, pady=3)
        self.employee_id_entry.insert(0, 0 )

        self.nameLable = ttk.Label(self.root , text="Employee Name :")
        self.nameLable.grid(row=1, column=0, padx=5, pady=3)
        self.employee_name_entry = ttk.Entry(self.root, width=30)
        self.employee_name_entry.grid(row=1, column=1, padx=5, pady=3)
        self.employee_name_entry.insert(0, "")

        self.ageLable = ttk.Label(self.root , text="Employee Age :")
        self.ageLable.grid(row=2, column=0, padx=5, pady=3)
        self.employee_age_entry = ttk.Entry(self.root, width=30)
        self.employee_age_entry.grid(row=2, column=1, padx=5, pady=3)
        self.employee_age_entry.insert(0 , 0)

        self.countryLable = ttk.Label(self.root , text="Employee Country :")
        self.countryLable.grid(row=3, column=0, padx=5, pady=3)
        self.employee_country_entry = ttk.Entry(self.root, width=30)
        self.employee_country_entry.grid(row=3, column=1, padx=5, pady=3)
        self.employee_country_entry.insert(0, "")

        # Buttons
        insert_button = ttk.Button(self.root, text="Insert Data", command=self.insert)
        insert_button.grid(row=4, column=0, padx=5, pady=10)

        update_button = ttk.Button(self.root, text="Update Data", command=self.update)
        update_button.grid(row=5, column=0, padx=5, pady=10)

        retrieve_button = ttk.Button(self.root, text="Show Data", command=self.retrieve)
        retrieve_button.grid(row=5, column=1, padx=5, pady=10)

        delete_button = ttk.Button(self.root, text="Delete Data", command=self.delete)
        delete_button.grid(row=6, column=0, padx=5, pady=3)

    def clear_entries(self):
        # Clear all entry fields
        self.employee_id_entry.delete(0, tk.END)
        self.employee_id_entry.insert(0 , 0)
        self.employee_name_entry.delete(0, tk.END)
        self.employee_age_entry.delete(0, tk.END)
        self.employee_age_entry.insert(0 , 0)
        self.employee_country_entry.delete(0, tk.END)

    def get_entry_values(self):
        employee_id = self.employee_id_entry.get()
        employee_name = self.employee_name_entry.get()
        employee_age = self.employee_age_entry.get()
        employee_country = self.employee_country_entry.get()

        try:
            # Validate and convert age to an integer
            employee_age = int(employee_age)
        except ValueError:
            # Handle the case where age is not a valid integer
            messagebox.showerror("Error", "Invalid age. Please enter a valid integer.")
            return None

        try:
            # Validate and convert ID to an integer
            employee_id = int(employee_id)
        except ValueError:
            # Handle the case where ID is not a valid integer
            messagebox.showerror("Error", "Invalid ID. Please enter a valid integer.")
            return None

        return employee_id, employee_name, employee_age, employee_country

    def insert(self):
        entry_values = self.get_entry_values()

        if entry_values is not None:
            employee_id, employee_name, employee_age, employee_country = entry_values

            data = {
                "Emp_Id": employee_id,
                "Emp_Name": employee_name,
                "Emp_Age": employee_age,
                "Emp_Country": employee_country
            }

            # Insert data into MongoDB
            result = self.collection.insert_one(data)

            if result.inserted_id:
                messagebox.showinfo("Insert Result", "Data inserted successfully")
                self.clear_entries()  # Clear entries after successful insert
            else:
                messagebox.showerror("Insert Result", "Failed to insert data")

    def update(self):
        entry_values = self.get_entry_values()

        if entry_values is not None:
            employee_id, employee_name, employee_age, employee_country = entry_values

            data = {
                "Emp_Id": employee_id,
                "Emp_Name": employee_name,
                "Emp_Age": employee_age,
                "Emp_Country": employee_country
            }

            # Update data in MongoDB
            result = self.collection.update_one({"Emp_Id": employee_id}, {"$set": data})

            if result.modified_count > 0:
                messagebox.showinfo("Update Result", "Data updated successfully")
                self.clear_entries()  # Clear entries after successful update
            else:
                messagebox.showerror("Update Result", "Failed to update data")

    def delete(self):
        entry_values = self.get_entry_values()

        if entry_values is not None:
            employee_id, _, _, _ = entry_values  # Only using the ID for deletion

            # Delete data from MongoDB
            result = self.collection.delete_one({"Emp_Id": employee_id})

            if result.deleted_count > 0:
                messagebox.showinfo("Delete Result", "Data deleted successfully")
                self.clear_entries()  # Clear entries after successful delete
            else:
                messagebox.showerror("Delete Result", "Failed to delete data")

    def retrieve(self):
        entry_values = self.get_entry_values()

        if entry_values is not None:
            employee_id, _, _, _ = entry_values  # Only using the ID for retrieval

            # Retrieve data from MongoDB
            data = self.collection.find_one({"Emp_Id": employee_id})

            if data:
                messagebox.showinfo(
                    "Retrieve Result",
                    f"Employee Data:\nID: {data.get('Emp_Id')}\nName: {data.get('Emp_Name')}\nAge: {data.get('Emp_Age')}\nCountry: {data.get('Emp_Country')}"
                )
            else:
                messagebox.showinfo("Retrieve Result", "Employee not found")

if __name__ == "__main__":
    root = tk.Tk()
    app = EmployeeDatabaseApp(root)
    root.mainloop()
