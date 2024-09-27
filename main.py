

import customtkinter
from tkinter import messagebox
import pandas as pd
from tkinter import ttk
from datetime import *
from PIL import Image
import tkinter as tk



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
    history_df = pd.read_csv('Files/history.csv')

    global history_table
    history_table = ttk.Treeview(history_tile_win, columns=('Position', 'Date', 'Task', 'Time_Left'), show='headings')
    history_table.heading('Position', text='Id')
    history_table.heading('Date', text='Date Added')
    history_table.heading('Task', text='Task')
    history_table.heading('Time_Left', text='Time Left')

    history_table.column('Position', width=25, stretch=False)
    history_table.column('Date', width=80, stretch=False, anchor='center')
    history_table.column('Task', anchor='center')
    history_table.column('Time_Left', width=120, stretch=False, anchor='center')

    history_table.pack(fill='both', expand=True)

    for row in history_table.get_children():
        history_table.delete(row)

    """history_df['TIME_LEFT'] = pd.to_timedelta(history_df['TIME_LEFT'])
    history_df['TIME_LEFT'] = history_df['TIME_LEFT'].apply(lambda x: pd.Timedelta(seconds=int(x.total_seconds())))"""

    history_df.sort_values(by="DATE_ADDED", ascending=False)

    # tag to point out expired tasks
    history_table.tag_configure('negative', background='#DB3B39', foreground='white')
    for i in range(0, history_df.shape[0]):
        full_seconds = history_df.loc[i, 'TIME_LEFT']
        if (full_seconds < 0):
            a = timedelta(seconds=abs(full_seconds))
            history_table.insert(parent='', index=customtkinter.END,
                         values=(i + 1, history_df.loc[i, 'DATE_ADDED'], history_df.loc[i, 'TASK'], a), tags=('negative'))
        else:
            a = timedelta(seconds=abs(full_seconds))
            history_table.insert(parent='', index=customtkinter.END,
                         values=(i + 1, history_df.loc[i, 'DATE_ADDED'], history_df.loc[i, 'TASK'], a))

    history_table.bind("<Double-1>", History_Expand_Task)

