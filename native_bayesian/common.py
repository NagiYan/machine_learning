import random

# config
attribute_count = 4
train_percent = 0.6


def read_data_set(file_name):
    data_set = []
    document = open(file_name)
    context = document.readline()
    while len(context) > 0:
        context = document.readline()
        if len(context) > 0:
            context = context.replace('\n', '')
            line = context.split(',')
            for index in range(len(line)):
                if index < attribute_count:
                    line[index] = float(line[index])
            data_set.append(line)
    return data_set


# config
train_data_set = read_data_set('data_train')
train_count = len(train_data_set)*train_percent
check_data_set = []
while len(train_data_set) > train_count:
    index = random.randint(0, len(train_data_set) - 1)
    check_data_set.append(train_data_set.pop(index))


categorys = ['Iris-setosa', 'Iris-versicolor', 'Iris-virginica']
