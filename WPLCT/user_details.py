from tkinter import*
from tkinter import ttk,messagebox
import sqlite3

class userClass:
    def __init__(self, root):
        self.root=root
        self.root.geometry("1100x500+220+140")
        self.root.title("Warehouse Pallet Detection and Tracking")
        self.root.config(bg="white")
        self.root.focus_force()

        #======All Variables=======
        self.var_user_id = StringVar()
        self.var_name = StringVar()
        self.var_email = StringVar()
        self.var_password = StringVar()
        self.var_utype = StringVar()


      # =======title=========
        user_Frame = Frame(self.root, bd=2, relief=RIDGE, bg="white")
        user_Frame.place(x=10, y=10, width=450, height=480)
        title=Label(user_Frame, text="Manage User Details", font=("goudy old style", 18), bg="#0f4d7d", fg="white").pack(side=TOP, fill=X)


        # =========Content======
        # ==row1==
        lbl_empid = Label(user_Frame, text="Emp ID", font=("goudy old style", 14), bg="white").place(x=30,y=60)
        txt_empid = Entry(user_Frame, textvariable=self.var_user_id, font=("goudy old style", 14),bg="lightyellow").place(x=150, y=60, width=200)

        lbl_name = Label(user_Frame, text="Name", font=("goudy old style", 14), bg="white").place(x=30, y=130)
        txt_name = Entry(user_Frame, textvariable=self.var_name, font=("goudy old style", 14),bg="lightyellow").place(x=150, y=130, width=200)

        lbl_email = Label(user_Frame, text="Email", font=("goudy old style", 14), bg="white").place(x=30,y=200)
        txt_email = Entry(user_Frame, textvariable=self.var_email, font=("goudy old style", 14),bg="lightyellow").place(x=150, y=200, width=200)

        lbl_password = Label(user_Frame, text="Password", font=("goudy old style", 14), bg="white").place(x=30,y=270)
        txt_password = Entry(user_Frame, textvariable=self.var_password, font=("goudy old style", 14),bg="lightyellow").place(x=150, y=270, width=200)


        lbl_utype = Label(user_Frame, text="User Type", font=("goudy old style", 14), bg="white").place(x=30, y=340)
        cmb_utype = ttk.Combobox(user_Frame, textvariable=self.var_utype, values=("Select", "Admin", "Employee"),state="readonly", font=("goudy old style", 14))
        cmb_utype.place(x=150, y=340, width=200)
        cmb_utype.current(0)


        btn_add = Button(user_Frame, text="Add", command=self.add, font=("goudy old style", 15), bg="#2196f3",fg="white", cursor="hand2").place(x=40, y=420, width=100, height=28)
        btn_update = Button(user_Frame, text="Update", command=self.update, font=("goudy old style", 15),bg="#4caf50", fg="white", cursor="hand2").place(x=160, y=420, width=100, height=28)
        btn_delete = Button(user_Frame, text="Delete", command=self.delete, font=("goudy old style", 15),bg="#f44336", fg="white", cursor="hand2").place(x=290, y=420, width=100, height=28)


        #User Details Tree View
        u_frame = Frame(self.root, bd=2, relief=RIDGE)
        u_frame.place(x=480, y=10, width=600, height=480)

        scrolly = Scrollbar(u_frame, orient=VERTICAL)
        scrollx = Scrollbar(u_frame, orient=HORIZONTAL)

        self.userTable = ttk.Treeview(u_frame,columns=("uid", "name", "email", "password", "utype"),yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.userTable.xview)
        scrolly.config(command=self.userTable.yview)

        self.userTable.heading("uid", text="U ID")
        self.userTable.heading("name", text="Name")
        self.userTable.heading("email", text="Email")
        self.userTable.heading("password", text="Password")
        self.userTable.heading("utype", text="User Type")

        self.userTable["show"] = "headings"

        self.userTable.column("uid", width=70)
        self.userTable.column("name", width=90)
        self.userTable.column("email", width=100)
        self.userTable.column("password", width=100)
        self.userTable.column("utype", width=90)

        self.userTable.pack(fill=BOTH, expand=1)
        self.userTable.bind("<ButtonRelease-1>", self.get_data)
        self.show()


    #=========All Functions===========
    def add(self):
        con=sqlite3.connect(database=r'userdatabase.db')
        cur=con.cursor()
        try:
            if self.var_user_id.get()=="" or self.var_name.get()=="" or self.var_email.get()=="" or self.var_password.get()=="":
                messagebox.showerror("Error","All Fields are required", parent=self.root)
            else:
                cur.execute("Select * from user where uid=?", (self.var_user_id.get(),))
                row=cur.fetchone()
                if row!=None:
                    messagebox.showerror("Error", "This User ID is already assigned, try different", parent=self.root)
                else:
                    cur.execute("Insert into user (uid,name,email,pass,utype) values(?,?,?,?,?)",(
                                            self.var_user_id.get(),
                                            self.var_name.get(),
                                            self.var_email.get(),
                                            self.var_password.get(),
                                            self.var_utype.get(),
                                            
                    ))
                    con.commit()
                    messagebox.showinfo("Success", "User Added Successfully", parent=self.root)
                    self.show()
                    self.clear()

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to :{str(ex)}", parent=self.root)


    def show(self):
        con = sqlite3.connect(database=r'userdatabase.db')
        cur = con.cursor()
        try:
            cur.execute("select * from user")
            rows=cur.fetchall()
            self.userTable.delete(*self.userTable.get_children())
            for row in rows:
                self.userTable.insert('', END, values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to :{str(ex)}", parent=self.root)


    def get_data(self, ev):
        f=self.userTable.focus()
        content=(self.userTable.item(f))
        row=content['values']
        self.var_user_id.set(row[0])
        self.var_name.set(row[1])
        self.var_email.set(row[2])
        self.var_password.set(row[3])
        self.var_utype.set(row[4])
        
    def update(self):
        con=sqlite3.connect(database=r'userdatabase.db')
        cur=con.cursor()
        try:
            if self.var_user_id.get()=="":
                messagebox.showerror("Error","User ID must be required", parent=self.root)
            else:
                cur.execute("Select * from user where uid=?", (self.var_user_id.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error", "Invalid User ID", parent=self.root)
                else:
                    cur.execute("Update user set name=?,email=?,pass=?, utype=? where uid=?",(
                                            self.var_name.get(),
                                            self.var_email.get(),
                                            self.var_password.get(),
                                            self.var_utype.get(),
                                            self.var_user_id.get(),

                    ))
                    con.commit()
                    messagebox.showinfo("Success", "User Updated Successfully", parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to :{str(ex)}", parent=self.root)


    def delete(self):
        con=sqlite3.connect(database=r'userdatabase.db')
        cur=con.cursor()
        try:
            if self.var_user_id.get()=="":
                messagebox.showerror("Error","User ID must be required", parent=self.root)
            else:
                cur.execute("Select * from user where uid=?", (self.var_user_id.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error", "Invalid User ID", parent=self.root)
                else:
                    op=messagebox.askyesno("Confirm", "Do you really want to delete", parent=self.root)
                    if op==True:
                        cur.execute("delete from user where uid=?",(self.var_user_id.get(),))
                        con.commit()
                        messagebox.showinfo("Delete", "User Deleted Successfully", parent=self.root)
                        self.clear()

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to :{str(ex)}", parent=self.root)

    def clear(self):
        self.var_user_id.set("")
        self.var_name.set("")
        self.var_email.set("")
        self.var_password.set("")
        self.var_utype.set("Select")
        self.show()


if __name__=="__main__":
    root=Tk()
    obj = userClass(root)
    root.mainloop()