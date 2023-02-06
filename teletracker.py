import time
import telepot
import telepot.aio
from telepot.aio.loop import MessageLoop
from telepot.aio.delegate import pave_event_space, per_chat_id, create_open

API_KEY = 'YOUR_TELEGRAM_BOT_API_KEY'
CHAT_ID = 'YOUR_CHAT_ID'
TARGET_USER = 'TARGET_USER_NAME'

class NotifyOnAction(telepot.aio.helper.ChatHandler):
    def __init__(self, *args, **kwargs):
        super(NotifyOnAction, self).__init__(*args, **kwargs)

    async def on_chat_message(self, msg):
        content_type, chat_type, chat_id = telepot.glance(msg)
        if content_type == 'status' and msg['status']['user']['username'] == TARGET_USER:
            if msg['status']['online']:
                await self.sender.sendMessage("The target user is now online")

bot = telepot.aio.DelegatorBot(API_KEY, [
    pave_event_space()(
        per_chat_id(), create_open, NotifyOnAction, timeout=10
    ),
])

loop = asyncio.get_event_loop()
loop.create_task(MessageLoop(bot).run_forever())
print('Listening ...')

loop.run_forever()
