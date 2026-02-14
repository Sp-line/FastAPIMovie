class UnsupportedMediaTypeException(Exception):
    def __init__(self, current_type: str | None, allowed_types: str):
        self.current_type = current_type
        self.allowed_types = allowed_types

        super().__init__(f"File type '{self.current_type}' is not supported, allowed types are: {self.allowed_types}")