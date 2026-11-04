# Schedule - pull ready issues every 30 minutes

One job: run `python3 _tools/factory.py pull` on a timer. In every onboarded repo, an issue labelled `factory:idea` becomes a full run from brainstorm to deploy (the idea issue closes when every task is deployed), and an issue labelled `factory:ready` gets built, reviewed, merged and deployed.

## Turn it on
```
cp setup/local.software-factory.plist ~/Library/LaunchAgents/
launchctl load ~/Library/LaunchAgents/local.software-factory.plist
```
It uses a login shell, so `claude`, `gh` and `python3` resolve as they do in your terminal. Output goes to `/tmp/software-factory.log`. A pull that is still running when the next one starts makes the new one exit, and a run already being driven by `new` or `resume` is left alone.

## Turn it off
```
launchctl unload ~/Library/LaunchAgents/local.software-factory.plist
```

## Check
After the first interval, `tail /tmp/software-factory.log` shows the pull ran, and `python3 _tools/factory.py status` lists any task it picked up.
