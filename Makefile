.PHONY: makemessages compilemessages

makemessages:
	python manage.py makemessages -l en

compilemessages:
	python manage.py compilemessages