import logging

from typing import Any, Dict, List, Optional, Union

from jira.resources import Issue
from jira import JIRA

from ansible_tickets.config import Config


class TicketManagement:
    __slots__ = ['_insight_field', '_insight_objects', '_jira', '_tickets']

    def __init__(self, config: Config):
        """
            Constructor
        """
        self._insight_field = config.get('insight_field')
        self._insight_objects: Dict[str, Any] = {}
        self._tickets: Dict[str, Issue] = {}
        self._jira = JIRA(
            config.get('jira_url'),
            basic_auth=(
                config.get('jira_username'),
                config.get('jira_password')
            )
        )

    def ticket_exists(self, project: str, title: str) -> bool:
        """
            Checks if a ticket exists with the given title in the given project

            :param project: Project to search for a ticket
            :param title: Title of the ticket we are looking for

            :return: True if a ticket was found False otherwise
        """
        if title in self._tickets:
            return True
        res = self.get_ticket(project, title)
        return bool(res)

    def create_ticket(
            self,
            project: str,
            title: str,
            description: str,
            insight_object_key: Optional[str],
            issue_type: str = 'Bug'
    ):
        """
            Creates a ticket in the given project

            :param project: Jira project the ticket should be created in
            :param title: The desired title of the ticket
            :param description: The description of the ticket
            :param insight_object_key: ID of insight object to link to the ticket
            :param issue_type: Ticket type
        """
        logging.info(f'Creating ticket {title} in project {project} of type {issue_type}')
        issue_dict: Dict[str, Union[str, Dict[str, str], List[Dict[str, str]]]] = {
            'project': {'key': project},
            'summary': title,
            'description': description,
            'issuetype': {'name': issue_type},
        }
        if insight_object_key:
            issue_dict[self._insight_field] = [{"key": f"{insight_object_key}"}]
        self._jira.create_issue(fields=issue_dict)

    def get_ticket(self, project: str, title: str) -> Optional[Issue]:
        """
            Gets the ticket details that match the project and title

            :param project: The Jira project that a ticket will exist in
            :param title: The title of the ticket required

            :return: Ticket details matching the search criteria
        """
        query = f'project={project} AND summary ~ "{title}" AND status not in (Closed,Done,Resolved)'
        res = self._jira.search_issues(query)
        if len(res) == 0:
            return None
        self._tickets[title] = self._jira.search_issues(query)[0]
        return self._tickets[title]

    def get_ticket_by_id(self, ticket_id: str) -> Optional[Issue]:
        """
            Retrieves a ticket by ID

            :param ticket_id: Jira ticket ID

            :return: Ticket matching provided reference number
        """
        # ToDo This will always search if even if we already know the ticket, correct it so that it doesn't
        query = f'issuekey = {ticket_id}'
        res = self._jira.search_issues(query)
        if len(res) == 0:
            return None
        title = self._jira.search_issues(query)[0].fields.summary
        self._tickets[title] = self._jira.search_issues(query)[0]
        return self._tickets[title]

    def update_ticket(self, ticket: Issue, comment: str) -> None:
        """
            Adds a comment to an existing Jira ticket

            :param ticket: Ticket requiring a new comment
            :param comment: Comment to be added
        """
        logging.debug(f'Updating ticket {ticket.key} with comment "{comment}"')
        self._jira.add_comment(ticket.key, comment)

    def get_insight_object_key(self, host: str) -> str:
        """
            Fetches Insight objects matching the IP

            :param host: IP or Hostname of the object to retrieve

            :return:
        """
        if host not in self._insight_objects:
            fields = {
                'iql': f'Hostname = {host} OR IP = {host}',
                'resultPerPage': 1,
            }
            res = self._jira.iql(fields=fields)
            if res.pageSize == 1:
                self._insight_objects[host] = res.objectEntries[0].objectKey

        return self._insight_objects.get(host, '')
