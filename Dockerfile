FROM python:3.10

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir fastapi uvicorn pydantic openai

# 🔥 Fix import issues
ENV PYTHONPATH=/app

EXPOSE 7860

# ✅ Only run API server (NOT inference)
CMD ["uvicorn", "server.app:app", "--host", "0.0.0.0", "--port", "7860"]
