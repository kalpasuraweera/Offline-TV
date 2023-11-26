import os
import tkinter as tk
from cryptography.fernet import Fernet
from datetime import date, timedelta

today = date.today()


# TODO: Ask how many videos per day
# TODO: save keys in a csv file with folder name or use one key for all
# TODO: check file extension


def handle_encrypt():
    folder_path = ent_folder.get()
    if os.path.exists(folder_path) and os.path.isdir(folder_path):
        files = os.listdir(folder_path)
        key = Fernet.generate_key()
        fernet = Fernet(key)
        with open("file_key.key", 'wb') as file_key:
            file_key.write(key)

        for i in range(len(files)):
            with open(f'{folder_path}\\{files[i]}', 'rb') as file:
                original = file.read()
            encrypted = fernet.encrypt(original)
            new_file_name = (today + timedelta(days=i)).strftime("%Y_%m_%d")
            with open(f'{folder_path}\\{new_file_name}.mp4', 'wb') as encrypted_file:
                encrypted_file.write(encrypted)
                print(f'Encrypted: {folder_path}\\{files[i]}')


def handle_decrypt():
    folder_path = ent_folder.get()
    if os.path.exists(folder_path) and os.path.isdir(folder_path):
        files = os.listdir(folder_path)
        with open("file_key.key", 'rb') as file_key:
            key = file_key.read()
        fernet = Fernet(key)
        for i in range(len(files)):
            today_file_name = today.strftime("%Y_%m_%d")
            if files[i].find(today_file_name) == -1:
                continue
            with open(f'{folder_path}\\{files[i]}', 'rb') as enc_file:
                encrypted = enc_file.read()
            original = fernet.decrypt(encrypted)
            with open(f'{folder_path}\\{files[i]}', 'wb') as decrypted:
                decrypted.write(original)
                print(f'Decrypted: {folder_path}\\{files[i]}')


if __name__ == '__main__':
    window = tk.Tk()
    window.title("Offline TV")

    # Set up frames for better organization
    title_frame = tk.Frame(window, padx=20, pady=20)
    title_frame.pack()

    input_frame = tk.Frame(window, padx=20, pady=10)
    input_frame.pack()

    # Label for title
    lbl_title = tk.Label(title_frame, text="Enter the Folder to Encrypt", font=("Arial", 20))
    lbl_title.pack()

    # Entry for input with label
    lbl_folder = tk.Label(input_frame, text="Folder Path: ")
    lbl_folder.pack(side=tk.LEFT)

    ent_folder = tk.Entry(input_frame, width=40)
    ent_folder.pack(side=tk.LEFT)

    # Button for encryption
    btn_encrypt = tk.Button(window, text="Encrypt", command=handle_encrypt, width=10)
    btn_encrypt.pack(pady=10)

    # Button for decryption
    btn_decrypt = tk.Button(window, text="Decrypt", command=handle_decrypt, width=10)
    btn_decrypt.pack(pady=10)

    window.mainloop()
