import config
"""
This file holds the messages in the project
Mostly for better abstraction
"""

number_of_symbols = 60
hashtag_decoration = "#" * number_of_symbols
hello_first_row = "Hello! This program will allow you to batch convert your"
hello_second_row = "PNG, JPEG, TIFF, GIF and WEBP files to WEBP."
files_placement = f"1. Place the file(s) that you want to convert in the \"{config.INPUT_DIR}\" folder."
ok_to_continue = "Type \"ok\" to continue: "
empty_folder = f"There are no files in the \"{config.INPUT_DIR}\" folder."
invalid_command = "Invalid command!"
quality_prompt = """2. Choose the quality of the image(s) (0-100):
        0 - worst quality and smallest file size
        100 - best quality and largest file size
        or press ENTER for default quality (75)"""
static_image_quality = "Converting static image... Applying quality settings."
animated_image_quality = "Converting animated GIF... Applying quality settings."
