#!/usr/bin/env python3

"""Transform Read The Docs webhook data into Slack webhook data

This script is used By Zapier to transform the webhook data sent by Read The
Docs into data that can be sent to Slack.
"""

import json

GH_ORG = "doitintl"
GH_REPO = "docs-sphinx-cmp"
GH_REPO_URL = f"https://github.com/{GH_ORG}/{GH_REPO}"
RTD_ORG = "doit-international"
RTD_PROJECTS = "readthedocs.com/projects"
RTD_SLUG = f"{RTD_ORG}-{GH_REPO}"
SLACK_FAVICON = "https://slack.github.com/static/img/favicon-neutral.png"

# From the Read The Docs documentation, we expect the incoming webhook data to
# look like the `examples/incoming.json` file.

# In Zapier, we map the  webhook data a dict with the structure below. The
# conditional creates the dict with some example values so we that can test
# this script without any input data.
if "input_data" not in locals():
    input_data = {
        "event": "build:passed",
        "name": GH_REPO,
        "slug": RTD_SLUG,
        "version": "latest",
        "commit": "b726f01758b17dee47dbf544e7ffe2b80a4fb1a1",
        "build": "783488",
        "start_date": "2021-11-25T17:26:39",
        "build_url": f"https://{RTD_PROJECTS}/{RTD_SLUG}/builds/783488/",
        "docs_url": f"https://{RTD_SLUG}.readthedocs-hosted.com/en/latest/",
    }


def main():
    """Handle the input dict and return an output dict."""

    build_str = f"Build <{input_data['build_url']}|{input_data['build']}>"

    commit_str = ""
    # The `commit` key may be an empty string (e.g. when a build is triggered
    # by hand instead of from an incoming GitHub webhook)
    if input_data["commit"]:
        commit_url = f"{GH_REPO_URL}/commit/{input_data['commit']}"
        # GitHub trims commit hashes to seven characters
        commit_short = input_data["commit"][:7]
        commit_str = f"for commit <{commit_url}|{commit_short}>"

    color = ""
    message = ""
    if input_data["event"] == "build:triggered":
        color = "warning"
        message = f"{build_str} triggered {commit_str}"
    if input_data["event"] == "build:failed":
        color = "danger"
        message = f"{build_str} failed {commit_str}"
    if input_data["event"] == "build:passed":
        color = "good"
        message = f"{build_str} passed {commit_str}"

    footer = f"<{input_data['docs_url']}|{input_data['docs_url']}>"

    json_dict = {
        "attachments": [
            {
                "text": message,
                "fallback": "",
                "pretext": "",
                "color": color,
                "mrkdwn_in": ["text"],
                "footer": footer,
                "footer_icon": SLACK_FAVICON,
            }
        ]
    }

    return {"json": json.dumps(json_dict, indent=4, sort_keys=True)}


if __name__ == "__main__":
    output = main()
    print(output["json"])
