import logging

logging.basicConfig(
    filemode="/var/log/ansible_tickets.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s:%(message)s",
)
