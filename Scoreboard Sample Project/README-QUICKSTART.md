# Scoreboard Sample Project — Quick Start

## 1) Open in VS Code
- Extract this folder somewhere simple like `C:\Dev\scoreboard` or `~/Dev/scoreboard`.
- In VS Code: **File → Open Folder…** and select `Scoreboard Sample Project`.

## 2) Create & activate a virtual environment
**Windows (PowerShell):**
```
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```
**macOS/Linux (bash/zsh):**
```
python3 -m venv .venv
source .venv/bin/activate
```

If activation is blocked on Windows, run this once in an **Administrator** PowerShell:
```
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

## 3) Install dependencies
```
pip install -r requirements.txt
```

## 4) Run the app
- Option A (Terminal):
```
python app.py
```
- Option B (VS Code Debug):
    - Press **F5** or choose **Run and Debug → Python: Flask (app.py)**

Then open http://127.0.0.1:5000/ in your browser.

## 5) Reset the database (optional)
Delete `scores.db` to start fresh. It will be recreated on next run.

## 6) Test adding a score
Use the form on the page, or from a terminal:
```
curl -X POST -d "name=Alice&score=123" http://127.0.0.1:5000/
```

## 7) Common gotchas
- If port 5000 is busy, change to a free port by editing the bottom of `app.py`:
```python
app.run(debug=True, port=5050)
```
- If you don’t see CSS, make sure the folder is named `static` and the file is `static/styles.css`.
- If VS Code prompts to **install Python** or **select interpreter**, pick the one from `.venv`.

## 8) Next steps for students
- Enforce top 10 scores only: change the SELECT query to order by score DESC and limit results.
- Add validation: prevent empty names or negative scores.
- Add REST endpoints: e.g., `/api/scores` to GET/POST JSON.
- Sort by highest score and show ranks.
