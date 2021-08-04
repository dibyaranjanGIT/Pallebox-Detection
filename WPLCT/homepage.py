from tkinter import*
from PIL import Image, ImageTk
import sqlite3
from tkinter import messagebox
import os
import time
from user_details import userClass
from dashboard import dashboardClass

class homePage:
    def __init__(self, root):
        self.root=root
        # self.root.geometry("1100x500+220+130")
        self.root.geometry("1350x700+0+0")
        self.root.title("Warehouse Pallet Detection and Tracking")
        self.root.config(bg="white")

        self.icon_title = PhotoImage(file="images/logo.png")
        title = Label(self.root, text="Warehouse Pallet Detection and Tracking", image=self.icon_title, compound=LEFT,font=("times new roman", 20, "bold"), bg="#010c48", fg="white", anchor="w", padx=20).place(x=0,y=0,relwidth=1,height=70)

        btn_logout = Button(self.root, command=self.logout, text="Logout", font = ("times new roman", 15, "bold"), bg="lightblue", cursor="hand2" ).place(x=1150, y=10, height=50, width=150)

        lbl_col = Label(self.root, bg="#4d636d", fg="white").place(x=0, y=70, relwidth=1, height=30)

        LeftMenu = Frame(self.root, bd=2, relief=RIDGE, bg="white")
        LeftMenu.place(x=0, y=102, width=200, height=160)

        self.icon_side = PhotoImage(file="images/side.png")
        lbl_menu = Label(LeftMenu, text="Menu", font=("times new roman", 20, "bold"), bg="lightblue").pack(side=TOP,fill=X)

        #====Menu Buttons
        btn_dashboard = Button(LeftMenu, command=self.dashboard, text="Dashboard", image=self.icon_side, compound=LEFT,padx=5, anchor="w", font=("times new roman", 16, "bold"), bg="white", bd=2, cursor="hand2").pack(side=TOP, fill=X)
        self.btn_users = Button(LeftMenu, command=self.user_details, text="Users", image=self.icon_side, compound=LEFT,padx=5, anchor="w", font=("times new roman", 16, "bold"), bg="white", bd=2,cursor="hand2")
        self.btn_users.pack(side=TOP, fill=X)
        btn_exit = Button(LeftMenu, command=self.exit, text="Exit", image=self.icon_side, compound=LEFT,padx=5, anchor="w", font=("times new roman", 16, "bold"), bg="white", bd=2,cursor="hand2").pack(side=TOP, fill=X)

        #===Footer==
        lbl_footer = Label(self.root, bg="#4d636d", fg="white").place(x=0, y=665, relwidth=1, height=35)


        #========Functions========

    def user_details(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = userClass(self.new_win)

    def dashboard(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = dashboardClass(self.new_win)


    def logout(self):
        self.root.destroy()
        os.system("python login.py")

    def exit(self):
        self.root.destroy()


if __name__=="__main__":
    root=Tk()
    obj = homePage(root)
    root.mainloop()