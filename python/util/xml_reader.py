import math
import xml.etree.ElementTree as Et
from typing import List, Tuple, Dict


class XmlReader:
    @staticmethod
    def _find_edge_by_ref(root: Et.Element, edge_ref: str) -> Et.Element | None:
        for edge in root.findall(".//Edges/*"):
            if edge.get("Edge") == edge_ref:
                return edge
            if edge.tag == edge_ref:
                return edge
            if edge.get("End1") == edge_ref or edge.get("End2") == edge_ref:
                return edge
        return None

    @staticmethod
    def parse_xml_to_obj_data(xml_content: str):
        root = Et.fromstring(xml_content)
        node_positions: Dict[str, Tuple[float, float, float]] = {}
        node_list: List[Tuple[float, float, float]] = []
        node_name_to_index: Dict[str, int] = {}

        for node in root.findall(".//Nodes/*"):
            if node.get("Type") == "MacroNode":
                name = node.tag
                x = float(node.get("X"))
                y = float(node.get("Y"))
                z = float(node.get("Z") or "0")
                node_positions[name] = (x, y, z)
                node_name_to_index[name] = len(node_list) + 1
                node_list.append((x, y, z))

        capsules: List[Tuple[Tuple[float, float, float], Tuple[float, float, float], float]] = []

        for fig in root.findall(".//Figures/*"):
            if fig.get("Type") == "Capsule":
                edge_ref = fig.get("Edge")
                if not edge_ref:
                    continue

                edge_elem = XmlReader._find_edge_by_ref(root, edge_ref)
                if edge_elem is not None:
                    end1_name = edge_elem.get("End1") or edge_elem.get("Node1")
                    end2_name = edge_elem.get("End2") or edge_elem.get("Node2")
                    if end1_name in node_positions and end2_name in node_positions:
                        r1 = float(fig.get("Radius1", 2))
                        r2 = float(fig.get("Radius2", 2))
                        radius = (r1 + r2) / 2.0
                        capsules.append((node_positions[end1_name], node_positions[end2_name], radius))

        triangles = []
        for fig in root.findall(".//Figures/*"):
            if fig.get("Type") == "Triangle":
                n1 = fig.get("Node1")
                n2 = fig.get("Node2")
                n3 = fig.get("Node3")
                if (n1 and n2 and n3 and n1 in node_name_to_index and n2 in node_name_to_index and n3
                        in node_name_to_index):
                    triangles.append((node_name_to_index[n1], node_name_to_index[n2], node_name_to_index[n3]))

        return node_list, capsules, triangles

    @staticmethod
    def generate_capsule_mesh(p1, p2, radius, segments=16, rings=6):
        """
        根据两端点 p1、p2 以及半径生成一段胶囊（圆柱 + 两端球冠）。
        返回值：
            v   : 顶点列表，元素为 (x, y, z)
            fig : 三角面列表，元素为 (i, j, k) —— 已经是 1-based 索引
        """
        v: list[tuple[float, float, float]] = []
        fig: list[tuple[int, int, int]] = []

        ax, ay, az = p1
        bx, by, bz = p2
        dx, dy, dz = bx - ax, by - ay, bz - az
        line = math.sqrt(dx * dx + dy * dy + dz * dz)
        if line < 1e-8:
            return [], []

        # 主轴方向 n（从 p1 指向 p2）
        nx, ny, nz = dx / line, dy / line, dz / line

        # 构造局部正交基 (t, b, n)，其中 t、b 与 n 正交
        if abs(nx) < 0.9:
            rx, ry, rz = 1.0, 0.0, 0.0
        else:
            rx, ry, rz = 0.0, 1.0, 0.0

        # t = normalize(r × n)
        tx = ry * nz - rz * ny
        ty = rz * nx - rx * nz
        tz = rx * ny - ry * nx
        t_len = math.sqrt(tx * tx + ty * ty + tz * tz)
        if t_len < 1e-8:
            return [], []
        tx /= t_len
        ty /= t_len
        tz /= t_len

        # b = n × t
        bx_, by_, bz_ = ny * tz - nz * ty, nz * tx - nx * tz, nx * ty - ny * tx

        def to_world(px, py, pz):
            """将局部坐标 (px, py, pz) 映射到世界坐标。"""
            return (
                ax + px * tx + py * bx_ + pz * nx,
                ay + px * ty + py * by_ + pz * ny,
                az + px * tz + py * bz_ + pz * nz,
            )

        # ----------------------
        # 1. 圆柱侧面
        # ----------------------
        base_cylinder = len(v)
        step_angle = 2 * math.pi / segments

        for i in range(segments):
            ang = i * step_angle
            c, s = math.cos(ang), math.sin(ang)
            # 底圆（局部 z = 0）
            x0, y0, z0 = radius * c, radius * s, 0.0
            # 顶圆（局部 z = line）
            x1, y1, z1 = radius * c, radius * s, line
            v.append(to_world(x0, y0, z0))
            v.append(to_world(x1, y1, z1))

        for i in range(segments):
            a = base_cylinder + i * 2
            b = base_cylinder + ((i * 2 + 2) % (segments * 2))
            c = base_cylinder + ((i * 2 + 3) % (segments * 2))
            d = base_cylinder + i * 2 + 1
            # OBJ 索引 1-based
            fig.append((a + 1, b + 1, c + 1))
            fig.append((a + 1, c + 1, d + 1))

        # ----------------------
        # 2. 底部球冠（中心在 p1）
        # ----------------------
        base_bottom = len(v)
        # 生成 rings-1 个纬圈（不包含极点），再手动加入南极点
        for ring in range(1, rings):
            phi = 0.5 * math.pi * ring / rings  # 0 -> pi/2
            sin_phi = math.sin(phi)
            cos_phi = math.cos(phi)
            for i in range(segments):
                ang = i * step_angle
                c, s = math.cos(ang), math.sin(ang)
                # 底部半球：局部 z 从 0 -> -radius
                px = radius * sin_phi * c
                py = radius * sin_phi * s
                pz = -radius * cos_phi
                v.append(to_world(px, py, pz))

        south_pole_index = len(v)
        v.append(to_world(0.0, 0.0, -radius))

        # 球冠与圆柱之间的接缝：连接最上面一圈到底部圆柱
        if rings > 0:
            ring_top_start = base_bottom + (rings - 2) * segments if rings > 1 else base_bottom
            for i in range(segments):
                next_i = (i + 1) % segments
                v1 = ring_top_start + i
                v2 = ring_top_start + next_i
                c0 = base_cylinder + i * 2  # 对应底部圆柱顶点（z=0）
                c1 = base_cylinder + next_i * 2
                fig.append((c0 + 1, v1 + 1, v2 + 1))
                fig.append((c0 + 1, v2 + 1, c1 + 1))

        # 球冠内部三角面（纬圈之间 + 连接南极）
        for ring in range(rings - 2):
            ring_start = base_bottom + ring * segments
            next_start = ring_start + segments
            for i in range(segments):
                next_i = (i + 1) % segments
                a = ring_start + i
                b = ring_start + next_i
                c_idx = next_start + i
                d_idx = next_start + next_i
                fig.append((a + 1, c_idx + 1, b + 1))
                fig.append((b + 1, c_idx + 1, d_idx + 1))

        # 最下面一圈连南极
        if rings > 1:
            last_ring_start = base_bottom
            for ring in range(rings - 2):
                last_ring_start += segments
            for i in range(segments):
                next_i = (i + 1) % segments
                a = last_ring_start + i
                b = last_ring_start + next_i
                fig.append((south_pole_index + 1, b + 1, a + 1))

        # ----------------------
        # 3. 顶部球冠（中心在 p2）
        # ----------------------
        # 为了复用 to_world，把局部 z 平移到 line + 局部 z
        def to_world_top(px, py, pz):
            return to_world(px, py, line + pz)

        base_top = len(v)
        for ring in range(1, rings):
            phi = 0.5 * math.pi * ring / rings  # 0 -> pi/2
            sin_phi = math.sin(phi)
            cos_phi = math.cos(phi)
            for i in range(segments):
                ang = i * step_angle
                c, s = math.cos(ang), math.sin(ang)
                # 顶部半球：局部 z 从 0 -> +radius
                px = radius * sin_phi * c
                py = radius * sin_phi * s
                pz = radius * cos_phi
                v.append(to_world_top(px, py, pz))

        north_pole_index = len(v)
        v.append(to_world_top(0.0, 0.0, radius))

        # 顶部球冠与圆柱接缝
        if rings > 0:
            ring_top_start = base_top + (rings - 2) * segments if rings > 1 else base_top
            for i in range(segments):
                next_i = (i + 1) % segments
                v1 = ring_top_start + i
                v2 = ring_top_start + next_i
                c0 = base_cylinder + i * 2 + 1  # 顶部圆柱顶点（z=line）
                c1 = base_cylinder + next_i * 2 + 1
                fig.append((c0 + 1, v2 + 1, v1 + 1))
                fig.append((c0 + 1, c1 + 1, v2 + 1))

        # 顶部球冠内部三角面
        for ring in range(rings - 2):
            ring_start = base_top + ring * segments
            next_start = ring_start + segments
            for i in range(segments):
                next_i = (i + 1) % segments
                a = ring_start + i
                b = ring_start + next_i
                c_idx = next_start + i
                d_idx = next_start + next_i
                fig.append((a + 1, b + 1, c_idx + 1))
                fig.append((b + 1, d_idx + 1, c_idx + 1))

        # 顶部最后一圈连北极
        if rings > 1:
            last_ring_start = base_top
            for ring in range(rings - 2):
                last_ring_start += segments
            for i in range(segments):
                next_i = (i + 1) % segments
                a = last_ring_start + i
                b = last_ring_start + next_i
                fig.append((north_pole_index + 1, a + 1, b + 1))

        return v, fig

    @staticmethod
    def generate_obj_string(xml_content: str, capsule_segments: int = 32, capsule_rings: int = 14) -> str:
        node_list, capsules, triangles = XmlReader.parse_xml_to_obj_data(xml_content)

        all_verticals = []
        all_faces = []

        all_verticals.extend(node_list)
        offset = len(all_verticals)

        # 只生成 Type="Capsule" 的胶囊
        for p1, p2, r in capsules:
            v, fig = XmlReader.generate_capsule_mesh(p1, p2, r, capsule_segments, capsule_rings)
            all_verticals.extend(v)
            for face in fig:
                all_faces.append((face[0] + offset, face[1] + offset, face[2] + offset))
            offset += len(v)

        # 三角面
        all_faces.extend(triangles)

        lines = ["# Generated by Tools",
                 "o Xml_Model"]
        for x, y, z in all_verticals:
            lines.append(f"v {x:.6f} {y:.6f} {z:.6f}")
        lines.append("s off")
        for a, b, c in all_faces:
            lines.append(f"f {a} {b} {c}")

        return "\n".join(lines)
