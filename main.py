import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

DATA_FILE = 'books.json'

# Загрузка данных из файла
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []

# Сохранение данных
def save_data():
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(books, f, ensure_ascii=False, indent=4)

# Проверка заполненности полей
def validate_fields():
    if not title_entry.get().strip():
        messagebox.showerror("Ошибка", "Введите название книги")
        return False
    if not author_entry.get().strip():
        messagebox.showerror("Ошибка", "Введите автора")
        return False
    if not genre_entry.get().strip():
        messagebox.showerror("Ошибка", "Введите жанр")
        return False
    pages = pages_entry.get().strip()
    if not pages.isdigit():
        messagebox.showerror("Ошибка", "Количество страниц должно быть числом")
        return False
    return True

# Добавление книги
def add_book():
    if not validate_fields():
        return
    book = {
        'title': title_entry.get().strip(),
        'author': author_entry.get().strip(),
        'genre': genre_entry.get().strip(),
        'pages': int(pages_entry.get().strip())
    }
    books.append(book)
    refresh_table()
    clear_fields()

# Очистка полей
def clear_fields():
    title_entry.delete(0, tk.END)
    author_entry.delete(0, tk.END)
    genre_entry.delete(0, tk.END)
    pages_entry.delete(0, tk.END)

# Обновление таблицы
def refresh_table(filtered_list=None):
    for row in tree.get_children():
        tree.delete(row)
    data = filtered_list if filtered_list is not None else books
    for b in data:
        tree.insert('', tk.END, values=(b['title'], b['author'], b['genre'], b['pages']))

# Фильтрация
def apply_filter():
    genre_filter = genre_filter_entry.get().strip().lower()
    pages_filter = pages_filter_entry.get().strip()
    filtered = books
    if genre_filter:
        filtered = [b for b in filtered if b['genre'].lower() == genre_filter]
    if pages_filter:
        if not pages_filter.isdigit():
            messagebox.showerror("Ошибка", "Количество страниц для фильтра должно быть числом")
            return
        pages_num = int(pages_filter)
        filtered = [b for b in filtered if b['pages'] > pages_num]
    refresh_table(filtered)

# Загрузка данных при запуске
books = load_data()

# Создаем окно
root = tk.Tk()
root.title("Book Tracker")

# Поля для ввода
tk.Label(root, text="Название книги").grid(row=0, column=0, padx=5, pady=5)
title_entry = tk.Entry(root)
title_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(root, text="Автор").grid(row=1, column=0, padx=5, pady=5)
author_entry = tk.Entry(root)
author_entry.grid(row=1, column=1, padx=5, pady=5)

tk.Label(root, text="Жанр").grid(row=2, column=0, padx=5, pady=5)
genre_entry = tk.Entry(root)
genre_entry.grid(row=2, column=1, padx=5, pady=5)

tk.Label(root, text="Количество страниц").grid(row=3, column=0, padx=5, pady=5)
pages_entry = tk.Entry(root)
pages_entry.grid(row=3, column=1, padx=5, pady=5)

btn_add = tk.Button(root, text="Добавить книгу", command=add_book)
btn_add.grid(row=4, column=0, columnspan=2, pady=10)

# Таблица с книгами
columns = ('title', 'author', 'genre', 'pages')
tree = ttk.Treeview(root, columns=columns, show='headings')
for col in columns:
    tree.heading(col, text=col.capitalize())
tree.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

# Фильтр
filter_frame = tk.Frame(root)
filter_frame.grid(row=6, column=0, columnspan=2, pady=10)

tk.Label(filter_frame, text="Фильтр по жанру").grid(row=0, column=0, padx=5)
genre_filter_entry = tk.Entry(filter_frame)
genre_filter_entry.grid(row=0, column=1, padx=5)

tk.Label(filter_frame, text="Показать книги с страниц >").grid(row=0, column=2, padx=5)
pages_filter_entry = tk.Entry(filter_frame)
pages_filter_entry.grid(row=0, column=3, padx=5)

btn_filter = tk.Button(filter_frame, text="Применить фильтр", command=apply_filter)
btn_filter.grid(row=0, column=4, padx=5)

# Выход и сохранение
def on_closing():
    save_data()
    root.destroy()

refresh_table()
root.protocol("WM_DELETE_WINDOW", on_closing)

root.mainloop()
