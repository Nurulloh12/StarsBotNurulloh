# states/channel.py
from aiogram.fsm.state import State, StatesGroup

class ChannelState(StatesGroup):
    waiting_for_channel_username = State()
    waiting_for_channel_deletion = State()  