import streamlit as st
from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate


load_dotenv()

st.set_page_config(
    page_title="Heart Health Chatbot",
    page_icon="❤️"
)
st.title("💕Heart Health AI Chatbot!!❤️")
st.write("This is an AI Heart Health bot this bot will be usefull for all")


st.write("Ask anything related to Heart Health....")

question = st.text_area(
    "Enter your Heart related queries"
)

if st.button("Ask your Personal AI"):
    llm = ChatGroq(
        model="llama-3.1-8b-instant",
        temperature=0.3
    )

    prompt = ChatPromptTemplate.from_template(
        """
Your are an Heart Health Expert.

Your job is to answer ONLY Heart Health related question

Topics include:
-Heart health basics
-Heart attack & cardiac arrest
-Blood pressure 
-cholestrol
-diabetes
-stress & mental well-being
-Genetics & family history

If the user asks anything outside heart health,
reply:
"Sorry, I only answer heart health related questions."

Question
{question}

Provide:
1. Simple Explanation
2. Step by step guidance
3. Best practices
4. Precautions if needed
"""

    )
    chain = prompt | llm
    response = chain.invoke(
        {
            "question":question
        }
    )

    st.success(response.content)