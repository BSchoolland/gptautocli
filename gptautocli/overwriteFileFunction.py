import os


def write_content_to_file(filepath: str, content: str) -> str:
    """Write content to an absolute filepath, creating parent directories as needed.

    Returns a status string describing the result; this is fed back to the model so
    it can react to filesystem errors (e.g. permission denied) rather than crashing.
    """
    if not os.path.isabs(filepath):
        return "The provided filepath must be an absolute path."

    directory = os.path.dirname(filepath)
    if directory and not os.path.exists(directory):
        os.makedirs(directory)

    try:
        with open(filepath, 'w', encoding='utf-8') as file:
            file.write(content)
    except OSError as e:
        return str(e)
    return "Successfully wrote content to file."
