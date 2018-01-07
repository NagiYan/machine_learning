import math
import common


def cal_u(data_set, index, category):
    total = 0.0;
    count = 0;
    for data in data_set:
        if data[common.attribute_count] == category:
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
            if index < common.attribute_count:
                xigema = xigema + math.exp(-0.5 * math.pow(attributes[index_a] - us[index], 2))
        final_p = final_p * p * xigema

    return final_p


avg_error = 0.0
run = 100
for time in range(0, run):
    u_category = []
    train_data_set = common.read_train_data()
    check_data_set = common.check_data_set
    #common.add_noise(train_data_set, 0.25)

    for index_category in range(len(common.categorys)):
        u_array = []
        for index in range(0, common.attribute_count):
            u = cal_u(train_data_set, index, common.categorys[index_category])
            u_array.append(u)
        u_category.append(u_array)

    error_count = 0

    for data in check_data_set:
        p_array = []
        for category_index in range(len(common.categorys)):
            p = cal_p_category(data, u_category[category_index])
            p_array.append(p)
        max_p = 0.0
        max_index = 0
        for index in range(len(p_array)):
            if max_p < p_array[index]:
                max_index = index
                max_p = p_array[index]
        #print("%s %s" % (data, common.categorys[max_index]))
        if data[common.attribute_count] != common.categorys[max_index]:
            error_count = error_count + 1
    #print("error: %d/%d error_rate: %.1f%%" % (error_count, len(check_data_set), error_count * 100.0 / len(check_data_set)))
    avg_error = avg_error + error_count * 100.0 / len(common.check_data_set)
    print time
print('%d run avg_error_rate: %.1f%%' % (run, avg_error / run))



