import os
import logging
import threading
import time
import google_trans_new as gt

# GUI
import tkinter as tk
from tkinter import END, filedialog
import tkinter.ttk as ttk


root = tk.Tk()
root.title("ClipBoard Translator")

languages_original = gt.constant.LANGUAGES
languages = []

stop_thread = False

# user options
update_time: float = 0.5
input_file_path = "input.txt"
output_file_path = "output.txt"
input_folder_path = ""
output_folder_path = ""


if __name__ == "__main__":
    for l in languages_original.keys():
        languages.append(languages_original[l])

    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")


# Processing

# Input Output


def start_threading():
    x = threading.Thread(target=check_file_changes, daemon=True)
    x.start()


def process_input():
    # Your processing logic goes here
    input_text = input_textbox.get("1.0", "end-1c")  # Get the input text

    translate_text(input_text)


def on_batch_folder_input_clicked(event):
    global input_folder_path
    logging.info("on_batch_folder_input_clicked")
    try:
        batch_folder_input.delete(0, END)
        input_folder_path = filedialog.askdirectory(
            parent=root,
            initialdir="C:\\",
            mustexist=True,
            title="Select your Input Source directory",
        )
        batch_folder_input.insert(0, input_folder_path)
        logging.info(input_folder_path)
    except:
        logging.exception("Folder Exception")
        batch_folder_input.insert(0, "")


def on_batch_folder_output_clicked(event):
    global output_folder_path
    logging.info("on_batch_folder_output_clicked")
    try:
        batch_folder_output.delete(0, END)
        output_folder_path = filedialog.askdirectory(
            initialdir="C:\\",
            mustexist=True,
            title="Select your Output Source directory",
        )
        batch_folder_output.insert(0, output_folder_path)
        logging.info(output_folder_path)
    except:
        logging.exception("Folder Exception")
        batch_folder_output.insert(0, "")


def read_text(input_file=input_file_path) -> str:
    f = open(input_file, "r")
    # print("length of file:",len(f.read()))
    text = f.read()
    logging.info("text in file\n" + text)
    return text


def translate_text(text: str) -> str:
    input_text(text)
    translator = gt.google_translator(url_suffix="com")  #  .Translator()
    translation = ""
    try:
        # Translate the text to the target language
        translation = translator.translate(
            text, lang_tgt=list(languages_original)[dropdown.current()]
        )
        output_text(translation)
        # save_translation(translation)
        logging.info("Thread %s: Finished Translation", 1)
    except Exception as e:
        logging.exception("Translation Error {e}")
    return translation


def clear_output_folder():
    logging.exception("not implemented")
    pass


def batch_translate():
    global input_folder_path
    global output_folder_path
    global stop_thread
    logging.info("FUNC: Batch Translate")
    stop_thread = True
    if not (os.path.exists(input_folder_path) and os.path.exists(output_folder_path)):
        logging.info("Paths don't exist")
        logging.info(input_folder_path)
        logging.info(output_folder_path)
        stop_thread = False
        start_threading()
        return
    try:
        txts = find_txt_files(input_folder_path)
        for t in txts:
            # t = filepath
            save_translation(
                translate_text(read_text(t)),
                os.path.join(output_folder_path, os.path.basename(t)),
            )
    except:
        logging.info("Failure to Batch Translate")
        pass

    stop_thread = False
    start_threading()


def input_text(text):
    input_textbox.delete("1.0", "end")
    input_textbox.insert("1.0", text)


def output_text(text):
    output_textbox.delete("1.0", "end")  # Clear the output textbox
    output_textbox.insert("1.0", text)  # Display processed text


def save_translation(translated_text, file_path_name=output_file_path):
    # trunc's the file to write
    f = open(file_path_name, "w", encoding="utf-8")
    f.write(translated_text)


