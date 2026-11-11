from sqlalchemy import event
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession


sync_session = AsyncSession.sync_session_class


@event.listens_for(sync_session, "after_flush")
def clean_after_flush(session: Session, flush_context):
    print("AFTER FLUSH")
    print("NEW:", session.new)
    print("DIRTY:", session.dirty)
    print("DELETED:", session.deleted)
    if session.new or session.dirty or session.deleted:
        session.info["clean"] = False


@event.listens_for(sync_session, "after_commit")
def clean_after_commit(session: Session):
    session.info["clean"] = True


@event.listens_for(sync_session, "after_rollback")
def clean_after_rollback(session: Session):
    session.info["clean"] = True
