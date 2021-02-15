# Ansible Ticket Creation

The Ansible ticket creation project is intended to allow Ansible
output to be parsed and tickets created for the failures that
occurred.

## Deployment

This application can be deployed as normal using a virtual
environment and pip such as:

```bash
python3 -m venv /opt/ansible_ticket_creation
. /opt/ansible_ticket_creation/bin/activate
pip install ansible_tickets
```

The script also requires a config file such as:

```yaml
jira_url: http://jira.url
jira_username: USERNAME
jira_password: PASSWORD
jira_project: TEST
ticket_type: Task
```
