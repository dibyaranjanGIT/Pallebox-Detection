from tkinter import*
from tkinter import ttk,messagebox, filedialog
import cv2
import tkinter
from tkinter import Tk, Label
from PIL import Image as Img
from PIL import ImageTk
import imutils
import datetime
from tkinter import *
from tkvideo import tkvideo


class dashboardClass:
    def __init__(self, root):
        self.root=root
        self.root.geometry("1100x500+220+140")
        self.root.title("Warehouse Pallet Detection and Tracking")
        self.root.config(bg="white")
        self.root.focus_force()

        #====Variables====
        self.var_filename = StringVar()

        #===Browse====
        lbl_select_folder = Label(self.root, text="Select File", font=("times new roman", 12, "bold"), bg="white").place(x=20,y=20)
        folder_name = Entry(self.root, textvariable=self.var_filename, font=("times new roman", 12), state='readonly',bg="lightyellow").place(x=110, y=20, height=28, width=560)
        self.btn_browse = Button(self.root, command=self.browse_function, text="BROWSE",font=("times new roman", 12, "bold"), bg="#262626", fg="white", activebackground="#262626",cursor="hand2", activeforeground="white").place(x=690, y=19, height=28, width=80)
        # self.btn_barcode = Button(self.root, command=self.VideoStream, text="QR READER",font=("times new roman", 12, "bold"), bg="#4caf50", fg="white", activebackground="#4caf50",cursor="hand2", activeforeground="white").place(x=830, y=19, height=28)
        self.btn_stop = Button(self.root, command=self.VideoStream, text="LIVE STREAM",font=("times new roman", 12, "bold"), bg="#f44336", fg="white", activebackground="#f44336",cursor="hand2", activeforeground="white").place(x=960, y=19, height=28)

        #===Dividing line
        hr = Label(self.root, bg="lightgray").place(x=20, y=60, height=2, width=1060)

        #===Frame===
        self.vid_frame=Label(self.root, bd=3, relief=RIDGE)
        self.vid_frame.place(x=20, y=82, height=400, width=650)


        #====Data Section====
        self.lbl_pallet = Label(self.root, text="Total Pallets\n[0]", bd=2, relief=RIDGE, bg="#607d8b", fg="white",font=("goudy old style", 12, "bold"))
        self.lbl_pallet.place(x=730, y=100, height=150, width=165)

        self.lbl_barcode = Label(self.root, text="Barcode Info\n[0]", bd=2, relief=RIDGE, bg="#607d8b", fg="white",font=("goudy old style", 12, "bold"))
        self.lbl_barcode.place(x=920, y=100, height=150, width=165)

        self.lbl_data = Label(self.root, text="Other Data\n[0]", bd=2, relief=RIDGE, bg="#607d8b", fg="white",font=("goudy old style", 12, "bold"))
        self.lbl_data.place(x=730, y=300, height=150, width=350)




    def browse_function(self):
        filepath = filedialog.askopenfilename(initialdir="C:\\Users\\PycharmProjects\\Main",
                                              title="Open file okay?",
                                              filetypes=(("all files", "*.*"),
                                                         ))
        file = open(filepath, 'r')
        self.play_video()

    def play_video(self):
        player = tkvideo("PalleteVideo.mp4", self.vid_frame, loop=1, size=(690, 400))
        player.play()

    #======Live Stream===

    def VideoStream(self):
        panel = None
        window = None
        camera = None
        self.panel = tkinter.Label(self.vid_frame)
        self.panel.pack()
       # initialize camera
        self.camera = cv2.VideoCapture(0)
        self.camera1()

    def camera1(self):
        _,frame = self.camera.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = Img.fromarray(frame)
        frame = ImageTk.PhotoImage(frame)
        self.panel.configure(image=frame)
        self.panel.image = frame
        self.panel.after(1, self.camera1)

    def stop_stream(self):
        pass


if __name__=="__main__":
    root=Tk()
    obj = dashboardClass(root)
    root.mainloop()