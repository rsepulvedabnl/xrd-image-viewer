from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from ..iovalidation import *
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from ..plotting import DataPlotter
import sys
from ..config import *

class RootWindowBuilder:
    def __init__(self):
        self.root = Tk()

    def buildroot(self):
        def nextwindow(rt, win, dt):
            PreviewWindow(rt, dt)
            win.withdraw()

        def validate(dir, sid, pid):
            arevalid, fsel, msg = PathEntryValidator.validateall(dir, sid, pid)

            if arevalid:
                nextwindow(self.root, self.root, fsel)
            else:
                messagebox.showerror(message=msg)
        
        def btn_path_pressed(pvar):
            p = filedialog.askdirectory()
            pvar.set(p)

        

        
        self.root.title("XRD Image Viewer")
        self.root.minsize(400,400)
        self.root.geometry("+25+25")
        self.root.rowconfigure(0, minsize=400)
        self.root.columnconfigure(0, minsize=400)

        content = Frame(self.root)
        content.grid(row=0, column=0, sticky="nsew")
        content.columnconfigure(0, minsize=400)

        lbl_welcome = Label(content, text="Welcome to the XRD Image Viewer!")
        lbl_welcome.grid(row=0, column=0)

        lbl_step1 = Label(content, text="STEP 1 : Select a scan directory.")
        lbl_step1.grid(row=1, column=0, sticky="w")

        sel_dir = Frame(content)
        sel_dir.grid(row=2, column=0)
        dirpath = StringVar()
        dirpath.set("")
        entry_path = Entry(sel_dir, textvariable=dirpath, width=40)
        entry_path.grid(row=0, column=0, padx=5)
        btn_path = Button(sel_dir, text="Select Directory", command=lambda : btn_path_pressed(dirpath))
        btn_path.grid(row=0, column=1, padx=5)

        lbl_step2 = Label(content, text="STEP 2 : Enter a scan identifier.")
        lbl_step2.grid(row=3, column=0, sticky="w")

        sel_scan = Frame(content)
        sel_scan.grid(row=4, column=0)
        scanid = StringVar()
        scanid.set("17Aug20")
        entry_scanid = Entry(sel_scan, textvariable=scanid, width=40)
        entry_scanid.grid(row=0, column=0, padx=5)

        lbl_step3 = Label(content, text="STEP 3 : Enter a point identifier regex (if different from default).")
        lbl_step3.grid(row=5, column=0, sticky="w")

        sel_point = Frame(content)
        sel_point.grid(row=6, column=0)
        pointid = StringVar()
        pointid.set("\d\d\d_data_")
        entry_pointid = Entry(sel_point, textvariable=pointid, width=40)
        entry_pointid.grid(row=0, column=0, padx=5)

        btn_submit = Button(content, text="Submit", command=lambda : validate(dirpath.get(), scanid.get(), pointid.get()))
        btn_submit.grid(row=7, column=0, sticky="e")
    
    def getroot(self):
        return self.root

