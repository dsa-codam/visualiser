---
name: create-issue
description: Turn the user's notes or ideas (English or Ukrainian, one or a list) into GitHub issues on the "Visualiser backlog" project of dsa-codam/visualiser. Use when the user asks to add tasks, ideas, notes or issues to the backlog, or pastes a list of ideas to file as issues.
---

# Create backlog issues

Turn the user's notes into issues in `dsa-codam/visualiser` and put them on the
"Visualiser backlog" project with **Status = Todo** and **Plan = Thinking**.

## Fixed IDs

| What | Value |
|---|---|
| Repo | `dsa-codam/visualiser` |
| Project | "Visualiser backlog", org `dsa-codam`, number `1`, id `PVT_kwDODwpkxc4Bmjl7` |
| Status field | `PVTSSF_lADODwpkxc4Bmjl7zhlMIP4`, option **Todo** = `f75ad846` |
| Plan field | `PVTSSF_lADODwpkxc4Bmjl7zhlM8Go`, option **Thinking** = `199269d4` (Settled = `e3355890`, never set it) |

`scripts/add-to-backlog.sh` uses these IDs. If a `gh` call says a field or option
does not exist, look the IDs up again, and tell the user before changing anything.

## Steps

### 1. Check access
Run `gh auth status`. If it isn't logged in, or the scopes lack `project`, ask the
user to run `! gh auth login --scopes project` (or `! gh auth refresh -s project`) and stop.

### 2. Read the existing backlog
```bash
gh issue list -R dsa-codam/visualiser --state open --limit 200 --json number,title,body
```
Read the titles and bodies of the open issues before you draft anything.

### 3. Split the notes
Make one issue per note or idea. If two notes in the batch look like the same
thing, ask the user whether to combine them; don't combine them yourself.

### 4. Draft each issue
- **Only what the user said.** Rephrase and fix grammar, but never add facts, reasons, steps,
  options, examples, priorities or acceptance criteria the user did not give.
  - Detailed plan given → keep all of it, in the same structure.
  - "Decide how to do A" → the issue says to decide how to do A. No invented plan.
  - A note that is only a title → title only, empty body. Don't pad it.
  - A question in the note stays a question; don't answer it.
- **Title:** short and specific. Drop prefixes like "visualiser –" (every issue is in that repo).
- **No labels, assignees or milestones.**

### 5. Check for overlap with existing issues
For each draft, compare it with the open issues from step 2. If it looks like the same
problem, or part of an existing issue, name that issue (`#N title`) and ask the user to pick:
- **skip:** create nothing
- **comment:** add the note as a comment on `#N`
- **sub-issue:** create it as a sub-issue of `#N`
- **separate:** create it as a separate issue

Never choose for the user. Never skip or merge on your own.

### 6. Show the drafts and wait
Show every draft: its number in the batch, title, body (or "title only"), and any
overlap question from step 5. Create nothing until the user says OK. Apply
corrections, and show the drafts again if the changes are large.

### 7. Create
Write each body to a file in the scratchpad (avoids shell-quoting problems), then:

```bash
# separate issue
gh issue create -R dsa-codam/visualiser --title "<title>" --body-file <file>
# sub-issue of #N
gh issue create -R dsa-codam/visualiser --title "<title>" --body-file <file> --parent N
# comment on #N (no new issue, no project fields to set)
gh issue comment N -R dsa-codam/visualiser --body-file <file>
```
For a title-only issue, use `--body ""` instead of `--body-file`.

Then, for every **new** issue (separate or sub-issue):
```bash
.claude/skills/create-issue/scripts/add-to-backlog.sh <issue-number>
```
This adds the issue to the project if it isn't there yet (the project auto-adds new issues,
so `gh project item-add` alone can fail with "Content already exists"). It also sets
Status = Todo and Plan = Thinking, and prints the values it stored. If any line doesn't show
`Status=Todo Plan=Thinking`, fix that item before reporting.

Handle each issue on its own, so that one failure doesn't stop the rest. Report any
failure exactly.

### 8. Report
Show a table with each issue's number, link and title, and for comments, the link to the
comment. Mention anything that failed or needed a retry.
