#!/usr/bin/env python3
"""Run offline Otto checks; browser assertions are driven only through shot.py.
No firmware, network socket, Git, or production HTML writes are performed.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
from datetime import datetime, timezone

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
SUITES = ('core', 'camera', 'sides', 'fullscreen', 'ui')

def locate_shot(value: str | None) -> Path:
    if value:
        p = Path(value).expanduser().resolve()
        if not p.is_file():
            raise FileNotFoundError(f'shot.py not found: {p}')
        return p
    candidates = []
    if os.environ.get('OTTO_SHOT_SCRIPT'):
        candidates.append(Path(os.environ['OTTO_SHOT_SCRIPT']))
    local = os.environ.get('LOCALAPPDATA')
    if local:
        candidates.append(Path(local) / 'Doubao/User Data/Default/.doubao/agent_mode/workspace/.skills/html/scripts/shot.py')
    candidates.extend([Path.home() / 'Doubao/skills/html/scripts/shot.py', Path.home() / '.agents/skills/html/scripts/shot.py'])
    for p in candidates:
        if p.is_file():
            return p.resolve()
    raise FileNotFoundError('需要 HTML 自检脚本；使用 --shot 路径或 OTTO_SHOT_SCRIPT 指定。静态检查可用 --static-only。')

def locate_browser(value: str | None) -> str | None:
    if value:
        p = Path(value).expanduser().resolve()
        if not p.is_file():
            raise FileNotFoundError(f'browser executable not found: {p}')
        return str(p)
    for var in ('PROGRAMFILES(X86)', 'PROGRAMFILES', 'LOCALAPPDATA'):
        base = os.environ.get(var)
        if not base:
            continue
        for suffix in ('Microsoft/Edge/Application/msedge.exe', 'Google/Chrome/Application/chrome.exe'):
            p = Path(base) / suffix
            if p.is_file():
                return str(p)
    return None

def run_command(args: list[str], timeout: int = 120) -> dict:
    p = subprocess.run(args, cwd=ROOT, capture_output=True, text=True, encoding='utf-8', errors='replace', timeout=timeout)
    return {'passed': p.returncode == 0, 'exit_code': p.returncode, 'stdout': p.stdout, 'stderr': p.stderr}

def main() -> int:
    parser = argparse.ArgumentParser(description='Otto 离线回归，不连接真机，不改生产 HTML')
    parser.add_argument('--html', type=Path, default=ROOT / 'otto-choreographer.html')
    parser.add_argument('--shot', help='HTML skill 的 scripts/shot.py 路径')
    parser.add_argument('--browser', help='Edge / Chrome 可执行文件路径；默认自动发现')
    parser.add_argument('--outdir', type=Path, help='报告输出目录；默认 otto-tests/results/时间戳')
    parser.add_argument('--suite', choices=SUITES, action='append', help='仅跑指定浏览器套件，可重复；默认全部')
    parser.add_argument('--static-only', action='store_true', help='仅静态/语法/逻辑fixture，不声明浏览器验证通过')
    args = parser.parse_args()
    stamp = datetime.now().strftime('%Y%m%d-%H%M%S-%f')
    out = (args.outdir or HERE / 'results' / stamp).resolve()
    out.mkdir(parents=True, exist_ok=False)
    html = args.html.resolve()
    if not html.is_file():
        raise FileNotFoundError(html)
    before = hashlib.sha256(html.read_bytes()).hexdigest()
    static = run_command([shutil.which('node') or 'node', str(HERE / 'static-check.cjs'), str(html), str(out / 'static')])
    (out / 'static-command.json').write_text(json.dumps(static, ensure_ascii=False, indent=2), encoding='utf-8')
    report = {'html': str(html), 'sha256': before, 'created_utc': datetime.now(timezone.utc).isoformat(), 'static': static, 'browser': [], 'static_only': args.static_only, 'network_policy': 'Browser fixtures use mock WebSocket; no device connection or firmware commands.'}
    success = static['passed']
    if success and not args.static_only:
        shot = locate_shot(args.shot)
        browser = locate_browser(args.browser)
        for suite in args.suite or SUITES:
            dest = out / suite
            command = [sys.executable, str(shot), str(html), '--no-auto-fix', '--outdir', str(dest), '--eval-file', str(HERE / f'{suite}.js'), '--format', 'png', '--max-width', '1440']
            if browser:
                command += ['--exec-path', browser]
            process = run_command(command)
            entry = {'suite': suite, 'process': process, 'views': [], 'passed': False}
            path = dest / 'report.json'
            if path.is_file():
                detail = json.loads(path.read_text(encoding='utf-8'))
                for view in ('desktop', 'mobile'):
                    v = detail.get('shots', {}).get(view, {})
                    ev = v.get('eval', {})
                    result = ev.get('result', {}) or {}
                    findings = [f for f in detail.get('findings', []) if f.get('severity') in ('blocker', 'error')]
                    passed = bool(ev.get('executed') and result.get('passed') is True and not ev.get('error') and not v.get('consoleErrors') and not v.get('resourceErrors') and not findings)
                    entry['views'].append({'view': view, 'passed': passed, 'count': result.get('count'), 'console_errors': v.get('consoleErrors'), 'console_warnings': v.get('consoleWarnings'), 'eval_error': ev.get('error'), 'screenshot': v.get('screenshot')})
                entry['passed'] = process['passed'] and all(v['passed'] for v in entry['views'])
            report['browser'].append(entry)
            success = success and entry['passed']
    report['production_unchanged'] = hashlib.sha256(html.read_bytes()).hexdigest() == before
    report['passed'] = success and report['production_unchanged']
    (out / 'summary.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f"{'PASS' if report['passed'] else 'FAIL'} {'(static-only; browser NOT run)' if args.static_only else ''}")
    print(f'Report: {out / "summary.json"}')
    for suite in report['browser']:
        print(f"{suite['suite']}: " + ', '.join(f"{v['view']}={v['passed']}({v['count']})" for v in suite['views']))
    return 0 if report['passed'] else 1

if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except (OSError, ValueError, subprocess.SubprocessError) as e:
        print(f'FAIL: {e}', file=sys.stderr)
        raise SystemExit(1)
