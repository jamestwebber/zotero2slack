# this is what I built the thing for: reading papers from a JSON Zotero feed
# and writing them out to Slack

import os
import requests

# this formats a JSON entry and makes a nice Slack message with
# the person who added it, the paper title and journal, and a link
def format_json(entry):
    name = entry['meta']['createdByUser']['name'] or entry['meta']['createdByUser']['username']
    return '{creator} added <{url}|{title}> - {journalAbbreviation}'.format(
        creator=name, **entry['data'])


# this is a hook for taking the new entries and sending them to a Slack app
# that will post them in the chat.
def output_entries(entries, cachefile=None):
    if cachefile is not None:
        with open(cachefile) as f:
            recent = [line.strip() for line in f]

    for entry in entries:
        if entry not in recent:
            payload = {'channel': '#general', 'username': 'Zotero', 'text': entry}
            requests.post(url=os.environ['SLACK_WEBHOOK'], json=payload)
            recent.append(entry)

    if cachefile is not None:
        with open(cachefile, 'w') as OUT:
            print >> OUT, '\n'.join(entries[-5:])
