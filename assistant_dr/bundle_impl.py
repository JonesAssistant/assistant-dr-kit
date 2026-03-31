from __future__ import annotations

import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional

import yaml


@dataclass
class AssistantDRConfig:
    workspace_root: Path
    bundle_output_path: Path
    include_files: List[str]
    include_dirs: List[str]
    docs: List[str]
    packages_dir: Optional[Path] = None
    scripts_dir: Optional[Path] = None
    models_dir: Optional[Path] = None
    services_dir: Optional[Path] = None

    @staticmethod
    def from_yaml(path: Path) -> "AssistantDRConfig":
        data = yaml.safe_load(path.read_text())

        root = Path(data["workspace_root"]).expanduser()
        out = Path(data["bundle_output_path"]).expanduser()

        def _opt_dir(key: str) -> Optional[Path]:
            val = data.get(key)
            return Path(val).expanduser() if val else None

        return AssistantDRConfig(
            workspace_root=root,
            bundle_output_path=out,
            include_files=data.get("include_files", []),
            include_dirs=data.get("include_dirs", []),
            docs=data.get("docs", []),
            packages_dir=_opt_dir("packages_dir"),
            scripts_dir=_opt_dir("scripts_dir"),
            models_dir=_opt_dir("models_dir"),
            services_dir=_opt_dir("services_dir"),
        )


def build_bundle(cfg_path: Path) -> Path:
    """Build a DR bundle based on the given config file.

    Returns the path to the bundle root directory.
    """

    cfg = AssistantDRConfig.from_yaml(cfg_path)

    # Create bundle root + standard subdirs
    bundle_root = cfg.bundle_output_path
    docs_dir = bundle_root / "docs"
    ws_dir = bundle_root / "workspace"
    packages_dir = bundle_root / "packages"
    scripts_dir = bundle_root / "scripts"
    models_dir = bundle_root / "models"
    services_dir = bundle_root / "services"

    for d in [docs_dir, ws_dir, packages_dir, scripts_dir, models_dir, services_dir]:
        d.mkdir(parents=True, exist_ok=True)

    # Copy include_files into workspace root (relative paths preserved)
    for rel in cfg.include_files:
        src = cfg.workspace_root / rel
        dest = ws_dir / rel
        if not src.exists():
            print(f"[WARN] include_file missing: {src}")
            continue
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dest)

    # Copy include_dirs recursively into workspace
    for rel in cfg.include_dirs:
        src = cfg.workspace_root / rel
        dest = ws_dir / rel
        if not src.exists():
            print(f"[WARN] include_dir missing: {src}")
            continue
        if dest.exists():
            shutil.rmtree(dest)
        shutil.copytree(src, dest)

    # Copy docs into docs_dir
    for rel in cfg.docs:
        src = cfg.workspace_root / rel
        dest = docs_dir / rel
        if not src.exists():
            print(f"[WARN] doc missing: {src}")
            continue
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dest)

    # Copy optional whole directories if they exist
    def _copy_optional(src_dir: Optional[Path], dest: Path, label: str) -> None:
        if not src_dir:
            return
        if not src_dir.exists():
            print(f"[INFO] {label} directory not found, skipping: {src_dir}")
            return
        # Replace existing dest to keep bundle clean
        if dest.exists():
            shutil.rmtree(dest)
        shutil.copytree(src_dir, dest)

    _copy_optional(cfg.packages_dir, packages_dir, "packages")
    _copy_optional(cfg.scripts_dir, scripts_dir, "scripts")
    _copy_optional(cfg.models_dir, models_dir, "models")
    _copy_optional(cfg.services_dir, services_dir, "services")

    return bundle_root
