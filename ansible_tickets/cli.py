import logging

from sys import argv

from ansible_tickets.runner import Runner

LOG = logging


def init():
    """
        Entry point for the application.
    """
    try:
        Runner(ansible_output=argv[1])
    except IndexError:
        LOG.debug('No data received')
        exit(1)


if __name__ == '__main__':
    init()
