from flask import Flask, render_template, request, redirect
import json
import os
from datetime import datetime
from datetime import timedelta
import calendar


def generate_calendar(year, month, log_dates, memos):
    cal = calendar.Calendar(firstweekday=6)
    month_days = cal.itermonthdays(year, month)
    today_strs = [datetime.strptime(d, "%Y-%m-%d").strftime("%Y-%m-%d") for d in log_dates]

    weeks = []
    week = []

    for day in month_days:
        if day == 0:
            week.append({"day": "", "done": False, "has_memo": False})
        else:
            date_str = f"{year}-{month:02d}-{day:02d}"
            week.append({
                "day": day, 
                "done": date_str in today_strs,
                "has_memo": date_str in memos
                })
        if len(week) == 7:
            weeks.append(week)
            week = []
    if week:
        while len(week) < 7:
            week.append({"day": "", "done": False, "has_memo": False})
        weeks.append(week)
    return weeks

app = Flask(__name__)
DATA_FILE = "data.json"
def today_str():
    return datetime.now().strftime("%Y-%m-%d")
def get_streak(log):
    today = datetime.now().date()
    log_dates = sorted([datetime.strptime(d, "%Y-%m-%d").date() for d in log], reverse=True)

    streak = 0
    for i, date in enumerate(log_dates):
        if date == today - timedelta(days=i):
            streak += 1
        else:
            break
    return streak

def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return{"habit": "", "log": [], "memos": {}}
    return {"habit": "", "log": [], "memos":{}}

def save_data(data):
    with open(DATA_FILE,"w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        
@app.route("/", methods=["GET", "POST"])
def index():
    year = int(request.args.get("year", datetime.now().year))
    month = int(request.args.get("month", datetime.now().month))
    selected_date = request.args.get("selected_date")
    
    data = load_data()
    already_done = False
    selected_memo = None
    
    if request.method == "POST":
        if "habit" in request.form:
            data["habit"] = request.form["habit"]
            data["log"] = []
            save_data(data)
            return redirect(f"/?year={year}&month={month}")
        
        elif "done" in request.form:
            today = today_str()
            already_done = today in data["log"]
            
            if not already_done:
                data["log"].append(today)
                data["log"] = sorted(list(set(data["log"])))
                save_data(data)
                return redirect(f"/?year={year}&month={month}&celebrate=1")
            else:
                return redirect(f"/?year={year}&month={month}")
        elif "memo" in request.form:
            today = today_str()
            memo = request.form.get("memo_text", "").strip()
            data.setdefault("memos", {})[today] = memo
            save_data(data)
            return redirect(f"/?year={year}&month={month}")
        
    if selected_date and selected_date in data.get("memos", {}):
        selected_memo = data["memos"][selected_date]
    now = datetime.now()
    calendar_weeks =generate_calendar(year, month, data["log"], data.get("memos", {}))
    streak = get_streak(data["log"])
    
    month_days = list(calendar.Calendar(firstweekday=6).itermonthdays(year, month))
    total_days = sum(1 for day in month_days if day != 0)

    month_str = f"{year}-{month:02d}"
    monthly_done = [d for d in data["log"] if d.startswith(month_str)]

    achievement_rate = round((len(monthly_done) / total_days) * 100, 1) if total_days else 0

    return render_template(
        "index.html", 
        data=data, 
        calendar_weeks=calendar_weeks, 
        streak=streak, 
        year=year, 
        month=month,
        achievement_rate=achievement_rate,
        celebrate=bool(request.args.get("celebrate") == "1"),
        already_done=already_done,
        today_str=today_str(),
        selected_date=selected_date,
        selected_memo=selected_memo
    )

if __name__== "__main__":
    app.run(debug=True, host="0.0.0.0", port=5003)