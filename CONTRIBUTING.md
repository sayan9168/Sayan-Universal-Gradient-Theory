# Contributing

Thank you for taking the time to improve Sayan Universal Gradient Theory (SUG).
Contributions are welcome, including careful criticism of the assumptions and
predictions as well as improvements to the software and documentation.

## Project and scientific status

SUG is a speculative theoretical proposal, not an established or empirically
validated theory. Its equations and numerical implementation make the proposal
explicit and reproducible; they do not demonstrate that its physical claims are
true. Please distinguish assumptions, mathematical consequences, model
calculations, and observations in discussions and contributions. The current
limitations and validation agenda are described in
[`paper/open_questions.md`](paper/open_questions.md).

## Before you start

- Read the relevant material in `paper/`, especially
  [`formal_framework.md`](paper/formal_framework.md),
  [`predictions.md`](paper/predictions.md), and
  [`open_questions.md`](paper/open_questions.md).
- For substantial changes to behavior or theory assumptions, open an issue or
discussion first so the scope and rationale can be agreed on.
- Use the repository's issue templates for bug reports, feature requests, and
theory discussions. Search existing issues before opening a duplicate.

## Development setup

The package metadata requires Python 3.9 or later; current classifiers list
Python 3.9–3.12. To create a local development environment and install the
project with its optional development dependencies:

```bash
python -m venv .venv
# Activate the environment:
# macOS / Linux: source .venv/bin/activate
# Windows:      .venv\Scripts\activate
python -m pip install --upgrade pip
python -m pip install -e ".[all]"
```

Run the test suite from the repository root:

```bash
python -m pytest -q
```

For a smaller environment focused on tests, install `.[test]` instead of
`.[all]`. If a change affects numerical behavior, include or update tests that
cover the relevant valid-input, boundary, and invalid-input cases.

## Contribution guidelines

### Software and examples

- Keep changes focused and consistent with the surrounding code and public API.
- Preserve the project's supported Python versions and document any new
dependencies or user-visible behavior.
- Make examples reproducible: state the inputs, reference scales, and units (or
  explicitly say when quantities are dimensionless).
- Do not present illustrative plots or outputs from the model as experimental
  evidence.

### Theory and documentation

- State assumptions and definitions before using them; keep notation consistent
  with the formal framework.
- Show intermediate steps for new derived relations and explain their domains
  and limits. In particular, the dimensionless field is defined for `x > 1`.
- Identify what could falsify a proposed claim. Cite sources for external facts,
  and separate established results from SUG postulates or open questions.
- Update nearby documentation when a contribution changes a formula, an
  interpretation, or a user-facing workflow.

There is no repository-wide formatter or linter configuration at present. Keep
style consistent with adjacent files and avoid unrelated formatting changes.

## Pull requests

Please keep each pull request focused and provide:

1. A concise description of the change and the problem it addresses.
2. The reasoning behind any mathematical or scientific claim, with references
   where useful.
3. The commands run to check the change and their results. Mention clearly if
   tests could not be run.
4. Any relevant limitations, compatibility considerations, or follow-up work.

Before submitting, review the pull request checklist in
[`.github/PULL_REQUEST_TEMPLATE.md`](.github/PULL_REQUEST_TEMPLATE.md). Be
respectful and constructive in review; this project follows the
[Contributor Covenant](CODE_OF_CONDUCT.md).
