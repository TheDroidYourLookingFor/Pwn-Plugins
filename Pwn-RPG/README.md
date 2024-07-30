# 🖥  Pwnagotchi | Pwn-RPG

Scripts for Pwnagotchi
* [Pwn-RPG](https://github.com/TheDroidYourLookingFor/Pwn-Plugins/tree/main/Pwn-RPG)
  * This is the RPG system I am writing for the Pwnagotchi. Its a 6 Stat+Luck system and currently very much a work in progress.

### Quickstart Guide
* Copy the script you like and SSH into your device.
* sudo vi /usr/local/share/pwnagotchi/custom-plugins/Pwn-RPG.py  (Example)
* Paste the contents of the current file into file by using Shift + Right Click
* Use :x to save and quit
* sudo vi /etc/pwnagotchi/config.tml
* Enter the required settings for the plugin
* Use :x to save and quit
* pwnkill

## Config
### Waveshare 3.7inch E-Paper E-Ink Display
```
    main.plugins.Pwn-RPG.enabled = true
    main.plugins.Pwn-RPG.exp_bar_symbols_count = 12
    main.plugins.Pwn-RPG.label_padding = 22
    main.plugins.Pwn-RPG.box_symbol = "_"
    main.plugins.Pwn-RPG.box_side_symbol = "|"
    main.plugins.Pwn-RPG.stat_box_wall_height = 6
    main.plugins.Pwn-RPG.stat_box_divider_height = 3
    main.plugins.Pwn-RPG.stat_box_top_x_coord = 0
    main.plugins.Pwn-RPG.stat_box_top_y_coord = 95
    main.plugins.Pwn-RPG.stat_box_top_length = 20
    main.plugins.Pwn-RPG.stat_box_bottom_x_coord = 0
    main.plugins.Pwn-RPG.stat_box_bottom_y_coord = 185
    main.plugins.Pwn-RPG.stat_box_bottom_length = 20
    main.plugins.Pwn-RPG.stat_box_side_vertical_spacing = 15
    main.plugins.Pwn-RPG.stat_box_side_left_x_coord = -4
    main.plugins.Pwn-RPG.stat_box_side_left_y_coord = 110
    main.plugins.Pwn-RPG.stat_box_center_x_coord = 82
    main.plugins.Pwn-RPG.stat_box_center_y_coord = 126
    main.plugins.Pwn-RPG.stat_box_side_right_x_coord = 180
    main.plugins.Pwn-RPG.stat_box_side_right_y_coord = 110
    main.plugins.Pwn-RPG.stat_box_age_x_coord = 0
    main.plugins.Pwn-RPG.stat_box_age_y_coord = 112
    main.plugins.Pwn-RPG.stat_box_age_length = 20
    main.plugins.Pwn-RPG.stat_box_stats_x_coord = 0
    main.plugins.Pwn-RPG.stat_box_stats_y_coord = 156
    main.plugins.Pwn-RPG.stat_box_stats_length = 20
    main.plugins.Pwn-RPG.stat_box_luck_x_coord = 0
    main.plugins.Pwn-RPG.stat_box_luck_y_coord = 170
    main.plugins.Pwn-RPG.stat_box_luck_length = 20
    main.plugins.Pwn-RPG.exp_label_padding = 5
    main.plugins.Pwn-RPG.exp_x_coord = 275
    main.plugins.Pwn-RPG.exp_y_coord = 242
    main.plugins.Pwn-RPG.age_label_padding = 22
    main.plugins.Pwn-RPG.age_x_coord = 13
    main.plugins.Pwn-RPG.age_y_coord = 111
    main.plugins.Pwn-RPG.level_label_padding = 5
    main.plugins.Pwn-RPG.level_x_coord = 410
    main.plugins.Pwn-RPG.level_y_coord = 242
    main.plugins.Pwn-RPG.str_x_coord = 3
    main.plugins.Pwn-RPG.str_y_coord = 128
    main.plugins.Pwn-RPG.dex_x_coord = 3
    main.plugins.Pwn-RPG.dex_y_coord = 143
    main.plugins.Pwn-RPG.con_x_coord = 3
    main.plugins.Pwn-RPG.con_y_coord = 158
    main.plugins.Pwn-RPG.int_x_coord = 90
    main.plugins.Pwn-RPG.int_y_coord = 128
    main.plugins.Pwn-RPG.wis_x_coord = 90
    main.plugins.Pwn-RPG.wis_y_coord = 143
    main.plugins.Pwn-RPG.cha_x_coord = 90
    main.plugins.Pwn-RPG.cha_y_coord = 158
    main.plugins.Pwn-RPG.luck_x_coord = 55
    main.plugins.Pwn-RPG.luck_y_coord = 172
    main.plugins.Pwn-RPG.asc_x_coord = 1
    main.plugins.Pwn-RPG.asc_y_coord = 186
    main.plugins.Pwn-RPG.deauth_x_coord = 70
    main.plugins.Pwn-RPG.deauth_y_coord = 186
```
### Waveshare 2.13inch E-Ink Display
```
    main.plugins.Pwn-RPG.enabled = true
    main.plugins.Pwn-RPG.exp_bar_symbols_count = 11
    main.plugins.Pwn-RPG.label_padding = 8
    main.plugins.Pwn-RPG.stat_box_side_vertical_spacing = 8
    main.plugins.Pwn-RPG.box_symbol = "_"
    main.plugins.Pwn-RPG.box_side_symbol = "|"
    main.plugins.Pwn-RPG.stat_box_wall_height = 6
    main.plugins.Pwn-RPG.stat_box_divider_height = 3
    main.plugins.Pwn-RPG.stat_box_top_x_coord = 0
    main.plugins.Pwn-RPG.stat_box_top_y_coord = 49
    main.plugins.Pwn-RPG.stat_box_top_length = 20
    main.plugins.Pwn-RPG.stat_box_bottom_x_coord = 0
    main.plugins.Pwn-RPG.stat_box_bottom_y_coord = 99
    main.plugins.Pwn-RPG.stat_box_bottom_length = 20
    main.plugins.Pwn-RPG.stat_box_side_left_x_coord = -4
    main.plugins.Pwn-RPG.stat_box_side_left_y_coord = 109
    main.plugins.Pwn-RPG.stat_box_center_x_coord = 61
    main.plugins.Pwn-RPG.stat_box_center_y_coord = 71
    main.plugins.Pwn-RPG.stat_box_side_right_x_coord = 123
    main.plugins.Pwn-RPG.stat_box_side_right_y_coord = 58
    main.plugins.Pwn-RPG.stat_box_age_x_coord = 0
    main.plugins.Pwn-RPG.stat_box_age_y_coord = 62
    main.plugins.Pwn-RPG.stat_box_age_length = 20
    main.plugins.Pwn-RPG.stat_box_stats_x_coord = 0
    main.plugins.Pwn-RPG.stat_box_stats_y_coord = 88
    main.plugins.Pwn-RPG.stat_box_stats_length = 20
    main.plugins.Pwn-RPG.stat_box_luck_x_coord = 0
    main.plugins.Pwn-RPG.stat_box_luck_y_coord = 169
    main.plugins.Pwn-RPG.stat_box_luck_length = 22
    main.plugins.Pwn-RPG.exp_label_padding = 2
    main.plugins.Pwn-RPG.exp_x_coord = 0
    main.plugins.Pwn-RPG.exp_y_coord = 98
    main.plugins.Pwn-RPG.age_label_padding = 10
    main.plugins.Pwn-RPG.age_x_coord = 5
    main.plugins.Pwn-RPG.age_y_coord = 60
    main.plugins.Pwn-RPG.level_x_coord = 81
    main.plugins.Pwn-RPG.level_y_coord = 99
    main.plugins.Pwn-RPG.level_label_padding = 4
    main.plugins.Pwn-RPG.str_x_coord = 2
    main.plugins.Pwn-RPG.str_y_coord = 72
    main.plugins.Pwn-RPG.dex_x_coord = 2
    main.plugins.Pwn-RPG.dex_y_coord = 80
    main.plugins.Pwn-RPG.con_x_coord = 2
    main.plugins.Pwn-RPG.con_y_coord = 88
    main.plugins.Pwn-RPG.int_x_coord = 65
    main.plugins.Pwn-RPG.int_y_coord = 72
    main.plugins.Pwn-RPG.wis_x_coord = 65
    main.plugins.Pwn-RPG.wis_y_coord = 80
    main.plugins.Pwn-RPG.cha_x_coord = 65
    main.plugins.Pwn-RPG.cha_y_coord = 88
    main.plugins.Pwn-RPG.luck_x_coord = 380
    main.plugins.Pwn-RPG.luck_y_coord = 72
    main.plugins.Pwn-RPG.asc_x_coord = 0
    main.plugins.Pwn-RPG.asc_y_coord = 49
    main.plugins.Pwn-RPG.deauth_x_coord = 60
    main.plugins.Pwn-RPG.deauth_y_coord = 49
```