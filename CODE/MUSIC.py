from tkinter import *
import pygame
from tkinter import filedialog
import time
import os
from mutagen.mp3 import MP3
import tkinter.ttk as ttk
root=Tk()
root.title('KARAOKE')
root.geometry("1800x800+0+0")
img=PhotoImage(file="T:\AD\AD-1\KARAOKE\IMAGES\karoake(2).png")
Label(root,image=img).place(x=0,y=0)

#initialize pygame player
pygame.mixer.init()
#Song length
def play_time():
    #To Check double timing
    if stopped:
        return
    #Grab current song time
    current_time=pygame.mixer.music.get_pos()/1000 
    #Throw up temp label to get data
    #slider_label.config(text=f'Slider:{int(my_slider.get())}and song pos:{int(current_time)})')
    #convert to time format
    convert_current_time=time.strftime('%M:%S',time.gmtime(current_time))

    # Get the current song 
    #current_song=song_box.curselection()
    song=song_box.get(ACTIVE)
    song=f'T:/AD/AD-1/AUDIO/{song}.mp3'
    #get song with mutagen
    song_mut=MP3(song)
    #Get song length
    global song_lenth
    song_lenth=song_mut.info.length
    #convert to Time format
    convert_song_length=time.strftime('%M:%S',time.gmtime(song_lenth))
    #Increase current time by 1 second
    current_time+=1
    if int(my_slider.get())==int(song_lenth):
        status_bar.config(text=f' {convert_song_length} ')
    elif paused:
        pass
    elif int(my_slider.get())==int(current_time):
        #update slider  To position
        slider_position=int(song_lenth)
        my_slider.config(to=slider_position,value=int(current_time))
    else:
        #update slider  To position
        slider_position=int(song_lenth)
        my_slider.config(to=slider_position,value=int(my_slider.get()))
        #convert to time format
        convert_current_time=time.strftime('%M:%S',time.gmtime(int(my_slider.get())))
        #Output time to status bar
        status_bar.config(text=f'{convert_current_time} of {convert_song_length} ')
        #move this by one second
        next_time=int(my_slider.get())+1
        my_slider.config(value=next_time)
    #Output time to status bar
    #status_bar.config(text=f'{convert_current_time} of {convert_song_length} ')
    #update slider position with the song position
    #my_slider.config(value=int(current_time))
    #Update time
    status_bar.after(1000,play_time)
#Add song Function
def add_song():
    song=filedialog.askopenfilename(initialdir='AUDIO/',title='Choose A Song',filetypes=(("mp3 Files","*.mp3"), ))
    #strip out the directory info and .mp3 extensions from the song
    song=song.replace("T:/AD/AD-1/AUDIO/","")
    song=song.replace(".mp3","")
    # add song to listbox
    song_box.insert(END,song)
#add many songs playlist
def add_many_song():
    songs=filedialog.askopenfilenames(initialdir='AUDIO/',title='Choose A Song',filetypes=(("mp3 Files","*.mp3"), ))
    #loop through song list and replace directory 
    for song in songs:
        song=song.replace("T:/AD/AD-1/AUDIO/","")
        song=song.replace(".mp3","")

        # add song to listbox
        song_box.insert(END,song)
#play selected song
def play():
    #set stopped variable to false to paly song after stop
    global stopped
    stopped=False
    song=song_box.get(ACTIVE)
    song=f'T:/AD/AD-1/AUDIO/{song}.mp3'
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)

    #Call the playtime function for song length
    play_time()

    #update slider position
    #slider_position=int(song_lenth)
    #my_slider.config(to=slider_position,value=0)
    #To get current volume
    #current_volume=pygame.mixer.music.get_volume()
    #slider_label.config(current_volume*100)

global stopped
stopped=False
#To repeat a song 
def repeat_song():
    status_bar.config(text='0')
    my_slider.config(value=0)
    pygame.mixer.music.stop()
    song_box.select_clear(ACTIVE)

    status_bar.config(text='')
    play()
    global stopped
    stopped=False
#stop playing song
def stop():
    #reset slider and status bar
    status_bar.config(text='0')
    my_slider.config(value=0)
    #stop song from playing
    pygame.mixer.music.stop()
    song_box.select_clear(ACTIVE)
    #clear status bar
    status_bar.config(text='')
    #Set stop Variable to True
    global stopped
    stopped=True

#play next song in playlist
def forward():
    #reset slider and status bar
    status_bar.config(text='0')
    my_slider.config(value=0)
    # Get the current song 
    next_one=song_box.curselection()
    #Add one to the current song number
    next_one=next_one[0] + 1
    song=song_box.get(next_one)
    song=f'T:/AD/AD-1/AUDIO/{song}.mp3'
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)
    #Move active bar in playlist listbox
    song_box.select_clear(0,END)
    #Activate new song bar
    song_box.activate(next_one)
    # Set Active bar to next song
    song_box.selection_set(next_one,last=None)

#play pervious song in listbox
def back():
    #reset slider and status bar
    status_bar.config(text='0')
    my_slider.config(value=0)
    # Get the current song 
    pervious_one=song_box.curselection()
    #Add one to the current song number
    pervious_one=pervious_one[0]-1
    song=song_box.get(pervious_one)
    song=f'T:/AD/AD-1/AUDIO/{song}.mp3'
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)
    #Move active bar in playlist listbox
    song_box.select_clear(0,END)
    #Activate new song bar
    song_box.activate(pervious_one)
    # Set Active bar to next song
    song_box.selection_set(pervious_one,last=None)
#delete a song
def delete_song():
    stop()
    #Delete currently selected song
    song_box.delete(ANCHOR)
    pygame.mixer.music.stop()

