from tkinter import *
import sqlite3
from tkinter import messagebox
root=Tk()
root.title('KARAOKE')
root.geometry("1800x800+0+0")
img=PhotoImage(file="IMAGES/karoake(2).png")
Label(root,image=img).place(x=0,y=0)
conn=sqlite3.connect('karaoke.db')
c=conn.cursor()
def clear():
    emailentry.delete(0,END)
    username.delete(0,END)
    password1.delete(0,END)
    password.delete(0,END)

def database():
    if emailentry.get()=='' or username.get()=='' or password1.get()==''or password.get()=='':
        messagebox.showerror('Error','ALL DETAILS ARE REQURIED')
    elif password1.get()!=password.get():
        messagebox.showerror('Error','PASSWORD MISMATCH')
    else:
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
        messagebox.showinfo('Success','Registration is success')
        clear()
        root.destroy()
        import LOGIN

def user_login():
    root.destroy()
    import LOGIN

f2=Frame(root,height=450,width=400,bg='lightblue')
f2.place(x=950,y=180)
email=Label(f2,text="E-MAIL",height=1,width=30,bg='lightblue',font="timesnewroman")
email.place(x=-70,y=30)
username_label=Label(f2,text="USERNAME",height=1,width=30,bg='lightblue',font="timesnewroman")
username_label.place(x=-50,y=100)
password_label1=Label(f2,text="PASSWORD",height=1,width=10,bg='lightblue',font="timesnewroman")
password_label1.place(x=60,y=160)
password_label2=Label(f2,text=" CONFIRM PASSWORD",height=1,width=20,bg='lightblue',font="timesnewroman",)
password_label2.place(x=55,y=220)
emailentry=Entry(f2,width=25,bg='white',font=("timesnewroman",15))
emailentry.place(x=70,y=70)
username=Entry(f2,width=25,bg="white",font=("timesnewroman",15))
username.place(x=70,y=130)
password1=Entry(f2,width=25,bg="white",font=("timesnewroman",15),show="*")
password1.place(x=70,y=190)
password=Entry(f2,width=25,bg="white",font=("timesnewroman",15),show="*")
password.place(x=70,y=250)

Button(f2,text='SIGNUP',bg='white',command=database).place(x=230,y=300)
Button(f2,text='BACK',bg='white',command=user_login).place(x=100,y=300)
conn.commit()
conn.close()

root.mainloop()