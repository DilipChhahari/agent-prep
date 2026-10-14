FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY main.py schema.sql seed.sql ./
RUN python -c "import sqlite3; c = sqlite3.connect('shop.db'); c.executescript(open('schema.sql').read()); c.executescript(open('seed.sql').read()); c.commit()"
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
