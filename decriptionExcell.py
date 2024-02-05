import pandas as pd
from openpyxl import Workbook

def caesar_cipher(text, shift):
    result = ""
    for char in text:
        if char.isalpha():
            ascii_offset = ord('a') if char.islower() else ord('A')
            result += chr((ord(char) - ascii_offset + shift) % 26 + ascii_offset)
        else:
            result += char
    return result

def caesar_decrypt(text, shift):
    return caesar_cipher(text, -shift)

def has_common_words(decrypted_text, common_words):
    words = decrypted_text.lower().split()
    return any(word in common_words for word in words)

def find_best_shift_for_text(encrypted_text, common_words):
    best_shift = 0
    max_common_words = 0
    for shift in range(1, 26):
        decrypted_text = caesar_decrypt(encrypted_text, shift)
        word_count = sum(decrypted_text.lower().count(word) for word in common_words)
        if word_count > max_common_words:
            max_common_words = word_count
            best_shift = shift
    return best_shift

def decrypt_excel_file(input_file_path, output_file_path, common_words):
    encrypted_entries = pd.read_excel(input_file_path)
    decrypted_data = []

    for _, row in encrypted_entries.iterrows():
        best_shift = find_best_shift_for_text(row['Message Body'], common_words)
        decrypted_message = caesar_decrypt(row['Message Body'], best_shift)
        decrypted_data.append({"Date and Time": row['Date and Time'], "Decrypted Message": decrypted_message, "Shift Used": best_shift})

    decrypted_df = pd.DataFrame(decrypted_data)
    decrypted_df.to_excel(output_file_path, index=False)

# List of common English words for basic NLP detection
common_words = [
    'the', 'be', 'to', 'of', 'and', 'a', 'in', 'that', 'have', 'I',
    'it', 'for', 'not', 'on', 'with', 'he', 'as', 'you', 'do', 'at',
    'this', 'but', 'his', 'by', 'from', 'they', 'we', 'say', 'her', 'she',
    'or', 'an', 'will', 'my', 'one', 'all', 'would', 'there', 'their', 'what',
    'so', 'up', 'out', 'if', 'about', 'who', 'get', 'which', 'go', 'me',
    'when', 'make', 'can', 'like', 'time', 'no', 'just', 'him', 'know', 'take',
    'people', 'into', 'year', 'your', 'good', 'some', 'could', 'them', 'see', 'other',
    'than', 'then', 'now', 'look', 'only', 'come', 'its', 'over', 'think', 'also',
    'back', 'after', 'use', 'two', 'how', 'our', 'work', 'first', 'well', 'way',
    'even', 'new', 'want', 'because', 'any', 'these', 'give', 'day', 'most', 'us'
]

# Specify the path to your encrypted Excel file and the output path for the decrypted content
encrypted_db_path = "journal_database_encrypted.xlsx"
decrypted_db_path = "decrypted_journal_database.xlsx"

# Run the decryption process
decrypt_excel_file(encrypted_db_path, decrypted_db_path, common_words)

print(f"Decryption completed. Decrypted messages are saved to {decrypted_db_path}.")
