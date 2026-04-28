FROM python:3.13.9-alpine3.22

SHELL ["/bin/sh", "-o", "pipefail", "-c"]

ARG USERNAME=carapi
ENV POETRY_VERSION=2.3.4 \ 
    PATH="/home/${USERNAME}/.local/bin:$PATH"

RUN apk add curl=8.14.1-r2 \
    --no-cache && \
    rm -rf /var/cache/apk/* && \
    adduser -s /bin/sh -D ${USERNAME}

USER ${USERNAME}

RUN curl -sSL https://install.python-poetry.org | python3 -

WORKDIR /home/${USERNAME}

COPY --chown=${USERNAME}:${USERNAME} pyproject.toml poetry.lock ./
RUN poetry install \
    --without dev \
    --no-root \
    --no-ansi

COPY --chown=${USERNAME}:${USERNAME} . .

CMD ["poetry", "run", "fastapi", "dev", "car_api/app.py", "--host", "0.0.0.0"]