def View_Button_Clicked():                  #creates a top-level window for view settings. Called by the 'view' button
    view_file = pd.read_csv("Files/view_data.csv")

    #below section creates a separate window for the the view settings
    view_tile_win = customtkinter.CTkToplevel()
    view_tile_win.title('View Options')
    view_tile_win.geometry("400x300")
    view_tile_win.minsize(width=400, height=300)


    """     left frame for sort functions   """
    left_frame = customtkinter.CTkFrame(view_tile_win)
    left_frame.place(x=0, y=0, relheight=1, relwidth=0.5)
    customtkinter.CTkLabel(left_frame, text='Sort', font=('default', 16, 'bold')).place(relx=0, rely=0)
    global sort_var
    cur_sort = view_file.loc[0, 'sort']                 #gets the current sort setting of data in the dataframe
    sort_var = customtkinter.StringVar(value=cur_sort)  #sets the sort mode to what was gotten from the dataframe

    customtkinter.CTkLabel(left_frame, text="By Date Created", font=('default', 14)).place(x=0, y=30)
    sort_date_old = customtkinter.CTkRadioButton(left_frame, text='Oldest first', value='oldest',variable=sort_var, command=Sort_Dataframe)
    sort_date_old.place(x=10, y=60)
    sort_date_new = customtkinter.CTkRadioButton(left_frame, text='Newest first', value='newest',variable=sort_var, command=Sort_Dataframe)
    sort_date_new.place(x=10, y=90)

    customtkinter.CTkLabel(left_frame, text="By Time Left", font=('default', 14)).place(x=0, y=120)
    sort_time_short = customtkinter.CTkRadioButton(left_frame, text='Shortest time first', value='shortest_time', variable=sort_var, command=Sort_Dataframe)
    sort_time_short.place(x=10, y=150)
    sort_time_long = customtkinter.CTkRadioButton(left_frame, text='Longest time first', value='longest_time', variable=sort_var, command=Sort_Dataframe)
    sort_time_long.place(x=10, y=180)

    customtkinter.CTkLabel(left_frame, text="By Task Name", font=('default', 14)).place(x=0, y=210)
    sort_asc= customtkinter.CTkRadioButton(left_frame, text='A-Z', value='ascending', variable=sort_var, command=Sort_Dataframe)
    sort_asc.place(x=10, y=240)
    sort_desc = customtkinter.CTkRadioButton(left_frame, text='Z-A', value='descending', variable=sort_var, command=Sort_Dataframe)
    sort_desc.place(x=10, y=270)

    """     right frame for theme setting"""
    right_frame = customtkinter.CTkFrame(view_tile_win)
    right_frame.place(relx=0.5, rely=0, relheight=1, relwidth=0.5)
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

        edit_title_entry.delete(0, 'end')
        edit_description_box.delete('0.0', 'end')
        edit_timer_entry_day.delete(0, 'end')

        edit_task_frame.pack(fill='both', side='bottom')

        edit_title_entry.insert(0, table.item(table.selection())['values'][2])

        data = pd.read_csv("Files/data.csv")
        # index of selected row = isr

        global isr
        isr = table.index(table.selection())        #gets the index of the selected tile
        edit_timer_mode.set(data.loc[isr, 'TIMER_MODE'])
        timer_mode_information = data.loc[isr, 'TIMER_MODE']
        Edit_Timer_Mode_Command(timer_mode_information, isr)

        edit_description_box.insert("0.0", data.loc[isr, 'DESCRIPTION'])    #inserts the decription data into the description box
        #update with original end_time - method - information

        deadline = data.loc[isr, 'END_TIME']
        deadline = datetime.strptime(deadline, "%Y-%m-%d %H:%M:%S")
        deadline_str = deadline.strftime('%Y-%m-%d %I:%M %p')
        created_dt = data.loc[isr, 'FULL_DATE']
        created_dt = datetime.strptime(created_dt, "%Y-%m-%d %H:%M:%S")
        created_dt_str = created_dt.strftime('%Y-%m-%d %I:%M %p')
        customtkinter.CTkLabel(edit_task_frame, text=created_dt_str, font=('default', 13)).place(relx=0, rely=0.6, anchor='w')
        customtkinter.CTkLabel(edit_task_frame, text=deadline_str, font=('default', 15)).place(relx=0, rely=0.8, anchor='w')

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

    df = pd.read_csv('Files/data.csv')
    edit_index = table.index(table.selection())

    og_creation_date = df.loc[edit_index, 'FULL_DATE']
    og_creation_date = datetime.strptime(og_creation_date, "%Y-%m-%d %H:%M:%S")
    date_now = datetime.now()

    choice = edit_timer_mode.get()

    if choice == 'Day':
        #make entry longer
        days_given_str = edit_timer_entry_day.get()

        days_given = int(days_given_str)

        in_timedelta = timedelta(days=days_given)

        end_time = og_creation_date + in_timedelta
        end_time = end_time.strftime('%Y-%m-%d %H:%M:%S')
        edit_end_time = pd.to_datetime(end_time, format='%Y-%m-%d %H:%M:%S')
        edit_time_left = edit_end_time - date_now


    elif choice == 'Time':
        hours_given = int(edit_timer_entry_time_hour.get())
        minutes_given = int(edit_timer_entry_time_minutes.get())
        in_timedelta = timedelta(hours=hours_given, minutes=minutes_given)
        end_time = og_creation_date + in_timedelta
        end_time = end_time.strftime('%Y-%m-%d %H:%M:%S')
        edit_end_time = pd.to_datetime(end_time, format='%Y-%m-%d %H:%M:%S')
        edit_time_left = edit_end_time - date_now


    elif choice == 'Finish By':
        str_1 = edit_time_month.get()
        edit_time_month_int = int(datetime.strptime(str_1, '%b').month)
        edit_time_day_int = int(edit_time_day.get())
        edit_time_year_int = int(edit_time_year.get())
        day_to_finish = date(edit_time_year_int, edit_time_month_int, edit_time_day_int)


        edit_time_given = edit_time_hour.get() +':'+ edit_time_minutes.get() +' '+ edit_time_method.get()
        edit_time_given_am_pm = datetime.strptime(edit_time_given, "%I:%M %p")
        edit_time_given_24 = edit_time_given_am_pm.strftime("%H:%M")
        edit_time_given_24 = datetime.strptime(edit_time_given_24, "%H:%M")
        edit_time_given_24 = edit_time_given_24.time()

        end_time = datetime.combine(day_to_finish, edit_time_given_24)
        end_time = end_time.strftime('%Y-%m-%d %H:%M:%S')
        edit_end_time = pd.to_datetime(end_time, format='%Y-%m-%d %H:%M:%S')
        edit_time_left = edit_end_time - date_now

    df.loc[edit_index, 'TASK'] = edit_title_entry.get()
    df.loc[edit_index, 'DESCRIPTION'] = edit_description_box.get('0.0', 'end-1c')
    df.loc[edit_index, 'TIMER_MODE'] = edit_timer_mode.get()
    df.loc[edit_index, 'END_TIME'] = edit_end_time
    df.loc[edit_index, 'TIME_LEFT'] = edit_time_left

    df.to_csv('Files/data.csv', index=False, mode='w', header=True)
    Refresh()

    edit_title_entry.delete('0', 'end')
    edit_description_box.delete('0.0', 'end-1c')
    edit_timer_entry_day.delete('0', 'end')
    edit_timer_entry_time_hour.delete('0', 'end')
    edit_timer_entry_time_minutes.delete('0', 'end')
    edit_time_hour.delete('0', 'end')
    edit_time_minutes.delete('0', 'end')

    edit_task_frame.pack_forget()

