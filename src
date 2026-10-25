import os
import re
from telethon import TelegramClient


class TelegramDownloader:

  def __init__(self, api_id, api_id_hash, session_name='tgdl_session'):
    self.api_id = api_id
    self.api_hash = api_id_hash
    self.session_name = session_name
    self.client = TelegramClient(self.session_name, self.api_id, self.api_hash)

  async def connect(self):
    await self.client.start()
    return await self.client.is_user_authorized()

  async def resolve_message(self, text):
    target_message = None

    # 1. tg://openmessage
    if 'tg://openmessage' in text or 'user_id=' in text:
      match_user = re.search(r'user_id=(-?\d+)', text)
      match_msg = re.search(r'message_id=(\d+)', text)
      if match_user and match_msg:
        peer_id = int(match_user.group(1))
        msg_id = int(match_msg.group(1))
        try:
          entity = await self.client.get_entity(peer_id)
        except Exception:
          entity = peer_id
        target_message = await self.client.get_messages(entity, ids=msg_id)

    # 2. t.me/c/
    elif 't.me/c/' in text:
      match_private = re.search(r't\.me/c/(\d+)/(\d+)', text)
      if match_private:
        chat_id = int('-100' + match_private.group(1))
        msg_id = int(match_private.group(2))
        entity = await self.client.get_entity(chat_id)
        target_message = await self.client.get_messages(entity, ids=msg_id)

    # 3. t.me/ public
    elif 't.me/' in text:
      match_public = re.search(r't\.me/([^/\s]+)/(\d+)', text)
      if match_public:
        chat_id = match_public.group(1)
        msg_id = int(match_public.group(2))
        entity = await self.client.get_entity(chat_id)
        target_message = await self.client.get_messages(entity, ids=msg_id)

    return target_message
