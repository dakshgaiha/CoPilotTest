"""
File Access Module

Provides utilities for enabling and managing file type access for users.
Resolves 'Consumption File Type Failure' by granting users access to files
based on allowed file types.
"""

ALLOWED_FILE_TYPES = {
    "text": [".txt", ".csv", ".log"],
    "document": [".pdf", ".docx", ".xlsx"],
    "image": [".png", ".jpg", ".jpeg", ".gif"],
    "data": [".json", ".xml", ".yaml", ".yml"],
}


def get_file_extension(filename: str) -> str:
    """Return the lowercase extension of a filename, or empty string if none."""
    idx = filename.rfind(".")
    if idx <= 0:
        return ""
    return filename[idx:].lower()


def is_file_type_allowed(filename: str, allowed_types: list[str] | None = None) -> bool:
    """
    Check whether a file's type is allowed for consumption.

    Args:
        filename: The name (or path) of the file.
        allowed_types: Optional list of allowed category names (e.g. ["text", "data"]).
                       Defaults to all categories in ALLOWED_FILE_TYPES.

    Returns:
        True if the file extension belongs to an allowed category, False otherwise.
    """
    ext = get_file_extension(filename)
    if not ext:
        return False

    categories = allowed_types if allowed_types is not None else ALLOWED_FILE_TYPES.keys()
    for category in categories:
        if category in ALLOWED_FILE_TYPES and ext in ALLOWED_FILE_TYPES[category]:
            return True
    return False


def enable_file_access(user: str, filename: str, allowed_types: list[str] | None = None) -> dict:
    """
    Enable access to a file for a given user if the file type is allowed.

    Args:
        user: The username requesting access.
        filename: The name (or path) of the file.
        allowed_types: Optional list of allowed category names to restrict access to.

    Returns:
        A dict with keys:
          - "user": the username
          - "filename": the filename
          - "access_granted": bool indicating whether access was granted
          - "reason": human-readable explanation
    """
    if not user or not user.strip():
        return {
            "user": user,
            "filename": filename,
            "access_granted": False,
            "reason": "Invalid user.",
        }

    if not filename or not filename.strip():
        return {
            "user": user,
            "filename": filename,
            "access_granted": False,
            "reason": "Invalid filename.",
        }

    if is_file_type_allowed(filename, allowed_types):
        return {
            "user": user,
            "filename": filename,
            "access_granted": True,
            "reason": f"Access granted to '{filename}' for user '{user}'.",
        }

    ext = get_file_extension(filename)
    return {
        "user": user,
        "filename": filename,
        "access_granted": False,
        "reason": (
            f"File type '{ext}' is not allowed for consumption. "
            "Please use a supported file type."
        ),
    }
