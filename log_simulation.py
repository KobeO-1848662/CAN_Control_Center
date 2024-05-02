import serial
import tkinter as tk
from tkinter import messagebox
import serial.tools.list_ports
import time
import numpy as np

ecuMessageMappingROAD = {
    0: [1031, 117, 1512, 458, 569, 61, 722, 1788, 651, 737, 930, 1262, 631, 1661, 1694, 1505],
    1: [1076, 1124, 1176, 1314, 1408, 215, 403, 526, 870, 1072, 304, 738, 837, 452, 1227, 560, 14],
    2: [1255, 1590, 1628, 1634, 1668, 192, 339, 412, 628, 661, 727, 996, 65, 1560, 1644, 519, 1225],
    3: [1307, 204, 241, 1621, 186, 627, 663, 676, 881, 263, 640],
    4: [1372, 58, 675, 1175, 1693, 354, 167, 208, 1277, 1331, 1455, 4095],
    5: [1398, 248, 426, 6, 1049, 51, 683, 1751, 778, 852, 1459],
    6: [253, 60, 705, 961, 541, 622, 692, 1760, 293, 1399, 953],
    7: [485, 813, 420, 470, 37, 1649, 695, 244, 300, 1413, 1533]
}

ecuMessageMappingCanTrain1 = {
    0: [1001, 1017, 1019, 1217, 1233, 1906, 417, 451, 707, 961, 977, 1265, 401],
    1: [1225, 1919, 413, 501, 249, 1322, 312, 193, 455, 969, 1249, 1005, 499],
    2: [1280, 1907, 381, 383, 388, 489, 761, 840, 461, 842, 485, 241, 1009],
    3: [298, 308, 1300, 409, 288, 820, 1905, 197, 201, 481, 1257, 497]
}

ecuMessageMappingCanTrain2 = {
    0: [1001, 1017, 1019, 1217, 1233, 1265, 1906, 201, 707, 977, 417, 451, 961, 413, 431, 401, 501],
    1: [1021, 1910, 459, 721, 969, 485, 1005, 1009],
    2: [1241, 1904, 1300, 409, 481, 491, 495, 1905],
    3: [1280, 1907, 193, 381, 383, 455, 461, 489, 761, 840, 842, 197, 388, 820, 298],
    4: [199, 249, 1919, 1225, 393, 1257, 497],
    5: [241, 288, 312, 1322, 1249, 493, 499]
}

ecuMessageMappingCanTrain3 = {
    0: [1001, 1265, 1267, 190, 417, 419, 426, 442, 451, 452, 453, 479, 500, 961, 977, 979, 985, 170, 1914, 398, 647, 707, 1912, 328],
    1: [1017, 1019, 1020, 1217, 1223, 1233, 1417, 1906, 485],
    2: [1225, 1919, 562, 1221, 209, 1257, 288, 1328, 493],
    3: [1280, 842, 1105, 199, 211, 241, 1322, 320, 1005],
    4: [1907, 1920, 208, 381, 386, 389, 454, 455, 462, 489, 508, 510, 532, 563, 564, 761, 840, 844, 866, 193],
    5: [1928, 304, 309, 311, 313, 289, 298, 352, 497],
    6: [413, 422, 431, 393, 501, 249, 810, 969, 1009],
    7: [460, 463, 197, 201, 1249, 1300, 1323, 481, 499]
}

ecuMessageMappingGids = {
    0: [1087, 880, 2, 160, 304, 320, 688,339], 
    1: [1201, 497, 399, 161, 305, 1088, 608], 
    2: [1440, 1442, 790, 809,  1349, 1264], 
    3: [1520, 1680, 672, 1072, 704, 848]
}
def sendMessageToECU(message, ecu, ecuList):
    for i in range(len(ecuList)):
        if ecu == i:
            ecuList[i].write(bytes(message, 'utf-8'))
            data = ecuList[i].read()
            print(data)
        

def assignEcus(portlist):
    ecuList = []
    for elem in portlist:
        ecu = serial.Serial(port=elem, baudrate=115200, timeout=0.01)
        ecuList.append(ecu)
    return ecuList

def runForLoop(val):
    for i in range(0,int(val)):
        for j in range(1):
            for k in range(1):
                for l in range(1):
                    pass

def calibrationError():
    messagebox.showwarning("Calibration Error", "Try running again")


