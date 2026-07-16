# SETUP — manual steps for quant-ai

Scaffolded by `teaching-content/tools/new_course.py`. The local kit is
complete (`make check` passes; `make build` works). Everything below is
the manual wiring a new course still needs. Delete this file when done.

## 1. GitHub repo

```sh
gh repo create MarkHendricks/quant-ai --private --source . --push=false
git remote add origin git@github.com:MarkHendricks/quant-ai.git
```

Do NOT push yet — pushing `main` IS the deploy (it triggers the Pages
Action). Finish steps 2-3 first.

## 2. CI deploy key (read access to teaching-content)

CI checks out the private canonical repo at the pinned SHA. It needs a
per-repo read-only deploy key on teaching-content, stored as an Actions
secret here (exactly what finm-genai needed on 2026-07-01):

```sh
ssh-keygen -t ed25519 -f /tmp/quant-ai-ci -N "" -C "quant-ai CI"
gh repo deploy-key add /tmp/quant-ai-ci.pub -R MarkHendricks/teaching-content --title "quant-ai CI (read-only)"
gh secret set TEACHING_CONTENT_DEPLOY_KEY -R MarkHendricks/quant-ai < /tmp/quant-ai-ci
rm /tmp/quant-ai-ci /tmp/quant-ai-ci.pub
```

(`deploy-key add` is read-only unless `--allow-write` is passed.)

## 3. GitHub Pages

Enable Pages with the Actions build type:

```sh
gh api -X POST repos/MarkHendricks/quant-ai/pages -f build_type=workflow
```

(Or Settings -> Pages -> Source: GitHub Actions.)

## 4. Branding

- Replace `docs/_static/logo.svg` and `docs/_static/favicon.svg`.
- Set the brand colors in `docs/_static/custom.css`.
- Fill in `docs/index.md` (description, data-folder and submission URLs).
- Check `docs/_config.yml`: title, copyright, repository URL.

## 5. Student data channel (Box)

- If the course ships data to students: set `BOX` in the Makefile to the
  course Box folder and use `make boxsync`. Box is the ONLY student data
  channel; the repo and site ship none.
- If not (finm-genai pattern): leave `BOX` empty; boxsync stays disabled.
- Record the decision in this repo's CLAUDE.md.

## 6. Content

- Fill the `course/discussions/` namesakes (Introduction, Notation; the
  Data Dictionary anchor text is usually fine as is).
- Write the manifest in `content.yml` (see the commented example chapter).
- `make pin` after any canonical change (push canonical first).
- `make check` and `make build`; preview with `make serve`.

## 7. First deploy

- `make pin && make check`, commit, then push `main` — that IS the deploy.
- Verify the Action goes green and the Pages URL renders.
- Deploy guardrails: `../teaching-content/shell/CLAUDE.md`.
