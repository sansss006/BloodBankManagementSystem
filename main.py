import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import sqlite3



# Global variable to store selected donor ID
selected_id = None


# ---------- DATABASE SETUP ----------
def create_table():
    conn = sqlite3.connect("bloodbank.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS donors (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        age INTEGER,
        gender TEXT,
        blood_group TEXT,
        phone TEXT
    )
    """)

    conn.commit()
    conn.close()


# ---------- ADD DONOR ----------
def add_donor():
    name = entry_name.get()
    age = entry_age.get()
    gender = entry_gender.get()
    blood_group = entry_blood.get()
    phone = entry_phone.get()

    if name == "" or blood_group == "":
        messagebox.showerror("Error", "Name and Blood Group are required!")
        return

    conn = sqlite3.connect("bloodbank.db")
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO donors (name, age, gender, blood_group, phone)
    VALUES (?, ?, ?, ?, ?)
    """, (name, age, gender, blood_group, phone))

    conn.commit()
    conn.close()

    messagebox.showinfo("Success", "Donor Added Successfully!")

    clear_fields()
    view_donors()


# ---------- VIEW DONORS ----------
def view_donors():
    for row in tree.get_children():
        tree.delete(row)

    conn = sqlite3.connect("bloodbank.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM donors")
    rows = cursor.fetchall()

    for row in rows:
        tree.insert("", tk.END, values=row)

    conn.close()


# ---------- SEARCH DONOR ----------
def search_donor():
    search_value = entry_search.get()

    if search_value == "":
        messagebox.showerror("Error", "Enter blood group to search!")
        return

    for row in tree.get_children():
        tree.delete(row)

    conn = sqlite3.connect("bloodbank.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM donors WHERE blood_group = ?", (search_value,))
    rows = cursor.fetchall()

    for row in rows:
        tree.insert("", tk.END, values=row)

    conn.close()


# ---------- SELECT DONOR ----------
def select_donor(event):
    global selected_id

    selected_item = tree.focus()
    data = tree.item(selected_item)

    if not data["values"]:
        return

    selected_id = data["values"][0]

    entry_name.delete(0, tk.END)
    entry_name.insert(0, data["values"][1])

    entry_age.delete(0, tk.END)
    entry_age.insert(0, data["values"][2])

    entry_gender.delete(0, tk.END)
    entry_gender.insert(0, data["values"][3])

    entry_blood.delete(0, tk.END)
    entry_blood.insert(0, data["values"][4])

    entry_phone.delete(0, tk.END)
    entry_phone.insert(0, data["values"][5])


# ---------- UPDATE DONOR ----------
def update_donor():
    global selected_id

    if selected_id is None:
        messagebox.showerror("Error", "Select a donor to update!")
        return

    conn = sqlite3.connect("bloodbank.db")
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE donors
    SET name=?, age=?, gender=?, blood_group=?, phone=?
    WHERE id=?
    """, (
        entry_name.get(),
        entry_age.get(),
        entry_gender.get(),
        entry_blood.get(),
        entry_phone.get(),
        selected_id
    ))

    conn.commit()
    conn.close()

    messagebox.showinfo("Success", "Donor Updated Successfully!")

    clear_fields()
    view_donors()


# ---------- DELETE DONOR ----------
def delete_donor():
    global selected_id

    if selected_id is None:
        messagebox.showerror("Error", "Select a donor to delete!")
        return

    conn = sqlite3.connect("bloodbank.db")
    cursor = conn.cursor()

    cursor.execute("DELETE FROM donors WHERE id=?", (selected_id,))

    conn.commit()
    conn.close()

    messagebox.showinfo("Success", "Donor Deleted Successfully!")

    clear_fields()
    view_donors()


# ---------- CLEAR FIELDS ----------
def clear_fields():
    entry_name.delete(0, tk.END)
    entry_age.delete(0, tk.END)
    entry_gender.delete(0, tk.END)
    entry_blood.delete(0, tk.END)
    entry_phone.delete(0, tk.END)


# ---------- MAIN WINDOW ----------
root = tk.Tk()
root.title("Blood Bank Management System")
root.geometry("800x550")

create_table()

# --------- TITLE LABEL ----------
tk.Label(root, 
         text="Blood Bank Management System",
         font=("Arial", 16, "bold")).pack(pady=10)

# ---------- INPUT FRAME ----------
frame_inputs = tk.Frame(root)
frame_inputs.pack(pady=10)

tk.Label(frame_inputs, text="Name").grid(row=0, column=0)
entry_name = tk.Entry(frame_inputs)
entry_name.grid(row=0, column=1)

tk.Label(frame_inputs, text="Age").grid(row=1, column=0)
entry_age = tk.Entry(frame_inputs)
entry_age.grid(row=1, column=1)

tk.Label(frame_inputs, text="Gender").grid(row=2, column=0)
entry_gender = tk.Entry(frame_inputs)
entry_gender.grid(row=2, column=1)

tk.Label(frame_inputs, text="Blood Group").grid(row=3, column=0)
entry_blood = tk.Entry(frame_inputs)
entry_blood.grid(row=3, column=1)

tk.Label(frame_inputs, text="Phone").grid(row=4, column=0)
entry_phone = tk.Entry(frame_inputs)
entry_phone.grid(row=4, column=1)

tk.Button(frame_inputs, text="Add Donor", command=add_donor).grid(row=5, column=0, pady=5)
tk.Button(frame_inputs, text="Update Donor", command=update_donor).grid(row=5, column=1, pady=5)
tk.Button(frame_inputs, text="Delete Donor", command=delete_donor).grid(row=6, columnspan=2, pady=5)


# ---------- SEARCH FRAME ----------
frame_search = tk.Frame(root)
frame_search.pack(pady=5)

tk.Label(frame_search, text="Search by Blood Group:").pack(side=tk.LEFT)

entry_search = tk.Entry(frame_search)
entry_search.pack(side=tk.LEFT, padx=5)

tk.Button(frame_search, text="Search", command=search_donor).pack(side=tk.LEFT)
tk.Button(frame_search, text="Show All", command=view_donors).pack(side=tk.LEFT, padx=5)


# ---------- TABLE ----------
columns = ("ID", "Name", "Age", "Gender", "Blood Group", "Phone")

tree = ttk.Treeview(root, columns=columns, show="headings")
tree.pack(fill="both", expand=True)

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=120)

tree.bind("<<TreeviewSelect>>", select_donor)

view_donors()

root.mainloop()