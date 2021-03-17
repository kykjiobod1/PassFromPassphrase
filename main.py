import hashlib
import re

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
    # set the rules
    passphrase = 'You are the sun, You are the only one'
    passphrase = passphrase.lower().encode('utf-8')  # Конвертирование пароля нижнем регистром в байты
    mini = None
    maxi = None
    salt = 'vk'.encode('utf-8') # Предоставление соли
    password = ''
    template = r'[A-z 0-9 . , : ; ? ! * + % - < > @ { } _ {} $ # \) ( / \\ \' \[ \] | " ~ & ^]'
    start = 1000  # Рекомендуется использоваться по крайней мере 100000 итераций SHA-256

while not (check(password)):  # Как задать необязательные параменты, который пользователь может ввести или не ввести?
        key = hashlib.pbkdf2_hmac('sha1', passphrase, salt, start, dklen=64)  # Получает ключ в 64 байта
        key = key.decode('utf-8', 'ignore')
        password = re.findall(template, key)
        password = ''.join(password)
        password = re.sub(' ', '', password)
        start += 1
print(password)




