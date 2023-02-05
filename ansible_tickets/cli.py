"""Module to handle entry point."""
import logging
import sys

from ansible_tickets.runner import Runner

LOG = logging


def init():
    """Entry point for the application."""
    input = ""
    for line in sys.stdin:
        input = input + line
    Runner(ansible_output=input)


if __name__ == "__main__":
    init()
