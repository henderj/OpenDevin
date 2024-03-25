from python:3.12-bookworm

ENV GOOGLE_API_KEY="AIzaSyCAY6BQJAqaxaCs5HOTwdYhtA0wvhoA3BI"
ENV OPEN_API_KEY="nothing"

RUN git config --global user.email "devin@opendevin.com"
RUN git config --global user.name "Devin Abierto"

RUN apt-get update
RUN apt-get install -y git sudo curl

WORKDIR /app

COPY requirements.txt ./requirements.txt
RUN python -m pip install -r requirements.txt

WORKDIR /workspace

CMD ["python", "/app/opendevin/main.py", "/workspace"]

