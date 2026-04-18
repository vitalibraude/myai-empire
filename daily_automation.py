"""
Daily Automation Runner — Master scheduler that runs all automated tasks.
=========================================================================
Run this once daily (via Windows Task Scheduler or cron) to:
1. Send follow-up emails to prospects who haven't replied
2. Send drip course emails to subscribers
3. Send wave 2 outreach to new prospects (batch of 50)
4. Log all activity

Usage:
  python daily_automation.py            Run all tasks (live)
  python daily_automation.py --dry-run  Preview what would happen
  python daily_automation.py --task follow-ups  Run specific task only
"""
import json
import os
import sys
import subprocess
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def log(msg):
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"  [{timestamp}] {msg}")


def run_task(name, script, args=None):
    """Run a Python script and capture output."""
    cmd = [sys.executable, os.path.join(BASE_DIR, script)]
    if args:
        cmd.extend(args)

    log(f"Starting: {name}")
    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=600, cwd=BASE_DIR
        )
        # Print last 20 lines of output
        lines = result.stdout.strip().split("\n")
        for line in lines[-20:]:
            print(f"    {line}")
        if result.returncode != 0 and result.stderr:
            log(f"  Error: {result.stderr[-200:]}")
        return result.returncode == 0
    except subprocess.TimeoutExpired:
        log(f"  Timeout: {name} took longer than 10 minutes")
        return False
    except Exception as e:
        log(f"  Failed: {e}")
        return False


def run_all(dry_run=False, task=None):
    print("=" * 60)
    print("  DAILY AUTOMATION RUNNER")
    print(f"  Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"  Mode: {'DRY RUN' if dry_run else 'LIVE'}")
    if task:
        print(f"  Task: {task}")
    print("=" * 60)

    results = {}
    args_base = ["--dry-run"] if dry_run else []

    # Task 1: Follow-up emails
    if not task or task == "follow-ups":
        print(f"\n{'─'*40}")
        print("  TASK 1: Follow-Up Emails")
        print(f"{'─'*40}")
        success = run_task(
            "Follow-up Pipeline",
            "follow_up_pipeline.py",
            args_base + ["--max", "25"]
        )
        results["follow-ups"] = success

    # Task 2: Email drip course
    if not task or task == "drip-course":
        print(f"\n{'─'*40}")
        print("  TASK 2: Email Drip Course")
        print(f"{'─'*40}")
        success = run_task(
            "Drip Course",
            "email_drip_course.py",
            ["--send-all-due"] + args_base
        )
        results["drip-course"] = success

    # Task 3: Wave 2 outreach (batch of 50)
    if not task or task == "outreach":
        print(f"\n{'─'*40}")
        print("  TASK 3: Wave 2 Outreach")
        print(f"{'─'*40}")
        success = run_task(
            "Wave 2 Outreach",
            "wave2_outreach.py",
            args_base + ["--batch", "50"]
        )
        results["outreach"] = success

    # Summary
    print(f"\n{'='*60}")
    print("  DAILY SUMMARY")
    print(f"{'='*60}")
    for task_name, success in results.items():
        status = "OK" if success else "FAILED"
        icon = "✅" if success else "❌"
        print(f"  {icon} {task_name}: {status}")

    # Save daily log
    log_dir = os.path.join(BASE_DIR, "data", "daily_logs")
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, f"{datetime.now().strftime('%Y-%m-%d')}.json")
    log_entry = {
        "date": datetime.now().isoformat(),
        "mode": "dry_run" if dry_run else "live",
        "results": {k: "success" if v else "failed" for k, v in results.items()},
    }
    with open(log_file, "w", encoding="utf-8") as f:
        json.dump(log_entry, f, indent=2)

    print(f"\n  Log saved: {log_file}")
    return all(results.values())


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--task", choices=["follow-ups", "drip-course", "outreach"])
    args = parser.parse_args()
    run_all(dry_run=args.dry_run, task=args.task)
