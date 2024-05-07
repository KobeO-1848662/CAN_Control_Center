import os
import tkinter as tk
from tkinter import messagebox
from log_simulation import chooseECUs

currentDirectory = os.path.dirname(__file__)
canTrainPath = os.path.join(currentDirectory, "datasets/canTrain")
roadPath = os.path.join(currentDirectory, "datasets/road")

paths = {
    "ROAD": roadPath,
    "HIGHWAY": os.path.join(roadPath, "attackFree/highway"),
    "DYNO": os.path.join(roadPath, "attackFree/dyno"),
    "ROADattack": os.path.join(roadPath, "attacks"),

    "GIDS": os.path.join(currentDirectory, "datasets/gids/attackFree"),
    "GIDS attacks": os.path.join(currentDirectory, "datasets/gids/attacks"),
    
    "CAN TRAIN AND TEST": canTrainPath,
    "CAR 1": os.path.join(canTrainPath, "attackFree/2011-chevrolet-impala"),
    "CAR 2": os.path.join(canTrainPath, "attackFree/2011-chevrolet-traverse"),
    "CAR 3": os.path.join(canTrainPath, "attackFree/2016-chevrolet-silverado"),
    
    "CAR 1 attacks": os.path.join(canTrainPath, "attacks/2011-chevrolet-impala"),
    "combined-attacks1": os.path.join(canTrainPath, "attacks/2011-chevrolet-impala/combined-attacks"),
    "DoS-attacks1": os.path.join(canTrainPath, "attacks/2011-chevrolet-impala/DoS-attacks"),
    "fuzzing-attacks1": os.path.join(canTrainPath, "attacks/2011-chevrolet-impala/fuzzing-attacks"),
    "gear-attacks1": os.path.join(canTrainPath, "attacks/2011-chevrolet-impala/gear-attacks"),
    "interval-attacks1": os.path.join(canTrainPath, "attacks/2011-chevrolet-impala/interval-attacks"),
    "rpm-attacks1": os.path.join(canTrainPath, "attacks/2011-chevrolet-impala/rpm-attacks"),
    "speed-attacks1": os.path.join(canTrainPath, "attacks/2011-chevrolet-impala/speed-attacks"),
    "standstill-attacks1": os.path.join(canTrainPath, "attacks/2011-chevrolet-impala/standstill-attacks"),
    "systematic-attacks1": os.path.join(canTrainPath, "attacks/2011-chevrolet-impala/systematic-attacks"),
    
    "CAR 2 attacks": os.path.join(canTrainPath, "attacks/2011-chevrolet-traverse"),
    "combined-attacks2": os.path.join(canTrainPath, "attacks/2011-chevrolet-traverse/combined-attacks"),
    "DoS-attacks2": os.path.join(canTrainPath, "attacks/2011-chevrolet-traverse/DoS-attacks"),
    "fuzzing-attacks2": os.path.join(canTrainPath, "attacks/2011-chevrolet-traverse/fuzzing-attacks"),
    "gear-attacks2": os.path.join(canTrainPath, "attacks/2011-chevrolet-traverse/gear-attacks"),
    "interval-attacks2": os.path.join(canTrainPath, "attacks/2011-chevrolet-traverse/interval-attacks"),
    "rpm-attacks2": os.path.join(canTrainPath, "attacks/2011-chevrolet-traverse/rpm-attacks"),
    "speed-attacks2": os.path.join(canTrainPath, "attacks/2011-chevrolet-traverse/speed-attacks"),
    "standstill-attacks2": os.path.join(canTrainPath, "attacks/2011-chevrolet-traverse/standstill-attacks"),
    "systematic-attacks2": os.path.join(canTrainPath, "attacks/2011-chevrolet-traverse/systematic-attacks"),
    
    "CAR 3 attacks": os.path.join(canTrainPath, "attacks/2016-chevrolet-silverado"),
    "combined-attacks3": os.path.join(canTrainPath, "attacks/2016-chevrolet-silverado/combined-attacks"),
    "DoS-attacks3": os.path.join(canTrainPath, "attacks/2016-chevrolet-silverado/DoS-attacks"),
    "fuzzing-attacks3": os.path.join(canTrainPath, "attacks/2016-chevrolet-silverado/fuzzing-attacks"),
    "gear-attacks3": os.path.join(canTrainPath, "attacks/2016-chevrolet-silverado/gear-attacks"),
    "interval-attacks3": os.path.join(canTrainPath, "attacks/2016-chevrolet-silverado/interval-attacks"),
    "rpm-attacks3": os.path.join(canTrainPath, "attacks/2016-chevrolet-silverado/rpm-attacks"),
    "speed-attacks3": os.path.join(canTrainPath, "attacks/2016-chevrolet-silverado/speed-attacks"),
    "standstill-attacks3": os.path.join(canTrainPath, "attacks/2016-chevrolet-silverado/standstill-attacks"),
    "systematic-attacks3": os.path.join(canTrainPath, "attacks/2016-chevrolet-silverado/systematic-attacks"),
 
    }


