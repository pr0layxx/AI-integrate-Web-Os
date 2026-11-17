import json
import os
from pathlib import Path

from fastapi import HTTPException

# Configuration location
BASE_DIR = Path(__file__).resolve().parent
CONFIG_DIR = BASE_DIR / "permissions"
CONFIG_FILE = CONFIG_DIR / "config.json"


class PermissionManager:

    def __init__(self):
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        self.config = self.load_config()

    def load_config(self):
        if not CONFIG_FILE.exists():
            raise RuntimeError("Permission configuration is missing.")

        try:
            with CONFIG_FILE.open("r", encoding="utf-8") as file:
                config = json.load(file)
        except (json.JSONDecodeError, OSError) as error:
            raise RuntimeError("Unable to load permission configuration.") from error

        required_keys = {"access_mode", "excluded_paths", "operations"}

        if not required_keys.issubset(config):
            raise RuntimeError("Invalid permission configuration.")

        if config["access_mode"] != "full_access":
            raise RuntimeError("Unsupported access mode.")

        if not isinstance(config["excluded_paths"], list):
            raise RuntimeError("excluded_paths must be a list.")

        if not all(
            isinstance(path, str) and path.strip() for path in config["excluded_paths"]
        ):
            raise RuntimeError("excluded_paths must contain only non-empty strings.")

        if not isinstance(config["operations"], dict):
            raise RuntimeError("operations must be an object.")

        return config

    def save_config(self):
        temporary_file = CONFIG_FILE.with_suffix(".tmp")

        with temporary_file.open("w", encoding="utf-8") as file:
            json.dump(self.config, file, indent=4)

        os.replace(temporary_file, CONFIG_FILE)

    def is_excluded(self, target_path: Path) -> bool:
        try:
            target = target_path.resolve(strict=True)

            for excluded in self.config["excluded_paths"]:
                excluded_path = Path(excluded).resolve(strict=True)

                try:
                    target.relative_to(excluded_path)
                    return True
                except ValueError:
                    continue

            return False
        except (OSError, RuntimeError):
            raise HTTPException(
                status_code=403,
                detail="Unable to verify excluded paths. Access denied.",
            )

    def validate_path(self, user_path: str) -> Path:

        if not isinstance(user_path, str) or not user_path.strip():
            raise HTTPException(status_code=400, detail="Path cannot be empty.")

        try:
            target = Path(user_path).resolve(strict=True)
        except (OSError, RuntimeError):
            raise HTTPException(
                status_code=403, detail="Path cannot be safely resolved."
            )

        if not target.exists():
            raise HTTPException(status_code=404, detail="Path does not exist.")

        if self.is_excluded(target):
            raise HTTPException(
                status_code=403, detail="Access to this location is blocked."
            )

        return target

    def check_operation(self, operation: str):

        allowed = self.config["operations"].get(operation)

        if allowed is not True:
            raise HTTPException(
                status_code=403, detail=f"Operation '{operation}' is not permitted."
            )

    def authorize(self, user_path: str, operation: str) -> Path:

        self.check_operation(operation)

        return self.validate_path(user_path)


# Shared permission manager instance
permission_manager = PermissionManager()