def calibrateForLoop(valList, threshold):
    for i in valList:
        timeTaken = []
        for j in range(50):
            start = time.time()
            runForLoop(i)
            end = time.time()
            timeTaken.append((end-start))

        median = np.median(timeTaken)*1000000 
        dev = abs(median - 10.0)
        if dev < threshold:
            return i
        else:
            if median > 10:                    
                newList = []
                lower = valList[valList.index(i)-1]
                upper = i
                nplist = np.linspace(lower, upper, 10)
                for e in nplist:
                    newList.append(int(e))
                result = calibrateForLoop(newList, threshold)
                if result is not None:
                    return result
                else:
                    break
        if i == valList[len(valList)-1]:
            return calibrationError()
            

def runSimulation(logfile, dataset, subDataset, portList):
    ecuList = assignEcus(portList)
    with open(logfile, 'r') as file:
        val = [10,100,1000,10000,100000]
        threshold = 1.0           
        value = calibrateForLoop(val, threshold)
        timeStamp = 0
        for line in file:
            if '#' in line:   
                timeStampPrev = timeStamp
                message = line.split()
                timeStamp = message[0].replace("(", "").replace(")","").replace(".", "")
                if timeStampPrev == 0:
                    dtime =  0 
                else:
                    dtime = (int(timeStamp) - int(timeStampPrev))/10
                data = message[2]
                mess = data.split('#')
                messLen = int(len(mess[1])/2)
                newMessage = f"{messLen}{mess[0]}{mess[1]}"
                messageID = mess[0]
                decimalID = int(messageID, 16)

                if dataset == "ROAD":
                    for ecuID, messages in ecuMessageMappingROAD.items():
                        if decimalID in messages:
                            runForLoop(int(dtime*value))
                            sendMessageToECU(newMessage, ecuID, ecuList)
                            break
                elif dataset == "CAN TRAIN AND TEST":
                    if subDataset == "CAR 1":
                        for ecuID, messages in ecuMessageMappingCanTrain1.items():
                            if decimalID in messages:
                                runForLoop(int(dtime*value))
                                sendMessageToECU(newMessage, ecuID, ecuList)
                                break
                    elif subDataset == "CAR 2":
                        for ecuID, messages in ecuMessageMappingCanTrain2.items():
                            if decimalID in messages:
                                runForLoop(int(dtime*value))
                                sendMessageToECU(newMessage, ecuID, ecuList)
                                break
                    else:
                        for ecuID, messages in ecuMessageMappingCanTrain3.items():
                            if decimalID in messages:
                                runForLoop(int(dtime*value))
                                sendMessageToECU(newMessage, ecuID, ecuList)
                                break
                else:
                    for ecuID, messages in ecuMessageMappingGids.items():
                        if decimalID in messages:
                            runForLoop(int(dtime*value))
                            sendMessageToECU(newMessage, ecuID, ecuList)
                            break        
        print("Simulation completed")

def checkValid(logfile, dataset, subDataset, portList):
    if len(portList) != len(set(portList)):
        messagebox.showwarning("Error", "Two ECUs are connected to the same port")
    else:
        runSimulation(logfile, dataset, subDataset, portList)


