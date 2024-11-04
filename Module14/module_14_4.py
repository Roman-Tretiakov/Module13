import asyncio
from aiogram import Bot, Dispatcher, F, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, FSInputFile
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
import crud_functions

API_TOKEN = ''

bot = Bot(token=API_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

all_products = crud_functions.get_all_products()

inline_kb = InlineKeyboardBuilder()
button_calories = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
button_formulas = InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas')
inline_kb.row(button_calories, button_formulas)

buy_kb = InlineKeyboardBuilder()
product_1_button = InlineKeyboardButton(text='Product1', callback_data='product_buying_1')
product_2_button = InlineKeyboardButton(text='Product2', callback_data='product_buying_2')
product_3_button = InlineKeyboardButton(text='Product3', callback_data='product_buying_3')
product_4_button = InlineKeyboardButton(text='Product4', callback_data='product_buying_4')
buy_kb.row(product_1_button, product_2_button, product_3_button, product_4_button)

main_kb = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text='Рассчитать калории'), KeyboardButton(text='Информация')],
              [KeyboardButton(text='Купить')]], resize_keyboard=True)


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


@dp.message(Command('start'))
async def start(message: types.Message):
    await message.answer("Привет! Я бот помогающий твоему здоровью. Выберите дальнейшие действия:",
                         reply_markup=main_kb)


@dp.message(F.text.casefold() == 'информация')
async def main_menu(message: types.Message):
    await message.answer("У нас вы можете рассчитать калории или купить пилюли", reply_markup=main_kb)


@dp.message(F.text.casefold() == 'рассчитать калории')
async def main_menu(message: types.Message):
    await message.answer("Выберите опцию ниже:", reply_markup=inline_kb.as_markup())


@dp.message(F.text.casefold() == 'купить')
async def get_buying_list(message: types.Message):
    for id, title, description, price in all_products:
        product = FSInputFile(f'bank{id}.png', 'rb')
        await message.answer_photo(product, f'Название: {title} | Описание: {description} '
                                            f'| Цена: {price} руб.', show_caption_above_media=True)
    await message.answer("Выберите продукт для покупки:", reply_markup=buy_kb.as_markup())


@dp.callback_query(F.data == 'formulas')
async def get_formulas(callback: types.CallbackQuery):
    formula = (
        "Формула Миффлина-Сан Жеора:\n"
        "Для мужчин: 10 * вес + 6.25 * рост - 5 * возраст + 5\n"
        "Для женщин: 10 * вес + 6.25 * рост - 5 * возраст - 161"
    )
    await callback.message.answer(formula)
    await callback.answer()


@dp.callback_query(F.data == 'product_buying_1')
async def send_confirm_message_1(callback: types.CallbackQuery):
    await callback.message.answer(f'Вы успешно приобрели Product1')
    await callback.answer()


@dp.callback_query(F.data == 'product_buying_2')
async def send_confirm_message_2(callback: types.CallbackQuery):
    await callback.message.answer(f'Вы успешно приобрели Product2')
    await callback.answer()


@dp.callback_query(F.data == 'product_buying_3')
async def send_confirm_message_3(callback: types.CallbackQuery):
    await callback.message.answer(f'Вы успешно приобрели Product3')
    await callback.answer()


@dp.callback_query(F.data == 'product_buying_4')
async def send_confirm_message_4(callback: types.CallbackQuery):
    await callback.message.answer(f'Вы успешно приобрели Product4')
    await callback.answer()


@dp.callback_query(F.data == 'calories')
async def set_age(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer("Введите свой возраст:")
    await state.set_state(UserState.age)
    await callback.answer()


@dp.message(UserState.age)
async def set_growth(message: types.Message, state: FSMContext):
    await state.update_data(age=message.text)
    await message.answer("Введите свой рост:")
    await state.set_state(UserState.growth)


@dp.message(UserState.growth)
async def set_weight(message: types.Message, state: FSMContext):
    await state.update_data(growth=message.text)
    await message.answer("Введите свой вес:")
    await state.set_state(UserState.weight)


@dp.message(UserState.weight)
async def send_calories(message: types.Message, state: FSMContext):
    data = await state.get_data()
    weight = int(message.text)
    growth = int(data['growth'])
    age = int(data['age'])

    cal_norm_m = 10 * weight + 6.25 * growth - 5 * age + 5
    cal_norm_f = 10 * weight + 6.25 * growth - 5 * age - 161

    await message.answer(f"Норма калорий для мужчин: {cal_norm_m}\nНорма калорий для женщин: {cal_norm_f}.")
    await state.clear()


@dp.message()
async def all_messages(message: types.Message):
    await message.answer('Введите команду /start, чтобы начать общение.')


async def start_bot():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(start_bot())