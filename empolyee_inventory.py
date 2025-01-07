from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import DateEntry
import pymysql


# this function connectivity to the data base
def Connect_database():
    try:
        connection = pymysql.Connect(
            host="localhost",
            user="root",
            passwd="Rafay?163:125",
        )
        curser = connection.cursor()
    except:
        messagebox.showerror("Error", "Database Connectivity issue Try Again")
        return None, None
    return curser, connection


#
def Create_database_Table():
    curser, connection = Connect_database()
    curser.execute("CREATE DATABASE IF NOT EXISTS EMPOLYEE_INVENTORY_SYSTEM")
    curser.execute("USE EMPOLYEE_INVENTORY_SYSTEM")
    curser.execute(
        "CREATE TABLE IF NOT EXISTS Empolyee_Data (empid INT PRIMARY KEY, name VARCHAR(100), email VARCHAR(100), gender VARCHAR(50), dob VARCHAR(50), contact VARCHAR(50), empolyment_type VARCHAR(50), work_shift VARCHAR(50), address VARCHAR(100), doj VARCHAR(50),salary VARCHAR(50), usertype VARCHAR(50))"
    )


# this fucntion is working on empty all input fields
def empty_fields(
    empolyee_ID,
    empolyee_name,
    empolyee_Email,
    empolyee_gender,
    empolyee_DOB,
    empolyee_Contact,
    empolyee_empolyementtype,
    empolyee_workshift,
    empolyee_address,
    empolyee_JOB,
    empolyee_salary,
    empolyeetype,
    check,
):
    empolyee_ID.delete(0, END)
    empolyee_name.delete(0, END)
    empolyee_Email.delete(0, END)
    empolyee_gender.set("Select Gender")
    from datetime import date

    empolyee_DOB.set_date(date.today())
    empolyee_Contact.delete(0, END)
    empolyee_empolyementtype.set("Select Type")
    empolyee_workshift.set("Select Shift")
    empolyee_address.delete(0, END)
    empolyee_JOB.set_date(date.today())
    empolyee_salary.delete(0, END)
    empolyeetype.set("User Select Type")
    if check:
        Empolyee_Treeview.selection_remove(Empolyee_Treeview.selection())


# Fetch the data to the database
def Display_data():
    curser, connection = Connect_database()
    if not curser or not connection:
        return
    curser.execute("USE EMPOLYEE_INVENTORY_SYSTEM")
    try:
        curser.execute("Select * from Empolyee_Data")
        empolyee_record = curser.fetchall()
        Empolyee_Treeview.delete(*Empolyee_Treeview.get_children())
        for record in empolyee_record:
            Empolyee_Treeview.insert("", END, values=record)
    except Exception as e:
        messagebox.showerror("Error", f"Error has occurred {e}")
    finally:
        curser.close()
        connection.close()


