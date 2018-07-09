
# coding: utf-8

# In[ ]:


import sqlite3
from tkinter import *
import webbrowser
import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import fpdf
import random
pdf = fpdf.FPDF(format='letter')
from PIL import ImageTk, Image
conn=sqlite3.connect('paper.db')
c=conn.cursor()

# to view all the table deatials in the database
c.execute("SELECT name FROM sqlite_master where type='table';")
print(c.fetchall())

#c.execute("""CREATE TABLE EASY6(ID INT PRIMARY KEY NOT NULL, QS CHAR(1000) NOT NULL)""")
#c.execute("INSERT INTO testpaper VALUES ('Difference between A* and AO*',5,37)")
#c.execute("SELECT * FROM testpaper")
#print(c.fetchall())
#conn.commit()
#conn.close()

def pdfgen(list1,list2,list3):
    pdf.add_page()
    pdf.set_font("Arial", size=15)
    pdf.cell(200,15,"Question paper NCU 2018", ln=1, align="C")
    pdf.set_font("Arial",'i', size=14)
    pdf.cell(200,15,"Generated using an automated paper generation system", ln=1, align="C")
    pdf.set_font("Times", size=10)
    pdf.cell(167,15,"Max Marks : 100", align="left")
    pdf.cell(100,15,"Time : 3 Hours",ln=1, align="right")
    pdf.set_font("Arial",'b', size=13)
    pdf.cell(134,15,"Section A", align="left")
    pdf.set_font("Arial",'i', size=11)
    pdf.cell(100,15,"Max marks for this section are 4",ln=1, align="left")
    pdf.set_font("Times", size=10)
    for i in range(5):
        pdf.cell(170,6,"Q"+str(i+1)+": "+list1[i][0],ln=1,align="left")
    pdf.set_font("Arial",'b', size=13)
    pdf.cell(134,15,"Section B", align="left")
    pdf.set_font("Times",'i', size=11)
    pdf.cell(100,15,"Max marks for this section are 6",ln=1, align="left")
    pdf.set_font("Arial", size=10)
    for i in range(5):
        pdf.cell(170,6,"Q"+str(i+1)+": "+list2[i][0],ln=1,align="left")
    pdf.set_font("Arial",'b', size=13)
    pdf.cell(133,15,"Section C", align="left")
    pdf.set_font("Times",'i', size=11)
    pdf.cell(100,15,"Max marks for this section are 10",ln=1, align="left")
    pdf.set_font("Arial", size=10)
    for i in range(5):
        pdf.cell(170,6,"Q"+str(i+1)+": "+list3[i][0],ln=1,align="left")
    pdf.output("test.pdf")
    fromaddr = "bobbyverma96@yahoo.in"
    toaddr = "gokuverma94@gmail.com"

    msg = MIMEMultipart()

    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "Generated test paper"
    body = "Here is your generated test sir"
    msg.attach(MIMEText(body, 'plain'))

    filename = "test.pdf"
    attachment = open("D:\\blah\\test.pdf", "rb")

    part = MIMEBase('application', 'octet-stream')
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment; filename= %s" % filename)

    msg.attach(part)
    conn=smtplib.SMTP('smtp.gmail.com',587)
    conn.ehlo()
    conn.starttls()
    conn.login('gokuverma94@gmail.com',os.environ["pass"])
    text = msg.as_string()
    conn.sendmail(fromaddr, toaddr, text)
    conn.quit()

def addqs(qs, marks, diff):
    c.execute("SELECT MAX(ID) FROM "+diff+marks)
    data = c.fetchone()
    if data[0] is None:
        i = 1
    else:
        i = data[0] + 1
    c.execute("INSERT INTO "+diff+marks+" VALUES("+str(i)+",\""+qs+"\");")
    print(qs)
    conn.commit()
    

def ques_select(diff3):
    c.execute("SELECT MAX(ID) FROM "+diff3+"4")
    data1=c.fetchone()
    c.execute("SELECT MAX(ID) FROM "+diff3+"6")
    data2=c.fetchone()
    c.execute("SELECT MAX(ID) FROM "+diff3+"10")
    data3=c.fetchone()
    
    if data1[0]<5 or data2[0]<5 or data3[0]<5:
        print("Not sufficient elements in Tables")
        exit()
    else:
        rand1 = random_num_gen(data1[0])
        rand2 = random_num_gen(data2[0])
        rand3 = random_num_gen(data3[0])
    obj1 = []
    obj2 = []
    obj3 = []
    for i in range(5):
        c.execute("SELECT QS FROM "+diff3+"4 WHERE "+"ID = "+str(rand1[i]))
        obj1.append(list(c.fetchone()))
        c.execute("SELECT QS FROM "+diff3+"6 WHERE "+"ID = "+str(rand2[i]))
        obj2.append(list(c.fetchone()))
        c.execute("SELECT QS FROM "+diff3+"10 WHERE "+"ID = "+str(rand3[i]))
        obj3.append(list(c.fetchone()))
    pdfgen(obj1,obj2,obj3)
    
