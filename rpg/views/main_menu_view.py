# """
# Main Menu
# """
from curses import window
import arcade
import arcade.gui

# self.window.show_view(self.window.views["game"])

class MainMenuView(arcade.View):
    def __init__(self, game_view):
        super().__init__()
        print(arcade.View.window.views)
        self.v_box = arcade.gui.UIBoxLayout()
        self.game_view = game_view
        
        start_button = arcade.gui.UIFlatButton(text="Start Game", width=200)
        self.v_box.add(start_button.with_space_around(bottom=20))
        
        settings_button = arcade.gui.UIFlatButton(text="Settings", width=200)
        self.v_box.add(settings_button.with_space_around(bottom=20))

    def on_click_start(self):
        print('start')

    def on_click_settings(self):
        print('settings')
        
    def on_key_press(self, key, _modifiers):
        if key == arcade.key.ESCAPE:
            print('yo I like your cut G')
            self.window.show_view(self.window.views["game"])
        
    def setup(self):
        pass

class QuitButton(arcade.gui.UIFlatButton):
    def on_click(self, event: arcade.gui.UIOnClickEvent):
        arcade.exit()

# class MainMenuView(arcade.Window):
#     def __init__(self):
#         super().__init__(800, 600, "UIFlatButton Example", resizable=True)

#         # --- Required for all code that uses UI element,
#         # a UIManager to handle the UI.
#         self.manager = arcade.gui.UIManager()
#         self.manager.enable()

#         # Set background color
#         arcade.set_background_color(arcade.color.DARK_BLUE_GRAY)

#         # Create a vertical BoxGroup to align buttons
#         self.v_box = arcade.gui.UIBoxLayout()

#         # Create the buttons
#         start_button = arcade.gui.UIFlatButton(text="Start Game", width=200)
#         self.v_box.add(start_button.with_space_around(bottom=20))

#         settings_button = arcade.gui.UIFlatButton(text="Settings", width=200)
#         self.v_box.add(settings_button.with_space_around(bottom=20))

#         # Again, method 1. Use a child class to handle events.

#         quit_button = QuitButton(text="Quit", width=200)
#         self.v_box.add(quit_button)

#         # # --- Method 2 for handling click events,
#         # assign self.on_click_start as callback
#         start_button.on_click = self.on_click_start
    
#         # # --- Method 3 for handling click events,
#         # # use a decorator to handle on_click events
#         # @settings_button.event("on_click")
#         # def on_click_settings(event):
#         #     print("Settings:", event)

#         # Create a widget to hold the v_box widget, that will center the buttons
#         self.manager.add(
#             arcade.gui.UIAnchorWidget(
#                 anchor_x="center_x",
#                 anchor_y="center_y",
#                 child=self.v_box)
#         )

#     def on_click_start(self, event):
#         print("Start:", event)
#         self.window.show_view(self.window.views["game"])

#     def on_draw(self):
#         self.clear()
#         self.manager.draw()

#     def setup(self):
#         pass

# window = MainMenuView()
# arcade.run()

# class MainMenuView(arcade.View):
#     def __init__(self):
#         super().__init__()
#         self.started = False
#         arcade.set_background_color(arcade.color.ALMOND)

#     def on_draw(self):
#         arcade.start_render()
#         arcade.draw_text(
#             "Main Menu",
#             self.window.width / 2,
#             self.window.height - 50,
#             arcade.color.ALLOY_ORANGE,
#             44,
#             anchor_x="center",
#             anchor_y="center",
#             align="center",
#             width=self.window.width,
#         )

#         arcade.draw_text(
#             "Settings (Y)",
#             self.window.width / 2,
#             self.window.height - 150,
#             arcade.color.AMAZON,
#             32,
#             anchor_x="center",
#             anchor_y="center",
#             align="center",
#             width=self.window.width,
#         )

#         arcade.draw_text(
#             "Close Game (Q)",
#             self.window.width / 2,
#             self.window.height - 250,
#             arcade.color.AMAZON,
#             32,
#             anchor_x="center",
#             anchor_y="center",
#             align="center",
#             width=self.window.width,
#         )

#         arcade.draw_text(
#             "Resume Game (ESC)",
#             self.window.width / 2,
#             self.window.height - 350,
#             arcade.color.AMAZON,
#             32,
#             anchor_x="center",
#             anchor_y="center",
#             align="center",
#             width=self.window.width,
#         )

#         arcade.draw_text(
#             "New Game (N)",
#             self.window.width / 2,
#             self.window.height - 450,
#             arcade.color.AMAZON,
#             32,
#             anchor_x="center",
#             anchor_y="center",
#             align="center",
#             width=self.window.width,
#         )
#         arcade.draw_text(
#             "Battle Screen (B)",
#             self.window.width / 2,
#             self.window.height - 550,
#             arcade.color.AMAZON,
#             32,
#             anchor_x="center",
#             anchor_y="center",
#             align="center",
#             width=self.window.width,
#         )

#     def setup(self):
#         pass

#     def on_show_view(self):
#         arcade.set_background_color(arcade.color.ALMOND)
#         arcade.set_viewport(0, self.window.width, 0, self.window.height)

#     def on_key_press(self, symbol: int, modifiers: int):
#         if symbol == arcade.key.ESCAPE:
            # self.window.show_view(self.window.views["game"])
#         elif symbol == arcade.key.Y:
#             self.window.show_view(self.window.views["settings"])
#         elif symbol == arcade.key.Q:
#             self.window.close()
#         elif symbol == arcade.key.N:
#             self.window.views["game"].setup()
#             self.window.show_view(self.window.views["game"])
#         elif symbol == arcade.key.B:
#             self.window.views["battle"].setup()
#             self.window.show_view(self.window.views["battle"])
