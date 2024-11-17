from tkinter import*
import customtkinter as ctk
from tkinter import messagebox
from tkinter import ttk
import sqlite3
from PIL import Image, ImageTk


count=0
count2=0
nup_rely=1.07

f1on_off=0
f2on_off=0
class notification():
    def notification_animation(self):
        global nup_rely
        if nup_rely>=0.85:
            notification_box.place(relx=0.65,rely=nup_rely,anchor='center')
            nup_rely=nup_rely-0.005
            win.after(1,self.notification_animation)
        else:
            nup_rely=1.07
            pass
    
    def messages(self,message):
        global notification_label
        notification_label.config(text=message)
        self.notification_animation()

def main_window():
    main_canvas1.pack(fill='both',expand=True)
    main_canvas1.create_image(400,250, image=wallpaper1, anchor='center')

def title_animation():
    global count,count2
    title_line="WELCOME to "
    title_line2="Password Manager "
    
    if count!=12:
        main_canvas.itemconfig(headers,text=title_line[:count])
        win.after(50,title_animation)
        count+=1
    else:
        if count2!=17:
            main_canvas.itemconfig(headers2,text=title_line2[:count2],fill='#f1c40f')
            win.after(50,title_animation)
            count2+=1
        else:
            pass

frame_rely=1
frame_relwidth=0.01               
def frame_animation():
    global frame_rely,frame_relwidth
    if frame_rely>=0.45:
        creator_frame.place(relx=0.54,rely=frame_rely,relheight=0.5,relwidth=0.01)
        frame_rely=frame_rely-0.005
        win.after(1,frame_animation)
    else:
        if frame_relwidth<=0.5:
            creator_frame.place(relx=0.52,rely=frame_rely,relheight=0.5,relwidth=frame_relwidth,anchor=CENTER)
            frame_relwidth+=0.005
            win.after(2,frame_animation)
        else:
            pass
    

def content_animation() :
    global create_password,create_button
    create_password.pack(pady=(50,20))   
    create_button.pack(pady=0)    

def content_animation2():
    enter_password.pack(pady=(50,20))   
    enter_button.pack(pady=0)
def createpass_erase(event):
    createpassval.set('')
    create_password.configure(text_color='black')

def enterpass_erase(event):
    enterpassval.set('')
    enter_password.configure(text_color='black')

def category_erase(event):
    preset.set('')
    category.configure(text_color='black')

def save_password():
    password_path='data\\password.txt'
    pass_file=open(password_path,'w')
    password_data=createpassval.get()
    pass_file.write(password_data)
    pass_file.close()
    run_path='data\\run.txt'
    run_data=open(run_path,'w')
    run_data.write('1')
    run_data.close()
    create_button.configure(text='Password saved! Kindly RESTART the app.',fg_color='#e74c3c',text_color='white',
                            hover_color='#e74c3c')

def check_password():
    password_path='data\\password.txt'
    pass_file=open(password_path,'r')
    password_data=enterpassval.get()
    if pass_file.read()==password_data:
        main_canvas.pack_forget()
        main_window()
    else:
        messagebox.showerror('Authentication Error',f'Entered password {enterpassval.get()} is wrong!\nPlease try again.')
relxx=1.25
def add_data():
    global relxx,f1on_off,f2on_off
    if f2on_off==1:
        close_screen_frame()
        win.after(1000,add_data)
    elif relxx>=0.68:
        add_data_frame.place(relx=relxx,rely=0.35,anchor='center')
        relxx=relxx-0.05
        win.after(2,add_data)
        f1on_off=1
    else:
        relxx=1.25
        pass

relyy=0.85
def notification_down(event):
    global relyy
    if relyy<=1.07:
        notification_box.place(relx=0.65,rely=relyy,anchor='center')
        relyy=relyy+0.005
        win.after(1,lambda:notification_down(event))
    else:
        relyy=0.85
        pass
    
def clear_inputs():
    category.delete(0,END)
    preset.set('Enter application/website name')
    user_id.delete(0,END)
    password.delete(0,END)
    email.delete(0,END)

