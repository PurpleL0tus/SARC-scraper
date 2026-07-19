import subprocess
import threading
import sys
import os
from flask import Flask, Response, render_template, request, stream_with_context

app = Flask(__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

_process = None
_process_lock = threading.Lock()

COMMANDS = {
    "online_scraper":  [sys.executable, "scrapers/online_scraper.py"],
    "pdf_scraper":     [sys.executable, "scrapers/pdf_scraper.py"],
    "json_to_text":    [sys.executable, "processors/json_to_text.py"],
    "pdf_to_text":     [sys.executable, "processors/pdf_to_text.py"],
    "inventory":       [sys.executable, "inventory.py"],
}

EXTRACT_SCRIPTS = [
    "processors/extract_school.py",
    "processors/extract_facilities.py",
    "processors/extract_building_info.py",
]

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/status")
def status():
    with _process_lock:
        running = _process is not None and _process.poll() is None
    return {"running": running}


@app.route("/abort")
def abort():
    global _process
    with _process_lock:
        if _process is None or _process.poll() is not None:
            return {"aborted": False}
        _process.terminate()
    return {"aborted": True}


@app.route("/run")
def run():
    global _process

    cmd_key = request.args.get("cmd", "")
    year_id = request.args.get("year", "")
    proc_env = {**os.environ, "PYTHONUNBUFFERED": "1"}
    if year_id.isdigit():
        proc_env["YEAR_ID"] = year_id

    if cmd_key == "extract_all":
        cmds = [[sys.executable, s] for s in EXTRACT_SCRIPTS]
    elif cmd_key in COMMANDS:
        cmds = [COMMANDS[cmd_key]]
    else:
        return Response("Unknown command", status=400)

    with _process_lock:
        if _process is not None and _process.poll() is None:
            return Response("A script is already running.", status=409)
        _process = subprocess.Popen(
            cmds[0],
            cwd=BASE_DIR,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            env=proc_env,
        )

    def generate():
        for i, cmd in enumerate(cmds):
            if i == 0:
                proc = _process
            else:
                proc = subprocess.Popen(
                    cmd,
                    cwd=BASE_DIR,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    bufsize=1,
                    env=proc_env,
                )
            yield f"data: [running {cmd[-1]}]\n\n"
            for line in proc.stdout:
                yield f"data: {line.rstrip()}\n\n"
            proc.wait()
            yield f"data: [exited with code {proc.returncode}]\n\n"
        yield "data: __DONE__\n\n"

    return Response(
        stream_with_context(generate()),
        mimetype="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


if __name__ == "__main__":
    app.run(debug=True, threaded=True)
