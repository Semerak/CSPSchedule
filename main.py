import lib.heuristics as heuristic
from lib.print_result import print_schedule
from lib.csp import generate_schedule, convert_solution_to_schedule

# Generating input data
from data.data import *


final_solution = generate_schedule(heuristic.MRV, heuristic.first_value, time_slots, rooms, courses, groups, teachers)
if not final_solution:
    print("With this input, there is no solution")
else:
    schedule = convert_solution_to_schedule(final_solution)
    print_schedule(schedule)