relxxx=0.68
def close_frame():
    global relxxx,f1on_off
    if relxxx<=1.25:
        add_data_frame.place(relx=relxxx,rely=0.35,anchor='center')
        relxxx+=0.005
        win.after(1,close_frame)
        f1on_off=0
    else:
        relxxx=0.68
        pass
def insert_record(category, user_id, password, email):
    global notifications
    conn = sqlite3.connect('data\\storage.db')
    cursor = conn.cursor()

    if not password:
        notifications.messages(message="Error: PASSWORD cannot be NULL or empty.")
        return

    try:
        # Insert the record into the table
        insert_query = '''
        INSERT INTO pmanager (CATEGORY, USER_ID, PASSWORD, EMAIL)
        VALUES (?, ?, ?, ?);
        '''
        
        cursor.execute(insert_query, (category, user_id, password, email))
        conn.commit()
        notifications.messages(message=f"Record inserted successfully.")
    
    except sqlite3.IntegrityError as e:
        # Check for duplicate category error (Unique constraint violation)
        if 'UNIQUE constraint failed: pmanager.CATEGORY' in str(e):
            notifications.messages(message=f"Error: CATEGORY '{category}' already exists.\n Cannot insert duplicate.")
        else:
            notifications.messages(message=f"Error: {e}")
    conn.close()

def data_displayer():
    global notifications
    conn = sqlite3.connect('data\\storage.db')
    cursor = conn.cursor()

    # Query to fetch the USER_ID and CATEGORY from the table
    select_query = '''
    SELECT SLNO, CATEGORY FROM pmanager;
    '''

    # Execute the query
    cursor.execute(select_query)

    # Fetch all the rows from the result
    rows = cursor.fetchall()

    # Print the output as a list of tuples (original form)
    
    if rows:
        main_data=rows
        main_data=sorted(main_data, key=lambda x: x[0])
        # print(main_data)
        for item in data_display.get_children():
            data_display.delete(item)
            
        for data in main_data :
            data_display.insert("",END,values=data)
    else:
        pass

    # Close the connection
    conn.close()

def save_inputs():
    insert_record(preset.get(),useridval.get(),passwordval.get(),emailval.get())
    conn = sqlite3.connect('data\\storage.db')
    cursor = conn.cursor()

    # Query to fetch the USER_ID and CATEGORY from the table
    select_query = '''
    SELECT SLNO, CATEGORY FROM pmanager;
    '''
    cursor.execute(select_query)

    rows = cursor.fetchall()
    if rows:
        main_data=rows
        main_data=sorted(main_data, key=lambda x: x[0])
    else:
        notifications.messages(message="No records found.")

    conn.close()
    
    for item in data_display.get_children():
        data_display.delete(item)
        
    for data in main_data :
        data_display.insert("",END,values=data)

sfrelxx=1.25
def show_data_frame(event):
    global sfrelxx,f1on_off,f2on_off
    if f1on_off==1:
        close_frame()
        win.after(1000,lambda:show_data_frame(event))
    elif sfrelxx>=0.68:
        screen_frame.place(relx=sfrelxx,rely=0.35,anchor='center')
        sfrelxx=sfrelxx-0.05
        win.after(7,lambda:show_data_frame(event))
        f2on_off=1
    else:
        sfrelxx=1.25
        pass

sfrelxxx=0.68
def close_screen_frame():
    global sfrelxxx, f2on_off
    if sfrelxxx<=1.25:
        screen_frame.place(relx=sfrelxxx,rely=0.35,anchor='center')
        sfrelxxx+=0.005
        win.after(1,close_screen_frame)
        f2on_off=0
    else:
        sfrelxxx=0.68
        pass

