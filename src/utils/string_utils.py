def normalize_string(s):
    """
    Normalize a string by converting it to lowercase and removing extra whitespace.

    Args:
        s (str): The input string to normalize.
    Returns:
        str: The normalized string.
    """
    return " ".join(s.lower().split())


def pascal_case(s):
    """
    Convert a string to PascalCase.

    Args:
        s (str): The input string to convert.
    Returns:
        str: The string converted to PascalCase.
    """
    return "".join(word.capitalize() for word in s.split())


def snake_case(s):
    """
    Convert a string to snake_case.

    Args:
        s (str): The input string to convert.
    Returns:
        str: The string converted to snake_case.
    """
    return "_".join(word.lower() for word in s.split())
