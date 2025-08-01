from transformers import RobertaTokenizer, RobertaForMaskedLM, pipeline
import torch
import re

def generate_comment(code_snippet, checkpoint="microsoft/codebert-base-mlm", device='cpu'):
    """
    Generate a comment for a given code snippet using CodeBERT.
    
    Args:
        code_snippet (str): The code to generate a comment for
        checkpoint (str): The model checkpoint to use
        device (str): 'cpu' or 'cuda' for GPU acceleration
        
    Returns:
        str: Generated comment for the code
    """
    try:
        # Load tokenizer and model
        tokenizer = RobertaTokenizer.from_pretrained(checkpoint)
        model = RobertaForMaskedLM.from_pretrained(checkpoint).to(device)
        
        # Parse the code to understand its structure
        code_lines = code_snippet.strip().split('\n')
        code_lines = [line for line in code_lines if line.strip()]
        
        # Different approach: use multiple strategies and combine results
        comments = []
        
        # Strategy 1: Use the first line with mask token
        if len(code_lines) > 0:
            prompt1 = f"# <mask> {code_lines[0]}"
            fill_mask = pipeline('fill-mask', model=model, tokenizer=tokenizer, device=0 if device=='cuda' else -1)
            predictions1 = fill_mask(prompt1)
            comment1 = predictions1[0]['sequence']
            # Extract just the comment part
            comment1 = comment1.split(code_lines[0])[0].replace('<s>', '').replace('#', '').strip()
            if comment1 and not comment1.startswith('<mask>') and len(comment1) > 3:
                comments.append(comment1)
        
        # Strategy 2: Analyze the function signature and body
        analyzed_comment = analyze_code(code_snippet)
        if analyzed_comment:
            comments.append(f"Function that {analyzed_comment}")
        
        # Strategy 3: Use a more descriptive prompt if it's a function
        func_match = re.search(r'def\s+([a-zA-Z0-9_]+)\s*\(([^)]*)\)', code_snippet)
        if func_match:
            func_name = func_match.group(1)
            params = func_match.group(2).strip()
            
            # Try to determine what the function returns
            return_pattern = re.search(r'return\s+(.+)', code_snippet)
            return_desc = ""
            if return_pattern:
                return_val = return_pattern.group(1).strip()
                if return_val.isdigit():
                    return_desc = f" and returns a number"
                elif return_val in ['True', 'False']:
                    return_desc = f" and returns a boolean"
                elif return_val.startswith('"') or return_val.startswith("'"):
                    return_desc = f" and returns a string"
                elif return_val.startswith('['):
                    return_desc = f" and returns a list"
                elif return_val.startswith('{'):
                    return_desc = f" and returns a dictionary"
                else:
                    return_desc = f" and returns {return_val}"
            
            if params:
                comments.append(f"The {func_name} function takes {params} as parameters{return_desc}")
            else:
                comments.append(f"The {func_name} function takes no parameters{return_desc}")
        
        # Combine the comments or use the best one
        if comments:
            # Sort by length and quality (prefer longer, more descriptive comments)
            comments.sort(key=lambda x: len(x), reverse=True)
            return comments[0]
        else:
            return "# Code implementation"
            
    except Exception as e:
        print(f"Error generating comment: {str(e)}")
        return "# " + analyze_code(code_snippet)

