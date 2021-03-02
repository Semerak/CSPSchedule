import lib.heuristics as heuristic
from lib.print_result import print_schedule
from lib.csp import generate_schedule, convert_solution_to_schedule
import time

# Generating input data
from data.data import *

t_start = time.time()
final_solution = generate_schedule(heuristic.Power, heuristic.LCV, time_slots, rooms, courses, groups, teachers)
print("Time: ", time.time() - t_start)


if not final_solution:
    print("With this input, there is no solution")
else:
    schedule = convert_solution_to_schedule(final_solution)
    print_schedule(schedule)