# this function is taking empolyee details and Save them into data base
def add_empolyee(
    empolyee_ID,
    empolyee_name,
    empolyee_Email,
    empolyee_gender,
    empolyee_DOB,
    empolyee_Contact,
    empolyee_empolyementtype,
    empolyee_workshift,
    empolyee_address,
    empolyee_JOB,
    empolyee_salary,
    empolyeetype,
):
    if (
        empolyee_ID == ""
        or empolyee_name == ""
        or empolyee_Email == ""
        or empolyee_gender == "Select Gender"
        or empolyee_DOB == ""
        or empolyee_Contact == ""
        or empolyee_empolyementtype == "Select Type"
        or empolyee_workshift == "Select Shift"
        or empolyee_address == ""
        or empolyee_JOB == ""
        or empolyee_salary == ""
        or empolyeetype == "User Select Type"
    ):
        messagebox.showerror("Error", "All Fields Are required")
    else:
        curser, connection = Connect_database()
        if not curser or not connection:
            return
        curser.execute("USE EMPOLYEE_INVENTORY_SYSTEM")
        try:
            curser.execute(
                "SELECT empid from empolyee_data WHERE empid=%s", (empolyee_ID)
            )
            if curser.fetchone():
                messagebox.showerror("Error", "ID already Exists!")
                empty_fields(
                    empolyee_ID_entry,
                    empolyee_name_entry,
                    empolyee_Email_entry,
                    empolyee_gender_entry,
                    empolyee_DOB_Entry,
                    empolyee_Contact_entry,
                    empolyee_empolyementtype_entry,
                    empolyee_workshift_entry,
                    empolyee_address_entry,
                    empolyee_JOB_Entry,
                    empolyee_salary_entry,
                    empolyeetype_entry,
                )
                return
            curser.execute(
                "INSERT INTO Empolyee_Data VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                (
                    empolyee_ID,
                    empolyee_name,
                    empolyee_Email,
                    empolyee_gender,
                    empolyee_DOB,
                    empolyee_Contact,
                    empolyee_empolyementtype,
                    empolyee_workshift,
                    empolyee_address,
                    empolyee_JOB,
                    empolyee_salary,
                    empolyeetype,
                ),
            )
            connection.commit()
            # call display function
            Display_data()
            # call empty fields
            empty_fields(
                empolyee_ID_entry,
                empolyee_name_entry,
                empolyee_Email_entry,
                empolyee_gender_entry,
                empolyee_DOB_Entry,
                empolyee_Contact_entry,
                empolyee_empolyementtype_entry,
                empolyee_workshift_entry,
                empolyee_address_entry,
                empolyee_JOB_Entry,
                empolyee_salary_entry,
                empolyeetype_entry,
                True,
            )
            # show dialogue box
            messagebox.showinfo("success", "The Data has inserted Successfull")
        except Exception as e:
            messagebox.showerror("Error", f"Error Has Occurred: {e}")
        finally:
            curser.close()
            connection.close()


# select row data
def Select_data(
    event,
    empolyee_ID,
    empolyee_name,
    empolyee_Email,
    empolyee_gender,
    empolyee_DOB,
    empolyee_Contact,
    empolyee_empolyementtype,
    empolyee_workshift,
    empolyee_address,
    empolyee_JOB,
    empolyee_salary,
    empolyeetype,
):

    index = Empolyee_Treeview.selection()
    content = Empolyee_Treeview.item(index)
    row = content["values"]
    empty_fields(
        empolyee_ID,
        empolyee_name,
        empolyee_Email,
        empolyee_gender,
        empolyee_DOB,
        empolyee_Contact,
        empolyee_empolyementtype,
        empolyee_workshift,
        empolyee_address,
        empolyee_JOB,
        empolyee_salary,
        empolyeetype,
        False,
    )
    empolyee_ID.insert(0, row[0])
    empolyee_name.insert(0, row[1])
    empolyee_Email.insert(0, row[2])
    empolyee_gender.set(row[3])
    empolyee_DOB.set_date(row[4])
    empolyee_Contact.insert(0, row[5])
    empolyee_empolyementtype.set(row[6])
    empolyee_workshift.set(row[7])
    empolyee_address.insert(0, row[8])
    empolyee_JOB.set_date(row[9])
    empolyee_salary.insert(0, row[10])
    empolyeetype.set(row[11])


