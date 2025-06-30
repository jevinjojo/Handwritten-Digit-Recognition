"""Vercel entry point.
This lightweight stub imports the main Flask `app` object from the root-level
`app.py` so that Vercel can detect it as a Serverless Function. Keeping this
file small avoids duplicating heavy dependencies.
"""

import sys
from pathlib import Path

# Add project root to Python path so that `import app` resolves.
project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

from app import app  # noqa: E402

# Vercel looks for a top-level variable called `app` that is a WSGI application.
