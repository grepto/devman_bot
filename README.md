# Мониторинг проверок уроков на [Devman'e](https://dvmn.org)
Скрипт контролирует появление новых результатов код-ревью на девмане и отправляет сообщение в телеграмм-чат
или в личку пользователю 


### Как установить
Для работы скрипта нужно зарегистрировать в операционной системе переменные окружения

- `TG_TOKEN` - Токен бота в телеграме
- `TG_CHAT_ID` - @Идентификатор телеграмм-чата или пользователя (например @smmreposting)

- `DEVMAN_TOKEN` Токен доступа пользователя к api Devman'a. Получать [тут](https://dvmn.org/api/docs/)
- `DEVMAN_ENDPOINT`= URL Devman'a (на данный момент https://dvmn.org)


- `LOG_LEVEL` - уровень логирования (NOTSET, DEBUG, INFO, WARNING, ERROR, CRITICAL). Подробно о каждом уровне
описано [тут](https://docs.python.org/3/library/logging.html)

 
Python3 должен быть уже установлен.
Затем используйте `pip` (или `pip3`, есть есть конфликт с Python2) для установки зависимостей:
```
pip install -r requirements.txt
```

### Как использовать
Запустить `main.py`


Пример использования
```bash
python main.py
```

### Цель проекта
Код написан в образовательных целях на онлайн-курсе для веб-разработчиков dvmn.org.