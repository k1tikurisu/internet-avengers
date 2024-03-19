from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from sqlalchemy import select
from utils import log_info
import models.status as status_model
from database import get_db

async def is_alive_dino():
    db = get_db()
    result = await db.execute(
        select(status_model.Users.github_name)
    )
    github_names = result.scalars().all()
    log_info(github_names[0])
    # for github_name in github_names:
    #     git_client = GitClient("roypeco")