# update functionality
def Update_Data(
    empolyee_ID,
    empolyee_name,
    empolyee_Email,
    empolyee_gender,
    empolyee_DOB,
    empolyee_Contact,
    empolyee_empolyementtype,
    empolyee_workshift,
    empolyee_address,
    empolyee_JOB,
    empolyee_salary,
    empolyeetype,
):
    selected = Empolyee_Treeview.selection()
    if not selected:
        messagebox.showerror("Error", "No Row is Selected")
    else:
        curser, connection = Connect_database()
    if not curser or not connection:
        return
    try:
        curser.execute("USE EMPOLYEE_INVENTORY_SYSTEM")
        curser.execute("SELECT * from empolyee_data WHERE empid = %s", (empolyee_ID,))
        current_data = curser.fetchone()
        current_data = current_data[1:]
        new_data = (
            empolyee_name,
            empolyee_Email,
            empolyee_gender,
            empolyee_DOB,
            empolyee_Contact,
            empolyee_empolyementtype,
            empolyee_workshift,
            empolyee_address,
            empolyee_JOB,
            empolyee_salary,
            empolyeetype,
        )
        if current_data == new_data:
            messagebox.showerror("Error", "No Changes Dedected!")
            return
        curser.execute(
            "UPDATE empolyee_data SET name=%s,email=%s,gender=%s,dob=%s,contact=%s,empolyment_type=%s,work_shift=%s,address=%s,doj=%s,salary=%s,usertype=%s WHERE empid=%s",
            (
                empolyee_name,
                empolyee_Email,
                empolyee_gender,
                empolyee_DOB,
                empolyee_Contact,
                empolyee_empolyementtype,
                empolyee_workshift,
                empolyee_address,
                empolyee_JOB,
                empolyee_salary,
                empolyeetype,
                empolyee_ID,
            ),
        )
        connection.commit()
        Display_data()
        empty_fields(
            empolyee_ID_entry,
            empolyee_name_entry,
            empolyee_Email_entry,
            empolyee_gender_entry,
            empolyee_DOB_Entry,
            empolyee_Contact_entry,
            empolyee_empolyementtype_entry,
            empolyee_workshift_entry,
            empolyee_address_entry,
            empolyee_JOB_Entry,
            empolyee_salary_entry,
            empolyeetype_entry,
            True,
        )
        messagebox.showinfo("successful", "the Data has been saved successfully")
    except Exception as e:
        messagebox.showerror("Error", f"Some Error Occurred {e}")
    finally:
        curser.close()
        connection.close()


def Delete_data(empolyee_ID):
    selected = Empolyee_Treeview.selection()
    if not selected:
        messagebox.showerror("Error", "No Row is Selected")
    else:
        result = messagebox.askyesno(
            "Confirm", "DO you want to really delete the record"
        )
        if result:
            curser, connection = Connect_database()
        if not curser or not connection:
            return
        curser.execute("USE EMPOLYEE_INVENTORY_SYSTEM")
        try:
            curser.execute(
                "DELETE FROM empolyee_data WHERE empid=%s",
                (empolyee_ID),
            )
            connection.commit()
            Display_data()
            empty_fields(
                empolyee_ID_entry,
                empolyee_name_entry,
                empolyee_Email_entry,
                empolyee_gender_entry,
                empolyee_DOB_Entry,
                empolyee_Contact_entry,
                empolyee_empolyementtype_entry,
                empolyee_workshift_entry,
                empolyee_address_entry,
                empolyee_JOB_Entry,
                empolyee_salary_entry,
                empolyeetype_entry,
                True,
            )
            messagebox.showinfo("successful", "the Data has been Deleted successfully")
        except Exception as e:
            messagebox.showerror("Error", f"Some Error Occurred {e}")
        finally:
            curser.close()
            connection.close()


# Search data functionality function
def Search_data(search_options, values):
    if search_options == "Search By":
        messagebox.showerror("Error", "No Option is Selected")
    elif values == "":
        messagebox.showerror("Error", "Enter the value for Search record")
    else:
        search_options = search_options.replace(" ", "_")
        curser, connection = Connect_database()
        if not curser or not connection:
            return
        curser.execute("USE EMPOLYEE_INVENTORY_SYSTEM")
        try:

            curser.execute(
                f"SELECT * FROM empolyee_inventory_system.empolyee_data where {search_options} LIKE %s",
                f"%{values}%",
            )
            search_Entry.delete(0, END)
            records = curser.fetchall()
            Empolyee_Treeview.delete(*Empolyee_Treeview.get_children())
            for record in records:
                Empolyee_Treeview.insert("", END, value=record)
        except Exception as e:
            messagebox.showerror("Error", f"Some Error Occurred {e}")
        finally:
            curser.close()
            connection.close()

        # SELECT * FROM empolyee_inventory_system.empolyee_data where name="Abdul Rafay";


# fetch All Record
def show_all_data(Search_Combo, search_Entry):
    Display_data()
    search_Entry.delete(0, END)
    Search_Combo.set("Search By")


