from tkinter import *
import sqlite3

root=Tk()
conn=sqlite3.connect('karaoke.db')
c=conn.cursor()
#to create a database
'''
c.execute("""CREATE TABLE data(
    email varchar(50),
    username varchar(100),
    password varchar(20)
     )""")

conn.commit()
conn.close()
'''
#To delete the user details
def delete():
    conn=sqlite3.connect('karaoke2.db')
    c=conn.cursor()
    c.execute("DROP TABLE songs")


    conn.commit()
    conn.close()

def submit():
    conn=sqlite3.connect('karaoke.db')
    c=conn.cursor()

    c.execute("INSERT INTO data VALUES(:email,:username,:password)",
                  {
                      'email':emailentry.get(),
                      'username':username.get(),
                      'password':password1.get(),
                      })

    conn.commit()
    conn.close()

def query():
    conn=sqlite3.connect('karaoke.db')
    c=conn.cursor()
    c.execute('SELECT *,oid FROM data')
    record=c.fetchall()
    print(record)

    conn.commit()
    conn.close()

def delete():
    conn=sqlite3.connect('karaoke.db')
    c=conn.cursor()
    c.execute("DELETE From data WHERE oid= "+delete_box.get())


    conn.commit()
    conn.close()

email=Label(root,text="E-MAIL",height=1,width=30,bg='lightblue',font="timesnewroman")
email.grid(row=1,column=0)
username_label=Label(root,text="USERNAME",height=1,width=30,bg='lightblue',font="timesnewroman")
username_label.grid(row=3,column=0)
password_label1=Label(root,text="PASSWORD",height=1,width=10,bg='lightblue',font="timesnewroman")
password_label1.grid(row=5,column=0)
password_label2=Label(root,text=" CONFIRM PASSWORD",height=1,width=20,bg='lightblue',font="timesnewroman")
password_label2.grid(row=7,column=0)
emailentry=Entry(root,width=25,bg='white',font=("timesnewroman",15))
emailentry.grid(row=2,column=0)
username=Entry(root,width=25,bg="white",font=("timesnewroman",15))
username.grid(row=4,column=0)
password1=Entry(root,width=25,bg="white",font=("timesnewroman",15))
password1.grid(row=6,column=0)
password=Entry(root,width=25,bg="white",font=("timesnewroman",15))
password.grid(row=8,column=0)


delete_box=Entry(root,width=30)
delete_box.grid(row=14,column=0)
delete_label=Label(root,text='id number')
delete_label.grid(row=13,column=0)
delete_button=Button(root,text='DELETE',command=delete)
delete_button.grid(row=15,column=0)
query_button=Button(root,text='Show records',command=query)
query_button.grid(row=9,column=0)

root.mainloop()