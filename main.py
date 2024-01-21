from aiogram import Bot, Dispatcher,types
from aiogram.filters import CommandStart
import asyncio
import requests
from openai import OpenAI
from configuration.config import bot_token, openai_api_key

client = OpenAI(api_key=openai_api_key)
dp = Dispatcher()
loop = asyncio.get_event_loop()

@dp.message(CommandStart())
async def start(message: types.Message):
    await message.reply("Hi! I'm a link to chat gpt. How can I help you?")


async def process_request(message: types.Message):
    print(message.text)
    response = client.chat.completions.create(
        model="text-embedding-ada-002",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": message.text}
        ]
    )
    result = response.choices[0].message.content

    await dp.edited_messages(message.chat.id, message.message_id, result)

@dp.message()
async def answer(message: types.Message):
    sent_message = await message.reply("Wait a couple of seconds...")

    asyncio.create_task(process_request(message))

async def main():
    bot = Bot(token=bot_token)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
