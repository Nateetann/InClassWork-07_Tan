def make_course(code, name, max_students):
    if max_students < 0:
        raise ValueError("Capacity cannot be negative")
    return {"code": code, "name": name, "max_students": max_students, "roster": []}

def is_full(course):
    return len(course["roster"]) >= course["max_students"]

def seats_left(course):
    s = course["max_students"] - len(course["roster"])
    if s < 0:
        s = 0
    return s

def safe_add_student(course, student):
    if is_full(course):
        return False
    i = 0
    while i < len(course["roster"]):
        if course["roster"][i] == student:
            return False
        i += 1
    course["roster"].append(student)
    return True

def bulk_add(course, students):
    added = 0
    i = 0
    while i < len(students):
        if is_full(course):
            break
        ok = safe_add_student(course, students[i])
        if ok:
            added += 1
        i += 1
    return added

def drop_student(course, student):
    i = 0
    while i < len(course["roster"]):
        if course["roster"][i] == student:
            j = i
            while j < len(course["roster"]) - 1:
                course["roster"][j] = course["roster"][j + 1]
                j += 1
            course["roster"].pop()
            return True
        i += 1
    return False

def transfer_student(src, dst, student):
    if not drop_student(src, student):
        return False
    if is_full(dst):
        safe_add_student(src, student)
        return False
    ok = safe_add_student(dst, student)
    if not ok:
        safe_add_student(src, student)
        return False
    return True

def find_course(courses, code):
    i = 0
    while i < len(courses):
        if courses[i]["code"] == code:
            return courses[i]
        i += 1
    return None

def roster_string(course):
    if len(course["roster"]) == 0:
        names = "<empty>"
    else:
        names = ""
        i = 0
        while i < len(course["roster"]):
            names += course["roster"][i]
            if i != len(course["roster"]) - 1:
                names += ", "
            i += 1
    return course["code"] + " (" + course["name"] + "): " + names

def merge_sections(a, b):
    merged_code = a["code"]
    merged_name = a["name"]
    merged_cap = a["max_students"] + b["max_students"]
    union = []
    i = 0
    while i < len(a["roster"]):
        exists = False
        j = 0
        while j < len(union):
            if union[j] == a["roster"][i]:
                exists = True
                break
            j += 1
        if not exists:
            union.append(a["roster"][i])
        i += 1
    i = 0
    while i < len(b["roster"]):
        exists = False
        j = 0
        while j < len(union):
            if union[j] == b["roster"][i]:
                exists = True
                break
            j += 1
        if not exists:
            union.append(b["roster"][i])
        i += 1
    i = 0
    while i < len(union) - 1:
        min_idx = i
        j = i + 1
        while j < len(union):
            if union[j] < union[min_idx]:
                min_idx = j
            j += 1
        if min_idx != i:
            tmp = union[i]
            union[i] = union[min_idx]
            union[min_idx] = tmp
        i += 1
    admitted = []
    num_dropped = 0
    i = 0
    while i < len(union):
        if len(admitted) < merged_cap:
            admitted.append(union[i])
        else:
            num_dropped += 1
        i += 1
    merged = {"code": merged_code, "name": merged_name, "max_students": merged_cap, "roster": admitted}
    return merged, num_dropped

def fill_from_waitlist(course, waitlist):
    added = 0
    while (not is_full(course)) and (len(waitlist) > 0):
        first = waitlist[0]
        k = 0
        while k < len(waitlist) - 1:
            waitlist[k] = waitlist[k + 1]
            k += 1
        waitlist.pop()
        if safe_add_student(course, first):
            added += 1
    return added

print("# Task 1")
fresh = make_course("EECE2560", "Algorithms", 2)
print(safe_add_student(fresh, "A"))
print(safe_add_student(fresh, "B"))
print(safe_add_student(fresh, "C"))
print("Final roster:", fresh["roster"])

print("\n# Task 2")
zero = make_course("EECE0000", "ZeroCap", 0)
print(safe_add_student(zero, "Z"))
print("is_full:", is_full(zero))

print("\n# Task 3")
alg = make_course("EECE2560", "Algorithms", 3)
print(safe_add_student(alg, "Alex"))
print(safe_add_student(alg, "Alex"))
print("Roster now:", alg["roster"])

