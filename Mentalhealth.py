import streamlit as st
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
import os
import html


# ---------------- Configuration ---------------- #

load_dotenv()

st.set_page_config(
    page_title="Mental Health Support AI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ---------------- Custom Styling ---------------- #

st.markdown("""
<style>
.stApp {
    background:
    radial-gradient(circle at top left, #ffccd5, transparent 30%),
    linear-gradient(135deg, #fff5f5, #ffffff);
}

.hero {
    background: linear-gradient(135deg, #e63946, #ff758f);
    padding: 35px;
    border-radius: 25px;
    color: white;
    text-align: center;
    box-shadow: 0px 10px 30px #ffb3c1;
}

.hero h1 {
    font-size: 40px;
    margin-bottom: 5px;
}

.hero p {
    font-size: 19px;
}

.card {
    background: white;
    padding: 20px;
    border-radius: 20px;
    box-shadow: 0px 5px 20px rgba(0,0,0,0.08);
}

.user {
    background: #ffe5ec;
    padding: 15px;
    border-radius: 20px;
    margin: 10px 0;
    overflow-wrap: anywhere;
}

.bot {
    background: #ffffff;
    padding: 20px;
    border-radius: 20px;
    margin: 10px 0;
    border-left: 5px solid #e63946;
    overflow-wrap: anywhere;
}

.stButton button {
    background: #e63946;
    color: white;
    border-radius: 15px;
    min-height: 45px;
    font-size: 15px;
    font-weight: bold;
}

.stButton button:hover {
    background: #c1121f;
    color: white;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #fff0f3, #ffffff);
}

.footer {
    text-align: center;
    color: #777;
    padding: 20px;
}
</style>
""", unsafe_allow_html=True)


# ---------------- Session Memory ---------------- #

if "messages" not in st.session_state:
    st.session_state.messages = []

if "selected" not in st.session_state:
    st.session_state.selected = None


# ---------------- Sidebar ---------------- #

with st.sidebar:

    st.markdown(
        """
        <h1 style='color:#e63946'>
        🧠 Mental Health Support AI
        </h1>
        """,
        unsafe_allow_html=True
    )

    st.markdown("---")

    menu = st.radio(
        "Navigation",
        [
            "💬 AI Chat",
            "🌿 Mental Wellness Tips",
            "📚 Mental Health Education",
            "⚙ Settings"
        ]
    )

    st.markdown("---")

    if st.button("🗑 Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.selected = None
        st.rerun()

    st.info(
        """
        **💚 A safe space to talk**

        This chatbot provides general mental health
        information and supportive coping strategies.

        It is not a therapist and cannot diagnose
        or treat mental health conditions.

        **Emergency:** If you may harm yourself or
        someone else, seek immediate help from local
        emergency services or a trusted person.
        """
    )


# ---------------- Hero Section ---------------- #

st.markdown(
    """
    <div class="hero">
        <h1>🧠 Mental Health Support AI Assistant</h1>
        <p>
        Your supportive companion for emotional wellness,
        self-care, and mental health awareness.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

st.write("")


# ---------------- Dashboard ---------------- #

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric("🌿 Focus", "Well-being")

with c2:
    st.metric("🤖 Model", "Llama 3.1")

with c3:
    st.metric("⚡ Responses", "AI-powered")

with c4:
    st.metric("💬 Support", "Anytime")


st.divider()


# ---------------- Navigation Content ---------------- #

if menu == "🌿 Mental Wellness Tips":

    st.subheader("🌱 Everyday Mental Wellness")

    st.markdown("""
    - **Practice mindfulness:** Take a few slow breaths
      and focus on the present moment.
    - **Maintain a routine:** Try to keep regular sleep
      and meal times.
    - **Stay connected:** Talk to someone you trust.
    - **Move your body:** Choose physical activity
      that feels comfortable for you.
    - **Set realistic goals:** Break overwhelming tasks
      into smaller, manageable steps.
    - **Take breaks:** Give yourself time to rest
      without feeling guilty.
    - **Seek support:** Consider speaking with a
      qualified mental health professional when needed.
    """)

elif menu == "📚 Mental Health Education":

    st.subheader("📚 Understanding Mental Health")

    st.markdown("""
    **What is mental health?**

    Mental health includes our emotional, psychological,
    and social well-being. It can affect how we think,
    feel, handle stress, and relate to others.

    **Common concerns include:**
    - Stress and anxiety
    - Low mood and depression
    - Sleep difficulties
    - Emotional exhaustion
    - Problems with confidence or relationships

    **When should you seek professional help?**

    Consider reaching out to a qualified professional
    if emotional difficulties persist, interfere with
    daily activities, or become difficult to manage.

    Mental health conditions are treatable, and asking
    for help is a positive step.
    """)
    
elif menu == "⚙️ Settings":

    st.subheader("⚙️ Chat Settings")

    st.write(
        f"Messages in this session: "
        f"{len(st.session_state.messages)}"
    )

    st.caption(
        "Chat history is maintained in the current "
        "Streamlit session."
    )


# ---------------- Suggested Questions ---------------- #

if menu == "💬 AI Chat":

    st.markdown("### 💡 Popular Questions")

    questions = [
        "How can I manage stress and anxiety?",
        "What are the signs of depression?",
        "How can I improve my mental well-being?",
        "What can I do when I feel overwhelmed?",
        "How can I improve my sleep?",
        "How can I support a struggling friend?"
    ]

    # Two columns keep question buttons readable.
    for start in range(0, len(questions), 2):

        cols = st.columns(2)

        for offset, col in enumerate(cols):

            index = start + offset

            if index < len(questions):

                q = questions[index]

                if col.button(q, key=f"question_{index}",
                              use_container_width=True):
                    st.session_state.selected = q
                    st.rerun()


    # ---------------- Chat Input ---------------- #

    question = st.chat_input(
        "Share what's on your mind..."
    )

    if st.session_state.selected:
        question = st.session_state.selected
        st.session_state.selected = None


    # ---------------- Display Chat History ---------------- #

    for msg in st.session_state.messages:

        safe_content = html.escape(msg["content"]).replace(
            "\n", "<br>"
        )

        if msg["role"] == "user":

            st.markdown(
                f"""
                <div class='user'>
                    👤 <b>You</b><br><br>
                    {safe_content}
                </div>
                """,
                unsafe_allow_html=True
            )

        else:

            st.markdown(
                f"""
                <div class='bot'>
                    🧠 <b>Mental Health AI</b><br><br>
                    {safe_content}
                </div>
                """,
                unsafe_allow_html=True
            )


    # ---------------- AI Response ---------------- #

    if question:

        st.session_state.messages.append(
            {
                "role": "user",
                "content": question
            }
        )

        prompt = ChatPromptTemplate.from_template("""
You are MindCare AI, a compassionate mental health
support and well-being education assistant.

YOUR PURPOSE:
Provide empathetic, non-judgmental, practical support
for emotional well-being and mental health awareness.

TOPICS YOU CAN HELP WITH:
- Everyday stress and anxiety management
- Emotional well-being and self-care
- Low mood and general information about depression
- Healthy sleep habits
- Mindfulness and relaxation techniques
- Confidence and self-esteem
- Relationships and communication
- Coping with difficult emotions
- Supporting friends and family
- Understanding when professional help may be useful

RESPONSE GUIDELINES:
1. Use warm, respectful, simple language.
2. Acknowledge the person's feelings without judging.
3. Offer a few practical, realistic coping strategies.
4. Ask a gentle follow-up question when appropriate.
5. Do not diagnose a mental health condition.
6. Do not prescribe medication or recommend changing
   prescribed medication.
7. Never promise confidentiality or claim to be a
   licensed therapist.
8. Do not dismiss, shame, or blame the user.
9. Avoid overwhelming the user with too much information.
10. If a question is unrelated to mental health or
    emotional well-being, politely explain your scope
    and invite a relevant question.

SAFETY AND CRISIS SUPPORT:
If the user indicates suicidal thoughts, self-harm,
immediate danger, or an intention to harm someone:
- Respond with empathy and take the concern seriously.
- Encourage contacting local emergency services or
  going to the nearest emergency department if danger
  is immediate.
- Encourage reaching out to a trusted person who can
  stay with them.
- For suicidal thoughts or self-harm urges, encourage
  contacting a qualified crisis counselor.
- Do not provide methods, instructions, or details
  that could facilitate self-harm.
- Do not rely on this chatbot as the person's only
  source of help.
- Ask a brief, direct safety question when appropriate.

RESPONSE FORMAT:
💚 Understanding
Briefly acknowledge the concern.

🌱 Helpful Steps
Provide practical coping strategies.

🧘 Self-Care
Suggest a suitable small activity when relevant.

🤝 Additional Support
Explain when talking to a trusted person or professional
may help.

Use only the sections that fit the question. For a simple
question, keep the answer concise and natural.

User Question:
{question}
""")


        try:

            api_key = os.getenv("GROQ_API_KEY")

            if not api_key:
                st.error(
                    "Groq API key not found. Add GROQ_API_KEY "
                    "to your .env file and restart the app."
                )
                st.stop()

            llm = ChatGroq(
                model="openai/gpt-oss-20b",
                temperature=0.4,
                api_key=api_key
            )

            chain = prompt | llm

            with st.spinner(
                "💚 Preparing a supportive response..."
            ):

                result = chain.invoke(
                    {"question": question}
                )

                answer = result.content

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": answer
                }
            )

            st.rerun()

        except Exception:
            st.error(
                "Unable to connect to the AI service. "
                "Please check your internet connection, "
                "Groq API key, and model availability, "
                "then try again."
            )


# ---------------- Footer ---------------- #

st.divider()

st.markdown(
    """
    <div class="footer">
        🧠 MindCare AI — Mental Health Support Assistant
        <br><br>
        Your feelings matter. Seeking support is a strength.
        <br>
        <small>
        Educational support only • Not a substitute for
        professional mental health care
        </small>
    </div>
    """,
    unsafe_allow_html=True
)