import google.generativeai as genai
import ast
import streamlit as st

# === SET YOUR GEMINI API KEY HERE ===
GEMINI_API_KEY = "AIzaSyCAHn4hvnJp3i-ZDgjLJtyujKeU0GIjLh4"  # <-- Replace with your Gemini API key from Google AI Studio

genai.configure(api_key=GEMINI_API_KEY)

def generate_docstring_gemini(code_snippet, node_type):
    """
    Generate a concise, necessary docstring for a given Python code snippet using Gemini.
    """
    prompt = (
        f'You are an expert Python developer. Write a concise, necessary docstring for the following {node_type}.'
        f' Only add a docstring if it is truly needed. Be brief and avoid over-commenting.'
        f' Do NOT repeat or restate the code; only explain what it does, its purpose, and any important details.'
        f' Include only what is essential for understanding the code.'
        f'\nCode:\n{code_snippet}\nDocstring:'
    )
    model = genai.GenerativeModel("gemini-1.5-flash-002")
    response = model.generate_content(prompt)
    docstring = response.text.strip()
    docstring = docstring.strip('"""').strip()
    return f'"""{docstring}"""'


def extract_functions_and_classes(code):
    """
    Extracts functions and classes from code using AST.
    Returns a list of (start_line, end_line, code_snippet, node_type) tuples for those WITHOUT a docstring.
    """
    tree = ast.parse(code)
    results = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            # Skip if node already has a docstring
            if ast.get_docstring(node):
                continue
            start_line = getattr(node, 'lineno', None)
            end_line = getattr(node, 'end_lineno', None)
            if start_line is None:
                continue
            if end_line is None:
                end_line = start_line
                for child in ast.walk(node):
                    child_end = getattr(child, 'end_lineno', None)
                    child_line = getattr(child, 'lineno', None)
                    if child_end is not None:
                        end_line = max(end_line, child_end)
                    elif child_line is not None:
                        end_line = max(end_line, child_line)
            snippet = "\n".join(code.splitlines()[start_line-1:end_line])
            node_type = "function" if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) else "class"
            results.append((start_line, end_line, snippet, node_type))
    results.sort(reverse=True, key=lambda x: x[0])
    return results

def insert_docstrings(code):
    """
    Inserts generated docstrings as the first statement inside each function and class in the code.
    """
    lines = code.splitlines()
    items = extract_functions_and_classes(code)
    for start, end, snippet, node_type in items:
        docstring = generate_docstring_gemini(snippet, node_type)
        # Find the correct indentation
        indent = ""
        def_line = lines[start-1]
        for char in def_line:
            if char in " \t":
                indent += char
            else:
                break
        docstring_lines = [(indent + "    " + l if l else "") for l in docstring.splitlines()]
        insert_at = start
        while insert_at < len(lines) and lines[insert_at].strip().startswith("@"):
            insert_at += 1
        lines[insert_at:insert_at] = docstring_lines
    return "\n".join(lines)

def comment_code(code):
    """
    Main function for Gradio: adds detailed docstrings to all functions/classes in the code.
    """
    try:
        commented_code = insert_docstrings(code)
        return commented_code
    except Exception as e:
        return f"Error processing code: {e}"

if __name__ == "__main__":
    st.set_page_config(page_title="Code Docstring Generator (Gemini)")
    st.title("Code Docstring Generator (Gemini)")
    st.write("Adds clear, human-like docstrings to each function and class in your Python code using Google Gemini.")
    code = st.text_area("Paste your Python code here", height=400)
    if st.button("Generate Docstrings"):
        if code.strip():
            with st.spinner("Generating docstrings with Gemini..."):
                result = comment_code(code)
            st.text_area("Code with Gemini Docstrings", value=result, height=440)
        else:
            st.warning("Please paste your Python code above.") 