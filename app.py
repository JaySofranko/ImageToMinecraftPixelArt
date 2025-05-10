from flask import Flask, request, jsonify, send_from_directory
import os
from PIL import Image
import numpy as np
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Ensure these directories exist
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'output'
BLOCK_TEXTURES_DIR = 'block_textures_dir'

# Create necessary directories if they don't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Allowed file extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# Example block color dictionary: {'block_name': (R, G, B)}
block_textures_dir = {
    'acacia_log': (103, 96, 86),
    'acacia_log_top': (150, 88, 55),
    'acacia_planks': (168, 90, 50),
    'acacia_trapdoor': (121, 67, 39),
    'amethyst_block': (133, 97, 191),
    'ancient_debris': (95, 63, 55),
    'andesite': (136, 136, 136),
    'azalea_leaves': (70, 89, 34),
    'bamboo_block': (127, 143, 57),
    'bamboo_mosaic': (190, 170, 78),
    'bamboo_planks_side': (193, 173, 80),
    'bamboo_planks_top': (193, 173, 80),
    'barrel_side': (107, 81, 50),
    'basalt_side': (73, 72, 77),
    'bedrock': (85, 85, 85),
    'bee_hive_back': (157, 126, 75),
    'bee_hive_front': (159, 127, 77),
    'bee_hive_with_honey': (167, 131, 73),
    'bee_nest': (183, 141, 76),
    'bee_nest_back': (196, 150, 77),
    'bee_nest_with_honey': (194, 151, 75),
    'birch_log': (216, 214, 209),
    'birch_log_top': (192, 179, 134),
    'birch_planks': (192, 175, 121),
    'birch_trapdoor': (206, 194, 157),
    'black_concrete': (8, 10, 15),
    'black_concrete_powder': (25, 26, 31),
    'black_glazed_terracotta': (67, 30, 32),
    'black_shulker_box_top': (25, 25, 29),
    'blackstone': (42, 35, 40),
    'black_terracotta': (25, 25, 25),
    'black_wool': (20, 21, 25),
    'blast_furnace_back': (107, 107, 107),
    'blast_furnace_front': (107, 107, 107),
    'blue_concrete': (44, 46, 143),
    'blue_concrete2': (51, 76, 178),
    'blue_concrete_powder': (70, 73, 166),
    'blue_glazed_terracotta': (47, 64, 139),
    'blue_ice': (116, 167, 252),
    'blue_shulker_box_top': (43, 45, 140),
    'blue_terracotta': (74, 59, 91),
    'blue_wool': (53, 57, 157),
    'bone_block': (229, 225, 207),
    'bookshelf': (117, 94, 59),
    'brain_coral_block': (207, 91, 159),
    'bricks': (151, 97, 83),
    'brown_concrete': (102, 76, 51),
    'brown_concrete_powder': (125, 84, 53),
    'brown_glazed_terracotta': (119, 106, 85),
    'brown_shulker_box_top': (106, 66, 35),
    'brown_terracotta': (57, 42, 35),
    'brown_wool': (114, 71, 40),
    'bubble_coral_block': (165, 26, 162),
    'budding_amethyst': (132, 96, 186),
    'calcite': (223, 224, 220),
    'cartography_table_front': (70, 50, 34),
    'cartography_table_side': (81, 61, 42),
    'cartography_table_side_blank': (67, 43, 20),
    'carved_pumpkin_front': (150, 84, 17),
    'cauldron_side': (74, 73, 74),
    'cherry_blossom_leaves': (193, 146, 164),
    'cherry_log': (54, 33, 44),
    'cherry_log_top': (184, 140, 136),
    'cherry_planks': (226, 178, 172),
    'cherry_trapdoor': (196, 155, 149),
    'chiseled_bookshelf': (90, 71, 41),
    'chiseled_bookshelf_side': (175, 141, 86),
    'chiseled_copper': (183, 100, 73),
    'chiseled_deepslate': (54, 54, 54),
    'chiseled_nether_bricks': (45, 22, 27),
    'chiseled_polished_blackstone': (53, 48, 56),
    'chiseled_quartz_block': (231, 226, 218),
    'chiseled_red_sandstone': (183, 96, 27),
    'chiseled_resin_bricks': (200, 84, 24),
    'chiseled_sandstone': (216, 203, 155),
    'chiseled_stone_bricks': (119, 118, 119),
    'chorus_flower': (151, 120, 151),
    'clay': (160, 166, 179),
    'coal_block': (16, 15, 15),
    'coal_ore': (105, 105, 105),
    'coarse_dirt': (119, 85, 59),
    'cobbled_deepslate': (77, 77, 80),
    'cobblestone': (127, 127, 127),
    'composter_side': (112, 70, 31),
    'copper_block': (192, 107, 79),
    'copper_bulb': (156, 86, 57),
    'copper_bulb_dot': (156, 86, 57),
    'copper_bulb_powered': (215, 150, 106),
    'copper_bulb_powered_dot': (215, 149, 106),
    'copper_grate': (135, 75, 56),
    'copper_ore': (124, 125, 120),
    'copper_trapdoor': (153, 85, 64),
    'cracked_deepslate_bricks': (44, 37, 43),
    'cracked_deepslate_stone_bricks': (64, 64, 65),
    'cracked_deepslate_tiles': (52, 52, 52),
    'cracked_nether_bricks': (40, 20, 23),
    'cracked_stone_bricks': (118, 117, 118),
    'crafting_table_side': (128, 105, 70),
    'creaking_heart_uprooted': (82, 68, 63),
    'crimson_nylium': (107, 27, 26),
    'crimson_planks': (101, 48, 70),
    'crimson_trapdoor': (87, 42, 61),
    'crying_obsidian': (32, 10, 61),
    'cut_copper': (191, 106, 80),
    'cut_red_sandstone': (189, 101, 31),
    'cut_sandstone': (217, 206, 159),
    'cyan_concrete': (21, 119, 136),
    'cyan_concrete2': (76, 127, 153),
    'cyan_concrete_powder': (36, 147, 157),
    'cyan_glazed_terracotta': (52, 118, 125),
    'cyan_shulker_box_top': (20, 121, 135),
    'cyan_terracotta': (86, 91, 91),
    'cyan_wool': (21, 137, 145),
    'dark_oak_log': (60, 46, 26),
    'dark_oak_log_top': (65, 44, 22),
    'dark_oak_planks': (66, 43, 20),
    'dark_oak_trapdoor': (75, 49, 23),
    'dark_prismarine': (51, 91, 75),
    'dead_brain_coral_block': (124, 117, 114),
    'dead_bubble_coral_block': (131, 123, 119),
    'dead_fire_coral_block': (131, 123, 119),
    'dead_tube_coral_block': (130, 123, 119),
    'deepslate': (80, 80, 82),
    'deepslate_bricks': (48, 42, 49),
    'deepslate_coal_ore': (74, 74, 76),
    'deepslate_copper_ore': (92, 93, 89),
    'deepslate_diamond_ore': (83, 106, 106),
    'deepslate_emerald_ore': (78, 104, 87),
    'deepslate_gold_ore': (115, 102, 78),
    'deepslate_iron_ore': (106, 99, 94),
    'deepslate_lapis_ore': (79, 90, 115),
    'deepslate_redstone_ore': (104, 73, 74),
    'deepslate_stone_bricks': (70, 70, 71),
    'deepslate_tiles': (54, 54, 55),
    'diamond_block': (97, 236, 227),
    'diamond_ore': (121, 141, 140),
    'diorite': (188, 188, 189),
    'dirt': (134, 96, 67),
    'dispenser_face': (122, 121, 121),
    'dripstone_block': (134, 107, 92),
    'dropper_face': (122, 121, 121),
    'emerald_block': (42, 203, 87),
    'emerald_ore': (108, 136, 115),
    'end_stone': (219, 222, 158),
    'endstone_bricks': (218, 224, 162),
    'exposed_chiseled_copper': (154, 119, 100),
    'exposed_copper_block': (161, 125, 103),
    'exposed_copper_bulb': (135, 107, 89),
    'exposed_copper_bulb_dot': (136, 106, 89),
    'exposed_copper_bulb_powered': (193, 145, 100),
    'exposed_copper_bulb_powered_dot': (194, 144, 99),
    'exposed_copper_grate': (114, 88, 73),
    'exposed_copper_trapdoor': (129, 100, 84),
    'exposed_cut_copper': (154, 121, 101),
    'fire_coral_block': (163, 35, 46),
    'fletching_table_side': (173, 155, 111),
    'fletching_table_side2': (191, 166, 129),
    'flowering_azalea_leaves': (80, 89, 49),
    'full_chiseled_bookshelf': (121, 94, 70),
    'furnace_back': (120, 119, 119),
    'furnace_front': (91, 91, 91),
    'gilded_blackstone': (55, 42, 38),
    'glowstone': (170, 130, 84),
    'gold_block': (246, 208, 61),
    'gold_ore': (145, 133, 106),
    'granite': (149, 103, 85),
    'gravel': (131, 127, 126),
    'gray_concrete': (54, 57, 61),
    'gray_concrete2': (76, 76, 76),
    'gray_concrete_powder': (76, 81, 84),
    'gray_glazed_terracotta': (83, 90, 93),
    'gray_shulker_box_top': (55, 58, 62),
    'gray_terracotta': (37, 22, 16),
    'gray_wool': (62, 68, 71),
    'green_concrete': (73, 91, 36),
    'green_concrete2': (102, 127, 51),
    'green_concrete_powder': (97, 119, 44),
    'green_glazed_terracotta': (117, 142, 67),
    'green_shulker_box_top': (79, 100, 31),
    'green_terracotta': (76, 83, 42),
    'green_wool': (84, 109, 27),
    'haybale_side': (166, 136, 38),
    'honey_block': (250, 188, 57),
    'honeycomb_block': (229, 148, 29),
    'horn_coral_block': (215, 199, 65),
    'iron_block': (220, 219, 219),
    'iron_ore': (136, 129, 122),
    'iron_trapdoor': (175, 175, 175),
    'jack_o_lantern': (214, 152, 52),
    'jungle_log': (85, 68, 25),
    'jungle_log_top': (149, 109, 70),
    'jungle_planks': (160, 115, 80),
    'jungle_trapdoor': (129, 93, 65),
    'kelp_side': (38, 48, 29),
    'lapis_block': (30, 67, 140),
    'lapis_ore': (107, 117, 141),
    'light_blue_concrete': (102, 153, 216),
    'light_blue_concrete2': (35, 137, 198),
    'light_blue_concrete_powder': (74, 180, 213),
    'light_blue_glazed_terracotta': (94, 164, 208),
    'light_blue_shulker_box_top': (49, 163, 212),
    'light_blue_terracotta': (113, 108, 138),
    'light_blue_wool': (58, 175, 217),
    'light_gray_concrete': (125, 125, 115),
    'light_gray_concrete2': (153, 153, 153),
    'light_gray_concrete_powder': (154, 154, 148),
    'light_gray_glazed_terracotta': (144, 166, 167),
    'light_gray_shulker_box_top': (124, 124, 115),
    'light_gray_terracotta': (135, 106, 97),
    'light_gray_wool': (142, 142, 134),
    'lime_concrete': (127, 204, 25),
    'lime_concrete2': (94, 168, 24),
    'lime_concrete_powder': (125, 189, 41),
    'lime_glazed_terracotta': (162, 197, 55),
    'lime_shulker_box_top': (99, 172, 22),
    'lime_terracotta': (103, 117, 52),
    'lime_wool': (112, 185, 25),
    'lodestone': (119, 120, 123),
    'loom_front': (148, 118, 82),
    'loom_side': (146, 101, 72),
    'magenta_concret2': (178, 76, 216),
    'magenta_concrete': (169, 48, 159),
    'magenta_concrete_powder': (192, 83, 184),
    'magenta_glazed_terracotta': (208, 100, 191),
    'magenta_shulker_box_top': (173, 54, 163),
    'magenta_terracotta': (149, 88, 108),
    'magenta_wool': (189, 68, 179),
    'mangrove_log': (83, 66, 41),
    'mangrove_log_top': (102, 48, 42),
    'mangrove_planks': (117, 54, 48),
    'mangrove_roots': (68, 58, 48),
    'melon': (114, 146, 30),
    'moss_block': (89, 109, 45),
    'mossy_cobblestone': (110, 118, 94),
    'mossy_stone_bricks': (115, 121, 105),
    'mud': (60, 57, 60),
    'mud_bricks': (137, 103, 79),
    'mushroom_block_inside': (201, 170, 120),
    'mushroom_block_stem': (203, 196, 185),
    'mycelium': (113, 87, 71),
    'nether_bricks': (44, 21, 26),
    'nether_gold_ore': (115, 54, 42),
    'netherite_block': (66, 61, 63),
    'nether_quartz_ore': (117, 65, 62),
    'netherrack': (97, 38, 38),
    'nether_wart_block': (114, 3, 2),
    'noteblock': (88, 58, 40),
    'oak_log': (109, 85, 50),
    'oak_log_top': (151, 121, 72),
    'oak_planks': (162, 130, 78),
    'oak_trapdoor': (108, 86, 49),
    'observer_back': (71, 69, 69),
    'observer_back_powered': (76, 68, 68),
    'observer_face': (103, 103, 103),
    'observer_side': (70, 68, 68),
    'obsidian': (15, 10, 24),
    'ochre_froglight': (245, 233, 181),
    'orange_concrete': (216, 127, 51),
    'orange_concrete2': (224, 97, 0),
    'orange_concrete_powder': (227, 131, 31),
    'orange_glazed_terracotta': (153, 147, 93),
    'orange_shulker_box_top': (234, 106, 8),
    'orange_terracotta': (161, 83, 37),
    'orange_wool': (240, 118, 19),
    'oxidized_chiseled_copper': (83, 161, 132),
    'oxidized_copper_block': (82, 162, 132),
    'oxidized_copper_bulb': (70, 132, 109),
    'oxidized_copper_bulb_dot': (72, 130, 108),
    'oxidized_copper_bulb_powered': (134, 154, 104),
    'oxidized_copper_bulb_powered_dot': (136, 153, 102),
    'oxidized_copper_grate': (57, 113, 92),
    'oxidized_copper_trapdoor': (67, 129, 106),
    'oxidized_cut_copper': (79, 153, 126),
    'packed_ice': (141, 180, 250),
    'pale_oak_log': (87, 77, 75),
    'pale_oak_log_top': (198, 188, 187),
    'pale_oak_planks': (227, 217, 216),
    'pale_oak_trapdoor': (229, 220, 218),
    'pearlescent_froglight': (235, 224, 228),
    'pink_concrete': (213, 101, 142),
    'pink_concrete2': (242, 127, 165),
    'pink_concrete_powder': (228, 153, 181),
    'pink_glazed_terracotta': (235, 154, 181),
    'pink_shulker_box_top': (230, 121, 157),
    'pink_terracotta': (161, 78, 78),
    'pink_wool': (237, 141, 172),
    'piston': (109, 104, 96),
    'podzol': (122, 87, 57),
    'polished_andesite': (132, 134, 133),
    'polished_basalt': (88, 88, 91),
    'polished_blackstone': (53, 48, 56),
    'polished_deepslate': (72, 72, 73),
    'polished_diorite': (192, 192, 194),
    'polished_granite': (154, 106, 89),
    'prismarine_bricks': (99, 171, 158),
    'pumpkin_side': (195, 114, 24),
    'purple_concrete': (100, 31, 156),
    'purple_concrete2': (127, 63, 178),
    'purple_concrete_powder': (131, 55, 177),
    'purple_glazed_terracotta': (109, 47, 152),
    'purple_shulker_box_top': (103, 32, 156),
    'purple_terracotta': (118, 70, 86),
    'purple_wool': (121, 42, 172),
    'purpur_block': (169, 125, 169),
    'purpur_pillar': (171, 129, 171),
    'quartz_block': (235, 229, 222),
    'quartz_bricks': (234, 229, 221),
    'quartz_pillar': (235, 230, 224),
    'raw_copper_block': (154, 105, 79),
    'raw_gold_block': (221, 169, 46),
    'raw_iron_block': (166, 135, 107),
    'red_concrete': (153, 51, 51),
    'red_concrete2': (142, 32, 32),
    'red_concrete_powder': (168, 54, 50),
    'red_glazed_terracotta': (182, 59, 53),
    'red_mushroom_block': (200, 46, 45),
    'red_nether_bricks': (69, 7, 8),
    'red_sand': (190, 102, 33),
    'red_sandstone': (186, 99, 29),
    'red_shulker_box_top': (140, 31, 30),
    'redstone_block': (175, 24, 5),
    'redstone_lamp': (95, 54, 30),
    'redstone_lamp_powered': (142, 101, 60),
    'redstone_ore': (140, 109, 109),
    'red_terracotta': (143, 61, 46),
    'red_wool': (160, 39, 34),
    'resin_block': (217, 99, 25),
    'resin_bricks': (205, 88, 24),
    'respawn_anchor': (39, 23, 63),
    'rooted_dirt': (144, 103, 76),
    'sand': (219, 207, 163),
    'sandstone': (216, 203, 155),
    'sculk_catalyst': (76, 93, 90),
    'shroomlight': (240, 146, 71),
    'shulker_box_top': (139, 96, 139),
    'slime_block': (111, 192, 91),
    'smithing_table_front': (56, 37, 38),
    'smithing_table_side': (55, 35, 35),
    'smoker_back': (102, 91, 75),
    'smoker_front': (87, 75, 58),
    'smooth_basalt': (72, 72, 78),
    'smooth_stone': (158, 158, 158),
    'smooth_stone_slab': (167, 167, 167),
    'snow_block': (248, 254, 254),
    'soul_sand': (81, 62, 50),
    'soul_soil': (75, 57, 46),
    'sponge': (195, 192, 74),
    'spruce_log': (58, 37, 16),
    'spruce_log_top': (105, 80, 46),
    'spruce_planks': (114, 84, 48),
    'spruce_trapdoor': (103, 79, 47),
    'stone': (125, 125, 125),
    'stone_bricks': (122, 121, 122),
    'stripped_acacia_log': (174, 92, 59),
    'stripped_acacia_log_top': (166, 90, 51),
    'stripped_birch_log': (196, 176, 118),
    'stripped_birch_log_top': (191, 171, 116),
    'stripped_cherry_log_side': (215, 145, 148),
    'stripped_cherry_log_top': (220, 164, 157),
    'stripped_crimson_stem': (137, 57, 90),
    'stripped_dark_oak_log': (72, 56, 36),
    'stripped_dark_oak_log_top': (67, 45, 22),
    'stripped_jungle_log': (171, 132, 84),
    'stripped_jungle_log_top': (165, 122, 81),
    'stripped_mangrove_log': (119, 54, 47),
    'stripped_mangrove_log_top': (109, 43, 43),
    'stripped_oak_log': (177, 144, 86),
    'stripped_oak_log_top': (159, 129, 77),
    'stripped_pale_oak_log_top': (235, 226, 225),
    'stripped_pale_oak_wood': (245, 238, 236),
    'stripped_spruce_log': (115, 89, 52),
    'stripped_spruce_log_top': (108, 80, 46),
    'stripped_warped_hyphae': (57, 150, 147),
    'target': (229, 175, 168),
    'terracotta': (152, 94, 67),
    'tnt_side': (182, 88, 83),
    'tube_coral_block': (49, 87, 206),
    'tuff': (108, 109, 102),
    'verdant_froglight': (211, 234, 208),
    'warped_nylium': (72, 61, 59),
    'warped_planks': (42, 104, 99),
    'warped_trapdoor': (37, 94, 88),
    'warped_wart_block': (22, 119, 121),
    'weathered_chiseled_copper': (104, 150, 111),
    'weathered_copper_block': (108, 152, 110),
    'weathered_copper_bulb': (92, 126, 99),
    'weathered_copper_bulb_dot': (94, 125, 98),
    'weathered_copper_bulb_powered': (156, 157, 98),
    'weathered_copper_bulb_powered_dot': (157, 155, 97),
    'weathered_copper_grate': (74, 107, 78),
    'weathered_copper_trapdoor': (87, 123, 88),
    'weathered_cut_copper': (109, 145, 107),
    'wet_sponge': (171, 181, 70),
    'white_concrete': (207, 213, 214),
    'white_concrete2': (255, 255, 255),
    'white_concrete_powder': (225, 227, 227),
    'white_glazed_terracotta': (187, 211, 201),
    'white_shulker_box_top': (215, 220, 220),
    'white_terracotta': (209, 178, 161),
    'white_wool': (233, 236, 236),
    'yellow_concrete': (240, 175, 21),
    'yellow_concrete2': (229, 229, 51),
    'yellow_concrete_powder': (232, 199, 54),
    'yellow_glazed_terracotta': (234, 192, 88),
    'yellow_shulker_box_top': (248, 188, 29),
    'yellow_terracotta': (186, 133, 35),
    'yellow_wool': (248, 197, 39),
}


