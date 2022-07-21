# PARKulting-server
Серверная часть проекта [PARKulting](https://github.com/OverHome/PARKulting).  
Состоит из базы данных, неиросети и API.

# Установка и запуск 

Скачать проект
```bash
$ git clone https://github.com/OverHome/PARKulting-server.git
$ cd PARKulting-server
```
Установить нужные библиотеки
```
$ pip install -r requirements.txt
```
Запустить приложение
```
$ python main.py
```

# Важно 
Приложение и сервер должны находиться в одной локальной сети или же пробросить порт через [ngrok](https://ngrok.com/) 

```bash
ngrok http 5000 
```

Так же нужно будет изменить BASE_URL в конфиге перед сборкой [PARKulting](https://github.com/OverHome/PARKulting/blob/main/app/src/main/java/com/over/parkulting/tools/ApiTool.java) 
```
private static final String BASE_URL = "{Ваш URl или IP сервера}";
```