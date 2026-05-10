## Summary

This change adds real persistent sandbox support to the Boxlite provider.

Previously the provider always created anonymous transient boxes and only stored the human-readable sandbox name in connect info. That meant AstrBot could preserve a registry record, but the Boxlite runtime itself had no stable identity to reuse after restart.

This patch switches Boxlite-managed sandboxes to use a stable runtime name, enables `reuse_existing=True`, disables auto-removal for persistent runtimes, and records the persistent runtime name in connect info. The booter now separates normal shutdown from destructive cleanup so AstrBot stop/restart keeps the underlying Boxlite runtime available, while explicit sandbox destruction still removes it.

## Validation

- `uv run ruff check provider.py booters/boxlite.py test_persistence.py`
- `uv run pytest test_persistence.py`
