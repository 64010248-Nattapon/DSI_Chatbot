from sentence_transformers import SentenceTransformer
import pinecone
import openai
import streamlit as st

openai.api_key = "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"
model = SentenceTransformer("all-MiniLM-L6-v2")

pinecone.init(
    api_key="6efed09f-2e8e-47f6-ac70-6aba2f0b858b", environment="us-west4-gcp-free"
)
index = pinecone.Index("testwebdsi")


def find_match(input):
    input_em = model.encode(input).tolist()
    result = index.query(input_em, top_k=2, includeMetadata=True)
    return (
        result["matches"][0]["metadata"]["text"]
        + "\n"
        + result["matches"][1]["metadata"]["text"]
    )


def query_refiner(conversation, query):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=f"CONVERSATION LOG: \n{conversation}\n\nคำถาม: {query}",
        max_tokens=480,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )
    return response["choices"][0]["text"]


def get_conversation_string():
    conversation_string = ""
    for i in range(len(st.session_state["responses"]) - 1):
        conversation_string += "Human: " + st.session_state["requests"][i] + "\n"
        conversation_string += "Bot: " + st.session_state["responses"][i + 1] + "\n"
    return conversation_string