def Save_New_Task():
    dt = datetime.now()
    full_date = dt.strftime('%Y-%m-%d %H:%M:%S')
    full_date = pd.to_datetime(full_date, format='%Y-%m-%d %H:%M:%S')
    date_today = dt.strftime("%d-%m-%y")
    #time = dt.strftime("%H:%M")
    add_task_frame.pack_forget()
    timer_mode = timer_mode_var.get()

    if timer_mode == 'Day':
        days_given = int(timer_entry_day.get())
        in_timedelta = timedelta(days=days_given)
        end_time = dt + in_timedelta
        end_time = end_time.strftime('%Y-%m-%d %H:%M:%S')
        end_time = pd.to_datetime(end_time, format='%Y-%m-%d %H:%M:%S')
        time_left = end_time - full_date

        '''time_left = int(timer_entry_day.get())*24
        time_left = str(time_left)+":00"'''
    elif timer_mode == 'Time':
        hours_given = int(timer_entry_time_hour.get())
        minutes_given = int(timer_entry_time_minutes.get())
        in_timedelta = timedelta(hours=hours_given, minutes=minutes_given)
        end_time = dt + in_timedelta
        end_time = end_time.strftime('%Y-%m-%d %H:%M:%S')
        end_time = pd.to_datetime(end_time, format='%Y-%m-%d %H:%M:%S')
        time_left = end_time - full_date

        '''time_left = timer_entry_time_hour.get()+':'+timer_entry_time_minutes.get()'''
    elif timer_mode == 'Finish By':
        str_1 = time_month.get()

        time_month_int = int(datetime.strptime(str_1, '%b').month)
        time_day_int = int(time_day.get())
        time_year_int = int(time_year.get())
        day_to_finish = date(time_year_int, time_month_int, time_day_int)


        time_given = time_hour.get() +':'+ time_minutes.get() +' '+ time_method.get()
        time_given_am_pm = datetime.strptime(time_given, "%I:%M %p")
        time_given_24 = time_given_am_pm.strftime("%H:%M")
        time_given_24 = datetime.strptime(time_given_24, "%H:%M")
        time_given_24 = time_given_24.time()

        end_time = datetime.combine(day_to_finish, time_given_24)
        end_time = end_time.strftime('%Y-%m-%d %H:%M:%S')
        end_time = pd.to_datetime(end_time, format='%Y-%m-%d %H:%M:%S')
        time_left = end_time - full_date


    dikt = {'PARENT':'', 'DATE_CREATED':[date_today], 'TASK':[title_entry.get()],
            'DESCRIPTION':[description_box.get('0.0', 'end-1c')],
            'TIMER_MODE':[timer_mode], 'END_TIME':[end_time], 'FULL_DATE':[full_date], 'TIME_LEFT': [time_left]}
    df = pd.DataFrame(dikt)
    df.to_csv('Files/data.csv', mode='a', index=False, header=False)

    Refresh()

    title_entry.delete('0', 'end')
    description_box.delete('0.0', 'end-1c')
    timer_entry_day.delete('0', 'end')
    timer_entry_time_hour.delete('0', 'end')
    timer_entry_time_minutes.delete('0', 'end')
    time_hour.delete('0', 'end')
    time_minutes.delete('0', 'end')


def Deselect(event):
    for i in table.selection():
        table.selection_remove(i)

def Timer_Mode_Command(choice):
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
        time_month_words = months[cur_dt.month - 1]
        time_day.set(cur_dt.day)
        time_month.set(time_month_words)
        #####   TIME_DAY, TIME_MONTH. ALL FROM CUR_DT



