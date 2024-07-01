# Create dockerfile for poetry python 3.10 fastapi
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Copy project
COPY . /app/

# Install dependencies
COPY ./poetry.lock ./pyproject.toml /app/
RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev

# Expose port
EXPOSE 8000:8000

# Run entrypoint.sh
CMD ["uvicorn", "src.api.http.run:app", "port=8000", "--host", "localhost"]