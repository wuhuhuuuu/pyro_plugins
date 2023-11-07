from pyrogram.errors import YouBlockedUser
from pyrogram import filters

from pagermaid import bot
from pagermaid.listener import listener
from pagermaid.enums import Message
from pagermaid.utils import alias_command


LetsMusic_Help_Msg = f'''
`,{alias_command('vkmusic')} 水星记 郭顶 or 富士山下`  # 通过歌曲名称+歌手（可选）点歌
'''


async def bot_start() -> None:
    try:
        await bot.send_message("vkmusic_bot", "/start")
    except YouBlockedUser:
        await bot.unblock_user("vkmusic_bot")

async def music_search(keyword: str, message: Message):
    async with bot.conversation("vkmusic_bot") as conv:
        await conv.send_message(keyword)
        await conv.mark_as_read()
        answer: Message = await conv.get_response(filters=filters.regex("Result"))
        await conv.mark_as_read()
        if not answer.reply_markup:
            return await message.edit(answer.text.html)
        await answer.click('1')
        await conv.mark_as_read()
        await bot.copy_message(
        	chat_id=message.chat.id,
        	from_chat_id='vkmusic_bot',
        	reply_to_message_id=message.reply_to_message_id
            or message.reply_to_top_message_id,
        	message_id=answer.id + 1
        	)
        await message.safe_delete()

@listener(
    command="vkmusic",
    parameters="[query]",
)
async def letsmusic(message: Message):
    if not message.arguments:
        return await message.edit(LetsMusic_Help_Msg)
    await bot_start()
    return await music_search(message.arguments, message)