window = Tk()
window.title("Empolyee Inventory System")
window.geometry("1980x1080+0+0")
window.config(bg="#E7FBB4")
global Empolyee_Treeview
# main label
bg_image = PhotoImage(file="logo.png")
title_lable = Label(
    window,
    image=bg_image,
    compound=LEFT,
    text=" EMPOLYEE INVENTORY MANAGEMENT SYSTEM!",
    bd=15,
    bg="#001A6E",
    fg="white",
    font=("poppins", 30, "bold"),
    padx=2,
    pady=10,
)
title_lable.place(x=0, y=0, relwidth=1)

# sub title Label
sub_title_label = Label(
    window,
    text="WELCOME TO EMPOLYEE \t\t Date: 02-01-2025 \t\t Time: 8:21:20 pm",
    font=("poppins", 15, "bold"),
    bg="#FFFDEC",
    pady=10,
)
sub_title_label.place(x=0, y=110, relwidth=1)

# create frame for Add Empolyee
full_frame = Frame(window, bd=10, relief=RIDGE, bg="#FFFDEC")
full_frame.place(x=15, y=170, width=1500, height=620)

# heading in frame

detail_logo = PhotoImage(file="detail.png")
heading_label = Label(
    full_frame,
    image=detail_logo,
    compound=LEFT,
    text=" MANAGE EMPOLYEES DETAILS",
    font=("poppins", 15, "bold"),
    bg="#001A6E",
    fg="white",
    pady=10,
)
heading_label.place(x=0, y=0, relwidth=1)

# top Frame fro Search Record
top_frame = Frame(full_frame, bd=10, relief=FLAT, bg="#E1EACD", pady=10)
top_frame.place(
    x=0,
    y=60,
    relwidth=1,
    height=300,
)
search_frame = Frame(top_frame, bg="#FFFDEC", padx=2)
search_frame.pack()

#  =============== Drop Down Search By
Search_Combo = ttk.Combobox(
    search_frame, width=17, font=("arial", 10, "bold"), state="readonly"
)
Search_Combo["values"] = (
    "empid",
    "Name",
    "Email",
    "Empolyment Type",
    "Work Shift",
    "Salary",
)
Search_Combo.set("Search By")
Search_Combo.grid(row=0, column=0, padx=10, pady=10)
# search Bar field
search_Entry = Entry(
    search_frame,
    bd=3,
    relief=RIDGE,
    width=17,
    font=("arial", 10, "bold"),
    bg="lightyellow",
)
search_Entry.grid(row=0, column=1, padx=10, pady=10)
# search btn
search_icon = PhotoImage(file="search.png")
Search_btn = Button(
    search_frame,
    text=" SEARCH",
    image=search_icon,
    compound=LEFT,
    font=("arial", 10, "bold"),
    fg="white",
    bg="darkgreen",
    width=100,
    command=lambda: Search_data(Search_Combo.get(), search_Entry.get()),
)
Search_btn.place(x=0, y=20)
Search_btn.grid(row=0, column=2, padx=10, pady=10)
Show_All = Button(
    search_frame,
    text="SHOW ALL",
    font=("arial", 10, "bold"),
    fg="white",
    bg="#001A6E",
    width=17,
    command=lambda: show_all_data(Search_Combo, search_Entry),
)
Show_All.place(x=0, y=20)
Show_All.grid(row=0, column=3, padx=10, pady=10)

