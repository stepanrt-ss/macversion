import os
import sys
import time

import requests
import string
import random
import json
import telebot
import ua_generator
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from faker import Faker
from concurrent.futures import ThreadPoolExecutor

import get_paths_function_reg

attempts_for_response = 0
found_numbers = 0
sucsesful = 0
invalid_account = 0
mails_for_regestration = []
number_list = []
botEx = telebot.TeleBot('6516240750:AAHHSC0BlT4xloCif5DP-45NoHBVbQ9Ogtk')
bot2 = telebot.TeleBot('7076742172:AAHXae2zRAvlUrin_yo4vrpD35DESjwJyOU')

path_to_dir = os.path.dirname(sys.executable)

# >>> Ввод имени (ФОРМА РЕГИСТРИАЦИИ)
xpath_entry_FirstName = get_paths_function_reg.get_path('xpath_entry_FirstName')

# >>> Ввод фамилии (ФОРМА РЕГИСТРАЦИИ)
xpath_entry_SecondName = get_paths_function_reg.get_path('xpath_entry_SecondName')

# >>> Ввод дня рождения (ФОРМА РЕГИСТРАЦИИ)
xpath_entry_birthDay = get_paths_function_reg.get_path('xpath_entry_birthDay')

# >>> Ввод паролья (ФОРМА РЕГИСТРАЦИИ)
xpath_entry_password = get_paths_function_reg.get_path('xpath_entry_password')

# >>> Ввод подтверждения пароль (ФОРМА РЕГИСТРАЦИИ)
xpath_entry_passwordTwo = get_paths_function_reg.get_path('xpath_entry_passwordTwo')

# >>> Ввод почты (ФОРМА РЕГИСТРАЦИИ)
xpath_entry_Email = get_paths_function_reg.get_path('xpath_entry_Email')

# >>> Подтвердить данные для регистрации (ФОРМА РЕГИСТРАЦИИ)
xpath_accpet_registration = get_paths_function_reg.get_path('xpath_accpet_registration')

# >>> Переход на сайт после регистрации (ФОРМА РЕГИСТРАЦИИ)
xpath_btn_next = get_paths_function_reg.get_path('xpath_btn_next')

# >>> Ввод номера телефона

# >>> Кнопка войти (ГЛАВНАЯ СТРАНИЦА ММ)
xpath_entrance = get_paths_function_reg.get_path('xpath_entrance')

auth_with_sberID_btn_path = get_paths_function_reg.get_path('auth_with_sberID_btn_path')

# >>> Ввод номера телефона для регистрации
xpath_entry_number = get_paths_function_reg.get_path('xpath_entry_number')

# >>> Подтверждение введеного номера телефона для регистрации
xpath_entry_number_accept_btn = get_paths_function_reg.get_path('xpath_entry_number_accept_btn')

xpath_entry_verification = get_paths_function_reg.get_path('xpath_entry_verification')


# >>> Прогрев

# Кнопка купить в карточке товара
buy_btn_path = get_paths_function_reg.get_path('buy_btn_path')

# Кнопка перейти в корзину в карточке товара

go_to_cors_list_path = get_paths_function_reg.get_path('go_to_cors_list_path')

# Кнопка оформить заказ

go_to_order_create_path = get_paths_function_reg.get_path('go_to_order_create_path')
# Предложение об оформлении карты

cancle_window_path = get_paths_function_reg.get_path('cancle_window_path')

# Ввод адреса

entry_addres_path = get_paths_function_reg.get_path('entry_addres_path')

# Выбор способа оплаты

sber_pay_span_path = get_paths_function_reg.get_path('sber_pay_span_path')

cancle_order_path = get_paths_function_reg.get_path('cancle_order_path')

reason_cancel_path = get_paths_function_reg.get_path('reason_cancel_path')

accept_btn_cancel_order_path = get_paths_function_reg.get_path('accept_btn_cancel_order_path')

entry_entrance_path = get_paths_function_reg.get_path('entry_entrance_path')

entry_floor_path = get_paths_function_reg.get_path('entry_floor_path')

entry_block_path = get_paths_function_reg.get_path('entry_block_path')

entry_domofon_path = get_paths_function_reg.get_path('entry_domofon_path')

on_sber_bonus_path = get_paths_function_reg.get_path('on_sber_bonus_path')

accept_on_sber_bonus_path = get_paths_function_reg.get_path('accept_on_sber_bonus_path')

