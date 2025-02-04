FROM python:3.11-slim

WORKDIR /code

# 필수 패키지 설치 (MySQL 대신 MariaDB 개발 패키지 사용)
RUN apt-get update && apt-get install -y \
    build-essential \
    libmariadb-dev \
    libmariadb-dev-compat \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r /code/requirements.txt

COPY . /code

# .env 파일이 없으면 자동 생성
RUN sh -c 'if [ ! -f "/code/.env" ]; then echo "DATABASE_URL=mysql://root:0000@db:3306/palink?charset=utf8mb4" > /code/.env; fi'


CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
