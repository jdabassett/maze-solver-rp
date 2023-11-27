from src.maze_solver.models.border import Border
from src.maze_solver.view.primitives import (
    DisjointLines,
    Line,
    NullPrimitive,
    Point,
    Polygon,
    Polyline,
    Primitive,
)


def decompose(border: Border, top_left: Point, square_size: int) -> Primitive:
    """
    Will return instance of square shape based on square border
    :param border:
    :param top_left:
    :param square_size:
    :return: Primitive
    """
    # create 3 other square points
    # uses type hints to specify they are point instances
    top_right: Point = top_left.translate(x=square_size)
    bottom_right: Point = top_left.translate(x=square_size, y=square_size)
    bottom_left: Point = top_left.translate(y=square_size)

    # create line instances for each side of square
    top = Line(top_left, top_right)
    bottom = Line(bottom_left, bottom_right)
    left = Line(top_left, bottom_left)
    right = Line(top_right, bottom_right)

    # if border on 4 sides make Polygon and return instance
    if border is Border.LEFT | Border.TOP | Border.RIGHT | Border.BOTTOM:
        return Polygon(
            [
                top_left,
                top_right,
                bottom_right,
                bottom_left,
            ]
        )
    # if border on 3 sides make Polyline and return instance
    if border is Border.BOTTOM | Border.LEFT | Border.TOP:
        return Polyline(
            [
                bottom_right,
                bottom_left,
                top_left,
                top_right,
            ]
        )
    # if border on 3 sides make Polyline and return instance
    if border is Border.LEFT | Border.TOP | Border.RIGHT:
        return Polyline(
            [
                bottom_left,
                top_left,
                top_right,
                bottom_right,
            ]
        )
    # if border on 3 sides make Polyline and return instance
    if border is Border.TOP | Border.RIGHT | Border.BOTTOM:
        return Polyline(
            [
                top_left,
                top_right,
                bottom_right,
                bottom_left,
            ]
        )
    # if border on 3 sides make Polyline and return instance
    if border is Border.RIGHT | Border.BOTTOM | Border.LEFT:
        return Polyline(
            [
                top_right,
                bottom_right,
                bottom_left,
                top_left,
            ]
        )
    # if border on 2 adjacent sides make Polyline and return instance
    if border is Border.LEFT | Border.TOP:
        return Polyline(
            [
                bottom_left,
                top_left,
                top_right,
            ]
        )
    # if border on 2 adjacent sides make Polyline and return instance
    if border is Border.TOP | Border.RIGHT:
        return Polyline(
            [
                top_left,
                top_right,
                bottom_right,
            ]
        )
    # if border on 2 adjacent sides make Polyline and return instance
    if border is Border.BOTTOM | Border.LEFT:
        return Polyline(
            [
                bottom_right,
                bottom_left,
                top_left,
            ]
        )
    # if border on 2 adjacent sides make Polyline and return instance
    if border is Border.RIGHT | Border.BOTTOM:
        return Polyline(
            [
                top_right,
                bottom_right,
                bottom_left,
            ]
        )
    # if border on 2 non-adjacent sides make DisjointLines and return instance
    if border is Border.LEFT | Border.RIGHT:
        return DisjointLines([left, right])
    # if border on 2 non-adjacent sides make DisjointLines and return instance
    if border is Border.TOP | Border.BOTTOM:
        return DisjointLines([top, bottom])
    # if border on one side return line that was created above
    if border is Border.TOP:
        return top
    # if border on one side return line that was created above
    if border is Border.RIGHT:
        return right
    # if border on one side return line that was created above
    if border is Border.BOTTOM:
        return bottom
    # if border on one side return line that was created above
    if border is Border.LEFT:
        return left
    # if no borders return Null object that still has draw method
    return NullPrimitive()
