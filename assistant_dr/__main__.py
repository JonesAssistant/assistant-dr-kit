from pathlib import Path

import typer

app = typer.Typer(help="assistant-dr-kit CLI - disaster recovery toolkit for local AI assistants")

DEFAULT_CONFIG_NAME = "assistant-dr.yaml"


TEMPLATE_CONFIG = """# assistant-dr.yaml
#
# Sample configuration for assistant-dr-kit.
# Adjust paths and lists to match your environment.

# Root of your assistant's workspace
workspace_root: /home/youruser/.openclaw/workspace

# Where to write the DR bundle (will be created if it doesn't exist)
bundle_output_path: /home/youruser/assistant-dr-bundles/latest

# Individual files (relative to workspace_root) to include in the bundle
include_files:
  - SOUL.md
  - USER.md
  - IDENTITY.md
  - IDENTITY_PROFILE.md
  - MEMORY.md
  - INDEX.md
  - FILE_ORGANIZATION_PROJECT.md

# Directories (relative to workspace_root) to include in the bundle
include_dirs:
  - memory
  - projects
  - skills

# Additional docs to include (relative to workspace_root)
docs:
  - MISS_JONES_DR_PROJECT.md
  - REPLICATION_CHECKLIST.md
  - REPLICATION_GUIDE.md
  - RIDE_THE_WAVE_PLAN.md

# Optional paths for extra content
packages_dir: /home/youruser/.openclaw/workspace/packages
scripts_dir: /home/youruser/.openclaw/workspace/scripts
models_dir: /home/youruser/.openclaw/workspace/models
services_dir: /home/youruser/.openclaw/workspace/services
"""


@app.command()
def init():
    """Create a sample assistant-dr.yaml config in the current directory."""

    cfg = Path(DEFAULT_CONFIG_NAME)

    if cfg.exists():
        typer.echo(f"Config file '{cfg}' already exists. Overwriting with template.")

    # Ensure parent directory exists
    cfg.parent.mkdir(parents=True, exist_ok=True)

    cfg.write_text(TEMPLATE_CONFIG)
    typer.echo(f"Wrote sample config to {cfg}")


@app.command()
def bundle():
    """Build a DR bundle from assistant-dr.yaml (not yet implemented)."""
    typer.echo("'assistant-dr bundle' is not implemented yet. TODO: implement bundling logic.")


@app.command()
def generate_revive():
    """Generate a revive-assistant.sh script (not yet implemented)."""
    typer.echo("'assistant-dr generate_revive' is not implemented yet. TODO: implement revive script generation.")


def main():
    app()


if __name__ == "__main__":  # pragma: no cover
    main()
