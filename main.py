import os
import time
import subprocess
from pathlib import Path
from PIL import Image
import messages as msg
from initial_message import start
import config 

VALID_STATIC_EXTENSIONS = ["png", "jpeg", "jpg", "tiff", "webp"]
VALID_ANIMATED_EXTENSIONS = ["gif"]


class WebPConverter:
    def __init__(
        self, 
        input_dir=config.INPUT_DIR, 
        output_dir=config.OUTPUT_DIR, 
        quality=config.DEFAULT_QUALITY, 
        reduce_frames=False, 
        split_frames=False):
        
        self.input_dir = Path(input_dir)
        self.output_dir = Path(output_dir)
        self._quality = quality
        self.reduce_frames = reduce_frames
        self.split_frames = split_frames
        self.valid_files = []
        self.report = []

        self.output_dir.mkdir(exist_ok=True)

    @property
    def quality(self):
        """Getter for quality."""
        return self._quality

    @quality.setter
    def quality(self, value):
        """Setter for quality, ensuring it's within the 0-100 range or defaults to a pre-set value."""
        max_quality = 100
        default_quality = config.DEFAULT_QUALITY

        if value == "":
            self._quality = default_quality
            return
        
        try:
            value = int(value)
        except ValueError:
            print(msg.invalid_command)
            value = -1

        if 0 <= value <= max_quality:
            self._quality = value
        else:
            print(msg.invalid_command)
            while not (0 <= value <= max_quality):
                try:
                    value = input(msg.quality_prompt)
                    if value == "":
                        self._quality = default_quality
                        return
                    value = int(value)
                except ValueError:
                    value = -1
                if 0 <= value <= max_quality:
                    self._quality = value
                else:
                    print(msg.invalid_command)


    def check_folder(self):
        """Wait for user confirmation to proceed."""
        while input(msg.ok_to_continue).strip().lower() != "ok":
            print(msg.invalid_command)

    def get_files(self):
        """Retrieve files from the input directory."""
        return [f for f in self.input_dir.iterdir() if f.is_file()]

    def is_animated_gif(self, file_path):
        """Check if a GIF file is animated."""
        with Image.open(file_path) as img:
            return hasattr(img, "is_animated") and img.is_animated

    def convert_images(self):
        """Convert valid image files to WebP."""
        files = self.get_files()

        if not files:
            print(msg.empty_folder)
            self.check_folder()
            return self.convert_images()

        for file in files:
            ext = file.suffix.lower().lstrip(".")
            output_file = self.output_dir / f"{file.stem}.webp"

            if ext in VALID_STATIC_EXTENSIONS:
                print(msg.static_image_quality) 
                self.convert_static_image(file, output_file)
            elif ext in VALID_ANIMATED_EXTENSIONS and self.is_animated_gif(file):
                print(msg.animated_image_quality)
                self.convert_animated_gif(file)
            else:
                self.report.append(f'Unsupported file "{file.name}" - conversion may not work.')

        self.print_report()

    def convert_static_image(self, input_file, output_file):
        """Convert a static image to WebP using cwebp."""
        self.valid_files.append(input_file.name)
        cmd = [config.CWEBP_PATH, str(input_file), "-o", str(output_file), "-q", str(self.quality)]
        subprocess.run(cmd, check=True)
        time.sleep(1)

    def convert_animated_gif(self, input_file):
        """Convert an animated GIF to WebP using gif2webp."""
        base_output = self.output_dir / input_file.stem

        cmd = [config.GIF2WEBP_PATH, str(input_file), "-o", str(base_output) + ".webp"]

        if self.split_frames:
            frame_number = 0
            with Image.open(input_file) as img:
                while True:
                    frame_file = base_output.with_name(f"{base_output.stem}_frame{frame_number}.webp")
                    img.save(frame_file, format="WebP", quality=self.quality)
                    frame_number += 1
                    try:
                        img.seek(frame_number)
                    except EOFError:
                        break
            self.valid_files.append(f"{input_file.name} (split into {frame_number} frames)")

        else:
            if self.reduce_frames:
                cmd.append("-mixed")
            else:
                cmd.append("-lossy")
                cmd.append("-q")
                cmd.append(str(self.quality))

            subprocess.run(cmd, check=True)
            # returns message in format "Saved output file (xxxxxx bytes): "
            # + first letter of the file path
            # example output: "Saved output file (991850 bytes): o", 
            # because the output folder is named "out"
            self.valid_files.append(input_file.name)


    def print_report(self):
        """Display conversion results."""
        if self.valid_files:
            print("CONVERTED FILES:")
            for f in self.valid_files:
                print(f)

        if self.report:
            print("REPORT:")
            for r in self.report:
                print(r)


if __name__ == "__main__":
    start()
    print(msg.files_placement)

    converter = WebPConverter()

    quality_value = input(msg.quality_prompt)
    converter.quality = quality_value

    reduce_frames = input("3. Reduce redundant frames in animated GIFs? (y/n): ").strip().lower() == "y"
    split_frames = input("4. Split GIF into individual frames? (y/n): ").strip().lower() == "y"

    converter.reduce_frames = reduce_frames
    converter.split_frames = split_frames

    converter.check_folder()
    converter.convert_images()
