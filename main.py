"""
4. Create task expansion via mouse click
3. Create nested tiles
6. Add ascending and descending buttons and functions to the date_created sort
2. Calculate time left, and integrate time left sort
        calculate, show and save time left when the task is created      -----  completed
        calculate, show and save time left when app is run
        create button to manually refresh the table ( between "Edit Tile" and "Delete Tile") - recalculate time left

####    EDIT TO END TIME
- create option for specific day and time --- completed
- day pre-filled current date. Time empty
- LINE 221

####    Time to completion unneeded
-calculate time left to show in table when task is created
-calculate time left when table is refreshed
-calculate time left when task is edited
-save time left in data file to use for... nothing

5. Add buttons to close the 'edit_task_frame' and 'delete_task_frame'


"""

import customtkinter
from tkinter import messagebox
import pandas as pd
from tkinter import ttk
from datetime import datetime
from datetime import date




def AddTile_Button_Clicked():               #packs the "add_task_frame". Called by the 'new_tile' button
    if edit_task_frame.winfo_manager() == 'pack':       #checks if the 'edit_task_frame' is packed
        edit_task_frame.pack_forget()                   #unpacks it if it is

    #The below section gets the current date and time and displays them to the user
    dt = datetime.now()
    date = dt.strftime("%d/%m/%y")
    time = dt.strftime("%H:%M")
    customtkinter.CTkLabel(add_task_frame, text=date, font=('default', 15, 'normal')).place(x=40, rely=0.5, anchor='w')
    customtkinter.CTkLabel(add_task_frame, text=time, font=('default', 15, 'normal')).place(x=40, rely=0.652, anchor='w')

    add_task_frame.pack(fill='both', side='bottom')



def History_Button_Clicked():                   #creates a top-level window to show completed tasks
    history_tile_win = customtkinter.CTkToplevel()
    history_tile_win.title('Task History')
    history_tile_win.geometry("600x600")
    customtkinter.CTkLabel(history_tile_win, text='History').pack()



def View_Button_Clicked():                  #creates a top-level window for view settings. Called by the 'view' button
    view_file = pd.read_csv("Files/view_data.csv")

    #below section creates a separate window for the the view settings
    view_tile_win = customtkinter.CTkToplevel()
    view_tile_win.title('View Options')
    view_tile_win.geometry("400x200")


    """     left frame for sort functions   """
    left_frame = customtkinter.CTkFrame(view_tile_win)
    left_frame.place(x=0, y=0)
    customtkinter.CTkLabel(left_frame, text='Sort', font=('default', 16, 'bold')).place(relx=0, rely=0)
    global sort_var
    cur_sort = view_file.loc[0, 'sort']                 #gets the current sort setting of data in the dataframe
    sort_var = customtkinter.StringVar(value=cur_sort)  #sets the sort mode to what was gotten from the dataframe
    sort_date = customtkinter.CTkRadioButton(left_frame, text='By Date Created', value='date_created', variable=sort_var, command=Sort_Dataframe)
    sort_date.place(x=0, y=30)
    sort_time = customtkinter.CTkRadioButton(left_frame, text='By Time Left', value='time_left', variable=sort_var, command=Sort_Dataframe)
    sort_time.place(x=0, y=60)
    sort_asc= customtkinter.CTkRadioButton(left_frame, text='Ascending', value='ascending', variable=sort_var, command=Sort_Dataframe)
    sort_asc.place(x=0, y=90)
    sort_desc = customtkinter.CTkRadioButton(left_frame, text='Descending', value='descending', variable=sort_var, command=Sort_Dataframe)
    sort_desc.place(x=0, y=120)

    """     right frame for theme setting"""
    right_frame = customtkinter.CTkFrame(view_tile_win)
    right_frame.place(relx=0.5, rely=0)
    customtkinter.CTkLabel(right_frame, text='Theme', font=('default', 16, 'bold')).place(relx=0, y=0)
    global theme_var
    cur_theme = view_file.loc[0, 'theme']       #gets the current theme in dataframe
    theme_var = customtkinter.StringVar(value=cur_theme)    #sets the theme to what was gotten from the dataframe
    system = customtkinter.CTkRadioButton(right_frame, text='System', command= Theme_Options, value='system', variable=theme_var)
    system.place(x=0, y=30)
    light = customtkinter.CTkRadioButton(right_frame, text='Light', command= Theme_Options, value='light', variable=theme_var)
    light.place(x=0, y=60)
    dark = customtkinter.CTkRadioButton(right_frame, text='Dark', command= Theme_Options, value='dark', variable=theme_var)
    dark.place(x=0, y=90)


