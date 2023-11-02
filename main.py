

if __name__ == '__main__':
    import re
    import csv


    # Функция для преобразования номера телефона в нужный формат
    def format_phone(phone):
        phone_pattern = r'(\+7|8)[\s\(]*(\d{3})[\s\)\-]*(\d{3})[\s\-]*(\d{2})[\s\-]*(\d{2})[\s]*(доб\.\s*(\d+))?'
        match = re.match(phone_pattern, phone)
        if match:
            groups = match.groups()
            if groups[6]:
                return f'+7({groups[2]}){groups[3]}-{groups[4]}-{groups[5]} доб.{groups[6]}'
            else:
                return f'+7({groups[2]}){groups[3]}-{groups[4]}-{groups[5]}'
        else:
            return phone


    # Читаем адресную книгу в формате CSV в список contacts_list:
    with open("phonebook_raw.csv") as f:
        rows = csv.reader(f, delimiter=",")
        contacts_list = list(rows)

    # Создаем словарь для хранения уникальных записей, где ключ - это ФИО, а значение - это данные о человеке
    unique_contacts = {}

    # Перебираем записи в contacts_list и обновляем данные в словаре unique_contacts:
    for contact in contacts_list[1:]:  # Пропускаем первую строку с заголовками
        full_name = re.split(r'\s+', contact[0])  # Разбиваем ФИО на части

        lastname, firstname, *surname = full_name  # Разделяем на фамилию, имя и отчество
        surname = ' '.join(surname) if surname else ''  # Отчество может быть пустым
        phone = format_phone(contact[5])  # Преобразуем номер телефона
        email = contact[6]  # Получаем адрес электронной почты
        key = (lastname, firstname, surname)  # Создаем ключ для уникальной идентификации записи

        if key not in unique_contacts:
            # Если записи о человеке с таким ключом еще нет, добавляем ее в словарь
            unique_contacts[key] = {
                'lastname': lastname,
                'firstname': firstname,
                'surname': surname,
                'organization': contact[3],
                'position': contact[4],
                'phone': phone,
                'email': email
            }
        else:
            # Если запись о человеке уже существует, обновляем телефон и e-mail
            unique_contacts[key]['phone'] += ', ' + phone
            unique_contacts[key]['email'] = ', ' + email

    # Преобразуем данные и сохраняем их в новом файле CSV:
    with open("phonebook.csv", "w", newline='') as f:
        fieldnames = ['lastname', 'firstname', 'surname', 'organization', 'position', 'phone', 'email']
        datawriter = csv.DictWriter(f, fieldnames=fieldnames)
        datawriter.writeheader()
        datawriter.writerows(unique_contacts.values())
