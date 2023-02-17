import json
import datetime
from aiogram.utils.markdown import hbold, hlink, hcode, hunderline
from aiogram import Dispatcher, executor, Bot, types
from news import check_news_update
from aiogram.dispatcher.filters import Text
import asyncio

token = '6050222744:AAGXHZFi1igkAa3jY-gUdzCR83FmofOiwN4'
user_id = '1581750481'


bot = Bot(token=token, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)


@dp.message_handler(commands='start')
async def start(message: types.Message):
    start_buttons = ['все новости', 'последние новости', '🆕свежие новости']
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)

    await message.answer('Выберите раздел', reply_markup=keyboard)

async def news_every_30_min():
    while True:
        fresh_news = check_news_update()
        if len(fresh_news) >= 1:
            for k, v in sorted(fresh_news.items()):
                news = f'<b>{datetime.datetime.fromtimestamp(v["time"])}</b>\n' \
                       f' {hlink(v["name"], v["url"])}'

                await bot.send_message(user_id, news, disable_notification=True)

        await asyncio.sleep(1800)



@dp.message_handler(Text(equals='все новости'))
async def get_all_news(message: types.Message):
    with open('news.json', encoding='utf-8') as file:
        news_dict = json.load(file)
        print(news_dict)

    for k, v in sorted(news_dict.items()):
        news = f'<b>{datetime.datetime.fromtimestamp(v["time"])}</b>\n' \
               f' {hlink(v["name"], v["url"])}'
        # f'<u>{v["name"]}</u>\n' \
        # f'{hcode(v["description"])}\n' \

        await message.answer(news)






@dp.message_handler(Text(equals='последние новости'))
async def get_last_news(message: types.Message):
    with open('news.json', encoding='utf-8') as file:
        news_dict = json.load(file)


    for k, v in sorted(news_dict.items())[-5:]:
        news = f'<b>{datetime.datetime.fromtimestamp(v["time"])}</b>\n' \
               f' {hlink(v["name"], v["url"])}'
        await message.answer(news)


@dp.message_handler(Text(equals='🆕свежие новости'))
async def get_fresh_news(message: types.Message):
    fresh_news = check_news_update()
    if len(fresh_news) >= 1:
        for k, v in sorted(fresh_news.items()):
            news = f'<b>{datetime.datetime.fromtimestamp(v["time"])}</b>\n' \
                   f' {hlink(v["name"], v["url"])}'
            await message.answer(news)
    else:
        await message.answer('Свежих новостей пока нет')


if __name__ == '__main__':
    asyncio.run(news_every_30_min())
    executor.start_polling(dp)
# if __name__ == '__main__':
#     loop= asyncio.get_event_loop()
#     loop.create_task(news_every_30_min())
#     executor.start_polling(dp)