def EditTile_Button_Clicked():      #packs the 'edit_task_frame'. Called by the 'edit_tile' button

    if len(table.selection()) == 1:                  # checks if only one item was selected
        if add_task_frame.winfo_manager() == 'pack':    #checks if the 'add_task_frame' is packed
            add_task_frame.pack_forget()                #unpacks it if it is

        #below section clears the data in the boxes(so they will not be packed with pre-entered texts)
        edit_title_entry.delete(0, 'end')
        edit_description_box.delete('0.0', 'end')
        edit_timer_entry_day.delete(0, 'end')

        edit_task_frame.pack(fill='both', side='bottom')

        edit_title_entry.insert(0, table.item(table.selection())['values'][2])
        edit_timer_entry_day.insert(0, table.item(table.selection())['values'][3])
        Edit_Timer_Mode_Command('Day')

        data = pd.read_csv("Files/data.csv")
        # index of selected row = isr
        isr = table.index(table.selection())        #gets the data of the selected tile
        edit_description_box.insert("0.0", data.loc[isr, 'DESCRIPTION'])    #inserts the decription data into the description box
        #print()

    else:   # if not, displays an error message
        messagebox.showerror('Error', "Select one tile to edit.")

def DeleteTile_Button_Clicked():
    if table.selection():
        output = messagebox.askyesno('Delete', "This will delete selected task.\nAre you sure?")
        if output == True:
            del_data = pd.read_csv("Files/data.csv")
            for i in table.selection():
                del_data.drop(index=table.index(i), inplace=True)
            for i in table.selection():
                table.delete(i)

            del_data.to_csv("Files/data.csv", mode='w', index=False)

    else:
        messagebox.showerror('Error', "No tile has been selected.")
    #Delete from file

def Theme_Options():
    new_theme = theme_var.get()
    customtkinter.set_appearance_mode(new_theme)
    open_view = pd.read_csv('Files/view_data.csv')
    open_view.loc[0, 'theme'] = new_theme
    open_view.to_csv("Files/view_data.csv", mode='w', index=False)

def Edit_Save():
    table.item(table.selection(), text="", values=(111, '20/20/2020', edit_title_entry.get(),  edit_timer_entry_day.get()))
    edit_task_frame.pack_forget()

def Save_New_Task():
    dt = datetime.now()
    date = dt.strftime("%d/%m/%y")
    time = dt.strftime("%H:%M")
    add_task_frame.pack_forget()
    timer_mode = timer_mode_var.get()

    if timer_mode == 'Day':
        time_left = int(timer_entry_day.get())*24
        time_left = str(time_left)+":00"
    elif timer_mode == 'Time':
        time_left = timer_entry_time_hour.get()+':'+timer_entry_time_minutes.get()
    elif timer_mode == 'Finish By':
        end_time = time_hour.get() + time_minutes.get() + time_method.get()
        print(end_time)


    table.insert(parent='', index=0, values=(111, date, title_entry.get(), time_left))
    dikt = {'PARENT':'', 'DATE_CREATED':[date], 'TASK':[title_entry.get()],
            'DESCRIPTION':[description_box.get('0.0', 'end-1c')], 'TIME_CREATED':[time],
            'TIMER_MODE':[timer_mode], 'END_TIME':[time_left]}#, 'TIME_TO_COMPLETION':[time_left]
    df = pd.DataFrame(dikt)
    df.to_csv('Files/data.csv', mode='a', index=False, header=False)


def Deselect(event):
    for i in table.selection():
        table.selection_remove(i)

