import tkinter as tk
import mysql.connector as sqltor
from tkinter import ttk
from tkinter import messagebox
import datetime

def mysql_login():
    db_log = input("Enter your MySQL login: ")
    db_pwd = input("Enter your MySQL password: ")
    global mydb
    try:
        mydb = sqltor.connect(host="localhost", user=db_log, passwd=db_pwd)
    except sqltor.errors.ProgrammingError:
        print("You have entered the incorrect MySQL login credentials. Try again!")
        mysql_login()

def createTables():
    # Creates all the tables required for this project

    # Table 1
    mycursor.execute("CREATE TABLE IF NOT EXISTS PAT_REG(UID char(6) NOT NULL, DOB date, NAME char(20) NOT NULL, SEX char(1), PH_NO bigint, PWD char(15) NOT NULL);")

    # Table 2
    mycursor.execute("CREATE TABLE IF NOT EXISTS VACCINATION(V_NAME char(20), QTY int);")

    # Table 3
    mycursor.execute("CREATE TABLE IF NOT EXISTS ADMIN(UID_D char(6), NAME char(20), DEPT char(20), AVAIL varchar(60), PWD char(15));")

    #Table 4
    mycursor.execute("CREATE TABLE IF NOT EXISTS CONSULTATION(DOC_VAC char(15), UID_P char(6), CONSUL_DATETIME datetime, DIAGNOSIS varchar(100), PRESCRIPTION varchar(200));")


def confirm(P_UID, pat_land, Booking, doctor_c, vaccine_c, date, time):
    '''Declares confirmation of booking

    Default Parameters:
    doctor_c--stores doctor booked
    vaccine_c--stores vaccine booked
    date--stores date of booking
    time--stores time of booking
    '''
    if doctor_c == False:
        mycursor.execute("INSERT INTO CONSULTATION VALUES ('{}','{}','{}','{}','{}')".format(vaccine_c, P_UID, (date + ' ' + time), 'N/A', 'N/A'))
        messagebox.showinfo("Booking Successful!", f'Vaccine: {vaccine_c}\nDate: {date}\nTime: {time}')
        mycursor.execute("UPDATE VACCINATION SET QTY = QTY-1;")
    elif vaccine_c == False:
        mycursor.execute("SELECT UID_D FROM ADMIN WHERE NAME = '{}'".format(doctor_c))
        D_UID = mycursor.fetchone()[0]
        mycursor.execute("INSERT INTO CONSULTATION VALUES ('{}','{}','{}','{}','{}')".format(D_UID, P_UID, (date + ' ' + time), 'N/A', 'N/A'))
        messagebox.showinfo("Booking Successful!", f'Doctor: {doctor_c}\nDate: {date}\nTime: {time}')  # Doctor/Vaccine
    mydb.commit()
    close(Booking)
    close(pat_land)
    appt_book(P_UID)


def availability(avail):
    num_avail = []
    for i in avail[0].split(','):
        i = i.lower()
        if i == 'monday':
            num_avail.append(0)
        elif i == 'tuesday':
            num_avail.append(1)
        elif i == 'wednesday':
            num_avail.append(2)
        elif i == 'thursday':
            num_avail.append(3)
        elif i == 'friday':
            num_avail.append(4)
        elif i == 'saturday':
            num_avail.append(5)
        elif i == 'sunday':
            num_avail.append(6)
    num_avail.sort()
    mycursor.execute("SELECT WEEKDAY(CURDATE());")
    curr_day = mycursor.fetchone()[0]
    avail = []
    for i in num_avail:
        if curr_day < i:
            mycursor.execute(("SELECT DATE_ADD(CURDATE(), INTERVAL {} DAY);").format(i - curr_day))
            data = mycursor.fetchone()
            avail += data
        elif curr_day == 6:
            curr_day = -1
            mycursor.execute(("SELECT DATE_ADD(CURDATE(), INTERVAL {} DAY);").format(i - curr_day))
            data = mycursor.fetchone()
            avail += data
    if avail == []:
        return False
    else:
        return avail


