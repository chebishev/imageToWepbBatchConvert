import messages

max_quality = 100


def quality(number):
    """This function keeps getting the user input until it is between 0 and 100
    :returns: quality that will be used for the conversion
    """
    while number not in range(max_quality + 1):
        print(messages.invalid_command)
        number = int(input(messages.quality_prompt))
    return number
