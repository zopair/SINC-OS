FROM python:3.11-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements.txt ./requirements.txt
RUN python -m pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -r requirements.txt
COPY orbitx_final.py ./orbitx_final.py
RUN useradd --create-home --uid 10001 appuser
USER appuser
CMD ["python", "orbitx_final.py"]
