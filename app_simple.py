"""
AI Code Commenter - Simple Streamlit Web Application

A simplified, working web interface for adding comments to code.
"""

import streamlit as st
import os
import sys
import tempfile
from pathlib import Path

# Configure page
st.set_page_config(
    page_title="AI Code Commenter",
    page_icon="🤖",
    layout="wide"
)

def detect_language_simple(code_text, filename=""):
    """Enhanced language detection for multiple programming languages."""
    code_lower = code_text.lower()
    
    # Filename-based detection (most reliable)
    if filename:
        ext = filename.lower().split('.')[-1] if '.' in filename else ''
        ext_map = {
            'py': 'python',
            'js': 'javascript', 'mjs': 'javascript', 'jsx': 'javascript',
            'ts': 'typescript', 'tsx': 'typescript',
            'java': 'java',
            'cpp': 'cpp', 'cc': 'cpp', 'cxx': 'cpp', 'c++': 'cpp',
            'c': 'c',
            'cs': 'csharp',
            'go': 'go',
            'rs': 'rust',
            'php': 'php',
            'rb': 'ruby',
            'swift': 'swift',
            'kt': 'kotlin',
            'scala': 'scala',
            'pl': 'perl',
            'lua': 'lua',
            'sh': 'bash', 'bash': 'bash',
            'ps1': 'powershell',
            'r': 'r',
            'sql': 'sql',
            'html': 'html',
            'css': 'css'
        }
        if ext in ext_map:
            return ext_map[ext]
    
    # Content-based detection with improved patterns
    patterns = {
        'python': ['def ', 'import ', 'from ', '__name__', 'elif ', 'print('],
        'javascript': ['function ', 'var ', 'let ', 'const ', 'console.log', '=>', 'document.'],
        'typescript': ['interface ', 'type ', ': string', ': number', ': boolean'],
        'java': ['public class', 'private ', 'system.out', 'public static void main'],
        'cpp': ['#include', 'using namespace', 'std::', 'cout <<', 'cin >>'],
        'c': ['#include', 'int main', 'printf(', 'scanf(', 'malloc('],
        'csharp': ['using system', 'public class', 'console.write', 'string[]'],
        'go': ['package ', 'func main', 'import ', 'fmt.print'],
        'rust': ['fn main', 'let mut', 'println!', 'use std::'],
        'ruby': ['def ', 'puts ', 'require ', 'class ', 'end'],
        'php': ['<?php', 'echo ', '$', 'function '],
        'swift': ['func ', 'var ', 'let ', 'print(', 'import foundation'],
        'kotlin': ['fun ', 'val ', 'var ', 'println('],
        'scala': ['def ', 'val ', 'var ', 'object '],
        'r': ['<- ', 'function(', 'library(', 'data.frame'],
        'sql': ['select ', 'insert ', 'update ', 'delete ', 'from ', 'where '],
        'html': ['<html', '<div', '<body', '<!doctype']
    }
    
    # Count pattern matches for each language
    scores = {}
    for lang, lang_patterns in patterns.items():
        score = sum(1 for pattern in lang_patterns if pattern in code_lower)
        if score > 0:
            scores[lang] = score
    
    # Return language with highest score
    if scores:
        return max(scores, key=scores.get)
    
    return 'text'

