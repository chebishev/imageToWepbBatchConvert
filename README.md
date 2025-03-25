# imageToWepbBatchConvert
Using the engine libwebp from Google Developers WebP (https://chromium.googlesource.com/webm/libwebp/) I've made a program that can do batch conversions of static and animated images to webp files

The downloaded archive from https://storage.googleapis.com/downloads.webmproject.org/releases/webp/index.html is extracted to "webp_convert" folder, which is in the repo too.
Latest version by today is libwebp-1.5.0

Supported formats are "png", "jpeg", "jpg", "tiff", gif and "webp".
As you can see on the demo any other format can be converted too, but the output isn't guaranteed, so try other formats on your own risk.
The program will show them in the REPORT anyway with warning message that they may be not usable.

This version of the program is currently working on Windows OS, but you can make changes for your desired OS in "config.py"

Click on the image to see the demo in YouTube:
<br>
[![DEMO](webpbatchconvert.png)](https://youtu.be/Tt3T_vvO8io)
