import copy;

#finalStatus = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
finalStatus = [[1, 2, 3], [8, 0 , 4], [7, 6, 5]]

def distance1(number, line, index):
    distancef = 0
    for linef in range(len(finalStatus)):
        for indexf in range(len(finalStatus[linef])):
            numberf = finalStatus[linef][indexf]
            if numberf == number:
                distancef = abs(line - linef) + abs(index - indexf)
                break
        if distancef > 0:
            break
    return distancef

def judgement1(status):
    length = 0
    for line in range(len(status)):
        for index in range(len(status[line])):
            number = status[line][index]
            if number != 0 and finalStatus[line][index] != number:
                length = length + distance1(number, line, index)
    return length


def distance2(number, line, index):
    distancef = 0
    for linef in range(len(finalStatus)):
        for indexf in range(len(finalStatus[linef])):
            numberf = finalStatus[linef][indexf]
            if numberf == number:
                if number == 1:
                    distancef = (abs(line - linef) + abs(index - indexf)) * 10
                elif number == 2 or number == 3:
                    distancef = (abs(line - linef) + abs(index - indexf)) * 5
                elif number == 4 or number == 5:
                    distancef = (abs(line - linef) + abs(index - indexf)) * 2
                else:
                    distancef = abs(line - linef) + abs(index - indexf)
                break
        if distancef > 0:
            break
    return distancef

def judgement2(status):
    length = 0
    for line in range(len(status)):
        for index in range(len(status[line])):
            number = status[line][index]
            if number != 0 and finalStatus[line][index] != number:
                length = length + distance2(number, line, index)
    return length



def new_status_from(status):
    status_list = []
    for line in range(len(status)):
        for index in range(len(status[line])):
            number = status[line][index]
            if number == 0:
                if line != 0:
                    status_t = copy.deepcopy(status)
                    status_t[line][index] = status[line - 1][index]
                    status_t[line - 1][index] = 0
                    status_list.append(status_t)
                if line != 2:
                    status_t = copy.deepcopy(status)
                    status_t[line][index] = status[line + 1][index]
                    status_t[line + 1][index] = 0
                    status_list.append(status_t)
                if index != 0:
                    status_t = copy.deepcopy(status)
                    status_t[line][index] = status[line][index - 1]
                    status_t[line][index - 1] = 0
                    status_list.append(status_t)
                if index != 2:
                    status_t = copy.deepcopy(status)
                    status_t[line][index] = status[line][index + 1]
                    status_t[line][index + 1] = 0
                    status_list.append(status_t)
                break
    return status_list


listTemp = []
listSeen = []

def is_new_move(status):
    if status in listSeen:
        return False
    else:
        return True


#beginStatus = [[4, 3, 2], [1, 6, 5], [8, 0, 7]]
beginStatus = [[0, 2, 1], [6, 7, 4], [3, 8, 5]]

listTemp.append(beginStatus)
while len(listTemp) > 0:
    print len(listSeen)
    status0 = listTemp[0]
    print status0[0]
    print status0[1]
    print status0[2]
    length = judgement1(status0)
    print length
    print '----------'
    if length <= 0:
        break
    else:
        listSeen.append(status0)
        listTemp.pop(0)
        status_list = new_status_from(status0)
        status_list = filter(is_new_move, status_list)
        for status in status_list:
            listTemp.append(status)
        listTemp = sorted(listTemp, key=lambda status: judgement2(status), reverse=False)


