# Code Comment Generator


## Overview

The Code Comment Generator is a web application that leverages a large language model to automatically generate inline comments for your Python code. This tool is designed to help developers improve code readability and documentation with minimal effort. Simply paste your Python code into the application, and the AI will analyze it and suggest relevant comments.

This project is built with [Streamlit](https://streamlit.io/) and uses the `edumunozsala/llama-2-7b-int4-python-code-20k` model from [Hugging Face](https://huggingface.co/).

## Features

-   **AI-Powered Comment Generation:** Automatically generates inline comments for Python code.
-   **Interactive Web Interface:** A user-friendly interface built with Streamlit for easy interaction.
-   **Powered by Hugging Face Transformers:** Utilizes a powerful language model for accurate and relevant comment generation.
-   **Easy to Deploy:** Can be easily deployed on Streamlit Community Cloud.

## Getting Started

To run this project locally, follow these steps:

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/karthikeya2536/CODE_COMMENT_GENERATOR.git
    cd CODE_COMMENT_GENERATOR
    ```

2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the Streamlit app:**
    ```bash
    streamlit run app.py
    ```

## Deployment

This application is ready to be deployed on [Streamlit Community Cloud](https://streamlit.io/cloud).

1.  **Push your code to the GitHub repository.**
2.  **Sign up for Streamlit Community Cloud.**
3.  **Click "New app" and connect your GitHub repository.**
4.  **Select the repository and the `app.py` file, then click "Deploy!".**

## Contributing

Contributions are welcome! If you have any ideas, suggestions, or bug reports, please open an issue or submit a pull request in this repository: [https://github.com/karthikeya2536/CODE_COMMENT_GENERATOR](https://github.com/karthikeya2536/CODE_COMMENT_GENERATOR).

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
