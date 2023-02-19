import arcade
import arcade.gui as gui

from .game import ViewGame


class ViewMainMenu(arcade.View):
    def __init__(self):
        super().__init__()
        self.ui_manager = gui.UIManager()

        self.anchor = self.ui_manager.add(gui.UIAnchorLayout())

        self.title = gui.UILabel(text="Community RPG", font_size=48)

        button_texture = gui.NinePatchTexture(
            left=5,
            right=5,
            bottom=5,
            top=5,
            texture=arcade.load_texture(
                ":resources:gui_basic_assets/red_button_normal.png"
            ),
        )

        button_hovered_texture = gui.NinePatchTexture(
            left=5,
            right=5,
            bottom=5,
            top=5,
            texture=arcade.load_texture(
                ":resources:gui_basic_assets/red_button_hover.png"
            ),
        )

        button_pressed_texture = gui.NinePatchTexture(
            left=5,
            right=5,
            bottom=5,
            top=5,
            texture=arcade.load_texture(
                ":resources:gui_basic_assets/red_button_press.png"
            ),
        )

        play_button = gui.UITextureButton(
            texture=button_texture,
            texture_hovered=button_hovered_texture,
            texture_pressed=button_pressed_texture,
            text="Play",
        )

        @play_button.event("on_click")
        def on_click_play(event):
            self.window.views["game"] = ViewGame()
            self.window.show_view(self.window.views["game"])

        quit_button = gui.UITextureButton(
            texture=button_texture,
            texture_hovered=button_hovered_texture,
            texture_pressed=button_pressed_texture,
            text="Quit",
        )

        @quit_button.event("on_click")
        def on_click_quit(event):
            self.window.close()

        self.v_box = gui.UIBoxLayout(
            children=[
                play_button,
                quit_button,
            ],
            space_between=20,
        )
        self.anchor.add(self.title, anchor_x="center_x", anchor_y="top", align_y=-100)
        self.anchor.add(
            self.v_box,
            anchor_x="center_x",
            anchor_y="center_y",
        )

    def on_show_view(self):
        self.ui_manager.enable()

    def on_hide_view(self):
        self.ui_manager.disable()

    def on_draw(self):
        self.clear()
        self.ui_manager.draw()
