# Autonomous Media Pipeline

A GitHub Actions workflow for processing **owned or explicitly licensed** media.

## Setup

1. Add `SOURCE_CHANNELS` as a repository secret with newline-separated authorized URLs.
2. Configure YouTube OAuth using the official Google OAuth consent flow. Add the authorized token JSON as `YOUTUBE_TOKEN_JSON` and the OAuth client JSON as `YOUTUBE_CLIENT_SECRETS_JSON` (the client JSON is retained for setup/documentation; the workflow does not bypass OAuth).
3. Review attribution, license conditions, and made-for-kids requirements before public publication.
4. The uploader defaults to **private** so a human can review the result before publishing.

The workflow processes one newest video per run, limits it to 55 seconds, formats it vertically, and removes temporary media in `finally` and in the workflow's `always()` cleanup step.

The script intentionally does not use browser cookies, bypass login/OAuth, alter pitch/speed to disguise a source, or automatically publish third-party material publicly.
