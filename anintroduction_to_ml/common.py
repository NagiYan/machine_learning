import random

# config
attribute_count = 4
train_percent = 0.6
check_data_set = []
train_data_set = []
categorys = ['Iris-setosa', 'Iris-versicolor', 'Iris-virginica']


def read_data_set(file_name):
    data_set = []
    document = open(file_name)
    context = document.readline()
    while len(context) > 0:
        context = context.replace('\n', '')
        line = context.split(',')
        for index in range(len(line)):
            if index < attribute_count:
                line[index] = float(line[index])
        data_set.append(line)
        context = document.readline()
    return data_set


def read_train_data():
    del check_data_set[:]
    del train_data_set[:]
    train_data_set.extend(read_data_set('data_train'))
    train_count = len(train_data_set) * train_percent
    while len(train_data_set) > train_count:
        index = random.randint(0, len(train_data_set) - 1)
        check_data_set.append(train_data_set.pop(index))
    return train_data_set


def add_noise(data_set, percent):
    count = int(len(data_set)*percent)
    random.shuffle(data_set)
    for index in range(0, count):
        cate = data_set[index][attribute_count]
        i = categorys.index(cate)
        i = (i + 1) % len(categorys)
        data_set[index][attribute_count] = categorys[i]
    return


