import pandas as pd
from datetime import datetime
from tkinter import Tk, Text, Button
import random
from pathlib import Path

def check_create_db(file_path, columns):
    if not Path(file_path).exists():
        df = pd.DataFrame(columns=columns)
        df.to_excel(file_path, index=False)

def add_entry_to_db(file_path, data, columns):
    check_create_db(file_path, columns)
    if Path(file_path).exists():
        df = pd.read_excel(file_path)
    else:
        df = pd.DataFrame(columns=columns)
    new_row = pd.DataFrame([data], columns=columns)
    df = pd.concat([df, new_row], ignore_index=True)
    df.to_excel(file_path, index=False)

# Modified Caesar cipher with random shift
def caesar_cipher(text, shift):
    result = ""
    for char in text:
        if char.isalpha():
            ascii_offset = ord('a') if char.islower() else ord('A')
            shifted = chr((ord(char) - ascii_offset + shift) % 26 + ascii_offset)
            result += shifted
        else:
            result += char
    return result

def submit_action():
    text = text_field.get("1.0", "end-1c")
    shift = random.randint(1, 25)  # Random shift between 1 and 25
    encoded_text = caesar_cipher(text, shift)
    
    # Current timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Add entries to the databases
    plain_db_path = "journal_database_plain.xlsx"
    encrypted_db_path = "journal_database_encrypted.xlsx"
    
    # Data for the plain database (includes shift for reference)
    plain_data = [timestamp, text, shift]
    plain_columns = ['Date and Time', 'Message Body', 'Shift']
    
    # Data for the encrypted database
    encrypted_data = [timestamp, encoded_text]
    encrypted_columns = ['Date and Time', 'Message Body']
    
    add_entry_to_db(plain_db_path, plain_data, plain_columns)
    add_entry_to_db(encrypted_db_path, encrypted_data, encrypted_columns)
    
    # Clear the text field after submission
    text_field.delete("1.0", "end")
    
    print("Entry added successfully!")  # Feedback - Consider replacing with GUI feedback

# GUI Setup
root = Tk()
root.title("Journal Submission")

text_field = Text(root, height=10, width=50)
text_field.pack()

submit_button = Button(root, text="Upload to Journal", command=submit_action)
submit_button.pack()

root.mainloop()