def time(P_UID, pat_land, Booking, date, doctor_t, vaccine_t):
    '''Selection of time for booking

    Default Parameters:
    doctor_t--stores doctor booked
    vaccine_t--stores vaccine booked
    date--stores date of booking
    Booking--parent window
    '''

    if doctor_t == False:
        time_avail = ['09:00:00', '09:30:00', '10:00:00', '11:00:00', '11:30:00', '12:00:00','12:30:00', '13:30:00', '14:00:00', '14:30:00', '15:00:00', '15:30:00',
                      '16:00:00', '16:30:00']
        choice_4 = tk.StringVar(Booking)
        choice_4.set("Select Time")
        options_4 = tk.OptionMenu(Booking, choice_4, *time_avail, command=lambda x: confirm(P_UID, pat_land, Booking, doctor_t,
                                  vaccine_t, date, choice_4.get()))
        options_4.place(relx=0.74, rely=0.2)
    if vaccine_t == False:
        mycursor.execute("SELECT UID_D FROM ADMIN WHERE NAME = '{}'".format(doctor_t))
        UID_D = [i[0] for i in mycursor.fetchall()][0]
        mycursor.execute("SELECT TIME(CONSUL_DATETIME) FROM CONSULTATION WHERE DOC_VAC = '{}' AND DATE(CONSUL_DATETIME) = '{}'".format(UID_D, date))  
        data = [i[0] for i in mycursor.fetchall()]
        booked_times = []
        for i in data:
            t = str((datetime.datetime.min + i).time())
            booked_times.append(t)
            
        times = ['09:00:00', '09:30:00', '10:00:00', '11:00:00', '11:30:00', '12:00:00', '12:30:00', '13:30:00', '14:00:00', '14:30:00', '15:00:00', '15:30:00',
                 '16:00:00', '16:30:00']
        time_avail = []
        for i in range(len(times)):
            if times[i] not in booked_times:
                time_avail.append(times[i])
        choice_4 = tk.StringVar(Booking)
        choice_4.set("Select Time")
        options_4 = tk.OptionMenu(Booking, choice_4, *time_avail, command=lambda x: confirm(P_UID, pat_land, Booking, doctor_t,
                                  vaccine_t, date, choice_4.get()))
        options_4.place(relx=0.79, rely=0.2)


def date(P_UID, pat_land, Booking, doctor=False, vaccine_d=False):
    '''Selection of date for booking

    Default Parameters:
    Booking--parent window
    doctor--stores doctor booked
    vaccine_d--stores vaccine booked
    '''
    if doctor == False:
        date_avail = []
        for i in range(1, 7):
            mycursor.execute(("SELECT DATE_ADD(CURDATE(), INTERVAL {} DAY);").format(i))
            date_avail.append(mycursor.fetchone()[0])
        choice_3 = tk.StringVar(Booking)
        choice_3.set("Select Date")
        options_3 = tk.OptionMenu(Booking, choice_3, *date_avail, command=lambda x: time(P_UID, pat_land, Booking, choice_3.get(), doctor_t=doctor, vaccine_t=vaccine_d))
        options_3.place(relx=0.49, rely=0.2)

    elif vaccine_d == False:
        mycursor.execute(
            "SELECT AVAIL FROM ADMIN WHERE NAME = '{}'".format(doctor))
        date_avail = mycursor.fetchone()
        date_avail = availability(date_avail)
        if date_avail != False:
            choice_3 = tk.StringVar(Booking)
            choice_3.set("Select Date")
            options_3 = tk.OptionMenu(Booking, choice_3, *date_avail, command=lambda x: time(P_UID, pat_land, Booking, choice_3.get(), doctor_t=doctor, vaccine_t=vaccine_d))
            options_3.place(relx=0.59, rely=0.2)
        else:
            messagebox.showinfo("Dates unavailable", "Doctor is unavailable for the rest of this week. Try again on Monday!")


def spec(P_UID, pat_land, Booking, choice, doctor, vaccine):
    '''Selection of Doctor in Selected Department
    
    Default Parameters:
    Booking--parent window
    choice--choice of Department of Doctor or vaccine
    doctor--stores True if choice is Doctor
    vaccine--stores True if choice is vaccine
    '''
    if doctor == False:
        date(P_UID, pat_land, Booking, vaccine_d=choice)
    elif vaccine == False:
        mycursor.execute("SELECT Name FROM ADMIN WHERE Dept = '{}'".format(choice))
        doc_with_spec = [i[0] for i in mycursor.fetchall()]
        choice_2 = tk.StringVar(Booking)
        choice_2.set("Select Doctor")
        options_2 = tk.OptionMenu(Booking, choice_2, *doc_with_spec, command=lambda x: date(P_UID, pat_land, Booking, doctor=choice_2.get()))
        options_2.place(relx=0.39, rely=0.2)