def get_meaningful_comment(line, language='python'):
    """Generate meaningful comments for multiple programming languages."""
    stripped = line.strip()
    
    # Function definitions (Multi-language)
    func_patterns = ['def ', 'function ', 'func ', 'fn ', 'public ', 'private ', 'static ']
    for pattern in func_patterns:
        if pattern in stripped and '(' in stripped:
            # Extract function name
            if 'def ' in stripped:
                func_name = stripped.split('(')[0].replace('def ', '').strip()
            elif 'function ' in stripped:
                func_name = stripped.split('(')[0].replace('function ', '').strip()
            elif 'fn ' in stripped:
                func_name = stripped.split('(')[0].replace('fn ', '').strip()
            elif any(mod in stripped for mod in ['public ', 'private ', 'static ']):
                # Java/C#/C++ style
                parts = stripped.split('(')[0].split()
                func_name = parts[-1] if parts else "function"
            else:
                func_name = stripped.split('(')[0].split()[-1]
            
            return f"Define {func_name.replace('_', ' ')} function"
    
    # Class definitions (Multi-language)
    if stripped.startswith('class ') or stripped.startswith('struct '):
        keyword = 'class' if 'class' in stripped else 'struct'
        class_name = stripped.split()[1].split('(')[0].split('{')[0].replace(':', '').strip()
        return f"Define {class_name} {keyword}"
    
    # Import/Include statements
    import_patterns = ['import ', 'from ', '#include', 'using ', 'require(', 'use ', 'extern crate']
    if any(pattern in stripped for pattern in import_patterns):
        return "Import required modules/libraries"
    
    # Variable declarations and assignments
    if '=' in stripped and not any(op in stripped for op in ['==', '!=', '<=', '>=', '===', '!==']):
        # Handle different assignment patterns
        var_part = stripped.split('=')[0].strip()
        value_part = stripped.split('=')[1].strip()
        
        # Extract variable name (handle var, let, const, type declarations)
        var_name = var_part
        for keyword in ['var ', 'let ', 'const ', 'int ', 'float ', 'double ', 'string ', 'bool ', 'char ', 'auto ']:
            var_name = var_name.replace(keyword, '')
        var_name = var_name.split()[-1] if var_name.split() else "variable"
        
        # Analyze value being assigned
        if any(pattern in value_part for pattern in ['input(', 'scanf(', 'cin >>', 'Scanner.', 'prompt(', 'readline()']):
            return f"Get {var_name.replace('_', ' ')} from user input"
        elif any(pattern in value_part for pattern in ['[]', '{}', 'new Array', 'new List', 'vector<', 'make_vec']):
            return f"Initialize {var_name.replace('_', ' ')} collection"
        elif any(pattern in value_part for pattern in ['new ', 'malloc(', 'calloc(']):
            return f"Create new {var_name.replace('_', ' ')} instance"
        elif '.split(' in value_part or '.Split(' in value_part:
            return f"Split string into {var_name.replace('_', ' ')}"
        elif any(func in value_part for func in ['len(', 'length', 'size(', 'count(', 'Length', 'Count']):
            return f"Get {var_name.replace('_', ' ')} count"
        else:
            return f"Set {var_name.replace('_', ' ')} value"
    
    # Loop statements (Multi-language)
    loop_patterns = [
        ('for (', "Loop with counter"),
        ('for ', "Loop through collection"),
        ('while (', "Loop while condition is true"),
        ('while ', "Loop while condition is true"),
        ('do {', "Execute at least once then loop"),
        ('foreach (', "Loop through each item"),
        ('for item in', "Loop through each item"),
        ('for i in range', "Loop through number sequence"),
        ('for (let', "Loop through items"),
        ('for (const', "Loop through items")
    ]
    
    for pattern, comment in loop_patterns:
        if stripped.startswith(pattern):
            return comment
    
    # Conditional statements (Multi-language)
    if any(stripped.startswith(pattern) for pattern in ['if (', 'if ', 'elsif ', 'else if', 'elif ']):
        if any(check in stripped for check in ['null', 'NULL', 'nil', 'None', 'undefined']):
            return "Check if value exists"
        elif any(check in stripped for check in ['length', 'Length', 'size(', 'len(', 'count']):
            return "Check collection size"
        elif any(check in stripped for check in ['instanceof', 'typeof', 'isinstance', 'is_a?']):
            return "Check variable type"
        else:
            return "Check condition"
    
    if stripped.startswith('else') and ('{' in stripped or ':' in stripped):
        return "Handle alternative case"
    
    # Return statements (Multi-language)
    if any(stripped.startswith(pattern) for pattern in ['return ', 'return;']):
        return "Return result"
    
    # Exception handling (Multi-language)
    exception_patterns = [
        ('try', "Try potentially risky operation"),
        ('catch', "Handle exception"),
        ('except', "Handle exception"),
        ('finally', "Execute cleanup code"),
        ('rescue', "Handle error"),
        ('ensure', "Execute cleanup code")
    ]
    
    for pattern, comment in exception_patterns:
        if stripped.startswith(pattern):
            return comment
    
    # Output statements (Multi-language)
    output_patterns = ['print(', 'printf(', 'cout <<', 'console.log(', 'System.out.', 'puts(', 'echo ', 'println!']
    if any(pattern in stripped for pattern in output_patterns):
        return "Display output"
    
    # Common method calls
    method_patterns = [
        ('.append(', 'Add item to collection'),
        ('.push(', 'Add item to collection'),
        ('.pop(', 'Remove item from collection'),
        ('.remove(', 'Remove item from collection'),
        ('.sort(', 'Sort collection'),
        ('.reverse(', 'Reverse collection order'),
        ('.clear(', 'Empty collection'),
        ('.close(', 'Close resource'),
        ('.flush(', 'Flush buffer'),
        ('.commit(', 'Save changes'),
        ('.rollback(', 'Undo changes'),
        ('.connect(', 'Establish connection'),
        ('.disconnect(', 'Close connection'),
        ('.execute(', 'Execute operation'),
        ('.query(', 'Run database query')
    ]
    
    for pattern, comment in method_patterns:
        if pattern in stripped:
            return comment
    
    # Control flow statements
    control_patterns = [
        ('break;', "Exit the loop"),
        ('break', "Exit the loop"),
        ('continue;', "Skip to next iteration"),
        ('continue', "Skip to next iteration"),
        ('pass', "No operation placeholder"),
        ('yield ', "Return generator value")
    ]
    
    for pattern, comment in control_patterns:
        if stripped == pattern or stripped.startswith(pattern):
            return comment
    
    # Memory management (C/C++)
    if any(pattern in stripped for pattern in ['malloc(', 'calloc(', 'new ', 'delete ', 'free(']):
        return "Manage memory allocation"
    
    # Threading/Async
    if any(pattern in stripped for pattern in ['async ', 'await ', 'Promise', 'Thread', 'pthread_', 'go func', 'spawn']):
        return "Handle asynchronous operation"
    
    return None

