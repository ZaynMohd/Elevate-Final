import streamlit as st
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
import os
import time


# ---------------- Configuration ---------------- #

load_dotenv()

st.set_page_config(
    page_title="Heart AI Doctor",
    page_icon="❤️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ---------------- Custom Styling ---------------- #

st.markdown("""
<style>

/* Background */

.stApp{
    background:
    radial-gradient(circle at top left,#ffccd5,transparent 30%),
    linear-gradient(135deg,#fff5f5,#ffffff);
}


/* Header */

.hero{
    background:
    linear-gradient(135deg,#e63946,#ff758f);
    padding:35px;
    border-radius:25px;
    color:white;
    text-align:center;
    box-shadow:0px 10px 30px #ffb3c1;
}


.hero h1{
    font-size:45px;
    margin-bottom:5px;
}


.hero p{
    font-size:20px;
}


/* Cards */

.card{

background:white;
padding:20px;
border-radius:20px;
box-shadow:
0px 5px 20px rgba(0,0,0,0.08);

}


/* Chat bubbles */


.user{

background:#ffe5ec;
padding:15px;
border-radius:20px;
margin:10px;

}


.bot{

background:#ffffff;
padding:20px;
border-radius:20px;
margin:10px;
border-left:5px solid #e63946;

}



/* Buttons */

.stButton button{

background:#e63946;
color:white;

border-radius:15px;
height:45px;

font-size:16px;
font-weight:bold;

}


.stButton button:hover{

background:#c1121f;
color:white;

}


/* Sidebar */

[data-testid="stSidebar"]{

background:
linear-gradient(
180deg,
#fff0f3,
#ffffff
);

}


.footer{

text-align:center;
color:#777;
padding:20px;

}

</style>

""",unsafe_allow_html=True)



# ---------------- Session Memory ---------------- #

if "messages" not in st.session_state:

    st.session_state.messages=[]



# ---------------- Sidebar ---------------- #

with st.sidebar:


    st.markdown(
    """
    <h1 style='color:#e63946'>
    ❤️ Heart AI
    </h1>
    """,
    unsafe_allow_html=True
    )


    st.markdown("---")


    menu=st.radio(
        "Navigation",
        [
            "💬 AI Chat",
            "❤️ Heart Tips",
            "📚 Education",
            "⚙ Settings"
        ]
    )


    st.markdown("---")


    if st.button("🗑 Clear Chat"):

        st.session_state.messages=[]

        st.rerun()


    st.info(
    """
    ⚠ Medical Disclaimer

    This AI provides educational information.
    It does not replace a doctor consultation.
    """
    )



# ---------------- Hero Section ---------------- #

st.markdown(
"""
<div class="hero">

<h1>❤️ Heart Health AI Assistant</h1>

<p>
Your intelligent companion for cardiovascular health education
</p>

</div>

""",
unsafe_allow_html=True
)



st.write("")



# ---------------- Dashboard ---------------- #

c1,c2,c3,c4=st.columns(4)


with c1:

    st.metric(
        "❤️ Topics",
        "10+"
    )


with c2:

    st.metric(
        "🤖 Model",
        "Llama 3.1"
    )


with c3:

    st.metric(
        "⚡ Response",
        "Fast"
    )


with c4:

    st.metric(
        "🕒 Support",
        "24/7"
    )



st.divider()



# ---------------- Suggested Questions ---------------- #

st.markdown("### 💡 Popular Questions")


questions=[

"What are early symptoms of heart attack?",

"How can I reduce cholesterol naturally?",

"What is normal blood pressure?",

"Best exercises for heart health?",

"Can stress damage the heart?"

]


cols=st.columns(len(questions))


for i,q in enumerate(questions):

    if cols[i].button(q[:18]+"..."):

        st.session_state.selected=q



# ---------------- Input ---------------- #

question=st.chat_input(
    "Ask your heart health question..."
)



if "selected" in st.session_state:

    question=st.session_state.selected

    del st.session_state.selected



# ---------------- Display Chat ---------------- #

for msg in st.session_state.messages:


    if msg["role"]=="user":

        st.markdown(
        f"""
        <div class='user'>
        👤 <b>You</b><br>
        {msg['content']}
        </div>
        """,
        unsafe_allow_html=True
        )


    else:

        st.markdown(
        f"""
        <div class='bot'>
        🤖 <b>Heart AI</b><br><br>
        {msg['content']}
        </div>
        """,
        unsafe_allow_html=True
        )



# ---------------- AI Response ---------------- #

if question:


    st.session_state.messages.append(
        {
            "role":"user",
            "content":question
        }
    )


    prompt=ChatPromptTemplate.from_template(

"""
You are Heart AI, a cardiovascular health assistant.

Only answer heart-related questions.

Allowed topics:

- Heart diseases
- Blood pressure
- Cholesterol
- Heart attack
- Cardiac arrest
- Diabetes impact
- Exercise
- Diet
- Stress
- Prevention


If unrelated:

Reply:
"Sorry, I only answer heart health related questions."


User Question:

{question}


Provide answer:

❤️ Explanation

📌 Steps to Follow

✅ Healthy Habits

⚠ Precautions

🚨 Emergency Signs

👨‍⚕ Doctor Consultation Advice


Use simple language.

"""
)


    try:


        llm=ChatGroq(

            model="llama-3.1-8b-instant",

            temperature=0.2

        )


        chain=prompt | llm


        with st.spinner(
            "🩺 Heart AI thinking..."
        ):


            result=chain.invoke(
                {
                    "question":question
                }
            )


            answer=result.content



        st.session_state.messages.append(

            {
                "role":"assistant",
                "content":answer
            }

        )


        st.rerun()



    except Exception as e:


        st.error(
            "Unable to connect with AI service."
        )



# ---------------- Footer ---------------- #

st.divider()


st.markdown(

"""
<div class="footer">

❤️ Heart Health AI Assistant

<br>

Healthy Heart • Healthy Life

</div>

""",

unsafe_allow_html=True

)