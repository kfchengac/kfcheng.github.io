FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN python -m pip install --upgrade pip && pip install -r requirements.txt
COPY . /app
ENV PYTHONUNBUFFERED=1
CMD ["rq", "worker", "default"]