def analyze_code(code_snippet):
    """Advanced code analyzer to extract detailed information about the code"""
    # Extract function name and parameters if it's a function
    func_match = re.search(r'def\s+([a-zA-Z0-9_]+)\s*\(([^)]*)\)', code_snippet)
    if func_match:
        func_name = func_match.group(1)
        params = func_match.group(2).strip()
        
        # Check for specific algorithm implementations
        if 'binary' in func_name and ('search' in func_name or 'find' in func_name):
            # Check if it's actually a binary search implementation
            if ('mid' in code_snippet and 
                ('left' in code_snippet or 'low' in code_snippet) and 
                ('right' in code_snippet or 'high' in code_snippet)):
                return "implements binary search algorithm to efficiently find an element in a sorted array"
        
        # Try to determine the function's purpose based on common naming patterns
        if func_name.startswith('get_') or func_name.startswith('fetch_'):
            purpose = f"retrieves {func_name.split('_', 1)[1]}"
        elif func_name.startswith('set_'):
            purpose = f"sets {func_name.split('_', 1)[1]}"
        elif func_name.startswith('is_') or func_name.startswith('has_'):
            purpose = f"checks if {func_name.split('_', 1)[1]}"
        elif func_name.startswith('calc_') or func_name.startswith('compute_'):
            purpose = f"calculates {func_name.split('_', 1)[1]}"
        elif 'sum' in func_name or 'add' in func_name:
            purpose = "performs addition or summation"
        elif 'mult' in func_name or 'product' in func_name:
            purpose = "performs multiplication"
        elif 'div' in func_name:
            purpose = "performs division"
        elif 'factorial' in func_name:
            purpose = "calculates the factorial of a number"
        elif 'sort' in func_name:
            purpose = "sorts data"
        elif 'search' in func_name or 'find' in func_name:
            # Check for binary search implementation even if not in the name
            if ('mid' in code_snippet and 
                ('left' in code_snippet or 'low' in code_snippet) and 
                ('right' in code_snippet or 'high' in code_snippet)):
                purpose = "implements binary search algorithm to efficiently find an element in a sorted array"
            else:
                purpose = "searches for specific data"
        elif 'print' in func_name or 'display' in func_name or 'show' in func_name:
            purpose = "displays information"
        elif 'save' in func_name or 'store' in func_name:
            purpose = "saves data"
        elif 'load' in func_name or 'read' in func_name:
            purpose = "loads data"
        elif 'convert' in func_name or 'transform' in func_name:
            purpose = "converts or transforms data"
        elif 'validate' in func_name or 'check' in func_name:
            purpose = "validates or checks data"
        elif 'create' in func_name or 'generate' in func_name or 'make' in func_name:
            purpose = "creates or generates something"
        else:
            purpose = f"implements {func_name} functionality"
        
        # Check for recursion
        if func_name in code_snippet.split(func_match.group(0), 1)[1]:
            purpose += " using recursion"
            
        return purpose
    
    # Check for class definition
    class_match = re.search(r'class\s+([a-zA-Z0-9_]+)(?:\s*\(([^)]*)\))?', code_snippet)
    if class_match:
        class_name = class_match.group(1)
        parent_class = class_match.group(2) if class_match.group(2) else None
        
        if parent_class:
            return f"defines {class_name} class that inherits from {parent_class}"
        else:
            return f"defines {class_name} class"
    
    # Check for loop constructs
    if 'for ' in code_snippet and ' in ' in code_snippet:
        return "iterates through a collection of items"
    
    if 'while ' in code_snippet:
        return "executes a block of code repeatedly while a condition is true"
    
    # Check for conditional statements
    if 'if ' in code_snippet and ': ' in code_snippet:
        return "executes code based on conditional logic"
    
    # Default response
    return "performs the specified operation"

def extract_functions_and_classes(code):
    """Extract functions and classes from code"""
    # Pattern to match function definitions
    function_pattern = re.compile(r'(def\s+[a-zA-Z0-9_]+\s*\([^)]*\)\s*:(?:[^\n]*\n+(?:[ \t]+[^\n]*\n+)*)?)', re.MULTILINE)
    
    # Pattern to match class definitions
    class_pattern = re.compile(r'(class\s+[a-zA-Z0-9_]+(?:\s*\([^)]*\))?\s*:(?:[^\n]*\n+(?:[ \t]+[^\n]*\n+)*)?)', re.MULTILINE)
    
    # Find all functions and classes
    functions = function_pattern.findall(code)
    classes = class_pattern.findall(code)
    
    # Combine and return all code blocks
    return functions + classes

def extract_class_methods(code_block):
    """Extract methods from a class definition"""
    # First, check if this is a class definition
    if not code_block.strip().startswith('class '):
        return []
    
    # Get the class body (everything after the class definition line)
    class_lines = code_block.strip().split('\n')
    class_body = '\n'.join(class_lines[1:]) if len(class_lines) > 1 else ''
    
    # Pattern to match method definitions within a class
    method_pattern = re.compile(r'([ \t]+def\s+[a-zA-Z0-9_]+\s*\([^)]*\)\s*:(?:[^\n]*\n+(?:[ \t]+[^\n]*\n+)*)*)', re.MULTILINE)
    
    # Find all methods
    methods = method_pattern.findall(class_body)
    
    # Clean up the methods (ensure they have proper indentation)
    cleaned_methods = []
    for method in methods:
        # Skip empty methods
        if not method.strip():
            continue
        cleaned_methods.append(method)
    
    return cleaned_methods

