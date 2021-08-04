from tkinter import *
from tkinter import messagebox
import sqlite3
import os
import email_pass
import smtplib
import time
from homepage import homePage


class System_Login:
    def __init__(self, root):
        self.root=root
        self.root.title("WPLCT System Login")
        self.root.geometry("1350x700+0+0")
        self.root.configure(bg="white", bd=2, relief=RIDGE)
        self.otp = ''

        #======Images===
        self.warehouse_image=PhotoImage(file="images/warehouse2.png")
        self.image_frame = Label(self.root, image= self.warehouse_image, bd=0, bg="white").place(x=100, y=90)

        #=====Login Frame===
        self.user_id = StringVar()
        self.password = StringVar()

        login_frame=Frame(self.root, bd=2, relief=RIDGE, bg="white")
        login_frame.place(x=800, y=90, width=350, height=460)

        title=Label(login_frame,text="System Login", font=("Elephant", 25, "bold"),bg="white").place(x=0,y=30,relwidth=1)
        lbl_user=Label(login_frame,text="User ID", font=("Andalus", 12), bg="white", fg="#767171").place(x=50,y=100)

        txt_user_id=Entry(login_frame,textvariable=self.user_id, font=("times new roman", 15),bg="#ECECEC").place(x=50,y=140, width=250)

        lbl_pass= Label(login_frame, text="Password", font=("Andalus", 12), bg="white", fg="#767171").place(x=50,y=200)
        txt_pass = Entry(login_frame, textvariable=self.password, show="*", font=("times new roman", 15), bg="#ECECEC").place(x=50, y=240, width=250)

        btn_login=Button(login_frame, command=self.login, text="Log In", font=("Arial Rounded MT Bold", 12),bg="#00B0F0", activebackground="#00B0F0", fg="white", activeforeground="white", cursor="hand2").place(x=50, y=300, width=250)

        hr=Label(login_frame, bg="lightgray").place(x=50,y=370, width=250, height=2)
        or_=Label(login_frame, text="OR", font=("times new roman", 15, "bold"), fg="lightgray", bg="white").place(x=150,y=355)

        btn_forget=Button(login_frame, command=self.forget_window, text="Forget Password?", font=("times new roman",11), bg="white", fg="#00759E", bd=0, activebackground="white", activeforeground="#00759E").place(x=110, y=400)

        #======Register Frame ====
        register_frame = Frame(self.root, bd=2, relief=RIDGE, bg="white")
        register_frame.place(x=800, y=570, width=350, height=60)
        lbl_reg=Label(register_frame,text="WPLCT TEAM | CONTACT US: 97X-XXX-XX35", font=("times new roman", 10),bg="white").place(x=0,y=20,relwidth=1)



    #========All Functions====
    def login(self):
        con = sqlite3.connect(database=r'userdatabase.db')
        cur = con.cursor()
        try:
            if self.user_id.get()=="" or self.password.get()=="":
                messagebox.showerror("Error", "All fields are required", parent=self.root)
            else:
                cur.execute("select utype from user where uid=? AND pass=?",(self.user_id.get(), self.password.get()))
                user = cur.fetchone()
                if user==None:
                    messagebox.showerror("Error", "Invalid USERNAME/ PASSWORD", parent=self.root)
                else:
                    if user[0]=="Admin":
                        self.root.destroy()
                        os.system("python homepage.py")
                    else:
                        self.root.destroy()
                        os.system("python homepage2.py")

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to :{str(ex)}", parent=self.root)

    def forget_window(self):
        con = sqlite3.connect(database=r'userdatabase.db')
        cur = con.cursor()
        try:
            if self.user_id.get() == "":
                messagebox.showerror("Error", "User ID must be required", parent=self.root)
            else:
                cur.execute("select email from user where uid=?",(self.user_id.get(),))
                email = cur.fetchone()
                if email == None:
                    messagebox.showerror("Error", "Invalid User ID, try again", parent=self.root)
                else:
                    #======Forget Window======
                    self.var_otp=StringVar()
                    self.var_new_pass=StringVar()
                    self.var_conf_pass=StringVar()

                    #calling send_email_function()
                    chk=self.send_email(email[0])
                    if chk=='f':
                        messagebox.showerror("Error", "Connection Error, Try Again", parent=self.root)

                    else:
                        self.forget_win=Toplevel(self.root)
                        self.forget_win.title('RESET PASSWORD')
                        self.forget_win.geometry('400x350+500+100')
                        self.forget_win.focus_force()

                        title=Label(self.forget_win,text="Reset Password", font=('goudy old style', 15, 'bold'),bg="#3f51b5", fg="white").pack(side=TOP, fill=X)
                        lbl_reset=Label(self.forget_win, text="Enter OTP Sent on Registered Email", font=("times new roman", 12)).place(x=20,y=60)
                        txt_reset=Entry(self.forget_win, textvariable=self.var_otp, font=("times new roman", 12),bg="lightyellow").place(x=20,y=100,width=250,height=30)
                        self.btn_reset=Button(self.forget_win, text="VALIDATE", command=self.validate_otp, font=("times new roman", 12, "bold"),bg="lightblue")
                        self.btn_reset.place(x=280,y=100,width=100,height=30)

                        lbl_new_pass = Label(self.forget_win, text="New Password",font=("times new roman", 12)).place(x=20, y=160)
                        txt_new_pass = Entry(self.forget_win, textvariable=self.var_new_pass, show="*", font=("times new roman", 12),bg="lightyellow").place(x=20, y=190, width=250, height=30)

                        lbl_c_pass = Label(self.forget_win, text="Confirm Password",font=("times new roman", 12)).place(x=20, y=225)
                        txt_c_pass = Entry(self.forget_win, textvariable=self.var_conf_pass, show="*", font=("times new roman", 12),bg="lightyellow").place(x=20, y=255, width=250, height=30)

                        self.btn_update = Button(self.forget_win, text="UPDATE", command=self.update_password, state=DISABLED, font=("times new roman", 12, "bold"),bg="lightblue")
                        self.btn_update.place(x=150, y=300, width=100, height=30)

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to :{str(ex)}", parent=self.root)


    def update_password(self):
        if self.var_new_pass.get()=="" or self.var_conf_pass.get()=="":
            messagebox.showerror("Error", "Password is required", parent=self.forget_win)
        elif self.var_new_pass.get()!= self.var_conf_pass.get():
            messagebox.showerror("Error", "New Password and Confirm password should be same", parent=self.forget_win)
        else:
            con = sqlite3.connect(database=r'userdatabase.db')
            cur = con.cursor()
            try:
                cur.execute("Update user SET pass=? where uid=?",(self.var_new_pass.get(),self.user_id.get()))
                con.commit()
                messagebox.showinfo("Success", "Password Updated Successfully", parent=self.forget_win)
                self.forget_win.destroy()
            except Exception as ex:
                messagebox.showerror("Error", f"Error due to :{str(ex)}", parent=self.root)

    def validate_otp(self):
        if int(self.otp)==int(self.var_otp.get()):
            self.btn_update.config(state=NORMAL)
            self.btn_reset.config(state=DISABLED)
        elif self.var_otp=="":
            messagebox.showerror("Error","Please enter OTP", parent=self.forget_win)
        else:
            messagebox.showerror("Error","Invalid OTP, Try again", parent=self.forget_win)



    def send_email(self,to_):
        s=smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()
        email_=email_pass.email_
        pass_=email_pass.pass_

        s.login(email_, pass_)
        self.otp=int(time.strftime("%H%S%M"))+int(time.strftime("%S"))

        subj='WPLCT - Reset Password OTP'
        msg=f'Dear User,\n\nYour Reset OTP is {str(self.otp)}.\n\nWith Regards,\nWPLCT Team'
        msg="Subject:{}\n\n{}".format(subj,msg)
        s.sendmail(email_,to_,msg)
        chk=s.ehlo()
        if chk[0]==250:
            return's'
        else:
            return'f'



root=Tk()
obj=System_Login(root)
root.mainloop()