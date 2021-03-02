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