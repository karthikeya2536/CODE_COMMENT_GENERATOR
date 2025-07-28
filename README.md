# CODE_COMMENT_GENERATOR

A simple web app that automatically generates concise, human-like docstrings for your Python functions and classes using Google Gemini.

## Features

- **Streamlit UI**: Paste your Python code and get back code with only necessary docstrings.
- **No Over-Commenting**: Only adds docstrings where missing, and avoids repeating code in comments.
- **Powered by Gemini**: Uses Google Gemini API for high-quality, human-like explanations.

## Usage

1. **Install dependencies:**
   ```
   pip install -r requirements.txt
   ```

2. **Set your Gemini API key:**
   - Open `code_comment_generator_gemini.py`
   - Replace the value of `GEMINI_API_KEY` with your key from [Google AI Studio](https://aistudio.google.com/app/apikey).

3. **Run the app:**
   ```
   streamlit run code_comment_generator_gemini.py
   ```

4. **Paste your Python code** in the text area and click "Generate Docstrings".

## Example

Paste this code:
```python
def add(a, b):
    return a + b
```

Get back:
```python
def add(a, b):
    """Returns the sum of a and b."""
    return a + b
```

## License

MIT
