# InClassWork 07

## Overview
A minimal course-enrollment kernel implemented only with variables, assignments and expressions, selection statements, loops and nested loops, and built-in data structures. The core data model is a dictionary with keys code, name, max_students, and roster where roster is a list of unique student names.

## Functions
make_course, is_full, seats_left, safe_add_student, bulk_add, drop_student, transfer_student, find_course, roster_string, merge_sections, fill_from_waitlist.

## Behavior
Duplicates are rejected by name. bulk_add stops when the course becomes full. drop_student removes exactly one matching name. transfer_student is atomic by reverting the source if the destination add fails. fill_from_waitlist adds in FIFO order. roster_string prints "<empty>" when no students are enrolled.

## Merge policy
merge_sections forms the union of both rosters, sorts names alphabetically with a simple selection sort, sets capacity to the sum of both sections, and admits in alphabetical order until capacity is reached while reporting how many were dropped.

## Capacity changes
Fullness is computed from the dictionary on each call, so changing max_students immediately affects is_full and seats_left.

## Running
Run the single script to print labeled evidence for each task from Task 1 through Task 14. The output screenshots you shared match the expected evidence after adding the overflow example in Task 12 and the brief notes requested in Tasks 9 and 14.
