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
    def generate_capsule_mesh(p1, p2, radius, segments=32, rings=12):
        v, fig = [], []
        ax, ay, az = p1
        bx, by, bz = p2
        dx, dy, dz = bx - ax, by - ay, bz - az
        line = math.sqrt(dx*dx + dy*dy + dz*dz)
        if line < 1e-8: return [], []

        nx, ny, nz = dx/line, dy/line, dz/line

        # 构造局部坐标系
        if abs(nz) > 0.99:
            ux, uy, uz = 1, 0, 0
        else:
            ux, uy, uz = 0, 0, 1
        tx = ny*uz - nz*uy
        ty = nz*ux - nx*uz
        tz = nx*uy - ny*ux
        t_length = math.sqrt(tx*tx + ty*ty + tz*tz)
        if t_length > 1e-8:
            tx /= t_length
            ty /= t_length
            tz /= t_length
        ux = ny*tz - nz*ty
        uy = nz*tx - nx*tz
        uz = nx*ty - ny*tx

        base = len(v)
        step = 2 * math.pi / segments

        # 圆柱侧面
        for i in range(segments):
            c, s = math.cos(i*step), math.sin(i*step)
            ox = (tx * c + ux * s) * radius
            oy = (ty * c + uy * s) * radius
            oz = (tz * c + uz * s) * radius
            v.append((ax + ox, ay + oy, az + oz))
            v.append((bx + ox, by + oy, bz + oz))

        for i in range(segments):
            a = base + i*2
            b = base + (i*2 + 2) % (segments*2)
            c = base + (i*2 + 3) % (segments*2)
            d = base + i*2 + 1
            fig.append((a + 1, b + 1, c + 1))
            fig.append((a + 1, c + 1, d + 1))

        # 底部半球
        v.append(p1)
        center1 = len(v)
        for ring in range(1, rings+1):
            theta = math.pi * ring / (2*rings)
            z = -math.cos(theta)
            r = math.sin(theta)
            for i in range(segments):
                c, s = math.cos(i*step), math.sin(i*step)
                vx = (tx * c + ux * s) * r - nx * z
                vy = (ty * c + uy * s) * r - ny * z
                vz = (tz * c + uz * s) * r - nz * z
                v.append((ax + vx*radius, ay + vy*radius, az + vz*radius))
        ring_start = center1 + 1
        for i in range(segments):
            a = ring_start + (rings-1)*segments + i
            b = ring_start + (rings-1)*segments + (i+1) % segments
            c = base + i*2 + 1
            d = base + (i+1) % segments*2 + 1
            fig.append((center1, a + 1, b + 1))
            fig.append((a + 1, c, d))
            fig.append((a + 1, d, b + 1))

        # 顶部半球（类似）
        v.append(p2)
        center2 = len(v)
        for ring in range(1, rings+1):
            theta = math.pi * ring / (2*rings)
            z = math.cos(theta)
            r = math.sin(theta)
            for i in range(segments):
                c, s = math.cos(i*step), math.sin(i*step)
                vx = (tx * c + ux * s) * r + nx * z
                vy = (ty * c + uy * s) * r + ny * z
                vz = (tz * c + uz * s) * r + nz * z
                v.append((bx + vx*radius, by + vy*radius, bz + vz*radius))
        ring_start = center2 + 1
        for i in range(segments):
            a = ring_start + (rings-1)*segments + i
            b = ring_start + (rings-1)*segments + (i+1) % segments
            c = base + i*2 + 2
            d = base + (i+1) % segments*2 + 2
            fig.append((center2, b + 1, a + 1))
            fig.append((a + 1, d, c))
            fig.append((a + 1, c, b + 1))

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
