from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from utils import utils

import models.status as status_model
import schemas.status as status_schema


async def check_status(db: AsyncSession, github_name: str) -> status_schema.MeResponse:
    users = await db.execute(
        select(status_model.Users).filter(status_model.Users.github_name == github_name)
    )
    user = users.first()

    if user:
        return {"status": user[0]}
    else:
        return {"status": None}


async def register_user(
    db: AsyncSession, status_register: status_schema.StatusRegisterRequest
) -> status_schema.StatusResponse:
    users = await db.execute(
        select(status_model.Users).filter(
            status_model.Users.github_name == status_register.github_name
        )
    )
    user = users.first()
    if user is None:
        status = status_model.Users(**status_register.dict())
        status.last_update = utils.what_time()
        db.add(status)
        await db.commit()
        await db.refresh(status)
        return {
            "color": status.color,
            "kind": status.kind,
            "level": status.level,
            "loop": status.loop,
        }
    else:
        user = user[0]
        user.loop += 1
        user.exp = 0
        user.level = 1
        user.color = status_register.color
        user.commits_count = 1
        user.last_update = utils.what_time()
        await db.commit()
        await db.refresh(user)
        return {
            "color": user.color,
            "kind": user.kind,
            "level": user.level,
            "loop": user.loop,
        }


async def feed_dino(db: AsyncSession, github_name: str) -> status_schema.StatusResponse:
    current_time_jst = utils.what_time()
    users = await db.execute(
        select(status_model.Users).filter(status_model.Users.github_name == github_name)
    )
    user = users.first()[0]
    user.level = 3
    user.exp = 3
    user.code_score = 3
    user.change_files = 3
    user.commits_count = 3
    user.last_update = current_time_jst
    user.loop = 3

    await db.commit()
    await db.refresh(user)
    return {
        "color": user.color,
        "kind": user.kind,
        "level": user.level,
        "loop": user.loop,
    }


async def kill_dino(db: AsyncSession, github_name: str) -> status_schema.StatusResponse:
    current_time_jst = utils.what_time()
    users = await db.execute(
        select(status_model.Users).filter(status_model.Users.github_name == github_name)
    )
    user = users.first()[0]
    user.level = 1
    user.exp = 0
    user.color = None
    user.kind = None
    user.last_update = current_time_jst
    user.loop = 1

    await db.commit()
    await db.refresh(user)
    return {
        "color": user.color,
        "kind": user.kind,
        "level": user.level,
        "loop": user.loop,
    }
