FROM python:3

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# / - root directory (like c:\ in Windows)
# WORKDIR /app -> mkdir /app && cd /app
WORKDIR /app

COPY requirements.txt /app/
# Result: /app/requirements.txt

RUN pip install -r requirements.txt

#COPY . /app/

COPY manage.py /app/manage.py
COPY media /app/media
COPY tests /app/tests
COPY templates /app/templates
COPY static /app/static
COPY static_files /app/static_files
COPY charity_app /app/charity_app