def closest_block_color(pixel_rgb):
    return min(block_textures_dir.items(),
               key=lambda block: np.linalg.norm(np.array(block[1]) - np.array(pixel_rgb)))[0]


def build_minecraft_image(input_img_path, quality, size):
    # Open the image in RGB mode
    img = Image.open(input_img_path).convert('RGB')

    # Resize image based on the quality value (1 = highest quality, 10 = lowest quality)
    width, height = img.size
    scale_factor = 1 / quality  # Lower quality means smaller image
    new_width = int(width * scale_factor)
    new_height = int(height * scale_factor)

    # Adjust the image size based on the size slider
    scale_size_factor = 1 + (size - 5) * 0.1  # Scale size between 1 and 2 based on the slider
    new_width = int(new_width * scale_size_factor)
    new_height = int(new_height * scale_size_factor)

    img = img.resize((new_width, new_height))

    # Initialize a dictionary to store block counts
    block_counts = {block_name: 0 for block_name in block_textures_dir.keys()}

    # Process the image pixel by pixel
    new_img = Image.new('RGB', (new_width * 16, new_height * 16))
    for y in range(new_height):
        for x in range(new_width):
            pixel = img.getpixel((x, y))
            block_name = closest_block_color(pixel)
            block_counts[block_name] += 1  # Count the blocks

            block_img_path = os.path.join

            # Get the corresponding block image and paste it into the new image
            block_img_path = os.path.join(BLOCK_TEXTURES_DIR, f"{block_name}.png")
            block_img = Image.open(block_img_path).resize((16, 16))
            new_img.paste(block_img, (x * 16, y * 16))

    # Save the processed image
    output_path = os.path.join(OUTPUT_FOLDER, 'pixelart_output.png')
    new_img.save(output_path)

    return output_path, block_counts

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({'success': False, 'message': 'No file part'})

    file = request.files['image']
    quality = int(request.form['quality'])  # Get the quality value from the form
    size = int(request.form['size'])  # Get the size value from the form

    if file.filename == '':
        return jsonify({'success': False, 'message': 'No selected file'})

    if file and file.filename.lower().endswith(tuple(ALLOWED_EXTENSIONS)):
        filename = secure_filename(file.filename)
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)

        # Process the image with Minecraft logic and get block counts
        output_path, block_counts = build_minecraft_image(file_path, quality, size)

        # Prepare the block counts as a sorted list (optional)
        sorted_block_counts = sorted(block_counts.items(), key=lambda x: x[1], reverse=True)

        # Serve the generated image as a static file
        output_image_url = '/static/' + os.path.basename(output_path)  # Adjust if needed

        # Return the block counts along with the image URL
        return jsonify({
            'success': True,
            'image_url': output_image_url,
            'block_counts': sorted_block_counts
        })

    return jsonify({'success': False, 'message': 'Invalid file format'})

if __name__ == '__main__':
    app.run(debug=True)
