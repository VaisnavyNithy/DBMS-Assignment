import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
import matplotlib.pyplot as plt
from openpyxl import Workbook

# ================= DATABASE =================
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="dbms_programming"
)
cursor = conn.cursor()

# ================= MAIN APP =================
def main_app():
    root = tk.Tk()
    root.title("News System")
    root.geometry("1400x850")

    notebook = ttk.Notebook(root)
    notebook.pack(fill='both', expand=True)

    # ================= UTIL =================
    def execute(query, params=()):
        try:
            cursor.execute(query, params)
            conn.commit()
        except Exception as e:
            messagebox.showerror("DB Error", str(e))

    # ================= TREE =================
    def create_tree(parent, cols):
        frame = ttk.Frame(parent)
        frame.pack(fill='both', expand=True)

        tree = ttk.Treeview(frame, columns=cols, show='headings')

        for c in cols:
            tree.heading(c, text=c)
            tree.column(c, width=120)

        vsb = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        hsb = ttk.Scrollbar(frame, orient="horizontal", command=tree.xview)

        tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")

        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        return tree

    # ================= SEARCH =================
    def search_tree(tree, query, table, cols):
        tree.delete(*tree.get_children())
        sql = f"SELECT * FROM {table} WHERE CONCAT_WS(' ', {','.join(cols)}) LIKE %s"
        cursor.execute(sql, ('%' + query + '%',))
        for row in cursor.fetchall():
            tree.insert("", tk.END, values=row)

    # ================= EXPORT EXCEL =================
    def export_excel(table):
        wb = Workbook()
        ws = wb.active

        cursor.execute(f"SELECT * FROM {table}")
        rows = cursor.fetchall()

        ws.append([i[0] for i in cursor.description])
        for r in rows:
            ws.append(r)

        wb.save(f"{table}.xlsx")
        messagebox.showinfo("Success", f"{table}.xlsx exported")

    # ================= USERS =================
    user_frame = ttk.Frame(notebook)
    notebook.add(user_frame, text="Users")

    left = ttk.Frame(user_frame)
    right = ttk.Frame(user_frame)
    left.pack(side="left", fill="y")
    right.pack(side="right", fill="both", expand=True)

    uid = tk.Entry(left)
    uname = tk.Entry(left)
    uemail = tk.Entry(left)

    tk.Label(left, text="ID").grid(row=0, column=0)
    tk.Label(left, text="Name").grid(row=1, column=0)
    tk.Label(left, text="Email").grid(row=2, column=0)

    uid.grid(row=0, column=1)
    uname.grid(row=1, column=1)
    uemail.grid(row=2, column=1)

    search_entry = tk.Entry(left)
    search_entry.grid(row=3, column=0, columnspan=2)

    user_tree = create_tree(right, ("User_Id","Name","Email"))

    def load_users():
        user_tree.delete(*user_tree.get_children())
        cursor.execute("SELECT * FROM User")
        for r in cursor.fetchall():
            user_tree.insert("", tk.END, values=r)

    def add_user():
        execute("INSERT INTO User VALUES (%s,%s,%s)", (uid.get(), uname.get(), uemail.get()))
        load_users()

    def update_user():
        execute("UPDATE User SET Name=%s, Email=%s WHERE User_Id=%s",
                (uname.get(), uemail.get(), uid.get()))
        load_users()

    def delete_user():
        execute("DELETE FROM User WHERE User_Id=%s", (uid.get(),))
        load_users()

    def search_user():
        search_tree(user_tree, search_entry.get(), "User", ["User_Id","Name","Email"])

    tk.Button(left, text="Add", command=add_user).grid(row=4,column=0)
    tk.Button(left, text="Update", command=update_user).grid(row=4,column=1)
    tk.Button(left, text="Delete", command=delete_user).grid(row=5,column=0)
    tk.Button(left, text="Search", command=search_user).grid(row=5,column=1)
    tk.Button(left, text="Export Excel", command=lambda: export_excel("User")).grid(row=6,column=0)

    # ================= ARTICLE VIEWS =================
    view_frame = ttk.Frame(notebook)
    notebook.add(view_frame, text="Article Views")

    tree_view = create_tree(view_frame, ("View_Id","Article_Id","User_Id","View_Date"))

    def load_views():
        tree_view.delete(*tree_view.get_children())
        cursor.execute("SELECT * FROM Article_View")
        for r in cursor.fetchall():
            tree_view.insert("", tk.END, values=r)

    load_views()

    # ================= REPORTS =================
    report_frame = ttk.Frame(notebook)
    notebook.add(report_frame, text="Reports")

    def show_chart():
        cursor.execute("SELECT Article_id, COUNT(*) FROM Article_View GROUP BY Article_id")
        data = cursor.fetchall()
        if not data:
            return
        x = [r[0] for r in data]
        y = [r[1] for r in data]
        plt.bar(x,y)
        plt.show()

    tk.Button(report_frame, text="Show Chart", command=show_chart).pack(pady=10)

    # ================= LOAD =================
    load_users()

    root.mainloop()

# ================= START APP DIRECTLY =================
main_app()

cursor.close()
conn.close()
