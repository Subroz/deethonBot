import shutil
import time

from telethon import Button, events
from telethon.events import NewMessage, StopPropagation

from . import bot, botStartTime, logger, plugins
from .utils import translate, fetch
from .utils.bot_utils import get_readable_file_size, get_readable_time

plugins.load()

inline_search_buttons = [
    [
        Button.switch_inline(translate.SEARCH_TRACK, same_peer=True),
        Button.switch_inline(
            translate.SEARCH_ALBUM, query=".a ", same_peer=True
        ),
    ],
    [Button.inline("❌")],
]


@bot.on(NewMessage(pattern="/start"))
async def start(event: NewMessage.Event):
    await event.reply(translate.WELCOME_MSG, buttons=inline_search_buttons)
    raise StopPropagation


@bot.on(NewMessage(pattern="/help"))
async def get_help(event: NewMessage.Event):
    await event.reply(translate.HELP_MSG)


@bot.on(NewMessage(pattern="/info"))
async def info(event: NewMessage.Event):
    await event.reply(translate.INFO_MSG)
    raise StopPropagation


@bot.on(NewMessage(pattern="/log"))
async def log(event: NewMessage.Event):
    await event.reply(file=f"{__name__}.log")
    raise StopPropagation


@bot.on(NewMessage(pattern="/stats"))
async def stats(event: NewMessage.Event):
    current_time = get_readable_time((time.time() - botStartTime))
    total, used, free = shutil.disk_usage(".")
    total = get_readable_file_size(total)
    used = get_readable_file_size(used)
    free = get_readable_file_size(free)
    await event.reply(
        translate.STATS_MSG.format(current_time, total, used, free)
    )
    raise StopPropagation


@bot.on(events.NewMessage())
async def search(event: NewMessage.Event):
    if event.text.startswith("/"):
        search_query = ""
    else:
        search_query = event.text
    await event.respond(
        translate.CHOOSE,
        buttons=[
            [
                Button.switch_inline(
                    translate.SEARCH_TRACK, query=search_query, same_peer=True
                ),
                Button.switch_inline(
                    translate.SEARCH_ALBUM,
                    query=".a " + search_query,
                    same_peer=True,
                ),
            ],
            [Button.inline("❌")],
        ],
    )


with bot:
    bot.run_until_disconnected()
    logger.info("Bot stopped")
    bot.loop.run_until_complete(fetch.session.close())