def chooseECUs(logfile, dataset, subDataset):
    ecuWindow = tk.Tk()
    ecuWindow.title("Choose ECUs")
    ecuWindow.geometry("400x400")

    ports = serial.tools.list_ports.comports()
    availablePorts = [port.name for port in ports]
    
    canvas = tk.Canvas(ecuWindow, width=400, height=100)
    canvas.create_text(200, 25, text="CAN control center", font ="bold", justify="center")
    canvas.create_text(200, 75, text="Assign your ECUs", justify="center")

    canvas.pack()
    
    if dataset == "ROAD":
        if len(availablePorts) < 8:
            messagebox.showwarning("Not enough ECUs", "There are not enough ECUs connected to run this file. The minimum amount that should be connected is 8")
            ecuWindow.destroy()
        else:
            canvas2 = tk.Canvas(ecuWindow, width=400, height=250)
            canvas2.pack()

            ecuVars = [tk.StringVar(canvas2, value=availablePorts[0]) for _ in range(8)]
            dropdowns = []

            for i in range(8):
                canvas2.create_text(150, 40 + i*25, text=f"ecu {i+1}: ", justify="center")
                dropdown = tk.OptionMenu(canvas2, ecuVars[i], *availablePorts)
                dropdown.pack()
                dropdowns.append(dropdown)
                canvas2.create_window(220, 40 + i*25, window=dropdowns[i])
 
            confirmButton = tk.Button(ecuWindow, text= "run simulation", command=lambda: checkValid(logfile, dataset, subDataset, portList=[f"/dev/{var.get()}" for var in ecuVars]))
            confirmButton.pack(pady=10)

    
    elif dataset == "CAN TRAIN AND TEST":
        if subDataset == "CAR 1":
            if len(availablePorts) < 4:
                messagebox.showwarning("Not enough ECUs", "There are not enough ECUs connected to run this file. The minimum amount that should be connected is 4")
                ecuWindow.destroy()
            else:
                canvas2 = tk.Canvas(ecuWindow, width=400, height=250)
                canvas2.pack()

                ecuVars = [tk.StringVar(canvas2, value=availablePorts[0]) for _ in range(4)]
                dropdowns = []

                for i in range(4):
                    canvas2.create_text(150, 40 + i*25, text=f"ecu {i+1}: ", justify="center")
                    dropdown = tk.OptionMenu(canvas2, ecuVars[i], *availablePorts)
                    dropdown.pack()
                    dropdowns.append(dropdown)
                    canvas2.create_window(220, 40 + i*25, window=dropdowns[i])

                confirmButton = tk.Button(ecuWindow, text= "run simulation", command=lambda: checkValid(logfile, dataset, subDataset, portList=[f"/dev/{var.get()}" for var in ecuVars]))
                confirmButton.pack(pady=10)
        
        elif subDataset == "CAR 2":
            if len(availablePorts) < 6:
                messagebox.showwarning("Not enough ECUs", "There are not enough ECUs connected to run this file. The minimum amount that should be connected is 6")
                ecuWindow.destroy()
            else:
                canvas2 = tk.Canvas(ecuWindow, width=400, height=250)
                canvas2.pack()

                ecuVars = [tk.StringVar(canvas2, value=availablePorts[0]) for _ in range(6)]
                dropdowns = []

                for i in range(6):
                    canvas2.create_text(150, 40 + i*25, text=f"ecu {i+1}: ", justify="center")
                    dropdown = tk.OptionMenu(canvas2, ecuVars[i], *availablePorts)
                    dropdown.pack()
                    dropdowns.append(dropdown)
                    canvas2.create_window(220, 40 + i*25, window=dropdowns[i])

                confirmButton = tk.Button(ecuWindow, text= "run simulation", command=lambda: checkValid(logfile, dataset, subDataset, portList=[f"/dev/{var.get()}" for var in ecuVars]))
                confirmButton.pack(pady=10)
        
        else:
            if len(availablePorts) < 8:
                messagebox.showwarning("Not enough ECUs", "There are not enough ECUs connected to run this file. The minimum amount that should be connected is 8")
                ecuWindow.destroy()
            else:
                canvas2 = tk.Canvas(ecuWindow, width=400, height=250)
                canvas2.pack()

                ecuVars = [tk.StringVar(canvas2, value=availablePorts[0]) for _ in range(8)]
                dropdowns = []

                for i in range(8):
                    canvas2.create_text(150, 40 + i*25, text=f"ecu {i+1}: ", justify="center")
                    dropdown = tk.OptionMenu(canvas2, ecuVars[i], *availablePorts)
                    dropdown.pack()
                    dropdowns.append(dropdown)
                    canvas2.create_window(220, 40 + i*25, window=dropdowns[i])

                confirmButton = tk.Button(ecuWindow, text= "run simulation", command=lambda: checkValid(logfile, dataset, subDataset, portList=[f"/dev/{var.get()}" for var in ecuVars]))
                confirmButton.pack(pady=10)
    else:
        if len(availablePorts) < 4:
            messagebox.showwarning("Not enough ECUs", "There are not enough ECUs connected to run this file. The minimum amount that should be connected is 4")
            ecuWindow.destroy()
        else:
            canvas2 = tk.Canvas(ecuWindow, width=400, height=250)
            canvas2.pack()

            ecuVars = [tk.StringVar(canvas2, value=availablePorts[0]) for _ in range(4)]
            dropdowns = []

            for i in range(4):
                canvas2.create_text(150, 40 + i*25, text=f"ecu {i+1}: ", justify="center")
                dropdown = tk.OptionMenu(canvas2, ecuVars[i], *availablePorts)
                dropdown.pack()
                dropdowns.append(dropdown)
                canvas2.create_window(220, 40 + i*25, window=dropdowns[i])
 
            confirmButton = tk.Button(ecuWindow, text= "run simulation", command=lambda: checkValid(logfile, dataset, subDataset, portList=[f"/dev/{var.get()}" for var in ecuVars]))
            confirmButton.pack(pady=10)

