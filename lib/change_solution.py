def implement_changes_teacher(solution: dict, undef_var: set, var: list, value: list):
    """Deletes values due to constrain, that teacher could not be in two rooms at the same time."""
    from data.data import rooms
    # unpack data
    teacher_id = value[0]
    time_slot_id = value[1]
    room_id = value[2]

    # generate set of forbidden values
    forbidden = set()
    for room_iter in range(len(rooms)):
        forbidden.add((teacher_id, time_slot_id, room_iter))

    for var_iter in undef_var:
        new_domain = solution[var_iter].difference(forbidden)
        if new_domain == set():  # if empty than return False
            return False
        # if not empty assign to the solution
        solution[var_iter] = new_domain
    return solution


def implement_changes_room(solution: dict, undef_var: set, var: list, value: list):
    """Deletes values due to constrain, that there could not be any other lessons in this room."""

    from data.data import teachers, time_slots
    # unpack data
    teacher_id = value[0]
    time_slot_id = value[1]
    room_id = value[2]

    # generate set of forbidden values
    forbidden = set()
    for teacher_iter in range(len(teachers)):
        forbidden.add((teacher_iter, time_slot_id, room_id))

    # deletes forbidden values
    for var_iter in undef_var:
        new_domain = solution[var_iter].difference(forbidden)
        if new_domain == set():  # if empty than return False
            return False
        # if not empty assign to the solution
        solution[var_iter] = new_domain
    return solution


def implement_changes_group(solution: dict, undef_var: set, var: list, value: list):
    """Deletes values due to constrain, that group could not be in two rooms at the same time."""

    from data.data import teachers, rooms
    # unpack data
    teacher_id = value[0]
    time_slot_id = value[1]
    room_id = value[2]

    # generate set of forbidden values
    forbidden = set()
    for teacher_iter in range(len(teachers)):
        for room_iter in range(len(rooms)):
            forbidden.add((teacher_iter, time_slot_id, room_iter))

    for var_iter in undef_var:
        if var_iter[0] == var[0]:  # if it is the same group
            if var_iter != var:
                new_domain = solution[var_iter].difference(forbidden)
                if new_domain == set():  # if empty than return False
                    return False
                # if not empty assign to the solution
                solution[var_iter] = new_domain

    return solution


def implement_changes(solution, undef_var, var, value):
    """
    Assign to the variable given value.
    Try to delete values due to 3 constrictions:
    1. Group could not be in two rooms at the same time
    2. Teacher could not be in two rooms at the same time
    3. There shouldn't be any other lessons in the same room.
    If domain become empty, return False.
    """
    solution[var] = set([value])
    cur_undef_var = undef_var.difference(var)
    solution = implement_changes_group(solution, cur_undef_var, var, value)
    if not solution:
        return False

    solution = implement_changes_room(solution, cur_undef_var, var, value)
    if not solution:
        return False

    solution = implement_changes_teacher(solution, cur_undef_var, var, value)
    if not solution:
        return False

    return solution