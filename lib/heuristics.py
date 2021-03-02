def MRV(solution: dict, undef_var: set):
    list_undef = list(undef_var)
    min_var = list_undef[0]
    min_number_of_values = len(solution[min_var])
    for var in list_undef[1:]:
        cur_len = len(solution[var])
        if min_number_of_values > cur_len:
            min_var = var
            min_number_of_values = cur_len
    return min_var


def Power(solution: dict, undef_var: set):
    for var in undef_var:
        return var


def first_value(var, solution, undef_var):
    return list(solution[var])


def LCV(var: list, solution: dict, undef_var: set):
    def count_reduce_for_var(target_var, var, value):
        target_set = solution[target_var]
        n_reduces = 0
        if var[0] != target_var[0]:
            for target_value in target_set:
                if value[1] == target_value[1] and value[2] == target_value[2]:
                    n_reduces += 1
                else:
                    if value[0] == target_value[0] and value[1] == target_value[1]:
                        n_reduces += 1
        else:
            for target_value in target_set:
                if value[1] == target_value[1]:
                    n_reduces += 1

        return n_reduces

    def count_reduces(value: list):
        total_reduces = 0
        for target_var in undef_var.difference(set([var])):
            total_reduces += count_reduce_for_var(target_var, var, value)
        # print(value," ",total_reduces)
        return total_reduces

    list_values = list(solution[var])
    return sorted(list_values, key=lambda value: count_reduces(value))
