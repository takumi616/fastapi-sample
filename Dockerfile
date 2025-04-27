# ---------- Builder Stage ----------
FROM python:3.12-slim AS builder

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

WORKDIR /app

# Copy only dependency files first (for better caching)
COPY pyproject.toml uv.lock ./

# Install dependencies inside .venv
RUN uv venv && \
    uv sync --frozen --no-editable

# Copy application code
COPY ./app ./app


# ---------- Final Stage ----------
FROM python:3.12-slim AS final

# Create a user
RUN useradd -m appuser

WORKDIR /app

# Copy installed virtualenv and application code
COPY --from=builder /app/.venv /app/.venv
COPY --from=builder /app/app ./app

# Set environment path
ENV PATH="/app/.venv/bin:$PATH"

# Use non-root user
USER appuser

# Command to run app using uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
