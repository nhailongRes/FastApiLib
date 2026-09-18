class NotFoundError(Exception):
    def __init__(self, detail:str = "Not Found"):
        self.detail = detail
        super().__init__(detail)
class ConflictError(Exception):
    def __init__(self, detail:str = "Conflict"):
        self.detail = detail
        super().__init__(detail)
class ValidationError(Exception):
    def __init__(self, detail: str = "Invalid"):
        self.detail = detail
        super().__init__(self.detail)
class DatabaseError(Exception):
    def __init__(self, detail: str = "Invalid Database"):
        self.detail = detail 
        super().__init__(detail)
class ForbiddenError(Exception):
    def __init__(self, detail: str = "Forbidden"):
        self.detail = detail
        super().__init__(detail)