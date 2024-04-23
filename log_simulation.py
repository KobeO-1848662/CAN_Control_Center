import serial
import time

ECU0 = serial.Serial(port='COM6', baudrate=115200, timeout=0.01)      

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

def sendMessageToECU(message, id):
    #if id == 0:
    ECU0.write(bytes(message, 'utf-8'))
    data = ECU0.read()
    return print(data)
    

def runSimulation(logfile):
    with open(logfile, 'r') as file:
        for line in file:
            if '#' in line:   
                message = line.split()
                data = message[2]
                mess = data.split('#')
                newMessage = f"{mess[0]} {mess[1]}"
                messageID = mess[0]
                decimalID = int(messageID, 16)

                for ecuID, messages in ecuMessageMappingROAD.items():
                    if decimalID in messages:
                        sendMessageToECU(newMessage, ecuID)
                        break
        print("simulatie voltooid")
