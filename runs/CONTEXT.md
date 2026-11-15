# runs - one folder per run

Shelf of product. Each run is `runs/{YYYY-MM-DD}-{repo}-{slug}/`, started by copying `_templates/run.md` to `RUN.md` inside it. Its shape and status rules live in the root [CONTEXT.md](../CONTEXT.md). Never hand-edit a stage's output from another stage; fix the stage and rerun it.

Runs are local to this machine (git ignores them), so the public factory repo never carries your specs, reviews or logs.
