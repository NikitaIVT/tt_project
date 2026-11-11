from uuid import UUID


class ProductNotFoundError(Exception):
    def __init__(self, uuid: UUID):
        self.uuid = uuid
