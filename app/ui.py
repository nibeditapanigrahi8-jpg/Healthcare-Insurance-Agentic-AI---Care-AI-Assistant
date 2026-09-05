import streamlit as st
from langchain_core.messages import HumanMessage
from langchain_core.runnables import RunnableConfig
from agent import graph
from langgraph.types import Command


st.set_page_config(
    page_title="Care AI Assistant",
    page_icon="🏥"
)

st.title("🏥 Care AI Assistant")
st.caption("Healthcare Insurance Agentic AI Assistant")

if st.button("🔄 New Conversation"):

    st.session_state.clear()

    st.rerun()
    
# Create a unique conversation thread
if "thread_id" not in st.session_state:
    st.session_state.thread_id = "streamlit-008-run"


# Store chat messages for displaying in UI
if "messages" not in st.session_state:
    st.session_state.messages = []

if "pending_approval" not in st.session_state:
    st.session_state.pending_approval = False

# LangGraph configuration
config: RunnableConfig ={
    "configurable": {
        "thread_id": st.session_state.thread_id
    }
}

# Display previous messages
for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.write(message["content"])


# Chat input
user_input = st.chat_input(
    "Ask me about your healthcare insurance..."
)

if user_input:

    # Display user message
    with st.chat_message("user"):
        st.write(user_input)

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    
    # Send user message to LangGraph
    result = graph.invoke(  # type: ignore[arg-type]
        {
             "messages": [
                (
                    "user",
                    user_input
                )
            ]
        },# type: ignore[arg-type]
        config # type: ignore[arg-type]
    )  

    if "__interrupt__" in result:

        st.session_state.pending_approval = True

        st.session_state.approval_request = (
            result["__interrupt__"][0].value
        )

    else:

        final_response = result["messages"][-1].content

        with st.chat_message("assistant"):
            st.write(final_response)

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": final_response
            }
        )

    # Get final assistant response
    #final_response = result["messages"][-1].content

# Display assistant response
if st.session_state.pending_approval:

    st.warning(
        "⚠️ Human approval required before submitting the claim appeal."
    )

    approval_request = st.session_state.approval_request

    st.write(
        f"**Claim ID:** {approval_request.get('claim_id', 'Unknown')}"
    )

    col1, col2 = st.columns(2)

    with col1:
        if st.button("✅ Approve"):

            result = graph.invoke(
                Command(resume="approved"),
                config
            )
            print("\n========== AFTER APPROVAL ==========")
            print(result)
            print("====================================")
            st.session_state.pending_approval = False

            final_response = result["messages"][-1].content
            if "messages" in result:

                final_response = result["messages"][-1].content

                with st.chat_message("assistant"):
                    st.write(final_response)

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": final_response
                    }
                )

            st.rerun()

    with col2:
        if st.button("❌ Reject"):

            result = graph.invoke(
                Command(resume="rejected"),
                config
            )
            print("\n========== AFTER REJECTION ==========")
            print(result)
            print("=====================================")
            st.session_state.pending_approval = False

            final_response = result["messages"][-1].content
            if "messages" in result:

                final_response = result["messages"][-1].content

                with st.chat_message("assistant"):
                    st.write(final_response)

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": final_response
                    }
                )

            st.rerun()