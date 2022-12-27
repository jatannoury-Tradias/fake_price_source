def assert_raise(condition: bool, exception: Exception) -> None:
    if not condition:
        raise exception
