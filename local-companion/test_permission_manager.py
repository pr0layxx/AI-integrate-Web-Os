from permission_manager import PermissionManager
from pathlib import Path
from fastapi import HTTPException
import pytest


def test_allowed_operation():
    manager = PermissionManager()

    manager.config["operations"]["read"] = True

    manager.check_operation("read")
    
    
def test_blocked_operation():
    manager = PermissionManager()

    manager.config["operations"]["delete"] = False

    with pytest.raises(HTTPException):
        manager.check_operation("delete")
        
        
def test_accessible_path(tmp_path):
    manager = PermissionManager()

    test_folder = tmp_path / "documents"
    test_folder.mkdir()

    result = manager.validate_path(str(test_folder))

    assert result == test_folder.resolve()
    
def test_excluded_path(tmp_path):
    manager = PermissionManager()

    excluded_folder = tmp_path / "private"
    excluded_folder.mkdir()

    manager.config["excluded_paths"] = [str(excluded_folder)]

    with pytest.raises(HTTPException):
        manager.validate_path(str(excluded_folder))

def test_nested_excluded_path(tmp_path):
    manager = PermissionManager()

    excluded_folder = tmp_path / "private"
    nested_folder = excluded_folder / "photos"

    nested_folder.mkdir(parents=True)

    manager.config["excluded_paths"] = [str(excluded_folder)]

    with pytest.raises(HTTPException):
        manager.validate_path(str(nested_folder))