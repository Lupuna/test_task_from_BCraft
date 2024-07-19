FROM python:3.11-alpine3.16

COPY requirements.txt /temp/requirements.txt
COPY core /core
WORKDIR /core
EXPOSE 8000

RUN pip install -r /temp/requirements.txt

RUN adduser --disabled-password service-user

USER service-user

#CMD ["gunicorn", "core.wsgi:application", "--bind", "0.0.0.0:8000"]
