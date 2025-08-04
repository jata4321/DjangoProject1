def addition(a: object, b: object, *args) -> int:
    s = sum([a, b, *args])
    return s