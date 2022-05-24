import arcade
 
# open the window
arcade.open_window(500, 500, "How to Play", False, False)
 
# set background color
arcade.set_background_color(arcade.color.BLACK)
 
# start drawing
arcade.start_render()
 
# finish drawing
arcade.finish_render()
 
# to keep output
# window open
arcade.run()