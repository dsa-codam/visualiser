#!/usr/bin/env python3
"""Print the open issues of dsa-codam/visualiser as a tree of issues and sub-issues.

Usage: python3 tools/issues.py
Needs the GitHub CLI (gh), logged in. Read only: it never changes an issue.
"""
import json
import subprocess
import sys

REPO_OWNER = "dsa-codam"
REPO_NAME = "visualiser"

QUERY = """
query($owner: String!, $name: String!) {
  repository(owner: $owner, name: $name) {
    issues(states: OPEN, first: 100, orderBy: {field: CREATED_AT, direction: ASC}) {
      nodes {
        number
        title
        parent { number state }
        subIssues(first: 50) { nodes { number title state } }
      }
    }
  }
}
"""


def fetch():
    cmd = ["gh", "api", "graphql",
           "-f", "query=" + QUERY,
           "-F", "owner=" + REPO_OWNER,
           "-F", "name=" + REPO_NAME]
    try:
        out = subprocess.run(cmd, capture_output=True, text=True, check=True).stdout
    except FileNotFoundError:
        sys.exit("gh is not installed. Install it with: brew install gh")
    except subprocess.CalledProcessError as e:
        sys.exit("gh failed:\n" + e.stderr.strip())
    return json.loads(out)["data"]["repository"]["issues"]["nodes"]


def main():
    issues = fetch()
    if not issues:
        print("No open issues.")
        return
    # Top level: open issues with no parent, or whose parent is already closed.
    top = [i for i in issues if not i["parent"] or i["parent"]["state"] != "OPEN"]
    for issue in top:
        note = ""
        if issue["parent"]:
            note = f"  (parent #{issue['parent']['number']} is closed)"
        print(f"#{issue['number']:<4} {issue['title']}{note}")
        subs = issue["subIssues"]["nodes"]
        for k, sub in enumerate(subs):
            branch = "└" if k == len(subs) - 1 else "├"
            print(f"   {branch} #{sub['number']:<4} {sub['title']}  [{sub['state'].lower()}]")


if __name__ == "__main__":
    main()
