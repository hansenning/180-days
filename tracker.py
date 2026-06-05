import json
import sys
from datetime import date

LOG_FILE = "log.json"


def load():
    try:
        with open(LOG_FILE) as f:
            return json.load(f)
    except FileNotFoundError:
        return []


def save(data):
    with open(LOG_FILE, "w") as f:
        json.dump(data, f, indent=2)


def log(description, minutes):
    data = load()
    entry = {
        "date": str(date.today()),
        "description": description,
        "minutes": int(minutes),
    }
    data.append(entry)
    save(data)
    print(f"Logged: {entry['date']} — {description} ({minutes} min)")


def status():
    data = load()
    if not data:
        print("No entries yet.")
        return

    total_days = len(set(e["date"] for e in data))
    total_minutes = sum(e["minutes"] for e in data)

    # calculate current streak
    from datetime import timedelta
    dates = sorted(set(date.fromisoformat(e["date"]) for e in data), reverse=True)
    streak = 1
    for i in range(1, len(dates)):
        if dates[i - 1] - dates[i] == timedelta(days=1):
            streak += 1
        else:
            break

    print(f"Total days logged : {total_days}")
    print(f"Total minutes     : {total_minutes} ({total_minutes // 60}h {total_minutes % 60}m)")
    print(f"Current streak    : {streak} day(s)")
    print(f"Progress          : {total_days}/180 days")
    print()
    print("Last 5 entries:")
    for e in data[-5:]:
        print(f"  {e['date']}  {e['minutes']:>3}m  {e['description']}")


def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python tracker.py log \"what you did\" <minutes>")
        print("  python tracker.py status")
        return

    command = sys.argv[1]

    if command == "log":
        if len(sys.argv) < 4:
            print("Usage: python tracker.py log \"description\" <minutes>")
            return
        log(sys.argv[2], sys.argv[3])

    elif command == "status":
        status()

    else:
        print(f"Unknown command: {command}")


if __name__ == "__main__":
    main()
