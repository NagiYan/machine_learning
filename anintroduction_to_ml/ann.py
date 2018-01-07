import math
import random
import numpy as np
import common

# train times
count_train = 500
# learn rate
eta = 0.1
# nerual count
count_hide = 100

count_output = 10
count_attribute = 4
count_class = 3
w_input = [[-1, 0.5], [0.1, 0.7]]
w_output = [[0.9, 0.5], [-0.3, -0.1]]
ex_input = [0.8, 0.1]


def f_sigma(sigma):
    result = 1 / (1 + math.pow(math.e, -sigma))
    return result


def random_w():
    for j in range(0, count_hide):
        w_k = []
        for k in range(0, count_hide):
            w = random.randint(1, 9) * 0.1
            w_k.append(w)
        w_input.append(w_k)

    for i in range(0, count_output):
        w_j = []
        for j in range(0, count_hide):
            w = random.randint(1, 9) * 0.1
            w_j.append(w)
        w_output.append(w_j)
    return


def f_z(inputs):
    hide_layer = []
    for j in range(len(inputs)):
        sigma = 0
        for k in range(len(inputs)):
            sigma = sigma + inputs[k] * w_input[j][k]
        h = f_sigma(sigma)
        hide_layer.append(h)

    output = []
    for i in range(len(w_output)):
        sigma = 0
        for j in range(len(hide_layer)):
            sigma = sigma + hide_layer[j] * w_output[i][j]
        h = f_sigma(sigma)
        output.append(h)

    print output


#f_z(ex_input)


w_input_v = np.array([[-1, 1], [1, 1]])
w_output_v = np.array([[1, 1], [-1, 1]])
ex_input_v = np.array([[1, -1]])
targets_v = np.array([[1, 0]])


def random_w_input_v():
    return np.random.randint(-10, 10, size=(count_hide, count_attribute)) * 0.1


def random_w_output_v():
    return np.random.randint(-10, 10, size=(count_class, count_hide)) * 0.1


def f_sigma_v(sigma):
    result = 1 / (1 + np.power(math.e, -1 * sigma))
    return result


def f_h_v(inputs):
    hide_layer = np.dot(w_input_v, inputs.T)
    hide_layer = f_sigma_v(hide_layer)
    return hide_layer


def f_z_v(hide_layer):
    output = np.dot(w_output_v, hide_layer)
    output = f_sigma_v(output)
    return output


def f_delta_1_v(outputs, index):
    temp = outputs * (1 - outputs)
    result = temp * (targets_v[index, :].T - outputs)
    return result


def f_delta_2_v(hide_layer, delta_1):
    temp = hide_layer * (1 - hide_layer)
    delta = np.dot(delta_1.T, w_output_v)
    result = delta * temp.T
    return result


def f_bp_w_1(delta, hide_layer):
    delta.shape = (len(common.categorys), 1)
    np.transpose(delta)
    hide_layer.shape = (1, count_hide)
    np.transpose(hide_layer)

    change = np.dot(eta * delta, hide_layer)
    result = w_output_v + change
    return result


def f_bp_w_2(delta, inputs):
    delta.shape = (count_hide, 1)
    inputs.shape = (1, common.attribute_count)
    np.transpose(inputs)
    change = np.dot(eta * delta, inputs)
    result = w_input_v + change
    return result


def data_input_v(train_data):
    array_input = []
    for i in range(len(train_data)):
        ex = train_data[i][0:common.attribute_count]
        array_input.append(ex)
    ex_v = np.array(array_input)
    max_v = np.max(ex_v, 0)
    min_v = np.min(ex_v, 0)

    for i in range(len(train_data) - 1):
        max_v = np.vstack((max_v, np.max(ex_v, 0)))
        min_v = np.vstack((min_v, np.min(ex_v, 0)))
    range_v = (max_v - min_v)
    ex_v = (ex_v - min_v) / range_v
    return ex_v


def data_target_v(train_data):
    array_target = []
    for i in range(len(train_data)):
        target = []
        for j in range(len(common.categorys)):
            category = common.categorys[j]
            category_t = train_data[i][common.attribute_count]
            if category == category_t:
                target.append(1)
            else:
                target.append(0)
        array_target.append(target)
    return np.array(array_target)


def check():
    count_error = 0
    check_data_raw = common.check_data_set
    check_target_v = data_target_v(check_data_raw)
    check_input_v = data_input_v(check_data_raw)
    for i in range(len(check_data_raw)):
        h = f_h_v(check_input_v[i, :])
        y = f_z_v(h)
        max = np.max(y, 0)
        for j in range(len(common.categorys)):
            if max == y[j] and check_target_v[i, j] != 1:
                count_error = count_error + 1
    print('error rate: %d of %d %.2f%%' % (count_error, len(check_data_raw), count_error*100.0/len(check_data_raw)))

# train data not vectoring
train_data_raw = common.read_train_data()
# build target that vectoring
targets_v = data_target_v(train_data_raw)
# build the train data that vectoring
ex_input_v = data_input_v(train_data_raw)
# build the input w that random
w_input_v = random_w_input_v()
# build the output w that random
w_output_v = random_w_output_v()

for iter in range(0, count_train):
    print iter
    for i in range(len(train_data_raw)):
        h = f_h_v(ex_input_v[i, :])
        y = f_z_v(h)
        delta_1 = f_delta_1_v(y, i)
        delta_2 = f_delta_2_v(h, delta_1)
        w_1 = f_bp_w_1(delta_1, h)
        w_2 = f_bp_w_2(delta_2, ex_input_v[i, :])
        w_input_v = w_2
        w_output_v = w_1
    check()

