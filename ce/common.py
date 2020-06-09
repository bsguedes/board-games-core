COLUMN_TO_CASH = [0, 1, 1, 2, 2, 0]
ROWS = ['Top', 'Mid', 'Bot']


def unique(lst):
    last = object()
    for item in lst:
        if item == last:
            continue
        yield item
        last = item


def sort_and_deduplicate(l):
    return list(unique(sorted(l, reverse=True)))
