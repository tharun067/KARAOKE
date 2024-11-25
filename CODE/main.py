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
def forgot_password():
    def change_password():
        if username.get()=='' or forgot_new_entry.get()=='' or forgot_entry.get()=='':
            messagebox.showerror('Error','All Details Are requried',parent=window)
        elif forgot_new_entry.get()!=forgot_entry.get():
            messagebox.showerror('Error','Password Mismatch',parent=window)
        else:
            conn=sqlite3.connect('karaoke.db')
            c=conn.cursor()
            c.execute("SELECT * FROM data WHERE username=?",(username.get(),))
            row=c.fetchone()
            if row==None:
                messagebox.showerror('Error','Incorrect username')
            else:
                params=(forgot_entry)
                c.execute("UPDATE data SET forgot_new_entry=? AND ?=? WHERE username=?",(forgot_new_entry.get(),forgot_entry.get(),username.get(),))
                conn.commit()
                conn.close()
                messagebox.showinfo('Success','Password is reset,please login with new paswword')
                window.destroy()
            
    window=Toplevel()
    window.geometry("1600x800+0+0")
    img=PhotoImage(file="IMAGES/karoake(2).png")
    Label(window,image=img).place(x=300,y=0)
    f3=Frame(window,height=400,width=400,bg='pink')
    f3.place(x=950,y=180)
    forgot_label=Label(f3,text='USERNAME',height=5,width=40,bg='pink')
    forgot_label.place(x=-20,y=30)
    username=Entry(f3,width=40)
    username.place(x=90,y=90)
    forgot_new=Label(f3,text='NEW PASSWORD',height=1,width=20,bg='pink')
    forgot_new.place(x=45,y=120)
    forgot_new_entry=Entry(f3,width=25,)
    forgot_new_entry.place(x=90,y=150)
    forgot_con=Label(f3,text='CONFORM PASSWORD',height=1,width=20,bg='pink')
    forgot_con.place(x=55,y=185)
    forgot_entry=Entry(f3,width=25)
    forgot_entry.place(x=90,y=210)
    forgot_home=Button(f3,text='CONTINUE',command=change_password)
    forgot_home.place(x=180,y=250)
    forgot_back=Button(f3,text='BACK',command=home)
    forgot_back.place(x=120,y=250)

    window.mainloop()



    

def home():
    if username.get()=='' or password.get()=='':
        messagebox.showerror('Error','ALL Details Are Required')
    else:
        conn=sqlite3.connect('karaoke.db')
        c=conn.cursor()
        c.execute("SELECT * FROM data WHERE username=? and password=?",(username.get(),password.get()))
        row=c.fetchone()
        if row==None:
            messagebox.showerror('Error','Invalid username or password')
        else:
            messagebox.showinfo('Welcome','Login successful')
            root.destroy()
            import MUSIC

        conn.commit()
        conn.close()
    





def user_signup():
    root.destroy()
    import SIGNUP




f1=Frame(root,height=400,width=400,bg='white')
f1.place(x=950,y=180)
name=Label(f1,text='USERNAME',height=1,width=10,bg='white',fg='deeppink',borderwidth=10,font="timesnewroman")
name.place(x=90,y=40)
pas=Label(f1,text='PASSWORD',height=5,width=10,bg='white',borderwidth=10,font='timesnewroman')
pas.place(x=90,y=80)
Label(f1,text='New to karaoke?',height=15,width=10,bg='white',borderwidth=10).place(x=100,y=180)
username=Entry(f1,width=15,font=("timesnewroman",15),bg="pink")
username.place(x=100,y=90)
password=Entry(f1,width=15,font=("timesnewroman",15),bg="pink",show='*')
password.place(x=100,y=160)
login_button=Button(f1,text='LOGIN',bg='white',cursor='hand2',command=home)
login_button.place(x=150,y=230)
signup_button=Button(f1,text='SIGNUP',bg='pink',cursor='hand2',bd=0,command=user_signup)
signup_button.place(x=150,y=320)
password_button=Button(f1,text='forgot password',height=1,bg='white',fg='blue',bd=0,command=forgot_password)
password_button.place(x=170,y=190)


conn.commit()
conn.close()
root.mainloop()