def book(pat_land, P_UID, doctor=False, vaccine=False):
    Booking = tk.Tk()
    Booking.title("Booking Page")
    Booking.config(bg='#42b0f5')
    Booking.geometry("1016x360")

    choice_1 = tk.StringVar(Booking)
    if doctor == True:
        mycursor.execute("SELECT DEPT FROM ADMIN WHERE UID_D LIKE 'D%';")
        choice_1.set("Select Department")
        x_pos = 0.19
        y_pos = 0.2
    if vaccine == True:
        mycursor.execute("SELECT V_NAME FROM VACCINATION WHERE QTY > 0;")
        choice_1.set("Select Vaccine")
        x_pos = 0.24
        y_pos = 0.2

    data = [i[0] for i in mycursor.fetchall()]
    options_1 = tk.OptionMenu(Booking, choice_1, *data, command=lambda x: spec(P_UID, pat_land, Booking, choice_1.get(), doctor, vaccine))
    options_1.place(relx=x_pos, rely=y_pos)


def appt_book(P_UID):
    '''Booking Page for doctors and vaccine

    Default Parameter:
    P_UID--stores the UID of the patient 
    '''

    mycursor.execute("SELECT DOB, NAME, SEX, PH_NO FROM PAT_REG WHERE UID = '{}';".format(P_UID))
    data = mycursor.fetchall()
    for i in data:
        DOB = i[0]
        name = i[1]
        sex = i[2]
        ph_no = i[3]

    pat_land = tk.Tk()
    pat_land.title(f"Patient: {name}")
    pat_land.config(bg='#42b0f5')
    display = tk.Text(pat_land, height=20, width=160)
    display.place(relx=0, rely=0)
    display.config(bg='#42b0f5')
    pat_land.geometry("1150x360")

    display.insert(tk.END, f'''UID: {P_UID}
Name: {name}
Sex: {sex}
Date of Birth: {DOB}
Phone Number: {ph_no}''')

    Logout = ttk.Button(pat_land, command=lambda: close(pat_land) or login(), text='Logout')
    Logout.place(relx=0.92, rely=0.027)

    Edit = ttk.Button(pat_land, text='Edit Information', command=lambda: edit_pat(P_UID))
    Edit.place(relx=0.9, rely=0.1)

    tree_1 = ttk.Treeview(pat_land, columns=("c1", "c2", "c3", "c4"), show='headings')
    tree_1.heading('#1', text='Doctor/Vaccine')
    tree_1.heading('#2', text='Past Consultation')
    tree_1.heading('#3', text='Diagnosis')
    tree_1.heading('#4', text='Prescription')
    tree_1.column(3, width = 300)
    
    mycursor.execute(("SELECT DOC_VAC, DATE(CONSUL_DATETIME), DIAGNOSIS, PRESCRIPTION FROM CONSULTATION WHERE UID_P = '{}' ORDER BY CONSUL_DATETIME DESC;").format(P_UID))
    data = mycursor.fetchmany(size=5)

    mycursor.execute("SELECT UID_D FROM ADMIN")
    l = mycursor.fetchall()
    doc_UID = [i[0] for i in l]
    
    for i in data:
        if i[0] in doc_UID:
            mycursor.execute(("SELECT NAME FROM ADMIN WHERE UID_D='{}';").format(i[0]))
            name = mycursor.fetchone()[0]
            copy = list(i)
            copy[0] = name
            tree_1.insert('', tk.END, values=copy)
        else: 
            tree_1.insert('', tk.END, values=i)
    tree_1.place(relx=0.1, rely=0.25)

    b_vac = ttk.Button(pat_land, text='Book Vaccine Slot', command=lambda: book(pat_land, P_UID, vaccine=True))
    b_doc = ttk.Button(pat_land, text='Book Doctor Appointment', command=lambda: book(pat_land, P_UID, doctor=True))
    b_vac.place(relx=0.7, rely=0.9)
    b_doc.place(relx=0.15, rely=0.9)


