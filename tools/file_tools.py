from pathlib import Path
WORKSPACE = Path("workspace").resolve()
def create_file(filename: str, content: str) -> str:
    """Create a file inside the agent workspace."""
    file_path = (WORKSPACE / filename).resolve()

    # Security check:
    # Make sure the file stays inside workspace/
    if WORKSPACE not in file_path.parents:
        return "Error: You are not allowed to create files outside the workspace."

    file_path.parent.mkdir(parents=True, exist_ok=True)

    file_path.write_text(content, encoding="utf-8")

    return f"File created successfully: {filename}"


def read_file(filename: str) -> str:
    """Read a file from the agent workspace."""

    file_path = (WORKSPACE / filename).resolve()

    if WORKSPACE not in file_path.parents:
        return "Error: You are not allowed to read files outside the workspace."

    if not file_path.exists():
        return f"Error: File '{filename}' does not exist."

    return file_path.read_text(encoding="utf-8")


def list_files() -> str:
    """List all files inside the agent workspace."""

    files = []

    for path in WORKSPACE.rglob("*"):
        if path.is_file():
            files.append(str(path.relative_to(WORKSPACE)))

    if not files:
        return "The workspace is empty."

    return "\n".join(files)