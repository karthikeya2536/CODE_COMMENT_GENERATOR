import streamlit as st
import torch
from infer import generate_comment, process_file, save_comments_to_file
import tempfile
import os

# Page configuration
st.set_page_config(
    page_title="Code Comment Generator",
    page_icon="💻",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #2c3e50;
        margin-bottom: 1rem;
    }
    .code-block {
        background-color: #f8f9fa;
        border-left: 4px solid #1f77b4;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
    }
    .info-box {
        background-color: #d1ecf1;
        border: 1px solid #bee5eb;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Header
    st.markdown('<h1 class="main-header">💻 Code Comment Generator</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; font-size: 1.2rem; color: #666;">Powered by Microsoft CodeBERT</p>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Settings")
        
        # Device selection
        device = st.selectbox(
            "Select Device",
            ["cpu", "cuda"] if torch.cuda.is_available() else ["cpu"],
            help="Choose CPU or GPU (CUDA) for processing"
        )
        
        # Language selection
        language = st.selectbox(
            "Programming Language",
            ["python", "javascript", "java", "csharp", "go", "ruby", "php"],
            help="Select the programming language of your code"
        )
        
        st.markdown("---")
        st.markdown("### 📊 Model Info")
        st.info(f"Using: **Microsoft CodeBERT**\n\nDevice: **{device.upper()}**\n\nLanguage: **{language.title()}**")
        
        st.markdown("---")
        st.markdown("### 🚀 Features")
        st.markdown("""
        - ✅ Intelligent code analysis
        - ✅ Multi-language support
        - ✅ Clean output format
        - ✅ Function & class detection
        - ✅ Parameter analysis
        """)
    
    # Main content
    tab1, tab2, tab3 = st.tabs(["📝 Single Code", "📁 File Upload", "ℹ️ About"])
    
    with tab1:
        st.markdown('<h2 class="sub-header">Generate Comments for Code Snippet</h2>', unsafe_allow_html=True)
        
        # Code input
        code_input = st.text_area(
            "Paste your code here:",
            height=300,
            placeholder="def example_function(param):\n    # Your code here\n    return result",
            help="Paste your code snippet to generate comments"
        )
        
        col1, col2 = st.columns([1, 4])
        
        with col1:
            if st.button("🚀 Generate Comments", type="primary"):
                if code_input.strip():
                    with st.spinner("🤖 Analyzing code and generating comments..."):
                        try:
                            # Generate comment
                            comment = generate_comment(code_input, device=device)
                            
                            # Display results
                            st.success("✅ Comments generated successfully!")
                            
                            # Show original code
                            st.markdown("### 📄 Original Code")
                            st.code(code_input, language=language)
                            
                            # Show commented code
                            st.markdown("### 💬 Commented Code")
                            commented_code = f"# {comment}\n{code_input}"
                            st.code(commented_code, language=language)
                            
                            # Download button
                            st.download_button(
                                label="📥 Download Commented Code",
                                data=commented_code,
                                file_name=f"commented_code.{language}",
                                mime="text/plain"
                            )
                            
                        except Exception as e:
                            st.error(f"❌ Error generating comments: {str(e)}")
                else:
                    st.warning("⚠️ Please enter some code first!")
        
        with col2:
            st.markdown("### 💡 Tips")
            st.markdown("""
            - **Functions**: The model will analyze function names and parameters
            - **Classes**: Class definitions and methods will be identified
            - **Algorithms**: Common algorithms like binary search are automatically detected
            - **Variables**: Important variables and their purposes will be commented
            """)
    
    with tab2:
        st.markdown('<h2 class="sub-header">Upload and Process Files</h2>', unsafe_allow_html=True)
        
        uploaded_file = st.file_uploader(
            "Choose a file to process:",
            type=['py', 'js', 'java', 'cpp', 'c', 'cs', 'go', 'rb', 'php'],
            help="Upload a code file to generate comments for all functions and classes"
        )
        
        if uploaded_file is not None:
            # Read file content
            file_content = uploaded_file.read().decode("utf-8")
            
            st.markdown("### 📄 File Preview")
            st.code(file_content, language=language)
            
            if st.button("🔍 Process File", type="primary"):
                with st.spinner("🤖 Processing file and generating comments..."):
                    try:
                        # Create temporary file
                        with tempfile.NamedTemporaryFile(mode='w', suffix=f'.{language}', delete=False) as tmp_file:
                            tmp_file.write(file_content)
                            tmp_file_path = tmp_file.name
                        
                        # Process the file
                        output_content = []
                        
                        # Capture the output
                        import io
                        import sys
                        from contextlib import redirect_stdout
                        
                        f = io.StringIO()
                        with redirect_stdout(f):
                            process_file(tmp_file_path)
                        output_content = f.getvalue()
                        
                        # Clean up temporary file
                        os.unlink(tmp_file_path)
                        
                        # Display results
                        st.success("✅ File processed successfully!")
                        
                        st.markdown("### 💬 Generated Comments")
                        st.text(output_content)
                        
                        # Download button
                        st.download_button(
                            label="📥 Download Commented File",
                            data=output_content,
                            file_name=f"commented_{uploaded_file.name}",
                            mime="text/plain"
                        )
                        
                    except Exception as e:
                        st.error(f"❌ Error processing file: {str(e)}")
    
    with tab3:
        st.markdown('<h2 class="sub-header">About Code Comment Generator</h2>', unsafe_allow_html=True)
        
        st.markdown("""
        ### 🤖 What is CodeBERT?
        CodeBERT is a pre-trained model for programming and natural language developed by Microsoft. 
        It's designed to understand the relationship between code and natural language, making it 
        perfect for generating intelligent code comments.
        
        ### 🎯 How it Works
        1. **Code Analysis**: The model analyzes your code structure
        2. **Pattern Recognition**: Identifies functions, classes, and algorithms
        3. **Comment Generation**: Creates meaningful, human-readable comments
        4. **Clean Output**: Delivers clean code with inline comments
        
        ### 🌟 Key Features
        - **Multi-language Support**: Python, JavaScript, Java, C#, Go, Ruby, PHP
        - **Intelligent Analysis**: Understands code context and purpose
        - **Clean Formatting**: No HTML markup or unnecessary attributes
        - **Easy to Use**: Simple web interface and command-line tools
        
        ### 🛠️ Technical Details
        - **Model**: Microsoft CodeBERT (`microsoft/codebert-base-mlm`)
        - **Framework**: PyTorch + Transformers
        - **Interface**: Streamlit web app
        - **Processing**: CPU/GPU support
        
        ### 📚 Example Usage
        ```python
        from infer import generate_comment
        
        code = '''
        def binary_search(arr, target):
            left, right = 0, len(arr) - 1
            while left <= right:
                mid = (left + right) // 2
                if arr[mid] == target:
                    return mid
                elif arr[mid] < target:
                    left = mid + 1
                else:
                    right = mid - 1
            return -1
        '''
        
        comment = generate_comment(code)
        print(comment)
        # Output: "implements binary search algorithm to efficiently find an element in a sorted array"
        ```
        """)
        
        st.markdown("---")
        st.markdown("### 🔗 Links")
        st.markdown("""
        - [GitHub Repository](https://github.com/karthikeya2536/CODE_COMMENT_GENERATOR)
        - [Microsoft CodeBERT Paper](https://arxiv.org/abs/2002.08155)
        - [Hugging Face Transformers](https://huggingface.co/transformers/)
        """)

if __name__ == "__main__":
    main() 