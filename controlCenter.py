import os
import tkinter as tk
from tkinter import messagebox
from log_simulation import simulateLogFile, simulateLogFileCANTRAIN


def onButtonClick():
    selectedOption = dropdownVar.get()
    if selectedOption in paths:
        if selectedOption == "CAN TRAIN AND TEST":
            openSubOptionsWindow()
        else:
            openLogWindow(selectedOption)

def openSubOptionsWindow():
    subOptionsWindow = tk.Toplevel(root)
    subOptionsWindow.title("CAN TRAIN AND TEST")

    subOptions = ["auto1", "auto2", "auto3"]

    subOptionVar = tk.StringVar(subOptionsWindow)
    subOptionVar.set(subOptions[0])

    subOptionDropdown = tk.OptionMenu(subOptionsWindow, subOptionVar, *subOptions)
    subOptionDropdown.pack(pady=10)

    confirmButton = tk.Button(subOptionsWindow, text="confirm", command=lambda: openLogWindow(subOptionVar.get()))
    confirmButton.pack(pady=5)

def openLogWindow(selectedOption):
    newWindow = tk.Toplevel(root)
    newWindow.title("Log file selection")

    path = paths[selectedOption]
    logFiles = [file for file in os.listdir(path) if os.path.isfile(os.path.join(path, file)) and file.endswith('.log')]

    if not logFiles:
        messagebox.showwarning("No Log Files", "No .log files found in the selected directory.")
        newWindow.destroy()
        return

    fileVar = tk.StringVar(newWindow)
    fileVar.set(logFiles[0])

    fileDropdown = tk.OptionMenu(newWindow, fileVar, *logFiles)
    fileDropdown.pack(pady=10)

    showFileButton = tk.Button(newWindow, text="kies log file", command=lambda: showSelectedFile(path, fileVar.get()))
    showFileButton.pack(pady=5)

def showSelectedFile(path, selectedFile):
    newWindow = tk.Toplevel(root)
    newWindow.title(selectedFile)

    canvas = tk.Canvas(newWindow, width= 100, height= 100)
    canvas.create_text(50, 50, text="gekozen file: \n" + selectedFile, fill="black")
    canvas.pack()

    runFileButton = tk.Button(newWindow, text="start simulatie", command=lambda: runSelectedFile(path, selectedFile))
    runFileButton.pack(pady=5)

def runSelectedFile(selectedPath, selectedFile):    
    path = selectedPath
    file = os.path.join(path, selectedFile)
    simulateLogFile(file)


root = tk.Tk()
root.title("CAN control center")

datasets = ["test", "ROAD", "GIDS", "CAN TRAIN AND TEST"]

dropdownVar = tk.StringVar(root)
dropdownVar.set(datasets[0])

dropdown = tk.OptionMenu(root, dropdownVar, *datasets)
dropdown.pack(pady=10)


currentDirectory = os.path.dirname(__file__)
canTrainPath = os.path.join(currentDirectory, "datasets/canTrain")

paths = {
    "test": os.path.join(currentDirectory, "datasets/test"),
    "ROAD": os.path.join(currentDirectory, "datasets/road/ambient"),
    "GIDS": os.path.join(currentDirectory, "datasets/gids"),
    "CAN TRAIN AND TEST": os.path.join(currentDirectory, "datasets/canTrain"),
    "auto1": os.path.join(canTrainPath, "2011-chevrolet-impala"),
    "auto2": os.path.join(canTrainPath, "2011-chevrolet-traverse"),
    "auto3": os.path.join(canTrainPath, "2016-chevrolet-silverado")
    }

button = tk.Button(root, text="kies dataset", command=onButtonClick)
button.pack(pady=5)


root.mainloop()