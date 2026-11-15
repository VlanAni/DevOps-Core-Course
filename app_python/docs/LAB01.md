| Criterion | FastAPI | Flask |
| --- | --- | --- |
| Footprint | `~120-140` MB for a simple HTTP-server with JSON-endpoints | `~54` MD for simple HTTP-server with JSON-endpoints |
| JSON Throughput | `~440 req/s` | `~344` req/s |
| Sync/Async | Async Model | Sync Model |
| OpenAPI | Yes | Yes, but with plugins |
| Learning Curve | Same | Same |

### Benchmark Reference

Source:
[API Framework Performance Benchmark:
FastAPI vs Flask vs Django](https://medium.com/@afolabiifeoluwa06/api-framework-performance-benchmark-fastapi-vs-flask-vs-django-e767ad51574c)

The benchmark was conducted using Python 3.13 on Linux
with 1 vCPU and 4 GB RAM.

### Choice

FastAPI. 

Reasons: 
    - Async support
    - More fast
    - OpenAPI convertion

### Proof

Command: `find app_python -maxdepth 2 -type f | sort `

```
app_python/__pycache__/app.cpython-314.pyc
app_python/.gitignore
app_python/.python-version
app_python/.venv/.gitignore
app_python/.venv/.lock
app_python/.venv/CACHEDIR.TAG
app_python/.venv/pyvenv.cfg
app_python/app.py
app_python/docs/LAB01.md
app_python/pyproject.toml
app_python/README.md
app_python/tests/__init__.py
app_python/uv.lock
```