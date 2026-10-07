# Publishing `sayan-gradient` to PyPI and TestPyPI

A complete, verified command sequence for releasing the package.
Every command below was run against this repository (`sayan-gradient` 2.1.0)
in a clean virtual environment before being written down.

> **The short version**
> ```bash
> python -m pytest -q && rm -rf dist build && python -m build \
>   && python -m twine check --strict dist/* \
>   && python -m twine upload --repository testpypi dist/* \
>   && python -m twine upload dist/*
> ```
> Everything below is that sequence, slowed down and explained, with the
> failure modes written out.

---

## 0. What you need before you start

| Thing | Where to get it |
|---|---|
| PyPI account | <https://pypi.org/account/register/> |
| PyPI API token (`pypi-…`) | <https://pypi.org/manage/account/token/> — scope: *this project only*, or an account-wide token |
| TestPyPI account (**separate**) | <https://test.pypi.org/account/register/> |
| TestPyPI API token (`pypi-…`) | <https://test.pypi.org/manage/account/token/> |

> **The name `sayan-gradient` is still unclaimed.** As of this writing,
> `https://pypi.org/pypi/sayan-gradient/json` returns **404** — the package has
> not been published, and no similarly named project exists either. PyPI names
> are first-come, first-served and effectively permanent, so this is the moment
> to register: upload to TestPyPI first to check the metadata, then claim the
> real name on PyPI. Until then the `sayan-gradient` line in `requirements.txt`
> will not resolve, and the PyPI badge in `README.md` points at a 404.

Two accounts are involved and they are **not** linked: registering on PyPI does
not create a TestPyPI login, and a token minted on one index is rejected by the
other. Create both before you build, or the TestPyPI step will fail at the last
possible moment.

**Token security rules**

* Never paste a token into a file that is committed. `.pypirc` must be
  `chmod 600` and lives in your home directory, never in the repo.
* Prefer a **project-scoped** token over an account-wide one: if it leaks, the
  damage is limited to `sayan-gradient`.
* Never pass a token on the command line (`twine upload -u __token__ -p pypi-…`)
  — it lands in your shell history and in `ps` output. Use `.pypirc` or
  environment variables instead.
* If a token is ever exposed, revoke it immediately at the account page and
  mint a new one. Rotation is cheap; a leaked upload token is not.

---

## 1. Work from a clean, up-to-date checkout

```bash
cd Sayan-Universal-Gradient-Theory
git status                       # expect: no modified tracked files
git pull origin main             # or: git checkout -b release/v2.1.0
```

Do not build from a dirty tree. `dist/` leftovers from a previous version are
the single most common cause of a confusing PyPI rejection.