def Edit_Timer_Mode_Command(choice, row_id):
    df = pd.read_csv('Files/data.csv')
    creation_date = df.loc[row_id, 'FULL_DATE']
    #creation_date.to_datetime("%Y-%m-%d %H:%M:%S")
    creation_date = datetime.strptime(creation_date, "%Y-%m-%d %H:%M:%S")
    deadline_date = df.loc[row_id, 'END_TIME']
    #deadline_date.to_datetime("%Y-%m-%d %H:%M:%S")
    deadline_date = datetime.strptime(deadline_date, "%Y-%m-%d %H:%M:%S")


    if choice == 'Day':
        edit_timer_entry_time_hour.place_forget()
        edit_timer_entry_time_minutes.place_forget()
        edit_time_hour_label.place_forget()
        edit_time_minutes_label.place_forget()

        edit_time_day.place_forget()
        edit_time_month.place_forget()
        edit_time_year.place_forget()
        edit_time_hour.place_forget()
        edit_colon_label.place_forget()
        edit_time_minutes.place_forget()
        edit_time_method.place_forget()

        edit_timer_entry_day.place(relx=1, y=135, anchor='e')

        edit_timer_entry_day.delete('0', 'end')

        og_day = deadline_date - creation_date
        og_day = str(og_day)
        og_day = int(og_day.split(' day')[0].split(' days')[0])
        edit_timer_entry_day.insert(0, og_day)

        #inserting with time part "0:00:00" + 'days'


    elif choice == 'Time':
        edit_timer_entry_day.place_forget()

        edit_time_day.place_forget()
        edit_time_month.place_forget()
        edit_time_year.place_forget()
        edit_time_hour.place_forget()
        edit_colon_label.place_forget()
        edit_time_minutes.place_forget()
        edit_time_method.place_forget()

        edit_time_hour_label.place(relx=0.93, y=135, anchor='e')
        edit_timer_entry_time_hour.place(relx=1, y=135, anchor='e')
        edit_time_minutes_label.place(relx=0.93, y=170, anchor='e')
        edit_timer_entry_time_minutes.place(relx=1, y=170, anchor='e')

        edit_timer_entry_time_hour.delete('0', 'end')
        edit_timer_entry_time_minutes.delete('0', 'end')


        #CONVERT TO SECONDS, THEN RECALCULATE HOURS AD MINUTES

        og_full_time = deadline_date - creation_date
        in_seconds = og_full_time.total_seconds()
        og_hours = in_seconds // 3600  # 1 hour = 3600 seconds
        og_minutes = (in_seconds % 3600) // 60  # Remaining seconds converted to minutes

        edit_timer_entry_time_hour.insert(0, int(og_hours))
        edit_timer_entry_time_minutes.insert(0, int(og_minutes))

        # INSERTING WITH DECIMALS
        # STACKING

    elif choice == 'Finish By':
        edit_timer_entry_time_hour.place_forget()
        edit_timer_entry_time_minutes.place_forget()
        edit_time_hour_label.place_forget()
        edit_time_minutes_label.place_forget()
        edit_timer_entry_day.place_forget()

        edit_time_day.place(relx=0.835, y=135, anchor='e')
        edit_time_month.place(relx=0.915, y=135, anchor='e')
        edit_time_year.place(relx=1, y=135, anchor='e')
        edit_time_hour.place(relx=0.85, y=170, anchor='e')
        edit_colon_label.place(relx=0.86, y=170, anchor='e')
        edit_time_minutes.place(relx=0.92, y=170, anchor='e')
        edit_time_method.place(relx=1, y=170, anchor='e')


        edit_time_hour.delete('0', 'end')
        edit_time_minutes.delete('0', 'end')

        edit_time_year.set(str(deadline_date.year))
        edit_time_month_words = months[deadline_date.month - 1]
        edit_time_day.set(str(deadline_date.day))
        edit_time_month.set(edit_time_month_words)
        #deadline_date_time = deadline_date.strftime("%I:%M %p")
        edit_time_hour.insert(0, deadline_date.strftime('%I'))
        edit_time_minutes.insert(0, deadline_date.strftime('%M'))
        edit_time_method.set(deadline_date.strftime('%p'))

        #DEADLINE_DATE

        #####   TIME_DAY, TIME_MONTH. ALL FROM CUR_DT

