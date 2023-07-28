FROM python:3.10-slim
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /src
COPY requirements.txt ./
RUN pip3 install -r requirements.txt --no-cache-dir
COPY . .