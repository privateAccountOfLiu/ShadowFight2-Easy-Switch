import ast
import csv
import struct

from python.core.core_classes import MoveBin, Obj, Node, Triangle
from python.util.values import *


class Tools:
    @staticmethod
    def edit_obj_data(obj_p: Obj, set_config: dict) -> Obj:  # 对obj获取到的数据进行处理
        obj_p.standardize_0()
        obj_p.standardize_1()
        obj_p.rotate(set_config['rotate_method'])
        if set_config.get('is_zoom', False):
            obj_p.zoom([set_config['x'], set_config['y'], set_config['z']])
        return obj_p

    @staticmethod
    def model_obj_to_xml(obj_p: Obj, set_config: dict) -> str:
        xml_doc = gap_msg_0
        node_item = ["    " + str(Node(*node, model_type=set_config['type'], node_id=index + set_config['begin_id'])) +
                     '\n'
                     for index, node in enumerate(obj_p.data['v '])]
        triangle_item = ["    " + str(Triangle(node, model_type=set_config['type'], tri_id=index + 1)) + '\n'
                         for index, node in enumerate(obj_p.data['f '])]
        for node in node_item:
            xml_doc += node
        xml_doc += gap_msg_1 + gap_msg_2
        for triangle in triangle_item:
            xml_doc += triangle
        xml_doc += gap_msg_3
        return xml_doc

    @staticmethod
    def animation_serialize(_csv: str) -> MoveBin:
        _result = b''
        header_struct, point_struct, end_byte = struct.Struct('I'), struct.Struct('<3f'), struct.pack('B', 1)
        with open(_csv, 'r', encoding="utf-8") as csv_in:
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
