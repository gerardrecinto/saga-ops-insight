FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml .
RUN pip install --no-cache-dir -e .

COPY signal_harbor/ signal_harbor/

EXPOSE 80

CMD ["uvicorn", "signal_harbor.main:app", "--host", "0.0.0.0", "--port", "80"]
