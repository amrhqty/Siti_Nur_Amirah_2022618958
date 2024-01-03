import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

def collect_data():
    try:
        Day = int(packs_entry.get())  # Get the input from the entry widget
        if 0 <= Day <= 30:  # Check if days late is within a month
            Charge = 0.50
            Total_charge = Day * Charge

            # Display the calculated result in the output label
            output_label.config(text=f"Day: {Day}, Charge: {Charge}, Total charge: RM{Total_charge}")

            # Assuming you have defined these variables earlier
            Stud_ID = ID_combobox.get()
            Stud_Course = Course_combobox.get()
            Lib_Incharge = Librarian_combobox.get()

            # Check if all fields are filled
            if Stud_ID and Stud_Course and Lib_Incharge:
                # Connect to MySQL database
                mydb = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="",
                    database="notice_payment"
                )

                # Inserting data into the 'id' table
                sql = "INSERT INTO `id` (Stud_ID, Stud_Course, Lib_Incharge, Day_late, Total_charge_RM) VALUES (%s, %s, %s, %s, %s)"
                val = (Stud_ID, Stud_Course, Lib_Incharge, Day, Total_charge)

                try:
                    mycursor = mydb.cursor()
                    mycursor.execute(sql, val)
                    mydb.commit()
                    print("Data inserted successfully!")

                    # Display success message (you can customize this)
                    print(f"Student charged successfully!")

                except mysql.connector.Error as err:
                    print(f"Error: {err}")
                    mydb.rollback()

            else:
                messagebox.showwarning("Incomplete Information", "Please fill in all the required fields.")

        else:
            messagebox.showwarning("Invalid Input", "Days late cannot be more than a month (30 days).")

    except ValueError:
        messagebox.showwarning("Invalid Input", "Please enter a valid number for days late.")

window = tk.Tk()
window.title("Data Entry Form")

# Saving User Info
user_info_frame = tk.LabelFrame(window, text="Notice payment")
user_info_frame.grid(row=0, column=0, padx=30, pady=20)

ID_label = tk.Label(user_info_frame, text="Student's ID")
ID_combobox = ttk.Combobox(user_info_frame, values=['14401', '14402', '14403', '14404', '14405', '11001', '11002', '11003', '11004', '11005'])
ID_label.grid(row=0, column=0)
ID_combobox.grid(row=0, column=1)

Course_label = tk.Label(user_info_frame, text="Course")
Course_combobox = ttk.Combobox(user_info_frame, values=['CDIM144', 'CDCS110'])
Course_label.grid(row=1, column=0)
Course_combobox.grid(row=1, column=1)

Librarian_label = tk.Label(user_info_frame, text="In Charge librarian")
Librarian_combobox = ttk.Combobox(user_info_frame, values=["Mr. Kairul Aming", "Ms. Mira Filzah"])
Librarian_label.grid(row=2, column=0)
Librarian_combobox.grid(row=2, column=1)

# Your Main window
window.title("Notice Payment")

# Page Title
label = tk.Label(window, text='Calculate your Package Price', font=("Times New Romans", 14, "bold"))
label.grid(row=1, column=0, pady=10)

# Trip Type Dropdown (Label)
Day_label = tk.Label(window, text="Day late:")
Day_label.grid(row=2, column=0, pady=(10, 0), columnspan=2)

# Prices List by using textbox
prices_text = tk.Text(window, height=15, width=45)
prices_text.grid(row=9, column=0, pady=10, columnspan=2)
prices_text.insert(tk.END, "This notice is for reminder purpose only.\n\n")
prices_text.insert(tk.END, "Book that has been returned 1 day late will\nbe charged RM0.50 \n\n")
prices_text.configure(state='disabled')

# Trip Type Entry
packs_entry = tk.Entry(window)
packs_entry.grid(row=4, column=0, pady=10, columnspan=2)

# Save Button
save_button = tk.Button(window, text="Calculate", command=collect_data)
save_button.grid(row=5, column=0, pady=10, columnspan=2)

# Output Label & result
label = tk.Label(window, text='Price Package', font=("Times New Romans", 12))
label.grid(row=6, column=0, pady=10, columnspan=2)
output_label = tk.Label(window, text="")
output_label.grid(row=7, column=0, columnspan=2)

window.mainloop()
