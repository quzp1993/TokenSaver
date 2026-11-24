# Project Guide

## Overview
This repository contains the codebase for our data-processing pipeline. It is very important to read this document carefully before making any changes, because the project has a number of conventions and rules that you should follow at all times throughout your work.

## Code Style
- Please always use 4 spaces for indentation, and never use tabs under any circumstances.
- Function names should use snake_case, and class names should use PascalCase.
- All public functions must include a docstring that explains what the function does, what parameters it takes, and what it returns.
- Keep line length under 88 characters wherever it is practical to do so.

## Testing
- Before committing any change, please run the full test suite with `pytest` and make absolutely sure that all tests pass.
- When you add a new feature, you must also add corresponding unit tests for that feature.
- Integration tests live in the `tests/integration/` directory and require a local database to run.
- Please run linting before pushing as well, using `ruff check .` and `mypy .` to catch type errors early.

## Git Workflow
- Please create a new branch for every feature or bugfix, and name it in a descriptive way that explains the change.
- Commit messages should be written in the imperative mood and should describe what the change does, not what you did.
- Before pushing, please run `git status` and carefully review your changes one more time.
- Squash fixup commits before merging so the history stays clean and easy to follow.

## Deployment
- The production environment is deployed automatically when you merge to the main branch.
- Staging is deployed from the develop branch.
- If a deploy fails, check the CI logs first before manually re-running the pipeline.
- Database migrations run automatically as part of the deploy, and must never be run by hand in production.

## Documentation
- Keep the README up to date whenever you change the public interface.
- Document any new environment variables in the `.env.example` file so others know about them.
- Add or update docstrings whenever you change a function's behavior or signature.

## Dependencies
- Add new dependencies with care; prefer the standard library wherever possible.
- Pin dependency versions in `requirements.txt` to keep builds reproducible.
- Run `pip-audit` occasionally to check for known vulnerabilities in your dependencies.

## Security
- Never commit secrets or API keys to the repository under any circumstances.
- Use environment variables for all credentials, and do not hardcode them anywhere in the code.
- Review third-party code carefully before adding it to the project, and prefer small, well-maintained libraries.

## Troubleshooting
- If the application fails to start, check the logs in the `logs/` directory first.
- Common issues are usually caused by missing environment variables or an incorrect database connection string.
- When you see a connection error, verify that the database container is running with `docker ps`.
