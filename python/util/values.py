from python.util.matrix import Matrix, Vector

gap_msg_0 = '<Scene>\n<Nodes>\n'
gap_msg_1 = '</Nodes>\n<Edges>\n'
gap_msg_2 = '</Edges>\n<Figures>\n'
gap_msg_3 = '</Figures>\n</Scene>\n'

error_mes_0 = 'something_wrong:{}-{}'
error_mes_1 = 'the iter length must >= 3 but length %d'
error_mes_2 = 'warning:something_wrong in obj {}-{}'
error_mes_3 = 'warning:please ensure the content of ./bin_dec/output.csv is NULL or WHAT YOU WANT'
error_mes_4 = 'This type is not acceptable'
error_mes_5 = 'object Frame can not mul type except int'
common_mes_0 = 'press Enter to exit:'
common_mes_1 = 'please ensure your range in config.txt:(y/n)'


node_msg = ('<MN{}{} Type="MacroNode" '
            'X="{:.5f}" Y="{:.5f}" Z="{:.5f}" Fixed="0" '
            'Visible="1"  NodesCount="4" '
            'ChildNode1="{}" ChildNode2="{}" ChildNode3="{}" ChildNode4="{}" '
            'LCC1="{:.5f}" LCC2="{:.5f}" LCC3="{:.5f}" LCC4="{:.5f}" />')

edge_msg_0 = ('<MN_Edge-{0}{3} Type="Edge"  Length="1"  WithSign="0"  Fixed="0"  Visible="1"  Selectable="1"  '
              'Node1="MN{0}{1}"  Node2="MN{0}{2}"  Force="100"  SubNodesCount="0"  '
              'End1="MN{0}{1}"  End2="MN{0}{2}" '
              'Radius="{4}" Margin1="0" Margin2="0"/>')
edge_msg_1 = ('<MN_capsule{1} Type="Capsule"  Edge="MN_Edge-{0}{1}"  '
              'Radius1="{2}"  Radius2="{3}"  Margin1="0"  Margin2="0" />')

triangle_msg = '<Triangle{4} Type="Triangle" DoubleSided="-1" Node1="MN{0}{1}" Node2="MN{0}{2}" Node3="MN{0}{3}"/>'

bin_frame_text = '[{}, \n{}]'

type_child_node = {"weapon": {"ChildNode1": "Weapon-Node4_1",
                              "ChildNode2": "Weapon-Node3_1",
                              "ChildNode3": "Weapon-Node2_1",
                              "ChildNode4": "Weapon-Node1_1"},
                   "helm": {"ChildNode1": "NHeadS_1",
                            "ChildNode2": "NHeadF",
                            "ChildNode3": "NHeadS_2",
                            "ChildNode4": "NTop"},
                   "ranged": {"ChildNode1": "Ranged-Node4_1",
                              "ChildNode2": "Ranged-Node3_1",
                              "ChildNode3": "Ranged-Node2_1",
                              "ChildNode4": "Ranged-Node1_1"},
                   "armor_a": {"ChildNode1": "NChestS_2",
                               "ChildNode2": "NChestF",
                               "ChildNode3": "NChestS_1",
                               "ChildNode4": "NNeck"},
                   "armor_b": {"ChildNode1": "NStomachS_2",
                               "ChildNode2": "NStomachF",
                               "ChildNode3": "NStomachS_1",
                               "ChildNode4": "NChest"},
                   "armor_c": {"ChildNode1": "NHip_1",
                               "ChildNode2": "NPelvisF",
                               "ChildNode3": "NHip_2",
                               "ChildNode4": "NStomach"}
                   }

node_msgs = {"Weapon-Node4_1": (78.1888046264648, 204.833297729492, 49.7735557556152),
             "Weapon-Node3_1": (22.1369762420654, 196.383895874023, 92.044059753418),
             "Weapon-Node2_1": (29.3087463378906, 214.682815551758, 46.0688629150391),
             "Weapon-Node1_1": (44.7105293273926, 305.636322021484, 84.6726913452148),
             "NHeadS_1": (-10.0914621353149, 261.223541259766, 6.32387971878052),
             "NHeadS_2": (-32.0835800170898, 261.797760009766, 6.20270729064941),
             "NTop": (-20.5197906494141, 283.477600097656, 7.33019399642944),
             "NHeadF": (-21.1619281768799, 260.979034423828, 17.2502841949463),
             "Ranged-Node4_1": (78.1888046264648, 204.833297729492, 49.7735557556152),
             "Ranged-Node3_1": (22.1369762420654, 196.383895874023, 92.044059753418),
             "Ranged-Node2_1": (29.3087463378906, 214.682815551758, 46.0688629150391),
             "Ranged-Node1_1": (44.7105293273926, 305.636322021484, 84.6726913452148)
             }

node_lcc_basis = {"weapon": Matrix([[-100, -150, -150],
                                    [150, 150, 250],
                                    [0, 0, 0]]),
                  "helm": Matrix([[-0.5241, -11.5921, -0.6701],
                                  [198.7617, 198.6318, 220.6692],
                                  [20.2918, 9.361, 9.1097]]),
                  "ranged": Matrix([[-100, -150, -150],
                                    [150, 150, 250],
                                    [0, 0, 0]]),
                  "armor_a": Matrix([[-3.8997, 7.0358, -4.3955],
                                     [170.7939, 170.5900, 197.3956],
                                     [12.6800, 1.6153, 0.7551]]),
                  "armor_b": Matrix([[-3.9686, 7.2415, -3.9623],
                                     [145.8809, 145.4798, 170.3539],
                                     [13.8250, 3.0438, 1.6926]]),
                  "armor_c": Matrix([[-0.7021, -14.1299, -3.7578],
                                     [122.6197, 122.2297, 145.3073],
                                     [14.0882, 6.2479, 2.8526]])
                  }
node_lcc_ori = {"weapon": Vector([-150, 150, -50]),
                "helm": Vector([10.4073, 198.7080, 9.2236]),
                "ranged": Vector([-150, 150, -50]),
                "armor_a": Vector([-14.9599, 170.2393, 1.7507]),
                "armor_b": Vector([-14.7519, 145.2777, 2.6246]),
                "armor_c": Vector([7.1487, 122.3356, 0.6628])}

basic_bin_bytes = b'\x01\x00\x00\x00\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