# daemon thread function
def check_file_changes():
    # Get the initial modification time
    last_modified_time = os.path.getmtime(input_file_path)

    prev_clipboard_contents = ""
    logging.info("Thread %s: starting", 1)

    while True:
        # Sleep for a short interval
        time.sleep(update_time)
        logging.info("Thread %s: checking for changes", 1)
        if stop_thread:
            logging.info("Thread %s: Stopped", 1)
            break
        # Check the current modification time
        current_modified_time = os.path.getmtime(input_file_path)
        try:
            current_clipboard_contents = tk.Tk().clipboard_get()
        except:
            # logging.info("Thread %s: Clipboard get failure", 1)
            current_clipboard_contents = ""

        # Compare with the initial modification time
        if current_modified_time != last_modified_time:
            logging.info("Thread %s: Detected File Change", 1)
            last_modified_time = current_modified_time
            print("new input.txt change: " + read_text())
            save_translation(translated_text=translate_text(read_text()))
            time.sleep(1)
            logging.info("Thread %s: Ready to Translate", 1)
        elif (prev_clipboard_contents != current_clipboard_contents) and (
            len(current_clipboard_contents) >= 1
        ):
            logging.info("Thread %s: Detected Clipboard Change", 1)
            prev_clipboard_contents = current_clipboard_contents

            translate_text(current_clipboard_contents)

            time.sleep(1)
            logging.info("Thread %s: Ready to Translate", 1)


def find_txt_files(folder_path):
    """Returns array of txt file paths in folder"""
    txt_files = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".txt"):
                file_path = os.path.join(root, file)
                txt_files.append(file_path)
    return txt_files


def on_closing():
    open(input_file_path, "w")
    open(output_file_path, "w")

    root.destroy()


# housekeeping
root.title("ClipBoard Translation")
root.protocol("WM_DELETE_WINDOW", on_closing)
# create new file if none exists
open("input.txt", "w")
open("output.txt", "w")

input_label = tk.Label(root, text="Input", justify="left")
input_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")

input_textbox = tk.Text(root, height=5, width=40)
input_textbox.grid(row=0, column=1, padx=10, pady=5, columnspan=2, sticky=tk.W + tk.E)

output_label = tk.Label(root, text="Output", justify="left")
output_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")

output_textbox = tk.Text(root, height=5, width=40)
output_textbox.grid(row=1, column=1, padx=10, pady=5, columnspan=2, sticky=tk.W + tk.E)

process_button = tk.Button(root, text="Process Input", command=process_input)
process_button.grid(row=2, column=0, pady=5)

batch_translate_button = tk.Button(
    root, text="Batch Translate", command=batch_translate
)
batch_translate_button.grid(row=2, column=1, pady=5, padx=5)

clear_output_folder_button = tk.Button(
    root, text="Clear output folder", command=clear_output_folder
)
clear_output_folder_button.grid(row=2, column=2, pady=5)
label = tk.Label(root, text="Language", justify="left")
label.grid(
    row=3, column=0, columnspan=1, pady=10, padx=10, sticky="w"
)  # Add padding to separate the label from other elements

selected_option = tk.StringVar()

# Create the dropdown menu
dropdown = ttk.Combobox(root, textvariable=selected_option, justify="left")
dropdown["values"] = languages
dropdown.set(languages[0])
dropdown.grid(row=3, column=1, columnspan=1, pady=10, padx=10, sticky="w")

folder_label = tk.Label(root, text="Batch \nTranslation", justify="left")
folder_label.grid(row=4, column=0, pady=10, padx=10, sticky="w")

batch_folder_input = tk.Entry(root)
batch_folder_input.insert(0, "set input dir")
batch_folder_input.bind("<Button-1>", func=on_batch_folder_input_clicked)
batch_folder_input.grid(row=4, column=1, pady=10, padx=10, sticky="w")

batch_folder_output = tk.Entry(root)
batch_folder_output.insert(0, "set output dir")
batch_folder_output.bind("<Button-1>", func=on_batch_folder_output_clicked)
batch_folder_output.grid(row=4, column=2, pady=10, padx=10, sticky="w")

# filedialog.askdirectory()

start_threading()

root.mainloop()