def data_fetcher(finder):
    
    conn = sqlite3.connect('data\\storage.db') 
    cursor = conn.cursor()

    
    category_value = finder  
    query = "SELECT * FROM pmanager WHERE CATEGORY = ?"
    cursor.execute(query, (category_value,))

    rows = cursor.fetchall()
    for row in rows:
        slno = row[0] 
        application_name = row[1]
        user_id = row[2] 
        password = row[3]  
        email = row[4]  
        
    data=f'''
    
    
    
  SLNO:  {slno}
  Application/website name:  {application_name}
  User ID:  {user_id}
  Password: {password}
  Email:  {email}
    '''
    data_textbox.config(state=NORMAL)
    data_textbox.delete('1.0',END)
    data_textbox.insert(END,data)
    data_textbox.config(state=DISABLED)
    # Close the database connection
    conn.close()

# def remove_selection():
#     data_display.selection_remove(data_display.selection())
        
def on_row_click(event):
    global f1on_off

    try:
        selected_item = data_display.selection()
        
        if selected_item:
            item_data = data_display.item(selected_item[0])['values']
            occupation = item_data[1]
            # win.after(500,remove_selection)
        
        data_fetcher(finder=occupation)
    except UnboundLocalError:
        # data_display.selection_remove(data_display.selection())
        pass
def delete_data():
    selected_item = data_display.selection()
    if selected_item:
        item_data = data_display.item(selected_item[0])['values']
        slno = item_data[0]

    conn = sqlite3.connect('data\\storage.db')
    cursor = conn.cursor()

    slno_value = slno 

    sql_query = "DELETE FROM pmanager WHERE SLNO = ?"

    cursor.execute(sql_query, (slno_value,))

    conn.commit()

    notifications.messages(message='Data deleted Successfully!')

    # Close the cursor and the connection
    cursor.close()
    conn.close()
    mess="\n\n\t\t No data to show!"
    data_textbox.config(state=NORMAL)
    data_textbox.delete('1.0',END)
    data_textbox.insert(END,mess)
    data_textbox.config(state=DISABLED)
    data_displayer()

def errorr():
    notifications.messages(message="Currently Update option is not Supported!\nDelet the data and renter the new one!")
    
win=Tk()
win.geometry("800x500")
win.title('Password Manager')
iconlogo='assets\\title.ico'
win.iconbitmap(iconlogo)

notifications=notification()

main_frame = Frame(win)
main_frame.propagate(False)
main_frame.pack(fill='both',expand=True)

main_canvas=Canvas(main_frame,bd=0,highlightthickness=0, relief='ridge')
main_canvas.propagate(False)
main_canvas.pack(fill='both',expand=True)

wallpaper_path='assets\\background.png'
load_wallpaper=Image.open(wallpaper_path).resize((800,500))
wallpaper=ImageTk.PhotoImage(load_wallpaper)
main_canvas.create_image(400,250, image=wallpaper, anchor='center')

headers=main_canvas.create_text(190,20, anchor='n',fill='#ecf0f1',text='', font=("Arial Black", 20))
headers2=main_canvas.create_text(510,10, anchor='n',fill='white',text='', font=("Arial Black", 30))
title_animation()


creator_frame=Frame(main_canvas,relief='ridge',bd=3,bg='#ebf5fb')
creator_frame.propagate(False)
creator_frame.place(relx=0.55,rely=1.0,relheight=0.5,relwidth=0.01)
win.after(2500,frame_animation)
run_path='data\\run.txt'
run_data=open(run_path,'r')
if run_data.read()=='0':
    run_data.close()
    createpassval=StringVar()
    create_password=ctk.CTkEntry(creator_frame,height=40,width=350,border_color='#d4ac0d',textvariable=createpassval,
                                font=('Calibri (Body)',12,'bold'),text_color='#b2babb',corner_radius=2,fg_color='#fcf3cf')
    createpassval.set('Create Your Password')
    create_password.bind("<ButtonRelease-1>",createpass_erase)

    create_button=ctk.CTkButton(creator_frame,text='Create Password',text_color='black',fg_color='green',height=40,width=100,
                                corner_radius=10,font=('Calibri (Body)',12,'bold'),command=save_password)

    win.after(3500,content_animation)
