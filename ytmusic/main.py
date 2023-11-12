from pyrogram.errors import YouBlockedUser
from pyrogram import filters

from pagermaid import bot
from pagermaid.listener import listener
from pagermaid.enums import Message
from pagermaid.utils import alias_command

from asyncio import sleep


ytMusic_Help_Msg = f'''
`,{alias_command('yt')} 水星记 郭顶 or 富士山下`  # 通过歌曲名称+歌手（可选）点歌
'''


async def bot_start() -> None:
	try:
		await bot.send_message("rvbsm_musicbot", "/start")
	except YouBlockedUser:
		await bot.unblock_user("rvbsm_musicbot")

async def music_search(keyword: str, message: Message):
	async with bot.conversation("rvbsm_musicbot") as conv:
		await conv.send_message(keyword)
		await conv.mark_as_read()
		answer: Message = await conv.get_response(filters=filters.inline_keyboard)
		await conv.mark_as_read()
		await answer.click(0)
		await conv.mark_as_read()
		await sleep(0.7)
		await bot.copy_message(
			chat_id=message.chat.id,
			from_chat_id='rvbsm_musicbot',
			reply_to_message_id=message.reply_to_message_id or message.reply_to_top_message_id,
			message_id=answer.id + 1
			)
		await message.safe_delete()

@listener(
	command="yt",
	description="ytMusic",
	parameters="[query]",
)
async def ytMusic(message: Message):
	if not message.arguments:
		return await message.edit(ytMusic_Help_Msg)
	await bot_start()
	return await music_search(message.arguments, message)
