Лабораторная работа №3. Работа с SQLite в PyQt5

Выполнил: Козлов Олег Антонович, гр. 6231-010402D

Файлы проекта:

Lab3.py - главное окно приложения, подключение SQLite и SQL-запросы

lab3.db - тестовая база данных SQLite

Запуск:

python Lab3.py

Описание файла Lab3.py

Функциональность:
Set connection - выбор и открытие SQLite-базы через QFileDialog;

Close connection - закрытие подключения и очистка таблиц;

Tab1 - таблица sqlite_master после подключения;

Tab2 - результат запроса SELECT name FROM sqlite_master;

Tab3 - результат запроса по выбранной таблице и колонке;

Tab4 - вывод структуры выбранной таблицы;

Tab5 - вывод первых записей выбранной таблицы.

Описание файла lab3.db

lab3.db - тестовая база данных SQLite для демонстрации работы программы.
В базе данных созданы три таблицы, одно представление и один индекс:

students - сведения о студентах: идентификатор, ФИО, группа и оценка.

subjects - учебные дисциплины и преподаватели.

grades - результаты студентов по дисциплинам.

student_results - представление с объединённой информацией о студенте,
группе, дисциплине и балле.

idx_grades_student - индекс для ускорения поиска оценок по студенту

Изображение окна:

<img width="1278" height="474" alt="image" src="https://github.com/user-attachments/assets/9a00becc-8685-4db3-bbe4-6c6b5fd2c5c2" />

<img width="1265" height="471" alt="image" src="https://github.com/user-attachments/assets/dc4cb30e-c2f8-4204-8878-8795f1bccc07" />

<img width="1264" height="431" alt="image" src="https://github.com/user-attachments/assets/c18adb1d-b5af-4579-b6b5-8f18f6c93d5c" />

<img width="1258" height="433" alt="image" src="https://github.com/user-attachments/assets/163d141c-57c5-4da9-adbe-ed4bed23a0c3" />

<img width="1270" height="429" alt="image" src="https://github.com/user-attachments/assets/c9169919-801a-4236-873e-414ebae0b536" />
