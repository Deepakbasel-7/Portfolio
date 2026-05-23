"""
Personal Portfolio — Python (zero dependencies)
Structure:
  portfolio.py              ← this file (server + your data)
  templates/index.html      ← HTML structure
  static/style.css          ← all styles
  static/script.js          ← animations & form

Run:   python3 portfolio.py
Open:  http://localhost:8080
"""

import http.server
import threading
import webbrowser
import time
import os

# ─────────────────────────────────────────────
#  EDIT YOUR INFO HERE
# ─────────────────────────────────────────────
NAME     = "DEEPAK BASHYAL"
ROLE     = "Software Developer"
TAGLINE  = "I build scalable systems, elegant APIs, and interfaces that make complex things feel simple."
ABOUT    = (
    "I'm a software developer with a passion for building things that live on the internet. "
    "I care deeply about clean code, thoughtful architecture, and user experiences that just work. "
    "Currently open to full-time roles and freelance projects — let's build something great together."
)
STATS    = [
    ("3+", "Years of Experience"),
    ("7+", "Projects Shipped"),
    ("6+", "Technologies"),
    ("100+",   "Bugs Fixed"),
]
EMAIL    = "kingofpirates952@gmail.com"
GITHUB   = "https://github.com/Deepakbasel-7"
LINKEDIN = "https://www.linkedin.com/in/deepak-basel-8a27b5243"

SKILLS = [
    ("Languages",    ["Python", "JavaScript", "php", "SQL"]),
    ("Frontend",     ["Next.js", "HTML/CSS", "Bootstrap", "blade"]),
    ("Backend",      ["Node.js", "Express", "REST","Flask"]),
    ("Data & Cloud", ["Sequelize", "Docker", "MySQL Server"]),
    ("Tools",        ["Git", "Jupyter", "Linux", "Agile", "Postman"]),
]

PROJECTS = [
    {
        "icon": "🤖",
        "title": "Salary Prediction Model",
        "desc": "A salary prediction program using machine learning algorithms. Analyzes job title, location, experience, and education to predict salary ranges for different roles.",
        "stack": ["Python", "SQL", "numpy", "pandas", "scikit-learn", "matplotlib"],
        "github": "https://github.com/Deepakbasel-7/Salary_predicting_model.git",
        "live": "",
    },
    {
        "icon": "🧬",
        "title": "Covid Classification Model",
        "desc": "A machine learning model for classifying Covid-19 cases based on medical imaging data.",
        "stack": ["Python", "SQL", "numpy", "pandas", "scikit-learn", "matplotlib"],
        "github": "https://github.com/Deepakbasel-7/Covid-Classification-Model.git",
        "live": "",
    },
    {
        "icon": "📊",
        "title": "Pizza Sales Analysis (SQL)",
        "desc": "SQL-based project to gain insights into pizza sales — querying a database to analyze trends, customer behavior, and product performance.",
        "stack": ["SQL", "Data Analysis", "MySQL Server"],
        "github": "https://github.com/Deepakbasel-7/Pizza-Sales-Analysis-with-SQL.git",
        "live": "",
    },

     {
        "icon": "🐶",
        "title": "Dog Care Portal",
        "desc": "It is dog care portal developed by using laravel and mysql. It provides a platform for dog owners to access information, resources, and services related to dog care. The portal includes features such as dog care tips, training guides, health advice, and a directory of local veterinarians and pet services.",
        "stack": ["SQL", "php", "blade"],
        "github": "https://github.com/Deepakbasel-7/Dog-care-portal.git",
        "live": "",
    },
]

PORT = 8080
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# ─────────────────────────────────────────────


def render_html():
    """Read index.html and substitute all {{PLACEHOLDERS}}."""

    # Build HTML snippets
    stats_html = "".join(
        f'<div class="stat-card">'
        f'<div class="stat-num">{n}</div>'
        f'<div class="stat-lbl">{l}</div>'
        f'</div>'
        for n, l in STATS
    )

    skills_html = "".join(
        f'<div class="skill-group">'
        f'<div class="skill-title">{cat}</div>'
        f'<div class="skill-tags">'
        + "".join(f'<span class="tag">{t}</span>' for t in tags)
        + '</div></div>'
        for cat, tags in SKILLS
    )

    projects_html = "".join(
        '<div class="card">'
        '<div class="card-top">'
        f'<span class="card-icon">{p["icon"]}</span>'
        '<div class="card-links">'
        f'<a href="{p["github"]}" target="_blank">GitHub ↗</a>'
        + (f'<a href="{p["live"]}" target="_blank">Live ↗</a>' if p["live"] else '')
        + '</div></div>'
        f'<div class="card-title">{p["title"]}</div>'
        f'<p class="card-desc">{p["desc"]}</p>'
        '<div class="card-stack">'
        + "".join(f'<span class="stack-tag">{s}</span>' for s in p["stack"])
        + '</div></div>'
        for p in PROJECTS
    )

    first = NAME.split()[0]
    last  = NAME.split()[-1] if len(NAME.split()) > 1 else ""

    # Read the template
    template_path = os.path.join(BASE_DIR, "templates", "index.html")
    with open(template_path, encoding="utf-8") as f:
        html = f.read()

    # Replace all placeholders
    replacements = {
        "{{NAME}}":          NAME,
        "{{FIRST}}":         first,
        "{{LAST}}":          last,
        "{{ROLE}}":          ROLE,
        "{{TAGLINE}}":       TAGLINE,
        "{{ABOUT}}":         ABOUT,
        "{{EMAIL}}":         EMAIL,
        "{{GITHUB}}":        GITHUB,
        "{{GITHUB_SHORT}}":  GITHUB.replace("https://", ""),
        "{{LINKEDIN}}":      LINKEDIN,
        "{{LINKEDIN_SHORT}}": LINKEDIN.replace("https://", ""),
        "{{STATS_HTML}}":    stats_html,
        "{{SKILLS_HTML}}":   skills_html,
        "{{PROJECTS_HTML}}": projects_html,
    }
    for key, val in replacements.items():
        html = html.replace(key, val)

    return html


class Handler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):
        # Serve static files
        if self.path.startswith("/static/"):
            file_path = os.path.join(BASE_DIR, self.path.lstrip("/"))
            if os.path.isfile(file_path):
                ext = os.path.splitext(file_path)[1]
                content_type = {
                    ".css": "text/css",
                    ".js":  "application/javascript",
                }.get(ext, "text/plain")
                with open(file_path, "rb") as f:
                    data = f.read()
                self.send_response(200)
                self.send_header("Content-Type", content_type)
                self.send_header("Content-Length", str(len(data)))
                self.send_header("Cache-Control", "no-store")
                self.end_headers()
                self.wfile.write(data)
            else:
                self.send_error(404)
            return

        # Serve main page (re-reads template + data on every request)
        html = render_html().encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(html)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(html)

    def log_message(self, *_):
        pass  # silence request logs


def main():
    server = http.server.HTTPServer(("", PORT), Handler)
    url = f"http://localhost:{PORT}"
    print(f"\n  🚀  Portfolio running at  {url}")
    print(f"  ✏️   Edit portfolio.py to update your content.")
    print(f"  🎨  Edit static/style.css to change styles.")
    print(f"  ⚡  Edit static/script.js to change behaviour.")
    print(f"  ⌨️   Press Ctrl+C to stop.\n")

    def open_browser():
        time.sleep(0.6)
        webbrowser.open(url)

    threading.Thread(target=open_browser, daemon=True).start()

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n  👋  Server stopped.")


if __name__ == "__main__":
    main()