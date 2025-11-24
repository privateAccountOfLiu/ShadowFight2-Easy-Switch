import ast
import csv
import struct

from python.core.core_classes import MoveBin


class Tools:
    @staticmethod
    def animation_serialize(_csv: str) -> MoveBin:
        _result = b''
        header_struct, point_struct, end_byte = struct.Struct('I'), struct.Struct('<3f'), struct.pack('B', 1)
        with open(_csv, 'r') as csv_in:
            _reader, data, num = csv.reader(csv_in), [], 0
            for row in _reader:
                data.append([len(row), [ast.literal_eval(_i) for _i in row]])
                num += 1
        _result += header_struct.pack(num) + end_byte
        for frame in data:
            _result += header_struct.pack(frame[0])
            points_data = b''.join(
                point_struct.pack(*point) for point in frame[1]
            )
            _result += points_data + end_byte
        return MoveBin.build_binary(_result)

    @staticmethod
    def animation_deserialize(_bin: MoveBin) -> str:
        return "\n".join(",".join(str(_i) for _i in frame.points) for i, frame in enumerate(_bin.bin_data))

