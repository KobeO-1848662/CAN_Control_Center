import serial
import tkinter as tk
from tkinter import messagebox
import serial.tools.list_ports


ecuMessageMappingROAD = {
    0: [1031, 117, 1512, 458, 569, 61, 722, 1788, 651, 737, 930, 1262, 631, 1661, 1694, 1505],
    1: [1076, 1124, 1176, 1314, 1408, 215, 403, 526, 870, 1072, 304, 738, 837, 452, 1227, 560, 14],
    2: [1255, 1590, 1628, 1634, 1668, 192, 339, 412, 628, 661, 727, 996, 65, 1560, 1644, 519, 1225],
    3: [1307, 204, 241, 1621, 186, 241, 627, 663, 676, 881, 263, 640],
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

def sendMessageToECU(message, id, ecuList):
    if id == 0:
        ECU0 = serial.Serial(port=ecuList[0], baudrate=115200, timeout=0.01) 
        ECU0.write(bytes(message, 'utf-8'))
        #data = ECU0.read()
        #return print(data)
    '''
    elif id == 1:
        ECU1 = serial.Serial(port=ecuList[1], baudrate=115200, timeout=0.01) 
        ECU1.write(bytes(message, 'utf-8'))
        data = ECU1.read()
        return print(data)
    
    elif id == 2:
        ECU2 = serial.Serial(port=ecuList[2], baudrate=115200, timeout=0.01) 
        ECU2.write(bytes(message, 'utf-8'))
        data = ECU2.read()
        return print(data)
    
    zelfde nog doen voor overige ECUs
    '''
    

def runSimulation(logfile, dataset, ecuList):
    with open(logfile, 'r') as file:
        for line in file:
            if '#' in line:   
                message = line.split()
                data = message[2]
                mess = data.split('#')
                newMessage = f"{mess[0]} {mess[1]}"
                messageID = mess[0]
                decimalID = int(messageID, 16)

                if dataset == "ROAD":
                    for ecuID, messages in ecuMessageMappingROAD.items():
                        if decimalID in messages:
                            sendMessageToECU(newMessage, ecuID, ecuList)
                            break
                if dataset == "CAN TRAIN AND TEST":
                    for ecuID, messages in ecuMessageMappingCanTrain1.items():
                        if decimalID in messages:
                            sendMessageToECU(newMessage, ecuID, ecuList)
                            break
                #if dataset == "GIDS":
                 #   for ecuID, messages in ecuMessageMappingROAD.items():
                  #      if decimalID in messages:
                   #         sendMessageToECU(newMessage, ecuID, ecuList)
                    #        break        
        print("simulatie voltooid")

def checkValid(logfile, dataset, ecuList):
    if len(ecuList) != len(set(ecuList)):
        messagebox.showwarning("Error", "Two ECUs are connected to the same port")
    else:
        runSimulation(logfile, dataset, ecuList)


def chooseECUs(logfile, dataset):
    ecuWindow = tk.Tk()
    ecuWindow.title("choose ECUs")
    ecuWindow.geometry("400x400")

    ports = serial.tools.list_ports.comports()
    availableECUs = [port.name for port in ports]
    
    canvas = tk.Canvas(ecuWindow, width=400, height=100)
    canvas.create_text(200, 25, text="Choose your ECUs", font="bold", justify="center")
    canvas.pack()
    
    if dataset == "ROAD":
        #if len(availableECUs) < 8:
        #    messagebox.showwarning("Not enough ECUs", "There are not enough ECUs connected to run this file. The minimum amount that should be connected is 8")
        #    ecuWindow.destroy()
        #else:
            canvas2 = tk.Canvas(ecuWindow, width=400, height=200)
            canvas2.pack()

            ecuVars = [tk.StringVar(canvas2, value=availableECUs[0]) for _ in range(8)]
            dropdowns = []

            for i in range(8):
                canvas2.create_text(150, 40 + i*20, text=f"ecu {i+1}: ", justify="center")
                dropdown = tk.OptionMenu(canvas2, ecuVars[i], *availableECUs)
                dropdown.pack()
                dropdowns.append(dropdown)
                canvas2.create_window(220, 40 + i*20, window=dropdowns[i])
 
            confirmButton = tk.Button(ecuWindow, text= "run simulation", command=lambda: checkValid(logfile, dataset, ecuList=[ecuVars[0].get()]))
            confirmButton.pack(pady=10)

    
    elif dataset == "CAN TRAIN AND TEST":
        if len(availableECUs) < 4:
            messagebox.showwarning("Not enough ECUs", "There are not enough ECUs connected to run this file. The minimum amount that should be connected is 4")
            ecuWindow.destroy()
        else:
            canvas2 = tk.Canvas(ecuWindow, width=400, height=200)
            canvas2.pack()

            ecuVars = [tk.StringVar(canvas2, value=availableECUs[0]) for _ in range(4)]
            dropdowns = []

            for i in range(4):
                canvas2.create_text(150, 40 + i*20, text=f"ecu {i+1}: ", justify="center")
                dropdown = tk.OptionMenu(canvas2, ecuVars[i], *availableECUs)
                dropdown.pack()
                dropdowns.append(dropdown)
                canvas2.create_window(220, 40 + i*20, window=dropdowns[i])

            confirmButton = tk.Button(ecuWindow, text= "run simulation", command=lambda: checkValid(logfile, dataset, ecuList=[var.get() for var in ecuVars]))
            confirmButton.pack(pady=10)
