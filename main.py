import os.path
import time
import messages as msg
from get_quailty import quality
from initial_message import start

VALID_EXTENSIONS = ["png", "jpeg", "jpg", "tiff", "webp"]

# show initial message
start()

# ask the user to place the files in the "in" folder
print(msg.files_placement)


def check_folder():
    """
    the function waits for the user to type "ok" to continue
    """
    command = input(msg.ok_to_continue)
    while command.lower() != "ok":
        print(msg.invalid_command)
        command = input(msg.ok_to_continue)


check_folder()

original_dir = 'in'
output_dir = 'out'

# check if the directory is empty
number_of_files = len([x for x in os.listdir(original_dir) if os.path.isfile(os.path.join(original_dir, x))])
while not number_of_files:
    print(msg.empty_folder)
    print(msg.files_placement)
    number_of_files = len([x for x in os.listdir(original_dir) if os.path.isfile(os.path.join(original_dir, x))])
    check_folder()

# getting the quality value from the user (0 - 100)
quality_value = quality(int(input(msg.quality_prompt)))

# path to cwebp.exe
path_to_exe = 'webp_convert\\bin\\cwebp.exe'

# this list will hold the converted files with valid extensions
valid_files = []

# this list will hold the converted files with unsupported extensions
report = []

# convert the files
for file in os.listdir(original_dir):
    # splitting the file gives as a list with 2 elements: name and extension
    output_file_name, extension = file.split('.')

    # adding .webp to the output file name
    output_file_name += '.webp'

    # checking for supported extensions and appending the file to the corresponding list
    if extension not in VALID_EXTENSIONS:
        report.append(f"""The file "{file}" is unsupported type,
        so you may not be able to open "{output_file_name}" after the conversion.""")
    else:
        valid_files.append(file)

    # the cmd command will be in this format:
    # cwebp \path\to\image_file.extension -o \path\to\output.webp -q 100
    os.system(f'{path_to_exe} "{original_dir}\\{file}" -o "{output_dir}\\{output_file_name}" -q {quality_value}')

    # waiting 1 second between each iteration
    time.sleep(1)

# printing the converted valid files
if valid_files:
    print("CONVERTED FILES: ")
    for f in valid_files:
        print(f)

# printing the files that may not be used after the conversion
# even if it successful
if report:
    print("REPORT: ")
    for r in report:
        print(r)
