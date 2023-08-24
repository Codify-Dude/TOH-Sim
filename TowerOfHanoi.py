import random
import time
from tkinter import *
import turtle
largefont = ('Calibri 20')

window = Tk()
window.title('Tower Of Hanoi')
window.geometry('1500x720')
window.resizable(False,False)
canvas = Canvas(window,height=630, width=1200, bg='White')
canvas.grid(row=0, column=0, sticky=NW ,columnspan=5)

screen = turtle.TurtleScreen(canvas)
draw = turtle.RawTurtle(screen)



class Pin(turtle.RawTurtle):
    def __init__(self, xpos):
        super().__init__(canvas,shape='square')
        self.xpos = xpos
        self.up()
        self.color('grey')
        self.shapesize(14,1)
        self.goto(self.xpos,-60)
        self.count = 0
        self.pos_list = [-180,-160, -140, -120, -100, -80, -60, -40, -20, 0]
        self.discs = []

class Disc(turtle.RawTurtle):
    def __init__(self, xpos, ypos, size, color):
        super().__init__(canvas,shape='square')
        self.xpos = xpos
        self.ypos = ypos
        self.size = size
        self.color(color)
        self.up()
        self.shapesize(1,self.size)
        self.goto(self.xpos,self.ypos)

def move_disc(disc, pin):
    while disc.ycor()<100:
        disc.goto(disc.xcor(),disc.ycor()+5)
        draw._update()
    disc.goto(pin.xcor(),100)
    # disc.goto(pin.xcor(),50)
    draw._update()
    while disc.ycor()>pin.pos_list[pin.count]:
        disc.goto(disc.xcor(),disc.ycor()-5)
        draw._update()
    time.sleep(0.01)

def move(f,t):
    if f == 'A':
        top_disc = pin1.discs[-1]
        start_pin = pin1
    elif f == 'B':
        top_disc = pin2.discs[-1]
        start_pin = pin2
    elif f == 'C':
        top_disc = pin3.discs[-1]
        start_pin = pin3

    if t == 'A':
        pin = pin1
    elif t == 'B':
        pin = pin2
    elif t == 'C':
        pin = pin3
        
    move_disc(top_disc,pin)
    start_pin.count-=1
    start_pin.discs.pop()
    pin.count+=1
    pin.discs.append(top_disc)

text = Text(window,width=25,bg='White',font='Calibri 16')
text.config(borderwidth=0,state=DISABLED)
text.grid(row=0,column=5,rowspan=3,sticky=NSEW)
v=Scrollbar(window,orient='vertical',command=text.yview)
v.grid(row=0,column=6,rowspan=3,sticky=NSEW)
text['yscrollcommand'] = v.set


# n number of discs
# f from position, h helper(via) and target pin
count = 0

def hanoi(n,f,h,t):
    global count
    if Start_Button['state'] == DISABLED:
        if n == 0:  
            # Prevent from moving 0 or negative discs
            pass
        else:
            hanoi(n-1,f,t,h) # move all but bottom to helper (A to B using C)
            n1=str(n)
            count+=1
            if Start_Button['state'] == DISABLED:
                canvas3.delete('all')
                canvas3.create_text(130,20,fill="black",font='Calibri 20', text=count)
            speed = int(Speed_Selector.get())
            screen.tracer(speed)
            s="  Move disk "+n1+" from "+f+" to "+t+"\n"
            if Start_Button['state'] == DISABLED:
                text.config(state=NORMAL)
                text.insert(END,s)
                text.see('end')
                text.config(state=DISABLED)
            move(f,t) # move bottom disc to target (from A to C)
            # print ("Move disk",n,"from source",f,"to destination",t)
            hanoi(n-1,h,f,t) # move rest from helper to target via from (from B to C using A)
    

label1 = Label(window, text='Discs', font=largefont, bg='Orange')
label1.grid(row=1,column=0,sticky=NSEW)
label1.config(borderwidth=3,relief=GROOVE)
Disc_selector = Scale(window, from_=1, to=10, orient='horizontal',bg='Orange')
Disc_selector.set(5)
Disc_selector.grid(row=2,column=0,sticky=NSEW)

label2 = Label(window, text='Speed', font=largefont, bg='Orange')
label2.grid(row=1,column=1,sticky=NSEW)
label2.config(borderwidth=3,relief=GROOVE)
Speed_Selector = Scale(window, from_=1, to=5, orient='horizontal',bg='Orange')
Speed_Selector.grid(row=2,column=1,sticky=NSEW)

label3 = Label(window, text='Moves', font=largefont, bg='Orange',borderwidth=3,relief=GROOVE)
label3.grid(row=1,column=2,sticky=NSEW)
canvas3 = Canvas(window, height=30,width=110,bg='White')
canvas3.grid(row=2,column=2,sticky=NSEW)
canvas3.create_text(130,20,fill="black",font='Calibri 20 bold', text=count)
def start():
    count=0
    speed = int(Speed_Selector.get())
    screen.tracer(speed)
    Start_Button['state'] = DISABLED
    Stop_Button['state'] = NORMAL
    Reset_Button['state'] = DISABLED
    Disc_selector['state'] = DISABLED
    global pin1
    global pin2
    global pin3 
    base = turtle.RawTurtle(screen)
    base.color('grey')
    base.shape('square')
    base.up()
    base.goto(0,-200)
    base.shapesize(1,57)

    pin1 = Pin(-400)
    pin2 = Pin(0)
    pin3 = Pin(400)
    pin1.discs = [] 
    
    pin1.count = int(Disc_selector.get())
    size = 15.5
    ypos = -180
    for i in range(pin1.count):
        r = (random.randint(0,255))/255
        g = (random.randint(0,255))/255
        b = (random.randint(0,255))/255
        rgb = [r,g,b]
        disc = Disc(-400, ypos, size, rgb)
        pin1.discs.append(disc)
        size-=1.5
        ypos+=20
    hanoi(pin1.count,'A','B','C')
    Stop_Button['state'] = DISABLED
    if Start_Button['state'] == DISABLED:
        Reset_Button['state'] = NORMAL
    Disc_selector['state'] = NORMAL
def stop():
    global count
    canvas3.delete('all')
    count=0
    canvas3.create_text(130,20,fill="black",font='Calibri 20', text=count)
    canvas.delete('all')
    text.config(state=NORMAL)
    text.delete('1.0','end')
    text.config(state=DISABLED)
    Start_Button['state'] = NORMAL
    Reset_Button['state'] = DISABLED
    Stop_Button['state'] = DISABLED
    Disc_selector['state'] = NORMAL

Start_Button = Button(window, text='START',font=('Calibri 12 bold'),bg='#33b249',fg='White',activeforeground='White',activebackground='#33b249',command=start,disabledforeground='Grey')
Start_Button.grid(row=1,column=3,sticky=NSEW)

Stop_Button = Button(window, text='STOP',font=('Calibri 12 bold'),bg='red',fg='White',activeforeground='White',activebackground='red',command=stop)
Stop_Button.grid(row=1,column=4,sticky=NSEW)
Stop_Button['state'] = DISABLED


Reset_Button = Button(window, text='RESET',font=('Calibri 12 bold'),bg='#4681f4',fg='White',activeforeground='White',activebackground='#4681f4',command=stop )
Reset_Button.grid(row=2,column=3,sticky=NSEW,columnspan=2)  
Reset_Button['state'] = DISABLED

window.mainloop()