# AGENTS.md

Guidance for AI coding agents working on projects for Aaron.

## Core Working Style

- Prefer action over long advisory prose. If the request is clear enough, inspect the repo, make the change, verify it, and summarize the outcome.
- Ask questions only when a missing answer would materially change the implementation or risk doing the wrong thing.
- Treat "push this to GitHub," "publish this," or "give me the link" as end-to-end work. Implement, commit/push when asked, configure the right host, verify the live result, and return the relevant URLs.
- Separate "stored on GitHub" from "published live." Provide both the repository URL and the live app/site URL when both exist.
- If outside input is required, ask for the exact auth, billing, browser, or deployment step needed. Do not hand back a generic checklist.
- Keep docs and handoff materials demo-safe, submitter-friendly, and accurate to the current app state.

## UI And Product Preferences

- Default to dark mode for dashboards and tools unless the user explicitly asks otherwise.
- Include a visible top-level light/dark toggle when theme switching is relevant. Persist the selected theme in browser storage.
- Put primary user inputs before comparison metrics and results, especially in dashboards.
- Favor quiet, practical, work-focused interfaces over marketing-style pages for SaaS, GovCon, finance, CRM, and operational tools.
- Build the actual usable tool as the first screen. Do not create a landing page unless the request specifically calls for one.
- On mobile, make controls easy to tap. Slider thumbs and other frequent controls should use large touch targets.
- Use clear formatting for financial values, usually full USD formatting such as `$1,000,000.00` where precision matters.
- Keep manual numeric inputs flexible when requested; do not force typed values to stay inside slider bounds unless the spec requires it.

## Engineering Preferences

- Follow existing repo patterns before introducing new abstractions.
- Keep changes scoped to the user request. Avoid broad refactors unless they are necessary to finish safely.
- Add focused tests for calculation logic, data transforms, exports, and behavior that could regress.
- Run the most relevant verification before declaring work complete: build, tests, compile checks, app smoke tests, or live endpoint checks depending on the project.
- When working in Windows/PowerShell, prefer commands that are known to work in this environment: `py`, `npm.cmd`, workspace-local tools, and bundled runtimes when needed.
- Use `rg`/`rg --files` for searching when available.
- Do not commit secrets, `.env` files, raw private downloads, generated database files, or private notes to public/demo repositories.

## Deployment Defaults

- Static React/Vite apps usually belong on GitHub Pages. Configure the correct Vite base path, Pages workflow, and verify a public asset URL or live page after deployment.
- Python/Streamlit apps usually belong on Streamlit Community Cloud, not GitHub Pages. Verify the actual Streamlit URL after deployment.
- For Streamlit Cloud issues, check repo visibility, app entrypoint, import paths, and `requirements.txt` before assuming the app logic is broken.
- Public demo repositories should be safe to make public and should include committed demo data only when that data is public, synthetic, or otherwise safe to share.
- A successful push is not the same as a successful deployment. Confirm the deployed page/app loads.

## Finance Dashboard Defaults

- Preserve the requested calculation model exactly.
- For investment projections, use monthly contributions and monthly compounding when requested. Do not silently substitute year-end lump-sum logic.
- Keep calculation logic testable and separate enough to validate independently from the UI.
- Support exports when requested, typically CSV first and Excel when useful. Lazy-load heavier export libraries such as `xlsx`.

## GovCon And Demo App Defaults

- For GovCon demos, prefer clear offline/demo behavior when API keys are absent.
- Use public USAspending or synthetic data for public demos unless explicitly provided with another safe source.
- Keep scope boundaries explicit: no real auth, no paid APIs, no real operational data, no production claims unless they are actually implemented.
- Include concise demo scripts and pre-demo checklists when preparing a repo for recording, review, or submission.

## Communication

- Final responses should be concise and concrete: what changed, where it is, what was verified, and any remaining blocker.
- When a live link exists, include it plainly. When it does not exist yet, say what is missing.
- If a command cannot be run or verification is blocked, state that directly and explain the next required step.
