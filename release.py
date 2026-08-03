"""Build, validate, and publish django-richmin to PyPI."""

import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DIST = ROOT / 'dist'
BUILD = ROOT / 'build'


def run(*args: str) -> None:
    subprocess.run([sys.executable, '-m', *args], cwd=ROOT, check=True)  # noqa


def main() -> None:
    # Never let artifacts from an older version join the current upload.
    shutil.rmtree(DIST, ignore_errors=True)
    shutil.rmtree(BUILD, ignore_errors=True)

    run('build')

    artifacts = sorted(str(path) for path in DIST.iterdir() if path.is_file())
    if not artifacts:
        raise RuntimeError('The build completed without creating any artifacts.')

    run('twine', 'check', *artifacts)
    # Uploads are performed one file at a time. If the connection fails after
    # one artifact succeeds, a retry should skip it and upload the remainder.
    run('twine', 'upload', '--verbose', '--skip-existing', *artifacts)


if __name__ == '__main__':
    main()
