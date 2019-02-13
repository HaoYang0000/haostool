from .util import Util
from .format_factory import process_each_character_per_line, process_each_word_per_line, post_format
import sys, getopt

HELP_MESSAGE = "Please pass an emoji and a sentence to print. \n\n" \
               "Format: python ./main.py {SLACK_EMOJI} {WORDS_OR_SENTENCE_YOU_WANT_TO_PRINT} \n\n" \
               "For example: python ./main.py :dealwithit: DEAL with it \n\n" \
               "To print the word in the same line, do: python ./main.py -s :dealwithit: DEAL with it \n\n" \
               "Add flag -c to avoid the copy process(for your convenience :) " \
               "For example: python ./main.py -c {SLACK_EMOJI} {WORDS_OR_SENTENCE_YOU_WANT_TO_PRINT} \n\n" \
               ";-) \n"


def generate(
    emoji: str = ':dealwithit:',
    padding: str = ':white_large_square:',
    input: str = 'DEAL with it',
    if_same_line: bool = False,
    if_copy_to_clipboard: bool = False,
    if_reverse: bool = False
) -> str:
    # Generate output format
    if if_same_line is False:
        output = process_each_character_per_line(emoji=emoji, sentence=input.split(' '))
    else:
        output = process_each_word_per_line(emoji=emoji, sentence=input.split(' '))

    # Format output
    output = post_format(output=output, padding=padding, emoji=emoji, if_reverse=if_reverse)
    return output
