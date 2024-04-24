import os
import tkinter as tk
from tkinter import messagebox
from log_simulation import chooseECUs

# directory to log files
currentDirectory = os.path.dirname(__file__)
canTrainPath = os.path.join(currentDirectory, "datasets/canTrain")
roadPath = os.path.join(currentDirectory, "datasets/road/ambient/")
paths = {
    "ROAD": roadPath,
    "GIDS": os.path.join(currentDirectory, "datasets/gids"),
    "CAN TRAIN AND TEST": canTrainPath,
    "auto1": os.path.join(canTrainPath, "2011-chevrolet-impala"),
    "auto2": os.path.join(canTrainPath, "2011-chevrolet-traverse"),
    "auto3": os.path.join(canTrainPath, "2016-chevrolet-silverado"),
    "HIGHWAY": os.path.join(roadPath, "highway"),
    "DYNO": os.path.join(roadPath, "dyno")
    }


def onButtonClick():
    selectedOption = dropdownVar.get()
    if selectedOption in paths:
        if selectedOption == "CAN TRAIN AND TEST" or selectedOption == "ROAD":
            openSubOptionsWindow(selectedOption)
        else:
            openLogWindow(selectedOption)


def openSubOptionsWindow(selectedOption):
    subOptionsWindow = tk.Toplevel(root)
    subOptionsWindow.title("Suboptions selection")
    subOptionsWindow.geometry("400x400")

    if selectedOption == "ROAD":
        subOptions = ["HIGHWAY", "DYNO"]
    else:    
        subOptions = ["auto1", "auto2", "auto3"]

    canvas = tk.Canvas(subOptionsWindow, width=400, height=100)
    canvas.create_text(200, 25, text="Choose a sub folder", font="bold", justify="center")
    canvas.pack()

    subOptionVar = tk.StringVar(subOptionsWindow)
    subOptionVar.set(subOptions[0])

    subOptionDropdown = tk.OptionMenu(subOptionsWindow, subOptionVar, *subOptions)
    subOptionDropdown.pack(pady=10)

    confirmButton = tk.Button(subOptionsWindow, text="Choose sub folder", command=lambda: openLogWindow(subOptionVar.get(), selectedOption))
    confirmButton.pack(pady=5)


def openLogWindow(selectedOption, dataset="{selectedOption}"):
    newWindow = tk.Toplevel(root)
    newWindow.title("Log file selection")
    newWindow.geometry("400x400")

    path = paths[selectedOption]   
    logFiles = [file for file in os.listdir(path) if os.path.isfile(os.path.join(path, file)) and file.endswith('.log')]

    if not logFiles:
        messagebox.showwarning("No Log Files", "No .log files found in the selected directory.")
        newWindow.destroy()
        return

    canvas = tk.Canvas(newWindow, width=400, height=100)
    canvas.create_text(200, 25, text="Choose a log file", font="bold", justify="center")
    canvas.pack()

    fileVar = tk.StringVar(newWindow)
    fileVar.set(logFiles[0])

    fileDropdown = tk.OptionMenu(newWindow, fileVar, *logFiles)
    fileDropdown.pack(pady=10)

    showFileButton = tk.Button(newWindow, text="Choose log file", command=lambda: showSelectedFile(path, fileVar.get(), dataset))
    showFileButton.pack(pady=5)


def showSelectedFile(path, selectedFile, dataset):
    newWindow = tk.Toplevel(root)
    newWindow.title("Simulate log file")
    newWindow.geometry("400x400")

    canvas = tk.Canvas(newWindow, width= 400, height= 100)
    canvas.create_text(200, 50, text="Chosen file: \n" + selectedFile, fill="black", justify="center")
    canvas.pack()

    runFileButton = tk.Button(newWindow, text="Start simulation", command=lambda: runSelectedFile(path, selectedFile, dataset))
    runFileButton.pack(pady=5)


def runSelectedFile(selectedPath, selectedFile, dataset):    
    path = selectedPath
    file = os.path.join(path, selectedFile)
    chooseECUs(file, dataset)
        


root = tk.Tk()
root.title("CAN control center")
root.geometry("400x400")

datasets = ["ROAD", "GIDS", "CAN TRAIN AND TEST"]

dropdownVar = tk.StringVar(root)
dropdownVar.set(datasets[0])

canvas = tk.Canvas(root, width=400, height=100)
canvas.create_text(200, 25, text="CAN control center", fill="black", font="bold", justify="center")
canvas.pack()

dropdown = tk.OptionMenu(root, dropdownVar, *datasets)
dropdown.pack(pady=10)

button = tk.Button(root, text="kies dataset", command=onButtonClick)
button.pack(pady=10)

root.mainloop()