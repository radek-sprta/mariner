"""Utility functions for Mariner."""
import pathlib


def check_path(path: pathlib.Path) -> pathlib.Path:
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
