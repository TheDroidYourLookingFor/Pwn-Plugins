import os
import json
import random
import logging
import toml
import time
import pwnagotchi
import pwnagotchi.plugins as plugins
import pwnagotchi.ui.faces as faces
import pwnagotchi.agent
import pwnagotchi.ui.fonts as fonts
from pwnagotchi.ui.components import LabeledValue
from pwnagotchi.ui.view import BLACK
from datetime import datetime

FACE_LEVELUP = '(≧◡◡≦)'
FACE_NEWACHIEVEMENT = '(≧◡◡≦)'
TAG = "[RPG Plugin]"
FILE_SAVE = "rpg_stats.json"
JSON_KEY_LEVEL = "Level"
JSON_KEY_EXP = "Experience"
JSON_KEY_EXP_TOT = "Experience_total"
JSON_KEY_STRENGTH = "Strength"
JSON_KEY_DEXTERITY = "Dexterity"
JSON_KEY_CONSTITUTION = "Constitution"
JSON_KEY_INTELLIGENCE = "Intelligence"
JSON_KEY_WISDOM = "Wisdom"
JSON_KEY_CHARISMA = "Charisma"
JSON_KEY_LUCK = "Luck"
JSON_KEY_ACHIEVMENTS = "Achievements"
# Stats file variables
JSON_KEY_NUM_HOPS = "num_hops"
JSON_KEY_NUM_PEERS = "num_peers"
JSON_KEY_NUM_DEAUTHS = "num_deauths"
JSON_KEY_NUM_ASSOCIATIONS = "num_associations"
JSON_KEY_NUM_HANDSHAKES = "num_handshakes"
JSON_KEY_NUM_ACCESS_POINTS = "num_access_points"
JSON_KEY_MISSED_INTERACTIONS = "missed_interactions"
JSON_KEY_AVERAGE_BOND = "avg_bond"
JSON_KEY_REWARD = "reward"
JSON_ACCESS_POINTS = "access_points"
# Static Variables
MULTIPLIER_ASSOCIATION = 1
MULTIPLIER_DEAUTH = 2
MULTIPLIER_HANDSHAKE = 3
MULTIPLIER_AI_BEST_REWARD = 5
# Bar Stuff
BAR_SINGLE = '─'
BAR_WALL = '│'
BAR_CORNER = '┌─┐'
BAR_BOTTOM = '└─┘'
BAR_CORNER_TOP_L = '┌'
BAR_CORNER_TOP_R = '┐'
BAR_CORNER_BOT_L = '└'
BAR_CORNER_BOT_R = '┘'
# Define the achievements as a class attribute
ACHIEVEMENTS = {
    "First Level Up": {"condition": "Level == 2", "unlocked": False},
    "Strength 10": {"condition": "Strength >= 10", "unlocked": False},
    "First AP Seen": {"condition": "Num_Access_Points >= 1", "unlocked": False},
    "First Deauth Sent": {"condition": "Num_DeAuths >= 1", "unlocked": False},
}