def Timer_Mode_Command(choice):
    #print(f"Timer_Mode_Command   TRIGGERED  {choice}")
    if choice == 'Day':
        timer_entry_time_hour.place_forget()
        timer_entry_time_minutes.place_forget()
        time_hour_label.place_forget()
        time_minutes_label.place_forget()
        timer_entry_day.place(relx=1, y=135, anchor='e')

    elif choice == 'Time':
        timer_entry_day.place_forget()
        time_day.place_forget()
        time_month.place_forget()
        time_year.place_forget()
        time_hour.place_forget()
        time_minutes.place_forget()
        time_method.place_forget()
        colon_label.place_forget()
        time_hour_label.place(relx=0.93, y=135, anchor='e')
        timer_entry_time_hour.place(relx=1, y=135, anchor='e')
        time_minutes_label.place(relx=0.93, y=170, anchor='e')
        timer_entry_time_minutes.place(relx=1, y=170, anchor='e')

    elif choice == 'Finish By':
        timer_entry_time_hour.place_forget()
        timer_entry_time_minutes.place_forget()
        time_hour_label.place_forget()
        time_minutes_label.place_forget()
        timer_entry_day.place_forget()

        time_day.place(relx=0.835, y=135, anchor='e')
        time_month.place(relx=0.915, y=135, anchor='e')
        time_year.place(relx=1, y=135, anchor='e')
        time_hour.place(relx=0.85, y=170, anchor='e')
        colon_label.place(relx=0.86, y=170, anchor='e')
        time_minutes.place(relx=0.92, y=170, anchor='e')
        time_method.place(relx=1, y=170, anchor='e')

        cur_dt = date.today()
        time_year.set(cur_dt.year)
        #####   TIME_DAY, TIME_MONTH. ALL FROM CUR_DT



def Edit_Timer_Mode_Command(choice):
    #print(f"Timer_Mode_Command   TRIGGERED  {choice}")
    if choice == 'Day':
        edit_timer_entry_time_hour.place_forget()
        edit_timer_entry_time_minutes.place_forget()
        edit_time_hour_label.place_forget()
        edit_time_minutes_label.place_forget()
        edit_timer_entry_day.place(relx=1, y=135, anchor='e')

    elif choice == 'Time':
        edit_timer_entry_day.place_forget()
        edit_time_hour_label.place(relx=0.93, y=135, anchor='e')
        edit_timer_entry_time_hour.place(relx=1, y=135, anchor='e')
        edit_time_minutes_label.place(relx=0.93, y=170, anchor='e')
        edit_timer_entry_time_minutes.place(relx=1, y=170, anchor='e')


def Refresh():
    df = pd.read_csv("Files/data.csv")
    #combine date and time created into 1 object, get current datetime
    #subtract from datetime created
    #show new time left, store in data file
    #replace time to completion taken from the dataframe to the time_left variable
    
    for i in range(0, df.shape[0]):
        table.insert(parent='', index=customtkinter.END, values=(i, df.loc[i, 'DATE_CREATED'], df.loc[i, 'TASK'], df.loc[i, 'END_TIME']))
# Remember to handle exceptions (like FileNotFoundError) in case the file doesn’t exist.


def Sort_Dataframe():
    #    date_created, time_left, ascending, descending
    #variable = sort_var
    df = pd.read_csv("Files/data.csv")
    sort_mode = sort_var.get()
    if sort_mode == 'ascending':
        df.sort_values(by='TASK', inplace=True)
    elif sort_mode == 'descending':
        df.sort_values(by='TASK', ascending=False, inplace=True)
    elif sort_mode == 'date_created':
        df['DATE_CREATED'] = pd.to_datetime(df['DATE_CREATED'])
        df.sort_values(by='DATE_CREATED', inplace=True)

    df.to_csv("Files/data.csv", mode='w', index=False)
    for row in table.get_children():
        table.delete(row)
    Refresh()
    view_df = pd.read_csv("Files/view_data.csv")
    view_df.loc[0, 'sort'] = sort_mode
    view_df.to_csv("Files/view_data.csv", mode='w', index=False)


def Refresh_Button_clicked(): # delete all table contents and recalculate all variables(time_left)
    table.delete(table.get_children())



"""     get and set theme to the one in use when the app was last exited"""
view_file = pd.read_csv("Files/view_data.csv")
cur_theme = view_file.loc[0, 'theme']
customtkinter.set_appearance_mode(cur_theme)

win = customtkinter.CTk()
win.title("To-Do List")
win.geometry('800x700')



