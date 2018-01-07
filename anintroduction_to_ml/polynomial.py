import random


def is_postive(ex):
    w = [1, -1, -1, -1]
    hx = w[0]
    for i in range(len(ex)):
        hx = w[i + 1] * ex[i]
    return hx > 0 and 1 or 0


def create_train_data(count):
    example = []
    for idx_count in range(0, count):
        ex = []
        for i in range(0, 3):
            x = random.randint(0, 10) * 0.1
            ex.append(x)
        hx = is_postive(ex)
        ex.append(hx)
        example.append(ex)
    return example


def write_train_data():
    file_object = open('data_train_polynomial', 'w')
    example = create_train_data(100)
    for index in range(len(example)):
        ex = example[index]
        s_line = '%.1f,%.1f,%.1f,%d\n' % (ex[0], ex[1], ex[2], ex[3])
        file_object.writelines(s_line)
    file_object.close()


n = 0.5

