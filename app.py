import streamlit as st
from utils import ask_gemini

# Page Config

st.set_page_config(
    page_title="AI Code Review Agent",layout="wide")

st.markdown("""
<style>
.stButton > button {
    height: 55px;
    border-radius: 12px;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

DEBUG_MODE = st.sidebar.toggle("Debug Mode",value = True)

# Session state

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "explanation" not in st.session_state:
    st.session_state.explanation = ""

# Debug toggle

if DEBUG_MODE:
    st.sidebar.info("Mock Mode ON (NO API CALLS)")

# Title

st.title("AI Code Review Agent UI and features")
st.markdown("Your AI-powered coding assistant for debugging & learning.")
st.divider()


uploaded_file = st.file_uploader(
    "Upload Source Code",
    type=["py", "cpp", "java", "c"]
)

if uploaded_file is not None:

    code = uploaded_file.read().decode("utf-8")

    st.success("File Uploaded Successfully")

    st.text_area(
        "Code",
        value=code,
        height=250
    )

else:

    code = st.text_area(
        "Paste your code here",
        height=250,
        key="main_code"
    )

difficulty = st.selectbox( "Bug Injection Difficulty",["Easy", "Medium", "Hard"],key="difficulty")

if "output" not in st.session_state:
    st.session_state.output = ""

st.divider()

# Sider ai mentor

st.sidebar.write("DEBUG_MODE =", DEBUG_MODE)
st.sidebar.title("AI Mentor")
user_question = st.sidebar.text_input("Ask anything about code")

if st.sidebar.button("Ask AI"):

    conversation = "\n".join([f"{r}: {m}" for r, m in st.session_state.chat_history])

    prompt = f"""
    You are an expert programming mentor.

    Code:
    {code}

    Conversation:
    {conversation}

    User Question:
    {user_question}

    Explain in simple terms with examples.
    """

    answer = ask_gemini(prompt, DEBUG_MODE)

    st.session_state.chat_history.append(("User", user_question))
    st.session_state.chat_history.append(("AI", answer))

# Chat history

st.sidebar.subheader("Conversation")

for role, msg in st.session_state.chat_history:
    st.sidebar.write(f"**{role}:**")
    st.sidebar.write(msg)
    st.sidebar.markdown("---")

# Quick learning 

st.sidebar.subheader("Quick Learn")
topic = st.sidebar.selectbox(
    "Choose Topic",["Time Complexity", "Pointers", "Recursion", "Binary Search","Dynamic Programming", "Segmentation Fault", "Memory Leak"]
)

if st.sidebar.button("Learn Topic"):

    prompt = f"Teach {topic} with examples and analogies."
    answer = ask_gemini(prompt, DEBUG_MODE)
    st.sidebar.write(answer)

# Main action button

st.divider()
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("Review Code",use_container_width = True):

        prompt = f"""
        Review code:

        Find bugs, errors, edge cases, complexity issues.
        Code:

        {code}
        """
        result = ask_gemini(prompt, DEBUG_MODE)

        st.session_state.output = f"""
        #Review Result

        {result}
        """

# inject bugs

with col2:
    if st.button("Inject Bugs",use_container_width = True):

        prompt = f"""
        Inject realistic bugs.

        Difficulty: {difficulty}

        Code:
        {code}
        """

        result = ask_gemini(prompt, DEBUG_MODE)

        st.session_state.output = f"""

        # Bug Injected Code

        {result}
        """

# Explain bug

with col3:
    if st.button("Explain Bug",use_container_width = True):

        prompt = f"""
        Explain bugs in code:
        - Why it happened
        - Impact
        - Fix
        - Real world analogy    
        Code:
        {code}
        """

        result = ask_gemini(prompt, DEBUG_MODE)

        st.session_state["explanation"] = result

        st.session_state.output = f"""
        # Bug Explanation

        {result}
        """

# interview questions

col4, col5, col6 = st.columns(3)

with col4:
    if st.button("Interview Questions",use_container_width = True):

        prompt = f"""
        Generate interview questions from this code.
        - Easy Questions
        - Medium Questions
        - Hard Questions
        - Optimization Questions

        Code:
        {code}
        """

        result = ask_gemini(prompt, DEBUG_MODE)

        st.session_state.output = f"""
        # Interview Questions

        {result}
        """

# Diagram

with col5:
    if st.button("Generate Learning Diagram",use_container_width = True):

        prompt = f"""
        Explain code flow with diagram:

        Code:
        {code}
        """

        result = ask_gemini(prompt, DEBUG_MODE)
        st.session_state.output = f"""
        # Learning Diagram

        {result}
        """

# bug difficulty

with col6:
    if st.button("Bug Difficulty",use_container_width = True):

        prompt = f"""
        Analyze this code.
        1. Difficulty Score (1-10)
        2. Complexity Level
        3. Learning Level
        4. Common Mistakes

        Code:
        {code}
        """

        result = ask_gemini(prompt, DEBUG_MODE)

        st.session_state.output = f"""
        # Bug Difficulty Score

        {result}
        """

with col6:
    if st.button("Code Quality Score",use_container_width = True):

        prompt = f"""
        Analyze this code and give:

        1. Overall Score out of 100
        2. Readability Score (/10)
        3. Performance Score (/10)
        4. Bug Risk Score (/10)
        5. Best Practices Score (/10)

        Also explain why each score was given.

        Code:
        {code}
            """

        result = ask_gemini(prompt, DEBUG_MODE)

        st.session_state.output = f"""
        # Code Quality Report

        {result}
        """

st.divider()

with st.container(border=True):

    st.subheader("Output Panel")

    if st.session_state.output:
        st.markdown(st.session_state.output)

    else:
        st.info("Select any feature to analyze the code.")