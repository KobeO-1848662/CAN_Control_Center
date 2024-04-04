import time

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

ecuMessageMappingCANTRAIN1 = {
    0: [1001, 1017, 1019, 1217, 1233, 1906, 417, 451, 707, 961, 977, 1265, 401],
    1: [1225, 1919, 413, 501, 249, 1322, 312, 193, 455, 969, 1249, 1005, 499],
    2: [1280, 1907, 381, 383, 388, 489, 761, 840, 461, 842, 485, 241, 1009],
    3: [298, 308, 1300, 409, 288, 820, 1905, 197, 201, 481, 1257, 497]
}

ecuMessageMappingCANTRAIN2 = {
    0: [1001, 1017, 1019, 1217, 1233, 1265, 1906, 201, 707, 977, 417, 451, 961, 413, 431, 401, 501],
    1: [1021, 1910, 459, 721, 969, 485, 1005, 1009],
    2: [1241, 1904, 1300, 409, 481, 491, 495, 1905],
    3: [1280, 1907, 193, 381, 383, 455, 461, 489, 761, 840, 842, 197, 388, 820, 298],
    4: [199, 249, 1919, 1225, 393, 1257, 497],
    5: [241, 288, 312, 1322, 1249, 493, 499],
}

ecuMessageMappingCANTRAIN3 = {
    0: [1001, 1265, 1267, 190, 417, 419, 426, 442, 451, 452, 453, 479, 500, 961, 977, 979, 985, 170, 1914, 398, 647, 707, 1912, 328],
    1: [1017, 1019, 1020, 1217, 1223, 1233, 1417, 1906, 485],
    2: [1225, 1919, 562, 1221, 209, 1257, 288, 1328, 493],
    3: [1280, 842, 1105, 199, 211, 241, 1322, 320, 1005],
    4: [1907, 1920, 208, 381, 386, 389, 454, 455, 462, 489, 508, 510, 532, 563, 564, 761, 840, 844, 866, 193],
    5: [1928, 304, 309, 311, 313, 289, 298, 352, 497],
    6: [413, 422, 431, 393, 501, 249, 810, 969, 1009],
    7: [460, 463, 197, 201, 1249, 1300, 1323, 481, 499]
}

def sendMessageToECU(ecuID, messageID, timestamp):
    print(f"Sending message {messageID} to ECU {ecuID}: ({timestamp})")

def simulateLogFile(logfile):
    with open(logfile, 'r') as file:
        for line in file:
            if '#' in line:
                message = line.split('#')[0]
                messageID = message.split(' ')[2]
                decimalID = int(messageID, 16)

                currentTimestamp = time.time()
                
                for ecuID, messages in ecuMessageMappingROAD.items():
                    if decimalID in messages:
                        sendMessageToECU(ecuID, decimalID, currentTimestamp)
                        break
                    #else: 
                    #    print(f"no mapping found for id {decimalID}")

    print(f"\neinde simulatie")

    time.sleep(0.01)

def simulateLogFileCANTRAIN(logfile):
    with open(logfile, 'r') as file:
        for line in file:
            if '#' in line:
                message = line.split('#')[0]
                messageID = message.split(' ')[2]
                decimalID = int(messageID, 16)

                currentTimestamp = time.time()
                
                for ecuID, messages in ecuMessageMappingCANTRAIN1.items():
                    if decimalID in messages:
                        sendMessageToECU(ecuID, decimalID, currentTimestamp)
                        break
                    #else: 
                    #    print(f"no mapping found for id {decimalID}")
    
    print(f"\neinde simulatie")
            
    time.sleep(0.01)


    



def getUniqueIds(file):
    messageIds = set()
    
    with open(file, 'r') as file:
        for line in file:
            if '#' in line:
                message = line.split('#')[0]
                messageId = message.split(' ')[2]
                decimalId = int(messageId, 16)
                messageIds.add(decimalId)
    
    print(messageIds)
    return messageIds

