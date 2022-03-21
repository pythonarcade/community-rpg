"""
Draw a percentage bar
"""
import arcade


def draw_bar(current_amount,
             max_amount,
             center_x,
             center_y,
             width,
             height,
             color_a,
             color_b):

    # Draw the background
    if current_amount < max_amount:
        arcade.draw_rectangle_filled(center_x=center_x,
                                     center_y=center_y,
                                     width=width,
                                     height=height,
                                     color=color_a)

    # Calculate width
    bar_width = width * (current_amount / max_amount)

    # Draw filled part
    arcade.draw_rectangle_filled(center_x=center_x - 0.5 * (width - bar_width),
                                 center_y=center_y,
                                 width=bar_width,
                                 height=height,
                                 color=color_b)
