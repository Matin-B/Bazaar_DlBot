import logging

from aiogram import Bot, Dispatcher, executor, filters, types
from aiogram.types import ParseMode
from bazaar_dl import download
from emoji import emojize

import config

# Configure logging
logging.basicConfig(level=logging.INFO)


bot = Bot(
    token=config.BOT_TOKEN,
    parse_mode=ParseMode.HTML,
)

dp = Dispatcher(bot=bot)


def convert_bytes(size):
    for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024.0:
            return "%3.1f %s" % (size, x)
        size /= 1024.0

    return size


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.reply(
        emojize(
            'Welcome to @bazaar_dlbot :raised_hand:\n\n'\
            ':check_mark_button: Please send me the app link in CafeBazaar.ir.\n\n\n'
            ':information: Source code is available on '\
            '<a href="https://github.com/Matin-B/bazaar_dlbot">GitHub</a>'
        )
    )


@dp.message_handler(filters.Regexp(regexp=r'cafebazaar\.ir\/app\/(.*)'))
async def download_app(message: types.Message, regexp):
    package_name = regexp.group(1)
    download_response = download(package_name)
    if download_response['status'] == 'success':
        download_link = download_response['data']['download_link']
        package_size = download_response['data']['package_size']
        installation_size = download_response['data']['installation_size']
        await message.reply(
            emojize(
                f':diamond_with_a_dot: Package Name: {package_name}\n'\
                f':small_orange_diamond: Package Size: {convert_bytes(int(package_size))}\n'\
                f':small_blue_diamond: Installation Size: {convert_bytes(int(installation_size))}\n\n'\
                f':link: Download Link:\n{download_link}\n\n'\
                ':robot: @bazaar_dlbot'
            )
        )
    else:
        await message.reply(
            'Please try again in a few minutes.'
        )


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
