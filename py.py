import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from datetime import datetime

class MariaDBApp:
    def __init__(self, root):
        self.root = root
        self.root.title("MariaDB Table Viewer")
        self.root.geometry("800x600")
        self.root.resizable(False, False)
        
        self.login_screen()

    def login_screen(self):
        self.clear_window()

        tk.Label(self.root, text="MariaDB Username:").grid(row=0, column=0, pady=5)
        self.username_entry = tk.Entry(self.root)
        self.username_entry.grid(row=0, column=1, pady=5)

        tk.Label(self.root, text="MariaDB Password:").grid(row=1, column=0, pady=5)
        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.grid(row=1, column=1, pady=5)

        login_button = tk.Button(self.root, text="Login", command=self.connect_db)
        login_button.grid(row=2, column=0, columnspan=2, pady=10)

    def connect_db(self):
        user = self.username_entry.get()
        password = self.password_entry.get()
        database = "lxc"

        try:
            self.db = mysql.connector.connect(
                host="localhost",
                user=user,
                password=password,
                database=database
            )
            self.cursor = self.db.cursor()
            self.show_tables()
        except mysql.connector.Error as err:
            messagebox.showerror("Connection Error", f"Failed to connect: {err}")

    def show_tables(self):
        self.clear_window()
        
        tk.Button(self.root, text="View Tables", command=self.show_table_view).grid(row=0, column=0, pady=5)
        tk.Button(self.root, text="Manage Members", command=self.show_member_management).grid(row=0, column=1, pady=5)
        tk.Button(self.root, text="Manage Fees", command=self.show_fee_management).grid(row=0, column=2, pady=5)
        tk.Button(self.root, text="Financial Reports", command=self.show_financial_reports).grid(row=0, column=3, pady=5)

    def show_table_view(self):
        self.clear_window()
        tk.Button(self.root, text="Back", command=self.show_tables).grid(row=0, column=0, pady=5)
        
        self.cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'lxc'
        """)
        self.tables = [table[0] for table in self.cursor.fetchall()]
        
        tk.Label(self.root, text="Select a table:").grid(row=1, column=0, pady=5)
        self.table_combo = ttk.Combobox(self.root, values=self.tables, state="readonly")
        self.table_combo.grid(row=1, column=1, pady=5)
        self.table_combo.bind("<<ComboboxSelected>>", self.display_table)

        self.text = tk.Text(self.root, width=100, height=30)
        self.text.grid(row=2, column=0, columnspan=2, pady=10)

    def show_member_management(self):
        self.clear_window()
        tk.Button(self.root, text="Back", command=self.show_tables).grid(row=0, column=0, pady=5)
        
        tk.Button(self.root, text="Add Member", command=self.add_member_form).grid(row=1, column=0, pady=5)
        tk.Button(self.root, text="Update Member", command=self.update_member_form).grid(row=1, column=1, pady=5)
        tk.Button(self.root, text="Delete Member", command=self.delete_member_form).grid(row=1, column=2, pady=5)
        tk.Button(self.root, text="Search Members", command=self.search_members_form).grid(row=1, column=3, pady=5)

    def add_member_form(self):
        self.clear_window()
        tk.Button(self.root, text="Back", command=self.show_member_management).grid(row=0, column=0, pady=5)

        self.cursor.execute("SELECT organization_id, name FROM ORGANIZATION")
        orgs = self.cursor.fetchall()
        org_options = [f"{org[0]} - {org[1]}" for org in orgs]
        
        fields = ["Student Number", "First Name", "Middle Initial", "Last Name", "Nickname", "Gender", "Degree Program"]
        self.entries = {}
        
        for i, field in enumerate(fields):
            tk.Label(self.root, text=field + ":").grid(row=i+1, column=0, pady=5)
            self.entries[field] = tk.Entry(self.root)
            self.entries[field].grid(row=i+1, column=1, pady=5)

        tk.Label(self.root, text="Organization:").grid(row=len(fields)+1, column=0, pady=5)
        self.org_combo = ttk.Combobox(self.root, values=org_options, state="readonly")
        self.org_combo.grid(row=len(fields)+1, column=1, pady=5)

        tk.Label(self.root, text="Status:").grid(row=len(fields)+2, column=0, pady=5)
        statuses = ["Active", "Inactive", "Alumni", "Suspended", "Expelled"]
        self.status_combo = ttk.Combobox(self.root, values=statuses, state="readonly")
        self.status_combo.grid(row=len(fields)+2, column=1, pady=5)
        self.status_combo.bind("<<ComboboxSelected>>", self.show_status_fields)

        self.status_frame = tk.Frame(self.root)
        self.status_frame.grid(row=len(fields)+3, column=0, columnspan=2, pady=5)

        tk.Button(self.root, text="Submit", command=self.submit_new_member).grid(row=len(fields)+4, column=0, columnspan=2, pady=10)

    def show_status_fields(self, event=None):
        for widget in self.status_frame.winfo_children():
            widget.destroy()

        status = self.status_combo.get()
        self.status_entries = {}
        
        if status == "Active":
            fields = [("Role", "Ex: Member, President"), ("Committee", "Ex: Creatives, Finance")]
            for i, (field, default) in enumerate(fields):
                tk.Label(self.status_frame, text=field + ":").grid(row=i, column=0, pady=5)
                self.status_entries[field] = tk.Entry(self.status_frame)
                self.status_entries[field].insert(0, default)
                self.status_entries[field].grid(row=i, column=1, pady=5)
                
        elif status in ["Inactive", "Alumni", "Suspended", "Expelled"]:
            date_label = f"Date of {status.lower()}:"
            tk.Label(self.status_frame, text=date_label).grid(row=0, column=0, pady=5)
            self.status_entries["date"] = tk.Entry(self.status_frame)
            self.status_entries["date"].insert(0, datetime.now().strftime('%Y-%m-%d'))
            self.status_entries["date"].grid(row=0, column=1, pady=5)

    def submit_new_member(self):
        try:
            self.cursor.execute("START TRANSACTION")

            member_data = (
                self.entries["Student Number"].get(),
                self.entries["First Name"].get(),
                self.entries["Middle Initial"].get(),
                self.entries["Last Name"].get(),
                self.entries["Nickname"].get(),
                self.entries["Gender"].get(),
                self.entries["Degree Program"].get()
            )
            self.cursor.execute("""
                INSERT INTO MEMBER (student_number, first_name, middle_initial, last_name, 
                nickname, gender, degree_program) VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, member_data)

            membership_id = f"M{self.entries['Student Number'].get()[-3:]}"
            current_year = datetime.now().year
            self.cursor.execute("""
                INSERT INTO MEMBERSHIP (membership_id, year_of_membership, academic_year, semester)
                VALUES (%s, %s, %s, %s)
            """, (membership_id, current_year, f"{current_year}-{current_year+1}", "1st"))

            self.cursor.execute("""
                INSERT INTO MEM_HAS_MEMBERSHIP (student_number, membership_id)
                VALUES (%s, %s)
            """, (self.entries["Student Number"].get(), membership_id))

            org_id = self.org_combo.get().split(" - ")[0]
            self.cursor.execute("""
                INSERT INTO MEM_IN_ORG (membership_id, organization_id)
                VALUES (%s, %s)
            """, (membership_id, org_id))

            status = self.status_combo.get()
            if status == "Active":
                self.cursor.execute("""
                    INSERT INTO ACTIVE_MEMBER (membership_id, role, committee, date_of_being_active)
                    VALUES (%s, %s, %s, CURDATE())
                """, (membership_id, self.status_entries["Role"].get(), self.status_entries["Committee"].get()))
            elif status == "Inactive":
                self.cursor.execute("""
                    INSERT INTO INACTIVE_MEMBER (membership_id, date_of_inactivity)
                    VALUES (%s, %s)
                """, (membership_id, self.status_entries["date"].get()))
            elif status == "Alumni":
                self.cursor.execute("""
                    INSERT INTO ALUMNI_MEMBER (membership_id, date_of_graduation)
                    VALUES (%s, %s)
                """, (membership_id, self.status_entries["date"].get()))
            elif status == "Suspended":
                self.cursor.execute("""
                    INSERT INTO SUSPENDED_MEMBER (membership_id, date_of_suspension)
                    VALUES (%s, %s)
                """, (membership_id, self.status_entries["date"].get()))
            elif status == "Expelled":
                self.cursor.execute("""
                    INSERT INTO EXPELLED_MEMBER (membership_id, date_of_expulsion)
                    VALUES (%s, %s)
                """, (membership_id, self.status_entries["date"].get()))

            self.db.commit()
            messagebox.showinfo("Success", "Member added successfully!")
            self.show_member_management()
        except mysql.connector.Error as err:
            self.db.rollback()
            messagebox.showerror("Error", f"Failed to add member: {err}")

    def update_member_form(self):
        self.clear_window()
        tk.Button(self.root, text="Back", command=self.show_member_management).grid(row=0, column=0, pady=5)

        self.cursor.execute("""
            SELECT m.student_number, m.first_name, m.last_name 
            FROM MEMBER m
        """)
        students = self.cursor.fetchall()
        student_options = [f"{std[0]} - {std[1]} {std[2]}" for std in students]

        tk.Label(self.root, text="Select Student:").grid(row=1, column=0, pady=5)
        self.student_combo = ttk.Combobox(self.root, values=student_options, state="readonly", width=40)
        self.student_combo.grid(row=1, column=1, pady=5)
        self.student_combo.bind("<<ComboboxSelected>>", self.load_member_details)

    def load_member_details(self, event=None):
        student_number = self.student_combo.get().split(" - ")[0]
        try:
            self.cursor.execute("""
                SELECT m.*, o.organization_id, o.name,
                CASE 
                    WHEN am.membership_id IS NOT NULL THEN 'Active'
                    WHEN im.membership_id IS NOT NULL THEN 'Inactive'
                    WHEN alm.membership_id IS NOT NULL THEN 'Alumni'
                    WHEN sm.membership_id IS NOT NULL THEN 'Suspended'
                    WHEN em.membership_id IS NOT NULL THEN 'Expelled'
                END as status
                FROM MEMBER m
                JOIN MEM_HAS_MEMBERSHIP mhm ON m.student_number = mhm.student_number
                JOIN MEM_IN_ORG mio ON mhm.membership_id = mio.membership_id
                JOIN ORGANIZATION o ON mio.organization_id = o.organization_id
                LEFT JOIN ACTIVE_MEMBER am ON mhm.membership_id = am.membership_id
                LEFT JOIN INACTIVE_MEMBER im ON mhm.membership_id = im.membership_id
                LEFT JOIN ALUMNI_MEMBER alm ON mhm.membership_id = alm.membership_id
                LEFT JOIN SUSPENDED_MEMBER sm ON mhm.membership_id = sm.membership_id
                LEFT JOIN EXPELLED_MEMBER em ON mhm.membership_id = em.membership_id
                WHERE m.student_number = %s
            """, (student_number,))
            
            member = self.cursor.fetchone()
            if member:
                fields = ["First Name", "Middle Initial", "Last Name", "Nickname", "Gender", "Degree Program"]
                self.update_entries = {}
                for i, (field, value) in enumerate(zip(fields, member[1:7])):
                    tk.Label(self.root, text=f"New {field}:").grid(row=i+2, column=0, pady=5)
                    self.update_entries[field] = tk.Entry(self.root)
                    self.update_entries[field].insert(0, value)
                    self.update_entries[field].grid(row=i+2, column=1, pady=5)

                self.cursor.execute("SELECT organization_id, name FROM ORGANIZATION")
                orgs = self.cursor.fetchall()
                org_options = [f"{org[0]} - {org[1]}" for org in orgs]
                
                tk.Label(self.root, text="New Organization:").grid(row=len(fields)+2, column=0, pady=5)
                self.update_org_combo = ttk.Combobox(self.root, values=org_options, state="readonly")
                self.update_org_combo.set(f"{member[7]} - {member[8]}")
                self.update_org_combo.grid(row=len(fields)+2, column=1, pady=5)

                tk.Label(self.root, text="New Status:").grid(row=len(fields)+3, column=0, pady=5)
                statuses = ["Active", "Inactive", "Alumni", "Suspended", "Expelled"]
                self.update_status_combo = ttk.Combobox(self.root, values=statuses, state="readonly")
                self.update_status_combo.set(member[9])
                self.update_status_combo.grid(row=len(fields)+3, column=1, pady=5)
                self.update_status_combo.bind("<<ComboboxSelected>>", self.show_update_status_fields)

                self.update_status_frame = tk.Frame(self.root)
                self.update_status_frame.grid(row=len(fields)+4, column=0, columnspan=2, pady=5)

                self.current_membership_id = None
                self.cursor.execute("SELECT membership_id FROM MEM_HAS_MEMBERSHIP WHERE student_number = %s", (student_number,))
                self.current_membership_id = self.cursor.fetchone()[0]

                tk.Button(self.root, text="Update", command=lambda: self.update_member(student_number)).grid(row=len(fields)+5, column=1, pady=10)
            else:
                messagebox.showerror("Error", "Member not found")
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Failed to load member: {err}")

    def show_update_status_fields(self, event=None):
        for widget in self.update_status_frame.winfo_children():
            widget.destroy()

        status = self.update_status_combo.get()
        self.update_status_entries = {}
        
        if status == "Active":
            fields = [("Role", "Member"), ("Committee", "General")]
            for i, (field, default) in enumerate(fields):
                tk.Label(self.update_status_frame, text=field + ":").grid(row=i, column=0, pady=5)
                self.update_status_entries[field] = tk.Entry(self.update_status_frame)
                self.update_status_entries[field].insert(0, default)
                self.update_status_entries[field].grid(row=i, column=1, pady=5)
        elif status in ["Inactive", "Alumni", "Suspended", "Expelled"]:
            date_label = f"Date of {status.lower()}:"
            tk.Label(self.update_status_frame, text=date_label).grid(row=0, column=0, pady=5)
            self.update_status_entries["date"] = tk.Entry(self.update_status_frame)
            self.update_status_entries["date"].insert(0, datetime.now().strftime('%Y-%m-%d'))
            self.update_status_entries["date"].grid(row=0, column=1, pady=5)

    def update_member(self, student_number):
        try:
            self.cursor.execute("START TRANSACTION")

            self.cursor.execute("""
                UPDATE MEMBER SET 
                first_name = %s, middle_initial = %s, last_name = %s,
                nickname = %s, gender = %s, degree_program = %s
                WHERE student_number = %s
            """, (
                self.update_entries["First Name"].get(),
                self.update_entries["Middle Initial"].get(),
                self.update_entries["Last Name"].get(),
                self.update_entries["Nickname"].get(),
                self.update_entries["Gender"].get(),
                self.update_entries["Degree Program"].get(),
                student_number
            ))

            new_org_id = self.update_org_combo.get().split(" - ")[0]
            self.cursor.execute("""
                UPDATE MEM_IN_ORG 
                SET organization_id = %s
                WHERE membership_id = %s
            """, (new_org_id, self.current_membership_id))

            status_tables = ["ACTIVE_MEMBER", "INACTIVE_MEMBER", "ALUMNI_MEMBER", 
                           "SUSPENDED_MEMBER", "EXPELLED_MEMBER"]
            for table in status_tables:
                self.cursor.execute(f"DELETE FROM {table} WHERE membership_id = %s", 
                                  (self.current_membership_id,))

            status = self.update_status_combo.get()
            if status == "Active":
                self.cursor.execute("""
                    INSERT INTO ACTIVE_MEMBER (membership_id, role, committee, date_of_being_active)
                    VALUES (%s, %s, %s, CURDATE())
                """, (self.current_membership_id, 
                      self.update_status_entries["Role"].get(),
                      self.update_status_entries["Committee"].get()))
            elif status in ["Inactive", "Alumni", "Suspended", "Expelled"]:
                table_map = {
                    "Inactive": "INACTIVE_MEMBER",
                    "Alumni": "ALUMNI_MEMBER",
                    "Suspended": "SUSPENDED_MEMBER",
                    "Expelled": "EXPELLED_MEMBER"
                }
                date_field_map = {
                    "Inactive": "date_of_inactivity",
                    "Alumni": "date_of_graduation",
                    "Suspended": "date_of_suspension",
                    "Expelled": "date_of_expulsion"
                }
                self.cursor.execute(f"""
                    INSERT INTO {table_map[status]} (membership_id, {date_field_map[status]})
                    VALUES (%s, %s)
                """, (self.current_membership_id, self.update_status_entries["date"].get()))

            self.db.commit()
            messagebox.showinfo("Success", "Member updated successfully!")
            self.show_member_management()
        except mysql.connector.Error as err:
            self.db.rollback()
            messagebox.showerror("Error", f"Failed to update member: {err}")

    def delete_member_form(self):
        self.clear_window()
        tk.Button(self.root, text="Back", command=self.show_member_management).grid(row=0, column=0, pady=5)

        self.cursor.execute("""
            SELECT m.student_number, m.first_name, m.last_name 
            FROM MEMBER m
        """)
        students = self.cursor.fetchall()
        student_options = [f"{std[0]} - {std[1]} {std[2]}" for std in students]

        tk.Label(self.root, text="Select Student to Delete:").grid(row=1, column=0, pady=5)
        self.delete_student_combo = ttk.Combobox(self.root, values=student_options, state="readonly", width=40)
        self.delete_student_combo.grid(row=1, column=1, pady=5)
        tk.Button(self.root, text="Delete Member", command=self.delete_member).grid(row=1, column=2, pady=5)

    def delete_member(self):
        student_number = self.delete_student_combo.get().split(" - ")[0]
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this member?"):
            try:
                self.cursor.execute("""
                    DELETE m, mhm, mio, am, im, alm, sm, em 
                    FROM MEMBER m
                    LEFT JOIN MEM_HAS_MEMBERSHIP mhm ON m.student_number = mhm.student_number
                    LEFT JOIN MEM_IN_ORG mio ON mhm.membership_id = mio.membership_id
                    LEFT JOIN ACTIVE_MEMBER am ON mhm.membership_id = am.membership_id
                    LEFT JOIN INACTIVE_MEMBER im ON mhm.membership_id = im.membership_id
                    LEFT JOIN ALUMNI_MEMBER alm ON mhm.membership_id = alm.membership_id
                    LEFT JOIN SUSPENDED_MEMBER sm ON mhm.membership_id = sm.membership_id
                    LEFT JOIN EXPELLED_MEMBER em ON mhm.membership_id = em.membership_id
                    WHERE m.student_number = %s
                """, (student_number,))
                self.db.commit()
                messagebox.showinfo("Success", "Member deleted successfully!")
                self.show_member_management()
            except mysql.connector.Error as err:
                self.db.rollback()
                messagebox.showerror("Error", f"Failed to delete member: {err}")

    def search_members_form(self):
        self.clear_window()
        tk.Button(self.root, text="Back", command=self.show_member_management).grid(row=0, column=0, pady=5)

        search_notebook = ttk.Notebook(self.root)
        search_notebook.grid(row=1, column=0, columnspan=3, padx=10, pady=5)

        position_frame = ttk.Frame(search_notebook)
        search_notebook.add(position_frame, text="Search by Position")

        tk.Label(position_frame, text="Enter Position:").grid(row=0, column=0, pady=5)
        self.position_entry = tk.Entry(position_frame)
        self.position_entry.grid(row=0, column=1, pady=5)
        tk.Button(position_frame, text="Search", command=self.search_by_position).grid(row=0, column=2, pady=5)

        tk.Label(position_frame, text="Examples: Member, President, Vice President, etc.", 
                font=("Arial", 8, "italic")).grid(row=1, column=0, columnspan=3, pady=2)

        status_frame = ttk.Frame(search_notebook)
        search_notebook.add(status_frame, text="Search by Status")

        tk.Label(status_frame, text="Select Status:").grid(row=0, column=0, pady=5)
        self.status_combo = ttk.Combobox(status_frame,
            values=["Active", "Inactive", "Alumni", "Suspended", "Expelled"],
            state="readonly")
        self.status_combo.grid(row=0, column=1, pady=5)
        tk.Button(status_frame, text="Search",
                 command=self.search_by_status).grid(row=0, column=2, pady=5)

        self.search_results = tk.Text(self.root, width=70, height=25)
        self.search_results.grid(row=2, column=0, columnspan=3, padx=10, pady=5)
        self.search_results.config(state='disabled')

    def search_by_position(self):
        position = self.position_entry.get()
        try:
            self.cursor.execute("""
                SELECT m.student_number, m.first_name, m.last_name, 
                       o.name as organization, am.role, am.committee
                FROM MEMBER m
                JOIN MEM_HAS_MEMBERSHIP mhm ON m.student_number = mhm.student_number
                JOIN MEM_IN_ORG mio ON mhm.membership_id = mio.membership_id
                JOIN ORGANIZATION o ON mio.organization_id = o.organization_id
                JOIN ACTIVE_MEMBER am ON mhm.membership_id = am.membership_id
                WHERE am.role = %s
                ORDER BY o.name, m.last_name
            """, (position,))
            
            self.display_search_results([
                "Student No.", "Name", "Organization", "Role", "Committee"
            ])

        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Failed to search members: {err}")

    def search_by_status(self):
        status = self.status_combo.get()
        try:
            table_map = {
                "Active": "ACTIVE_MEMBER",
                "Inactive": "INACTIVE_MEMBER",
                "Alumni": "ALUMNI_MEMBER",
                "Suspended": "SUSPENDED_MEMBER",
                "Expelled": "EXPELLED_MEMBER"
            }
            
            date_field = {
                "Active": "date_of_being_active",
                "Inactive": "date_of_inactivity",
                "Alumni": "date_of_graduation",
                "Suspended": "date_of_suspension",
                "Expelled": "date_of_expulsion"
            }
            
            self.cursor.execute(f"""
                SELECT m.student_number, m.first_name, m.last_name, 
                       o.name as organization, stat.{date_field[status]},
                       CASE 
                           WHEN stat.role IS NOT NULL THEN stat.role
                           ELSE ''
                       END as role,
                       CASE 
                           WHEN stat.committee IS NOT NULL THEN stat.committee
                           ELSE ''
                       END as committee
                FROM {table_map[status]} stat
                JOIN MEM_HAS_MEMBERSHIP mhm ON stat.membership_id = mhm.membership_id
                JOIN MEMBER m ON mhm.student_number = m.student_number
                JOIN MEM_IN_ORG mio ON mhm.membership_id = mio.membership_id
                JOIN ORGANIZATION o ON mio.organization_id = o.organization_id
                ORDER BY o.name, m.last_name
            """)
            
            if status == "Active":
                columns = ["Student No.", "Name", "Organization", "Date Active", "Role", "Committee"]
            else:
                columns = ["Student No.", "Name", "Organization", f"Date of {status.lower()}"]
                
            self.display_search_results(columns)

        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Failed to search members: {err}")

    def display_search_results(self, columns):
        results = self.cursor.fetchall()
        self.search_results.config(state='normal')
        self.search_results.delete(1.0, tk.END)
        
        self.search_results.insert(tk.END, " | ".join(columns) + "\n")
        self.search_results.insert(tk.END, "-" * 80 + "\n")
        
        for row in results:
            formatted_row = []
            for item in row:
                if isinstance(item, datetime):
                    formatted_row.append(item.strftime('%Y-%m-%d'))
                else:
                    formatted_row.append(str(item))
            self.search_results.insert(tk.END, " | ".join(formatted_row) + "\n")
        
        self.search_results.config(state='disabled')

    def display_table(self, event):
        table = self.table_combo.get()
        self.cursor.execute(f"SELECT * FROM {table}")
        rows = self.cursor.fetchall()
        columns = [desc[0] for desc in self.cursor.description]

        self.text.delete(1.0, tk.END)
        self.text.insert(tk.END, " | ".join(columns) + "\n")
        self.text.insert(tk.END, "-" * 100 + "\n")
        for row in rows:
            self.text.insert(tk.END, " | ".join(str(val) for val in row) + "\n")

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def show_fee_management(self):
        self.clear_window()
        tk.Button(self.root, text="Back", command=self.show_tables).grid(row=0, column=0, pady=5)
        
        tk.Button(self.root, text="Add Dues", command=self.add_dues_form).grid(row=1, column=0, pady=5)
        tk.Button(self.root, text="Record Payment", command=self.record_payment_form).grid(row=1, column=1, pady=5)

    def add_dues_form(self):
        self.clear_window()
        tk.Button(self.root, text="Back", command=self.show_fee_management).grid(row=0, column=0, pady=5)

        self.cursor.execute("""
            SELECT mhm.membership_id, m.first_name, m.last_name, o.name
            FROM MEM_HAS_MEMBERSHIP mhm 
            JOIN MEMBER m ON mhm.student_number = m.student_number
            JOIN MEM_IN_ORG mio ON mhm.membership_id = mio.membership_id
            JOIN ORGANIZATION o ON mio.organization_id = o.organization_id
        """)
        members = self.cursor.fetchall()
        member_options = [f"{mem[0]} - {mem[1]} {mem[2]} ({mem[3]})" for mem in members]

        tk.Label(self.root, text="Select Member:").grid(row=1, column=0, pady=5)
        self.member_combo = ttk.Combobox(self.root, values=member_options, state="readonly", width=50)
        self.member_combo.grid(row=1, column=1, pady=5)

        tk.Label(self.root, text="Amount Due:").grid(row=2, column=0, pady=5)
        self.amount_entry = tk.Entry(self.root)
        self.amount_entry.grid(row=2, column=1, pady=5)

        tk.Label(self.root, text="Due Date:").grid(row=3, column=0, pady=5)
        self.due_date_entry = tk.Entry(self.root)
        self.due_date_entry.insert(0, datetime.now().strftime('%Y-%m-%d'))
        self.due_date_entry.grid(row=3, column=1, pady=5)

        tk.Button(self.root, text="Submit", command=self.submit_dues).grid(row=4, column=0, columnspan=2, pady=10)

    def record_payment_form(self):
        self.clear_window()
        tk.Button(self.root, text="Back", command=self.show_fee_management).grid(row=0, column=0, pady=5)

        self.cursor.execute("""
            SELECT d.due_id, m.first_name, m.last_name, o.name, d.amount_due, d.due_date
            FROM DUES d
            JOIN HAS_DUES hd ON d.due_id = hd.due_id
            JOIN MEM_HAS_MEMBERSHIP mhm ON hd.membership_id = mhm.membership_id
            JOIN MEMBER m ON mhm.student_number = m.student_number
            JOIN MEM_IN_ORG mio ON mhm.membership_id = mio.membership_id
            JOIN ORGANIZATION o ON mio.organization_id = o.organization_id
            WHERE d.due_status = 'Unpaid'
            ORDER BY d.due_date
        """)
        dues = self.cursor.fetchall()
        due_options = [f"{due[0]} - {due[1]} {due[2]} ({due[3]}) ₱{due[4]} Due: {due[5]}" for due in dues]

        tk.Label(self.root, text="Select Due to Pay:").grid(row=1, column=0, pady=5)
        self.due_combo = ttk.Combobox(self.root, values=due_options, state="readonly", width=60)
        self.due_combo.grid(row=1, column=1, pady=5)

        tk.Label(self.root, text="Payment Date:").grid(row=2, column=0, pady=5)
        self.payment_date_entry = tk.Entry(self.root)
        self.payment_date_entry.insert(0, datetime.now().strftime('%Y-%m-%d'))
        self.payment_date_entry.grid(row=2, column=1, pady=5)

        tk.Button(self.root, text="Submit Payment", command=self.submit_payment).grid(row=3, column=0, columnspan=2, pady=10)

    def submit_dues(self):
        try:
            self.cursor.execute("START TRANSACTION")
            
            self.cursor.execute("SELECT MAX(due_id) FROM DUES")
            last_id = self.cursor.fetchone()[0] or 'D000'
            new_id = f"D{int(last_id[1:]) + 1:03d}"

            self.cursor.execute("""
                INSERT INTO DUES (due_id, amount_due, due_date, due_status)
                VALUES (%s, %s, %s, 'Unpaid')
            """, (new_id, self.amount_entry.get(), self.due_date_entry.get()))

            membership_id = self.member_combo.get().split(" - ")[0]
            self.cursor.execute("""
                INSERT INTO HAS_DUES (membership_id, due_id)
                VALUES (%s, %s)
            """, (membership_id, new_id))

            self.db.commit()
            messagebox.showinfo("Success", "Dues added successfully!")
            self.show_fee_management()
        except mysql.connector.Error as err:
            self.db.rollback()
            messagebox.showerror("Error", f"Failed to add dues: {err}")

    def submit_payment(self):
        try:
            self.cursor.execute("START TRANSACTION")
            
            self.cursor.execute("SELECT MAX(reference_id) FROM PAYMENT")
            last_id = self.cursor.fetchone()[0] or 'P000'
            new_payment_id = f"P{int(last_id[1:]) + 1:03d}"

            due_id = self.due_combo.get().split(" - ")[0]
            self.cursor.execute("SELECT amount_due FROM DUES WHERE due_id = %s", (due_id,))
            amount_due = self.cursor.fetchone()[0]

            self.cursor.execute("INSERT INTO PAYMENT (reference_id) VALUES (%s)", (new_payment_id,))
            
            self.cursor.execute("""
                INSERT INTO SETTLES (reference_id, due_id, payment_date, amount_paid)
                VALUES (%s, %s, %s, %s)
            """, (new_payment_id, due_id, self.payment_date_entry.get(), amount_due))

            self.cursor.execute("""
                UPDATE DUES SET due_status = 'Paid'
                WHERE due_id = %s
            """, (due_id,))

            self.cursor.execute("""
                INSERT INTO REQUIRES (membership_id, reference_id)
                SELECT hd.membership_id, %s
                FROM HAS_DUES hd
                WHERE hd.due_id = %s
            """, (new_payment_id, due_id))

            self.db.commit()
            messagebox.showinfo("Success", "Payment recorded successfully!")
            self.show_fee_management()
        except mysql.connector.Error as err:
            self.db.rollback()
            messagebox.showerror("Error", f"Failed to record payment: {err}")

    def show_financial_reports(self):
        self.clear_window()
        tk.Button(self.root, text="Back", command=self.show_tables).grid(row=0, column=0, pady=5)

        self.cursor.execute("SELECT organization_id, name FROM ORGANIZATION")
        orgs = self.cursor.fetchall()
        org_options = ["All Organizations"] + [f"{org[0]} - {org[1]}" for org in orgs]

        tk.Label(self.root, text="Select Organization:").grid(row=1, column=0, pady=5)
        self.report_org_combo = ttk.Combobox(self.root, values=org_options, state="readonly")
        self.report_org_combo.set("All Organizations")
        self.report_org_combo.grid(row=1, column=1, pady=5)
        self.report_org_combo.bind("<<ComboboxSelected>>", self.generate_financial_report)

        self.report_text = tk.Text(self.root, width=70, height=25)
        self.report_text.grid(row=2, column=0, columnspan=2, padx=10, pady=5)

        self.generate_financial_report()

    def generate_financial_report(self, event=None):
        try:
            selection = self.report_org_combo.get()
            where_clause = ""
            params = ()
            
            if selection != "All Organizations":
                org_id = selection.split(" - ")[0]
                where_clause = "WHERE o.organization_id = %s"
                params = (org_id,)

            query = f"""
                SELECT o.name AS organization,
                COALESCE(SUM(s.amount_paid), 0) AS total_collected,
                COALESCE(SUM(d.amount_due), 0) AS total_due
                FROM ORGANIZATION o
                LEFT JOIN MEM_IN_ORG mio ON o.organization_id = mio.organization_id
                LEFT JOIN HAS_DUES hd ON mio.membership_id = hd.membership_id
                LEFT JOIN DUES d ON hd.due_id = d.due_id
                LEFT JOIN SETTLES s ON d.due_id = s.due_id
                {where_clause}
                GROUP BY o.name
            """
            
            self.cursor.execute(query, params)
            results = self.cursor.fetchall()

            self.report_text.delete(1.0, tk.END)
            self.report_text.insert(tk.END, "Organization | Total Due | Total Collected | Collection Rate\n")
            self.report_text.insert(tk.END, "-" * 65 + "\n")

            for org, collected, due in results:
                collection_rate = (collected / due * 100) if due > 0 else 0
                self.report_text.insert(tk.END, 
                    f"{org} | ₱{due:.2f} | ₱{collected:.2f} | {collection_rate:.1f}%\n")

        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Failed to generate report: {err}")

if __name__ == "__main__":
    root = tk.Tk()
    app = MariaDBApp(root)
    root.mainloop()
