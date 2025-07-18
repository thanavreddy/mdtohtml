# Markdown to HTML Converter

A powerful command-line tool that converts Markdown files to clean, well-formatted HTML with built-in styling. Perfect for generating documentation, blog posts, or any content that needs to be converted from Markdown to HTML.

## Features

**Comprehensive Markdown Support**
- Headers (H1-H6)
- **Bold** and *italic* text formatting
- ~~Strikethrough~~ text
- `Inline code` and code blocks
- Unordered and ordered lists
- Links and auto-links
- Blockquotes
- Horizontal rules
- Tables and line breaks

🎨 **Professional Output**
- Clean, responsive HTML5 output
- Built-in CSS styling with modern typography
- Mobile-friendly responsive design
- Syntax highlighting for code blocks
- Print-friendly styles

 **Easy to Use**
- Simple command-line interface
- Batch processing for multiple files
- Customizable output file names
- Verbose mode for detailed feedback
- Error handling and encoding support

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/thanavreddy/mdtohtml.git
   cd mdtohtml
   ```

2. **Make the script executable (Unix/Linux/macOS):**
   ```bash
   chmod +x main.py
   ```

3. **No additional dependencies required!** The tool uses only Python standard library.

## Quick Start

**Convert a single file:**
```bash
python main.py README.md
```

This will create `README.html` in the same directory.

**Specify output file:**
```bash
python main.py document.md -o my_webpage.html
```

**Convert multiple files:**
```bash
python main.py *.md
```

## Usage

### Basic Syntax

```bash
python main.py [OPTIONS] INPUT_FILE [INPUT_FILE...]
```

### Options

| Option | Description |
|--------|-------------|
| `-o, --output` | Specify output HTML file (only for single input) |
| `-v, --verbose` | Enable verbose output with detailed conversion info |
| `-h, --help` | Show help message and exit |

### Examples

**Convert single file with custom output:**
```bash
python main.py docs/guide.md -o public/guide.html
```

**Convert all Markdown files in current directory:**
```bash
python main.py *.md -v
```

**Convert specific files:**
```bash
python main.py README.md CHANGELOG.md docs/API.md
```

## Supported Markdown Syntax

### Headers
```markdown
# H1 Header
## H2 Header
### H3 Header
#### H4 Header
##### H5 Header
###### H6 Header
```

### Text Formatting
```markdown
**Bold text** or __Bold text__
*Italic text* or _Italic text_
~~Strikethrough text~~
`Inline code`
```

### Links
```markdown
[Link text](https://example.com)
<https://example.com>
```

### Lists
```markdown
- Unordered list item
* Another item
+ Yet another item

1. Ordered list item
2. Second item
3. Third item
```

### Code Blocks
````markdown
```python
def hello_world():
    print("Hello, World!")
```

    # Indented code block
    echo "This is also code"
````

### Blockquotes
```markdown
> This is a blockquote
> It can span multiple lines
```

### Horizontal Rules
```markdown
---
***
```

## Output Features

The generated HTML includes:

- **Responsive Design**: Looks great on desktop, tablet, and mobile
- **Clean Typography**: Uses system fonts for optimal readability
- **Syntax Highlighting**: Code blocks are properly formatted
- **Professional Styling**: Modern, clean appearance
- **Semantic HTML**: Proper HTML5 structure for accessibility
- **Print Styles**: Optimized for printing



## Requirements

- Python 3.6 or higher

## Troubleshooting

**Common Issues:**

1. **File not found error:**
   - Make sure the input file exists and the path is correct
   - Check file permissions

2. **Encoding issues:**
   - The tool automatically handles UTF-8 and Latin1 encodings
   - For other encodings, convert your file to UTF-8 first

3. **Permission denied:**
   - Make sure you have write permissions in the output directory
   - On Unix systems, use `chmod +x main.py`

**Getting Help:**

```bash
python main.py --help
```
