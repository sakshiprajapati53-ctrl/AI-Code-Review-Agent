import streamlit as st
from utils import ask_gemini

# Page Config

st.set_page_config(
    page_title="AI Code Review Agent",
    layout="wide"
)

# Session State

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Main UI

st.title("AI Code Review Agent + AI Mentor")

code = st.text_area(
    "Paste your code here",
    height=300,
    key="main_code"
)

difficulty = st.selectbox(
    "Bug Injection Difficulty",
    ["Easy", "Medium", "Hard"],
    key="difficulty"
)

# Sidebar AI Mentor

st.sidebar.title("AI Mentor")

user_question = st.sidebar.text_input(
    "Ask about any bug, concept, error or output",
    key="mentor_question"
)

if st.sidebar.button("Ask AI"):

    conversation = ""

    for role, msg in st.session_state.chat_history:
        conversation += f"{role}: {msg}\n"

    prompt = f"""
    You are an expert programming mentor.

    Current Code:
    {code}

    Previous Conversation:
    {conversation}

    User Question:
    {user_question}

    Explain:
    - Key Idea
    - Why It Happens
    - Fix
    - Real World Analogy
    - Example

    Keep the explanation beginner friendly.
    """

    answer = ask_gemini(prompt)

    st.session_state.chat_history.append(
        ("User", user_question)
    )

    st.session_state.chat_history.append(
        ("AI", answer)
    )

st.sidebar.markdown("---")

st.sidebar.subheader("Conversation")

for role, msg in st.session_state.chat_history:
    st.sidebar.write(f"**{role}:**")
    st.sidebar.write(msg)
    st.sidebar.markdown("---")


# Quick Learn

st.sidebar.subheader("Quick Learn")

topic = st.sidebar.selectbox(
    "Choose Topic",
    [
        "Time Complexity",
        "Space Complexity",
        "Pointers",
        "Recursion",
        "Binary Search",
        "Dynamic Programming",
        "Segmentation Fault",
        "Memory Leak",
        "Arrays",
        "Linked List"
    ],
    key="topic_select"
)

if st.sidebar.button("Learn Topic"):

    prompt = f"""
    Teach {topic} to a beginner.

    Include:
    1. Definition
    2. Importance
    3. Example
    4. Real-world analogy
    5. Common mistakes
    6. Interview tips

    Use simple language.
    """

    answer = ask_gemini(prompt)

    st.sidebar.subheader(topic)
    st.sidebar.write(answer)


# Main Buttons

col1, col2 = st.columns(2)

with col1:

    if st.button("Review Code"):

        prompt = f"""
        Review the following code.

        Find:
        1. Bugs
        2. Logic Errors
        3. Edge Cases
        4. Complexity Issues
        5. Best Practices

        Code:
        {code}
        """

        result = ask_gemini(prompt)

        st.subheader("Review Result")
        st.write(result)

with col2:

    if st.button("Inject Bugs"):

        prompt = f"""
        Inject realistic bugs into this code.

        Difficulty: {difficulty}

        Rules:
        - Keep code compilable if possible
        - Add logical bugs
        - Add realistic mistakes
        - Return only modified code

        Code:
        {code}
        """

        result = ask_gemini(prompt)

        st.subheader("Bug Injected Code")
        st.code(result)


# Explain Bug

if st.button("Explain Bug"):

    prompt = f"""
    Analyze the code.

    For every bug explain:

    1. Bug Name
    2. Why it happened
    3. Impact
    4. Fix
    5. Real-world analogy
    6. Beginner-friendly explanation

    Code:
    {code}
    """

    result = ask_gemini(prompt)

    st.subheader("Bug Explanation")
    st.write(result)


# Learning Diagram

if st.button("Generate Learning Diagram"):

    prompt = f"""
    Explain the bug using ASCII diagrams.

    Include:
    - Program Flow
    - Bug Location
    - Wrong Flow
    - Correct Flow

    Code:
    {code}
    """

    result = ask_gemini(prompt)

    st.subheader("Visual Learning Diagram")
    st.code(result)