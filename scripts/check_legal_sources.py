"""Run outside the request/UI path; reports only, never edits approved rules."""
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from services.legal_source_watch import scan_sources


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--report-dir', default='legal-watch-report')
    args = parser.parse_args()
    folder = Path(args.report_dir)
    folder.mkdir(parents=True, exist_ok=True)
    previous_path = folder / 'latest.json'
    previous = json.loads(previous_path.read_text(encoding='utf-8')) if previous_path.exists() else {}
    registry = json.loads((ROOT / 'data/legal_references.json').read_text(encoding='utf-8'))
    report = scan_sources(registry, previous, checked_at=datetime.now(timezone.utc).isoformat())
    temp = folder / 'latest.tmp'
    temp.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    temp.replace(previous_path)
    summary = Path(__import__('os').environ.get('GITHUB_STEP_SUMMARY', folder / 'summary.md'))
    summary.write_text('# Legal source watch\n\nStatus: ' + report['status'] +
        '\n\nChanges: ' + str(len(report['changes'])) + '; failed sources: ' + str(len(report['failures'])) +
        '\n\nReview latest.json. No approved legal rules were changed. This is not proof of current validity or complete discovery.\n', encoding='utf-8')
    return 2 if report['status'] == 'review_required' else 0


if __name__ == '__main__':
    sys.exit(main())