def edit_pat(P_UID):
    win_pat = tk.Tk()
    win_pat.geometry("828x128")
    win_pat.title("Edit your details")
    #win_pat.config(bg='#42b0f5')

    data = ttk.Entry(win_pat, width=50)
    data['state'] = 'disabled'
    data.grid(row=0, column=1, pady=2)

    choice = tk.StringVar(win_pat)
    choice.set("Select Field")
    fields = ['Name', 'Sex', 'Ph_No', 'PWD']
    options = tk.OptionMenu(win_pat, choice, *fields, command=lambda x: data.config(state='enabled'))
    options.grid(row=0, column=0)

    enter = ttk.Button(win_pat, text="Submit", command=lambda: sql_edit_pat(P_UID, data.get(), choice.get()) or close(win_pat))
    enter.grid(row=1, column=1, pady=2)


def sql_edit_pat(P_UID, data, column):
    try:
        mycursor.execute(("UPDATE PAT_REG SET {} = '{}' WHERE UID = '{}';").format(column, data, P_UID))
        mydb.commit()
        messagebox.showinfo("Information Edited", "Your details have been altered successfully! Logout and relogin for changes to reflect")
    except:
        messagebox.showerror("Data Error", "Values entered may be too long or of incorrect type. Try again!")
        edit_pat(P_UID)


def show_doc():
    mycursor.execute("SELECT * FROM ADMIN WHERE UID_D LIKE 'D%';")
    data = mycursor.fetchall()

    doc_win = tk.Tk()
    doc_win.title("Show Doctor Records")
    #doc_win.config(bg='#42b0f5')
    
    tree_1 = ttk.Treeview(doc_win, columns=("c1", "c2", "c3", "c4"), show='headings')
    tree_1.heading('#1', text='Doctor UID')
    tree_1.heading('#2', text='Name')
    tree_1.heading('#3', text='Department')
    tree_1.heading('#4', text='Availability')  #Date and time#
    tree_1.column(0, width = 100)
    tree_1.column(1, width = 200)
    tree_1.column(2, width = 300)
    tree_1.column(3, width = 400)

    for i in data:
        tree_1.insert('', tk.END, values=i)
    tree_1.pack()
    doc_win.mainloop()


def add_doc():
    UID_D = UID_gen('D')
    win_doc = tk.Tk()
    win_doc.geometry("828x128")
    win_doc.title("Add Doctor")
    #win_doc.config(bg='#42b0f5')

    add_name = ttk.Entry(win_doc, width=50)
    l1 = ttk.Label(win_doc, text="Enter doctor's name: ")
    l1.grid(row=0, column=0, sticky=tk.W, pady=2)
    add_name.grid(row=0, column=1, pady=2)

    add_dept = ttk.Entry(win_doc, width=50)
    l2 = ttk.Label(win_doc, text="Enter doctor's department: ")
    l2.grid(row=2, column=0, sticky=tk.W, pady=2)
    add_dept.grid(row=2, column=1, pady=2)

    add_avail = ttk.Entry(win_doc, width=50)
    l3 = ttk.Label(win_doc, text="Enter doctor's availability as a comma separated list of days: ")
    l3.grid(row=4, column=0, sticky=tk.W, pady=2)
    add_avail.grid(row=4, column=1, pady=2)

    add_pwd = ttk.Entry(win_doc, width=50)
    l4 = ttk.Label(win_doc, text="Enter password to be assigned to the doctor: ")
    l4.grid(row=6, column=0, sticky=tk.W, pady=2)
    add_pwd.grid(row=6, column=1, pady=2)

    enter = ttk.Button(win_doc, text="Submit", command=lambda: sql_add_doc(UID_D, add_name.get(), add_dept.get(), add_avail.get(), add_pwd.get()) or close(win_doc))
    enter.grid(row=8, column=1, pady=2)


def sql_add_doc(UID_D, name, dept, avail, pwd):
    try:
        mycursor.execute("INSERT INTO ADMIN VALUES ('{}','{}','{}','{}','{}');".format(UID_D, name, dept, avail, pwd))
        mydb.commit()
        messagebox.showinfo("Doctor Added", "Doctor has been added successfully!")
    except:
        messagebox.askretrycancel("Data Error", "Values entered may be too long or of incorrect type. Try again!")
        add_doc()