#Delete all songs
def delete_all_songs():
    stop()
    #Delete All songs
    song_box.delete(0,END)
    pygame.mixer.music.stop()
#create a global pause variable
global paused
paused=False
#pause and unpause the song
def pause(is_paused):
    global paused
    paused=is_paused
    if paused:
        #unpause
        pygame.mixer.music.unpause()
        paused=False
    else:
        #pause
        pygame.mixer.music.pause()
        paused= True
    
#Create slider function
def slide(x):
    #slider_label.config(text=f'{int(my_slider.get())} of {int(song_lenth)}')
    song=song_box.get(ACTIVE)
    song=f'T:/AD/AD-1/AUDIO/{song}.mp3'
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0,start=int(my_slider.get()))

#Create volume function
def volume(x):
    pygame.mixer.music.set_volume(volume_slider.get())
    #To get current volume
    #current_volume=pygame.mixer.music.get_volume()
    #slider_label.config(current_volume*100)

#To Search a song in listbox
def search():
    #reset slider and status bar
    status_bar.config(text='0')
    my_slider.config(value=0)
    stop()
    query=search_entry.get().lower()
    song_box.delete(0,END)
    for song in all_songs:
        if query in song.lower():
            song=song.replace("T:/AD/AD-1/AUDIO/","")
            song=song.replace(".mp3","")
            song_box.insert(END,song)
songs_dict='T:\AD\AD-1\KARAOKE\AUDIO/'
all_songs=[song for song in os.listdir(songs_dict)if song.lower().endswith(".mp3")]
#to creare a function for search bar entry
def on_entry(event):
    if search_entry.get()=='Search':
        search_entry.delete(0,END)   

#Create Master Frame
master_frame=Frame(root,width=430,height=480,bg='green')
master_frame.place(x=500,y=200)

#create playlist Box
song_box=Listbox(master_frame,bg='hotpink',fg='green',width=60,height=20,selectbackground='grey',selectforeground='black')
song_box.place(x=0,y=30)
#create player control button images
back_btn=PhotoImage(file='T:\AD\AD-1\KARAOKE\IMAGES\BACK.png')
forward_btn=PhotoImage(file='T:\AD\AD-1\KARAOKE\IMAGES\FORWARD.png')
pause_btn=PhotoImage(file='T:\AD\AD-1\KARAOKE\IMAGES\pause.png')
play_btn=PhotoImage(file='T:\AD\AD-1\KARAOKE\IMAGES\play.png')
stop_btn=PhotoImage(file='T:\AD\AD-1\KARAOKE\IMAGES\stop.png')
repeat_btn=PhotoImage(file='T:\AD\AD-1\KARAOKE\IMAGES/repeat.png')
search_btn=PhotoImage(file='T:\AD\AD-1\KARAOKE\IMAGES\search.png')
#create player control frame
control_frame=Frame(master_frame,width=50)
control_frame.place(x=0,y=360)
#create volume label frame
volume_frame=LabelFrame(master_frame,text='Volume',width=60,height=140)
volume_frame.place(x=365,y=80)
#create player  control buttons
back_button=Button(control_frame,image=back_btn,borderwidth=0,command=back)
back_button.grid(row=0,column=0,padx=10)
forward_button=Button(control_frame,image=forward_btn,borderwidth=0,command=forward)
forward_button.grid(row=0,column=1,padx=10)
pause_button=Button(control_frame,image=pause_btn,borderwidth=0,command=lambda:pause(paused))
pause_button.grid(row=0,column=2,padx=10)
play_button=Button(control_frame,image=play_btn,borderwidth=0,command=play)
play_button.grid(row=0,column=3,padx=10)
stop_button=Button(control_frame,image=stop_btn,borderwidth=0,command=stop)
stop_button.grid(row=0,column=4,padx=10)
repeat_button=Button(control_frame,image=repeat_btn,borderwidth=0,command=repeat_song)
repeat_button.grid(row=0,column=5,padx=5)
#create a searech bar 
search_entry=Entry(master_frame,font=("timesnewroman",11),width=45)
search_entry.place(x=0,y=5)
search_entry.insert(0,'Search')
search_entry.bind('<FocusIn>',on_entry)
search_button=Button(master_frame,image=search_btn,borderwidth=0,height=20,command=search)
search_button.place(x=350,y=5)
#create menu
my_menu=Menu(root)
root.config(menu=my_menu)
#add song menu
add_song_menu=Menu(my_menu)
my_menu.add_cascade(label='Add Songs',menu=add_song_menu)
add_song_menu.add_command(label='Add One Song To Playlist',command=add_song)
#Add many songs to playlist
add_song_menu.add_command(label='Add many Song To Playlist',command=add_many_song)
#Create a Delete song menu
remove_song_menu=Menu(my_menu)
my_menu.add_cascade(label="Remove songs",menu=remove_song_menu)
remove_song_menu.add_command(label='Delete A Song From Playlist',command=delete_song)
remove_song_menu.add_command(label='Delete All Song From Playlist',command=delete_all_songs)
#Create status Bar
status_bar=Label(master_frame,text='',relief=GROOVE,anchor=E,bg='white',width=20)
status_bar.place(x=280,y=455)
#Create Music position Slider
my_slider=ttk.Scale(master_frame,from_=0,to=100,orient=HORIZONTAL,value=0,command=slide,length=360)
my_slider.place(x=0,y=420)
#Create volume slider
volume_slider=ttk.Scale(volume_frame,from_=0,to=1,orient=VERTICAL,value=1,command=volume,length=125)
volume_slider.place(x=15,y=0)

#slider_label=Label(root,text='0')
#slider_label.place(x=600,y=620)

root.mainloop()