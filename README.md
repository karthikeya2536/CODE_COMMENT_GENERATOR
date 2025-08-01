# Code Comment Generator - CodeBERT for Inline Code Comments

## Overview
This project uses Microsoft's CodeBERT model to generate intelligent inline code comments for multiple programming languages. It provides both a web interface and command-line tools for easy code comment generation.

## Features
- **CodeBERT Integration**: Uses Microsoft's `microsoft/codebert-base-mlm` model for intelligent comment generation
- **Web Interface**: User-friendly HTML interface for interactive code comment generation
- **Command Line Interface**: Python script for batch processing and file-based comment generation
- **Multi-language Support**: Works with Python, Java, JavaScript, Ruby, Go, and PHP
- **Clean Output**: Generates clean, readable comments without HTML markup or class labels
- **Advanced Code Analysis**: Intelligently analyzes code structure to generate meaningful comments

## Project Structure
```
CODE COMMENT GENERATOR/
├── infer.py              # Main inference script using CodeBERT
├── code_demo.html        # Web interface for code comment generation
├── requirements.txt      # Python dependencies
├── README.md            # Project documentation
└── .gitignore           # Git ignore rules
```

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/karthikeya2536/CODE_COMMENT_GENERATOR.git
   cd CODE_COMMENT_GENERATOR
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Option 1: Web Interface (Recommended for beginners)

1. **Open the web interface**:
   ```bash
   # On Windows
   start code_demo.html
   
   # On macOS/Linux
   open code_demo.html
   ```

2. **Use the interface**:
   - Paste your code in the text area
   - Select the programming language
   - Click "Generate Comments"
   - View the commented code in the output section

### Option 2: Command Line Interface

1. **Generate comments for a specific file**:
   ```bash
   python infer.py your_file.py
   ```

2. **Generate comments and save to output file**:
   ```bash
   python infer.py your_file.py output_file.txt
   ```

3. **Use the default example**:
   ```bash
   python infer.py
   ```

### Option 3: Programmatic Usage

```python
from infer import generate_comment

# Generate comment for a code snippet
code = """
def factorial(n):
    if n == 0:
        return 1
    else:
        return n * factorial(n - 1)
"""

comment = generate_comment(code)
print(comment)
# Output: "Function that calculates the factorial of a number using recursion"
```

## Example Output

### Input Code:
```javascript
const todoInput = document.getElementById('todoInput');
const addTodoBtn = document.getElementById('addTodoBtn');
const todoList = document.getElementById('todoList');

function addTodo() {
    const taskText = todoInput.value.trim();
    if (taskText === '') {
        alert('Please enter a task!');
        return;
    }
    // ... rest of the function
}
```

### Generated Comments:
```javascript
// JavaScript code for todo list management
const todoInput = document.getElementById('todoInput');  // Stores the todo input
const addTodoBtn = document.getElementById('addTodoBtn');  // Stores the add todo btn
const todoList = document.getElementById('todoList');  // Stores the todo list

function addTodo() {  // Handles add todo functionality
    const taskText = todoInput.value.trim();  // Stores the task text
    if (taskText === '') {  // Checks the specified condition
        alert('Please enter a task!');
        return;
    }
    // ... rest of the function
}
```

## Model Details

This project uses **Microsoft's CodeBERT** (`microsoft/codebert-base-mlm`), which is:
- A BERT-based model pretrained on code in multiple programming languages
- Uses masked language modeling to understand and generate code-related text
- Provides intelligent code analysis and comment generation
- Supports multiple programming languages including Python, Java, JavaScript, Ruby, Go, and PHP

## Key Features

### Intelligent Code Analysis
- **Function Detection**: Automatically identifies functions and their purposes
- **Parameter Analysis**: Analyzes function parameters and return types
- **Algorithm Recognition**: Detects common algorithms (e.g., binary search, sorting)
- **Class Analysis**: Identifies class definitions and their purposes

### Clean Output Format
- **No HTML Markup**: Output is clean without class attributes or HTML tags
- **Readable Comments**: Generates human-readable, meaningful comments
- **Consistent Formatting**: Maintains proper code formatting and indentation

### Multi-Platform Support
- **Web Interface**: Works in any modern web browser
- **Command Line**: Cross-platform Python script
- **Programmatic API**: Can be integrated into other Python projects

## Requirements

- Python 3.7+
- PyTorch
- Transformers library
- CUDA (optional, for GPU acceleration)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the MIT License.

## Acknowledgments

- Microsoft for the CodeBERT model
- Hugging Face for the Transformers library
- The open-source community for various tools and libraries used in this project