def Refresh():
    df = pd.read_csv("Files/data.csv")
    for i in range(0, df.shape[0]):
        date_now = datetime.now()
        date_now.strftime('%Y-%m-%d %H:%M:%S')
        date_now = pd.to_datetime(date_now, format='%Y-%m-%d %H:%M:%S')
        end_time = df.loc[i, 'END_TIME']
        end_time = pd.to_datetime(end_time, format='%Y-%m-%d %H:%M:%S')
        time_left = end_time - date_now
        df.loc[i, 'TIME_LEFT'] = time_left
    #df['TIME_LEFT'] = pd.to_timedelta(df['TIME_LEFT'])
    df['TIME_LEFT'] = df['TIME_LEFT'].apply(lambda x: pd.Timedelta(seconds=int(x.total_seconds())))   #lambda x: pd.Timedelta(seconds=int(x.total_seconds()))
    #df.sort_values(by='TIME_LEFT', inplace=True)


    for row in table.get_children():
        table.delete(row)

    #tag to point out expired tasks
    table.tag_configure('negative', background='#DB3B39', foreground='white')
    for i in range(0, df.shape[0]):
            if (df.loc[i, 'TIME_LEFT'] < timedelta(0)):
                df.loc[i, 'TIME_LEFT'] = pd.Timedelta(seconds=int(abs(df.loc[i, 'TIME_LEFT'].total_seconds())))
                table.insert(parent='', index=customtkinter.END, values=(i+1, df.loc[i, 'DATE_CREATED'], df.loc[i, 'TASK'], "EXPIRED"), tags=('negative'))
            else:
                table.insert(parent='', index=customtkinter.END, values=(i+1, df.loc[i, 'DATE_CREATED'], df.loc[i, 'TASK'], df.loc[i, 'TIME_LEFT']))
    # Remember to handle exceptions (like FileNotFoundError) in case the file doesn’t exist.
    df.to_csv('Files/data.csv', mode='w', index=False)



def Sort_Dataframe():
    #    date_created, time_left, ascending, descending
    #variable = sort_var
    df = pd.read_csv("Files/data.csv")
    sort_mode = sort_var.get()
    if sort_mode == 'ascending':
        df.sort_values(by='TASK', inplace=True)
    elif sort_mode == 'descending':
        df.sort_values(by='TASK', ascending=False, inplace=True)
    elif sort_mode == 'oldest':
        df['FULL_DATE'] = pd.to_datetime(df['FULL_DATE'], format='%Y-%m-%d %H:%M:%S')
        df.sort_values(by='FULL_DATE', inplace=True)
    elif sort_mode == 'newest':
        df['FULL_DATE'] = pd.to_datetime(df['FULL_DATE'], format='%Y-%m-%d %H:%M:%S')
        df.sort_values(by='FULL_DATE', inplace=True, ascending=False)
    elif sort_mode == 'longest_time':
        for i in range(0,df.shape[0]):
            full_date = df.loc[i,'FULL_DATE']
            full_date = pd.to_datetime(full_date, format='%Y-%m-%d %H:%M:%S')
            end_time = df.loc[i,'END_TIME']
            end_time = pd.to_datetime(end_time, format='%Y-%m-%d %H:%M:%S')
            time_left = end_time - full_date
            df.loc[i, 'TIME_LEFT'] = time_left
        df['TIME_LEFT'] = pd.to_timedelta(df['TIME_LEFT'])
        df.sort_values(by='TIME_LEFT', inplace=True, ascending=False)
    elif sort_mode == 'shortest_time':
        for i in range(0,df.shape[0]):
            full_date = df.loc[i,'FULL_DATE']
            full_date = pd.to_datetime(full_date, format='%Y-%m-%d %H:%M:%S')
            end_time = df.loc[i,'END_TIME']
            end_time = pd.to_datetime(end_time, format='%Y-%m-%d %H:%M:%S')
            time_left = end_time - full_date
            df.loc[i, 'TIME_LEFT'] = time_left
        df['TIME_LEFT'] = pd.to_timedelta(df['TIME_LEFT'])
        df.sort_values(by='TIME_LEFT', inplace=True, ascending=True)



    df.to_csv("Files/data.csv", mode='w', index=False)

    Refresh()
    view_df = pd.read_csv("Files/view_data.csv")
    view_df.loc[0, 'sort'] = sort_mode
    view_df.to_csv("Files/view_data.csv", mode='w', index=False)



def close_task_frame():
    if (edit_task_frame.winfo_manager() == 'pack'):
        edit_task_frame.pack_forget()
    elif(add_task_frame.winfo_manager() == 'pack'):
        add_task_frame.pack_forget()



#previous_item = None
def main_context_menu(event):
    context_item = table.identify_row(event.y)

    table.selection_set(context_item)

    context_menu.post(event.x_root, event.y_root)
    global treeview_row_id
    treeview_row_id = context_item




