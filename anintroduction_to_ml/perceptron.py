import common
import random
import math

common.attribute_count = 4
#train_data = common.read_data_set('data_train_perceptron')
train_data = common.read_data_set('data_train_polynomial')
#train_data = common.read_data_set('data_train_temp')
common.attribute_count = common.attribute_count - 1


def xigema(w, ex):
    result = w[0]
    for index in range(0, common.attribute_count):
        result = result + w[index + 1] * ex[index]
    return result


def h_x(w, ex, theata):
    result = xigema(w, ex)
    return result > theata and 1 or 0


def learn_w_perceptron_1(w, n, cx, hx, x):
    w = w + n * (cx - hx) * x
    return w


def learn_w_perceptron_2(w, n, cx, hx, x):
    w = w + n * (cx - hx)
    return w


def learn_w_perceptron_3(w, n, cx, xigema, x):
    w = w + n * (cx - xigema) * x
    return w


def learn_w_perceptron_4(w, n, cx, xigema, x):
    w = w + n * (cx - xigema)
    return w


def learn_w_winnow(w, a, cx, hx, x):
    if x == 0:
        return w
    else:
        w = w * math.pow(a, cx - hx)
        return w


def add_c(N):
    if N == 0:
        return
    for index in range(len(train_data)):
        for i in range(0, N):
            train_data[index].insert(0, random.randint(0, 1))
        train_data[index].pop()
        c = train_data[index].count(1) >= 3 and 1 or 0
        train_data[index].append(c)


winnow = False
winnow_double = False
logAll = False

append = 0
for index in range(len(train_data)):
    print train_data[index]
add_c(append)
for index in range(len(train_data)):
    print train_data[index]
common.attribute_count = common.attribute_count + append

n = 0.5

w_array = []
for index in range(0, common.attribute_count + 1):
    if winnow:
        w_array.append(index == 0 and 0 or 1)
        if index != 0 and winnow_double:
            w_array.append(1)
    else:
        w_array.append(random.randint(1, 9) * 0.1)

if winnow and winnow_double:
    for index in range(len(train_data)):
        for i in range(0, common.attribute_count):
            item = train_data[index][i]
            insert = item == 0 and 1 or 0
            train_data[index].insert(common.attribute_count + i, insert)
    common.attribute_count = common.attribute_count * 2
    for index in range(len(train_data)):
        print train_data[index]

print w_array

max_step = 0
error_count = 1
while error_count > 0 and max_step < 100:
    max_step = max_step + 1
    error_count = 0
    print('################################## round %d' % (max_step))
    for index in range(len(train_data)):
        xgma = xigema(w_array, train_data[index])
        if winnow:
            hx = h_x(w_array, train_data[index], common.attribute_count - 0.1)
        else:
            hx = h_x(w_array, train_data[index], 0.0)
        ex = train_data[index]
        cx = ex[common.attribute_count]
        if logAll:
            print('---------start--------')
            print ex
            print w_array
        if logAll:
            print('hx %d cx %d' % (hx, cx))

        if cx != hx:
            if logAll:
                print 'learn'
            error_count = error_count + 1
            for i in range(winnow and 1 or 0, len(w_array)):
                x_i = i == 0 and 1 or ex[i - 1]
                if winnow:
                    w_array[i] = learn_w_winnow(w_array[i], 2, cx, hx, x_i)
                else:
                    #w_array[i] = learn_w_perceptron_1(w_array[i], n, cx, hx, x_i)
                    w_array[i] = learn_w_perceptron_4(w_array[i], n, cx, xgma, x_i)
                    if logAll:
                        print('w%d = %.2f' % (i, w_array[i]))
        else:
            if logAll:
                print 'pass'
                print '---------finish---------'
    print w_array
    print('error_rate %.2f%%' % (error_count*1.0 / len(train_data) * 100.0))
print error_count == 0 and 'success' or 'failed'