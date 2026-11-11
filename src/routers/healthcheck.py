from typing import Dict

from cadwyn import VersionedAPIRouter


router = VersionedAPIRouter()


@router.get('/healthcheck')
async def healthcheck() -> Dict[str, str]:
    return {'status': 'ok'}
