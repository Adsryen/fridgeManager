FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8080

ENV HOST=0.0.0.0
ENV PORT=8080
ENV DATABASE_DIR=/data
ENV FLASK_ENV=production

CMD ["python", "run.py"]
