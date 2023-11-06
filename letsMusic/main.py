''' PagerMaid Music Plugin , Thanks to @VmomoVBot '''

from pyrogram.errors import YouBlockedUser
from pyrogram import filters

from pagermaid import bot
from pagermaid.listener import listener
from pagermaid.enums import Message
from pagermaid.utils import alias_command
from pyrogram.raw.functions.channels import JoinChannel


LetsMusic_Help_Msg = f'''
`,{alias_command('letsMusic')} 水星记 郭顶 or 富士山下`  # 通过歌曲名称+歌手（可选）点歌
'''


async def bot_start() -> None:
    try:
        await bot.send_message("VmomoVBot", "/start")
    except YouBlockedUser:
        await bot.unblock_user("VmomoVBot")

async def channel_start() -> None:
	try:
		await bot.invoke(JoinChannel(channel=InputChannel(channel_id=-1001269673131)))
	except AttributeError as e:
		await message.edit(e)

async def music_search(keyword: str, message: Message):
    async with bot.conversation("VmomoVBot") as conv:
        await conv.send_message(keyword)
        await conv.mark_as_read()
        answer: Message = await conv.get_response(filters=filters.regex("Page"))
        await conv.mark_as_read()
        if not answer.reply_markup:
            return await message.edit(answer.text.html)
        await bot.request_callback_answer(
            answer.chat.id,
            answer.id,
            callback_data=answer.reply_markup.inline_keyboard[0][0].callback_data,
        )
        await conv.mark_as_read()
        answer: Message = await conv.get_response(filters=filters.audio)
        await conv.mark_as_read()
        await answer.copy(
            message.chat.id,
            reply_to_message_id=message.reply_to_message_id
            or message.reply_to_top_message_id,
        )
        await message.safe_delete()

@listener(
    command="letsMusic",
    description="Lets Music",
    parameters="[query]",
)
async def letsmusic(message: Message):
    if not message.arguments:
        return await message.edit(LetsMusic_Help_Msg)
    await bot_start()
#    await channel_start()
    return await music_search(message.arguments, message)
