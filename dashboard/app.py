from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)
DB_FILE = "foreseen_vault.json"

def load_data():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            try:
                return json.load(f)
            except:
                pass
    return [{"metrics": {"cash": 0, "burn_rate": 0}}]

@app.route("/")
def index():
    data = load_data()
    return render_template("index.html", current=data[0])

@app.route("/update", methods=["GET", "POST"])
def update_metrics():
    data = load_data()
    if request.method == "POST":
        data[0]["metrics"]["cash"] = float(request.form.get("cash", 0))
        data[0]["metrics"]["burn_rate"] = float(request.form.get("burn_rate", 0))
        with open(DB_FILE, "w") as f:
            json.dump(data, f)
        return redirect(url_for("index"))
    return render_template("update.html", data=data[0])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
