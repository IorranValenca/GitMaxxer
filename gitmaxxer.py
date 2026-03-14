#!/usr/bin/env python3
import os, subprocess, argparse, random, datetime, time, uuid, shutil, sys

# Comprehensive list of realistic commit messages
COMMIT_MESSAGES = [
    # Features
    "feat: Add user authentication system",
    "feat: Implement payment gateway integration",
    "feat: Add dark mode support",
    "feat: Create mobile app responsive design",
    "feat: Add email notification system",
    "feat: Implement two-factor authentication",
    "feat: Add search functionality",
    "feat: Create dashboard analytics",
    "feat: Implement API rate limiting",
    "feat: Add file upload support",
    "feat: Create user profile customization",
    "feat: Add real-time notifications",
    "feat: Implement database backup system",
    "feat: Add multi-language support",
    "feat: Create admin panel",
    "feat: Add batch import feature",
    "feat: Implement webhook support",
    "feat: Add spreadsheet export",
    "feat: Create advanced search filters",
    "feat: Implement caching layer",
    "feat: Add user role management",
    "feat: Create API documentation",
    "feat: Add automated testing pipeline",
    "feat: Implement data encryption",
    "feat: Add social media integration",
    "feat: Create performance monitoring dashboard",
    "feat: Implement GraphQL API",
    "feat: Add blockchain integration",
    "feat: Create recommendation engine",
    "feat: Add voice command support",
    
    # Fixes
    "fix: Resolve login button not responding",
    "fix: Handle database connection timeout",
    "fix: Correct CSS styling on mobile devices",
    "fix: Fix memory leak in cache system",
    "fix: Resolve race condition in data sync",
    "fix: Fix null pointer exception",
    "fix: Correct date formatting issue",
    "fix: Fix concurrent request handling",
    "fix: Resolve CORS policy violations",
    "fix: Fix infinite loop in pagination",
    "fix: Correct JWT token validation",
    "fix: Fix XSS vulnerability in user input",
    "fix: Resolve file encoding issues",
    "fix: Fix timezone conversion bug",
    "fix: Correct regex pattern matching",
    "fix: Fix image compression artifacts",
    "fix: Resolve socket connection errors",
    "fix: Fix Unicode character handling",
    "fix: Correct API response formatting",
    "fix: Fix broken dependency links",
    "fix: Resolve memory buffer overflow",
    "fix: Fix SSL certificate validation",
    "fix: Correct SQL injection vulnerability",
    "fix: Fix authentication token expiration",
    "fix: Resolve network latency issues",
    "fix: Fix form validation logic",
    "fix: Correct sorting algorithm",
    "fix: Fix background job scheduling",
    "fix: Resolve caching inconsistency",
    
    # Refactoring
    "refactor: Extract utility functions into separate module",
    "refactor: Improve error handling and logging",
    "refactor: Optimize database queries",
    "refactor: Clean up code structure and organization",
    "refactor: Consolidate duplicate code",
    "refactor: Improve naming conventions",
    "refactor: Separate concerns in components",
    "refactor: Simplify conditional logic",
    "refactor: Reduce method complexity",
    "refactor: Improve type safety",
    "refactor: Reorganize directory structure",
    "refactor: Extract magic numbers into constants",
    "refactor: Improve function signatures",
    "refactor: Remove deprecated code",
    "refactor: Simplify loop structures",
    "refactor: Improve test coverage",
    "refactor: Refactor state management",
    "refactor: Improve API contract design",
    "refactor: Consolidate configuration files",
    "refactor: Split large classes into smaller ones",
    "refactor: Improve dependency injection",
    "refactor: Remove dead code paths",
    "refactor: Refactor authentication flow",
    "refactor: Improve error messages",
    "refactor: Simplify build configuration",
    
    # Documentation
    "docs: Update API documentation",
    "docs: Add setup and installation instructions",
    "docs: Write README for authentication module",
    "docs: Document environment variables",
    "docs: Add code examples in docs",
    "docs: Document database schema",
    "docs: Create troubleshooting guide",
    "docs: Add contributing guidelines",
    "docs: Document deployment process",
    "docs: Add architecture diagrams",
    "docs: Document API endpoints",
    "docs: Add security best practices",
    "docs: Create quick start guide",
    "docs: Document configuration options",
    "docs: Add performance tuning guide",
    "docs: Create release notes",
    "docs: Document error codes",
    "docs: Add webhook documentation",
    "docs: Document rate limits",
    
    # Performance
    "perf: Optimize image loading and compression",
    "perf: Reduce bundle size by code splitting",
    "perf: Implement lazy loading for components",
    "perf: Optimize database indexing",
    "perf: Reduce API response times",
    "perf: Improve query performance",
    "perf: Cache expensive computations",
    "perf: Optimize memory usage",
    "perf: Reduce network requests",
    "perf: Improve rendering performance",
    "perf: Optimize asset delivery with CDN",
    "perf: Reduce JavaScript execution time",
    "perf: Improve CSS performance",
    "perf: Optimize database connection pooling",
    "perf: Reduce payload size",
    "perf: Implement request batching",
    "perf: Optimize sorting algorithms",
    "perf: Improve data structure efficiency",
    
    # Testing
    "test: Add unit tests for authentication",
    "test: Add integration tests for API",
    "test: Add end-to-end tests",
    "test: Improve test coverage",
    "test: Add edge case tests",
    "test: Add performance benchmarks",
    "test: Add regression tests",
    "test: Add security tests",
    "test: Improve test reliability",
    "test: Add smoke tests",
    "test: Add load testing",
    "test: Improve test organization",
    
    # Style
    "style: Format code with prettier",
    "style: Organize imports",
    "style: Update code style guide",
    "style: Remove unused imports",
    "style: Correct indentation",
    "style: Apply consistent formatting",
    "style: Update linting rules",
    
    # Build
    "build: Update dependencies",
    "build: Configure webpack optimizations",
    "build: Update build scripts",
    "build: Add production build optimization",
    "build: Configure Docker setup",
    "build: Update CI/CD pipeline",
    "build: Improve build performance",
    "build: Add environment configuration",
    
    # Dependencies
    "deps: Upgrade React to v18",
    "deps: Update Node.js version",
    "deps: Remove deprecated dependencies",
    "deps: Update security packages",
    "deps: Upgrade database driver",
    "deps: Update TypeScript to latest",
    "deps: Add new testing library",
    
    # DevOps/Infrastructure
    "infra: Set up automatic backups",
    "infra: Configure load balancing",
    "infra: Add monitoring and alerting",
    "infra: Set up auto-scaling",
    "infra: Configure environment-specific settings",
    "infra: Implement disaster recovery",
    "infra: Add log aggregation",
    "infra: Configure health checks",
    
    # Data Migration
    "data: Migrate user data to new schema",
    "data: Backfill missing data fields",
    "data: Clean up legacy data",
    "data: Archive old records",
    "data: Migrate to new database",
    "data: Transform data format",
    
    # Release/Version
    "release: Bump version to 2.0.0",
    "release: Prepare for production deployment",
    "release: Create release branch",
    "release: Tag release version",
]

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


