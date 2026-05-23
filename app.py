"""
Portfolio Backend — Flask
Run:   pip install flask  →  python app.py
Site:  http://localhost:5000
Admin: http://localhost:5000/admin
"""

from flask import Flask, request, jsonify, render_template, redirect, url_for, flash
import sqlite3, json, os
from datetime import datetime

app = Flask(__name__)
app.secret_key = "deepak-portfolio-secret"

DB   = "portfolio.db"
BASE = os.path.dirname(os.path.abspath(__file__))


# ─── DATABASE ────────────────────────────────
def db():
    conn = sqlite3.connect(os.path.join(BASE, DB))
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with db() as c:
        c.executescript("""
        CREATE TABLE IF NOT EXISTS profile (
            key TEXT PRIMARY KEY, value TEXT
        );
        CREATE TABLE IF NOT EXISTS stats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            num TEXT NOT NULL, label TEXT NOT NULL, ord INTEGER DEFAULT 0
        );
        CREATE TABLE IF NOT EXISTS skills (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT NOT NULL, tags TEXT NOT NULL, ord INTEGER DEFAULT 0
        );
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            icon TEXT DEFAULT '📦', title TEXT NOT NULL,
            desc TEXT NOT NULL, stack TEXT NOT NULL,
            github TEXT DEFAULT '', live TEXT DEFAULT '', ord INTEGER DEFAULT 0
        );
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL, email TEXT NOT NULL, message TEXT NOT NULL,
            read INTEGER DEFAULT 0,
            created TEXT DEFAULT (datetime('now','localtime'))
        );
        CREATE TABLE IF NOT EXISTS visitors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ip TEXT, agent TEXT, path TEXT,
            created TEXT DEFAULT (datetime('now','localtime'))
        );
        """)

        # Seed only if empty
        if c.execute("SELECT COUNT(*) FROM profile").fetchone()[0] == 0:
            for k, v in {
                "name":     "DEEPAK BASHYAL",
                "role":     "Software Developer",
                "tagline":  "I build scalable systems, elegant APIs, and interfaces that make complex things feel simple.",
                "about":    "I'm a software developer with a passion for building things that live on the internet. I care deeply about clean code, thoughtful architecture, and user experiences that just work. Currently open to full-time roles and freelance projects — let's build something great together.",
                "email":    "kingofpirates952@gmail.com",
                "github":   "https://github.com/Deepakbasel-7",
                "linkedin": "https://www.linkedin.com/in/deepak-basel-8a27b5243",
            }.items():
                c.execute("INSERT OR IGNORE INTO profile VALUES (?,?)", (k, v))

            for i, (n, l) in enumerate([
                ("3+",   "Years of Experience"),
                ("7+",   "Projects Shipped"),
                ("6+",   "Technologies"),
                ("100+", "Bugs Fixed"),
            ]):
                c.execute("INSERT INTO stats (num,label,ord) VALUES (?,?,?)", (n, l, i))

            for i, (cat, tags) in enumerate([
                ("Languages",    ["Python", "JavaScript", "PHP", "SQL"]),
                ("Frontend",     ["Next.js", "HTML/CSS", "Bootstrap", "Blade"]),
                ("Backend",      ["Node.js", "Express", "REST", "Flask"]),
                ("Data & Cloud", ["Sequelize", "Docker", "MySQL Server"]),
                ("Tools",        ["Git", "Jupyter", "Linux", "Agile", "Postman"]),
            ]):
                c.execute("INSERT INTO skills (category,tags,ord) VALUES (?,?,?)",
                          (cat, json.dumps(tags), i))

            for i, (icon, title, desc, stack, github, live) in enumerate([
                ("🤖", "Salary Prediction Model",
                 "A salary prediction program using machine learning algorithms. Analyzes job title, location, experience, and education to predict salary ranges for different roles.",
                 "Python,SQL,numpy,pandas,scikit-learn,matplotlib",
                 "https://github.com/Deepakbasel-7/Salary_predicting_model.git", ""),
                ("🧬", "Covid Classification Model",
                 "A machine learning model for classifying Covid-19 cases based on medical imaging data.",
                 "Python,SQL,numpy,pandas,scikit-learn,matplotlib",
                 "https://github.com/Deepakbasel-7/Covid-Classification-Model.git", ""),
                ("📊", "Pizza Sales Analysis (SQL)",
                 "SQL-based project to gain insights into pizza sales — querying a database to analyze trends, customer behavior, and product performance.",
                 "SQL,Data Analysis,MySQL Server",
                 "https://github.com/Deepakbasel-7/Pizza-Sales-Analysis-with-SQL.git", ""),
                ("🐶", "Dog Care Portal",
                 "A dog care portal developed using Laravel and MySQL. Provides a platform for dog owners to access care tips, training guides, health advice, and a directory of local veterinarians and pet services.",
                 "PHP,SQL,Blade,Laravel,MySQL",
                 "https://github.com/Deepakbasel-7/Dog-care-portal.git", ""),
            ]):
                c.execute(
                    "INSERT INTO projects (icon,title,desc,stack,github,live,ord) VALUES (?,?,?,?,?,?,?)",
                    (icon, title, desc, stack, github, live, i)
                )

        c.commit()


