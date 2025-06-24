import re
import sys
import os
import argparse
from pathlib import Path


class MarkdownToHtmlConverter:
    def __init__(self):
        self.html_template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }}
        h1, h2, h3, h4, h5, h6 {{
            margin-top: 1.5em;
            margin-bottom: 0.5em;
            color: #2c3e50;
        }}
        h1 {{ border-bottom: 2px solid #eee; padding-bottom: 10px; }}
        h2 {{ border-bottom: 1px solid #eee; padding-bottom: 5px; }}
        code {{
            background-color: #f4f4f4;
            padding: 2px 4px;
            border-radius: 3px;
            font-family: 'Courier New', monospace;
        }}
        pre {{
            background-color: #f8f8f8;
            border: 1px solid #ddd;
            border-radius: 5px;
            padding: 15px;
            overflow-x: auto;
        }}
        pre code {{
            background-color: transparent;
            padding: 0;
        }}
        blockquote {{
            border-left: 4px solid #ddd;
            margin: 0;
            padding-left: 20px;
            color: #666;
        }}
        ul, ol {{ padding-left: 20px; }}
        li {{ margin-bottom: 5px; }}
        a {{ color: #3498db; text-decoration: none; }}
        a:hover {{ text-decoration: underline; }}
        table {{
            border-collapse: collapse;
            width: 100%;
            margin: 20px 0;
        }}
        th, td {{
            border: 1px solid #ddd;
            padding: 12px;
            text-align: left;
        }}
        th {{ background-color: #f2f2f2; }}
        hr {{
            border: none;
            height: 1px;
            background-color: #ddd;
            margin: 20px 0;
        }}
    </style>
</head>
<body>
{content}
</body>
</html>"""

    def convert_headers(self, text):
        """Convert Markdown headers to HTML"""
        lines = text.split('\n')
        result = []
        
        for line in lines:
            # Handle ATX headers (# ## ### etc.)
            header_match = re.match(r'^(#{1,6})\s+(.+)', line)
            if header_match:
                level = len(header_match.group(1))
                content = header_match.group(2).strip()
                result.append(f'<h{level}>{content}</h{level}>')
            else:
                result.append(line)
        
        return '\n'.join(result)

    def convert_emphasis(self, text):
        """Convert bold, italic, and strikethrough"""
        # Bold (**text** or __text__)
        text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
        text = re.sub(r'__(.+?)__', r'<strong>\1</strong>', text)
        
        # Italic (*text* or _text_)
        text = re.sub(r'\*([^*]+?)\*', r'<em>\1</em>', text)
        text = re.sub(r'_([^_]+?)_', r'<em>\1</em>', text)
        
        # Strikethrough (~~text~~)
        text = re.sub(r'~~(.+?)~~', r'<del>\1</del>', text)
        
        return text

    def convert_links(self, text):
        """Convert Markdown links to HTML"""
        # [text](url)
        text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', text)
        
        # Auto-links <url>
        text = re.sub(r'<(https?://[^>]+)>', r'<a href="\1">\1</a>', text)
        
        return text

    def convert_inline_code(self, text):
        """Convert inline code"""
        # Inline code `code`
        text = re.sub(r'`([^`]+)`', r'<code>\1</code>', text)
        return text

    def convert_code_blocks(self, text):
        """Convert code blocks"""
        # Fenced code blocks ```
        text = re.sub(r'```(\w+)?\n(.*?)\n```', r'<pre><code>\2</code></pre>', text, flags=re.DOTALL)
        
        # Indented code blocks (4 spaces or 1 tab)
        lines = text.split('\n')
        result = []
        in_code_block = False
        code_content = []
        
        for line in lines:
            if line.startswith('    ') or line.startswith('\t'):
                if not in_code_block:
                    in_code_block = True
                    code_content = []
                code_content.append(line[4:] if line.startswith('    ') else line[1:])
            else:
                if in_code_block:
                    result.append('<pre><code>' + '\n'.join(code_content) + '</code></pre>')
                    in_code_block = False
                    code_content = []
                result.append(line)
        
        # Handle remaining code block
        if in_code_block:
            result.append('<pre><code>' + '\n'.join(code_content) + '</code></pre>')
        
        return '\n'.join(result)

    def convert_lists(self, text):
        """Convert unordered and ordered lists"""
        lines = text.split('\n')
        result = []
        in_ul = False
        in_ol = False
        
        for line in lines:
            stripped = line.strip()
            
            # Unordered list
            if re.match(r'^[-*+]\s+', stripped):
                if not in_ul:
                    if in_ol:
                        result.append('</ol>')
                        in_ol = False
                    result.append('<ul>')
                    in_ul = True
                content = re.sub(r'^[-*+]\s+', '', stripped)
                result.append(f'<li>{content}</li>')
            
            # Ordered list
            elif re.match(r'^\d+\.\s+', stripped):
                if not in_ol:
                    if in_ul:
                        result.append('</ul>')
                        in_ul = False
                    result.append('<ol>')
                    in_ol = True
                content = re.sub(r'^\d+\.\s+', '', stripped)
                result.append(f'<li>{content}</li>')
            
            # Regular line
            else:
                if in_ul:
                    result.append('</ul>')
                    in_ul = False
                if in_ol:
                    result.append('</ol>')
                    in_ol = False
                result.append(line)
        
        # Close any remaining lists
        if in_ul:
            result.append('</ul>')
        if in_ol:
            result.append('</ol>')
        
        return '\n'.join(result)

    def convert_blockquotes(self, text):
        """Convert blockquotes"""
        lines = text.split('\n')
        result = []
        in_blockquote = False
        quote_content = []
        
        for line in lines:
            if line.startswith('> '):
                if not in_blockquote:
                    in_blockquote = True
                    quote_content = []
                quote_content.append(line[2:])
            else:
                if in_blockquote:
                    result.append('<blockquote>' + '\n'.join(quote_content) + '</blockquote>')
                    in_blockquote = False
                    quote_content = []
                result.append(line)
        
        # Handle remaining blockquote
        if in_blockquote:
            result.append('<blockquote>' + '\n'.join(quote_content) + '</blockquote>')
        
        return '\n'.join(result)

    def convert_horizontal_rules(self, text):
        """Convert horizontal rules"""
        text = re.sub(r'^---+$', '<hr>', text, flags=re.MULTILINE)
        text = re.sub(r'^\*\*\*+$', '<hr>', text, flags=re.MULTILINE)
        return text

    def convert_line_breaks(self, text):
        """Convert line breaks and paragraphs"""
        # Split into blocks
        blocks = re.split(r'\n\s*\n', text)
        result = []
        
        for block in blocks:
            block = block.strip()
            if not block:
                continue
            
            # Skip if it's already an HTML block element
            if re.match(r'^<(h[1-6]|p|div|ul|ol|blockquote|pre|hr|table)', block):
                result.append(block)
            else:
                # Convert single line breaks to <br> within paragraphs
                block = re.sub(r'\n(?!\s*\n)', '<br>\n', block)
                result.append(f'<p>{block}</p>')
        
        return '\n\n'.join(result)

    def convert_markdown_to_html(self, markdown_text):
        """Convert Markdown text to HTML"""
        html = markdown_text
        
        # Apply conversions in order
        html = self.convert_code_blocks(html)  # Do this first to protect code content
        html = self.convert_headers(html)
        html = self.convert_horizontal_rules(html)
        html = self.convert_blockquotes(html)
        html = self.convert_lists(html)
        html = self.convert_emphasis(html)
        html = self.convert_links(html)
        html = self.convert_inline_code(html)
        html = self.convert_line_breaks(html)
        
        return html

    def convert_file(self, input_file, output_file=None):
        """Convert a Markdown file to HTML"""
        input_path = Path(input_file)
        
        if not input_path.exists():
            raise FileNotFoundError(f"Input file '{input_file}' not found")
        
        if not input_path.suffix.lower() == '.md':
            print(f"Warning: Input file '{input_file}' doesn't have .md extension")
        
        # Read the Markdown file
        try:
            with open(input_path, 'r', encoding='utf-8') as f:
                markdown_content = f.read()
        except UnicodeDecodeError:
            with open(input_path, 'r', encoding='latin1') as f:
                markdown_content = f.read()
        
        # Convert to HTML
        html_content = self.convert_markdown_to_html(markdown_content)
        
        # Generate title from filename
        title = input_path.stem.replace('-', ' ').replace('_', ' ').title()
        
        # Create complete HTML document
        full_html = self.html_template.format(title=title, content=html_content)
        
        # Determine output file
        if output_file is None:
            output_file = input_path.with_suffix('.html')
        
        # Write HTML file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(full_html)
        
        return output_file


def main():
    parser = argparse.ArgumentParser(
        description='Convert Markdown files to HTML',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s README.md                    # Convert README.md to README.html
  %(prog)s docs.md -o output.html       # Convert docs.md to output.html
  %(prog)s *.md                         # Convert all .md files in current directory
        """
    )
    
    parser.add_argument('input_files', nargs='+', help='Markdown file(s) to convert')
    parser.add_argument('-o', '--output', help='Output HTML file (only for single input)')
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose output')
    
    args = parser.parse_args()
    
    converter = MarkdownToHtmlConverter()
    
    # Handle multiple files
    if len(args.input_files) > 1:
        if args.output:
            print("Error: Cannot specify output file when processing multiple inputs")
            sys.exit(1)
        
        for input_file in args.input_files:
            try:
                output_file = converter.convert_file(input_file)
                if args.verbose:
                    print(f"Converted: {input_file} -> {output_file}")
            except Exception as e:
                print(f"Error converting {input_file}: {e}")
    
    # Handle single file
    else:
        input_file = args.input_files[0]
        try:
            output_file = converter.convert_file(input_file, args.output)
            if args.verbose:
                print(f"Converted: {input_file} -> {output_file}")
            else:
                print(f"Successfully converted to {output_file}")
        except Exception as e:
            print(f"Error: {e}")
            sys.exit(1)


if __name__ == '__main__':
    main()