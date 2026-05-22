# Use official Python 3.12 slim image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install uv
RUN pip install uv

# Copy dependency files first (for better caching)
COPY pyproject.toml uv.lock ./

# Install dependencies (no dev dependencies in production)
RUN uv sync --frozen --no-dev

# Copy the rest of the project
COPY . .

# Expose the port Litestar runs on
EXPOSE 8000

# Run the app
CMD ["uv", "run", "litestar", "--app", "main:app", "run", "--host", "0.0.0.0", "--port", "8000"]