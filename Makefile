.PHONY: runserver test

runserver:
	uv run python manage.py runserver

test:
	uv run pytest