def random_num_gen(n):
    rlist = random.sample(range(n),5)
    rlist = [x+1 for x in rlist]
    return rlist

def genwin():
    main=Toplevel()
    main.geometry("600x400+8+400")
    main.title("Generate Test")
    canvas=Canvas(main,width=470,height=80,relief='raised',borderwidth=3)
    canvas.grid(row=0,column=1,padx=50,pady=20)
    canvas.create_text(250,50,fill="blue",font="Times 13 italic bold",
                            text="Generated test will be e-mailed to you!!!")
    
    def click2():
        diff3=variable.get()
        ques_select(diff3)
    
    frame=Frame(main)
    frame.grid(row=1,column=1,padx=50,pady=40)
    frame2=Frame(frame)
    frame2.grid(row=0,column=1,padx=50,pady=40)
    button1=Button(frame,text="Generate test",font="Times 10 italic bold")
    gg=Label(frame,text="Please select the complexity level")
    gg.grid(row=0,column=0)
    OPTIONS = ['Easy','Medium','Hard']
    variable = StringVar()
    variable.set(OPTIONS[0])

    w = OptionMenu(frame2, variable, *OPTIONS)
    w.grid(row=0,column=1)
    button1.config( height =2, width = 13,bg="yellow", command=click2)
    button1.grid(row=1,column=0,padx=10,pady=30)

def addwin():
    main=Toplevel()
    main.geometry("600x400+8+400")
    main.title("Add Question")
    canvas=Canvas(main,width=470,height=80,relief='raised',borderwidth=3)
    canvas.grid(row=0,column=1,padx=80,pady=20)
    canvas.create_text(250,50,fill="green",font="Times 15 italic bold",
                            text="Please Add Relevant Questions")
    def click1():
        ques=namez.get()
        diff=variable1.get()
        marks=variable2.get()
        c.execute("create table if not exists "+diff+marks+" (ID INT PRIMARY KEY NOT NULL, QS CHAR(1000) NOT NULL)")
        addqs(ques, marks, diff)
    frame=Frame(main)
    lbl1 = Label(frame, text = "Enter question",background='#ECECEC')
    lbl1.grid(row=0,column=0,pady=0)      
    namez=Entry(frame)
    namez.grid(row=0,column=1,pady=0)
    lbl2=Label(frame,text="Enter Question complexity")
    lbl2.grid(row=1,column=0)
    OPTIONS = ['Easy','Medium','Hard']
    variable1 = StringVar()
    variable1.set(OPTIONS[0])
    namez2 = OptionMenu(frame, variable1, *OPTIONS)
    namez2.grid(row=1,column=1)
    
    lbl3=Label(frame,text="Enter The Marks")
    lbl3.grid(row=2,column=0)
    OPTIONS = [4,6,10]
    variable2 = StringVar()
    variable2.set(OPTIONS[0])
    namez3 = OptionMenu(frame, variable2, *OPTIONS)
    namez3.grid(row=2,column=1)
    frame.grid(row=1,column=1,padx=50,pady=40)
    button1=Button(frame,text="Add Question To Database",font="Times 10 italic bold",command=click1)
    button1.config( height =2, width = 30,bg="yellow")
    button1.grid(row=3,column=1,padx=0)

def mainwin():
    main = Tk()
    main.title("Test Generator System")
    img = ImageTk.PhotoImage(Image.open("a.gif"))
    main.geometry("800x600+8+400")

    canvas=Canvas(main,width=470,height=80,relief='raised',borderwidth=3)
    canvas.grid(row=0,column=4,padx=80,pady=20)
    canvas.create_text(250,50,fill="green",font="Times 15 italic bold",
                            text="Best Test Generator Ever! Easy to use too!!")

    text=Label(main,text="Welcome to Test Generator, if you have new questions please add them",font="Times 15 italic bold")
    text.configure(bg="green",foreground="yellow")
    text.grid(row=1,column=4,padx=80,pady=40)
    panel = Label(main, image = img,height=220,width=600)
    panel.grid(row=3,column=4,padx=80,pady=20)
    frame=Frame(main)
    frame.grid(row=4,column=4,padx=50,pady=20)
    button1=Button(frame,text="Add Question",font="Times 10 italic bold",command=addwin)
    button1.config( height =3, width = 15,bg="green")
    button1.grid(row=0,column=0,padx=50)
    button2=Button(frame,text="Generate test",font="Times 10 italic bold",command=genwin)
    button2.config( height =3, width = 15,bg="yellow")
    button2.grid(row=0,column=1)
    main.mainloop()
mainwin()

