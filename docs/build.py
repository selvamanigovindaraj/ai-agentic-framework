import markdown2
import os

TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Agentic Framework</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/github-markdown-css/5.2.0/github-markdown.min.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/github.min.css">
    <style>
        body {
            box-sizing: border-box;
            min-width: 200px;
            max-width: 980px;
            margin: 0 auto;
            padding: 45px;
        }
        @media (max-width: 767px) {
            body {
                padding: 15px;
            }
        }
        .markdown-body {
            box-sizing: border-box;
            min-width: 200px;
            max-width: 980px;
            margin: 0 auto;
            padding: 45px;
        }
        .nav {
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 1px solid #eaecef;
        }
        .nav a {
            margin-right: 15px;
            text-decoration: none;
            color: #0366d6;
            font-weight: bold;
        }
        .nav a:hover {
            text-decoration: underline;
        }
    </style>
</head>
<body>
    <div class="nav">
        <a href="index.html">Home</a>
        <a href="api/index.html">API Docs</a>
        <a href="publishing.html">Publishing Guide</a>
    </div>
    <article class="markdown-body">
        {content}
    </article>
    
    <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js"></script>
    <script>hljs.highlightAll();</script>
    
    <script type="module">
        import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
        mermaid.initialize({ startOnLoad: true });
    </script>
</body>
</html>
"""

def convert_file(input_path, output_path):
    with open(input_path, "r") as f:
        md_content = f.read()
    
    # Convert markdown to HTML with extras
    html_content = markdown2.markdown(
        md_content,
        extras=["fenced-code-blocks", "tables", "mermaid", "header-ids"]
    )
    
    # Render template
    final_html = TEMPLATE.format(content=html_content)
    
    with open(output_path, "w") as f:
        f.write(final_html)
    print(f"Generated {output_path}")

if __name__ == "__main__":
    # Ensure docs directory exists
    if not os.path.exists("docs"):
        os.makedirs("docs")
        
    convert_file("docs/index.md", "docs/index.html")
    convert_file("docs/publishing.md", "docs/publishing.html")