"""     frame for buttons at the top of the window    ---   'Add Tile', 'History', and 'View' """
upper_menu_frame = customtkinter.CTkFrame(win)
#customtkinter.CTkLabel(menu_frame, text='Menu Frame').pack()
upper_menu = customtkinter.CTk
new_tile = customtkinter.CTkButton(upper_menu_frame, text="Add Tile", command=AddTile_Button_Clicked, font=('default', 15, 'bold'))
new_tile.pack(side='left', expand=1, fill='x')
history = customtkinter.CTkButton(upper_menu_frame, text="History", command=History_Button_Clicked, font=('default', 15, 'bold'))
history.pack(side='left', expand=1, fill='x')
show = customtkinter.StringVar()
#view = customtkinter.CTkOptionMenu(upper_menu_frame, variable=show, values=['Theme', 'View'], command=View_Button_Clicked)
view = customtkinter.CTkButton(upper_menu_frame, text='View', command=View_Button_Clicked, font=('default', 15, 'bold'))
view.pack(side='left', expand=1, fill='x')



"""     middle frame for the treeview widget only"""
middle_frame = customtkinter.CTkFrame(win, fg_color='orange')


"""     creates the table for displaying data   """

table = ttk.Treeview(middle_frame, columns=('Position', 'Date', 'Task', 'Time_Left'), show='headings')
table.heading('Position', text='Id')
table.heading('Date', text='Date Created')
table.heading('Task', text='Task')
table.heading('Time_Left', text='Time Left')

table.column('Position', width=25, stretch=False)
table.column('Date', width=80, stretch=False, anchor='center')
table.column('Task', anchor='center')
table.column('Time_Left', width=80, stretch=False, anchor='center')

ttk_style = ttk.Style()
#ttk_style.configure("Treeview", background='gray', foreground='black', rowheight=25, fieldbackground='white')

table.pack(fill='both', expand=True)


"""     frame to hold the buttons at the bottom of the window   ---   'Edit Tile' and 'Delete Tile' buttons  """
lower_menu_frame = customtkinter.CTkFrame(win)
edit_tile = customtkinter.CTkButton(lower_menu_frame, text="Edit Tile", command=EditTile_Button_Clicked, fg_color='green', font=('default', 15, 'bold'))
edit_tile.pack(side='left', expand=1, fill='x')
refresh_table = customtkinter.CTkButton(lower_menu_frame, text='Refresh', command=Refresh_Button_clicked)
refresh_table.pack(side='left')
delete_tile = customtkinter.CTkButton(lower_menu_frame, text="Delete Tile", command=DeleteTile_Button_Clicked,fg_color='red', font=('default', 15, 'bold'))
delete_tile.pack(side='left', expand=1, fill='x')

global time_left    #variable to hold the exact time left in %H%M. time in days will be converted in %H%M


"""     frame to edit task   ---  pops up when the 'Edit Tile' button is pressed"""

edit_task_frame = customtkinter.CTkFrame(win, height=200)

customtkinter.CTkLabel(edit_task_frame, text="Title:", font=('default', 15, 'bold')).place(relx=0, y=30)
edit_title_entry = customtkinter.CTkEntry(edit_task_frame, width=500)
edit_title_entry.place(relx=0.5, y=30, anchor='n')
customtkinter.CTkLabel(edit_task_frame, text="Description:", font=('default', 15, 'bold')).place(relx=0, y=60)
edit_description_box = customtkinter.CTkTextbox(edit_task_frame, width=400)
edit_description_box.place(relx=0.5, y=60, anchor='n')
edit_task_button = customtkinter.CTkButton(edit_task_frame, text="Edit Task", font=('default', 15, 'bold'), command=Edit_Save)
edit_task_button.place(relx=0.5, rely=0, anchor='n')
customtkinter.CTkLabel(edit_task_frame, text='TIME LEFT   ', font=('default', 15, 'bold')).place(relx=1, y=80, anchor='e')
edit_timer_mode_var = customtkinter.StringVar()
edit_timer_mode = customtkinter.CTkOptionMenu(edit_task_frame, variable=edit_timer_mode_var, values=['Day', 'Time'], width=20, command=Edit_Timer_Mode_Command)
edit_timer_mode.set("Day")
edit_timer_mode.place(relx=1, y=105, anchor='e')

edit_timer_entry_day = customtkinter.CTkEntry(edit_task_frame, width=50)
edit_time_hour_label = customtkinter.CTkLabel(edit_task_frame, text="Hours: ")
edit_timer_entry_time_hour = customtkinter.CTkEntry(edit_task_frame, width=40)
edit_time_minutes_label = customtkinter.CTkLabel(edit_task_frame, text="Minutes: ")
edit_timer_entry_time_minutes = customtkinter.CTkEntry(edit_task_frame, width=40)

