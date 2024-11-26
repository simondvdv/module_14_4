from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
import asyncio
from crud_functions import *

api = "7320391879:AAFb0h_U6NJO-hOUYtae2_ubOVhjaTzq64A"
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

# initiate_db()
# database_add()

kb = ReplyKeyboardMarkup(resize_keyboard=True)
bt_clrs = KeyboardButton(text='Рассчитать')
bt_info = KeyboardButton(text='Информация')
bt_buy = KeyboardButton(text='Купить')
kb.add(bt_clrs)
kb.add(bt_info)
kb.add(bt_buy)

kb_1 = InlineKeyboardMarkup()
bt_clrs_1 = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
bt_formula = InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas')
kb_1.add(bt_formula)
kb_1.add(bt_clrs_1)

product_menu_inline = InlineKeyboardMarkup()
bt_product1 = InlineKeyboardButton(text="Product1", callback_data="product_buying")
bt_product2 = InlineKeyboardButton(text="Product2", callback_data="product_buying")
bt_product3 = InlineKeyboardButton(text="Product3", callback_data="product_buying")
bt_product4 = InlineKeyboardButton(text="Product4", callback_data="product_buying")
product_menu_inline.add(bt_product1)
product_menu_inline.add(bt_product2)
product_menu_inline.add(bt_product3)
product_menu_inline.add(bt_product4)


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

#
# @dp.message_handler(text=["Купить"])
# async def get_buying_list(message):
#     for i in range(1, 5):
#         with open(f'images/img_bot_{i}.png', 'rb') as img:
#             await message.answer_photo(img, f'Название: Product{i} | Описание {i} | Цена: {100 * i}')
#         await message.answer("Выберете продукт для покупки:", reply_markup=product_menu_inline)


@dp.message_handler(text=["Купить"])
async def get_buying_list(message):
    image_count = 0
    for i in get_all_products():
        image_count += 1
        # id = i[0]
        title = i[1]
        description = i[2]
        price = i[3]
        with open(f'images/img_bot_{image_count}.png', 'rb') as img:
            await message.answer_photo(img, f'Название: {title} | Описание {description} | Цена: {price}')
    await message.answer("Выберете продукт для покупки:", reply_markup=product_menu_inline)


@dp.callback_query_handler(text=["product_buying"])
async def send_confirm_message(call):
    await call.message.answer("Вы успешно приобрели продукт!")
    await call.answer()


@dp.message_handler(text=['Рассчитать'])
async def main_menu(message):
    await message.answer('Выберите опцию:', reply_markup=kb_1)


@dp.callback_query_handler(text=['formulas'])
async def get_formulas(call):
    await call.message.answer('10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5;')
    await call.answer()


@dp.message_handler(commands=["start"])
async def start_message(message):
    await message.answer(text='Привет! Я бот помогающий твоему здровью.', reply_markup=kb)


@dp.callback_query_handler(text=['calories'])
async def set_age(call):
    await call.message.answer('Введите свой возраст:')
    await call.answer()
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(user_age=message.text)
    await message.answer('Введите свой рост:')
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(user_growth=message.text)
    await message.answer('Введите свой вес:')
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(user_weight=message.text)
    data = await state.get_data()
    calories = 10 * int(data['user_weight']) + 6.25 * int(data['user_growth']) - 5 * int(data['user_age']) + 5
    await message.answer(f"Ваша норма калорий {calories}")
    await state.finish()
#
#
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)