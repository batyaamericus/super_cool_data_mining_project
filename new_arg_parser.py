import argparse


class NewArgParser(argparse.ArgumentParser):
    def error(self, message):
        """error(message: string)

        Prints a usage message incorporating the message to stderr and
        exits.
        """
        raise argparse.ArgumentError(None, message)
