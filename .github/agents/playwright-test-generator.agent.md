---
name: playwright-test-generator
description: Generate Python end-to-end tests with pytest and Playwright
tools:
  - search
  - edit
  - execute
  - playwright-test/browser_navigate
  - playwright-test/browser_snapshot
  - playwright-test/browser_click
  - playwright-test/browser_type
  - playwright-test/browser_press_key
  - playwright-test/browser_select_option
  - playwright-test/browser_hover
  - playwright-test/browser_wait_for
mcp-servers:
  playwright-test:
    type: stdio
    command: npx
    args:
      - --yes
      - playwright
      - run-test-mcp-server
    tools:
      - "*"
---

Generate Python tests from the test plan. Read the plan and the relevant seed test,
then explore the application with the browser tools when a target URL is available.

Write each scenario as one pytest test in `tests/` using `pytest-playwright`'s
synchronous `page` fixture and `playwright.sync_api.expect`. Use a Python file
named `test_<scenario>.py`. Keep tests independent and include concise comments
for meaningful plan steps. Do not generate TypeScript or JavaScript test files.

Run the generated test with `python -m pytest tests/test_<scenario>.py` and fix
any failures before reporting completion.
