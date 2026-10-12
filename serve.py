#!/usr/bin/env python3
"""Run CRISPR4P locally with Python's built-in http.server.

Usage (from a Python <= 3.12 environment with primer3-py installed):

    python serve.py [port]

then open http://localhost:8000/webapp.py
"""
import os
import sys
from http.server import CGIHTTPRequestHandler, ThreadingHTTPServer

ROOT = os.path.dirname(os.path.abspath(__file__))


class Handler(CGIHTTPRequestHandler):
    # Use subprocess + sys.executable instead of fork/execve, so the script
    # runs under this interpreter (e.g. the virtualenv) regardless of its shebang.
    have_fork = False

    def is_cgi(self):
        # Treat webapp.py at the site root as the CGI script; serve everything
        # else (css/, etc.) as static files.
        path = self.path.split('?', 1)[0]
        if path == '/webapp.py':
            self.cgi_info = '', self.path[1:]
            return True
        return False


if __name__ == '__main__':
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    os.chdir(ROOT)  # webapp.py resolves data/ and precomputed/ relative to cwd
    with ThreadingHTTPServer(('127.0.0.1', port), Handler) as httpd:
        print(f"Serving CRISPR4P at http://localhost:{port}/webapp.py")
        httpd.serve_forever()
