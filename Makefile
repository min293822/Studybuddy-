# Makefile for Django project

.PHONY:	migrations
migrations:
	python	manage.py	makemigrations

.PHONY:	migrate
migrate:
	python	manage.py	migrate

.PHONY:	update
update:	migrations	migrate

.PHONY: mysqld
mysqld:
	mysqld_safe	&

.PHONY: mysql
mysql:
	mysql	-u	min293822	-p

.PHONY:	gitadd
gitadd:
	git add	.

.PHONY:	gitcommit
gitcommit:
	git	commit	-m	'commit_all'

.PHONY:	gitpush
gitpush:
	git	push	origin	main

.PHONY:	git
git:
	gitadd	gitcommit	gitpush

.PHONY: collectstatic
collectstatic:
	python	manage.py	collectstatic

.PHONY:	runserver
runserver:
	python	manage.py	runserver

.PHONY:	superuser
superuser:
	python	manage.py	createsuperuser

.PHONY:	django_app
django_app:
	python	manage.py	startapp	'my_app'

.PHONY:	django_rest
django_rest:
	python	manage.py	startapp	'api'
