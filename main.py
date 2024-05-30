import requests
import base64
import time
from random import randint
from aiogram import Bot, Dispatcher, types, executor

Api = '6855894723:AAH1P5ctZQNRW39z53b4B4-FV7CoaTteeYw'
bot = Bot(token= Api)
dp = Dispatcher(bot)

@dp.message_handler(commands='start')
async def start(message: types.Message):
    await message.answer('попробуй мою нейронку на минималках')





def generate_image(prompt_text):

    prompt = {
      "modelUri": "art://b1gscl6cclrd16qrrl5b/yandex-art/latest",
      "generationOptions": {
        "seed": randint(10000, 2000000000)
      },
      "messages": [
        {
          "weight": 1,
          "text": prompt_text
        }
      ]
      }

    url = "https://llm.api.cloud.yandex.net/foundationModels/v1/imageGenerationAsync"

    headers = {
       "Content-Type": "application/json",
       "Authorization": "Api-key AQVNz1Jc0e0zKGzDP0XSkT_E019e6xglrVuA41ke"
      }

    response = requests.post(url=url, headers= headers, json= prompt)
    result = response.json()
    print(result)

    operation_id = result['id']

    operation_url = f"https://llm.api.cloud.yandex.net:/operations/{operation_id}"

    while True:
        operation_response = requests.get(url= operation_url, headers= headers)
        operation_result = operation_response.json()
        if 'response' in operation_result:
          image_base64 = operation_result['response']['image']
          image_data = base64.b64decode(image_base64)
          return image_data
        else:
          print('Ожидайте, изображение не готово')
          time.sleep(5)



@dp.message_handler()
async def handle_message(message: types.Message):
    user_text = message.text
    await message.reply('Идет генерация изображения, жди')

    try:
        image_data = generate_image(user_text)
        await message.reply_photo(photo= image_data)
    except Exception as e:
        await message.reply(f"Произошла оишбка {e}")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates= True)


