# Lens: performance - will it hold at real size

Report only with a plausible trigger: the data size or request rate at which it bites.

- Server: queries in loops (N+1), new query patterns with no index, unbounded queries with no pagination, blocking I/O on a request path, work repeated per request that could be done once.
- Payloads: responses or props carrying far more than the screen uses.
- Web: bundle added to the critical path, client components that could be server-rendered, needless re-renders, images without sizes, layout shift, render-blocking scripts.
- Mobile: long lists not virtualized, work on the JS thread during animation, images not cached.
- Background: jobs with no batching, no timeout, or retries that can storm.