customtkinter.CTkLabel(edit_task_frame, text="Date Created", font=('default', 15, 'bold')).place(relx=0, rely=0.5, anchor='w')


edit_task_frame.pack_propagate(False)



"""     frame to add task   ---     pops up when the 'ADD TASK' button is pressed"""
add_task_frame = customtkinter.CTkFrame(win, height=200)
customtkinter.CTkLabel(add_task_frame, text="Title:", font=('default', 15, 'bold')).place(relx=0, y=30)
title_entry = customtkinter.CTkEntry(add_task_frame, width=500)
title_entry.place(relx=0.5, y=30, anchor='n')
customtkinter.CTkLabel(add_task_frame, text="Description:", font=('default', 15, 'bold')).place(relx=0, y=60)
description_box = customtkinter.CTkTextbox(add_task_frame, width=400)
description_box.place(relx=0.5, y=60, anchor='n')
add_task_button = customtkinter.CTkButton(add_task_frame, text="Add Task", font=('default', 15, 'bold'), command=Save_New_Task)
add_task_button.place(relx=0.5, rely=0, anchor='n')
customtkinter.CTkLabel(add_task_frame, text='TIME LEFT   ', font=('default', 15, 'bold')).place(relx=1, y=80, anchor='e')
timer_mode_var = customtkinter.StringVar()
timer_mode = customtkinter.CTkOptionMenu(add_task_frame, variable=timer_mode_var, values=['Day', 'Time', 'Finish By'], width=20, command=Timer_Mode_Command)
timer_mode.set("           ")
timer_mode.place(relx=1, y=105, anchor='e')

timer_entry_day = customtkinter.CTkEntry(add_task_frame, width=50)
time_hour_label = customtkinter.CTkLabel(add_task_frame, text="Hours: ")
timer_entry_time_hour = customtkinter.CTkEntry(add_task_frame, width=40)
time_minutes_label = customtkinter.CTkLabel(add_task_frame, text="Minutes: ")
timer_entry_time_minutes = customtkinter.CTkEntry(add_task_frame, width=40)

days = ['Mon', 'Tue' , 'Wed' , 'Thu' , 'Fri' , 'Sat' , 'Sun']
months = ['Jan' , 'Feb' , 'Mar' , 'Apr' , 'May' , 'Jun' , 'Jul' , 'Aug' , 'Sep' , 'Oct' , 'Nov' , 'Dec']
years = ['2024', '2025', '2026', '2027', '2028', '2029', '2030']
time_hour_strvar = customtkinter.StringVar()
time_day = customtkinter.CTkOptionMenu(add_task_frame, variable=time_hour_strvar, values=days, width=40)
time_month_strvar = customtkinter.StringVar()
time_month = customtkinter.CTkOptionMenu(add_task_frame,  variable=time_month_strvar, values=months, width=40)
time_year_strvar = customtkinter.StringVar()
time_year = customtkinter.CTkOptionMenu(add_task_frame,  variable=time_year_strvar, values=years, width=40)

time_hour = customtkinter.CTkEntry(add_task_frame, width=40)
colon_label = customtkinter.CTkLabel(add_task_frame,text=':')
time_minutes = customtkinter.CTkEntry(add_task_frame, width=40)
am_or_pm = customtkinter.StringVar()
time_method = customtkinter.CTkOptionMenu(add_task_frame, variable=am_or_pm, values=['AM', 'PM'], width=10)
time_method.set('AM')

customtkinter.CTkLabel(add_task_frame, text="Date:", font=('default', 15, 'bold')).place(relx=0, rely=0.5, anchor='w')
customtkinter.CTkLabel(add_task_frame, text="Time:", font=('default', 15, 'bold')).place(relx=0, rely=0.65, anchor='w')

add_task_frame.pack_propagate(False)    # prevent frame from adjusting to widget


upper_menu_frame.pack(fill='x')
middle_frame.pack(fill='both', expand=1)
lower_menu_frame.pack(side='bottom',fill='x')

Refresh()

win.bind("<Escape>", Deselect)  #bind the 'Escape' key to the 'Deselect' fucntion

win.mainloop()