def rem_doc():
    win_doc = tk.Tk()
    win_doc.geometry("828x128")
    win_doc.title("Remove Doctor")
    #win_doc.config(bg='#42b0f5')

    rem_UID = ttk.Entry(win_doc, width=50)
    l1 = ttk.Label(win_doc, text="Enter doctor's UID: ")
    l1.grid(row=0, column=0, sticky=tk.W, pady=2)
    rem_UID.grid(row=0, column=1, pady=2)

    enter = ttk.Button(win_doc, text="Submit", command=lambda: sql_rem_doc(rem_UID.get(), win_doc))
    enter.grid(row=2, column=1, pady=2)


def sql_rem_doc(UID_D, win_doc):
    mycursor.execute("SELECT UID_D FROM ADMIN;")
    data = [i[0] for i in mycursor.fetchall()]
    if UID_D in data:
        mycursor.execute(("DELETE FROM ADMIN WHERE UID_D = '{}';").format(UID_D))
        mydb.commit()
        messagebox.showinfo("Doctor Removed", "Doctor has been removed successfully!")
        close(win_doc)
    else:
        messagebox.askretrycancel("Wrong UID!", "Doctor with entered UID does not exist! Try again?")


def alter_doc():
    win_doc = tk.Tk()
    win_doc.geometry("828x128")
    win_doc.title("Alter Doctor Details")
    #win_doc.config(bg='#42b0f5')

    data = ttk.Entry(win_doc, width=50)
    data['state'] = 'disabled'
    data.grid(row=1, column=1, pady=2)

    choice = tk.StringVar(win_doc)
    choice.set("Select Field")
    fields = ['Name', 'Dept', 'Avail', 'PWD']
    options = tk.OptionMenu(win_doc, choice, *fields, command=lambda x: data.config(state='enabled'))
    options.grid(row=1, column=0)

    UID = ttk.Entry(win_doc, width=50)
    l1 = ttk.Label(win_doc, text="Enter doctor's UID: ")
    l1.grid(row=0, column=0, sticky=tk.W, pady=2)
    UID.grid(row=0, column=1, pady=2)

    enter = ttk.Button(win_doc, text="Submit", command=lambda: sql_alt_doc(UID.get(), data.get(), choice.get(), win_doc))
    enter.grid(row=2, column=1, pady=2)


def sql_alt_doc(UID_D, data, column, win_doc):
    mycursor.execute("SELECT UID_D FROM ADMIN;")
    sql_data = [i[0] for i in mycursor.fetchall()]
    if UID_D in sql_data:
        try:
            mycursor.execute(("UPDATE ADMIN SET {} = '{}' WHERE UID_D = '{}';").format(column, data, UID_D))
            mydb.commit()
            messagebox.showinfo("Doctor Altered", "Doctor details have been altered successfully! Use Show Doctor Records to check.")
            close(win_doc)
        except:
            messagebox.askretrycancel("Data Error", "Values entered may be too long or of incorrect type. Try again!")
            alter_doc()
    else:
        messagebox.askretrycancel("Wrong UID!", "Doctor with entered UID does not exist! Try again?")


def show_pat():
    mycursor.execute("SELECT UID, DOB, NAME, SEX, PH_NO FROM PAT_REG;")
    data = mycursor.fetchall()
    pat_win = tk.Tk()
    pat_win.title("Show Patient Records")
    #pat_win.config(bg='#42b0f5')
    
    tree_1 = ttk.Treeview(pat_win, columns=("c1", "c2", "c3", "c4", "c5"), show='headings')
    tree_1.heading('#1', text='Patient UID')
    tree_1.heading('#2', text='DOB')
    tree_1.heading('#3', text='Name')
    tree_1.heading('#4', text='Gender')
    tree_1.heading('#5', text='Phone Number')

    for i in data:
        tree_1.insert('', tk.END, values=i)
    tree_1.pack()
    pat_win.mainloop()


def show_vac():
    mycursor.execute("SELECT * FROM VACCINATION;")
    data = mycursor.fetchall()
    vac_win = tk.Tk()
    vac_win.title("Show Vaccines")
    #vac_win.config(bg='#42b0f5')
    
    tree_1 = ttk.Treeview(vac_win, columns=("c1", "c2"), show='headings')
    tree_1.heading('#1', text='Vaccine Name')
    tree_1.heading('#2', text='Quantity')

    for i in data:
        tree_1.insert('', tk.END, values=i)
    tree_1.pack()
    vac_win.mainloop()


