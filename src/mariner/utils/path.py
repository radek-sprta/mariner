"""Platform-independent paths for Mariner."""
import os
import pathlib
import platform
import subprocess
from typing import Union


def check(path: Union[str, pathlib.Path]) -> pathlib.Path:
    """Check if path exists. If not, create it.

    Args:
      path: Path to check.

    Returns:
      Resulting path.
    """
    # Convert to Path object if needed
    if not isinstance(path, pathlib.Path):
        path = pathlib.Path(path)
    path = path.expanduser()

    # If path points to a file, get the parent directory
    directory = path.parent if path.suffix else path

    # Create path if needed
    directory.mkdir(parents=True, exist_ok=True)

    return path


def open_with_default_app(path: str, *, verbose=False) -> None:
    """Open file in OS's default application.

    Args:
        path: Path to the file.
        verbose: Print verbose output.
    """
    if platform.system() == "Linux":
        if verbose:
            subprocess.run(["xdg-open", path], check=False)
        else:
            with open(os.devnull) as devnull:
                subprocess.run(["xdg-open", path], stdout=devnull, stderr=devnull, check=False)
    elif platform.system() == "Windows":
        os.startfile(path)  # pylint: disable=no-member


def cache() -> pathlib.Path:
    """Cache path for the application.

    Returns:
        Cache path for the application.
    """
    if platform.system() == "Linux":
        config_dir = os.getenv("XDG_CACHE_HOME", "~/.cache")
        cache_dir = ""
    elif platform.system() == "Windows":
        config_dir = os.getenv("APPDATA")
        cache_dir = "Cache"
    return pathlib.Path(config_dir, "mariner", cache_dir)


def config() -> pathlib.Path:
    """Configuration path for the application.

    Returns:
        Configuration path for the application.
    """
    if platform.system() == "Linux":
        config_dir = os.getenv("XDG_CONFIG_HOME", "~/.config")
    elif platform.system() == "Windows":
        config_dir = os.getenv("APPDATA")
    return pathlib.Path(config_dir, "mariner")


def data() -> pathlib.Path:
    """Data path for the application.

    Returns:
        Data path for the application.
    """
    if platform.system() == "Linux":
        data_dir = os.getenv("XDG_DATA_HOME", "~/.local/share")
    elif platform.system() == "Windows":
        data_dir = os.getenv("APPDATA")
    return pathlib.Path(data_dir, "mariner")


def download() -> pathlib.Path:
    """User's download path.

    Returns:
        User's download path.
    """
    return pathlib.Path("~/Downloads").expanduser()


def log() -> pathlib.Path:
    """Log path for the application.

    Returns:
        Log path for the application.
    """
    if platform.system() == "Linux":
        data_dir = os.getenv("XDG_DATA_HOME", "~/.local/share")
        log_dir = "log"
    elif platform.system() == "Windows":
        data_dir = os.getenv("APPDATA")
        log_dir = "Logs"
    return pathlib.Path(data_dir, "mariner", log_dir)
