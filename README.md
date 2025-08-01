# Code Comment Generator - CodeBERT for Inline Code Comments

## Overview
This project fine-tunes Microsoft's CodeBERT model to generate inline code comments for multiple programming languages using the CodeSearchNet dataset.

## Structure
- `load_data.py`: Loads and preprocesses the CodeSearchNet dataset for multiple programming languages.
- `tokenize_dataset.py`: Tokenizes the dataset for CodeBERT model input using masked language modeling approach.
- `train.py`: Fine-tunes the pretrained CodeBERT model on code comment generation.
- `infer.py`: Generates inline comments for new code snippets using the fine-tuned model.

## Model Details
This project uses Microsoft's CodeBERT model (`microsoft/codebert-base-mlm`), which is a BERT-based model pretrained on code in multiple programming languages. Unlike sequence-to-sequence models, CodeBERT uses masked language modeling to understand and generate code-related text.

## Instructions
1. Ensure the CodeSearchNet dataset is available in the `CodeSearchNet/` directory with language subdirectories.
2. Install dependencies: `pip install -r requirements.txt`
3. Run training: `python train.py`
4. Generate comments for your code: `python infer.py`

## Example Usage
```python
from infer import generate_comment

code = """
def factorial(n):
    if n == 0:
        return 1
    else:
        return n * factorial(n - 1)"""

comment = generate_comment(code)
print(comment)
```

## Notes
- The model works best with well-structured code snippets.
- Adjust batch sizes and epochs in `train.py` based on your hardware capabilities.
- Using a GPU is highly recommended for faster training and inference.
- The model supports Python, Java, JavaScript, Ruby, Go, and PHP.