def alter_vac():
    win_vac = tk.Tk()
    win_vac.geometry("828x128")
    #win_vac.config(bg='#42b0f5')
    win_vac.title("Alter Vaccine Details")

    data = ttk.Entry(win_vac, width=50)
    data['state'] = 'disabled'
    data.grid(row=1, column=1, pady=2)

    choice = tk.StringVar(win_vac)
    choice.set("Select Field")
    fields = ['V_Name', 'Qty']
    options = tk.OptionMenu(win_vac, choice, *fields, command=lambda x: data.config(state='enabled'))
    options.grid(row=1, column=0)

    name = ttk.Entry(win_vac, width=50)
    l1 = ttk.Label(win_vac, text="Enter vaccine name: ")
    l1.grid(row=0, column=0, sticky=tk.W, pady=2)
    name.grid(row=0, column=1, pady=2)

    enter = ttk.Button(win_vac, text="Submit", command=lambda: sql_alt_vac(name.get(), data.get(), choice.get(), win_vac))
    enter.grid(row=2, column=1, pady=2)


def sql_alt_vac(name, data, column, win_vac):
    mycursor.execute("SELECT V_NAME FROM VACCINATION;")
    sql_data = [i[0] for i in mycursor.fetchall()]
    if name in sql_data:
        try:
            mycursor.execute(("UPDATE VACCINATION SET {} = '{}' WHERE V_NAME = '{}';").format(column, data, name))
            mydb.commit()
            messagebox.showinfo("Vaccine Details Altered", "Vaccine details have been altered successfully! Use Show Vaccines to check.")
            close(win_vac)
        except:
            messagebox.askretrycancel("Data Error", "Values entered may be too long or of incorrect type. Try again!")
            close(win_vac)
            alter_vac()
    else:
        messagebox.askretrycancel("Wrong Vaccine name!", "Vaccine with entered name does not exist! Try again?")


def consul():
    win_consul = tk.Tk()
    win_consul.geometry("1150x360")
    #win_vac.config(bg='#42b0f5')
    win_consul.title("Show Doctor Consultations")

    choice = tk.StringVar(win_consul)
    choice.set("Select Doctor UID")
    mycursor.execute("SELECT UID_D FROM ADMIN WHERE UID_D LIKE 'D%';") 
    fields = [i[0] for i in mycursor.fetchall()]
    options = tk.OptionMenu(win_consul, choice, *fields, command=lambda x: display_consul(win_consul, choice.get()))
    options.grid(row=0, column=0)


def display_consul(win_consul, UID_D):
    tree_1 = ttk.Treeview(win_consul, columns=("c1", "c2", "c3", "c4"), show='headings')
    tree_1.heading('#1', text='Patient')
    tree_1.heading('#2', text='Date')
    tree_1.heading('#3', text='Diagnosis')
    tree_1.heading('#4', text='Prescription')
    tree_1.column(0, width = 150)
    tree_1.column(1, width = 150)
    tree_1.column(2, width = 400)
    tree_1.column(3, width = 400)
    
    mycursor.execute(("SELECT UID_P, DATE(CONSUL_DATETIME), DIAGNOSIS, PRESCRIPTION FROM CONSULTATION WHERE DOC_VAC = '{}' ORDER BY CONSUL_DATETIME DESC;").format(UID_D))
    data = mycursor.fetchmany(size=5)
    
    for i in data:
        mycursor.execute(("SELECT NAME FROM PAT_REG WHERE UID='{}';").format(i[0]))
        name = mycursor.fetchone()[0]
        copy = list(i)
        copy[0] = name
        tree_1.insert('', tk.END, values=copy)
    tree_1.place(relx=0.02, rely=0.25)


