import markdown2
import os

TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Agentic Framework</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/github.min.css">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --primary-color: #2563eb;
            --sidebar-width: 280px;
            --header-height: 60px;
            --bg-color: #ffffff;
            --text-color: #1f2937;
            --sidebar-bg: #f8fafc;
            --border-color: #e2e8f0;
        }

        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            margin: 0;
            padding: 0;
            color: var(--text-color);
            background-color: var(--bg-color);
            display: flex;
            min-height: 100vh;
        }

        /* Sidebar */
        .sidebar {
            width: var(--sidebar-width);
            background-color: var(--sidebar-bg);
            border-right: 1px solid var(--border-color);
            position: fixed;
            height: 100vh;
            overflow-y: auto;
            top: 0;
            left: 0;
            display: flex;
            flex-direction: column;
            z-index: 100;
        }

        .sidebar-header {
            height: var(--header-height);
            display: flex;
            align-items: center;
            padding: 0 1.5rem;
            border-bottom: 1px solid var(--border-color);
            font-weight: 700;
            font-size: 1.1rem;
            color: #0f172a;
            text-decoration: none;
        }

        .sidebar-nav {
            padding: 1.5rem;
            display: flex;
            flex-direction: column;
            gap: 0.5rem;
        }

        .nav-link {
            display: block;
            padding: 0.5rem 0.75rem;
            color: #475569;
            text-decoration: none;
            border-radius: 0.375rem;
            font-size: 0.95rem;
            font-weight: 500;
            transition: all 0.2s;
        }

        .nav-link:hover, .nav-link.active {
            background-color: #e0e7ff;
            color: var(--primary-color);
        }

        /* Main Content */
        .main-content {
            margin-left: var(--sidebar-width);
            flex: 1;
            padding: 2rem 4rem;
            max-width: 900px;
        }

        /* Markdown Styles */
        h1, h2, h3, h4, h5, h6 {
            color: #0f172a;
            margin-top: 2rem;
            margin-bottom: 1rem;
            line-height: 1.3;
        }

        h1 { font-size: 2.25rem; margin-top: 0; border-bottom: 1px solid var(--border-color); padding-bottom: 0.5rem; }
        h2 { font-size: 1.75rem; border-bottom: 1px solid var(--border-color); padding-bottom: 0.3rem; }
        h3 { font-size: 1.5rem; }

        p { line-height: 1.7; margin-bottom: 1.2rem; color: #334155; }
        
        a { color: var(--primary-color); text-decoration: none; }
        a:hover { text-decoration: underline; }

        code {
            background-color: #f1f5f9;
            padding: 0.2rem 0.4rem;
            border-radius: 0.25rem;
            font-family: 'Menlo', 'Monaco', 'Courier New', monospace;
            font-size: 0.9em;
            color: #0f172a;
        }

        pre {
            background-color: #f8fafc;
            padding: 1rem;
            border-radius: 0.5rem;
            overflow-x: auto;
            border: 1px solid var(--border-color);
            margin-bottom: 1.5rem;
        }

        pre code {
            background-color: transparent;
            padding: 0;
            color: inherit;
            font-size: 0.9rem;
        }

        blockquote {
            border-left: 4px solid var(--primary-color);
            margin: 1.5rem 0;
            padding-left: 1rem;
            color: #475569;
            background-color: #f8fafc;
            padding: 1rem;
            border-radius: 0 0.5rem 0.5rem 0;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            margin: 1.5rem 0;
        }

        th, td {
            border: 1px solid var(--border-color);
            padding: 0.75rem;
            text-align: left;
        }

        th {
            background-color: #f8fafc;
            font-weight: 600;
        }

        /* Mobile Responsive */
        @media (max-width: 768px) {
            .sidebar {
                transform: translateX(-100%);
                transition: transform 0.3s ease;
            }
            
            .sidebar.open {
                transform: translateX(0);
            }

            .main-content {
                margin-left: 0;
                padding: 1.5rem;
            }

            .mobile-header {
                display: flex;
                align-items: center;
                padding: 1rem;
                background-color: var(--bg-color);
                border-bottom: 1px solid var(--border-color);
                position: sticky;
                top: 0;
                z-index: 90;
            }

            .menu-toggle {
                background: none;
                border: none;
                font-size: 1.5rem;
                cursor: pointer;
                margin-right: 1rem;
            }
        }
        
        @media (min-width: 769px) {
            .mobile-header {
                display: none;
            }
        }
    </style>
</head>
<body>
    <!-- Mobile Header -->
    <div class="mobile-header">
        <button class="menu-toggle" onclick="document.querySelector('.sidebar').classList.toggle('open')">☰</button>
        <div style="font-weight: 700;">AI Agentic Framework</div>
    </div>

    <!-- Sidebar -->
    <aside class="sidebar">
        <a href="index.html" class="sidebar-header">
            🤖 AI Agentic Framework
        </a>
        <nav class="sidebar-nav">
            <a href="index.html" class="nav-link {active_home}">Home</a>
            <a href="api/index.html" class="nav-link {active_api}">API Reference</a>
            <a href="publishing.html" class="nav-link {active_pub}">Publishing Guide</a>
        </nav>
    </aside>

    <!-- Main Content -->
    <main class="main-content">
        {content}
    </main>

    <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js"></script>
    <script>hljs.highlightAll();</script>
    
    <script type="module">
        import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
        mermaid.initialize({ startOnLoad: true });
    </script>
</body>
</html>
"""

def convert_file(input_path, output_path, page_type="home"):
    with open(input_path, "r") as f:
        md_content = f.read()
    
    # Convert markdown to HTML with extras
    html_content = markdown2.markdown(
        md_content,
        extras=["fenced-code-blocks", "tables", "mermaid", "header-ids"]
    )
    
    # Determine active link
    active_home = "active" if page_type == "home" else ""
    active_api = "active" if page_type == "api" else ""
    active_pub = "active" if page_type == "publishing" else ""
    
    # Render template
    final_html = TEMPLATE.replace("{content}", html_content)
    final_html = final_html.replace("{active_home}", active_home)
    final_html = final_html.replace("{active_api}", active_api)
    final_html = final_html.replace("{active_pub}", active_pub)
    
    with open(output_path, "w") as f:
        f.write(final_html)
    print(f"Generated {output_path}")

if __name__ == "__main__":
    # Ensure docs directory exists
    if not os.path.exists("docs"):
        os.makedirs("docs")
        
    convert_file("docs/index.md", "docs/index.html", "home")
    convert_file("docs/publishing.md", "docs/publishing.html", "publishing")
