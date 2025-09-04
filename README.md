# Боты для интеграции DialogFlow с Telegram и VK

Этот проект включает двух ботов для Telegram и ВКонтакте, которые используют Google DialogFlow для обработки естественного языка и интеллектуального ответа на сообщения пользователей.

## Требования

-   Python 3.9
    
-   Аккаунт Google Cloud с доступом к DialogFlow API
    
-   Бот в Telegram
    
-   Сообщество в ВКонтакте с настроенным API

## Установка

Клонируйте репозиторий:

```bash
git clone <ссылка-на-репозиторий>
cd VoiceBot
```
Установите зависимости:

```bash
pip install -r requirements.txt
```

Создайте файл `.env` в корне проекта и добавьте переменные:
```text
TELEGRAM_TOKEN=ваш_токен_бота_telegram
VK_TOKEN=ваш_токен_сообщества_vk
YOUR_PROJECT_ID=id_вашего_проекта_dialogflow
LANGUAGE_CODE=ru
TG_CHAT_ID=id_чата_для_отправки_логов
TELEGRAM_LOGS_TOKEN=токен_бота_для_логов
GOOGLE_APPLICATION_CREDENTIALS=путь/к/файлу/сервисного_аккаунта.json
```

## Запуск
Запустите Telegram бота:
```bash
python telegram_bot.py
```
Запустите VK бота:
```bash
python vk_bot.py
```

## Как это работает
Боты используют Google DialogFlow для обработки естественного языка. Когда пользователь отправляет сообщение:
1.  Сообщение отправляется в DialogFlow API
2.  ИИ обрабатывает запрос и определяет намерение пользователя
3.  Бот получает ответ от DialogFlow и отправляет его пользователю
4.  Если бот не понимает запрос (is_fallback = True), сообщение переходит операторам

## Мониторинг
Боты автоматически отправляют логи об ошибках в указанный Telegram-чат. Это позволяет оперативно реагировать на проблемы и обеспечивать стабильную работу 24/7.

## Развертывание на сервере
Бот развернут на сервере с характеристиками:
-   IP-адрес:  `195.133.194.120`
-   Пользователь:  `root`
-   Порт SSH:  `22`
    
Для подключения к серверу:
```bash
ssh root@195.133.194.120 -p 22
```
Расположение проекта:
```bash
cd /opt/VoiceBot
```
Запуск сервисов:
```bash
systemctl start vk-bot.service
systemctl start telegram-bot.service
```

## Пример работы
<p>
  <strong>Telegram бот</strong>: @voiceDetectedDevman_bot<br>
  <img alt="test" src="%D0%A1%D0%BD%D0%B8%D0%BC%D0%BE%D0%BA%20%D1%8D%D0%BA%D1%80%D0%B0%D0%BD%D0%B0%202025-09-04%20%D0%B2%2020.30.00.png" width="400">
</p>
<p >
  <strong>VK бот</strong>: Сообщество ВК (<a href="https://vk.com/club232492725">ссылка</a>)<br>
  <img alt="test" src="%D0%A1%D0%BD%D0%B8%D0%BC%D0%BE%D0%BA%20%D1%8D%D0%BA%D1%80%D0%B0%D0%BD%D0%B0%202025-09-04%20%D0%B2%2020.30.30.png" width="400">
</p>

