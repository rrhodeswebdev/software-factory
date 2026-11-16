---
name: factory
description: Runs the factory's scripts so the person never has to remember them. Use for "/factory start", "stop", "status", "pull", "dashboard", "check", or any ask to start, stop, run, watch or show the factory.
---
# factory - run the factory's scripts

Map what the person asked to one row and run its command from the factory root. No argument, or one you can't map: run `status` and list the actions below in one line each.

| Ask | Command | Then tell them |
|---|---|---|
| `start` (watch issues and open the board) | the `watch` and `dashboard` rows, together | both lines below |
| `watch` [minutes] | if `pgrep -f "_tools/factory.py watch"` finds nothing: `mkdir -p .locks && nohup python3 _tools/factory.py watch {minutes or 5} >> .locks/watch.log 2>&1 &` | "Watching every onboarded repo's `factory` issues every {n} min. Log: `.locks/watch.log`." If it was already running, say so and start nothing. |
| `dashboard` | if `pgrep -f "_tools/dashboard.py"` finds nothing: `mkdir -p .locks && nohup python3 _tools/dashboard.py >> .locks/dashboard.log 2>&1 &`; then `open http://127.0.0.1:8787` | "Dashboard: http://127.0.0.1:8787" |
| `stop` | `pkill -f "_tools/factory.py watch"; pkill -f "_tools/dashboard.py"` | Agents already running finish their current stage on their own; nothing new starts. |
| `status` | `python3 _tools/factory.py status`, plus whether `watch` and the dashboard are running (`pgrep -f`) | the lines in plain words: what's running, queued, waiting on them, merged |
| `pull` [repo ...] | `python3 _tools/factory.py pull {repos}` in the background (it can run for an hour); report when it ends | "Working {repos or every repo}'s open `factory` issues once." |
| `check` | `python3 -m unittest _tools/test_factory.py` and `python3 -I _tools/links.py` | pass, or what failed |

Other asks have their own skills: new tasks are [new-task](../new-task/SKILL.md), stopped tasks (feedback, approve, reject) are [unblock](../unblock/SKILL.md), adding a repo is [onboard-repo](../onboard-repo/SKILL.md).

`nohup` keeps `watch` and the dashboard running after this session closes, until `stop` or a restart. To survive restarts, point them at [the schedule setup](../../setup/schedule.md).
