# Lens: security - can someone do or see what they should not

- Authentication on every new route, endpoint, procedure and screen.
- Authorization per object: can user A read or change user B's record by changing an id?
- Input validated at each trust boundary: request bodies, query params, headers, webhooks, file uploads.
- Injection: SQL, shell, HTML/XSS, template, path traversal, SSRF, open redirects.
- Secrets in code, logs, error messages or client bundles; personal data in responses or logs it does not need to be in.
- Webhooks: signature verified before the payload is trusted; replay handled.
- CORS, CSRF and cookie flags changed.
- Rate limits on login, signup, password reset, and anything that costs money per call.
- New dependencies: known vulnerabilities, abandoned, or far more than the job needs.
- Randomness or crypto: a non-cryptographic random for tokens, home-made crypto.
