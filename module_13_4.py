from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import executor

API_TOKEN = ''

bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


@dp.message_handler(commands='start')
async def send_welcome(message: types.Message):
    await message.answer("Привет! Я бот помогающий твоему здоровью.")


@dp.message_handler(Text(equals='calories', ignore_case=True))
async def set_age(message: types.Message):
    await message.answer("Введите свой возраст:")
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_growth(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['age'] = message.text
    await message.answer("Введите свой рост:")
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['growth'] = message.text
    await message.answer("Введите свой вес:")
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['weight'] = message.text

    data = await state.get_data()
    cal_norm_m = 10 * int(data['weight']) + 6.25 * int(data['growth']) - 5 * int(data['age']) + 5
    cal_norm_f = 10 * int(data['weight']) + 6.25 * int(data['growth']) - 5 * int(data['age']) - 161
    await message.answer(f"Норма калорий для мужчин: {cal_norm_m}\nНорма калорий для женщин: {cal_norm_f}.")
    await state.finish()

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)