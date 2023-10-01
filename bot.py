from langchain.document_loaders import PyPDFLoader, DirectoryLoader
from langchain.prompts import PromptTemplate
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.llms import CTransformers
from langchain.chains import RetrievalQA
import chainlit as cl
import os
from langchain.memory import ConversationBufferMemory
from torch import cuda

device = f'cuda:{cuda.current_device()}' if cuda.is_available() else 'cpu'

DB_FAISS_PATH = 'vectorstore/db_faiss'
memory = ConversationBufferMemory()


custom_prompt_template = """The user is facing problem in his life and wants some help from the holy book of hindus the bhagvat geeta.
Use the information provided to give the solution for the user and solve his problem.

Context: {context}
Question: {question}

Given the question return an answer that solves his problem and satisfies him.
"""

def set_custom_prompt():
    """
    Prompt template for QA retrieval for each vectorstore
    """
    prompt = PromptTemplate(template=custom_prompt_template,
                            input_variables=['context', 'question'])
    return prompt

#Retrieval QA Chain
def retrieval_qa_chain(llm, prompt, db, memory):
    qa_chain = RetrievalQA.from_chain_type(llm=llm,
                                       chain_type='stuff',
                                       retriever=db.as_retriever(search_kwargs={'k': 2}),
                                       return_source_documents=False,
                                       chain_type_kwargs={'prompt': prompt},
                                       memory=memory
                                       )
    return qa_chain

#Loading the model
def load_llm():
    # Load the locally downloaded model here
    llm = CTransformers(
        model = "llama-2-7b-chat.ggmlv3.q8_0.bin",
        model_type="llama",
        max_new_tokens = 1024,
        temperature = 0.8
    )
    return llm

#QA Model Function
def qa_bot(memory):
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2",
                                       model_kwargs={'device': device})
    db = FAISS.load_local(DB_FAISS_PATH, embeddings)
    llm = load_llm()
    qa_prompt = set_custom_prompt()
    qa = retrieval_qa_chain(llm, qa_prompt, db, memory=memory)

    return qa

#output function
def final_result(query, memory):
    qa_result = qa_bot(memory)
    response = qa_result({'query': query})
    return response

#chainlit code
@cl.on_chat_start
async def start():
    chain = qa_bot(ConversationBufferMemory())
    msg = cl.Message(content="Starting the bot...")
    await msg.send()
    msg.content = "Hi, Welcome to Gita Bot. What is your problem?"
    await msg.update()

    cl.user_session.set("chain", chain)

@cl.on_message
async def main(message):
    chain = cl.user_session.get("chain")
    cb = cl.AsyncLangchainCallbackHandler(
        stream_final_answer=True, answer_prefix_tokens=["FINAL", "ANSWER"]
    )
    cb.answer_reached = True
    res = await chain.acall(message, callbacks=[cb])
    answer = res["result"]

    await cl.Message(content=answer).send()

