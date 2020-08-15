#!/usr/bin/env bash
pipenv run black src/ tests/
pipenv run isort .