#!/usr/bin/env bash
# Put an issue on the "Visualiser backlog" project and set Status = Todo, Plan = Thinking.
# Usage: add-to-backlog.sh <issue-number>
# Prints: #<number> <url> Status=<..> Plan=<..>
set -euo pipefail

REPO_OWNER=dsa-codam
REPO_NAME=visualiser
PROJECT_NUMBER=1
PROJECT_ID=PVT_kwDODwpkxc4Bmjl7
STATUS_FIELD=PVTSSF_lADODwpkxc4Bmjl7zhlMIP4
STATUS_TODO=f75ad846
PLAN_FIELD=PVTSSF_lADODwpkxc4Bmjl7zhlM8Go
PLAN_THINKING=199269d4

n=${1:?issue number required}
url="https://github.com/$REPO_OWNER/$REPO_NAME/issues/$n"

# The project auto-adds new repo issues, so the item may already exist (or appear
# while we are adding it). Look it up first; add only if missing.
find_item() {
  gh api graphql -F n="$n" -f query='query($n:Int!){repository(owner:"dsa-codam",name:"visualiser"){issue(number:$n){projectItems(first:20){nodes{id project{id}}}}}}' \
    --jq ".data.repository.issue.projectItems.nodes[] | select(.project.id==\"$PROJECT_ID\") | .id"
}

item=$(find_item)
if [ -z "$item" ]; then
  item=$(gh project item-add "$PROJECT_NUMBER" --owner "$REPO_OWNER" --url "$url" --format json --jq .id 2>/dev/null || true)
  [ -n "$item" ] || item=$(find_item)
fi
[ -n "$item" ] || { echo "could not find or add project item for #$n" >&2; exit 1; }

gh project item-edit --id "$item" --project-id "$PROJECT_ID" \
  --field-id "$STATUS_FIELD" --single-select-option-id "$STATUS_TODO" >/dev/null
gh project item-edit --id "$item" --project-id "$PROJECT_ID" \
  --field-id "$PLAN_FIELD" --single-select-option-id "$PLAN_THINKING" >/dev/null

# Verify what is actually stored.
gh api graphql -f query="{node(id:\"$item\"){... on ProjectV2Item{s:fieldValueByName(name:\"Status\"){... on ProjectV2ItemFieldSingleSelectValue{name}} p:fieldValueByName(name:\"Plan\"){... on ProjectV2ItemFieldSingleSelectValue{name}}}}}" \
  --jq "\"#$n $url Status=\" + (.data.node.s.name // \"-\") + \" Plan=\" + (.data.node.p.name // \"-\")"
