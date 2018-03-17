from util import *
import numpy as np
import math


# ========== Helper Function ==========
def small_product(num_arr):
    """
    use the fact that a1 x a2 x ... x ak = exp(log(a1) + log(a2) + ... + log(ak)) to
    compute product of small numbers to prevent underflow
    :param num_arr: a list of small numbers
    :type num_arr: list
    :return: the computed result
    :rtype: float
    """
    logged_num = [math.log(n) for n in num_arr]
    return math.exp(sum(logged_num))


# ========== Naive Bayes ==========
def naive_bayes(train_label, real_dict, fake_dict, test_words, m, p_hat):
    """
    The naive bayes classifier
    :param train_label: the training label
    :type train_label: list
    :param test_words: the test list that contains words
    :type test_words: list
    :param m: number of virtual prior
    :type m: int
    :param p_hat: the virtual prior
    :type p_hat: float
    :return: the label 1 (real) or 0 (fake)
    :rtype: int
    """
    real_count = train_label.count(1)
    fake_count = train_label.count(0)
    total_count = len(train_label)

    # Get priors
    p_real = float(real_count) / float(total_count)
    p_fake = float(fake_count) / float(total_count)

    # Get all words probability (count) P(w | c)
    # P(w | c) = count(word, c) / count(c)
    real_probs, fake_probs = [], []
    for word in test_words:
        if word in real_dict.keys():
            word_real_count = real_dict[word]
        else:
            word_real_count = 0
        if word in fake_dict.keys():
            word_fake_count = fake_dict[word]
        else:
            word_fake_count = 0
        p_word_given_real = (float(word_real_count) + m * p_hat) / float(real_count + m)
        p_word_given_fake = (float(word_fake_count) + m * p_hat) / float(fake_count + m)
        real_probs.append(p_word_given_real)
        fake_probs.append(p_word_given_fake)

    # Get the likelihoods and calculate the probability of test being real and fake
    p_real_likelihood = small_product(real_probs)
    p_real_prob = p_real * p_real_likelihood

    p_fake_likelihood = small_product(fake_probs)
    p_fake_prob = p_fake * p_fake_likelihood

    if p_real_prob >= p_fake_prob:
        return 1
    else:
        return 0


if __name__ == "__main__":
    sets = separate_sets(seed = 0, overwrite = False)
    train_set = sets[TRAIN_SET]
    train_label = sets[TRAIN_LABEL]
    val_set = sets[VAL_SET]
    val_label = sets[VAL_LABEL]
    test_set = sets[TEST_SET]
    test_label = sets[TEST_LABEL]

    real_dict, fake_dict = get_set_word_dict(train_set, train_label)

    m = 1
    p_hat = 0.15
    correct = 0
    # for i in range(len(val_set)):
    #     test_words = val_set[i].split()
    #     result = naive_bayes(train_label, real_dict, fake_dict, test_words, m, p_hat)
    #     if result == val_label[i]:
    #         correct += 1
    # print float(correct) / float(len(val_label))

    test_words = val_set[1].split()
    result = naive_bayes(train_label, real_dict, fake_dict, test_words, m, p_hat)
    print "label: ", val_label[1]
    print "result: ", result