# scroll bar of this three view
Scroll_bar_x = ttk.Scrollbar(top_frame, orient=HORIZONTAL)
Scroll_bar_y = ttk.Scrollbar(top_frame, orient=VERTICAL)
# treeview record
Empolyee_Treeview = ttk.Treeview(
    top_frame,
    columns=(
        "empid",
        "name",
        "email",
        "gender",
        "dob",
        "contact",
        "employment_type",
        "work_shift",
        "address",
        "doj",
        "salary",
        "usertype",
    ),
    show="headings",
    xscrollcommand=Scroll_bar_x.set,
    yscrollcommand=Scroll_bar_y.set,
)
Scroll_bar_y.pack(side=RIGHT, fill=Y, pady=(10, 0))
Scroll_bar_x.pack(side=BOTTOM, fill=X)
Scroll_bar_x.config(command=Empolyee_Treeview.xview)
Scroll_bar_x.config(command=Empolyee_Treeview.yview)
#
Empolyee_Treeview.pack(pady=(10, 0), padx=(0, 0))
Empolyee_Treeview.heading("empid", text="Emp ID")
Empolyee_Treeview.heading("name", text="Name")
Empolyee_Treeview.heading("email", text="Email")
Empolyee_Treeview.heading("gender", text="Gender")
Empolyee_Treeview.heading("dob", text="Date Of Birth")
Empolyee_Treeview.heading("contact", text="Contact")
Empolyee_Treeview.heading("employment_type", text="Employment Type")
Empolyee_Treeview.heading("work_shift", text="Work Shift")
Empolyee_Treeview.heading("address", text="Address")
Empolyee_Treeview.heading("doj", text="Date Of Join")
Empolyee_Treeview.heading("salary", text="Salary")
Empolyee_Treeview.heading("usertype", text="User Type")

Empolyee_Treeview.column("empid", width=50)
Empolyee_Treeview.column("name", width=120)
Empolyee_Treeview.column("email", width=200)
Empolyee_Treeview.column("gender", width=80)
Empolyee_Treeview.column("dob", width=100)
Empolyee_Treeview.column("contact", width=100)
Empolyee_Treeview.column("employment_type", width=120)
Empolyee_Treeview.column("work_shift", width=100)
Empolyee_Treeview.column("address", width=300)
Empolyee_Treeview.column("doj", width=100)
Empolyee_Treeview.column("salary", width=100)
Empolyee_Treeview.column("usertype", width=100)
Display_data()


Empolyee_Details = Frame(full_frame, bd=3, relief=SOLID, bg="#E1EACD", padx=50, pady=0)
Empolyee_Details.place(x=0, y=370, relwidth=1, height=230)

# empolyee id
empolyee_ID_label = Label(
    Empolyee_Details, width=15, text="Emp ID:", font=("times new roman", 12, "bold")
)
empolyee_ID_label.grid(row=0, column=0, padx=5, pady=10)

empolyee_ID_entry = Entry(
    Empolyee_Details,
    bd=3,
    bg="lightyellow",
    relief=RIDGE,
    width=25,
    font=("arial", 10, "bold"),
)
empolyee_ID_entry.grid(row=0, column=1, padx=5, pady=10)

# empolyee name
empolyee_name_label = Label(
    Empolyee_Details, width=15, text="Name: ", font=("times new roman", 12, "bold")
)
empolyee_name_label.grid(row=0, column=2, padx=5, pady=10)
empolyee_name_entry = Entry(
    Empolyee_Details,
    bd=3,
    bg="lightyellow",
    relief=RIDGE,
    width=25,
    font=("arial", 10, "bold"),
)
empolyee_name_entry.grid(row=0, column=3, padx=5, pady=10)
# Empolyee DOB
empolyee_DOB_label = Label(
    Empolyee_Details,
    width=15,
    text="Bate Of Birth: ",
    font=("times new roman", 12, "bold"),
)
empolyee_DOB_label.grid(row=0, column=4, padx=5, pady=10)
empolyee_DOB_Entry = DateEntry(
    Empolyee_Details,
    width=20,
    font=("times new roman", 12, "bold"),
    state="readonly",
    data_pattern="dd/mm/yyyy",
)
empolyee_DOB_Entry.grid(row=0, column=5)

