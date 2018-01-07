import math
import random
import numpy as np


count_output = 2
count_hide = 2
count_attribute = 2
count_class = 2
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
targets_v = np.array([[1], [0]])
eta = 0.1


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


def f_delta_1_v(outputs):
    temp = outputs * (1 - outputs)
    result = temp * (targets_v - outputs)
    return result


def f_delta_2_v(hide_layer, delta_1):
    temp = hide_layer * (1 - hide_layer)
    delat = np.dot(delta_1.T, w_output_v)
    result = delat * temp.T
    return result


def f_bp_w_1(delta, hide_layer):
    result = w_output_v + np.dot(eta * delta, hide_layer.T)
    return result


def f_bp_w_2(delta, inputs):
    result = w_input_v + np.dot(eta * delta.T, inputs)
    return result


w_input_v = random_w_input_v()
w_output_v = random_w_output_v()


h = f_h_v(ex_input_v)
y = f_z_v(h)
delta_1 = f_delta_1_v(y)
delta_2 = f_delta_2_v(h, delta_1)
w_1 = f_bp_w_1(delta_1, h)
w_2 = f_bp_w_2(delta_2, ex_input_v)


print h
print y
print delta_1
print delta_2
print w_1
print w_2
