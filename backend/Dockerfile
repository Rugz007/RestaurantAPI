# ---- Base python ----
FROM python:3.9-alpine AS base

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# Create app directory
WORKDIR /src

# ---- Dependencies ----
FROM base AS dependencies

# Create Python virtualenv and use it
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt ./
RUN pip install -r requirements.txt --no-cache-dir

# ---- Copy Files/Build ----
FROM base

WORKDIR /src

COPY . /src

COPY --from=dependencies /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY ./tools/wait-for-it.sh /wait-for-it.sh
RUN apk add --no-cache \
    bash \
    && chmod +x /wait-for-it.sh


CMD /wait-for-it.sh rabbitmq:5672 --strict --timeout=0 \
    && python manage.py makemigrations \
    && python manage.py migrate \
    && python manage.py shell < tools/create_superuser.py \
    && python manage.py runserver 0.0.0.0:8000