def admin():
    # Function with all admin controls
    admin_screen = tk.Tk()
    admin_screen.config(bg='#42b0f5')
    admin_screen.title("Admin Window")

    s_width = admin_screen.winfo_screenwidth()
    s_height = admin_screen.winfo_screenheight()
    admin_screen.geometry(f"{s_width}x{s_height}")

    Logout = ttk.Button(admin_screen,  command=lambda: close(admin_screen) or login(), text='Logout')
    Logout.place(relx=0.92, rely=0.027)

    s = ttk.Style()
    s.configure('my.TButton', font=('Helvetica', 15))
    showdoc = ttk.Button(admin_screen, text='\n\n  Show Doctor Records  \n\n', command=lambda: show_doc(), style='my.TButton')

    showdoc.place(relx=0.03, rely=0.6)
    #showdoc.grid(row=3, column=2)

    adddoc = ttk.Button(admin_screen, text="\n\n      Add Doctors      \n\n", command=lambda: add_doc(), style='my.TButton')
    adddoc.place(relx=0.31, rely=0.6)
    #adddoc.grid(row=3, column=4)

    remdoc = ttk.Button(admin_screen, text="\n\n    Remove Doctors     \n\n", command=lambda: rem_doc(), style='my.TButton')
    remdoc.place(relx=0.53, rely=0.6)
    #remdoc.grid(row=3, column=6)

    alterdoc = ttk.Button(admin_screen, text="\n\n Alter Doctor Records  \n\n", command=lambda: alter_doc(), style='my.TButton')
    alterdoc.place(relx=0.798, rely=0.6)
    #alterdoc.grid(row=3, column=8)

    showpat = ttk.Button(admin_screen, text="\n\n     Show Patients     \n\n", command=lambda: show_pat(), style='my.TButton')
    showpat.place(relx=0.03, rely=0.2)
    #showpat.grid(row=1, column=2)

    showvac = ttk.Button(admin_screen, text="\n\n   Show Vaccine Details   \n\n", command=lambda: show_vac(), style='my.TButton')
    showvac.place(relx=0.31, rely=0.2)
    #showvac.grid(row=1, column=4)

    altervac = ttk.Button(admin_screen, text="\n\n Alter Vaccine Details \n\n", command=lambda: alter_vac(), style='my.TButton')
    altervac.place(relx=0.53, rely=0.2)
    #altervac.grid(row=1, column=6)

    showconsul = ttk.Button(admin_screen, text="\n\n  Show Consultations  \n\n", command=lambda: consul(), style='my.TButton')
    showconsul.place(relx=0.798, rely=0.2)

    admin_screen.mainloop()


def createacc(UID, Signup_Window, dob, name, pwd, sex, p_n):
    # Creates patient account, put age, name, sex accordingly
    try:
        mycursor.execute("INSERT INTO PAT_REG VALUES('{}','{}','{}','{}',{},'{}');".format(UID, dob, name, sex, p_n, pwd))
        mydb.commit()
        messagebox.showinfo("Account created!", f"Your UID is: {UID} and your password is: {pwd}")
        close(Signup_Window)
    except:
        messagebox.showerror("Data Error", "Values entered may be too long or of incorrect type. Try again!")
        signup()


def close(obj):
    # Function to close any tkinter object
    obj.destroy()


def check(UID, pwd, Login_Window):
    # Function to check whether password is correct or not
    if UID[0] == 'P':
        mycursor.execute("SELECT UID, PWD FROM PAT_REG WHERE UID='{}';".format(UID))
        PWD_l = mycursor.fetchall()
        if PWD_l != []:
            if pwd == PWD_l[0][1]:
                close(Login_Window)
                appt_book(UID)
            else:
                messagebox.askretrycancel("Wrong password!", "Wrong password entered! Try again?")
        else:
            messagebox.askretrycancel("Wrong UID!", "Wrong UID entered! Try again?")
    elif UID[0] == 'A' or UID[0] == 'D':
        mycursor.execute("SELECT UID_D, PWD FROM ADMIN WHERE UID_D = '{}';".format(UID))
        PWD_l = mycursor.fetchall()
        if PWD_l != []:
            if pwd == PWD_l[0][1]:
                close(Login_Window)
                admin()
            else:
                messagebox.askretrycancel("Wrong password!", "Wrong password entered! Try again?")
        else:
            messagebox.askretrycancel("Wrong UID!", "Wrong UID entered! Try again?")


