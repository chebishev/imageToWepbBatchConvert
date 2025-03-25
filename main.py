import os
import time
import subprocess
from pathlib import Path
from PIL import Image  # Used to detect animated GIFs
import messages as msg
import get_quailty
from initial_message import start

VALID_STATIC_EXTENSIONS = ["png", "jpeg", "jpg", "tiff", "webp"]
VALID_ANIMATED_EXTENSIONS = ["gif"]  # Only GIFs can be animated
CWEBP_PATH = "webp_convert/bin/cwebp.exe"
GIF2WEBP_PATH = "webp_convert/bin/gif2webp.exe"


class WebPConverter:
    def __init__(self, input_dir="in", output_dir="out", quality=75, reduce_frames=False, split_frames=False):
        self.input_dir = Path(input_dir)
        self.output_dir = Path(output_dir)
        self.quality = quality
        self.reduce_frames = reduce_frames
        self.split_frames = split_frames
        self.valid_files = []
        self.report = []

        self.output_dir.mkdir(exist_ok=True)  # Ensure output directory exists

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
            return self.convert_images()  # Retry if the folder is empty

        for file in files:
            ext = file.suffix.lower().lstrip(".")
            output_file = self.output_dir / f"{file.stem}.webp"

            if ext in VALID_STATIC_EXTENSIONS:
                self.convert_static_image(file, output_file)
            elif ext in VALID_ANIMATED_EXTENSIONS and self.is_animated_gif(file):
                self.convert_animated_gif(file)
            else:
                self.report.append(f'Unsupported file "{file.name}" - conversion may not work.')

        self.print_report()

    def convert_static_image(self, input_file, output_file):
        """Convert a static image to WebP using cwebp."""
        self.valid_files.append(input_file.name)
        cmd = [CWEBP_PATH, str(input_file), "-o", str(output_file), "-q", str(self.quality)]
        subprocess.run(cmd, check=True)
        time.sleep(1)  # Prevent overloading CPU

    def convert_animated_gif(self, input_file):
        """Convert an animated GIF to WebP using gif2webp."""
        base_output = self.output_dir / input_file.stem

        if self.split_frames:
            # Extract frames separately
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
            # Convert GIF as a single animated WebP
            output_file = f"{base_output}.webp"
            cmd = [GIF2WEBP_PATH, str(input_file), "-o", output_file, "-q", str(self.quality)]
            if self.reduce_frames:
                cmd.append("-mixed")  # Reduces redundant frames to optimize size
            subprocess.run(cmd, check=True)
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

    quality_value = get_quailty.quality(int(input(msg.quality_prompt)))

    # User options for frame handling
    reduce_frames = input("Reduce redundant frames in animated GIFs? (y/n): ").strip().lower() == "y"
    split_frames = input("Split GIF into individual frames? (y/n): ").strip().lower() == "y"

    converter = WebPConverter(quality=quality_value, reduce_frames=reduce_frames, split_frames=split_frames)
    converter.check_folder()
    converter.convert_images()
