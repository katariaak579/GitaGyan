FROM python
WORKDIR /app
COPY ingest.py /app/
COPY data/ /app/data/
COPY bot.py /app/
COPY requirements.txt /app/


RUN wget -P /app https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGML/resolve/main/llama-2-7b-chat.ggmlv3.q8_0.bin

EXPOSE 8000

RUN pip install -r requirements.txt 
RUN pip install ctransformers  
RUN python ingest.py


CMD ["chainlit", "run", "bot.py", "-w"]
