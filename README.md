# GitaGPT

GitaGyan is an AI chatbot to provide solution to various problems you have. 
 and guidance based on the teachings of The Bhagavad Gita. It utilizes Meta’s Llama 2( llama-2-7b-chat.ggmlv3.q8_0.bin ) model to generate meaningful responses to user queries. It uses ConversationBufferMemory and VectorStoreRetrieveMemory to provide best possible answer according to the past conversations with the user.

# How to run
I have created a bash file chat.sh which will run the application by running the container using the docker image. Make the bash file availbale in your system. 
Go to the directory where the file is present

to make the bash file executable run:
```bash
chmod +x run.sh
```

simply run the bash file:
```bash
./run.sh
```

Now you can access the chat bot on 
```bash
[localhost:8000](http://localhost:8000/)
```

# Work done
- Developed a chat bot application using llama 2 model available on hugging face.
- Provided memory to llm for conversationBufferMemory and vectorStoreRetrievalMemory
- Used chainlit for UI. 
- Dockerized the application. 
- I also added github workflow actions which will automatically build and push the image to dockerhub, which will be initiated whenever something is pushed.
- I also created a bash script which will run the container and will also provide instructions how to access the chat bot.
- Created kubernetes manifest file development.yaml which will be used tom host the web server
