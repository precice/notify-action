from datetime import datetime, timezone
from zoneinfo import ZoneInfo
import asyncio
import nio
import os

def buildMessage(status: str, repo: str, name: str, link: str, tag_all: bool):
    assert status in {"success", "failure", "skipped"}
    icon = {
        "success": "🟢",
        "failure": "🟥",
        "skipped": "🔷",
    }.get(status)

    ts = datetime.now(ZoneInfo("Europe/Berlin")).strftime("%d.%m.%yT%H:%M")

    mention = " @room" if tag_all else ""

    body = f"{icon} {repo}/{name} {link} {ts}{mention}"
    formatted_body = f'{icon} <a href="{link}">{repo}/{name}</a> {ts}{mention}'

    return {
        "msgtype": "m.text",
        "body": body,
        "format": "org.matrix.custom.html",
        "formatted_body": formatted_body,
    }


async def main() -> None:
    status = os.environ["STATUS"]
    repo = os.environ["REPO"]
    assert "/" in repo
    repo = repo.partition("/")[-1] # drop owner
    name = os.environ["NAME"]
    link = os.environ["LINK"]
    tag_all = os.environ.get("TAG_ALL", "false").lower() in {"true", "1", "yes", "y", "t"}

    message = buildMessage(status=status, repo=repo, name=name, link=link, tag_all=tag_all)

    room_id = os.environ["ROOM_ID"]

    client = nio.AsyncClient(os.environ["HOMESERVER"], os.environ["LOGIN"])
    print(await client.login(os.environ["PASSWORD"]))

    await client.room_send(
        room_id=room_id,
        message_type="m.room.message",
        content=message,
    )
    await client.close()

if __name__ == "__main__":
    asyncio.run(main())
