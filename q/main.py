import contextlib
from asyncio import sleep

from pyrogram.errors import Flood
from pyrogram.errors.exceptions.bad_request_400 import ChatForwardsRestricted

from pagermaid.listener import listener
from pagermaid.enums import Client, Message


@listener(command="q",
          description="将回复的消息或者输入的字符串转换成语录")
async def yv_lu(bot: Client, message: Message):
    bot_username = "QuotLyBot"
    if message.reply_to_message:
        if message.parameter:
            try:
                reply = message.reply_to_message_id or message.reply_to_top_message_id
                count = int(message.arguments)
                ids = []
                for i in range(count):
                    ids.append(reply + i)
            except Exception as e:
                await message.edit(e)
        else:
            ids = message.reply_to_message_id or message.reply_to_top_message_id       
    else:
        return await message.edit('你需要回复一条消息。')
    with contextlib.suppress(Exception):
        await bot.unblock_user(bot_username)
    async with bot.conversation(bot_username) as conv:
        try:
            #await reply.forward(bot_username)
            await bot.forward_messages(
                chat_id=bot_username,
                from_chat_id=message.chat.id,
                message_ids=ids
                )
        except ChatForwardsRestricted:
            return await message.edit('群组消息不允许被转发。')
        await sleep(.1)
        chat_response = await conv.get_response()
        await conv.mark_as_read()
    try:
        await chat_response.copy(
            message.chat.id,
            reply_to_message_id=message.reply_to_message_id or message.reply_to_top_message_id)
    except Flood as e:
        await sleep(e.value + 1)
        with contextlib.suppress(Exception):
            await chat_response.copy(
                message.chat.id,
                reply_to_message_id=message.reply_to_message_id or message.reply_to_top_message_id)
    except Exception:
        pass
    await message.safe_delete()
