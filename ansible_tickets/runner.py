from ansible_parser.play import Play
from ansible_tickets.config import Config
from ansible_tickets.ticket_management import TicketManagement


class Runner:
    __slots__ = ['_config', '_failures', '_parser', '_tickets']

    def __init__(self, ansible_output):
        """
            Sets up the parser

            :param ansible_output: The output received from Ansible
        """
        self._config = Config('ansible_tickets.conf')
        self._failures = self._parser.failures()
        self._parser = Play(ansible_output)
        self._tickets = TicketManagement(self._config)
        for play in self._failures:
            self._process_play(play)

    def _process_play(self, play: str):
        """
            Process a play

            :param play: The name of the play being processed
        """
        for job in self._failures[play]:
            self._process_level(play, job)

    def _process_level(self, play: str, job: str):
        """
            Process a job

            :param play: The name of the play being processed
            :param job: The name of the job being processed
        """
        for level in self._failures[play][job]:
            self._process_job(play, job, level)

    def _process_job(self, play: str, job: str, level: str):
        """
            Process a job

            :param play: The name of the play being processed
            :param job: The name of the job being processed
            :param level: The name of the level being processed
        """
        for host in self._failures[play][job][level]:
            ticket_title = f'{host["host"]} - {play} - {job}'
            if self._tickets.ticket_exists('TEST', ticket_title):
                existing_ticket = self._tickets.get_ticket(self._config.get('jira_project'), ticket_title)
                self._tickets.update_ticket(existing_ticket, host['failure_message'])
            else:
                self._tickets.create_ticket(
                    self._config.get('jira_project'),
                    ticket_title,
                    host['failure_message'],
                    self._config.get('ticket_type')
                )
