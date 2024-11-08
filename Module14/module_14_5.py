import asyncio
from aiogram import Bot, Dispatcher, F, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, FSInputFile
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
import crud_functions2

API_TOKEN = ''

bot = Bot(token=API_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

all_products = crud_functions2.get_all_products()
buy_kb = InlineKeyboardBuilder()

for index, product in enumerate(all_products, start=1):
    button = InlineKeyboardButton(
        text=product[1],
        callback_data=f'product_buying_{index}'
    )
    buy_kb.add(button)
buy_kb.adjust(4)

inline_kb = InlineKeyboardBuilder()
button_calories = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
button_formulas = InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas')
inline_kb.row(button_calories, button_formulas)

main_kb = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text='Регистрация')], [KeyboardButton(text='Рассчитать калории'),
                KeyboardButton(text='Информация')], [KeyboardButton(text='Купить')]], resize_keyboard=True)


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


class RegistrationState(StatesGroup):
    username = State()
    email = State()
    age = State()
    balance = State()


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
    product_name = all_products[0][1]
    await callback.message.answer(f'Вы успешно приобрели {product_name}')
    await callback.answer()


@dp.callback_query(F.data == 'product_buying_2')
async def send_confirm_message_2(callback: types.CallbackQuery):
    product_name = all_products[1][1]
    await callback.message.answer(f'Вы успешно приобрели {product_name}')
    await callback.answer()


@dp.callback_query(F.data == 'product_buying_3')
async def send_confirm_message_3(callback: types.CallbackQuery):
    product_name = all_products[2][1]
    await callback.message.answer(f'Вы успешно приобрели {product_name}')
    await callback.answer()


@dp.callback_query(F.data == 'product_buying_4')
async def send_confirm_message_4(callback: types.CallbackQuery):
    product_name = all_products[3][1]
    await callback.message.answer(f'Вы успешно приобрели {product_name}')
    await callback.answer()


@dp.callback_query(F.data == 'calories')
async def set_age(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer("Введите свой возраст:")
    await state.set_state(UserState.age)
    await callback.answer()


# User States:
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


# Registration States:
@dp.message(F.text.casefold() == 'регистрация')
async def sign_up(message: types.Message, state: FSMContext):
    await message.answer("Введите имя пользователя (только латинский алфавит):")
    await state.set_state(RegistrationState.username)


@dp.message(RegistrationState.username)
async def set_username(message: types.Message, state: FSMContext):
    if not crud_functions2.is_included(message.text):
        await state.update_data(username=message.text)
        await message.answer("Введите email пользователя:")
        await state.set_state(RegistrationState.email)
    else:
        await message.answer("Пользователь существует, введите другое имя")
        await state.set_state(RegistrationState.username)


@dp.message(RegistrationState.email)
async def set_email(message: types.Message, state: FSMContext):
    await state.update_data(email=message.text)
    await message.answer("Введите возраст пользователя:")
    await state.set_state(RegistrationState.age)


@dp.message(RegistrationState.age)
async def set_age(message: types.Message, state: FSMContext):
    await state.update_data(age=message.text)
    data = await state.get_data()
    username = str(data['username'])
    email = str(data['email'])
    age = data['age']
    crud_functions2.add_user(username=username, email=email, age=age)
    await message.answer("Регистрация прошла успешно!", reply_markup=main_kb)
    await state.clear()


# General texts
@dp.message()
async def all_messages(message: types.Message):
    await message.answer('Введите команду /start, чтобы начать общение.')


async def start_bot():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(start_bot())