# Empolyee Date of Join
empolyee_JOB_label = Label(
    Empolyee_Details,
    width=15,
    text="Date Of Join: ",
    font=("times new roman", 12, "bold"),
)
empolyee_JOB_label.grid(row=0, column=6, padx=5, pady=10)
empolyee_JOB_Entry = DateEntry(
    Empolyee_Details,
    width=20,
    font=("times new roman", 12, "bold"),
    state="readonly",
    data_pattern="dd/mm/yyyy",
)
empolyee_JOB_Entry.grid(row=0, column=7)
# empolyee Email
empolyee_Email_label = Label(
    Empolyee_Details, width=15, text="Email: ", font=("times new roman", 12, "bold")
)
empolyee_Email_label.grid(row=1, column=0, padx=5, pady=10)
empolyee_Email_entry = Entry(
    Empolyee_Details,
    bd=3,
    bg="lightyellow",
    relief=RIDGE,
    width=25,
    font=("arial", 10, "bold"),
)
empolyee_Email_entry.grid(row=1, column=1, padx=5, pady=10)
# Empolyee DOB
# empolyee_DOB_label = Label(
#     Empolyee_Details,
#     width=15,
#     text="Bate Of Birth: ",
#     font=("times new roman", 12, "bold"),
# )
# empolyee_DOB_label.grid(row=1, column=0, padx=5, pady=10)
# empolyee_DOB_Entry = DateEntry(
#     Empolyee_Details,
#     width=20,
#     font=("times new roman", 12, "bold"),
#     state="readonly",
#     data_pattern="dd/mm/yyyy",
# )
# empolyee_DOB_Entry.grid(row=1, column=1)

# contact label
empolyee_Contact_label = Label(
    Empolyee_Details, width=15, text="Contact: ", font=("times new roman", 12, "bold")
)
empolyee_Contact_label.grid(row=1, column=2, padx=5, pady=10)
empolyee_Contact_entry = Entry(
    Empolyee_Details,
    bd=3,
    bg="lightyellow",
    relief=RIDGE,
    width=25,
    font=("arial", 10, "bold"),
)
empolyee_Contact_entry.grid(row=1, column=3, padx=5, pady=10)

# empolyement type
empolyee_empolyementtype_label = Label(
    Empolyee_Details,
    width=15,
    text="Empolyement Type: ",
    font=("times new roman", 12, "bold"),
)
empolyee_empolyementtype_label.grid(row=1, column=4, padx=5, pady=10)
empolyee_empolyementtype_entry = ttk.Combobox(
    Empolyee_Details,
    width=25,
    values=("Full Time", "Part Time", "Casual", "Contract", "Intern"),
    state="readonly",
)
empolyee_empolyementtype_entry.set("Select Type")
empolyee_empolyementtype_entry.grid(row=1, column=5, padx=5, pady=10)

# empolyement work shift
empolyee_workshift_label = Label(
    Empolyee_Details,
    width=15,
    text="Work Shift: ",
    font=("times new roman", 12, "bold"),
)
empolyee_workshift_label.grid(row=1, column=6, padx=5, pady=10)
empolyee_workshift_entry = ttk.Combobox(
    Empolyee_Details, width=25, values=("Morning", "Evening"), state="readonly"
)
empolyee_workshift_entry.set("Select Shift")
empolyee_workshift_entry.grid(row=1, column=7, padx=5, pady=10)

# Empolyee Address
empolyee_address_label = Label(
    Empolyee_Details, width=15, text="Address: ", font=("times new roman", 12, "bold")
)
empolyee_address_label.grid(row=2, column=0, padx=5, pady=10)
empolyee_address_entry = Entry(
    Empolyee_Details,
    bd=3,
    bg="lightyellow",
    relief=RIDGE,
    width=25,
    font=("arial", 10, "bold"),
)
empolyee_address_entry.grid(row=2, column=1, padx=5, pady=10)

# empolyee Gender
empolyee_gender_label = Label(
    Empolyee_Details, width=15, text="Gender: ", font=("times new roman", 12, "bold")
)
empolyee_gender_label.grid(row=2, column=2, padx=5, pady=10)
empolyee_gender_entry = ttk.Combobox(
    Empolyee_Details, width=25, values=("Male", "Female"), state="readonly"
)
empolyee_gender_entry.set("Select Gender")
empolyee_gender_entry.grid(row=2, column=3, padx=5, pady=10)
# Empolyee Salary
empolyee_salary_label = Label(
    Empolyee_Details, width=15, text="Salary: ", font=("times new roman", 12, "bold")
)
empolyee_salary_label.grid(row=2, column=4, padx=5, pady=10)
empolyee_salary_entry = Entry(
    Empolyee_Details,
    bd=3,
    bg="lightyellow",
    relief=RIDGE,
    width=25,
    font=("arial", 10, "bold"),
)
empolyee_salary_entry.grid(row=2, column=5, padx=5, pady=10)

