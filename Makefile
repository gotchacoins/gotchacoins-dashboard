.PHONY: makemessages compilemessages

makemessages:
	uv run python manage.py makemessages -l en

compilemessages:
	uv run python manage.py compilemessages