def add_comments_rule_based(code_text, language='python'):
    """Generate intelligent, contextual comments for multiple languages."""
    lines = code_text.split('\n')
    commented_lines = []
    
    for line in lines:
        stripped = line.strip()
        indent = " " * (len(line) - len(line.lstrip()))
        
        # Add the original line first
        commented_lines.append(line)
        
        # Skip empty lines and existing comments
        existing_comment_styles = ['#', '//', '/*', '*', '--', '%', ';']
        if not stripped or any(stripped.startswith(style) for style in existing_comment_styles):
            continue
        
        # Generate meaningful comment
        comment = get_meaningful_comment(line, language)
        if comment:
            # Use appropriate comment style for each language
            if language in ['python', 'ruby', 'bash', 'r', 'perl']:
                commented_lines.append(f'{indent}# {comment}')
            elif language in ['javascript', 'typescript', 'java', 'cpp', 'c', 'csharp', 'go', 'rust', 'swift', 'kotlin', 'scala', 'php']:
                commented_lines.append(f'{indent}// {comment}')
            elif language == 'sql':
                commented_lines.append(f'{indent}-- {comment}')
            elif language == 'lua':
                commented_lines.append(f'{indent}-- {comment}')
            elif language == 'html':
                commented_lines.append(f'{indent}<!-- {comment} -->')
            elif language == 'css':
                commented_lines.append(f'{indent}/* {comment} */')
            else:
                # Default to // for unknown languages
                commented_lines.append(f'{indent}// {comment}')
    
    return '\n'.join(commented_lines)

def main():
    # Header
    st.markdown("""
    # 🤖 AI Code Commenter
    ### Add intelligent comments to your code
    """)
    
    # Two column layout
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.header("📝 Input")
        
        # Just the input field
        code_input = st.text_area(
            "Paste your code here:",
            height=500,
            placeholder="def hello_world():\n    print('Hello, World!')"
        )
    
    with col2:
        st.header("✨ Output")
        
        if code_input.strip():
            # Auto-detect language
            detected_language = detect_language_simple(code_input)
            
            # Show detected language
            st.info(f"🔍 **Detected Language:** {detected_language.upper()}")
            
            # Process button
            if st.button("🚀 Add Comments", type="primary"):
                with st.spinner(f"Adding {detected_language} comments..."):
                    try:
                        # Add comments using rule-based approach
                        commented_code = add_comments_rule_based(code_input, detected_language)
                        
                        # Show commented code
                        st.code(commented_code, language=detected_language)
                        
                        # Stats
                        original_lines = len(code_input.split('\n'))
                        commented_lines = len(commented_code.split('\n'))
                        added_comments = commented_lines - original_lines
                        
                        # Show stats and download in columns
                        col_a, col_b = st.columns([2, 1])
                        with col_a:
                            st.success(f"✅ Added **{added_comments}** helpful comments!")
                        with col_b:
                            # Get appropriate file extension
                            ext_map = {
                                'python': 'py', 'javascript': 'js', 'typescript': 'ts',
                                'java': 'java', 'cpp': 'cpp', 'c': 'c', 'csharp': 'cs',
                                'go': 'go', 'rust': 'rs', 'php': 'php', 'ruby': 'rb'
                            }
                            ext = ext_map.get(detected_language, 'txt')
                            
                            st.download_button(
                                label="📥 Download",
                                data=commented_code,
                                file_name=f"commented_code.{ext}",
                                mime="text/plain"
                            )
                        
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")
        
        else:
            st.info("👈 Please enter code to add comments")

if __name__ == "__main__":
    main()