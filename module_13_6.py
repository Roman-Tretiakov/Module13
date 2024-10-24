from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor

API_TOKEN = ''

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

inline_kb = InlineKeyboardMarkup(row_width=2)
button_calories = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
button_formulas = InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas')
inline_kb.row(button_calories, button_formulas)


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


@dp.message_handler(commands='start')
async def start(message: types.Message):
    await message.answer("Привет! Я бот помогающий твоему здоровью.")


@dp.message_handler(Text(equals='Рассчитать', ignore_case=True))
async def main_menu(message: types.Message):
    await message.answer("Выберите опцию ниже:", reply_markup=inline_kb)


@dp.callback_query_handler(Text(equals='formulas'))
async def get_formulas(call):
    print('Callback \'formulas\' received')
    formula = (
        "Формула Миффлина-Сан Жеора:\n"
        "Для мужчин: 10 * вес + 6.25 * рост - 5 * возраст + 5\n"
        "Для женщин: 10 * вес + 6.25 * рост - 5 * возраст - 161"
    )
    await call.message.answer(formula)
    await call.answer()


@dp.callback_query_handler(Text(equals='calories'))
async def set_age(call):
    print('Callback \'calories\' received')
    await call.message.answer("Введите свой возраст:")
    await UserState.age.set()
    await call.answer()


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


@dp.message_handler()
async def all_messages(message: types.Message):
    await message.answer('Введите команду /start, чтобы начать общение.')

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