google_btn = get_paths_function_reg.get_path('google_btn')

sber_pay_buy_path = get_paths_function_reg.get_path('sber_pay_buy_path')

input_change_adres_locate_path = get_paths_function_reg.get_path('input_change_adres_locate_path')

take_menu_adres_click = get_paths_function_reg.get_path('take_menu_adres_click')

accept_change_adres_locate_path = get_paths_function_reg.get_path('accept_change_adres_locate_path')

url = 'https://smshub.org/stubs/handler_api.php'
proxy = {
    'http': 'http://BGLMPt:HamYYZ@46.3.185.122:8000',
    'https': 'http://BGLMPt:HamYYZ@46.3.185.122:8000'
}
proxy_attempts = None
proxy_list = []
proxy_host = None
proxy_port = None
proxy_password = None
proxy_username = None

def generate_data():
    russian_letters = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
    random_letters = ''.join(random.choices(russian_letters, k=2))
    random_digits = ''.join(random.choices(string.digits, k=2))
    data = random_letters + random_digits
    return data


def click_func(driver, path, time_check):
    for by, selector in path:
        try:
            button = WebDriverWait(driver, time_check).until(EC.element_to_be_clickable((by, selector)))
            button.click()
            break
        except:
            print(f'Ошибка в кнопке {path} {by}\n пробуем нажать другим способом')
    else:
        print('ERROR ### ERROR ### ERROR ### ERROR ### ERROR\n'
              'Все способы были провалены. Для продолжения работы с программой обратитесь к скриптеру')


def send_keys_func(driver, path, time_check, data):
    for by, selector in path:
        try:
            send_keys = WebDriverWait(driver, time_check).until(EC.element_to_be_clickable((by, selector)))
            if path == entry_addres_path:
                send_keys.send_keys(data)
                time.sleep(1)
                send_keys.send_keys(Keys.TAB)
                break
            else:
                send_keys.send_keys(data)
                break
        except:
            print(f'Ошибка в вводе данных {path} {by}\n пробуем ввести другим способом')
    else:
        print('ERROR ### ERROR ### ERROR ### ERROR ### ERROR\n'
              'Все способы были провалены. Для продолжения работы с программой обратитесь к скриптеру')