def get_random_message():
    """Get a random realistic commit message from the list."""
    return random.choice(COMMIT_MESSAGES)


def make_commits(path, file_name, timestamps, message_prefix="chore: automated commit", dry_run=False, use_realistic=False):
    path = os.path.abspath(path)
    if not timestamps:
        print("No timestamps to commit.")
        return
    for ts in timestamps:
        entry = f"{ts.isoformat()} {uuid.uuid4().hex}\n"
        target = os.path.join(path, file_name)
        
        # Choose message based on use_realistic flag
        if use_realistic:
            commit_message = get_random_message()
        else:
            commit_message = f"{message_prefix} {ts.isoformat()}"
        
        if dry_run:
            print(f"[DRY] Would append to {target}: {entry.strip()}")
        else:
            with open(target, "a", encoding="utf-8") as f:
                f.write(entry)
        # stage and commit
        if dry_run:
            print(f"[DRY] git add {file_name} && git commit -m '{commit_message}' with GIT_AUTHOR_DATE={format_git_date(ts)}")
        else:
            run(["git", "add", file_name], cwd=path)
            env = os.environ.copy()
            env["GIT_AUTHOR_DATE"] = format_git_date(ts)
            env["GIT_COMMITTER_DATE"] = env["GIT_AUTHOR_DATE"]
            try:
                run(["git", "commit", "-m", commit_message], cwd=path, env=env)
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
    p.add_argument("--realistic", action="store_true", help="use realistic commit messages instead of automated prefix")
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
    make_commits(args.repo, args.file, timestamps, message_prefix=args.message, dry_run=args.dry_run, use_realistic=args.realistic)

    if args.push:
        if args.dry_run:
            print(f"[DRY] Would push {args.branch} to {args.remote} with --force")
        else:
            print(f"Pushing {args.branch} to {args.remote}...")
            run(["git", "push", "--force", args.remote, args.branch], cwd=args.repo)


if __name__ == "__main__":
    main()