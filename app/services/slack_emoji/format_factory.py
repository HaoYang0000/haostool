import sys
from .characters import *
from .characters import GRID_SIZE


def process_each_character_per_line(emoji: str, sentence: list) -> str:
    """
    Process each word, and print out each character to per line
    :param emoji:
    :param sentence:
    :return: str
    """
    output = ""
    # Append every word in array
    for words in sentence:
        # Process each character
        for character in words:
            class_name = character
            word = __str_to_class(class_name.upper())
            if word is not None:
                output = output + word(emoji=emoji).get_format() + "{line_break}"
        output = output + "{line_break}"
    return output


def process_each_word_per_line(emoji: str, sentence: list) -> str:
    """
    Process each word, and print out each character for a word on the same line
    :param emoji:
    :param sentence:
    :return: str
    """
    output = ""
    # Append every word in array
    for words in sentence:
        # Tokenize each line of the character format
        format_token = {}
        for character in words:
            class_name = character
            word = __str_to_class(class_name.upper())
            format_token[character] = word(emoji=emoji).get_format().split('{line_break}')
        # Process each line of token
        for i in range(0, GRID_SIZE):
            for token in format_token:
                output = output + format_token[token][i]
            output = output + "{line_break}"
        output = output + "{line_break}"
    return output


def post_format(output: str, padding: str, emoji: str, if_reverse: bool = False) -> str:
    if if_reverse is True:
        return output.format(emoji, padding, line_break="\n")
    return output.format(padding, emoji, line_break="\n")


def __str_to_class(class_name: str):
    """
    Convert string of class name to class
    :param class_name:str
    :return: class
    """
    try:
        return getattr(sys.modules[__name__], class_name)
    except AttributeError:
        print("The character {character} is not implemented yet :( ".format(character=class_name))
        return None