def telegram_send_message(user_n, type_message, message_data):
    print(user_n)
    with open(f'{path_to_dir}/mainData/smm_auto_reg_setting.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        telegram_api = data['telegram_api']
    if telegram_api == "":
        pass
    else:
        bot = telebot.TeleBot(telegram_api)
        if type_message == 'account_data':
            try:
                message = message_data
                cook = message[0]
                mail = message[1]
                password = message[2]
                first_name = message[3]
                second_name = message[4]
                bot.send_message(int(user_n),
                                 f'Аккаунт: {cook}\n\nПароль: {password}\nПочта: {mail}\n\nИмя: {first_name}\nФамилия: {second_name}')
            except Exception as ex:
                print(ex)
        elif type_message == 'nvalid_photo':
            try:
                photo = open('nvalid.png', 'rb')
                bot.send_photo(int(user_n), photo, caption=f'Аккаунт: {message_data}\n\nПеремещен в невалид')
            except Exception as ex:
                print(ex)
        elif type_message == 'test':
            bot.send_message(int(user_n), 'Я боб')


def start_registrarion(num, user_n, m):
    global invalid_account

    # >>> Чтение настроек
    with open(f'{path_to_dir}/mainData/smm_auto_reg_setting.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        url_bag = data['url_bag']
        adres_bag = data['adres_bag']
        way_to_cookies = data['way_to_cookies']
        way_to_dont_grev_cookies = data['way_to_dont_grev_cookies']
        use_grev = data['use_grev']
        use_rand_mails = data['use_rand_mails']
        use_activate_sber_spasibo = data['use_activate_sber_spasibo']
        use_txt_proxy = data['use_txt_proxy']
        use_mobile_proxy = data['use_mobile_proxy']
        link_change_mobile_proxy = data['link_change_mobile_proxy']

    def get_chromedriver():
        options = webdriver.ChromeOptions()
        ua = ua_generator.generate(device='desktop', browser='chrome')
        prefs = {"profile.default_content_setting_values.notifications": 2}
        options.add_argument(f'user-agent={ua}')
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--allow-running-insecure-content")
        options.add_argument("--enable-automation")
        options.add_argument("--disable-infobars")
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-save-password-bubble")
        options.add_argument("--disable-translate")
        options.add_argument("--disable-offer-upload-credit-cards")
        print(ua)
        options.add_experimental_option("prefs", prefs)
        options.page_load_strategy = 'eager'

        # >>> Добавление прокси в браузер
        if use_txt_proxy == 'True':
            PROXY = f'{proxy_host}:{proxy_port}'
            options.add_argument('--proxy-server=%s' % PROXY)
            options.add_extension('proxt_auto_auth.crx')

        if use_mobile_proxy == 'True':
            PROXY = f'{proxy_host}:{proxy_port}'
            options.add_argument('--proxy-server=%s' % PROXY)
            options.add_extension('proxt_auto_auth.crx')

        driver = webdriver.Chrome(options=options)
        return driver

    print(num)

    # >>> Настройки браузера
    try:
        driver = get_chromedriver()
    except Exception as ex:
        botEx.send_message(882124917, f'Ошибка у пользователя {user_n}\n{ex}\n СТРОКА 231 VirtualNumbers')
        botEx.send_message(5203489590, f'Ошибка у пользователя {user_n}\n{ex}\n СТРОКА 231 VirtualNumbers')
        print(ex)
        return

    # >>> Блок создания переменной для используемого номера
    try:
        to_droch = num
        number = num
    except Exception as ex:
        botEx.send_message(882124917, f'Ошибка у пользователя {user_n}\n{ex}\n СТРОКА 244 VirtualNumbers')
        botEx.send_message(5203489590, f'Ошибка у пользователя {user_n}\n{ex}\n СТРОКА 244 VirtualNumbers')
        print(ex)
        driver.close()
        return

    # >>> Блок авторизации в прокси
    if use_txt_proxy == 'True' or use_mobile_proxy == 'True':

        driver.get('chrome-extension://ggmdpepbjljkkkdaklfihhngmmgmpggp/options.html')
        tabs = driver.window_handles
        driver.switch_to.window(tabs[0])
        driver.set_window_size(1920, 1080)
        time.sleep(2)
        driver.refresh()
        try:
            input_proxy_login = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#login')))
            input_proxy_login.send_keys(f'{proxy_username}')
        except Exception as ex:
            print(ex)

        try:
            input_proxy_password = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '#password')))
            input_proxy_password.send_keys(f'{proxy_password}')
        except Exception as ex:
            print(ex)

        try:
            accept_proxy_settings = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '#save')))
            accept_proxy_settings.click()
        except Exception as ex:
            print(ex)
    else:
        pass

    if use_mobile_proxy == 'True':
        while True:
            url_change_proxy = f'{link_change_mobile_proxy}'

            response = requests.get(url_change_proxy)
            if response.status_code == 200:
                print('Поменялся')
                break
            else:
                print('Не поменялся')
    else:
        pass

    driver.refresh()
    time.sleep(0.5)
    driver.refresh()

    if use_mobile_proxy == 'False':
        # >>> Блок откртия Google для обхода капчи
        try:
            driver.get('https://www.google.ru/')
            time.sleep(2)
            driver.set_window_size(1920, 1080)
            try:
                tring = "//div[text()='Accept all']"
                trs = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, tring)))
                trs.click()
            except:
                pass
            click_func(driver, google_btn, 10)
            time.sleep(5)
            driver.get('https://www.google.com/search?q=%D0%BC%D0%B5%D0%B3%D0%B0%D0%BC%D0%B0%D1%80%D0%BA%D0%B5%D1%82&oq=%D0%BC%D0%B5%D0%B3%D0%B0%D0%BC%D0%B0%D1%80%D0%BA%D0%B5%D1%82&gs_lcrp=EgZjaHJvbWUyBggAEEUYOdIBCDI5NDdqMGo0qAIAsAIA&sourceid=chrome&ie=UTF-8')
            try:
                tring = "//div[text()='Accept all']"
                trs = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, tring)))
                trs.click()
            except:
                pass
            path = "//*[contains(text(), 'Мегамаркет')]"
            elements = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, path)))
            elements.click()

        except:
            pass
    else:
        pass

    if use_mobile_proxy == 'True':
        driver.get('https://megamarket.ru/')
    else:
        pass

    time.sleep(15)

    click_func(driver, xpath_entrance, 10)

    # >>> Проверка наличия капчи на сайте
    html_check_valid = driver.page_source
    soup_check_valid = BeautifulSoup(html_check_valid, 'html.parser')
    status_elements_order = soup_check_valid.find_all(class_='header-profile-actions')
    statuses_check_valid = [status.get_text(strip=True) for status in status_elements_order]
    status_valid = statuses_check_valid
    print(status_valid)
    if len(status_valid) != 0:
        print('капчи нет')
    else:
        print('Капча')
        print(to_droch)
        driver.close()
        do_droch(to_droch, user_n, m)
        time.sleep(5)
        return

    # >>> Блок ввода номера телефона

    click_func(driver, auth_with_sberID_btn_path, 10)

    send_keys_func(driver, xpath_entry_number, 10, number)
    click_func(driver, xpath_entry_number_accept_btn, 10)

    # >>> Блок генерации данных для регистрации
    try:
        fake = Faker('ru_RU')
        f_name = fake.first_name_male()
        s_name = fake.last_name_male()
        day = random.randint(10, 27)
        month = random.randint(10, 12)
        year = random.randint(1981, 2003)
        rand_simbols = ''.join(random.choices(string.ascii_letters + string.digits, k=random.randint(11, 13)))
        f_psw = fake.password(19) + '-'
        rand_email = rand_simbols + '@' + 'rumbler.ru'
        birth = (str(day) + str(month) + str(year))
    except Exception as ex:
        botEx.send_message(882124917, f'Ошибка у пользователя {user_n}\n{ex}\n СТРОКА 393 VirtualNumbers')
        botEx.send_message(5203489590, f'Ошибка у пользователя {user_n}\n{ex}\n СТРОКА 393 VirtualNumbers')
        print(ex)
        driver.close()
        return

    # >>> Блок ввода данных для регистрации
    try:
        send_keys_func(driver, xpath_entry_FirstName, 999, f_name)
        send_keys_func(driver, xpath_entry_SecondName, 10, s_name)
        send_keys_func(driver, xpath_entry_birthDay, 10, birth)
        send_keys_func(driver, xpath_entry_password, 10, f_psw)
        send_keys_func(driver, xpath_entry_passwordTwo, 10, f_psw)
        # >>> Отправка данных в файл + бота [Рандомные почты]
        if use_rand_mails == 'True':
            send_keys_func(driver, xpath_entry_Email, 10, rand_email)
            t = open('accounts.txt', 'r', encoding='utf-8')
            if t == '':
                with open('accounts.txt', 'w', encoding='utf-8') as f:
                    f.write(f'{number}  {rand_email}\n')
            else:
                with open('accounts.txt', 'a', encoding='utf-8') as f:
                    f.write(f'{number}  {rand_email}\n')
            # >>> Отправка данных в бота
            try:
                type_message = 'account_data'
                message_data = [f'{num}', f'{rand_email}', f'{f_psw}', f'{f_name}', f'{s_name}']
                telegram_send_message(user_n, type_message, message_data)
            except:
                pass
        # >>> Отправка данных в файл + бота [Свои почты]
        else:
            send_keys_func(driver, xpath_entry_Email, 10, m)
            # >>> Запись данных в файл
            t = open('accounts.txt', 'r', encoding='utf-8')
            if t == '':
                with open('accounts.txt', 'w', encoding='utf-8') as f:
                    f.write(f'{number}  {m}')
            else:
                with open('accounts.txt', 'a', encoding='utf-8') as f:
                    f.write(f'{number}  {m}')
            # >>> Отправка данных в бота
            try:
                type_message = 'account_data'
                message_data = [f'{num}', f'{m}', f'{f_psw}', f'{f_name}', f'{s_name}']
                telegram_send_message(user_n, type_message, message_data)
            except Exception as ex:
                print(ex)

        click_func(driver, xpath_accpet_registration, 10)
        click_func(driver, xpath_btn_next, 10)
    except Exception as ex:
        invalid_account += 1 ### СДЕЛАТЬ ПРОВЕРКУ ЧЕРЕЗ BS4
        botEx.send_message(882124917, f'Ошибка у пользователя {user_n}\n{ex}\n СТРОКА 463 VirtualNumbers\nНевалидный аккаунт, после регестрации нет кнопки завершить или аккаунт уже зарегестрирован')
        botEx.send_message(5203489590, f'Ошибка у пользователя {user_n}\n{ex}\n СТРОКА 463 VirtualNumbers\nНевалидный аккаунт, после регестрации нет кнопки завершить или аккаунт уже зарегестрирован')
        print(ex)
        driver.close()
        return

    # >>> Блок создания файла с cookies
    try:
        time.sleep(10)
        cookies = driver.get_cookies()
        for cookie in cookies:
            if 'sameSite' in cookie:
                cookie['sameSite'] = 'lax'
        with open(f'{way_to_dont_grev_cookies}/{number}.json', 'w', encoding='utf-8') as file:
            json.dump(cookies, file)
        time.sleep(2)
    except Exception as ex:
        print(ex)
        botEx.send_message(882124917, f'Ошибка у пользователя {user_n}\n{ex}\n СТРОКА 481 VirtualNumbers')
        botEx.send_message(5203489590, f'Ошибка у пользователя {user_n}\n{ex}\n СТРОКА 481 VirtualNumbers')
        driver.close()
        return

    # >>> Блок включения сберспасибо
    if use_activate_sber_spasibo == 'True':
        driver.get('https://megamarket.ru/personal/loyalty')
        click_func(driver, on_sber_bonus_path, 10)
        click_func(driver, accept_on_sber_bonus_path, 10)
        time.sleep(2)
    else:
        pass

    try:
        driver.get('https://megamarket.ru/personal/address/add/')
    except Exception as ex:
        print(ex)

    send_keys_func(driver, input_change_adres_locate_path, 10, adres_bag)
    click_func(driver, take_menu_adres_click, 10)
    click_func(driver, accept_change_adres_locate_path, 10)
    time.sleep(3)

    # >>> Блок прогрева
    if use_grev == 'False':
        driver.get(f'{url_bag}')
        time.sleep(10)

        # >>> Купить
        click_func(driver, buy_btn_path, 10)

        # >>> Перейти в корзину
        click_func(driver, go_to_cors_list_path, 10)

        # >>> Перейти к созданию заказа
        click_func(driver, go_to_order_create_path, 10)

        # >>> Всплывающие окно
        click_func(driver, cancle_window_path, 10)

        # >>> Ввод входа
        entrance = generate_data()
        send_keys_func(driver, entry_entrance_path, 10, entrance)

        # >>> Ввод этажа
        floor = generate_data()
        send_keys_func(driver, entry_floor_path, 10, floor)

        # >>> Ввод квартиры
        block = generate_data()
        send_keys_func(driver, entry_block_path, 10, block)

        # >>> Ввод домофона
        domofon = generate_data()
        send_keys_func(driver, entry_domofon_path, 10, domofon)

        # >>> Способ оплаты = SberPay
        click_func(driver, sber_pay_span_path, 10)



        try:
            click_func(driver, sber_pay_buy_path, 10)
            time.sleep(5)
        except:
            os.remove(f'{way_to_dont_grev_cookies}/{number}.json')
            cookies = driver.get_cookies()
            for cookie in cookies:
                if 'sameSite' in cookie:
                    cookie['sameSite'] = 'lax'
            with open(f'{way_to_dont_grev_cookies}/{number}.json', 'w', encoding='utf-8') as file:
                json.dump(cookies, file)
            time.sleep(3)
            driver.close()
            return


        while True:
            try:
                driver.get('https://megamarket.ru/personal/order/#?orderFilter=ORDER_FILTER_NOT_HIDDEN')
                driver.refresh()
                time.sleep(10)
                html_orders = driver.page_source
                soup_order = BeautifulSoup(html_orders, 'html.parser')
                status_elements_order = soup_order.find_all(class_='order-delivery-status')
                statuses = [status.get_text(strip=True) for status in status_elements_order]
                order_status = statuses
                if order_status[0] == 'Заказ создан':
                    break
                else:
                    pass
            except Exception as ex:
                print(ex)

        driver.get('https://megamarket.ru/personal/order/#?orderFilter=ORDER_FILTER_NOT_HIDDEN')
        time.sleep(5)

        click_func(driver, cancle_order_path, 10)
        click_func(driver, reason_cancel_path, 10)
        click_func(driver, accept_btn_cancel_order_path, 10)

        time.sleep(5)
        os.remove(f'{way_to_dont_grev_cookies}/{number}.json')
        cookies = driver.get_cookies()
        for cookie in cookies:
            if 'sameSite' in cookie:
                cookie['sameSite'] = 'lax'
        with open(f'{way_to_cookies}/{number}.json', 'w', encoding='utf-8') as file:
            json.dump(cookies, file)
        time.sleep(10)
    else:
        pass


