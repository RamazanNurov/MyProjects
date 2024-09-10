import sqlite3 as sq
import tkinter as tk
from tkinter import messagebox
from tkinter.ttk import *

class Connect_db:
    def __init__(self, db_name):
        self.db_name = db_name
        self.con = sq.connect(self.db_name)
        self.cursor = self.con.cursor()

    def execute_sql(self, sql_text):
        try:
            self.sql_text = sql_text
            return self.cursor.execute(self.sql_text)
        except:
            messagebox.showerror("Ошибка!", "Невозможно получить данные")

    def close_sql(self):
        self.con.commit()
        self.cursor.close()
        self.con.close()


class My_window:
    def __init__(self):
        self.win = tk.Tk()
        self.win.geometry('900x400')
        self.win.title('СТО')
        self.create_frames()
        self.win.mainloop()

    def update(self,table):
        for row in table.get_children():
            table.delete(row)

        self.new_con = sq.connect('shop.db')

        if table == self.table_tov:
            self.sql = self.new_con.execute(f"SELECT * FROM tovar")
            for row in self.sql:
                self.db_name = row[1]
                self.db_price = row[2]
                self.table_tov.insert("", tk.END, values=[self.db_name, self.db_price])

        self.new_con.close()

    def create_frames(self):
        self.notebook = Notebook()

        style = Style()

        style.configure('TFrame0', background='lightblue')
        self.notebook.pack(expand=True, fill=tk.BOTH)


        self.frame1 = Frame(self.notebook)
        self.frame2 = Frame(self.notebook)
        self.frame3 = Frame(self.notebook)


        self.frame1.pack(fill=tk.BOTH, expand=True)
        self.frame2.pack(fill=tk.BOTH, expand=True)
        self.frame3.pack(fill=tk.BOTH, expand=True)

        self.notebook.add(self.frame1, text="Товары")
        self.notebook.add(self.frame2, text="Купить")
        self.notebook.add(self.frame3, text="Продать")

        self.tovar()
        self.buy()
        self.sell()

    def tovar(self):
        self.table_tov = Treeview(self.frame1, columns=['tovar', 'price'], show='headings')
        self.table_tov.heading('tovar', text='Товар')
        self.table_tov.heading('price', text='Цена')
        self.table_tov.column('tovar', width=150, anchor='c')
        self.table_tov.column('price', width=150, anchor='c')
        self.table_tov.place(x=10, y=10)

        self.tovar_name = tk.StringVar()
        self.lb_name = Label(self.frame1, text='Наименование товара', font='Arial 12', background='lightblue')
        self.lb_name.place(x = 350, y = 20)

        self.entry_name = tk.Entry(self.frame1, textvariable=self.tovar_name, font='Arial 12')
        self.entry_name.place(x=350, y = 60)

        self.tovar_price = tk.DoubleVar()
        self.lb_name = tk.Label(self.frame1, text='Цена товара', font='Arial 12', background='lightblue')
        self.lb_name.place(x = 350, y = 100)

        self.entry_price = tk.Entry(self.frame1, textvariable=self.tovar_price, font='Arial 12')
        self.entry_price.place(x=350, y = 140)

        self.btn_new_tov = tk.Button(self.frame1, text='Добавить новый товар',)
        self.btn_new_tov.place(x=600, y=60)

        self.btn_delete_tov = tk.Button(self.frame1, text='Удалить товар')
        self.btn_delete_tov.place(x=600, y=100)

        self.btn_update_tov = tk.Button(self.frame1, text='Изменить товар')
        self.btn_update_tov.place(x=600, y=140)

        self.update(self.table_tov)

    def select_tov(self):
        pass


new_win = My_window()