def Task_Completed():
    id_of_selected = table.index(treeview_row_id)

    if not isinstance(id_of_selected, list):
        id_of_selected = [id_of_selected]

    df = pd.read_csv('Files/data.csv')
    selected_row = df.iloc[id_of_selected].copy()

    selected_row.drop(columns=['TIMER_MODE'], inplace=True)
    selected_row.drop(columns=['DATE_CREATED'], inplace=True)

    selected_row['STATUS'] = 'COMPLETED'
    date_added = datetime.now()
    date_added = date_added.replace(microsecond=0)
    selected_row['DATE_ADDED'] = date_added
    selected_row['END_TIME'] = pd.to_datetime(selected_row['END_TIME'])
    selected_row['FULL_DATE'] = pd.to_datetime(selected_row['FULL_DATE'])
    time_left = selected_row['END_TIME'] - date_added
    selected_row['TIME_LEFT'] = time_left.dt.total_seconds()
    selected_row.to_csv('Files/history.csv', mode='a', index=False, header=False)

    df.drop(index=id_of_selected, inplace=True)
    df.to_csv('Files/data.csv', mode='w', index=False, header=True)
    Refresh()


def Renew_Task():
    renew_box = messagebox.askyesno("Renew Task", "Do you want to renew the task?")

    if renew_box:
        date_now = datetime.now()
        date_now = date_now.replace(microsecond=0)
        id_of_selected = table.index(treeview_row_id)

        #Take original date, and end time, find the time in between
        #add that difference to current day
        #changing original date, and end time
        df = pd.read_csv('Files/data.csv')

        org_creation_date = df.loc[id_of_selected, 'FULL_DATE']
        org_creation_date = datetime.strptime(org_creation_date, "%Y-%m-%d %H:%M:%S")
        org_end_time = df.loc[id_of_selected, 'END_TIME']
        org_end_time = datetime.strptime(org_end_time, "%Y-%m-%d %H:%M:%S")
        org_time_difference = org_end_time - org_creation_date
        new_end_datetime = date_now + org_time_difference
        new_end_datetime = new_end_datetime.strftime("%Y-%m-%d %H:%M:%S")
        new_creation_date = date_now.strftime("%d-%m-%y")


        df.loc[id_of_selected, 'DATE_CREATED'] = new_creation_date
        df.loc[id_of_selected, 'FULL_DATE'] = date_now
        df.loc[id_of_selected, 'END_TIME'] = new_end_datetime

        df.to_csv('Files/data.csv', mode='w', index=False, header=True)

        Refresh()



def Expired_Task():
    id_of_selected = table.index(treeview_row_id)

    if not isinstance(id_of_selected, list):
        id_of_selected = [id_of_selected]

    date_added = datetime.now()
    date_added = date_added.replace(microsecond=0)

    df = pd.read_csv('Files/data.csv')
    selected_row = df.iloc[id_of_selected].copy()

    selected_row.drop(columns=['TIMER_MODE'], inplace=True)
    selected_row.drop(columns=['DATE_CREATED'], inplace=True)

    selected_row['STATUS'] = 'EXPIRED'
    date_added = date_added.replace(microsecond=0)
    selected_row['DATE_ADDED'] = date_added
    selected_row['END_TIME'] = pd.to_datetime(selected_row['END_TIME'])
    selected_row['FULL_DATE'] = pd.to_datetime(selected_row['FULL_DATE'])
    time_left = selected_row['END_TIME'] - date_added
    selected_row['TIME_LEFT'] = time_left.dt.total_seconds()

    selected_row.to_csv('Files/history.csv', mode='a', index=False, header=False)
    df.drop(index=id_of_selected, inplace=True)
    df.to_csv('Files/data.csv', mode='w', index=False, header=True)
    Refresh()

def Expand_Task(event):
    expanded = customtkinter.CTkToplevel()
    expanded.title("Expanded Task")
    expanded.minsize(width=500, height=400)
    df = pd.read_csv('Files/data.csv')

    sel = table.index(table.selection())
    full_sel = df.iloc[sel]


    customtkinter.CTkLabel(expanded, text=f"TITLE: {full_sel['TASK']}", font=('default', 15, 'bold')).place(relx=0.5, rely=0, anchor='n')
    customtkinter.CTkLabel(expanded, text=f"CREATED ON: {full_sel['FULL_DATE']}", font=('default', 15, 'bold')).place(relx=0, rely=0.2, anchor='w')
    customtkinter.CTkLabel(expanded, text=f"END BY: {full_sel['END_TIME']}", font=('default', 15, 'bold')).place(relx=1, rely=0.2, anchor='e')
    customtkinter.CTkLabel(expanded, text=f"TIME LEFT: {full_sel['TIME_LEFT']}", font=('default', 15, 'bold')).place(relx=0.5, rely=0.4, anchor='n')
    customtkinter.CTkLabel(expanded, text='DESCRIPTION', font=('default', 20, 'bold')).place(relx=0.5, rely=0.5, anchor='n')
    customtkinter.CTkLabel(expanded, text=full_sel['DESCRIPTION'], font=('default', 15, 'bold')).place(relx=0.5, rely=0.6, anchor='n')