def Pool(user_n):
    global proxy_list
    global number_list
    global mails_for_regestration

    with open(f'{path_to_dir}/mainData/smm_auto_reg_setting.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        pool_value = data['pool_value']
        use_txt_proxy = data['use_txt_proxy']

        way_to_uses_txt_proxy = data['way_to_uses_txt_proxy']
        way_to_txt_proxy = data['way_to_txt_proxy']
        use_mobile_proxy = data['use_mobile_proxy']
        mobile_proxy = data['mobile_proxy']
        you_numbers = data['you_numbers']
        number_list = you_numbers.split('\n')
        mails = data['mails']
        use_rand_mails = data['use_rand_mails']
        mails_for_regestration = mails.split('\n')

        if use_txt_proxy == 'True':
            with open(f'{way_to_txt_proxy}', 'r') as f:
                proxy = f.read()
                proxy_list = proxy.split('\n')
                print(proxy_list)
        else:
            pass

    def process_number(num):
        if use_rand_mails == 'False':
            m = mails_for_regestration[0]
            del mails_for_regestration[0]
        else:
            m = 'Don`t used'
        start_registrarion(num, user_n, m)

    try:
        with ThreadPoolExecutor(max_workers=int(pool_value)) as executor:
            for num in number_list:
                if use_txt_proxy == 'True':
                    global proxy_attempts, proxy_host, proxy_port, proxy_username, proxy_password
                    if use_txt_proxy == 'True':
                        global proxy_host, proxy_port, proxy_username, proxy_password
                        proxy_get = proxy_list[0]
                        b = proxy_get.split(':')
                        # Настройка прокси
                        proxy_host = b[0]
                        proxy_port = b[1]
                        proxy_username = b[2]
                        proxy_password = b[3]
                        del proxy_list[0]
                        a = open(f'{way_to_uses_txt_proxy}', 'r', encoding='utf-8')
                        if a == '':
                            with open(f'{way_to_uses_txt_proxy}', 'w', encoding='utf-8') as f:
                                f.write(proxy + '\n')
                        else:
                            with open(f'{way_to_uses_txt_proxy}', 'a', encoding='utf-8') as f:
                                f.write(proxy + '\n')
                        a.close()
                    elif use_mobile_proxy == 'True':
                        data = mobile_proxy.split(':')
                        proxy_host = data[0]
                        proxy_port = data[1]
                        proxy_username = data[2]
                        proxy_password = data[3]
                    else:
                        pass
                executor.submit(process_number, num)
                time.sleep(5)  # Добавляем задержку в 3 секунды между вызовами функций
            executor.shutdown(wait=True)
            to_json_result = {'f_num': f'{found_numbers}', 'i_num': f'{invalid_account}', 's_num': f'{sucsesful}'}
            with open('results.json', 'w') as f:
                json.dump(to_json_result, f)
    except Exception as ex:
        print(ex)
        botEx.send_message(882124917, f'Ошибка у пользователя {user_n}\n{ex}\n СТРОКА 874 VirtualNumbers')
        botEx.send_message(5203489590, f'Ошибка у пользователя {user_n}\n{ex}\n СТРОКА 874 VirtualNumbers')
        return

def do_droch(to_droch, user_n, m):
    print('Обход капчи')
    def process_number(to_droch, user_n):
        try:
            num = to_droch
            start_registrarion(num, user_n, m)
        except Exception as ex:
            botEx.send_message(882124917, f'Ошибка у пользователя {user_n}\n{ex}\n СТРОКА 885 VirtualNumbers')
            botEx.send_message(5203489590, f'Ошибка у пользователя {user_n}\n{ex}\n СТРОКА 885 VirtualNumbers')
    try:
        with ThreadPoolExecutor(max_workers=1) as executor:
            executor.submit(process_number, to_droch, user_n)
            time.sleep(3)
    except Exception as ex:
        botEx.send_message(882124917, f'Ошибка у пользователя {user_n}\n{ex}\n СТРОКА 892 VirtualNumbers')
        botEx.send_message(5203489590, f'Ошибка у пользователя {user_n}\n{ex}\n СТРОКА 892 VirtualNumbers')