def get_all():
    with db() as c:
        profile  = {r["key"]: r["value"] for r in c.execute("SELECT key,value FROM profile")}
        stats    = c.execute("SELECT * FROM stats ORDER BY ord").fetchall()
        skills   = c.execute("SELECT * FROM skills ORDER BY ord").fetchall()
        projects = c.execute("SELECT * FROM projects ORDER BY ord").fetchall()
    return profile, stats, skills, projects


# ─── VISITOR TRACKING ────────────────────────
@app.before_request
def track():
    if request.path.startswith(("/admin", "/static", "/api")):
        return
    ip    = request.headers.get("X-Forwarded-For", request.remote_addr)
    agent = request.headers.get("User-Agent", "")[:200]
    with db() as c:
        c.execute("INSERT INTO visitors (ip,agent,path) VALUES (?,?,?)",
                  (ip, agent, request.path))
        c.commit()


# ─── FRONTEND ────────────────────────────────
@app.route("/")
def index():
    profile, stats, skills, projects = get_all()
    parsed_skills   = [(s["category"], json.loads(s["tags"]), s["id"]) for s in skills]
    parsed_projects = []
    for p in projects:
        d = dict(p)
        d["stack_list"] = [t.strip() for t in d["stack"].split(",")]
        parsed_projects.append(d)
    return render_template("index.html",
        profile=profile, stats=stats,
        skills=parsed_skills, projects=parsed_projects)


# ─── CONTACT API ─────────────────────────────
@app.route("/api/contact", methods=["POST"])
def contact():
    data    = request.get_json() or {}
    name    = (data.get("name")    or "").strip()
    email   = (data.get("email")   or "").strip()
    message = (data.get("message") or "").strip()
    if not all([name, email, message]):
        return jsonify({"ok": False, "error": "All fields are required."}), 400
    with db() as c:
        c.execute("INSERT INTO messages (name,email,message) VALUES (?,?,?)",
                  (name, email, message))
        c.commit()
    return jsonify({"ok": True, "message": "Thanks! I'll get back to you soon."})


# ─── ADMIN ───────────────────────────────────
@app.route("/admin")
def admin():
    profile, stats, skills, projects = get_all()
    parsed_skills = [(s["category"], json.loads(s["tags"]), s["id"]) for s in skills]
    with db() as c:
        messages  = c.execute("SELECT * FROM messages ORDER BY created DESC").fetchall()
        unread    = c.execute("SELECT COUNT(*) FROM messages WHERE read=0").fetchone()[0]
        visitors  = c.execute("SELECT * FROM visitors ORDER BY created DESC LIMIT 100").fetchall()
        vis_total = c.execute("SELECT COUNT(*) FROM visitors").fetchone()[0]
        vis_today = c.execute("SELECT COUNT(*) FROM visitors WHERE date(created)=date('now','localtime')").fetchone()[0]
        unique_ip = c.execute("SELECT COUNT(DISTINCT ip) FROM visitors").fetchone()[0]
    return render_template("admin.html",
        profile=profile, stats=stats, skills=parsed_skills, projects=projects,
        messages=messages, unread=unread,
        visitors=visitors, vis_total=vis_total, vis_today=vis_today, unique_ips=unique_ip)


