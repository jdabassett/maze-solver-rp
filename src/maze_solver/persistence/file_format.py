import array
# to convert content into c struct binary types
import struct
from dataclasses import dataclass
# for type hinting binary input or output
from typing import BinaryIO

#
MAGIC_NUMBER: bytes = b"MAZE"


@dataclass(frozen=True)
class FileHeader:
    """
    Immutable data-class to create binary file header for maze
    """
    format_version: int
    width: int
    height: int

    @classmethod
    def read(cls, file: BinaryIO) -> "FileHeader":
        """
        Input file name to read header of binary maze file
        Creates and returns instance of class from file header values
        :param file:
        :return:
        """
        assert (
            # raise exception if magic number from file does match global variable
            file.read(len(MAGIC_NUMBER)) == MAGIC_NUMBER
        ), "Unknown file type"
        # always returns tuple
        (format_version,) = struct.unpack("B", file.read(1))
        width, height = struct.unpack("<2I", file.read(2 * 4))
        # create and return new instance
        return cls(format_version, width, height)

    def write(self, file: BinaryIO) -> None:
        """
        Input file name to write header of binary maze file
        :param file:
        :return: None
        """
        # writes magic number to header first to make maze distinct from all other binary files
        file.write(MAGIC_NUMBER)
        # B: unsigned byte
        file.write(struct.pack("B", self.format_version))
        # <: little-endian byte order
        # 2: consecutive values of same type provided
        # I: 32-bit unsigned integer type
        file.write(struct.pack("<2I", self.width, self.height))


@dataclass(frozen=True)
class FileBody:
    """
    Immutable data-class to create binary file body for maze
    """
    square_values: array.array

    @classmethod
    def read(cls, header: FileHeader, file: BinaryIO) -> "FileBody":
        """

        :param header:
        :param file:
        :return:
        """
        return cls(array.array("B", file.read(header.width * header.height)))

    def write(self, file: BinaryIO) -> None:
        """
        Input file name to write body of binary maze file
        :param file:
        :return: None
        """
        file.write(self.square_values.tobytes())
