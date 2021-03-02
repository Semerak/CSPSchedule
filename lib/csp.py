from typing import Callable

import numpy as np

from lib.change_solution import implement_changes


def get_teachers_by_course(teachers, course_id):
    res = []
    for teacher in teachers:
        if course_id in teacher['courses']:
            res.append(teacher['id'])
    return res


def generate_basic_solution(time_slots, rooms, courses, groups, teachers):
    solution = {}
    for group_id in range(len(groups)):
        for course_id in groups[group_id]['courses']:
            for hour_id in range(courses[course_id]["hours"]):
                variable = (group_id, course_id, hour_id)
                domain = set()
                for teacher_id in get_teachers_by_course(teachers, course_id):
                    for time_slot_id in range(len(time_slots)):
                        for room_id in range(len(rooms)):
                            domain.add((teacher_id, time_slot_id, room_id))
                solution[variable] = domain

    return solution


def finder_step(solution: dict, undef_var: set, var_heuristic: Callable, value_heuristic: Callable, level=0):
    """Step in the algorithm solution tree."""
    print(level)
    if undef_var == set():
        print("The end!")
        return solution
    var = var_heuristic(solution, undef_var)
    list_of_values = value_heuristic(var, solution, undef_var)

    # try to do define a value to the variable
    result_solution = False
    for value in list_of_values:  # try to assign a value to the variable

        # try to implement changes. If we got some problems, the result will be false.
        result_solution = implement_changes(solution.copy(), undef_var.difference(set([var])), var, value)

        if result_solution:  # if there was no problem with implementing changes, we can make next step
            # try to do next step
            result_solution = finder_step(result_solution, undef_var.difference(set([var])), var_heuristic,
                                          value_heuristic, level + 1)
            if result_solution:
                # if the result of next steps is not false, we fount the result!
                break
                # if the result is False, we try to assign another value to variable

    return result_solution


def convert_solution_to_schedule(solution):
    from data.data import time_slots, rooms
    schedule = np.full((len(time_slots), len(rooms), 3), -1, dtype=object)
    for var, value in solution.items():
        group_id, course_id, hour_id = var[0], var[1], var[2]

        list_val = list(value)
        if len(list_val) != 1:  # check if we have only 1 value
            return False
        teacher_id, time_slot_id, room_id = list_val[0][0], list_val[0][1], list_val[0][2]

        if schedule[time_slot_id][room_id][1] != -1:  # check if the room with the time slot is free
            return False

        schedule[time_slot_id][room_id] = [np.array([group_id]), teacher_id, course_id]

    return schedule


def generate_schedule(var_heuristic, value_heuristic, time_slots, rooms, courses, groups, teachers):
    """Find a schedule with given heuristics."""
    solution = generate_basic_solution(time_slots, rooms, courses, groups, teachers)
    undef_var = set(solution.keys())
    solution = finder_step(solution, undef_var, var_heuristic, value_heuristic)
    if not solution:
        return False

    return solution
