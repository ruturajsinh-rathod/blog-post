# Builder stage
FROM python:3.12-alpine AS builder

# Prevent Python from writing .pyc files to disk
ENV PYTHONDONTWRITEBYTECODE=1

# Make Python output unbuffered
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apk add --no-cache build-base libffi-dev postgresql-dev curl

# Set workdir
WORKDIR /code

# Copy only dependency-related files first (for better caching)
COPY pyproject.toml poetry.lock ./

# Install Poetry and dependencies
RUN pip install --no-cache-dir pip==23.3.1 poetry==1.6.1 && \
    poetry config virtualenvs.create false && \
    poetry install --no-root --no-interaction --no-ansi

# Copy the rest of the code
COPY . .

# Runner stage
FROM python:3.12-alpine AS runner

# Prevents Python from writing .pyc files to disk.
ENV PYTHONDONTWRITEBYTECODE=1

# # Make Python output unbuffered
ENV PYTHONUNBUFFERED=1

ENV PYTHONPATH="/code/src"

# Install runtime packages
RUN apk add --no-cache libffi postgresql-libs curl

# Create user, run the app as the app user, not root.
RUN addgroup -S app && adduser -S app -G app

# Set user and working dir
USER app
WORKDIR /code/src

# Copy installed deps and source code
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /code /code

# Healthcheck
HEALTHCHECK --interval=10s --timeout=3s --start-period=10s --retries=3 \
  CMD curl -f http://localhost:${DOCKER_PORT}/healthcheck || exit 1

# Entrypoint
ENTRYPOINT ["/bin/sh", "-c", "python main.py migrate && python main.py run"]