else:
    run_data.close()
    enterpassval=StringVar()
    enter_password=ctk.CTkEntry(creator_frame,height=40,width=350,border_color='#d4ac0d',textvariable=enterpassval,
                                font=('Calibri (Body)',12,'bold'),text_color='#b2babb',corner_radius=2,fg_color='#fcf3cf')
    enterpassval.set('Enter Your Password')
    enter_password.bind("<ButtonRelease-1>",enterpass_erase)

    enter_button=ctk.CTkButton(creator_frame,text='Login',text_color='white',fg_color='#3498db',height=40,width=100,
                                corner_radius=10,font=('Calibri (Body)',12,'bold'),command=check_password)

    win.after(3500,content_animation2)
    
    main_canvas1=Canvas(main_frame,bd=0,highlightthickness=0, relief='ridge')
    main_canvas1.propagate(False)

    wallpaper_path1='assets\\background1.png'
    load_wallpaper1=Image.open(wallpaper_path1).resize((800,500))
    wallpaper1=ImageTk.PhotoImage(load_wallpaper1)
    
    data_frame=ctk.CTkFrame(main_canvas1,width=300,border_color='#1abc9c',border_width=3,fg_color='#d1f2eb')
    data_frame.propagate(False)
    data_frame.pack(side=LEFT,fill=Y,padx=10,pady=10)
    
    style = ttk.Style()

    # Set the font for Treeview widget (use any valid font)
    style.configure("Treeview" ,font=('Calibri (Body)',11))

    # You can also modify the font for the headings separately:
    style.configure("Treeview.Heading",font=('Calibri (Body)',12,'bold'))
    
    column=('slno','mc')
    data_display=ttk.Treeview(data_frame,columns=column,show='headings')
    data_display.heading('slno',text='ID')
    data_display.heading('mc',text='Application/Sites')
    
    data_display.column('slno',width=40,anchor='w')
    data_display.column('mc',anchor='center')
    data_display.pack(fill=BOTH,expand=True,padx=(7,25),pady=7)
    
    data_display.bind("<<TreeviewSelect>>", lambda event:[on_row_click(event),show_data_frame(event)])
    
    scrollbar = ttk.Scrollbar(data_frame, orient="vertical", command=data_display.yview)
    data_display.configure(yscroll=scrollbar.set)
    scrollbar.place(relx=0.9521,width=15,height=466,anchor='center',rely=0.5)
    
    data_displayer()
    
    add_path='assets\\plus.png'
    load_add=Image.open(add_path).resize((70,70))
    add=ImageTk.PhotoImage(load_add)
    add_button=Button(main_canvas1,image=add,relief='flat',command=add_data)
    add_button.pack(anchor='se',padx=20,pady=20,side='bottom')
                                #0.68
    add_data_frame=ctk.CTkFrame(main_canvas1,fg_color='#ebdef0',height=300,width=400,border_color='#6c3483',
                                border_width=3)
    add_data_frame.propagate(False)
    preset=StringVar()
    category=ctk.CTkEntry(add_data_frame,height=40,width=250,font=('Calibri (Body)',12,'bold'),border_color='#f1c40f'
                          ,textvariable=preset,text_color='#95a5a6',corner_radius=20)
    preset.set('Enter application/website name')
    category.pack(pady=15)
    
    category.bind("<ButtonRelease-1>",category_erase)
    
    user_id_label=Label(add_data_frame,text='User ID (if any):',font=('Calibri (Body)',11,'bold'),fg='#6c3483',bg='#ebdef0')
    user_id_label.place(relx=0.17,rely=0.3,anchor='center')

    useridval=StringVar()
    user_id=ctk.CTkEntry(add_data_frame,height=40,width=250,font=('Calibri (Body)',13,'bold'),border_color='#f1c40f'
                          ,textvariable=useridval,text_color='#717d7e',corner_radius=20)
    user_id.place(x=130,y=70)
    
    password_label=Label(add_data_frame,text='Password(must):',font=('Calibri (Body)',11,'bold'),fg='#6c3483',bg='#ebdef0')
    password_label.place(relx=0.17,rely=0.45,anchor='center')
    
    passwordval=StringVar()
    password=ctk.CTkEntry(add_data_frame,height=40,width=250,font=('Calibri (Body)',13,'bold'),border_color='#f1c40f'
                          ,textvariable=passwordval,text_color='#717d7e',corner_radius=20)
    password.place(x=130,y=115)
    
    email_label=Label(add_data_frame,text='Email(if any):',font=('Calibri (Body)',11,'bold'),fg='#6c3483',bg='#ebdef0')
    email_label.place(relx=0.17,rely=0.6,anchor='center')
    
    emailval=StringVar()
    email=ctk.CTkEntry(add_data_frame,height=40,width=250,font=('Calibri (Body)',13,'bold'),border_color='#f1c40f'
                          ,textvariable=emailval,text_color='#717d7e',corner_radius=20)
    email.place(x=130,y=160)
    
    save_button=ctk.CTkButton(add_data_frame,text='Save',font=('Calibri (Body)',13,'bold'),fg_color='#2ecc71',
                              text_color='black',height=40,width=100,corner_radius=20,command=save_inputs)
    
    clear_button=ctk.CTkButton(add_data_frame,text='Clear',font=('Calibri (Body)',13,'bold'),fg_color='#c0392b',
                              text_color='white',height=40,width=100,corner_radius=20,command=clear_inputs)
    
    close_button=ctk.CTkButton(add_data_frame,text='Close',font=('Calibri (Body)',13,'bold'),fg_color='#34495e',
                              text_color='white',height=40,width=100,corner_radius=20,command=close_frame)
    close_button.pack(side=RIGHT,anchor='s',pady=25,padx=(15,25))
    clear_button.pack(side=RIGHT,anchor='s',pady=25,padx=15)
    save_button.pack(side=RIGHT,anchor='s',pady=25)
    
    screen_frame=ctk.CTkFrame(main_canvas1,fg_color='#f9e79f',height=300,width=400,border_color='#d4ac0d',
                                border_width=3)
    screen_frame.propagate(False)
    
    data_textbox=Text(screen_frame,relief='ridge',bd=3,font=('Calibri (Body)',10,'bold'),
                      state=DISABLED,bg='#f9e79f',fg='#117864')
    data_textbox.place(x=10,y=10,height=200,width=380)
    
    update_button=ctk.CTkButton(screen_frame,text='Update',font=('Calibri (Body)',13,'bold'),fg_color='#2ecc71',
                              text_color='black',height=40,width=100,corner_radius=20,command=errorr)
    
    delete_button=ctk.CTkButton(screen_frame,text='Delete',font=('Calibri (Body)',13,'bold'),fg_color='#c0392b',
                              text_color='white',height=40,width=100,corner_radius=20,command=delete_data)
    
    frame_close_button=ctk.CTkButton(screen_frame,text='Close',font=('Calibri (Body)',13,'bold'),fg_color='#34495e',
                              text_color='white',height=40,width=100,corner_radius=20,command=close_screen_frame)
    frame_close_button.pack(side=RIGHT,anchor='s',pady=25,padx=(15,25))
    delete_button.pack(side=RIGHT,anchor='s',pady=25,padx=15)
    update_button.pack(side=RIGHT,anchor='s',pady=25)
    
    notification_box=ctk.CTkFrame(main_canvas1,width=350,height=100,border_color='#6c3483',border_width=3,
                                  fg_color='#d2b4de',corner_radius=35)
    notification_box.propagate(False) #rely=0.85
    notification_box.place(relx=0.65,rely=1.07,anchor='center')
    
    notification_label=Label(notification_box,text='',font=('Calibri (Body)',11,'bold'),fg='#7d6608',
                bg='#d2b4de')
    notification_label.pack(pady=10)
    
    notification_button=Label(notification_box,text='close',width=10,height=25,bg='#d2b4de',font=('Calibri (Body)',10,'bold'),
                  relief='flat',cursor='hand2')
    notification_button.pack(pady=(0,10))
    notification_button.bind("<ButtonRelease-1>",notification_down)
    


win.mainloop()