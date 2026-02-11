import pyglet

class ManageFont:
    def __init__(self):
        # Register custom font files
        pyglet.font.add_file("fonts/Koulen-Regular.ttf")
        pyglet.font.add_file("fonts/TTNormsPro-ExtraLight.otf")

        # Define font styles
        self.heading_font = ("Koulen", 28, "bold")
        self.medium_letters_font = ("TT Norms Pro ExtraLight", 14)
        self.larger_letters_font = ("TT Norms Pro ExtraLight", 18)
        self.smaller_letters_font = ("TT Norms Pro ExtraLight", 12)

        self.medium_bold_heading_font = ("Koulen", 20, "bold")
        self.large_italic_heading_font = ("Koulen", 22, "italic")
        self.small_bold_heading_font = ("TT Norms Pro ExtraLight", 12, "bold")
🔑 Key points
