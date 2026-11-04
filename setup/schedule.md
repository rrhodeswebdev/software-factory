# Schedule - pull ready issues every 30 minutes

One job: run `python3 _tools/factory.py pull` on a timer, so any issue labelled `factory:ready` in an onboarded repo gets built, reviewed, merged and deployed without anyone starting it.

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