def signup():
    # Function for the user to sign up(shows sign up window)

    usertype = 'P'

    Signup_Window = tk.Tk()
    Signup_Window.title("Create Account")
    Signup_Window.config(bg='#42b0f5')
    Signup_Window.geometry(f"{Signup_Window.winfo_screenwidth()//2}x{Signup_Window.winfo_screenheight()//2}")
    Label_pn = ttk.Label(Signup_Window, text='Enter your Phone Number: ')
    Label_n = ttk.Label(Signup_Window, text="Enter your Name: ")
    Label_a = ttk.Label(Signup_Window, text="Enter Date of Birth(YYYY/MM/DD): ")
    Label_g = ttk.Label(Signup_Window, text="Enter Gender: ")
    Label_p = ttk.Label(Signup_Window, text="Enter Password: ")
    Label_n.place(relx=0.3, rely=0.1428571428571429)
    Label_a.place(relx=0.28, rely=0.2857142857142857)
    Label_g.place(relx=0.31, rely=0.4285714285714287)
    Label_pn.place(relx=0.29, rely=0.5714285714285716)
    Label_p.place(relx=0.3, rely=0.7142857142857145)

    Entry_n = ttk.Entry(Signup_Window)  # Textbox to enter details
    Entry_a = ttk.Entry(Signup_Window)
    Entry_g = ttk.Entry(Signup_Window)
    Entry_p = ttk.Entry(Signup_Window)
    Entry_pn = ttk.Entry(Signup_Window)

    Entry_n.place(relx=0.6, rely=0.1428571428571429)
    Entry_a.place(relx=0.6, rely=0.2857142857142857)
    Entry_g.place(relx=0.6, rely=0.4285714285714287)
    Entry_pn.place(relx=0.6, rely=0.571428571428571)
    Entry_p.place(relx=0.6, rely=0.7142857142857145)

    Submit = ttk.Button(Signup_Window, text="Submit", command=lambda: createacc(UID_gen(usertype), Signup_Window, Entry_a.get(), Entry_n.get(), Entry_p.get(),
                                                                                Entry_g.get(), Entry_pn.get()))

    Submit.place(relx=0.485, rely=0.8571428571428574)


def UID_gen(usertype):
    # Function to generate random UIDs

    if usertype=='P':
        mycursor.execute("SELECT UID FROM pat_reg ORDER BY UID DESC;")
        UID_list = mycursor.fetchall()
        if UID_list == []:
            UID = 'P00001'
        else:
            UID_last = UID_list[0]
            num = UID_last[0][1:]
            UID_newnum = str(int(num)+1)
            UID = 'P'+ '0'*(5-len(UID_newnum)) +UID_newnum
    else:
        mycursor.execute("SELECT UID_D FROM admin ORDER BY UID_D DESC")
        UID_list = mycursor.fetchall()
        if UID_list == []:
            UID = 'D00001'
        else:
            UID_last = UID_list[0]
            num = UID_last[0][1:]
            UID_newnum = str(int(str(num))+1)
            UID = 'D'+ '0'*(5-len(UID_newnum)) +UID_newnum

    return (UID)


def login():
    # Function to display login page, which is the landing page for the project.

    # Login page
    Login_Window = tk.Tk()
    Login_Window.title('Hospital Login Page')
    Login_Window.config(bg='#42b0f5')
    Login_Window.geometry(f"{Login_Window.winfo_screenwidth()//2}x{Login_Window.winfo_screenheight()//2}")

    message = ttk.Label(Login_Window, text="Welcome to Hospital Management System!")
    message.place(relx=0.33, rely=0.01)

    username = ttk.Label(Login_Window, text="Enter Username: ")
    password = ttk.Label(Login_Window, text="Enter Password: ")
    UID = ttk.Entry(Login_Window)
    pwd = ttk.Entry(Login_Window, show='*')

    username.place(relx=0.3, rely=0.3)
    password.place(relx=0.3, rely=0.5)
    UID.place(relx=0.55, rely=0.3)
    pwd.place(relx=0.55, rely=0.5)

    submit = ttk.Button(Login_Window, text="Submit", command=lambda: check(UID.get(), pwd.get(), Login_Window))
    submit.place(relx=0.456, rely=0.7)

    create_ac = ttk.Button(Login_Window, text="Don't have an account? Sign up now!", command=signup)
    create_ac.place(relx=0.35, rely=0.8)

    Login_Window.tk.mainloop()


# main
if __name__ == '__main__':
    # Connecting with db
    mysql_login()
    mycursor = mydb.cursor()
    mycursor.execute("CREATE DATABASE IF NOT EXISTS hospital_mgmt_sys;")
    mycursor.execute("USE hospital_mgmt_sys;")
    if mydb.is_connected():
        print("Connected to database")
    createTables()
    login()
    mydb.close()
    print("You have exited the program!")
