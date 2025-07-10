def sanitize_isoformat(value: str) -> str:
    if value.endswith("Z+00:00"):
        return value.replace("Z+00:00", "+00:00")
    elif value.endswith("Z"):
        return value.replace("Z", "+00:00")
    return value
