VEHICLE_CLASSES = [2, 3, 5, 6, 7]

def vehicles_in_result(cls):
    count = 0
    for c in cls:
        if c in VEHICLE_CLASSES:
            count += 1
    return count