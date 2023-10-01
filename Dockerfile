FROM python:3.9-slim

COPY ingest.py /app/
# COPY data/ /app/data/
COPY bot.py /app/
COPY requirements.txt /app/
COPY llama-2-7b-chat.ggmlv3.q8_0.bin /app/
WORKDIR /app

RUN pip install -r requirements.txt 
# RUN python ingest.py

CMD ["chainlit", "run", "bot.py", "-w"]