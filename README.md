# Тестовое задание для Lesta Games


### Description
Реализовать веб-приложение. В качестве интерфейса сделать страницу с формой для загрузки текстового файла, после загрузки и обработки файла отображается таблица с 50 словами с колонками:
- слово
- tf, сколько раз это слово встречается в тексте
- idf, обратная частота документа 

Вывод упорядочить по уменьшению idf.


### Technology stack
- fastapi 0.110.2
- Jinja2 3.1.3
- python-multipart 0.0.9
- uvicorn[standard] 0.29.0


### Project run on Windows
- Install and activate the virtual environment:  
```
py -m venv venv
. venv/Scripts/activate
```

- Upgrade pip:  
```
python.exe -m pip install --upgrade pip
```

- Install dependencies from requirements.txt:  
```
pip install -r requirements.txt
```

- Run the application:  
```
uvicorn main:app
```


#### Author
Karapetyan Zorik  
Russian Federation, St. Petersburg, Kupchino.