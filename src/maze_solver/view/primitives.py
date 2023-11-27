from dataclasses import dataclass
from typing import NamedTuple, Protocol


class Primitive(Protocol):
    """
    Class for type hints that must contain draw method
    """
    def draw(self, **attributes) -> str:
        ...


class NullPrimitive:
    """
    Null object class that must contain draw method
    """
    def draw(self, **attributes) -> str:
        return ""


class Point(NamedTuple):
    """
    Class point to contribute to maze render
    """
    x: int
    y: int

    def draw(self, **attributes) -> str:
        """
        Will return string of point x and y values
        :param attributes:
        :return: string
        """
        return f"{self.x},{self.y}"

    def translate(self, x=0, y=0) -> "Point":
        """
        Input x and y offsets that be used with self to create new Point instance
        :param x:
        :param y:
        :return: Point
        """
        return Point(self.x + x, self.y + y)


class Line(NamedTuple):
    """
    Class line to contribute to maze render
    """
    start: Point
    end: Point

    def draw(self, **attributes) -> str:
        """
        Input self and dictionary of attributes
        Returns xml element of line
        :param attributes:
        :return: xml as string
        """
        return tag(
            "line",
            x1=self.start.x,
            y1=self.start.y,
            x2=self.end.x,
            y2=self.end.y,
            **attributes,
        )


class Polyline(tuple[Point, ...]):
    """
    Polyline are connected lines whose ends might not connect
    """
    def draw(self, **attributes) -> str:
        """
        Input self and dictionary of attributes
        Returns xml element of polyline
        :param attributes:
        :return: xml as string
        """
        points = " ".join(point.draw() for point in self)
        return tag("polyline", points=points, **attributes)


class Polygon(tuple[Point, ...]):
    """
    Polygon is connections of lines that whose ends must connect
    """
    def draw(self, **attributes) -> str:
        """
        Input self and dictionary of attributes
        Returns xml element of line
        :param attributes:
        :return: xml as string
        """
        points = " ".join(point.draw() for point in self)
        return tag("polygon", points=points, **attributes)


class DisjointLines(tuple[Line, ...]):
    """
    DisjointLines used predominantly to render corridors
    """
    def draw(self, **attributes) -> str:
        """
        Input self and dictionary of attributes
        Returns xml element of disjointed lines
        :param attributes:
        :return: xml as string
        """
        return "".join(line.draw(**attributes) for line in self)


@dataclass
class Rect:
    """
    Dataclass to create rectangular objects
    """
    top_left: Point | None = None

    def draw(self, **attributes) -> str:
        """
        Input self and dictionary of attributes
        Returns xml element of rectangle
        :param attributes:
        :return: xml as string
        """
        if self.top_left:
            attrs = attributes | {"x": self.top_left.x, "y": self.top_left.y}
        else:
            attrs = attributes
        return tag("rect", **attrs)


@dataclass(frozen=True)
class Text:
    """
    Immutable dataclass to create text elements of squares
    """
    content: str
    point: Point

    def draw(self, **attributes) -> str:
        """
        Input self and dictionary of attributes
        Returns xml element for text inside square
        :param attributes:
        :return: xml as string
        """
        return tag(
            "text", self.content, x=self.point.x, y=self.point.y, **attributes
        )


def tag(name: str, value: str | None = None, **attributes) -> str:
    """
    Accepts name of xml element
    Can accept string of value contents to place inside xml element
    Can accept dictionary of attributes to be assigned to xml element
    :param name: string
    :param value: string or None
    :param attributes: dictionary
    :return: xml as string
    """
    # will return "" if no attributes
    # if attributes exists, returns string of concatenated attributes
    attrs = (
        ""
        if not attributes
        else " "
        + " ".join(
            f'{key.replace("_", "-")}="{value}"'
            for key, value in attributes.items()
        )
    )
    # adds value contents if they exist
    if value is None:
        return f"<{name}{attrs} />"
    return f"<{name}{attrs}>{value}</{name}>"
