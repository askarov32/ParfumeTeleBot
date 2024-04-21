import pandas as pd
import telebot
import warnings
warnings.filterwarnings("ignore", message="^PyArrow will become a required dependency of pandas.*", category=DeprecationWarning)

bot = telebot.TeleBot(" ")


df = pd.read_csv("misha.csv")

@bot.message_handler(commands=['start'])
def start(message):
    welcome_message = "Привет! Я бот для поиска информации о товарах. Просто отправь мне название товара, и я постараюсь предоставить информацию о нем."
    bot.send_message(message.chat.id, welcome_message)

@bot.message_handler(func=lambda message: True)
def getinfo(message):
    try:
        request = message.text

        if request.startswith('/') and len(request.split()) > 1:
            return


        matching_names = df[df['name'].str.contains(request, case=False)]['name'].unique()

        if len(matching_names) > 0:
            # Loop through all matching names
            for name in matching_names:
                response = f"Название - {df.loc[df['name'] == name, 'name'].values[0]}\n" \
                           f"Цена в долларах - {df.loc[df['name'] == name, 'price'].values[0]}\n" \
                           f"Объем в мл - {df.loc[df['name'] == name, 'volume'].values[0]}"
                bot.send_message(message.chat.id, response)
        else:
            bot.send_message(message.chat.id, "Товар не найден.")

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        bot.send_message(message.chat.id, "Произошла ошибка при обработке запроса.")

if __name__ == '__main__':
    bot.polling(none_stop=True)
