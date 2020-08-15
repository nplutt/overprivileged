#!/usr/bin/env bash
pipenv run black overprivileged/ tests/ --check
pipenv run isort . -c