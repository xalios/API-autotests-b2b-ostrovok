from datetime import datetime as dt


def is_order_by_ascending(lst: list) -> bool:
    for i in range(len(lst)-1):
        x = dt.strptime(lst[i], '%Y-%m-%d')
        y = dt.strptime(lst[i+1], '%Y-%m-%d')
        if x > y:
            return False
    return True


def is_order_by_descending(lst: list) -> bool:
    for i in range(len(lst)-1):
        x = dt.strptime(lst[i], '%Y-%m-%d')
        y = dt.strptime(lst[i+1], '%Y-%m-%d')
        if x < y:
            return False
    return True

