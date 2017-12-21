import math

# config
attribute_count = 4


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
checke_data_set = read_data_set('data_check')
categorys = ['Iris-setosa', 'Iris-versicolor', 'Iris-virginica']


def cal_u(data_set, index, category):
    total = 0.0;
    count = 0;
    for data in data_set:
        if data[attribute_count] == category:
            total = total + data[index]
            count = count + 1
    u = total / count
    return u


def cal_p_category(attributes, us):
    p = 1 / math.sqrt(math.pow(math.pi * 2, 3))

    final_p = 1
    for index_a in range(len(us)):
        xigema = 0.0
        for index in range(len(attributes)):
            if index < attribute_count:
                xigema = xigema + math.exp(-0.5 * math.pow(attributes[index_a] - us[index], 2))
        final_p = final_p * p * xigema

    return final_p



u_category = []
for index_category in range(len(categorys)):
    u_array = []
    for index in range(0, attribute_count):
        u = cal_u(train_data_set, index, categorys[index_category])
        u_array.append(u)
    u_category.append(u_array)

for data in checke_data_set:
    p_array = []
    for category_index in range(len(categorys)):
        p = cal_p_category(data, u_category[category_index])
        p_array.append(p)
    max_p = 0.0
    max_index = 0
    for index in range(len(p_array)):
        if max_p < p_array[index]:
            max_index = index
            max_p = p_array[index]
    print("%s %s" % (data, categorys[max_index]))

