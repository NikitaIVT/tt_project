from uuid import UUID


class EntityNotFoundError(Exception):
    def __init__(self, uuid: UUID):
        self.uuid = uuid
