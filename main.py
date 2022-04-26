import hashlib
import re
import telebot

API_TOKEN = '<api_token>'
bot = telebot.TeleBot(API_TOKEN)
user_dict = {}


class User:
    def __init__(self):
        self.salt = None
        self.passphrase = None


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == "/pass":
        bot.send_message(message.from_user.id, "Для какого сайта?")
        bot.register_next_step_handler(message, get_salt)
    elif message.text == "/help":
        bot.send_message(message.from_user.id, "напиши /pass для получения пароля")
    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")

def get_salt(message):
    try:
        user = User()
        user.salt = message.text
        user_dict[message.chat.id] = user
        bot.send_message(message.from_user.id, 'Какая у тебя запоминающаяся, ключевая фраза?')
        bot.register_next_step_handler(message, get_passphrase)
    except Exception as ex:
        msg = ex
        bot.send_message(message.from_user.id, msg)

def get_passphrase(message):
    user = user_dict[message.chat.id]
    user.passphrase = message.text
    msg = user.passphrase + user.salt
    bot.send_message(message.from_user.id, 'Твой пароль:')
    msg = get_pass(user.salt, user.passphrase)
    bot.send_message(message.from_user.id, msg)


def get_pass(salt, passphrase):
    passphrase = passphrase.lower().encode('utf-8')  # Конвертирование пароля нижнем регистром в байты
    mini = None   #the lupa
    maxi = None
    salt = salt.encode('utf-8') # Предоставление соли
    password = ''
    template = r'[A-z 0-9 . , : ; ? ! * + % - < > @ { } _ {} $ # \) ( / \\ \' \[ \] | " ~ & ^]'
    start = 1000  # Рекомендуется использоваться по крайней мере 100000 итераций SHA-256

    while not (check(password)):  
        key = hashlib.pbkdf2_hmac('sha1', passphrase, salt, start, dklen=64)  # Получает ключ в 64 байта
        key = key.decode('utf-8', 'ignore')
        password = re.findall(template, key)
        password = ''.join(password)
        password = re.sub(' ', '', password)
        start += 1
        print(password)
    return password

def check (password, sizemin=12, sizemax=23):
    if (sizemin <= len(password) <= sizemax
            and (re.findall('[0-9]', password))
            and (re.findall('[a-z]', password))
            and (re.findall('[A-Z]', password))
            and (re.findall(r'[A-z 0-9 . , : ; ? ! * + % - < > @ { } _ {} $ # \) ( / \\ \' \[ \] | " ~ & ^]', password))):
        return True
    else:
        return False

if __name__ == '__main__':
    bot.polling(none_stop=True, interval=0)





