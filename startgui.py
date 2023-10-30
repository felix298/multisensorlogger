import tkinter as tk
import subprocess
import os
import threading
import concurrent.futures
import psutil

# Function to run a program and update the status label
def run_program(line:str, status_label: tk.Label):
    line = line.removeprefix('"')
    line = line.removesuffix('\n')
    line = line.removesuffix('"')
    process = None
    if line.endswith('.exe'):
        try:
            process = psutil.Popen(line)
            status_label.config(text="Running")
        except subprocess.CalledProcessError as e:
            print(f"Failed to run {line}: {e}")
            status_label.config(text="Error")
    elif line.endswith('.py'):
        try:
            process = psutil.Popen(["cmd.exe", "/c", "start", "python", line])
            status_label.config(text="Running")
        except subprocess.CalledProcessError as e:
            print(f"Failed to run {line}: {e}")
            status_label.config(text="Error")
    elif line.endswith('.lnk'):
        try:
            os.startfile(line)
            status_label.config(text="Running")
        except Exception as e:
            print(f"Failed to run {line}: {e}")
            status_label.config(text="Error")

    # Function to check if the process is still running and update the status label
    def check_process():
        if process and not process.is_running():
            status_label.config(text="Not running")

    # Start a new thread to periodically check the process status
    threading.Thread(target=check_process).start()

# Create a new tkinter window
root = tk.Tk()

# Open the config file and read the lines
with open('config.txt', 'r') as file:
    lines = file.readlines()

# Create a list to store the status labels
status_labels = []

# For each line in the file, add a label, a status label and a button to the window
for i, line in enumerate(lines):
    line = line.strip()
    label = tk.Label(root, text=line.split('\\')[-1].split(".")[0])
    status_label = tk.Label(root, text="Not running")
    button = tk.Button(root, text="Start", command=lambda line=line, label=status_label: threading.Thread(target=run_program, args=(line, label)).start())
    label.grid(row=i, column=0)
    status_label.grid(row=i, column=1)
    button.grid(row=i, column=2)
    status_labels.append(status_label)

# Function to run all programs in parallel
def run_all_programs():
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(run_program, lines, status_labels)

# Add a button to run all programs in parallel
run_all_button = tk.Button(root, text="Run All", command=run_all_programs)
run_all_button.grid(row=len(lines), column=0, columnspan=3)

# Start the tkinter main loop
root.mainloop()