class RPG(plugins.Plugin):
    __author__ = 'TheDroidUrLookingFor, GaelicThunder, Kaska89, Rai, JayofElony, & Terminator'
    __version__ = '1.0.0'
    __license__ = 'MIT'
    __description__ = 'This is my attempt at writing a fun plugin for the pwnagotchi using the Six Stat system with Luck included.'

    # Attention number masking
    def LogInfo(self, text):
        logging.info(TAG + " " + text)

    # Attention number masking
    def LogDebug(self, text):
        logging.debug(TAG + " " + text)

    def __init__(self):
        self.LogInfo('Starting up!')
        self.options = {
            'exp_bar_symbols_count': 12,
            'label_padding': 22,
            'box_symbol': '_',
            'box_side_symbol': '|',
            'stat_box_side_vertical_spacing': 15,
            'stat_box_wall_height': 6,
            'stat_box_divider_height': 3,
            'stat_box_top_x_coord': 0,
            'stat_box_top_y_coord': 95,
            'stat_box_top_length': 20,
            'stat_box_bottom_x_coord': 0,
            'stat_box_bottom_y_coord': 185,
            'stat_box_bottom_length': 20,
            'stat_box_age_x_coord': 0,
            'stat_box_age_y_coord': 112,
            'stat_box_age_length': 20,
            'stat_box_stats_x_coord': 0,
            'stat_box_stats_y_coord': 156,
            'stat_box_stats_length': 20,
            'stat_box_luck_x_coord': 0,
            'stat_box_luck_y_coord': 170,
            'stat_box_luck_length': 20,
            'stat_box_side_left_x_coord': -4,
            'stat_box_side_left_y_coord': 110,
            'stat_box_center_x_coord': 82,
            'stat_box_center_y_coord': 126,
            'stat_box_side_right_x_coord': 180,
            'stat_box_side_right_y_coord': 110,
            'age_label_padding': 22,
            'age_x_coord': 13,
            'age_y_coord': 111,
            'exp_x_coord': 275,
            'exp_y_coord': 242,
            'exp_label_padding': 5,
            'level_label_padding': 5,
            'level_x_coord': 410,
            'level_y_coord': 242,
            'str_x_coord': 3,
            'str_y_coord': 128,
            'dex_x_coord': 3,
            'dex_y_coord': 143,
            'con_x_coord': 3,
            'con_y_coord': 158,
            'int_x_coord': 90,
            'int_y_coord': 128,
            'wis_x_coord': 90,
            'wis_y_coord': 143,
            'cha_x_coord': 90,
            'cha_y_coord': 158,
            'luck_x_coord': 55,
            'luck_y_coord': 172,
            'assoc_label_padding': 5,
            'asc_x_coord': 1,
            'asc_y_coord': 186,
            'deauth_label_padding': 5,
            'deauth_x_coord': 70,
            'deauth_y_coord': 186
        }
        self.Access_Points = {
            "count": 0,
            "macs": set()
        }
        # Calculate stats and level?
        self.calculateInitialXP = False
        self.Show_Reward_Window = False
        self.Show_Achievement_Window = True
        self.Show_Achievement_Duration = 20
        self.Show_Achievement_Timer = time.time()
        self.Last_Achievement_Header = "Started Pwn-RPG!"
        self.Last_Achievement_Body = "You started the best RPG\n plugin for the pwnagotchi,\n thanks for checking out\n this project!"
        self.Age = '0y 0w 0d'
        self.Level = 1
        # 6 Stat + Luck System
        self.Strength = 1
        self.Dexterity = 1
        self.Constitution = 1
        self.Intelligence = 1
        self.Wisdom = 1
        self.Charisma = 1
        self.Luck = 1
        # Session Stats Info
        self.Num_Hops = 0
        self.Num_Peers = 0
        self.Num_DeAuths = 0
        self.Num_Associations = 0
        self.Num_Handshakes = 0
        self.Missed_Interactions = 0
        self.Average_Bond = 0
        self.Reward = 0
        # Other Stuff
        self.Num_Access_Points = 0
        self.train_epochs = 0
        self.device_start_time = datetime.now()
        self.Experience = 0
        self.Experience_total = self.calcActualSum(self.Level, self.Experience)
        self.Experience_needed = 0
        self.Experience_percent = 0
        self.Achievements = ACHIEVEMENTS
        # Save stuff
        self.save_file = self.getSaveFileName()

        self.LogInfo('Checking for save file.')
        # Create save file
        if not os.path.exists(self.save_file):
            self.Save(self.save_file)
        else:
            try:
                # Try loading
                self.Load(self.save_file)
            except:
                # Likely throws an exception if json file is corrupted, so we need to calculate from scratch
                self.calculateInitialXP = True

        self.LogInfo('Checking save file data.')
        # No previous data, try get it
        if self.Level == 1 and self.Experience == 0:
            self.calculateInitialXP = True
        if self.Experience_total == 0:
            self.LogInfo("Need to calculate Total Exp")
            self.Experience_total = self.calcActualSum(
                self.Level, self.Experience)
            self.Save(self.save_file)

        self.Experience_needed = self.calcExpNeeded(self.Level)
        self.LogInfo('Finished loading data and starting Pwn-RPG!')

    def getSaveFileName(self):
        file = os.path.dirname(os.path.realpath(__file__))
        file = file + "/" + FILE_SAVE
        return file

    # TODO: one day change save file mode to file date
    def Load(self, file):
        self.LogDebug('Loading Exp')
        self.loadFromJsonFile(file)

    def Save(self, file):
        self.LogDebug('Saving Exp')
        self.saveToJsonFile(file)

    def ensure_positive(self, value):
        return max(value, 1)

    def loadFromJsonFile(self, file):
        data = {}
        try:
            with open(file, 'r') as f:
                data = json.loads(f.read())

            if data:
                self.LogInfo("Loaded JSON file")
                self.Level = data[JSON_KEY_LEVEL]
                self.Experience = data[JSON_KEY_EXP]
                self.Experience_total = data[JSON_KEY_EXP_TOT]
                self.Strength = self.ensure_positive(data[JSON_KEY_STRENGTH])
                self.Dexterity = self.ensure_positive(data[JSON_KEY_DEXTERITY])
                self.Constitution = self.ensure_positive(
                    data[JSON_KEY_CONSTITUTION])
                self.Intelligence = self.ensure_positive(
                    data[JSON_KEY_INTELLIGENCE])
                self.Wisdom = self.ensure_positive(data[JSON_KEY_WISDOM])
                self.Charisma = self.ensure_positive(data[JSON_KEY_CHARISMA])
                self.Luck = self.ensure_positive(data[JSON_KEY_LUCK])
                self.Achievements = data[JSON_KEY_ACHIEVMENTS]
                self.Num_Hops = data[JSON_KEY_NUM_HOPS]
                self.Num_Peers = data[JSON_KEY_NUM_PEERS]
                self.Num_Associations = data[JSON_KEY_NUM_ASSOCIATIONS]
                self.Num_DeAuths = data[JSON_KEY_NUM_DEAUTHS]
                self.Num_Handshakes = data[JSON_KEY_NUM_HANDSHAKES]
                self.Num_Access_Points = data[JSON_KEY_NUM_ACCESS_POINTS]
                self.Missed_Interactions = data[JSON_KEY_MISSED_INTERACTIONS]
                self.Average_Bond = data[JSON_KEY_AVERAGE_BOND]
                self.Reward = data[JSON_KEY_REWARD]
                # self.Access_Points = data[JSON_ACCESS_POINTS]
            else:
                self.LogInfo("Empty JSON file")
        except FileNotFoundError:
            self.LogInfo(f"File not found: {file}")
        except json.JSONDecodeError:
            self.LogInfo(f"Error decoding JSON from file: {file}")

    def saveToJsonFile(self, file):
        data = {
            JSON_KEY_LEVEL: self.Level,
            JSON_KEY_EXP: self.Experience,
            JSON_KEY_EXP_TOT: self.Experience_total,
            JSON_KEY_STRENGTH: self.ensure_positive(self.Strength),
            JSON_KEY_DEXTERITY: self.ensure_positive(self.Dexterity),
            JSON_KEY_CONSTITUTION: self.ensure_positive(self.Constitution),
            JSON_KEY_INTELLIGENCE: self.ensure_positive(self.Intelligence),
            JSON_KEY_WISDOM: self.ensure_positive(self.Wisdom),
            JSON_KEY_CHARISMA: self.ensure_positive(self.Charisma),
            JSON_KEY_LUCK: self.ensure_positive(self.Luck),
            JSON_KEY_ACHIEVMENTS: self.Achievements,
            JSON_KEY_NUM_HOPS: self.Num_Hops,
            JSON_KEY_NUM_PEERS: self.Num_Peers,
            JSON_KEY_NUM_DEAUTHS: self.Num_DeAuths,
            JSON_KEY_NUM_ASSOCIATIONS: self.Num_Associations,
            JSON_KEY_NUM_HANDSHAKES: self.Num_Handshakes,
            JSON_KEY_NUM_ACCESS_POINTS: self.Num_Access_Points,
            JSON_KEY_MISSED_INTERACTIONS: self.Missed_Interactions,
            JSON_KEY_AVERAGE_BOND: self.Average_Bond,
            JSON_KEY_REWARD: self.Reward
            # JSON_ACCESS_POINTS: self.Access_Points
        }
        try:
            with open(file, 'w') as f:
                f.write(json.dumps(data, sort_keys=True,
                        indent=4, separators=(',', ': ')))
                self.LogInfo("Saved JSON file")
        except IOError as e:
            self.LogInfo(f"Error saving to file: {file}, {e}")

    def on_loaded(self):
        self.LogInfo("Began loading Pwnagotchi Data")
        data_path = '/root/brain.json'
        self.load_data(data_path)
        config = self._read_config()
        if config:
            self.options.update(config)
        if not self.device_start_time:
            self.device_start_time = datetime.now()
        self.LogInfo("Finished loading Pwnagotchi Data!")

    def _read_config(self):
        try:
            with open('/etc/pwnagotchi/config.toml', 'r') as f:
                config = toml.load(f)
                return config.get('main', {}).get('plugins', {}).get('Pwn-RPG', {})
            self.LogInfo("Read config.toml file!")
        except FileNotFoundError:
            logging.warning("Config file not found, using default options")
            return {}
        except toml.TomlDecodeError:
            logging.error(
                "Error parsing the config file, using default options")
            return {}

    def generate_stat_box_text(self, length):
        return self.options["box_symbol"] * length

    def draw_box(self, box_width, box_height):
        # Create the border strings
        top_border = BAR_CORNER_TOP_L + BAR_SINGLE * \
            (box_width - 2) + BAR_CORNER_TOP_R
        bottom_border = BAR_CORNER_BOT_L + BAR_SINGLE * \
            (box_width - 2) + BAR_CORNER_BOT_R

        middle_row = ''
        if box_height >= 2:
            for i in range(box_height):
                build_string = BAR_WALL + ' ' * (box_width - 2) + BAR_WALL
                if i != box_height:
                    build_string += "\n"
                middle_row += build_string
        elif box_height == 1:
            middle_row = BAR_WALL + ' ' * (box_width - 2) + BAR_WALL + "\n"
        else:
            middle_row = ''

        # Combine all rows
        if box_height == 0:
            bordered_string = f"{top_border}\n{bottom_border}"
        else:
            bordered_string = f"{top_border}\n{middle_row}{bottom_border}"

        return bordered_string

    def generate_achievement_box_draw(self, ui):
        self.achievement_start_time = time.time()
        box_achmain_x_coord = int(176)
        box_achmain_y_coord = int(104)
        box_header_x_coord = int(176)
        box_header_y_coord = int(121)
        box_body_x_coord = int(176)
        box_body_y_coord = int(138)
        main_ach_text_x_coord = int(195)
        main_ach_text_y_coord = int(115)
        header_text_x_coord = int(195)
        header_text_y_coord = int(132)
        body_text_x_coord = int(170)
        body_text_y_coord = int(145)
        box_header_width = int(20)
        box_header_height = int(0)
        box_body_width = int(20)
        box_body_height = int(2)
        box_string_ach_header = self.draw_box(
            box_header_width, box_header_height)
        ui.add_element('Achievement_Main', LabeledValue(color=BLACK, label='', value=box_string_ach_header, position=(
            box_achmain_x_coord, box_achmain_y_coord), label_font=fonts.Bold, text_font=fonts.Medium))
        ui.add_element('Achievement_Main_Text', LabeledValue(color=BLACK, label='', value='Latest Achievement', position=(
            main_ach_text_x_coord, main_ach_text_y_coord), label_font=fonts.Bold, text_font=fonts.BoldSmall, label_spacing=int(self.options["label_padding"])))
        box_string = self.draw_box(box_header_width, box_header_height)
        ui.add_element('Achievement_Header', LabeledValue(color=BLACK, label='', value=box_string, position=(
            box_header_x_coord, box_header_y_coord), label_font=fonts.Bold, text_font=fonts.Medium))
        ui.add_element('Achievement_Header_Text', LabeledValue(color=BLACK, label='', value=self.Last_Achievement_Header, position=(
            header_text_x_coord, header_text_y_coord), label_font=fonts.BoldSmall, text_font=fonts.BoldSmall, label_spacing=int(self.options["label_padding"])))
        box_string_2 = self.draw_box(box_body_width, box_body_height)
        ui.add_element('Achievement_Body', LabeledValue(color=BLACK, label='', value=box_string_2, position=(
            box_body_x_coord, box_body_y_coord), label_font=fonts.Bold, text_font=fonts.Medium))
        ui.add_element('Achievement_Body_Text', LabeledValue(color=BLACK, label='', value=self.Last_Achievement_Body, position=(
            body_text_x_coord, body_text_y_coord), label_font=fonts.BoldSmall, text_font=fonts.BoldSmall, label_spacing=int(self.options["label_padding"])))

    def on_ui_setup(self, ui):
        self.generate_achievement_box_draw(ui)
        # Draw the box elements
        ui.add_element('Stat_Box_Top', LabeledValue(color=BLACK, label=self.generate_stat_box_text(self.options['stat_box_top_length']), position=(int(
            self.options["stat_box_top_x_coord"]), int(self.options["stat_box_top_y_coord"])), label_font=fonts.Bold, text_font=fonts.Medium))

        ui.add_element('Stat_Box_Bottom', LabeledValue(color=BLACK, label=self.generate_stat_box_text(self.options['stat_box_bottom_length']), position=(int(
            self.options["stat_box_bottom_x_coord"]), int(self.options["stat_box_bottom_y_coord"])), label_font=fonts.Bold, text_font=fonts.Medium))

        ui.add_element('Stat_Box_Age', LabeledValue(color=BLACK, label=self.generate_stat_box_text(self.options['stat_box_age_length']), position=(int(
            self.options["stat_box_age_x_coord"]), int(self.options["stat_box_age_y_coord"])), label_font=fonts.Bold, text_font=fonts.Medium))

        ui.add_element('Stat_Box_Stats', LabeledValue(color=BLACK, label=self.generate_stat_box_text(self.options['stat_box_stats_length']), position=(int(
            self.options["stat_box_stats_x_coord"]), int(self.options["stat_box_stats_y_coord"])), label_font=fonts.Bold, text_font=fonts.Medium))

        ui.add_element('Stat_Box_Luck', LabeledValue(color=BLACK, label=self.generate_stat_box_text(self.options['stat_box_luck_length']), position=(int(
            self.options["stat_box_luck_x_coord"]), int(self.options["stat_box_luck_y_coord"])), label_font=fonts.Bold, text_font=fonts.Medium))

        # Draw vertical lines on the left side of the box
        for i in range(self.options["stat_box_wall_height"]):
            ui.add_element(f'Stat_Box_Side_Left_{i+1}', LabeledValue(color=BLACK, label=self.options["box_side_symbol"], position=(int(self.options["stat_box_side_left_x_coord"]), int(
                self.options["stat_box_side_left_y_coord"]) + i * int(self.options["stat_box_side_vertical_spacing"])), label_font=fonts.Bold, text_font=fonts.Medium))

        # Draw vertical lines in the center of the box
        for i in range(self.options["stat_box_divider_height"]):
            ui.add_element(f'Stat_Box_Center_{i+1}', LabeledValue(color=BLACK, label=self.options["box_side_symbol"], position=(int(self.options["stat_box_center_x_coord"]), int(
                self.options["stat_box_center_y_coord"]) + i * int(self.options["stat_box_side_vertical_spacing"])), label_font=fonts.Bold, text_font=fonts.Medium))

        # Draw vertical lines on the right side of the box
        for i in range(self.options["stat_box_wall_height"]):
            ui.add_element(f'Stat_Box_Side_Right_{i+1}', LabeledValue(color=BLACK, label=self.options["box_side_symbol"], position=(int(self.options["stat_box_side_right_x_coord"] - 5), int(
                self.options["stat_box_side_right_y_coord"]) + i * int(self.options["stat_box_side_vertical_spacing"])), label_font=fonts.Bold, text_font=fonts.Medium))

        ui.add_element('Age', LabeledValue(color=BLACK, label='▸ Age', value='',
                                           position=(int(self.options["age_x_coord"]),
                                                     int(self.options["age_y_coord"])),
                                           label_font=fonts.Bold, text_font=fonts.Medium, label_spacing=int(self.options["age_label_padding"])))
        ui.add_element('Level', LabeledValue(color=BLACK, label='Lvl', value=0,
                                             position=(int(self.options["level_x_coord"]),
                                                       int(self.options["level_y_coord"])),
                                             label_font=fonts.Bold, text_font=fonts.Medium, label_spacing=int(self.options["level_label_padding"])))
        ui.add_element('Strength', LabeledValue(color=BLACK, label='⚔Str', value=0,
                                                position=(int(self.options["str_x_coord"]),
                                                          int(self.options["str_y_coord"])),
                                                label_font=fonts.Bold, text_font=fonts.Medium, label_spacing=int(self.options["label_padding"])))
        ui.add_element('Dexterity', LabeledValue(color=BLACK, label='⚡Dex', value=0,
                                                 position=(int(self.options["dex_x_coord"]),
                                                           int(self.options["dex_y_coord"])),
                                                 label_font=fonts.Bold, text_font=fonts.Medium, label_spacing=int(self.options["label_padding"])))
        ui.add_element('Constitution', LabeledValue(color=BLACK, label='♥Con', value=0,
                                                    position=(int(self.options["con_x_coord"]),
                                                              int(self.options["con_y_coord"])),
                                                    label_font=fonts.Bold, text_font=fonts.Medium, label_spacing=int(self.options["label_padding"])))
        ui.add_element('Intelligence', LabeledValue(color=BLACK, label='★Int', value=0,
                                                    position=(int(self.options["int_x_coord"]),
                                                              int(self.options["int_y_coord"])),
                                                    label_font=fonts.Bold, text_font=fonts.Medium, label_spacing=int(self.options["label_padding"])))
        ui.add_element('Wisdom', LabeledValue(color=BLACK, label='☆Wis', value=0,
                                              position=(int(self.options["wis_x_coord"]),
                                                        int(self.options["wis_y_coord"])),
                                              label_font=fonts.Bold, text_font=fonts.Medium, label_spacing=int(self.options["label_padding"])))
        ui.add_element('Charisma', LabeledValue(color=BLACK, label='☀Cha', value=0,
                                                position=(int(self.options["cha_x_coord"]),
                                                          int(self.options["cha_y_coord"])),
                                                label_font=fonts.Bold, text_font=fonts.Medium, label_spacing=int(self.options["label_padding"])))
        ui.add_element('Luck', LabeledValue(color=BLACK, label='☂Luck', value=0,
                                            position=(int(self.options["luck_x_coord"]),
                                                      int(self.options["luck_y_coord"])),
                                            label_font=fonts.Bold, text_font=fonts.Medium, label_spacing=int(self.options["label_padding"])))
        ui.add_element('Associations', LabeledValue(color=BLACK, label='⚙A', value=0,
                                                    position=(int(self.options["asc_x_coord"]),
                                                              int(self.options["asc_y_coord"])),
                                                    label_font=fonts.Bold, text_font=fonts.Medium, label_spacing=int(self.options["assoc_label_padding"])))
        ui.add_element('Deauths Sent', LabeledValue(color=BLACK, label='✖D', value=0,
                                                    position=(int(self.options["deauth_x_coord"]),
                                                              int(self.options["deauth_y_coord"])),
                                                    label_font=fonts.Bold, text_font=fonts.Medium, label_spacing=int(self.options["deauth_label_padding"])))
        ui.add_element('Experience', LabeledValue(color=BLACK, label='Exp', value=0,
                                                  position=(int(self.options["exp_x_coord"]),
                                                            int(self.options["exp_y_coord"])),
                                                  label_font=fonts.Bold, text_font=fonts.Medium, label_spacing=int(self.options["exp_label_padding"])))

    def on_unload(self, ui):
        with ui._lock:
            ui.remove_element('Stat_Box_Top')
            ui.remove_element('Stat_Box_Bottom')
            ui.remove_element('Stat_Box_Side_Left_1')
            ui.remove_element('Stat_Box_Side_Left_2')
            ui.remove_element('Stat_Box_Side_Left_3')
            ui.remove_element('Stat_Box_Side_Left_4')
            ui.remove_element('Stat_Box_Side_Left_5')
            ui.remove_element('Stat_Box_Side_Left_6')
            ui.remove_element('Stat_Box_Side_Right_1')
            ui.remove_element('Stat_Box_Side_Right_2')
            ui.remove_element('Stat_Box_Side_Right_3')
            ui.remove_element('Stat_Box_Side_Right_4')
            ui.remove_element('Stat_Box_Side_Right_5')
            ui.remove_element('Stat_Box_Side_Right_6')
            ui.remove_element('Age')
            ui.remove_element('Level')
            ui.remove_element('Strength')
            ui.remove_element('Dexterity')
            ui.remove_element('Constitution')
            ui.remove_element('Intelligence')
            ui.remove_element('Wisdom')
            ui.remove_element('Charisma')
            ui.remove_element('Luck')
            ui.remove_element('Associations')
            ui.remove_element('Deauths Sent')
            ui.remove_element('Experience')
            ui.remove_element('Achievement_Main')
            ui.remove_element('Achievement_Header')
            ui.remove_element('Achievement_Body')
            ui.remove_element('Achievement_Header_Text')
            ui.remove_element('Achievement_Body_Text')
            ui.remove_element('Achievement_Main_Text')

    def remove_achievement_box(self, ui):
        ui.set('Achievement_Main', '')
        ui.set('Achievement_Header', '')
        ui.set('Achievement_Body', '')
        ui.set('Achievement_Header_Text', '')
        ui.set('Achievement_Body_Text', '')
        ui.set('Achievement_Main_Text', '')
        self.Show_Achievement_Window = False
        self.achievement_start_time = None

    def show_achievement_box(self, ui):
        if not self.Show_Achievement_Window:
            box_header_width = int(20)
            box_header_height = int(0)
            box_body_width = int(20)
            box_body_height = int(2)
            box_string_ach = self.draw_box(box_header_width, box_header_height)
            box_string = self.draw_box(box_header_width, box_header_height)
            box_string_2 = self.draw_box(box_body_width, box_body_height)
            ui.set('Achievement_Main', box_string_ach)
            ui.set('Achievement_Header', box_string)
            ui.set('Achievement_Body', box_string_2)
            ui.set('Achievement_Header_Text', self.Last_Achievement_Header)
            ui.set('Achievement_Body_Text', self.Last_Achievement_Body)
            ui.set('Achievement_Main_Text', 'Latest Achievement')
            self.Show_Achievement_Window = True
            self.achievement_start_time = time.time()

    def check_achievement_display(self, ui):
        if self.Show_Achievement_Window and self.achievement_start_time:
            elapsed_time = time.time() - self.achievement_start_time
            if elapsed_time >= self.Show_Achievement_Duration:
                self.remove_achievement_box(ui)
            else:
                self.show_achievement_box(ui)

    def on_ui_update(self, ui):
        self.check_achievement_display(ui)
        ui.set('Age', self.calculate_device_age())
        ui.set('Level', self.calculate_device_level())
        ui.set('Strength', self.calculate_device_strength())
        ui.set('Dexterity', self.calculate_device_dexterity())
        ui.set('Constitution', self.calculate_device_constitution())
        ui.set('Intelligence', self.calculate_device_intelligence())
        ui.set('Wisdom', self.calculate_device_wisdom())
        ui.set('Charisma', self.calculate_device_charisma())
        ui.set('Luck', self.calculate_device_luck())
        ui.set('Associations', str(self.Num_Associations))
        ui.set('Deauths Sent', str(self.Num_DeAuths))
        self.Experience_needed = self.calcExpNeeded(self.Level)
        self.Experience_percent = int(
            (self.Experience / self.Experience_needed) * 100)
        symbols_count = int(self.options["exp_bar_symbols_count"])
        bar = self.barString(symbols_count, self.Experience_percent)
        ui.set('Experience', "%s" % bar)

    def load_data(self, data_path):
        self.LogInfo("Attempting to load data")
        if os.path.exists(data_path):
            try:
                with open(data_path) as f:
                    data = json.load(f)
                    self.epochs = data.get('epochs_lived', 0)
                    self.train_epochs = data.get('epochs_trained', 0)
                    born_at = data.get('born_at')
                    if born_at:
                        self.device_start_time = datetime.fromtimestamp(
                            born_at)
                    self.LogInfo("Data loaded from file!")
            except FileNotFoundError:
                logging.warning("Data file not found")
            except json.JSONDecodeError:
                logging.error("Error decoding JSON data")

    def barString(self, symbols_count, p):
        if p > 100:
            return BAR_ERROR
        length = symbols_count - 2
        bar_char = '▥'
        blank_char = ' '
        bar_length = int(round((length / 100) * p))
        blank_length = length - bar_length
        res = '|' + bar_char * bar_length + blank_char * blank_length + '|'
        return res

    def parseSessionStats(self):
        sum = 0
        dir = pwnagotchi.config['main']['plugins']['session-stats']['save_directory']
        # TODO: remove
        self.LogInfo("Session-Stats dir: " + dir)
        for filename in os.listdir(dir):
            self.LogInfo("Parsing " + filename + "...")
            if filename.endswith(".json") and filename.startswith("stats"):
                try:
                    sum += self.parseSessionStatsFile(
                        os.path.join(dir, filename))
                except:
                    self.LogInfo("ERROR parsing File: " + filename)

        return sum

    def try_increase_stat(self, agent, stat_name, increase_amount=1, chance=0.5, action_face=faces.MOTIVATED):
        try:
            self.LogInfo(f"Increasing stats! self: {self} agent: {agent} stat_name: {stat_name} increase_amount: {increase_amount} chance: {chance}")
            if random.random() < chance:
                current_value = getattr(self, stat_name, 0)
                new_value = current_value + increase_amount
                test_value = self.ensure_positive(new_value)
                setattr(self, stat_name, test_value)
                view = agent.view()
                view.set('face', action_face)
                view.set('status', "My " + str(stat_name) + " has changed by " + str(increase_amount) + ". It\n" "is now " + str(test_value) + ".")
                view.update(force=True)
                self.checkAchievements(agent)
            self.Save(self.save_file)
        except:
            self.LogInfo(
                f"ERROR increasing stats! self: {self} agent: {agent} stat_name: {stat_name} increase_amount: {increase_amount} chance: {chance}")

    def parseSessionStatsFile(self, path):
        total_sum = 0
        deauths = 0
        handshakes = 0
        associations = 0
        hops = 0
        peers = 0
        missed_interactions = 0
        total_bond = 0
        total_reward = 0

        # Read the session stats file
        with open(path) as json_file:
            data = json.load(json_file)
            entries = data.get("data", {})

            for entry in entries:
                stats = entries[entry]
                deauths += stats.get("num_deauths", 0)
                handshakes += stats.get("num_handshakes", 0)
                associations += stats.get("num_associations", 0)
                hops += stats.get("num_hops", 0)
                peers += stats.get("num_peers", 0)
                missed_interactions += stats.get("missed_interactions", 0)
                total_bond += stats.get("avg_bond", 0)
                total_reward += stats.get("reward", 0)

        # Apply multipliers and calculate total sum
        total_sum += deauths * MULTIPLIER_DEAUTH
        total_sum += handshakes * MULTIPLIER_HANDSHAKE
        total_sum += associations * MULTIPLIER_ASSOCIATION

        # Store computed values in instance variables (if needed)
        self.Num_DeAuths += deauths
        self.Num_Handshakes += handshakes
        self.Num_Associations += associations
        self.Num_Hops += hops
        self.Num_Peers += peers
        self.Missed_Interactions += missed_interactions
        self.Average_Bond = total_bond / len(entries) if entries else 0
        self.Reward = total_reward / len(entries) if entries else 0

        return total_sum

    def lastSessionPoints(self, agent):
        summary = 0
        summary += agent.LastSession.handshakes * MULTIPLIER_HANDSHAKE
        summary += agent.LastSession.associated * MULTIPLIER_ASSOCIATION
        summary += agent.LastSession.deauthed * MULTIPLIER_DEAUTH
        return summary

    def level_checkpoint(self, agent):
        view = agent.view()
        view.set('face', FACE_LEVELUP)
        view.set('status', "Ding level " + self.Level + "!")
        view.update(force=True)
        self.Save(self.save_file)

    def age_checkpoint(self, agent):
        view = agent.view()
        view.set('face', faces.HAPPY)
        view.set('status', "Wow, I've lived for " + self.calculate_device_age())
        view.update(force=True)
        self.Save(self.save_file)

    def exp_check(self, agent):
        self.LogDebug("EXP CHECK")
        if self.Experience >= self.Experience_needed:
            self.Experience = 1
            self.Level = self.Level + 1
            self.Experience_needed = self.calcExpNeeded(self.Level)
            self.displayLevelUp(agent)

    # If initial sum is 0, we try to parse it
    def calculateInitialSum(self, agent):
        sessionStatsActive = False
        sum = 0
        # Check if session stats is loaded
        for plugin in pwnagotchi.plugins.loaded:
            if plugin == "session-stats":
                sessionStatsActive = True
                break

        if sessionStatsActive:
            try:
                self.LogInfo("parsing session-stats")
                sum = self.parseSessionStats()
            except:
                self.LogInfo("Error parsing session-stats")

        else:
            self.LogInfo("parsing last session")
            sum = self.lastSessionPoints(agent)

        self.LogInfo(str(sum) + " Points calculated")
        return sum

    # Helper function to calculate multiple Levels from a sum of EXPs
    def calcLevelFromSum(self, sum, agent):
        sum1 = sum
        level = 1
        while sum1 > self.calcExpNeeded(level):
            sum1 -= self.calcExpNeeded(level)
            level += 1
        self.Level = level
        self.Experience = sum1
        self.Experience_needed = self.calcExpNeeded(level) - sum1
        if level > 1:
            # get Excited ;-)
            self.level_checkpoint(agent)

        total_deauths = self.Num_DeAuths
        total_handshakes = sum / MULTIPLIER_HANDSHAKE
        total_associations = sum / MULTIPLIER_ASSOCIATION
        total_events = total_deauths + total_handshakes + total_associations
        if total_events > 0:
            self.LogInfo("Granting initial stats based on experience sum")

            # Calculate proportions based on the sum
            deauths_proportion = (sum / MULTIPLIER_DEAUTH) / total_events
            handshakes_proportion = (sum / MULTIPLIER_HANDSHAKE) / total_events
            associations_proportion = (
                sum / MULTIPLIER_ASSOCIATION) / total_events
            self.LogInfo(
                f"deauths_proportion: {deauths_proportion} handshakes_proportion: {handshakes_proportion} associations_proportion: {associations_proportion}")

            # Assign stats based on the proportions
            self.try_increase_stat(
                agent, 'Strength', increase_amount=deauths_proportion * 10, chance=1.0)
            self.try_increase_stat(
                agent, 'Dexterity', increase_amount=handshakes_proportion * 10, chance=1.0)
            self.try_increase_stat(
                agent, 'Intelligence', increase_amount=associations_proportion * 10, chance=1.0)

            # Assign other stats based on remaining proportions
            self.try_increase_stat(
                agent, 'Constitution', increase_amount=deauths_proportion * 5, chance=1.0)
            self.try_increase_stat(
                agent, 'Wisdom', increase_amount=handshakes_proportion * 5, chance=1.0)
            self.try_increase_stat(
                agent, 'Charisma', increase_amount=associations_proportion * 5, chance=1.0)
            self.try_increase_stat(agent, 'Luck', increase_amount=(
                deauths_proportion + handshakes_proportion + associations_proportion) / 3 * 5, chance=1.0)

    def calcActualSum(self, level, exp):
        lvlCounter = 1
        sum = exp
        # I know it wouldn't work if you change the lvl algorithm
        while lvlCounter < level:
            sum += self.calcExpNeeded(lvlCounter)
            lvlCounter += 1
        return sum

    def calcExpNeeded(self, level):
        # If the pwnagotchi is lvl <1 it causes the keys to be deleted
        if level == 1:
            return 5
        return int((level ** 3) / 2)

    def calculate_device_age(self):
        current_time = datetime.now()
        age_delta = current_time - self.device_start_time

        years = age_delta.days // 365
        remaining_days = age_delta.days % 365
        months = remaining_days // 30
        days = remaining_days % 30

        age_str = f'{years}y {months}m {days}d ◂'
        return age_str

    def calculate_device_level(self):
        level_str = str(self.Level)
        return level_str

    def calculate_device_strength(self):
        self.Strength = self.Experience * self.Level * 0.05  # Example calculation
        rounded_strength = round(self.Strength)
        return str(int(rounded_strength))

    def calculate_device_dexterity(self):
        return str(round(self.Dexterity))

    def calculate_device_constitution(self):
        return str(round(self.Constitution))

    def calculate_device_intelligence(self):
        self.Intelligence = self.train_epochs
        return str(self.Intelligence)

    def calculate_device_wisdom(self):
        return str(round(self.Wisdom))

    def calculate_device_charisma(self):
        return str(round(self.Charisma))

    def calculate_device_luck(self):
        return str(round(self.Luck))

    # Achievement System
    def checkAchievements(self, agent):
        self.LogInfo("Check for new achievements")
        for name, achievement in self.Achievements.items():
            if not achievement["unlocked"]:
                condition = achievement["condition"]
                # Evaluate the condition dynamically
                if eval(condition, vars(self)):
                    achievement["unlocked"] = True
                    self.Last_Achievement_Header = name
                    self.Last_Achievement_Body = achievement["condition"]
                    self.notifyAchievement(agent, name)

    def notifyAchievement(self, agent, achievement):
        self.LogInfo(f"New Achievement Unlocked: {achievement}")
        view = agent.view()
        view.set('face', FACE_NEWACHIEVEMENT)
        view.set('status', f"New Achievement Unlocked: {achievement}")
        view.update(force=True)
        self.Save(self.save_file)

    # Event Handling
    def on_ai_training_step(self, agent, _locals, _globals):
        self.train_epochs += 1
        self.Num_Access_Points += len(agent.view().access_points())
        self.Num_DeAuths += agent.stats('deauth')
        if self.train_epochs % 100 == 0:
            self.try_increase_stat(agent, 'Strength', chance=0.9)
            self.try_increase_stat(agent, 'Constitution', chance=0.5)
        self.Save(self.save_file)

    def on_epoch(self, agent, epoch, epoch_data):
        self.epochs += 1
        if self.epochs % 100 == 0:
            self.age_checkpoint(agent)
        self.Save(self.save_file)

    def on_ready(self, agent):
        if self.calculateInitialXP:
            self.LogInfo("Initial point calculation")
            sum = self.calculateInitialSum(agent)
            self.Experience_total = sum
            self.calcLevelFromSum(sum, agent)
        self.Save(self.save_file)

    def on_association(self, agent, access_point):
        self.Experience += MULTIPLIER_ASSOCIATION
        self.Experience_total += MULTIPLIER_ASSOCIATION
        self.Num_Associations += 1
        self.exp_check(agent)
        self.Save(self.save_file)

    def on_deauthentication(self, agent, access_point, client_station):
        self.Experience += MULTIPLIER_DEAUTH
        self.Experience_total += MULTIPLIER_DEAUTH
        self.Num_DeAuths += 1
        self.exp_check(agent)
        self.Save(self.save_file)

    def on_handshake(self, agent, filename, access_point, client_station):
        self.Experience += MULTIPLIER_HANDSHAKE
        self.Experience_total += MULTIPLIER_HANDSHAKE
        self.Num_Handshakes += 1
        self.exp_check(agent)
        self.Save(self.save_file)

    def displayLevelUp(self, agent):
        view = agent.view()
        view.set('face', faces.HAPPY)
        view.set('status', "I'm now level " + str(self.Level))
        view.update(force=True)
        self.Save(self.save_file)

    def on_ai_best_reward(self, agent):
        self.LogInfo('Achieved a best reward!')
        self.try_increase_stat(agent, 'Strength', chance=0.5)
        self.try_increase_stat(agent, 'Dexterity', chance=0.5)
        self.try_increase_stat(agent, 'Luck', chance=0.25)

    def on_ai_worst_reward(self, agent):
        self.LogInfo('Achieved a worst reward!')
        self.try_increase_stat(agent, 'Wisdom', chance=0.5)

    def on_ai_training_start(self, agent):
        self.LogInfo('Beginning my training!')
        self.try_increase_stat(agent, 'Constitution', chance=0.5)

    def on_ai_training_end(self, agent):
        self.LogInfo('Finished my training!')
        self.try_increase_stat(agent, 'Intelligence', chance=0.5)

    def on_sad(self, agent):
        self.LogInfo('Big Sad!')
        self.try_increase_stat(
            agent, 'Charisma', increase_amount=-1, chance=0.5)
        self.try_increase_stat(agent, 'Luck', increase_amount=-1, chance=0.5)

    def on_bored(self, agent):
        self.LogInfo('Le bored!')
        self.try_increase_stat(agent, 'Intelligence',
                               increase_amount=-1, chance=0.5)

    def on_excited(self, agent):
        self.LogInfo('Woop Woop!')
        self.try_increase_stat(agent, 'Charisma', chance=0.5)
        self.try_increase_stat(agent, 'Luck', chance=0.5)

    def on_lonely(self, agent):
        self.LogInfo('So lonely!')
        self.try_increase_stat(agent, 'Wisdom', increase_amount=-1, chance=0.5)
        self.try_increase_stat(
            agent, 'Charisma', increase_amount=-1, chance=0.5)

    def on_peer_detected(self, agent):
        self.LogInfo('A new friend!')
        self.try_increase_stat(agent, 'Charisma', chance=0.5)
        self.try_increase_stat(agent, 'Intelligence', chance=0.5)

    def on_peer_lost(self, agent):
        self.LogInfo('My new friend left!')
        self.try_increase_stat(agent, 'Wisdom', chance=0.5)

    def on_captive_portal_detected(self, agent, access_point):
        self.LogInfo('Detected a captive portal!')
        self.try_increase_stat(agent, 'Intelligence', chance=0.7)
        self.try_increase_stat(agent, 'Wisdom', chance=0.7)

    def on_internet_access_detected(self, agent):
        self.LogInfo('Detected internet access!')
        self.try_increase_stat(agent, 'Charisma', chance=0.5)
        self.try_increase_stat(agent, 'Luck', chance=0.5)

    def on_channel_switch(self, agent, channel):
        self.LogInfo(f'Switched to channel {channel}!')
        self.try_increase_stat(agent, 'Dexterity', chance=0.6)
        self.try_increase_stat(agent, 'Wisdom', chance=0.6)

    def on_new_ap_found(self, agent, access_point):
        self.LogInfo('Found a new access point!')
        self.try_increase_stat(agent, 'Intelligence', chance=0.5)
        self.try_increase_stat(agent, 'Luck', chance=0.5)

    def on_configuration_change(self, agent, config):
        self.LogInfo('Configuration changed!')
        self.try_increase_stat(agent, 'Constitution', chance=0.5)
        self.try_increase_stat(agent, 'Wisdom', chance=0.5)

    def process_access_points(self, ap_list):
        for ap in ap_list:
            mac = ap.get("mac")
            if mac not in self.Access_Points["macs"]:
                self.Access_Points["macs"].add(mac)
                self.Access_Points["count"] += 1
        self.Save(self.save_file)
        
    def on_unfiltered_ap_list(self, ap_list):
        self.process_access_points(ap_list)

    def on_wifi_update(self, ap_list):
        self.process_access_points(ap_list)
