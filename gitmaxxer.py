#!/usr/bin/env python3
import os, subprocess, argparse, random, datetime, time, uuid, shutil, sys

def run(cmd, cwd=None, env=None, capture_output=False):
    try:
        return subprocess.run(cmd, cwd=cwd, env=env or os.environ, check=True, capture_output=capture_output)
    except subprocess.CalledProcessError as e:
        print(f"Command failed: {' '.join(cmd)}")
        if e.stdout:
            print(e.stdout.decode(errors='ignore'))
        if e.stderr:
            print(e.stderr.decode(errors='ignore'))
        raise


def ensure_git_available():
    if not shutil.which("git"):
        print("git not found in PATH. Please install Git and ensure it's on your PATH.")
        sys.exit(2)


def ensure_repo(path, name=None, email=None):
    path = os.path.abspath(path)
    os.makedirs(path, exist_ok=True)
    if not os.path.exists(os.path.join(path, ".git")):
        print(f"Initializing new git repository at {path}")
        run(["git", "init"], cwd=path)
        # create main branch name if git supports it (ignored if already set)
        try:
            run(["git", "branch", "-M", "main"], cwd=path)
        except Exception:
            pass
    if name:
        run(["git", "config", "user.name", name], cwd=path)
    if email:
        run(["git", "config", "user.email", email], cwd=path)


def gen_timestamps(date, start_h, end_h, n, jitter_seconds=300):
    # ensure sensible bounds
    if not (0 <= start_h <= 23 and 0 <= end_h <= 23 and start_h <= end_h):
        raise ValueError("start and end must be hours between 0 and 23 and start <= end")
    tz = datetime.datetime.now().astimezone().tzinfo
    start_dt = datetime.datetime.combine(date, datetime.time(start_h, 0, 0)).replace(tzinfo=tz)
    end_dt = datetime.datetime.combine(date, datetime.time(end_h, 59, 59)).replace(tzinfo=tz)
    total = (end_dt - start_dt).total_seconds()
    if total <= 0:
        return [start_dt]
    if n <= 0:
        return []
    if n == 1:
        return [start_dt + datetime.timedelta(seconds=total / 2)]
    times = []
    for i in range(n):
        frac = i / (n - 1) if n > 1 else 0.5
        sec = frac * total
        t = start_dt + datetime.timedelta(seconds=sec)
        t = t + datetime.timedelta(seconds=random.randint(-jitter_seconds, jitter_seconds))
        # ensure tzinfo preserved
        if t.tzinfo is None:
            t = t.replace(tzinfo=tz)
        times.append(t)
    times.sort()
    return times


def format_git_date(ts: datetime.datetime) -> str:
    # Ensure ts has tzinfo
    if ts.tzinfo is None:
        ts = ts.replace(tzinfo=datetime.datetime.now().astimezone().tzinfo)
    # Git accepts: 'Thu Apr 07 22:13:13 2005 -0700'
    return ts.strftime('%a %b %d %H:%M:%S %Y %z')


def make_commits(path, file_name, timestamps, message_prefix="chore: automated commit", dry_run=False):
    path = os.path.abspath(path)
    if not timestamps:
        print("No timestamps to commit.")
        return
    for ts in timestamps:
        entry = f"{ts.isoformat()} {uuid.uuid4().hex}\n"
        target = os.path.join(path, file_name)
        if dry_run:
            print(f"[DRY] Would append to {target}: {entry.strip()}")
        else:
            with open(target, "a", encoding="utf-8") as f:
                f.write(entry)
        # stage and commit
        if dry_run:
            print(f"[DRY] git add {file_name} && git commit -m '{message_prefix} {ts.isoformat()}' with GIT_AUTHOR_DATE={format_git_date(ts)}")
        else:
            run(["git", "add", file_name], cwd=path)
            env = os.environ.copy()
            env["GIT_AUTHOR_DATE"] = format_git_date(ts)
            env["GIT_COMMITTER_DATE"] = env["GIT_AUTHOR_DATE"]
            try:
                run(["git", "commit", "-m", f"{message_prefix} {ts.isoformat()}"], cwd=path, env=env)
            except Exception:
                print(f"Failed to commit for timestamp {ts.isoformat()}")
                raise
        # small pause to avoid very tight loops
        time.sleep(0.02)


def main():
    ensure_git_available()
    p = argparse.ArgumentParser(description="Automate many commits with controlled timestamps")
    p.add_argument("--repo", required=True, help="Path to repo to create/use")
    p.add_argument("--commits", type=int, default=100)
    p.add_argument("--date", type=lambda s: datetime.datetime.strptime(s, "%Y-%m-%d").date(), default=datetime.date.today())
    p.add_argument("--start", type=int, default=0, help="start hour (0-23)")
    p.add_argument("--end", type=int, default=23, help="end hour (0-23)")
    p.add_argument("--name", help="git user.name to set for this repo (optional)")
    p.add_argument("--email", required=True, help="git user.email to set for this repo")
    p.add_argument("--push", action="store_true", default=True, help="push to remote after creating commits (requires remote configured)")
    p.add_argument("--remote", default="origin")
    p.add_argument("--branch", default="main")
    p.add_argument("--file", default="commit_log.txt", help="file to modify for commits")
    p.add_argument("--message", default="chore: automated commit", help="commit message prefix")
    p.add_argument("--dry-run", action="store_true", help="show actions without performing git operations or file writes")
    args = p.parse_args()

    # validations
    if args.commits < 0:
        p.error("--commits must be >= 0")
    if args.start < 0 or args.start > 23 or args.end < 0 or args.end > 23 or args.start > args.end:
        p.error("--start and --end must be hours between 0 and 23 and start <= end")

    ensure_repo(args.repo, args.name, args.email)

    target_file = os.path.join(os.path.abspath(args.repo), args.file)
    # initial commit if file doesn't exist
    if not os.path.exists(target_file):
        if args.dry_run:
            print(f"[DRY] Would create initial file {target_file} and make init commit")
        else:
            open(target_file, "w", encoding="utf-8").close()
            run(["git", "add", args.file], cwd=args.repo)
            try:
                run(["git", "commit", "-m", "chore: init commit"], cwd=args.repo)
            except Exception:
                # if commit fails (e.g., hook), continue
                print("Initial commit failed or already exists; continuing...")

    timestamps = gen_timestamps(args.date, args.start, args.end, args.commits)
    print(f"Generating {len(timestamps)} commits on {args.date} between {args.start}:00 and {args.end}:59")
    make_commits(args.repo, args.file, timestamps, message_prefix=args.message, dry_run=args.dry_run)

    if args.push:
        if args.dry_run:
            print(f"[DRY] Would push {args.branch} to {args.remote}")
        else:
            print(f"Pushing {args.branch} to {args.remote}...")
            run(["git", "push", args.remote, args.branch], cwd=args.repo)


if __name__ == "__main__":
    main()