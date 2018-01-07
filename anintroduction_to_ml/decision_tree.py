import math
import common
import numpy as np


class Node:
    def __init__(self, node_type, category, attribute=[0, 0]):
        # 1 positive 0 neg
        self.category = category
        # 1 leaf
        self.node_type = node_type
        self.attribute_index = attribute[0]
        self.attribute_value = attribute[1]

    left_node = None
    right_node = None



#to seprate target in yes or no, which is the category
test_category_index = 1

def cal_entropy(p_pos):
    if p_pos == 1 or p_pos == 0:
        return 0
    else:
        h_t = -p_pos * math.log(p_pos, 2) - (1 - p_pos) * math.log((1 - p_pos), 2)
        return h_t


def cal_entropy_all(train_data):
    p_pos = train_data.count(1) * 1.0 / len(train_data)
    return cal_entropy(p_pos)


def data_input_v(train_data):
    array_input = []
    for i in range(len(train_data)):
        ex = train_data[i][0:common.attribute_count]
        array_input.append(ex)
    ex_v = np.array(array_input)
    return ex_v


#is the category yes or no
def data_target(train_data, category_index):
    array_target = []
    for i in range(len(train_data)):
        category = common.categorys[category_index]
        category_t = train_data[i][common.attribute_count]
        if category == category_t:
            array_target.append(1)
        else:
            array_target.append(0)
    return array_target


def cal_h_below_theta(target_data, index):
    p_pos = target_data[0:index].count(1)*1.0/index
    return cal_entropy(p_pos)


def cal_h_over_theta(target_data, index):
    p_pos = target_data[index:].count(1) * 1.0 / (len(target_data) - index)
    return cal_entropy(p_pos)


def cal_h_theta(train_data, index):
    p_v = np.array([index * 1.0/len(train_data), 1 - index * 1.0/len(train_data)])
    h_below = cal_h_below_theta(train_data, index)
    h_over = cal_h_over_theta(train_data, index)
    theta_v = np.array([h_below, h_over])
    result = np.dot(p_v, theta_v)
    return np.sum(result)


def cal_entropy_add(train_data, index):
    h_theta = []
    theta_index = []
    sorted_array = sorted(train_data, key=lambda ex: ex[index], reverse=False)
    #print sorted_array
    #print len(sorted_array)
    sorted_targets = data_target(sorted_array, test_category_index)
    sorted_targets_v = np.array(sorted_targets)
    entropy = cal_entropy_all(sorted_targets)
    #print entropy
    #print sorted_targets_v

    target = sorted_targets_v[0]
    for i in range(len(sorted_targets_v)):
        if sorted_targets_v[i] != target:
            target = sorted_targets_v[i]
            if sorted_array[i][index] == sorted_array[i - 1][index]:
                h_theta.append(0)
            else:
                h_theta.append(entropy - cal_h_theta(sorted_targets, i))
            theta_index.append(i)
    max_index = theta_index[h_theta.index(max(h_theta))]
    #print max_index
    #print h_theta
    #print theta_index

    return [h_theta, sorted_array[max_index][index]]


def select_attribute(train_data):
    h_theta = []
    entropy = []
    theta = []
    for index in range(0, common.attribute_count):
        temp = cal_entropy_add(train_data, index)
        h_theta.append(temp[0])
        theta.append(temp[1])
        entropy.append(max(temp[0]))
    attribute_index = entropy.index(max(entropy))
    return [attribute_index, theta[attribute_index]]


def separate_train_data(attribute, train_data):
    theta = attribute[1]
    attribute_index = attribute[0]
    train_data_left = []
    train_data_right = []
    for i in range(len(train_data)):
        if train_data[i][attribute_index] < theta:
            train_data_left.append(train_data[i])
        else:
            train_data_right.append(train_data[i])
    return [train_data_left, train_data_right]


def tree_clear(train_data):
    category = common.categorys[test_category_index]
    all_different = True
    all_same = True
    for i in range(len(train_data)):
        category_t = train_data[i][common.attribute_count]
        if category != category_t:
            all_same = False
        else:
            all_different = False
    return [all_different or all_same, all_same]


def make_tree(train_data, node):
    attribute = select_attribute(train_data)
    separated = separate_train_data(attribute, train_data)

    node.node_type = 0
    node.attribute_index = attribute[0]
    node.attribute_value = attribute[1]

    #print '----tree----'
    #print attribute
    #print('seperate %d %d\n-------' % (len(separated[0]), len(separated[1])))
    if len(separated[0]) > 0:
        verify = tree_clear(separated[0])
        if verify[0] is False:
            #print('%s %d' % (verify[0], len(separated[0])))
            child_node = Node(-1, 0)
            node.left_node = child_node
            make_tree(separated[0], child_node)
        else:
            #print('%s %d' % (verify[0], len(separated[0])))
            child_node = Node(1, verify[1] is True and 1 or 0)
            node.left_node = child_node
    #print '-----leaf-----'
    else:
        node.node_type = 1
        node.category = 0
        return
    if len(separated[1]) > 0:
        verify = tree_clear(separated[1])
        if verify[0] is False:
            #print('%s %d' % (verify[0], len(separated[1])))
            child_node = Node(-1, 0)
            node.right_node = child_node
            make_tree(separated[1], child_node)
        else:
            #print('%s %d' % (verify[0], len(separated[1])))
            child_node = Node(1, verify[1] is True and 1 or 0)
            node.right_node = child_node
    #print '-----leaf-----'
    else:
        node.node_type = 1
        node.category = 0
        return
    return


def tree_description(tree):
    if tree.node_type == 0:
        print '-------------'
        print ('node: %d %.1f' % (tree.attribute_index, tree.attribute_value))
        print ('left node:')
        tree_description(tree.left_node)
        print ('right_node')
        tree_description(tree.right_node)
        print '-------------'
    else:
        print '-------------'
        print ('leaf: %s' % (tree.category == 1 and True or False))
        print '-------------'


def data_is_the_category(check_data, node):
    if node.node_type == 0:
        if check_data[node.attribute_index] < node.attribute_value:
            return data_is_the_category(check_data, node.left_node)
        else:
            return data_is_the_category(check_data, node.right_node)
    else:
        return node.category == 1 and True or False


def check(train_data_raw):
    tree = Node(-1, 0)
    make_tree(train_data_raw, tree)
    # tree_description(tree)
    check_data_raw = common.check_data_set
    error_count = 0
    category = common.categorys[test_category_index]
    for data in check_data_raw:
        is_category = data_is_the_category(data, tree)
        category_t = data[common.attribute_count]
        if category != category_t and is_category is True:
            error_count = error_count + 1
        if category == category_t and is_category is False:
            error_count = error_count + 1
    #print('error %d/%d, %.2f%%' % (error_count, len(check_data_raw), error_count*1.0/len(check_data_raw)*100))
    return error_count*1.0/len(check_data_raw)*100


error_rate1 = 0
error_rate2 = 0
error_rate3 = 0
count = 100
for i in range(0, count):
    print i
    train_data_raw = common.read_train_data()
    test_category_index = 0
    error_rate1 = error_rate1 + check(train_data_raw)
    test_category_index = 1
    error_rate2 = error_rate2 + check(train_data_raw)
    test_category_index = 2
    error_rate3 = error_rate3 + check(train_data_raw)

print('error rate %.2f%%' % (error_rate1/count))
print('error rate %.2f%%' % (error_rate2/count))
print('error rate %.2f%%' % (error_rate3/count))