@app.route("/admin/save/profile", methods=["POST"])
def save_profile():
    with db() as c:
        for f in ["name","role","tagline","about","email","github","linkedin"]:
            c.execute("INSERT OR REPLACE INTO profile (key,value) VALUES (?,?)",
                      (f, request.form.get(f, "")))
        c.commit()
    flash("✅ Profile updated!", "success")
    return redirect(url_for("admin") + "#profile")


@app.route("/admin/save/stats", methods=["POST"])
def save_stats():
    with db() as c:
        c.execute("DELETE FROM stats")
        for i, (n, l) in enumerate(zip(request.form.getlist("num"), request.form.getlist("label"))):
            if n.strip() or l.strip():
                c.execute("INSERT INTO stats (num,label,ord) VALUES (?,?,?)", (n.strip(), l.strip(), i))
        c.commit()
    flash("✅ Stats updated!", "success")
    return redirect(url_for("admin") + "#stats")


@app.route("/admin/save/skills", methods=["POST"])
def save_skills():
    with db() as c:
        c.execute("DELETE FROM skills")
        for i, (cat, tags) in enumerate(zip(request.form.getlist("category"), request.form.getlist("tags"))):
            if cat.strip():
                tag_list = json.dumps([t.strip() for t in tags.split(",") if t.strip()])
                c.execute("INSERT INTO skills (category,tags,ord) VALUES (?,?,?)", (cat.strip(), tag_list, i))
        c.commit()
    flash("✅ Skills updated!", "success")
    return redirect(url_for("admin") + "#skills")


@app.route("/admin/save/project", methods=["POST"])
def save_project():
    pid   = request.form.get("id")
    icon  = request.form.get("icon", "📦").strip()
    title = request.form.get("title", "").strip()
    desc  = request.form.get("desc", "").strip()
    stack = request.form.get("stack", "").strip()
    github= request.form.get("github", "").strip()
    live  = request.form.get("live", "").strip()
    with db() as c:
        if pid:
            c.execute("UPDATE projects SET icon=?,title=?,desc=?,stack=?,github=?,live=? WHERE id=?",
                      (icon, title, desc, stack, github, live, pid))
        else:
            n = c.execute("SELECT COALESCE(MAX(ord),0)+1 FROM projects").fetchone()[0]
            c.execute("INSERT INTO projects (icon,title,desc,stack,github,live,ord) VALUES (?,?,?,?,?,?,?)",
                      (icon, title, desc, stack, github, live, n))
        c.commit()
    flash("✅ Project saved!", "success")
    return redirect(url_for("admin") + "#projects")


@app.route("/admin/delete/project/<int:pid>", methods=["POST"])
def delete_project(pid):
    with db() as c:
        c.execute("DELETE FROM projects WHERE id=?", (pid,))
        c.commit()
    flash("🗑 Project deleted.", "success")
    return redirect(url_for("admin") + "#projects")


@app.route("/admin/message/<int:mid>/read", methods=["POST"])
def mark_read(mid):
    with db() as c:
        c.execute("UPDATE messages SET read=1 WHERE id=?", (mid,))
        c.commit()
    return redirect(url_for("admin") + "#messages")


@app.route("/admin/message/<int:mid>/delete", methods=["POST"])
def delete_message(mid):
    with db() as c:
        c.execute("DELETE FROM messages WHERE id=?", (mid,))
        c.commit()
    flash("🗑 Message deleted.", "success")
    return redirect(url_for("admin") + "#messages")


# ─────────────────────────────────────────────
if __name__ == "__main__":
    init_db()
    print("\n  🚀  Portfolio  →  http://localhost:5000")
    print("  ⚙️   Admin      →  http://localhost:5000/admin\n")
    app.run(debug=True, port=5000)