import pandas as pd
import datetime
import os

now = datetime.datetime.now()

def read_notes():
    data = pd.read_csv("notes.csv", sep=';')
    return data

def print_notes(data_start=None, data_finish=None):
    data = read_notes()
    if data_start:
        data = data[data['last_change'] >= data_start]
    if data_finish:
        data = data[data['last_change'] <= data_finish]
    print(data.head(10))


class Note:
    def __init__(self):
        self.data = dict()

    def add(self, title, body):
        self.data['id'] = 0
        self.data['title'] = title
        self.data['body'] = body
        self.data['last_change'] = now.strftime("%d-%m-%Y %H:%M")

    def save(self):
        if not os.path.exists('notes.csv'):
            self.data['id'] = 1
            header = True
        else:
            self.data['id'] = read_notes().shape[0]+1
            header = False
        df = pd.DataFrame([self.data])
        df.to_csv('notes.csv', mode='a', index=False, header=header, sep=';')

    @staticmethod
    def edit(edit_id, title=None, body=None):
        all_notes = read_notes()
        if title:
            all_notes.loc[(all_notes['id'] == edit_id), 'title'] = title
        if body:
            all_notes.loc[(all_notes['id'] == edit_id), 'body'] = body
        all_notes.loc[(all_notes['id'] == edit_id), 'last_change'] = now.strftime("%d-%m-%Y %H:%M")
        all_notes.to_csv('notes.csv', mode='w', index=False, header=True, sep=';')
        print(f'Заметка {edit_id} успешно изменена')

    @staticmethod
    def delete(del_id):
        all_notes = read_notes()
        if del_id > all_notes.shape[0]:
            print('Нет заметки с таким номером!')
        else:
            all_notes_new = all_notes[all_notes['id'] != del_id]
            all_notes_new.reset_index(drop= True , inplace= True)
            for i in range(all_notes_new.shape[0]):
                all_notes_new.loc[i, 'id'] = i+1
            all_notes_new.to_csv('notes.csv', mode='w', index=False, header=True, sep=';')
            print(f'Заметка {del_id} успешно удалена')


def create():
    note_1 = Note()
    print(note_1.add('first one', 'kkkkk'))
    note_2 = Note()
    note_1.save()
    note_2.add('second one', 'ffff')
    note_2.save()
    note_2.edit('nnnnn','jjjjjj')

# create()
# create()
# create()
# Note.delete(1)
# print_notes("07-02-2023", "09-02-2023")


while True:
    print('====================\n'
          'Возможные команды:\n'
          'add - создание заметки\n'
          'edit id - редактирование заметки с номером  id\n'
          'print_all - вывести все заметки\n'
          'print DD-MM-YYYY DD-MM-YYYY - вывести все заметки с фильтром с даты1 до даты2\n'
          'delete id - удалить заметку с номером id\n'
          'exit - выход из приложения\n'
          '====================')
    print('Введите команду:')
    comand = input().split()
    try:
        if comand[0] == 'add':
            note_1 = Note()
            title = input('Введите заголовок заметки:')
            body = input('Введите тело заметки:')
            note_1.add(title, body)
            note_1.save()
            print('Заметка успешно сохранена')
        elif comand[0] == 'edit':
            ans_1 = input('Изменить заголовок? Y/n\n')
            if ans_1 == 'Y':
                title = input('Введите новый заголовок заметки:')
                ans_2 = input('Изменить тело заметки? Y/n\n')
                if ans_2 == 'Y':
                    body = input('Введите новое тело заметки:')
                    Note.edit(int(comand[1]), title, body)
                else:
                    Note.edit(int(comand[1]), title)
            else:
                ans_2 = input('Изменить тело заметки? Y/n\n')
                if ans_2 == 'Y':
                    body = input('Введите новое тело заметки:')
                    Note.edit(int(comand[1]), None, body)
                else:
                    Note.edit(f'Заметка {int(comand[1]) } осталась без изменений')
        elif comand[0] == 'print_all':
            print_notes()
        elif comand[0] == 'print':
            if len(comand) == 2:
                print_notes(comand[1])
            else:
                print_notes(comand[1], comand[2])
        elif comand[0] == 'delete':
            Note.delete(int(comand[1]))
        elif comand[0] == 'exit':
            break
        else:
            print('Неверная команда')
    except:
        print('Неверная команда')

print('Завершение работы приложения.')