def onButtonClick():
    selectedOption = dropdownVar.get()
    if selectedOption in paths:
        if selectedOption == "CAN TRAIN AND TEST":
            if attack_var.get() == True:
                openSubOptionsWindow(selectedOption, selectedOption, attack=True)
            else:    
                openSubOptionsWindow(selectedOption, selectedOption, attack=False)
        elif selectedOption == "ROAD":
            if attack_var.get() == True:
                openLogWindow(selectedOption="ROADattack", dataset="ROAD", subDataset=None)
            else:
                openSubOptionsWindow(selectedOption, selectedOption, attack=False)
        else:
            if attack_var.get() == True:
                openLogWindow(selectedOption="GIDS attacks", dataset="GIDS", subDataset=None)
            else:
                openLogWindow(selectedOption, selectedOption, subDataset=None)


def openSubOptionsWindow(selectedOption, dataset, attack):
    subOptionsWindow = tk.Toplevel(root)
    subOptionsWindow.title("Suboptions selection")
    subOptionsWindow.geometry("400x400")

    if selectedOption == "ROAD":
        subOptions = ["HIGHWAY", "DYNO"]
    elif selectedOption == "CAN TRAIN AND TEST":
        if attack == True:
            subOptions= ["CAR 1 attacks","CAR 2 attacks", "CAR 3 attacks"]
        else:   
            subOptions = ["CAR 1", "CAR 2", "CAR 3"]
    else:
        if selectedOption == "CAR 1 attacks":
            subOptions = ["combined-attacks1", "DoS-attacks1","fuzzing-attacks1", "gear-attacks1", "interval-attacks1", "rpm-attacks1", "speed-attacks1", "standstill-attacks1", "systematic-attacks1"]
        elif selectedOption == "CAR 2 attacks":
            subOptions = ["combined-attacks2", "DoS-attacks2","fuzzing-attacks2", "gear-attacks2", "interval-attacks2", "rpm-attacks2", "speed-attacks2", "standstill-attacks2", "systematic-attacks2"]
        else:
            subOptions = ["combined-attacks3", "DoS-attacks3","fuzzing-attacks3", "gear-attacks3", "interval-attacks3", "rpm-attacks3", "speed-attacks3", "standstill-attacks3", "systematic-attacks3"]
    
    canvas = tk.Canvas(subOptionsWindow, width=400, height=100)
    canvas.create_text(200, 25, text="CAN control center", fill="black", font="bold", justify="center")
    canvas.create_text(200, 75, text="Choose a sub folder", justify="center")
    canvas.pack()
    
    subOptionVar = tk.StringVar(subOptionsWindow)
    subOptionVar.set(subOptions[0])

    subOptionDropdown = tk.OptionMenu(subOptionsWindow, subOptionVar, *subOptions)
    subOptionDropdown.pack(pady=10)
    if selectedOption == "CAN TRAIN AND TEST" and attack == True:
        confirmButton = tk.Button(subOptionsWindow, text="Choose sub folder", command=lambda: openSubOptionsWindow(subOptionVar.get(), dataset, attack))
        confirmButton.pack(pady=5)
    else:
        if selectedOption == "CAR 1 attacks":
            confirmButton = tk.Button(subOptionsWindow, text="Choose sub folder", command=lambda: openLogWindow(subOptionVar.get(), dataset, subDataset="CAR 1"))
            confirmButton.pack(pady=5)
        elif selectedOption == "CAR 2 attacks":
            confirmButton = tk.Button(subOptionsWindow, text="Choose sub folder", command=lambda: openLogWindow(subOptionVar.get(), dataset, subDataset="CAR 2"))
            confirmButton.pack(pady=5)
        elif selectedOption == "CAR 3 attacks":
            confirmButton = tk.Button(subOptionsWindow, text="Choose sub folder", command=lambda: openLogWindow(subOptionVar.get(), dataset, subDataset="CAR 3"))
            confirmButton.pack(pady=5)
        else:
            confirmButton = tk.Button(subOptionsWindow, text="Choose sub folder", command=lambda: openLogWindow(subOptionVar.get(), dataset, subOptionVar.get()))
            confirmButton.pack(pady=5)


