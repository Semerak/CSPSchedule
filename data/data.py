from data.generator import *

courses = data_generator_courses()

teachers = data_generator_teachers(courses)

groups = data_generator_groups(courses)

rooms = data_generator_rooms()

time_slots = data_generator_time_slots()
