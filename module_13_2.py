from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters.command import Command
from aiogram.fsm.storage.memory import MemoryStorage
import asyncio


API_TOKEN = ''

bot = Bot(token=API_TOKEN)
dp = Dispatcher(storage=MemoryStorage())


@dp.message(Command(commands=['start']))
async def start(message: Message):
    print("Привет! Я бот помогающий твоему здоровью.")


@dp.message()
async def all_messages(message):
    print('Введите команду /start, чтобы начать общение.')


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

