FROM python:3.12-slim

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y

ENV PATH="/root/.cargo/bin:${PATH}"

RUN mkdir /app
WORKDIR /app

ADD . /app/

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

EXPOSE 8000

CMD [ "inv", "prod" ]
