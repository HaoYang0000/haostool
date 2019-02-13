import os, platform


class Util:
    @staticmethod
    def add_to_clipboard(output):
        # TODO: Fix this method.
        if platform.system() == 'Windows':
            command = 'echo ' + output.strip() + '| clip'
            os.system(command)
        else:
            os.system("echo '%s' | pbcopy" % output)


