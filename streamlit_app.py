import streamlit as st
import os
import requests
import time

st.title('Analyzer GPT - Digital Data Analyzer')

# Backend API URL
BACKEND_URL = os.getenv("BACKEND_URL", "http://backend:8000")

uploaded_file = st.file_uploader('Upload your Data file', type=['csv', 'xlsx', 'json'])

if 'messages' not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if "code" in msg and msg["code"]:
            with st.expander("Show Generated Python Code"):
                st.code(msg["code"], language="python")

task = st.chat_input("Enter your Task.")

if task:
    if uploaded_file is None:
        st.warning("Please upload a file")
    else:
        # Display user message
        with st.chat_message("user"):
            st.markdown(task)
        st.session_state.messages.append({"role": "user", "content": task})

        # Save file locally (which is mounted to backend)
        if not os.path.exists('temp'):
            os.makedirs('temp')

        # Determine file extension and name
        original_filename = uploaded_file.name
        file_path = os.path.join('temp', original_filename)
        
        with open(file_path, 'wb') as f:
            f.write(uploaded_file.getbuffer())

        # Call Backend API
        with st.chat_message("assistant"):
            with st.spinner("Analyzing..."):
                try:
                    response = requests.post(
                        f"{BACKEND_URL}/analyze",
                        json={"task": task, "filename": original_filename},
                        timeout=600  # 10 minutes timeout for long analysis
                    )
                    
                    if response.status_code == 200:
                        result = response.json()
                        final_msg = result.get("message", "Analysis completed.")
                        output_file = result.get("output_file")
                        generated_code = result.get("generated_code", "")
                        
                        st.markdown(final_msg)
                        if generated_code and generated_code != "# No code file generated.":
                             with st.expander("Show Generated Python Code"):
                                st.code(generated_code, language="python")

                        st.session_state.messages.append({
                            "role": "assistant", 
                            "content": final_msg,
                            "code": generated_code if generated_code != "# No code file generated." else None
                        })
                        
                        # Check for output image
                        # The backend says "output_file": "output.png"
                        # We expect it in 'temp/output.png' because of volume mount
                        image_path = f"temp/{output_file}"
                        if os.path.exists(image_path):
                            st.image(image_path, caption='Analysis Output')
                            # Optionally add image to chat history if supported, or just leave it as ephemeral
                    else:
                        error_msg = f"Error: {response.status_code} - {response.text}"
                        st.error(error_msg)
                        st.session_state.messages.append({"role": "assistant", "content": error_msg})
                
                except Exception as e:
                    error_msg = f"Connection failed: {str(e)}"
                    st.error(error_msg)
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})