def process_file(file_path):
    """Process a Python file and generate comments for each function and class"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            code = f.read()
        
        # Extract functions and classes
        code_blocks = extract_functions_and_classes(code)
        
        if not code_blocks:
            print(f"No functions or classes found in {file_path}")
            return
        
        print(f"\nProcessing {file_path}...\n")
        
        # Generate comments for each code block
        for i, block in enumerate(code_blocks):
            # Get the first line to identify the block
            first_line = block.strip().split('\n')[0]
            
            # Check if this is a class definition
            if first_line.startswith('class '):
                # Generate comment for the class
                device = 'cuda' if torch.cuda.is_available() else 'cpu'
                class_comment = generate_comment(block, device=device)
                
                print(f"# {class_comment}")
                print(block)
                print()
                
                # Extract and process methods within the class
                methods = extract_class_methods(block)
                for j, method in enumerate(methods):
                    # Generate comment for the method
                    method_comment = generate_comment(method, device=device)
                    
                    print(f"# {method_comment}")
                    print(method)
                    print()
            else:
                # Generate comment for the function
                device = 'cuda' if torch.cuda.is_available() else 'cpu'
                comment = generate_comment(block, device=device)
                
                print(f"# {comment}")
                print(block)
                print()
            
    except Exception as e:
        print(f"Error processing file {file_path}: {str(e)}")

def save_comments_to_file(file_path, output_file=None):
    """Process a Python file and save generated comments to an output file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            code = f.read()
        
        # Extract functions and classes
        code_blocks = extract_functions_and_classes(code)
        
        if not code_blocks:
            result = f"No functions or classes found in {file_path}"
            print(result)
            if output_file:
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(result + '\n')
            return
        
        # Prepare output
        output = []
        output.append(f"Processing {file_path}...\n")
        
        # Generate comments for each code block
        for i, block in enumerate(code_blocks):
            # Get the first line to identify the block
            first_line = block.strip().split('\n')[0]
            
            # Check if this is a class definition
            if first_line.startswith('class '):
                # Generate comment for the class
                device = 'cuda' if torch.cuda.is_available() else 'cpu'
                class_comment = generate_comment(block, device=device)
                
                output.append(f"# {class_comment}\n")
                output.append(block + "\n")
                
                # Extract and process methods within the class
                methods = extract_class_methods(block)
                for j, method in enumerate(methods):
                    # Generate comment for the method
                    method_comment = generate_comment(method, device=device)
                    
                    output.append(f"# {method_comment}\n")
                    output.append(method + "\n")
            else:
                # Generate comment for the function
                device = 'cuda' if torch.cuda.is_available() else 'cpu'
                comment = generate_comment(block, device=device)
                
                output.append(f"# {comment}\n")
                output.append(block + "\n")
        
        # Print to console
        for line in output:
            print(line, end='')
        
        # Save to file if specified
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                for line in output:
                    f.write(line)
            print(f"\nComments saved to {output_file}")
            
    except Exception as e:
        error_msg = f"Error processing file {file_path}: {str(e)}"
        print(error_msg)
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(error_msg + '\n')

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        # Process the specified file
        file_path = sys.argv[1]
        
        # Check if output file is specified
        output_file = None
        if len(sys.argv) > 2:
            output_file = sys.argv[2]
        else:
            # Default output file name
            output_file = file_path + "_comments.txt"
        
        save_comments_to_file(file_path, output_file)
    else:
        # Use the default example if no file is provided
        test_code = """
def factorial(n):
    if n == 0:
        return 1
    else:
        return n * factorial(n - 1)
"""
        comment = generate_comment(test_code, device='cuda' if torch.cuda.is_available() else 'cpu')
        print("Generated Comment:\n", comment)