def openLogWindow(selectedOption, dataset, subDataset):
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
    canvas.create_text(200, 25, text="CAN control center", fill="black", font="bold", justify="center")
    canvas.create_text(200, 75, text="Choose a log file", justify="center")
    canvas.pack()

    fileVar = tk.StringVar(newWindow)
    fileVar.set(logFiles[0])

    fileDropdown = tk.OptionMenu(newWindow, fileVar, *logFiles)
    fileDropdown.pack(pady=10)

    showFileButton = tk.Button(newWindow, text="Choose log file", command=lambda: showSelectedFile(path, fileVar.get(), dataset, subDataset))
    showFileButton.pack(pady=5)


def showSelectedFile(path, selectedFile, dataset, subDataset):
    newWindow = tk.Toplevel(root)
    newWindow.title("Simulate log file")
    newWindow.geometry("400x400")

    canvas = tk.Canvas(newWindow, width= 400, height= 100)
    canvas.create_text(200, 25, text="CAN control center", fill="black", font="bold", justify="center")
    canvas.create_text(200, 75, text="Chosen file: \n" + selectedFile, justify="center")
    canvas.pack()

    runFileButton = tk.Button(newWindow, text="Start simulation", command=lambda: runSelectedFile(path, selectedFile, dataset, subDataset))
    runFileButton.pack(pady=5)


def runSelectedFile(selectedPath, selectedFile, dataset, subDataset):
    path = selectedPath
    file = os.path.join(path, selectedFile)
    chooseECUs(file, dataset, subDataset, attack_var.get())

        
def onAttackCheck():
    attack_var.set(True)
    attack_free_var.set(False)

def onAttackFreeCheck():
    attack_var.set(False)
    attack_free_var.set(True)


root = tk.Tk()
root.title("CAN control center")
root.geometry("400x400")

datasets = ["ROAD", "GIDS", "CAN TRAIN AND TEST"]

dropdownVar = tk.StringVar(root)
dropdownVar.set(datasets[0])

canvas = tk.Canvas(root, width=400, height=100)
canvas.create_text(200, 25, text="CAN control center", fill="black", font="bold", justify="center")
canvas.create_text(200, 75, text="Choose a dataset to simulate", justify="center")
canvas.pack()

dropdown = tk.OptionMenu(root, dropdownVar, *datasets)
dropdown.pack(pady=10)

button = tk.Button(root, text="Choose dataset", command=onButtonClick)
button.pack(pady=10)

attack_var = tk.BooleanVar()
attack_free_var = tk.BooleanVar(value=True)

attack_checkbox = tk.Checkbutton(root, text="Attack", variable=attack_var, command=onAttackCheck)
attack_checkbox.pack()

attack_free_checkbox = tk.Checkbutton(root, text="Attack Free", variable=attack_free_var, command=onAttackFreeCheck)
attack_free_checkbox.pack()

root.mainloop()
