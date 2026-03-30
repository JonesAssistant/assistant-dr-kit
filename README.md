# assistant-dr-kit

Disaster recovery toolkit for local AI assistants – build portable DR bundles (files, configs, scripts) so you can revive your agent on new hardware fast.

> **Status:** Early design / v0.1 planning. Not production-ready yet.

## Why?

If you run a local AI assistant (on your own machine, server, or homelab), you don’t want to lose:

- Its **identity** (persona, long-term memory),
- Its **workspace** (docs, configs, skills, scripts),
- Its **routing + model setup**,

just because a disk dies or you move to a new box.

`assistant-dr-kit` helps you:

- Describe what matters in a simple config file,
- Bundle it into a structured **disaster-recovery package** (e.g. USB or archive),
- Generate a **revive script** to restore your assistant on a fresh machine.

## What v0.1 will do

Planned initial features:

- `assistant-dr init`  
  - Create a sample `assistant-dr.yaml` config in the current directory.
- `assistant-dr bundle`  
  - Read `assistant-dr.yaml` and build a DR bundle with:
    - `/docs` – DR notes, identity/profile, guides.
    - `/workspace` – selected files/dirs from your assistant’s workspace.
    - `/packages` – optional local installers or archives (e.g. OpenClaw tarball, Node archive).
    - `/scripts` – revive scripts, helper scripts.
    - `/models` – optional local model files.
    - `/services` – optional service definitions (systemd units, etc.).
- `assistant-dr generate-revive`  
  - Generate a generic `revive-assistant.sh` script tailored to the bundle layout.

## Example config (draft)

```yaml
# assistant-dr.yaml

workspace_root: /home/youruser/.openclaw/workspace

bundle_output_path: /home/youruser/assistant-dr-bundles/latest

include_files:
  - SOUL.md
  - USER.md
  - IDENTITY.md
  - IDENTITY_PROFILE.md
  - MEMORY.md
  - INDEX.md
  - FILE_ORGANIZATION_PROJECT.md

include_dirs:
  - memory
  - projects
  - skills

docs:
  - MISS_JONES_DR_PROJECT.md
  - REPLICATION_CHECKLIST.md
  - REPLICATION_GUIDE.md
  - RIDE_THE_WAVE_PLAN.md

packages_dir: /home/youruser/.openclaw/workspace/packages
scripts_dir: /home/youruser/.openclaw/workspace/scripts
models_dir: /home/youruser/.openclaw/workspace/models
services_dir: /home/youruser/.openclaw/workspace/services
