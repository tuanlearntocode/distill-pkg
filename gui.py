import tkinter as tk
from distill import Distill
from pathlib import Path
import openpyxl


parent = Path(__file__).resolve().parent
workBook = openpyxl.load_workbook(str(parent) + '\data.xlsx')
sheetNames = workBook.sheetnames
sheetNames.sort()

root = tk.Tk()  # create root window
root.title("Distillation Premium")
root.config(bg="skyblue")
root.maxsize(900, 600)
root.iconbitmap('favicon.ico')

# Create Frame widget
fr1 = tk.Frame(root, width=200, height=300, bg='#efc760')
fr1.grid(row=0, column=0, padx=10, pady=10)
fr2 = tk.Frame(root, width=200, height=300, bg='#efc760')
fr2.grid(row=0, column=1, padx=10, pady=10)
fr3 = tk.Frame(root, width=200, height=300, bg='#efc760')
fr3.grid(row=0, column=2, padx=10, pady=10)
fr_btn = tk.Frame(root, bg='purple', width=100, height=100)
fr_btn.grid(row=1, column=0, padx=5, pady=5)

# Frame 1
xw = tk.Label(fr1, text='xw = ').grid(row=0, column=0, padx=1, pady=1)
in_xw = tk.Entry(fr1, width=10)
in_xw.grid(row=0, column=1, padx=1, pady=1)

xf = tk.Label(fr1, text='xf = ').grid(row=1, column=0, padx=1, pady=1)
in_xf = tk.Entry(fr1, width=10)
in_xf.grid(row=1, column=1, padx=1, pady=1)

xd = tk.Label(fr1, text='xd = ').grid(row=2, column=0, padx=1, pady=1)
in_xd = tk.Entry(fr1, width=10)
in_xd.grid(row=2, column=1, padx=1, pady=1)

comp = tk.Label(fr1, text='Composition: ').grid(
    row=3, column=0, padx=1, pady=1)
value_inside = tk.StringVar(fr1)
value_inside.set("Choose composition")
in_comp = tk.OptionMenu(fr1, value_inside, *sheetNames)
in_comp.grid(row=3, column=1, padx=1, pady=1)

# Frame 2
yw = tk.Label(fr2, text='yw = ').grid(row=0, column=0, padx=1, pady=1)
result_yw = tk.Label(fr2, text='', width=10).grid(
    row=0, column=1, padx=1, pady=1)

yf = tk.Label(fr2, text='yf = ').grid(row=1, column=0, padx=1, pady=1)
result_yf = tk.Label(fr2, text='', width=10).grid(
    row=1, column=1, padx=1, pady=1)

yd = tk.Label(fr2, text='yd = ').grid(row=2, column=0, padx=1, pady=1)
result_yd = tk.Label(fr2, text='', width=10).grid(
    row=2, column=1, padx=1, pady=1)

yf_vapor = tk.Label(fr2, text='yf* = ').grid(row=3, column=0, padx=1, pady=1)
result_yf_vapor = tk.Label(fr2, text='', width=10).grid(
    row=3, column=1, padx=1, pady=1)

# Frame 3
R_min = tk.Label(fr3, text='R_min = ').grid(row=0, column=0, padx=1, pady=1)
result_R_min = tk.Label(fr3, text='', width=10).grid(
    row=0, column=1, padx=1, pady=1)

R = tk.Label(fr3, text='R = ').grid(row=1, column=0, padx=1, pady=1)
result_R = tk.Label(fr3, text='', width=10).grid(
    row=1, column=1, padx=1, pady=1)

t_stage = tk.Label(fr3, text='Theory stages = ').grid(
    row=2, column=0, padx=1, pady=1)
result_t_stage = tk.Label(fr3, text='', width=10).grid(
    row=2, column=1, padx=1, pady=1)


def calculation_yx():
    xw = float(in_xw.get())
    xf = float(in_xf.get())
    xd = float(in_xd.get())
    compostion = value_inside.get()
    oDistill = Distill(xf, xw, xd, compostion)
    oDistill.initial_calulate()
    oDistill.draw_yx()


def calculation_tx():
    xw = float(in_xw.get())
    xf = float(in_xf.get())
    xd = float(in_xd.get())
    compostion = value_inside.get()
    oDistill = Distill(xf, xw, xd, compostion)
    oDistill.draw_tx()


def result():
    xw = float(in_xw.get())
    xf = float(in_xf.get())
    xd = float(in_xd.get())
    compostion = value_inside.get()
    oDistill = Distill(xf, xw, xd, compostion)
    oDistill.initial_calulate()

    # Fram 2
    result_yw = tk.Label(fr2, text=oDistill.yw, width=10).grid(
        row=0, column=1, padx=1, pady=1)
    result_yf = tk.Label(fr2, text=oDistill.yf, width=10).grid(
        row=1, column=1, padx=1, pady=1)
    result_yd = tk.Label(fr2, text=oDistill.yd, width=10).grid(
        row=2, column=1, padx=1, pady=1)
    result_yf_vapor = tk.Label(fr2, text=oDistill.yf_vapor, width=10).grid(
        row=3, column=1, padx=1, pady=1)

    # Frame 3
    result_R_min = tk.Label(fr3, text=oDistill.R_min, width=10).grid(
        row=0, column=1, padx=1, pady=1)
    result_R = tk.Label(fr3, text=oDistill.R, width=10).grid(
        row=1, column=1, padx=1, pady=1)
    result_t_stage = tk.Label(fr3, text=oDistill.t_stage, width=10).grid(
        row=2, column=1, padx=1, pady=1)


# Frame button
btn1 = tk.Button(fr_btn, text='T-x chart',
                 command=calculation_tx).grid(row=0, column=0)
btn2 = tk.Button(fr_btn, text='y-x chart',
                 command=calculation_yx).grid(row=0, column=1)
btn3 = tk.Button(fr_btn, text='Calculate',
                 command=result).grid(row=0, column=2)

# Calculation
# Can not conversion data get from entry to float directly so I put it into a function


def run():
    root.mainloop()