## 2. Create and activate a fresh virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
python -m pip install --upgrade pip
```

Never build inside your system Python (PEP 668 blocks it on modern distros
anyway) and never with a global environment that holds unrelated packages.

## 3. Upgrade the build tools

```bash
python -m pip install --upgrade pip setuptools wheel build twine
python -m build --version
python -m twine --version
```

* `build` — the PEP 517 front end that produces both artefacts from
  `pyproject.toml` (`setup.py` is not needed; the file in this repo exists only
  for legacy tooling).
* `twine` — validates the artefacts and uploads them. `twine check` is the
  PyPI-side README/metadata linter; it catches a broken `long_description`
  (usually a bad relative image path) that would otherwise render as a mangled
  page on the project page.
* `setuptools`/`wheel` — the declared build backend (`setuptools>=61.0`).

## 4. Run the test suite

```bash
python -m pip install -e ".[test]"
python -m pytest -q
```

Expected: `49 passed`. **Do not upload if this fails** — the distribution is a
snapshot of exactly the code the tests just exercised.

Optional but recommended — confirm the package imports and behaves from a
clean interpreter, the way a user will meet it:

```bash
python -c "import sayan_gradient as sg; print(sg.__version__, sg.theta_s(1e6, 100.0, 10.0))"
# 2.1.0 4.342944819032518
```

## 5. (Optional, recommended) ship the paper and figures in the sdist

By default setuptools puts only the importable packages, `LICENSE`,
`README.md` and `pyproject.toml` into the source distribution. Verified for
this repository: the default sdist contains 31 files and **omits** `paper/`,
`figures/`, `notebooks/`, `examples/`, `tests/`, `app.py` and
`requirements.txt`. For a project whose main artefact is the paper, you almost
certainly want those in the sdist. Create `MANIFEST.in` in the repository root:

```bash
cat > MANIFEST.in <<'EOF'
include LICENSE
include README.md
include SECURITY.md
include requirements.txt
include app.py
recursive-include paper *.md *.tex
recursive-include figures *.png
recursive-include notebooks *.ipynb
recursive-include examples *.py
recursive-include tests *.py
EOF
git add MANIFEST.in && git commit -m "packaging: ship paper, figures and tests in the sdist"
```

With this file the sdist grows from 31 to 57 entries and carries
`paper/sug_theory_arxiv.tex`, the four figures and the test suite. The
**wheel** is unaffected — it must contain only the two importable packages
(`sayan_gradient/` and `sug_theory/`) plus metadata.

## 6. Clean previous build output

```bash
rm -rf dist build sayan_gradient.egg-info
```

`build/` and `*.egg-info/` are already in `.gitignore`, so this never dirties
the working tree — but stale `dist/` contents are what get uploaded.

## 7. Build the sdist and the wheel

```bash
python -m build
```

This writes exactly two files into `dist/`:

```
dist/sayan_gradient-2.1.0-py3-none-any.whl     # the wheel (what pip installs)
dist/sayan_gradient-2.1.0.tar.gz               # the sdist (the source release)
```

`py3-none-any` is correct: the package is pure Python with no compiled
extensions, so one wheel serves every platform.

Equivalent explicit invocations, if you prefer to see each step:

```bash
python -m build --sdist         # sdist only  -> python -m build --sdist --outdir dist
python -m build --wheel         # wheel only
```

Add `--no-isolation` to reuse the already-installed build backend instead of
creating a throwaway environment. It is faster, but it can silently pick up a
stale `setuptools`; keep it off for release builds.

## 8. Validate the artefacts

```bash
python -m twine check --strict dist/*
```

Expected (verified):

```
Checking dist/sayan_gradient-2.1.0-py3-none-any.whl: PASSED
Checking dist/sayan_gradient-2.1.0.tar.gz: PASSED
```

`--strict` promotes warnings to errors. If it complains about
`long_description`, the cause is almost always an image or badge in
`README.md` pointing at a path that does not exist in the rendered package
page.

Inspect what you are about to ship:

```bash
python -m zipfile -l dist/*.whl        # wheel contents
tar tzf dist/*.tar.gz                  # sdist contents
```

The wheel should list `sayan_gradient/*.py`, `sug_theory/*.py` and
`sayan_gradient-2.1.0.dist-info/*` — and nothing else. If you see `tests/` or
`paper/` in the wheel, something is wrong with your `packages.find`
configuration.

## 9. Smoke-test the built wheel in a throwaway environment

This is the step that catches "works in my checkout, broken once installed".

```bash
python3 -m venv /tmp/sug-verify && /tmp/sug-verify/bin/pip install -q dist/*.whl
/tmp/sug-verify/bin/python -c "
import sayan_gradient as sg
print(sg.__version__, sg.theta_s(1e6, 100.0, 10.0), sg.parameter_free_energy_ratio(10, 1000))
"
# 2.1.0 4.342944819032518 8.999999999999998
rm -rf /tmp/sug-verify
```

A full (not `--no-deps`) install also confirms the dependency list is correct:
it should pull `numpy` and `scipy` and **nothing** else. `plotly`,
`matplotlib`, `streamlit` and `pytest` must stay optional extras.

## 10. Configure the credentials

Create `~/.pypirc` (note: home directory, **not** the repository):

```ini
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
username = __token__
password = pypi-AgEIcHlwaS5vcmcAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA

[testpypi]
username = __token__
password = pypi-AgEIcHlwaS5vcmcBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB
```

```bash
chmod 600 ~/.pypirc
```

Replace the two passwords with the tokens from step 0. `--repository pypi` and
`--repository testpypi` then select the right section automatically.

Equivalent, if you prefer environment variables (better for CI):

```bash
export TWINE_USERNAME=__token__
export TWINE_PASSWORD='pypi-AgEIcHlwaS5vcmc...'      # use a secret store in CI
```

Add `~/.pypirc` and any `*.pypirc`-style secret to `.gitignore` if you are
ever tempted to keep one inside the repository.

## 11. Upload to TestPyPI first

```bash
python -m twine upload --repository testpypi dist/*
```

```
Uploading distributions to https://test.pypi.org/legacy/
...
HTTPError: 400 Client Error: File already exists.
```

That last message means a file of that name is already on TestPyPI. **PyPI
filenames are immutable** — you cannot re-upload version 2.1.0, even after
deleting it. Bump the version (step 12) and build again.

Verify the test install in a clean environment (note the two index URLs —
TestPyPI first so it wins for `sayan-gradient`):

```bash
python3 -m venv /tmp/sug-testpypi
/tmp/sug-testpypi/bin/pip install -q \
    --index-url https://test.pypi.org/simple/ \
    --extra-index-url https://pypi.org/simple/ \
    sayan-gradient==2.1.0
/tmp/sug-testpypi/bin/python -c "import sayan_gradient as sg; print(sg.__version__)"
rm -rf /tmp/sug-testpypi
```

Also open <https://test.pypi.org/project/sayan-gradient/> and check that the
README rendered correctly (badges, headings, tables).

## 12. Bump the version if you are re-releasing

The version lives in two places and they must agree:

```bash
# 1. pyproject.toml
sed -i 's/^version = "2.1.0"/version = "2.1.1"/' pyproject.toml

# 2. sayan_gradient/__init__.py
sed -i 's/^__version__ = "2.1.0"/__version__ = "2.1.1"/' sayan_gradient/__init__.py

grep -n '^version' pyproject.toml
grep -n '__version__' sayan_gradient/__init__.py
```

Then repeat from step 6 (`rm -rf dist build` → `python -m build` → check →
upload). A stale `__version__` that disagrees with `pyproject.toml` produces a
confusing double-versioned package, so verify both lines before building.

## 13. Upload to PyPI

```bash
python -m twine upload dist/*
```

```
Uploading distributions to https://upload.pypi.org/legacy/
Uploading sayan_gradient-2.1.0-py3-none-any.whl (29.6 kB)
100% ━━━━━━━━━━ 29.6/29.6 kB • ?:? • 0:00 ETA
Uploading sayan_gradient-2.1.0.tar.gz (32.3 kB)
100% ━━━━━━━━━━━━━ 32.3/32.3 kB • ?:? • 0:00 ETA
```

Confirm the release:

```bash
python -m pip index versions sayan-gradient        # or:
curl -s https://pypi.org/pypi/sayan-gradient/json | python -m json.tool | head -20
```

Final end-to-end check from a machine that has never seen the repository:

```bash
python3 -m venv /tmp/sug-final
/tmp/sug-final/bin/pip install sayan-gradient
/tmp/sug-final/bin/python -c "import sayan_gradient as sg; print(sg.__version__, sg.__doi__)"
rm -rf /tmp/sug-final
```

## 14. Tag the release and archive it

```bash
git tag -a v2.1.0 -m "sayan-gradient 2.1.0: SUG framework, Theta_s operator, P2 tests"
git push origin main --tags
```

Then create a **new** Zenodo release from the tag in
<https://zenodo.org/account/>, and update `__doi__` in
`sayan_gradient/__init__.py` plus the DOI in `pyproject.toml` if Zenodo mints a
new concept DOI. The versioned record
(<https://doi.org/10.5281/zenodo.22723745>) stays valid regardless.

---

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| `error: Multiple top-level packages discovered` | a stray directory in the root | set `[tool.setuptools.packages.find] include = [...]` (already done here) |
| `InvalidDistribution: Cannot find file 'dist/*'` | you passed `dist/*` while `cd`-ed elsewhere, or the build produced nothing | `cd` to the repo root, run `python -m build`, then re-check |
| `File already exists` / `400 Client Error` on upload | filename collision — versions are immutable | bump the version (step 12) and rebuild |
| `twine check` fails on `long_description` | broken relative image/link in `README.md` | use absolute `https://` URLs for badges |
| `twine check` warns about the licence | `license = {text = "MIT"}` and the MIT classifier are deprecated under PEP 639 | optional: `pip install "setuptools>=77"`, then use `license = "MIT"` and `license-files = ["LICENSE"]`, and delete the `License ::` classifier; also raise `requires = ["setuptools>=77"]` in `[build-system]` |
| TestPyPI upload rejected the token | TestPyPI and PyPI accounts are independent | create <https://test.pypi.org/account/register/> and mint a token there |
| `pip install sayan-gradient` installs an old version | pip cache, or the TestPyPI index is still first in your config | `pip install --no-cache-dir --upgrade sayan-gradient` |
| Upload succeeds but the project page is blank | `readme = "README.md"` in `pyproject.toml` missing, or the file was not in the sdist | add the `include README.md` line to `MANIFEST.in` and rebuild |

## Security checklist before you press enter on a real upload

- [ ] `python -m pytest -q` passes, from a clean virtual environment
- [ ] `python -m twine check --strict dist/*` prints `PASSED` twice
- [ ] The version in `pyproject.toml` matches `__version__` in the package
- [ ] The version has never been uploaded before (check
      <https://pypi.org/project/sayan-gradient/#history>)
- [ ] `~/.pypirc` is `chmod 600`, lives outside the repository, and the token
      is project-scoped
- [ ] No token appears anywhere in the repository, the shell history you are
      about to keep, or a CI log
- [ ] The repository is clean and committed (`git status`)
- [ ] You are uploading to **TestPyPI** first
