# Boost Software Support Engineer technical exercise

Welcome, and thanks for taking the time to do this exercise. 👋

This is a small Flask application that mirrors a slice of the
real Boost platform: the part that **emails a distributor's fulfilment team
whenever one of their retailers places an order**.

One of our country teams has reported a problem with it. Your job is to do
what a Software Support Engineer does every day: **reproduce the issue, find the
root cause, ship a fix with a test that stops it coming back, and suggest how we
could make this code better.**

There is no trick and no need to write lots of code. We're far more interested
in how you diagnose the problem and how you communicate about it.

---

## The report

See **[ISSUE.md](ISSUE.md)**. This is the report exactly as it reached us from
the field, so start there.

---

## What we'd like you to do

1. **Reproduce the issue.** Get the app running and confirm the reported
   behaviour for yourself.
2. **Inspect the customer setup.** Use SQL to inspect the customer data behind
   the report and connect what you find to the app behaviour.
3. **Diagnose the root cause.** Find out *why* it happens. Write a short,
   plain language explanation (a few sentences is plenty) in `DIAGNOSIS.md`.
   Imagine you're explaining it to the engineer who will review your fix.
4. **Reply to the country team.** In `COUNTRY_TEAM_REPLY.md`, write the message
   you would send back to the team who filed the report.
5. **Fix it.** Make the smallest sensible change that resolves the issue.
6. **Add a regression test.** Add a test (or tests) that fails before your
   fix and passes after it.
7. **Suggest improvements.** In `IMPROVEMENTS.md`, list 2-5 changes you'd
   consider if this were production code. Focus on reliability, observability,
   correctness, testing, or structure. You don't need to implement these, and
   it's fine to say something is not worth changing.

### Using AI tools

You're welcome to use Claude, Codex, or your preferred AI tools. We use them
every day. What matters is that you **understand and can explain your diagnosis
and your fix**; we may ask you to walk us through your reasoning afterwards.

---

## Getting set up

### Prerequisites

You'll need these installed:

- **[`uv`](https://docs.astral.sh/uv/)**, a Python package and environment manager
- **[`just`](https://github.com/casey/just)**, a command runner
- **`sqlite3`**, the command line SQLite client for inspecting the support data

On macOS with Homebrew:

```bash
brew install uv just
```

(macOS includes `sqlite3` by default. See the `uv` and `just` links above for
Linux/Windows install options.)

### Running it (our convention)

```bash
just bootstrap   # create the venv and install dependencies
just test        # run the test suite
just run         # run the local development server
just lint        # run ruff
```

Run `just` on its own to see all available recipes. The `just test` suite should be green before you start.

### Reproduce the report

With the app running, place a sample order against the seed data and **watch the
server logs**:

```bash
curl -X POST http://localhost:5000/orders/place-sample
```

The seed data (`app/domain/store.py`) is set up to match the report. Compare what
you see in the logs with what you'd expect to happen when an order is placed.

### Inspect the customer data

The same customer setup is available in `data/support.db`. Use SQL to inspect it
as part of your diagnosis:

```bash
sqlite3 data/support.db
```

Start with the customer named in the report and inspect the setup that seems
relevant to order emails.

You are not expected to change the database schema or data. Treat it as a small
support snapshot that helps you understand the report.

---

## Where to look

```
app/
  adapters/notifications.py   # order placed email logic
  mail.py                     # how email is actually sent in each environment
  domain/                     # tiny in-memory models + seed data
  orders/routes.py            # the endpoint that places an order
  templates/email/            # the email template
data/
  support.db                  # small SQLite snapshot of the customer setup
  support.sql                 # SQL used to build the snapshot
tests/
  test_notifications.py       # existing tests
ISSUE.md                      # the report from the field
```

In the real platform these models are backed by PostgreSQL and email is sent via
a Celery task; here everything is kept in memory so it runs anywhere in seconds.

---

## What we're looking for

In rough order of importance:

- **Diagnosis & communication**: a clear, correct, plainly written root cause
  explanation that supports the root cause with evidence from the app and
  customer data, plus a concise and useful reply to the country team.
- **A meaningful regression test**: one that genuinely fails without your fix
  and targets the actual bug, not just the symptom.
- **A clean, minimal fix**: idiomatic, no collateral changes, easy to review.
- **Thoughtful SQL backed diagnosis**: evidence you can inspect customer data
  and connect it to code behaviour.
- **Thoughtful improvement suggestions**: evidence you can spot how to raise the
  bar.

We don't expect you to spend more than **two hours** on this. Please don't
overdo it; if you run short on time, prioritise the diagnosis and the test.

---

## How to submit

Send us your solution as a **zip** of this project, with your changes.

If you use `just package` to create the zip, commit your changes first. The
package recipe builds the archive from committed files only, so uncommitted
changes will not be included.

If you received the exercise as a zip without git history, initialise a local git
repository and make an initial commit before you start:

```bash
git init
git add .
git commit -m "Initial exercise files"
```

If a zip is difficult to send, you can share a **GitHub / GitLab repository**
link instead. If the repository is private, let us know and we'll tell you who
to invite.

Good luck. We're looking forward to reading your diagnosis!
