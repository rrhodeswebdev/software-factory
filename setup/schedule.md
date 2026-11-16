# Schedule - keep the factory working without a terminal open

`python3 _tools/factory.py watch` pulls every five minutes and starts new work at once. Run it in a terminal tab, or let macOS keep it alive with launchd:

1. Save as `~/Library/LaunchAgents/local.software-factory.plist`, with your factory path in both places:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0"><dict>
  <key>Label</key><string>local.software-factory</string>
  <key>ProgramArguments</key><array>
    <string>/bin/zsh</string><string>-lc</string>
    <string>cd /path/to/software-factory &amp;&amp; exec python3 _tools/factory.py watch 5</string>
  </array>
  <key>RunAtLoad</key><true/>
  <key>KeepAlive</key><true/>
  <key>StandardOutPath</key><string>/path/to/software-factory/.locks/watch.log</string>
  <key>StandardErrorPath</key><string>/path/to/software-factory/.locks/watch.log</string>
</dict></plist>
```

2. `mkdir -p .locks` in the factory (the log goes there), then `launchctl load ~/Library/LaunchAgents/local.software-factory.plist` to start; `launchctl unload` the same path to stop.

`zsh -lc` gives it your login PATH, so `claude`, `gh`, `git` and the repos' own tools (bun, node) are found. `gh` and `claude` must already be signed in.

The dashboard (`python3 _tools/dashboard.py`) shows whether a runner is alive and when it last pulled.