class PreviewWindow:
    def __init__(self, root, sel):
        def nextwindow(rt, win, dt):
            FunctionWindow(rt, dt)
            win.destroy()

        def redraw(idx, ax, min, max):
            if int(min) < int(max):
                path = self.fileselection.pointpaths[int(idx)]
                DataPlotter.plotpath(path, ax, min, max)
                plt.draw()
            else:
                messagebox.showwarning(message="Int Min. must be less than Int Max.")

        def idxshift(idxscale, shift, npoints):
            newidx = int(idxscale.get()) + shift
            if (newidx >= 0) and (newidx <= npoints-1):
                idxscale.set(newidx)

        self.root = root
        self.fileselection = sel
        self.window = Toplevel(root)
        self.window.title("Image Previewer")
        self.window.minsize(400,400)
        self.window.geometry("+25+25")
        self.window.rowconfigure(0, minsize=400)
        self.window.columnconfigure(0, minsize=400)
        self.window.protocol("WM_DELETE_WINDOW", lambda : exit())

        # btn_spec = Button(self.window, text="Special Window", command=lambda : nextwindow(self.root, self.window))
        # btn_spec.grid()

        content = Frame(self.window)
        content.grid(row=0, column=0, sticky="nsew")
        content.columnconfigure(0, minsize=100)
        content.columnconfigure(1, minsize=300)

        header_frame = Frame(content)
        panel_frame = ttk.Labelframe(content, text="Controls")
        plot_frame = Frame(content)
        header_frame.grid(row=0, column=0, columnspan=2)
        panel_frame.grid(row=1, column=0)
        plot_frame.grid(row=1, column=1)
        header_frame.columnconfigure(0, minsize=200)
        header_frame.columnconfigure(1, minsize=200)
        panel_frame.columnconfigure(0, minsize=100)

        scanid = StringVar()
        scanid.set("Scan ID : "+self.fileselection.getscanregex())
        imgtotal = StringVar()
        imgtotal.set("Image Total : "+str(self.fileselection.getpointcount()))
        lbl_scanid = Label(header_frame, textvariable=scanid)
        lbl_imgtotal = Label(header_frame, textvariable=imgtotal)
        lbl_scanid.grid(row=0, column=0, sticky="w")
        lbl_imgtotal.grid(row=0, column=1, sticky="e")

        idx = IntVar()
        idx.set(0)
        intmin = IntVar()
        intmin.set(0)
        intmax = IntVar()
        intmax.set(1e4)

        fig, ax = plt.subplots()
        DataPlotter.plotpath(self.fileselection.pointpaths[idx.get()], ax, intmin.get(), intmax.get())
        canvas = FigureCanvasTkAgg(fig, master=plot_frame)
        toolbar = NavigationToolbar2Tk(canvas, plot_frame)
        toolbar.grid(row=0, column=0)
        canvas.get_tk_widget().grid(row=1, column=0)

        idx_scale = Scale(panel_frame, orient="horizontal", length=90, from_=0, to=self.fileselection.getpointcount()-1, variable=idx, label="Image Index", command=lambda val : redraw(val, ax, intmin.get(), intmax.get()))
        intmin_scale = Scale(panel_frame, orient="horizontal", length=90, from_=0, to=MINHIGH, variable=intmin, label="Int Min.", command=lambda val : redraw(idx.get(), ax, val, intmax.get()))
        intmax_scale = Scale(panel_frame, orient="horizontal", length=90, from_=0, to=MAXHIGH, variable=intmax, label="Int Max.", command=lambda val : redraw(idx.get(), ax, intmin.get(), val))
        idx_scale.grid(row=0, column=0)
        intmin_scale.grid(row=1, column=0)
        intmax_scale.grid(row=2, column=0)

        movebtn_frame = Frame(panel_frame)
        movebtn_frame.grid(row=3, column=0)
        btn_back = Button(movebtn_frame, text="<", command=lambda : idxshift(idx_scale, -1, self.fileselection.getpointcount()))
        btn_forw = Button(movebtn_frame, text=">", command=lambda : idxshift(idx_scale, 1, self.fileselection.getpointcount()))
        btn_back.grid(row=0, column=0)
        btn_forw.grid(row=0, column=1)

        btn_func = Button(panel_frame, text="Apply Functions", command=lambda : nextwindow(self.root, self.window, self.fileselection))
        btn_func.grid(row=4, column=0)



class FunctionWindow():
    def __init__(self, root, sel):
        self.root = root
        self.fileselection = sel
        self.window = Toplevel(root)
        self.window.title("Function Wizard")
        self.window.minsize(400,400)
        self.window.geometry("+25+25")
        self.window.rowconfigure(0, minsize=400)
        self.window.columnconfigure(0, minsize=400)
        self.window.protocol("WM_DELETE_WINDOW", lambda : exit())

        content = Frame(self.window)
        content.grid(row=0, column=0, sticky="nsew")
        content.columnconfigure(0, minsize=100)
        content.columnconfigure(1, minsize=300)

        panel_frame = Frame(content)
        plot_frame = Frame(content)
        panel_frame.grid(row=0, column=0, padx=FPANELPADX, pady=FPANELPADY)
        plot_frame.grid(row=0, column=1)
        panel_frame.columnconfigure(0, minsize=100)

        fns = ["Max", "Max - BG", "Avg - Bg"]
        fnsvar = StringVar(value=fns)
        fnlist = Listbox(panel_frame, listvariable=fnsvar)
        fnlist.grid(row=0, column=0, sticky="ew")