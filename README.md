<p align="center">
  <a href="" rel="noopener">
 <img src="https://user-images.githubusercontent.com/73960471/202877762-e2a5770d-9ea8-46f4-aa7e-51323abcb5fa.png" alt="Hackathon logo" width="250"></a>
</p>
<h3 align="center">Scenery Vision. Desktop приложение</h3>

<div align="center">




[![Project](https://img.shields.io/badge/Project-SceneryVision-red)](https://pt.2035.university/project/scenery-vision)
[![Status](https://img.shields.io/badge/status-active-success.svg)]()
[![License](https://img.shields.io/badge/license-AGPL--3.0%20license-blue)](LICENSE.md)

</div>

---

<p align="center">
Scenery Vision - интеллектуальная система для автоматической генерации текста с помощью ИИ.
    <br>
</p>

## 📝 Содержание

- [Постановка задачи](#problem_statement)
- [Решение](#idea)
- [Идеи развития](#future_scope)
- [Как запустить](#getting_started)
- [Как использовать](#usage)
- [Использованные технологии](#tech_stack)
- [Авторы](#authors)

## 🧐 Постановка задачи <a name = "problem_statement"></a>

Любое изделие требует четкого описания. Для эффективного продвижения, необходимо уметь красиво преподносить все особенности и характеристики изделий. Такое описание можно придумать, но для большого количества товаров – это очень большие трудозатраты

Цель:
Создание интеллектуального системного приложения для автоматизации генерация текста для товаров и различных продуктов, с возможностью адаптации под иностранные языки.

## 💡 Решение <a name = "idea"></a>

Для достижения поставленной цели было разработана концепция системы. Система разделена на 2 основные части - сервер и клиент, клиентом могут выступать Desktop приложение
или web-интерфейс. В данном репозитории рассматривается Desktop-приложение-клиент. Приложение написано на языке Python с использованием PyQt. Оно умеет 
принимать пользовательские данные отправлять их на сервер, получать результаты генерации с сервера и формировать вывод в интерфейс,
также собирать результаты генерации в общую таблицу.

## 🚀 Идеи развития <a name = "future_scope"></a>

В ближайшее время планируется создать редизайн интерфейса и добавить некоторые фичи.

## 🏁 Как запустить <a name = "getting_started"></a>

Данная инструкция поможет вам запустить и протестировать наше приложение.

### Библиотеки

Все необходимые библиотеки устанавливаются с помощью следующей команды.

```
pip install requirements.txt
```

### Установка и запуск

Для работы с приложением необходимо запустить файл main.py

```
python main.py
```

## 🎈 Как использовать <a name="usage"></a>

Для полноценной работы приложения сервер должен быть запущен. Также необходим выход в интернет. После открытия приложения
вы выбираете файл-таблицу, для примера можно использовать небольшую таблицу SOKOLOV_SHORT.xlsx .
Далее приложение загружает таблицу и начинает общение с сервером, и выводит полученные результаты в интерфейс. 
В любой момент можно экспортировать полученные данные в виде excel таблицы, или загрузить новый файл.


## ⛏️ Использованные технологии <a name = "tech_stack"></a>

- [PyQt](https://doc.qt.io/qtforpython/) - Qt Framework for python
- [Pandas](https://pandas.pydata.org/) - data analysis tool
- [Requests](https://github.com/psf/requests) - HTTP library
- [multiprocessing](https://docs.python.org/3/library/multiprocessing.html) - Package for processes

## ✍️ Авторы <a name = "authors"></a>

- [@artem-sann](https://github.com/artem-sann) - Idea & Initial work
- [@tiffirg](https://github.com/tiffirg) - API interaction
- [@dgcjcjclb](https://github.com/dgcjcjclb) - UI/UX Design
