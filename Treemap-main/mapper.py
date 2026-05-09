""" Construct a treemap.
Author: Cai Burin
Credits:
"""

# Standard Python library modules
import logging
import doctest

# Project modules, provided
import geometry
import display

# Enable logging with log.debug(msg), log.info(msg), etc.
logging.basicConfig()
log = logging.getLogger(__name__)  # Log messages will look like "DEBUG:mapper:msg"
log.setLevel(logging.INFO)   # Change to logging.INFO to suppress debugging messages


# Layout works with integers, floating point numbers, or a mix of the two.
type Real = type[int] | type[float]    # Named type for use in type annotations
type Nest = Real | list[Nest] | dict[ str, Nest] | tuple[str, Nest]


def treemap(values: list[Real], width: int, height: int):
    """Create treemap of values in width x height pixel display
    in Tk interface and in SVG file written to treemap.svg.
    """
    display.init(width, height)
    area = geometry.Rect(geometry.Point(0, 0),
                         geometry.Point(width, height))
    layout(values, area)
    display.wait_close()


def layout(items: Nest, rect: geometry.Rect):
    """Lay elements of items out in rectangle.
    Recursively lays out a nested list of integers
    """
    log.debug(f"Laying out {items} in {rect}")
    if isinstance(items, (int, float)):  # i.e., Real
        display.draw_tile(rect, items)
    elif isinstance(items, list):
            if len(items) == 1:
                layout(items[0], rect)
            if len(items) >= 2:
                left, right = bisect(items) # "right" not used because it is equal to "not" left
                proportion = deep_sum(left) / deep_sum(items)
                left_rect, right_rect = rect.split(proportion)
                ind_break = len(left)
                layout(items[:ind_break], left_rect)
                layout(items[ind_break:], right_rect)
    elif isinstance(items, dict):
        items = list(items.items()) # Turning a dict into a list of tuples
        layout(items, rect)
    elif isinstance(items, tuple):
        key, value = items
        if isinstance(value, (int, float)):
            display.draw_tile(rect, key, value)
        else:
            display.begin_group(rect, key, deep_sum(value))
            layout(value, rect)
            display.end_group()

    else: 
        assert False, f"What have we here? {items}"


def badness(target: Real, candidate: Real) -> Real: 
    """How far is the candidate from the target?"""
    return abs(candidate - target)


def bisect(li: list[Real]) -> tuple[list[Real], list[Real]]:
    """Returns (prefix, suffix) such that prefix+suffix == items
    and abs(sum(prefix) - sum(suffix)) is minimal.
    Breaks tie in favor of earlier split, e.g., bisect([1,5,1]) == ([1], [5, 1]).
    Requires len(items) >= 2, and all elements of items positive.

    >>> bisect([1, 1, 2])  # Perfect balance
    ([1, 1], [2])
    >>> bisect([1.5, 1.5, 3.0])  # Similar, works with floats
    ([1.5, 1.5], [3.0])
    >>> bisect([2.0, 1, 1.0])  # Perfect balance, mixed
    ([2.0], [1, 1.0])
    >>> bisect([1, 2, 1])  # Equally bad either way; split before pivot
    ([1], [2, 1])
    >>> bisect([6, 5, 4, 3, 2, 1])  # Must include element at split
    ([6, 5], [4, 3, 2, 1])
    >>> bisect([1, 2, 3, 4, 5])
    ([1, 2, 3], [4, 5])
    >>> bisect([1, 1, [1, 1]])
    ([1, 1], [[1, 1]])
    >>> bisect([[3, 3], 5, [2, 2], [1, 1, 1]])
    ([[3, 3], 5], [[2, 2], [1, 1, 1]])
    """
    if isinstance(li, dict):
        li = list(li.items())
    assert isinstance(li, list), f"bisect is only for lists, can't split {li}"
    assert len(li) >= 2, f"Cannot bisect {li}; length must be at least 2"
    log.debug(f"Bisecting {li}")
    target = deep_sum(li) / 2
    total = 0
    for i in range(len(li)):
        total += deep_sum(li[i])
        if total > target: 
            break
    if badness(target, deep_sum(li[:i+1])) < badness(target, deep_sum(li[:i])):
        return li[:i+1], li[i+1:]
    return li[:i], li[i:]


def deep_sum(nest: Nest) -> Real:
    """Returns the total of all numbers in the Nest.

    >>> deep_sum(12)
    12
    >>> deep_sum([12, 13, 10])
    35
    >>> deep_sum([[7, 3], [1, [2, 7]], 10])
    30
    >>> deep_sum([[1.0, 2.0], [3, 4]])
    10.0
    >>> deep_sum({ "Cake": { "Chocolate": 10, "Carrot": 4 }, "Ice Cream": 15 })
    29
    """
    if isinstance(nest, dict):
        nest = list(nest.items())
    if isinstance(nest, tuple):
        key, value = nest   # Crashes if len(items) != 2
        return deep_sum(value)
    # Base Case
    if nest == []:
        return 0
    if isinstance(nest, (int, float)):
        return nest
    # Recusive Cases
    if isinstance(nest, list):
        return (deep_sum(nest[0])+ deep_sum(nest[1:]))
    else: 
        assert False, f"Unanticipated type in deep_sum: {nest}"


if __name__ == "__main__":
    doctest.testmod()
