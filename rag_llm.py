
from langchain.embeddings import OpenAIEmbeddings, HuggingFaceInstructEmbeddings
from langchain.vectorstores import FAISS
from langchain_text_splitters import (Language,RecursiveCharacterTextSplitter,)
from langchain_openai import OpenAI, ChatOpenAI, OpenAIEmbeddings
import os
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain

def llm_response(api_key, context, prompt, code):
    
    #------------------------------------------------
    # # Prompt the user for their OpenAI API key
    # api_key = input("insert api key")
    # # Set the API key as an environment variable
    # os.environ["OPENAI_API_KEY"] = api_key
    # print("done!")

    #---------------------------------------------------
    text_splitter = RecursiveCharacterTextSplitter(
    # Set a really small chunk size, just to show.
    chunk_size=100,
    chunk_overlap=20,
    length_function=len,
    is_separator_regex=False,
    )

    texts = text_splitter.split_text(context)
    print(texts)
    #-------------------------------------------------

    # Create vector store
    embeddings = OpenAIEmbeddings()

    vectorstore = FAISS.from_texts(texts=texts, embedding=embeddings)

    #---------------------------------------------------
    # Create conversation chain
    # llm = ChatOpenAI(temperature=0.7, model_name="gpt-3.5-turbo",max_tokens=7000)
    llm = ChatOpenAI(api_key=api_key, model ="gpt-3.5-turbo-0125", max_tokens=4000)

    
    prompt = ChatPromptTemplate.from_template("""Answer the following question based only on the provided code:
    <context>{context}</context>
    Question: {input}
    Code: {code}""")
    document_chain = create_stuff_documents_chain(llm, prompt)

    retriever = vectorstore.as_retriever()
    retrieval_chain = create_retrieval_chain(retriever, document_chain)

    response = retrieval_chain.invoke({"input": f"""{prompt}""", "code": f"{code}"})
    print(response["answer"])
    return response["answer"]