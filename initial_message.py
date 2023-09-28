import messages as msg


def start():
    """
    This function prints the initial message as the name suggests
    It contains "hello" message, "supported extensions" message,
    and information about supported animated images
    """
    print(msg.hashtag_decoration)
    print(msg.hello_first_row.center(msg.number_of_symbols, ' '))
    print(msg.hello_second_row.center(msg.number_of_symbols, ' '))
    print(msg.dash_decoration)
    print(msg.supported_extensions.center(msg.number_of_symbols, ' '))
    print(msg.hashtag_decoration)