def History_Expand_Task(event):
    history_expanded = customtkinter.CTkToplevel()
    history_expanded.title("History Task Expanded")
    history_expanded.minsize(width=500, height=400)
    history_df = pd.read_csv('Files/history.csv')

    sel = history_table.index(history_table.selection())
    full_sel = history_df.iloc[sel]

    d_time = full_sel['TIME_LEFT']
    if d_time < 0:
        time_left = str(timedelta(seconds=abs(d_time)))
        time_left = '-'+time_left
    else:
        time_left = str(timedelta(seconds=d_time))

    customtkinter.CTkLabel(history_expanded, text=f"TITLE: {full_sel['TASK']}", font=('default', 15, 'bold')).place(relx=0.5, rely=0, anchor='n')
    customtkinter.CTkLabel(history_expanded, text=f"CREATED ON: {full_sel['FULL_DATE']}", font=('default', 15, 'bold')).place(relx=0, rely=0.2, anchor='w')
    customtkinter.CTkLabel(history_expanded, text=f"END BY: {full_sel['END_TIME']}", font=('default', 15, 'bold')).place(relx=1, rely=0.2, anchor='e')
    customtkinter.CTkLabel(history_expanded, text=f"TIME LEFT BEFORE ADDITION: {time_left}", font=('default', 15, 'bold')).place(relx=0.5, rely=0.4, anchor='n')
    customtkinter.CTkLabel(history_expanded, text='DESCRIPTION', font=('default', 20, 'bold')).place(relx=0.5, rely=0.5, anchor='n')
    customtkinter.CTkLabel(history_expanded, text=full_sel['DESCRIPTION'], font=('default', 15, 'bold')).place(relx=0.5, rely=0.6, anchor='n')




"""     get and set theme to the one in use when the app was last exited"""
view_file = pd.read_csv("Files/view_data.csv")
cur_theme = view_file.loc[0, 'theme']
customtkinter.set_appearance_mode(cur_theme)

win = customtkinter.CTk()
win.title("To-Do List")
win.geometry('800x600')



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
table.column('Time_Left', width=120, stretch=False, anchor='center')


table.pack(fill='both', expand=True)


"""         CONTEXT MENU        """
context_menu = tk.Menu(win, tearoff=0)
context_menu.add_command(label='Completed', command=Task_Completed)
context_menu.add_command(label='Renew', command=Renew_Task)
context_menu.add_command(label='Expired', command=Expired_Task)

win.bind("<Button-3>", main_context_menu) #context menu for main window

#get selections ... apply function


"""     frame to hold the buttons at the bottom of the window   ---   'Edit Tile' and 'Delete Tile' buttons  """
lower_menu_frame = customtkinter.CTkFrame(win)
edit_tile = customtkinter.CTkButton(lower_menu_frame, text="Edit Tile", command=EditTile_Button_Clicked, fg_color='green', font=('default', 15, 'bold'))
edit_tile.pack(side='left', expand=1, fill='x')
refresh_table = customtkinter.CTkButton(lower_menu_frame, text='Refresh', command=Refresh)
refresh_table.pack(side='left')
delete_tile = customtkinter.CTkButton(lower_menu_frame, text="Delete Tile", command=DeleteTile_Button_Clicked,fg_color='red', font=('default', 15, 'bold'))
delete_tile.pack(side='left', expand=1, fill='x')

#global time_left    #variable to hold the exact time left in %H%M. time in days will be converted in %H%M



exit_image = customtkinter.CTkImage(light_image=Image.open("Files/exit_image.png"),dark_image=Image.open("Files/exit_image.png"),size=(30, 30))


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
customtkinter.CTkLabel(edit_task_frame, text='UPDATE TIME   ', font=('default', 15, 'bold')).place(relx=1, y=80, anchor='e')
edit_timer_mode_var = customtkinter.StringVar()
edit_timer_mode = customtkinter.CTkOptionMenu(edit_task_frame, variable=edit_timer_mode_var, values=['Day', 'Time', 'Finish By'], width=20, command=lambda choice:Edit_Timer_Mode_Command(choice, isr))
edit_timer_mode.place(relx=1, y=105, anchor='e')

