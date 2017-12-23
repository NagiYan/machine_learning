import math
import common

k = 3


def xigama_d_x_y(ex, ex_i):
    total = 0
    for index in range(len(ex)):
        if index < common.attribute_count:
            total = total + math.pow(ex[index] - ex_i[index], 2)
    total = math.sqrt(total)
    return total


def tomek(train_set):
    for i in range(len(train_set)):
        train_set[i].append(i)

    T = set()
    for i in range(1, len(train_set)):
        x = train_set[i]
        sorted_array = sorted(train_set, key=lambda ex: xigama_d_x_y(x, ex), reverse=False)
        y = sorted_array[1]
        if y[common.attribute_count] != x[common.attribute_count]:
            sorted_array_y = sorted(train_set, key=lambda ex: xigama_d_x_y(y, ex), reverse=False)
            if sorted_array_y[1][common.attribute_count+1] == x[common.attribute_count+1]:
                T.add(x[common.attribute_count+1])
                T.add(sorted_array[1][common.attribute_count+1])
    t_array = []
    for item in T:
        t_array.append(item)
    t_array.sort(reverse=True)
    #if len(t_array) > 0:
        #print t_array
    for i in range(len(t_array)):
        #print("pop %d index: %d" % (len(train_set), t_array[i]))
        train_set.pop(t_array[i])

    for ex in train_set:
        ex.pop()
    return train_set


avg_error = 0.0
run = 100
for time in range(0, run):
    train_data_set = common.read_train_data()
    common.add_noise(train_data_set, 0.25)

    have_tomek = True
    while have_tomek:
        count_before = len(train_data_set)
        train_data_set = tomek(train_data_set)
        count_after = len(train_data_set)
        have_tomek = count_before != count_after

    error_count = 0

    for index in range(len(common.check_data_set)):
        for index_t in range(len(train_data_set)):
            distance = xigama_d_x_y(common.check_data_set[index], train_data_set[index_t])
            train_data_set[index_t].append(distance)
        sorted_array = sorted(train_data_set, key=lambda ex: ex[common.attribute_count + 1], reverse=False)

        category_map = {}
        for category in common.categorys:
            category_map[category] = 0

        for k_i in range(0, k):
            category_map[sorted_array[k_i][common.attribute_count]] = category_map[
                                                                          sorted_array[k_i][common.attribute_count]] + 1

        max_p = 0
        max_key = ''
        for key, value in category_map.items():
            if max_p < value:
                max_key = key
                max_p = value

        # print("%s %s %s" % (common.check_data_set[index], max_key, category_map[max_key]))
        if common.check_data_set[index][common.attribute_count] != max_key:
            error_count = error_count + 1
        for ex in train_data_set:
            ex.pop()
    #print("error: %d/%d error_rate %.1f%%" % (error_count, len(common.check_data_set), error_count*100.0/len(common.check_data_set)))
    avg_error = avg_error + error_count*100.0/len(common.check_data_set)
    print time
print('%d run avg_error_rate: %.1f%%' % (run, avg_error/run))



