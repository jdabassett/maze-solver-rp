import tempfile
import textwrap
import webbrowser
from dataclasses import dataclass

from src.maze_solver.models.maze import Maze
from src.maze_solver.models.role import Role
from src.maze_solver.models.solution import Solution
from src.maze_solver.models.square import Square
from src.maze_solver.view.decomposer import decompose
from src.maze_solver.view.primitives import Point, Polyline, Rect, Text, tag

# generate dictionary to store strings of emoji characters as values
# use enum constants as keys
# use get method so None is returned if key is missing
ROLE_EMOJI = {
    Role.ENTRANCE: "\N{pedestrian}",
    Role.EXIT: "\N{chequered flag}",
    Role.ENEMY: "\N{ghost}",
    Role.REWARD: "\N{white medium star}",
}

# frozen dataclasses are immutable
@dataclass(frozen=True)
class SVG:
    """
    Class to generate HTML from xml content and open temporary file in browser for viewing.
    """
    xml_content: str

    @property
    def html_content(self) -> str:
        """
        Construct HTML from xml
        :return: HTML as string
        """
        # use dedent to remove leading spaces
        return textwrap.dedent(
            """\
        <!DOCTYPE html>
        <html lang="en">
        <head>
          <meta charset="utf-8">
          <meta name="viewport" content="width=device-width, initial-scale=1">
          <title>SVG Preview</title>
        </head>
        <body>
        {0}
        </body>
        </html>"""
        ).format(self.xml_content)

    def preview(self) -> None:
        """
        Takes xml content from class instance,
        opens a temporary file,
        calls html_content to convert xml to html,
        writes to file,
        and opens browser to display svg.
        :return:
        """
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", suffix=".html", delete=False) as file:
            file.write(self.html_content)
        webbrowser.open(f"file://{file.name}")


@dataclass(frozen=True)
class SVGRenderer:
    square_size: int = 100
    line_width: int = 6

    @property
    def offset(self):
        """
        To accommodate left side cutoff.
        Offset will shift maze to right.
        :return:
        """
        return self.line_width // 2

    def render(self, maze: Maze, solution: Solution | None = None) -> SVG:
        """
        Will create render of maze and pass to SVG class to be displayed
        :param maze:
        :param solution:
        :return:
        """
        # margins around map
        margins = 2 * (self.offset + self.line_width)
        # total width and height with margins based on maze and square size
        width = margins + maze.width * self.square_size
        height = margins + maze.height * self.square_size
        # create and return SVG class
        return SVG(
            # will be pass in template literal into HTML
            tag(
                "svg",
                # maze and solution generated
                self._get_body(maze, solution),
                xmlns="http://www.w3.org/2000/svg",
                stroke_linejoin="round",
                width=width,
                height=height,
                viewBox=f"0 0 {width} {height}",
            )
        )

    def _get_body(self, maze: Maze, solution: Solution | None) -> str:
        """
        Compile maze elements and solution
        Returns string of xml elements
        :param maze:
        :param solution:
        :return: string
        """
        return "".join(
            [
                # create arrow points to exit
                arrow_marker(),
                # create background
                background(),
                # create maze xml elements and unpack list of strings
                *map(self._draw_square, maze),
                # create solution xml element if solution exists
                self._draw_solution(solution) if solution else "",
            ]
        )

    def _draw_square(self, square: Square) -> str:
        """
        Calls all draw methods for each square element
        Returns string of xml square elements for border, walls, exteriors, emojis
        :param square:
        :return:
        """
        # find squares top left point
        top_left: Point = self._transform(square)
        tags = []
        if square.role is Role.EXTERIOR:
            # create and append if exterior
            tags.append(exterior(top_left, self.square_size, self.line_width))
        elif square.role is Role.WALL:
            # otherwise create and append if wall
            tags.append(wall(top_left, self.square_size, self.line_width))
        elif emoji := ROLE_EMOJI.get(square.role):
            # otherwise create and append emoji if special role
            tags.append(label(emoji, top_left, self.square_size // 2))
        # regardless add borders
        tags.append(self._draw_border(square, top_left))
        # compile into string and return
        return "".join(tags)

    def _draw_border(self, square: Square, top_left: Point) -> str:
        """
        Base on square border will return different primitive and call draw method,
        Will return xml element of squares borders
        :param square:
        :param top_left:
        :return:
        """
        return decompose(square.border, top_left, self.square_size).draw(
            stroke_width=self.line_width, stroke="black", fill="none"
        )

    def _draw_solution(self, solution: Solution) -> str:
        """
        Accepts solution
        Return xml element of solution
        :param solution:
        :return:
        """
        # creates Polyline from solution, calls draw, and returns xml of solution
        return Polyline(
            [
                # offsets each point in solution
                self._transform(point, self.square_size // 2)
                for point in solution
            ]
            # creates xml element
        ).draw(
            stroke_width=self.line_width * 2,
            stroke_opacity="50%",
            stroke="red",
            fill="none",
            marker_end="url(#arrow)",
        )

    def _transform(self, square: Square, extra_offset: int = 0) -> Point:
        """
        Converts square into a point representing the squares top left location including offsets
        :param square:
        :param extra_offset:
        :return:
        """
        return Point(
            x=square.column * self.square_size,
            y=square.row * self.square_size,
            # will add offsets and return new point
        ).translate(x=self.offset + extra_offset, y=self.offset + extra_offset)


def arrow_marker() -> str:
    """
    Will return an arrow xml element to render over exit
    :return:
    """
    return tag(
        "defs",
        tag(
            "marker",
            tag(
                "path",
                d="M 0,0 L 10,5 L 0,10 2,5 z",
                fill="red",
                fill_opacity="50%",
            ),
            id="arrow",
            viewBox="0 0 20 20",
            refX="2",
            refY="5",
            markerUnits="strokeWidth",
            markerWidth="10",
            markerHeight="10",
            orient="auto",
        ),
    )


def background() -> str:
    """
    Generate background to maze
    Uses Rect dataclass from primitives
    :return: svg elements as string
    """
    return Rect().draw(width="100%", height="100%", fill="white")


def exterior(top_left: Point, size: int, line_width: int) -> str:
    """
    Based on point and square dimensions will return xml element of exterior square
    :param top_left:
    :param size:
    :param line_width:
    :return:
    """
    return Rect(top_left).draw(
        width=size,
        height=size,
        stroke_width=line_width,
        stroke="none",
        fill="white",
    )


def wall(top_left: Point, size: int, line_width: int) -> str:
    """
    Based on point and square dimensions will return xml element of wall
    :param top_left:
    :param size:
    :param line_width:
    :return:
    """
    return Rect(top_left).draw(
        width=size,
        height=size,
        stroke_width=line_width,
        stroke="none",
        fill="lightgray",
    )


def label(emoji: str, top_left: Point, offset: int) -> str:
    """
    Based on point and square dimensions will return xml element of emoji text
    :param emoji:
    :param top_left:
    :param offset:
    :return:
    """
    return Text(emoji, top_left.translate(x=offset, y=offset)).draw(
        font_size=f"{offset}px",
        text_anchor="middle",
        dominant_baseline="middle",
    )
