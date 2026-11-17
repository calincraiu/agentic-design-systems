---
name: start-course
description: Starts the course app (the slides and live widgets) and opens it in the browser. Use when the student says start, open the course, open the slides, or the app.
---

# Start the course app

1. Tell the student, in one sentence, that you're starting a small web server on their own computer. Nothing goes on the internet.
2. Run `uv run course` **in the background**, so the conversation can carry on.
3. When it prints `Course app running at http://...`, give the student that address as a link. The browser should open by itself; if it doesn't, they can click the link.
4. Explain: the app keeps running while this session is open. If the page stops responding, run `/start-course` again.

If it fails because `uv` isn't found or something is missing, suggest `/setup-course`.

Students can also start the app without Claude: double-click `Start course.cmd` on Windows, or `Start course.command` on a Mac.