# Empolyee type
empolyeetype_label = Label(
    Empolyee_Details,
    width=15,
    text="User Type: ",
    font=("times new roman", 12, "bold"),
)
empolyeetype_label.grid(row=2, column=6, padx=5, pady=10)
empolyeetype_entry = ttk.Combobox(
    Empolyee_Details,
    width=25,
    values=("Empolyee"),
    state="readonly",
)
empolyeetype_entry.set("User Select Type")
empolyeetype_entry.grid(row=2, column=7, padx=5, pady=10)

# button to save data
Data_add_btn = Button(
    Empolyee_Details,
    text="Add Data",
    font=("poppins", 12, "bold"),
    width=15,
    cursor="hand2",
    fg="white",
    bg="#001A6E",
    command=lambda: add_empolyee(
        empolyee_ID_entry.get(),
        empolyee_name_entry.get(),
        empolyee_Email_entry.get(),
        empolyee_gender_entry.get(),
        empolyee_DOB_Entry.get(),
        empolyee_Contact_entry.get(),
        empolyee_empolyementtype_entry.get(),
        empolyee_workshift_entry.get(),
        empolyee_address_entry.get(),
        empolyee_JOB_Entry.get(),
        empolyee_salary_entry.get(),
        empolyeetype_entry.get(),
    ),
)
Data_add_btn.grid(row=3, column=2, pady=15)
# button to update data
Data_update_btn = Button(
    Empolyee_Details,
    text="Update Data",
    font=("poppins", 12, "bold"),
    width=15,
    cursor="hand2",
    fg="white",
    bg="green",
    command=lambda: Update_Data(
        empolyee_ID_entry.get(),
        empolyee_name_entry.get(),
        empolyee_Email_entry.get(),
        empolyee_gender_entry.get(),
        empolyee_DOB_Entry.get(),
        empolyee_Contact_entry.get(),
        empolyee_empolyementtype_entry.get(),
        empolyee_workshift_entry.get(),
        empolyee_address_entry.get(),
        empolyee_JOB_Entry.get(),
        empolyee_salary_entry.get(),
        empolyeetype_entry.get(),
    ),
)
Data_update_btn.grid(row=3, column=3, pady=15)
# button to Delete data
Data_delete_btn = Button(
    Empolyee_Details,
    text="Delete Data",
    font=("poppins", 12, "bold"),
    width=15,
    cursor="hand2",
    fg="white",
    bg="red",
    command=lambda: Delete_data(empolyee_ID_entry.get()),
)
Data_delete_btn.grid(row=3, column=4, pady=15)
# button to Clear data
Data_clear_btn = Button(
    Empolyee_Details,
    text="Clear Data",
    font=("poppins", 12, "bold"),
    width=15,
    cursor="hand2",
    fg="white",
    bg="#500073",
    command=lambda: empty_fields(
        empolyee_ID_entry,
        empolyee_name_entry,
        empolyee_Email_entry,
        empolyee_gender_entry,
        empolyee_DOB_Entry,
        empolyee_Contact_entry,
        empolyee_empolyementtype_entry,
        empolyee_workshift_entry,
        empolyee_address_entry,
        empolyee_JOB_Entry,
        empolyee_salary_entry,
        empolyeetype_entry,
        True,
    ),
)
Data_clear_btn.grid(row=3, column=5, pady=15)

# called select row update function
Empolyee_Treeview.bind(
    "<ButtonRelease-1>",
    lambda event: Select_data(
        event,
        empolyee_ID_entry,
        empolyee_name_entry,
        empolyee_Email_entry,
        empolyee_gender_entry,
        empolyee_DOB_Entry,
        empolyee_Contact_entry,
        empolyee_empolyementtype_entry,
        empolyee_workshift_entry,
        empolyee_address_entry,
        empolyee_JOB_Entry,
        empolyee_salary_entry,
        empolyeetype_entry,
    ),
)

Create_database_Table()
window.mainloop()
