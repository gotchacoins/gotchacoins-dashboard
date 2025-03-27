FROM --platform=linux/amd64 python:3.12.9
LABEL maintainer="madeffort"

ENV PYTHONUNBUFFERED 1
COPY /pyproject.toml /tmp/pyproject.toml
COPY /uv.lock /tmp/uv.lock

COPY /server /server
WORKDIR /server
EXPOSE 9000

RUN pip install --upgrade pip && pip install uv

RUN uv venv venv
RUN uv sync

RUN adduser --disabled-password --no-create-home django-user

ENV PATH="/scripts:/venv/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/snap/bin:/:"${PATH}

RUN chown django-user:django-user -R /server/

USER root
COPY ./infra/gunicorn/entrypoint.sh /gunicorn/entrypoint.sh
RUN chmod +x /gunicorn/entrypoint.sh
RUN mkdir -p /server/staticfiles && \
    chown -R django-user:django-user /server/staticfiles && \
    chmod -R 755 /server/staticfiles

RUN /venv/bin/python manage.py collectstatic --no-input

RUN mkdir -p /var/log/gunicorn && \
    chown -R django-user:django-user /var/log/gunicorn && \
    chmod -R 755 /var/log/gunicorn

USER django-user
VOLUME /server/staticfiles

CMD ["/gunicorn/entrypoint.sh"]
