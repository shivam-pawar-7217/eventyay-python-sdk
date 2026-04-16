Release Checklist
=================

Use this checklist before publishing a release.

Code Quality
------------

* Run tests: ``pytest -q``
* Run type checks: ``mypy --config-file pyproject.toml eventyay``
* Run lint checks:

  * ``flake8 eventyay tests --count --exclude=.venv,venv --select=E9,F63,F7,F82 --show-source --statistics``
  * ``flake8 eventyay tests --count --exclude=.venv,venv --max-complexity=10 --max-line-length=127 --statistics``

Documentation
-------------

* Ensure README examples match current method signatures.
* Ensure docs include any new features or behavior changes.

Contracts and Compatibility
---------------------------

* Run optional live contract checks when release risk is high:

  * ``EVENTYAY_LIVE_TEST=1 pytest tests/test_contract_live_optional.py -q``

* Confirm changelog entries for user-visible changes.

Packaging
---------

* Bump version in package metadata.
* Build source and wheel artifacts.
* Verify install and import smoke tests on a clean virtual environment.
