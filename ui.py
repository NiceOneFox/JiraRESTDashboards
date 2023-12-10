from tkinter import *

from main import func
from main2 import func2
from main3 import func3
from main4 import func4
from main5 import func5
from main6 import func6

window = Tk()
window.title("Графики JIRA")
window.geometry('600x400')

btn = Button(window, text="График1", command=func)
btn.grid(column=1, row=0)

btn2 = Button(window, text="График2", command=func2)
btn2.grid(column=2, row=0)

btn3 = Button(window, text="График3", command=func3)
btn3.grid(column=3, row=0)

btn4 = Button(window, text="График4", command=func4)
btn4.grid(column=4, row=0)

btn5 = Button(window, text="График5", command=func5)
btn5.grid(column=5, row=0)

btn6 = Button(window, text="График6", command=func6)
btn6.grid(column=6, row=0)

window.mainloop()
