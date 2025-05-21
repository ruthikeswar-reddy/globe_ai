import streamlit as st
import requests

st.set_page_config(page_title="Restaurant Recommender", page_icon="🍽️")

st.title("🍽️ Restaurant Recommendation Chatbot")

st.markdown(
    "I can help you find restaurant recommendations based on your preferences. "
    "Please ask a question related to restaurant."
)

# Input text box
user_question = st.text_input("Your question:")

# Button to trigger the request
if st.button("Ask"):
    if user_question.strip() == "":
        st.warning("Please enter a question.")
    else:
        with st.spinner("Thinking..."):
            try:
                # Replace this URL with your FastAPI backend endpoint
                API_URL = "http://127.0.0.1:8000/ask"

                # Send the user question to the backend API
                response = requests.post(API_URL, json={"user_question": user_question})

                if response.status_code == 200:
                    # Extract the response from the backend
                    data = response.json()

                    # Check if the backend response contains an answer
                    if "response" in data:
                        answer = data["response"]
                        st.success("Here's what I found:")
                        st.markdown(answer)
                    else:
                        # If no answer is found, show a generic message
                        st.info("Sorry, I couldn't find any relevant recommendations for your query.")
                elif response.status_code == 400:
                    # Handle the irrelevant query case
                    data = response.json()
                    if "detail" in data and data["detail"] == "The question is irrelevant.":
                        st.info(
                            "Sorry, the question seems irrelevant. I can only answer restaurant-related queries. "
                            "Please ask about restaurant recommendations in your city."
                        )
                    else:
                        st.error(f"Error from backend: {response.status_code} - {response.text}")
                else:
                    st.error(f"Error from backend: {response.status_code} - {response.text}")
            except requests.exceptions.RequestException as e:
                st.error(f"Request failed: {e}")
