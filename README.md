# 🤖 AI Code Commenter - Simple Edition

**Instantly add intelligent comments to your code in 20+ programming languages!**

## 🚀 Quick Start

### 1️⃣ Install Dependencies
```bash
pip install -r requirements_streamlit.txt
```

### 2️⃣ Run the App
```bash
streamlit run app_simple.py --server.port 8502
```

### 3️⃣ Open Browser
```
http://localhost:8502
```

## ✨ Features

- **🌐 Multi-Language Support**: Python, JavaScript, Java, C++, Go, Rust, PHP, Ruby, Swift, Kotlin, SQL, HTML, CSS and more!
- **🧠 Smart Comments**: Contextual, meaningful comments that actually help
- **🔍 Auto-Detection**: Automatically detects programming language
- **📱 Simple UI**: Clean, easy-to-use Streamlit interface
- **📥 Download Results**: Get commented code with proper file extensions
- **⚡ Fast & Local**: No API keys needed, runs completely offline

## 📝 Example

**Input (Python):**
```python
def calculate_tax(income, rate):
    if income > 50000:
        return income * rate * 1.1
    return income * rate
```

**Output:**
```python
def calculate_tax(income, rate):
# Define calculate tax function
    if income > 50000:
    # Check condition
        return income * rate * 1.1
        # Return result
    return income * rate
    # Return result
```

## 🌟 Supported Languages

| Language | Extension | Comment Style |
|----------|-----------|---------------|
| Python | `.py` | `#` |
| JavaScript | `.js` | `//` |
| TypeScript | `.ts` | `//` |
| Java | `.java` | `//` |
| C/C++ | `.c/.cpp` | `//` |
| C# | `.cs` | `//` |
| Go | `.go` | `//` |
| Rust | `.rs` | `//` |
| PHP | `.php` | `//` |
| Ruby | `.rb` | `#` |
| Swift | `.swift` | `//` |
| Kotlin | `.kt` | `//` |
| SQL | `.sql` | `--` |
| HTML | `.html` | `<!-- -->` |
| CSS | `.css` | `/* */` |
| And more! | | |

## 📁 Project Structure

```
📦 AI Code Commenter/
├── 🚀 app_simple.py              # Main Streamlit app
├── 📋 requirements_streamlit.txt # Dependencies
├── 📖 README.md                  # This file
├── 🧹 cleanup.py                 # Cleanup script
├── 🔧 .zencoder/                 # AI assistant config
└── 🚫 .gitignore                 # Git ignore rules
```

## 🧹 Maintenance

**Clean temporary files:**
```bash
python cleanup.py
```

## 🎯 Why This Version?

This is the **streamlined version** focusing on:
- ✅ **Simplicity** - One file, one purpose
- ✅ **Speed** - Fast and responsive
- ✅ **Reliability** - No complex dependencies
- ✅ **Universal** - Works with all languages

This focused version contains only the essential files for maximum simplicity.

---

**🌟 Ready to make your code more readable? Run the app and start commenting!**