print("\n# Task 4")
safe_add_student(alg, "Priya")
print("Seats left before:", seats_left(alg))
safe_add_student(alg, "Jordan")
print("Seats left after fill:", seats_left(alg))
print("Roster:", alg["roster"])

print("\n# Task 5")
short = make_course("EECE2140", "CompFund", 2)
long_list = ["A", "B", "C", "D"]
added_count = bulk_add(short, long_list)
print("Added count:", added_count)
print("Final roster:", short["roster"])

print("\n# Task 6")
ds = make_course("EECE2561", "Data Structures", 3)
bulk_add(ds, ["Jordan", "Lee"])
print("Drop Jordan (1):", drop_student(ds, "Jordan"))
print("Roster:", ds["roster"])
print("Drop Jordan (2):", drop_student(ds, "Jordan"))
print("Roster:", ds["roster"])

print("\n# Task 7")
alg = make_course("EECE2560", "Algorithms", 2)
bulk_add(alg, ["Alex", "Priya"])
ds = make_course("EECE2561", "Data Structures", 1)
bulk_add(ds, ["Sam"])
print("Transfer when dst full:", transfer_student(alg, ds, "Alex"))
print("alg roster:", alg["roster"])
print("ds roster:", ds["roster"])
drop_student(ds, "Sam")
print("Transfer when dst not full:", transfer_student(alg, ds, "Alex"))
print("alg roster:", alg["roster"])
print("ds roster:", ds["roster"])

print("\n# Task 8")
courses = [
    make_course("EECE2560", "Algorithms", 2),
    make_course("EECE2561", "Data Structures", 2),
    make_course("EECE2140", "CompFund", 2)
]
found = find_course(courses, "EECE2560")
missing = find_course(courses, "EECE9999")
print("Found EECE2560:", roster_string(found))
print("Missing EECE9999:", missing)

print("\n# Task 9")
alg = make_course("EECE2560", "Algorithms", 2)
bulk_add(alg, ["A", "B"])
print("is_full before:", is_full(alg))
alg["max_students"] = 3
print("is_full after:", is_full(alg))
print("Add one more:", safe_add_student(alg, "C"))
print("Roster:", alg["roster"])
print("Because is_full() reads the dict each time, changing max_students affects fullness immediately.")


print("\n# Task 10")
try:
    bad = make_course("EECEX", "Bad", -1)
    print("Should not print:", bad)
except ValueError as e:
    print("Caught:", str(e))

print("\n# Task 11")
empty = make_course("EECE3000", "EmptyCourse", 2)
print(roster_string(empty))
bulk_add(empty, ["Alex", "Priya"])
print(roster_string(empty))

print("\n# Task 12")
secA = make_course("EECE2560", "Algorithms", 2)
secB = make_course("EECE2560", "Algorithms", 2)
bulk_add(secA, ["Zara", "Alex"])
bulk_add(secB, ["Priya", "Alex"]) 
secA["max_students"] = 1
secB["max_students"] = 1
merged, num_dropped = merge_sections(secA, secB)
print("Merged cap:", merged["max_students"])
print("Merged roster:", merged["roster"])
print("Num dropped:", num_dropped)
print("Admission policy: alphabetical by student name.")


print("\n# Task 13")
alg = make_course("EECE2560", "Algorithms", 3)
wait_alg = ["A", "B", "C", "D"]
print("Before:", alg["roster"], "| wait:", wait_alg)
added = fill_from_waitlist(alg, wait_alg)
print("Added:", added)
print("After:", alg["roster"], "| wait:", wait_alg)
ds = make_course("EECE2561", "Data Structures", 2)
wait_ds = ["J", "K"]
safe_add_student(ds, "I")
print("Before:", ds["roster"], "| wait:", wait_ds)
added = fill_from_waitlist(ds, wait_ds)
print("Added:", added)
print("After:", ds["roster"], "| wait:", wait_ds)

print("\n# Task 14")
c = make_course("EECE9999", "Alias", 1)
safe_add_student(c, "A")
rc = c
rc["max_students"] = 0
print("Bad aliasing demo:", is_full(c))
print("Clearer pattern: return booleans/counts, not the dict itself.")