#The below are for Edit's "TIME LEFT: " time mode
edit_timer_entry_day = customtkinter.CTkEntry(edit_task_frame, width=50)
edit_time_hour_label = customtkinter.CTkLabel(edit_task_frame, text="Hours: ")
edit_timer_entry_time_hour = customtkinter.CTkEntry(edit_task_frame, width=40)
edit_time_minutes_label = customtkinter.CTkLabel(edit_task_frame, text="Minutes: ")
edit_timer_entry_time_minutes = customtkinter.CTkEntry(edit_task_frame, width=40)

#The below are for Edit's "FINISH BY: " DATE mode
edit_days = ['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30','31']
edit_months = ['Jan' , 'Feb' , 'Mar' , 'Apr' , 'May' , 'Jun' , 'Jul' , 'Aug' , 'Sep' , 'Oct' , 'Nov' , 'Dec']
edit_years = ['2024', '2025', '2026', '2027', '2028', '2029', '2030']
edit_time_day_strvar = customtkinter.StringVar()
edit_time_day = customtkinter.CTkOptionMenu(edit_task_frame, variable=edit_time_day_strvar, values=edit_days, width=30)
edit_time_month_strvar = customtkinter.StringVar()
edit_time_month = customtkinter.CTkOptionMenu(edit_task_frame,  variable=edit_time_month_strvar, values=edit_months, width=40)
edit_time_year_strvar = customtkinter.StringVar()
edit_time_year = customtkinter.CTkOptionMenu(edit_task_frame,  variable=edit_time_year_strvar, values=edit_years, width=40)

#The below are for Edit's "FINISH BY: " time mode
edit_time_hour = customtkinter.CTkEntry(edit_task_frame, width=40)
edit_colon_label = customtkinter.CTkLabel(edit_task_frame,text=':')
edit_time_minutes = customtkinter.CTkEntry(edit_task_frame, width=40)
edit_am_or_pm = customtkinter.StringVar()
edit_time_method = customtkinter.CTkOptionMenu(edit_task_frame, variable=edit_am_or_pm, values=['AM', 'PM'], width=10)
#edit_time_method.set('AM')


edit_close = customtkinter.CTkButton(edit_task_frame, text='', image=exit_image, width=0, height=0,
                                     fg_color='transparent', command=close_task_frame)
edit_close.place(relx=1, rely=0, anchor='ne')

customtkinter.CTkLabel(edit_task_frame, text="Deadline:", font=('default', 15, 'bold')).place(relx=0, rely=0.7, anchor='w')
customtkinter.CTkLabel(edit_task_frame, text="Created:", font=('default', 15, 'bold')).place(relx=0, rely=0.5, anchor='w')


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


days = ['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30','31']
months = ['Jan' , 'Feb' , 'Mar' , 'Apr' , 'May' , 'Jun' , 'Jul' , 'Aug' , 'Sep' , 'Oct' , 'Nov' , 'Dec']
years = ['2024', '2025', '2026', '2027', '2028', '2029', '2030']
time_day_strvar = customtkinter.StringVar()
time_day = customtkinter.CTkOptionMenu(add_task_frame, variable=time_day_strvar, values=days, width=30)
time_month_strvar = customtkinter.StringVar()
time_month = customtkinter.CTkOptionMenu(add_task_frame,  variable=time_month_strvar, values=months, width=40)
time_year_strvar = customtkinter.StringVar()
time_year = customtkinter.CTkOptionMenu(add_task_frame,  variable=time_year_strvar, values=years, width=40)

time_hour = customtkinter.CTkEntry(add_task_frame, width=40)
colon_label = customtkinter.CTkLabel(add_task_frame,text=':')
time_minutes = customtkinter.CTkEntry(add_task_frame, width=40)
am_or_pm = customtkinter.StringVar()
time_method = customtkinter.CTkOptionMenu(add_task_frame, variable=am_or_pm, values=['AM', 'PM'], width=10)


add_close = customtkinter.CTkButton(add_task_frame, text='', image=exit_image, width=0,
                                    height=0, fg_color='transparent', command=close_task_frame)
add_close.place(relx=1, rely=0, anchor='ne')

customtkinter.CTkLabel(add_task_frame, text="Date:", font=('default', 15, 'bold')).place(relx=0, rely=0.5, anchor='w')
customtkinter.CTkLabel(add_task_frame, text="Time:", font=('default', 15, 'bold')).place(relx=0, rely=0.65, anchor='w')

add_task_frame.pack_propagate(False)    # prevent frame from adjusting to widget






upper_menu_frame.pack(fill='x')
middle_frame.pack(fill='both', expand=1)
lower_menu_frame.pack(side='bottom',fill='x')

Refresh()

win.bind("<Escape>", Deselect)
table.bind("<Double-1>", Expand_Task)


win.mainloop()
