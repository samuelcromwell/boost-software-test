set export

VENV_DIRNAME := ".venv"


@_default:
    just --list

# Materialise the environment and install dependencies
@bootstrap:
    [ -d $VENV_DIRNAME ] || uv venv $VENV_DIRNAME
    uv sync

# Runs the local development server
@run:
    uv run flask --app run run --debug

# Runs all tests
@test *options:
    uv run pytest {{options}}

# Runs all linting
@lint *options:
    uv run ruff check {{options}}

# Builds the candidate zip from committed files only
@package:
    git archive --format=zip --output ../boost-support-engineer-test.zip HEAD
    @echo "Created ../boost-support-engineer-test.zip from committed files only"
