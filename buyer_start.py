r""""""
import os
import random
import re
import string
import sys

import time
import json
import pickle

import requests
import telebot
import ua_generator
from concurrent.futures import ThreadPoolExecutor

from bs4 import BeautifulSoup
from faker import Faker
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC

import get_paths_function_aub

# >>> For cookies with sber ID

close_changer_adres_btn_path = get_paths_function_aub.get_path('close_changer_adres_btn_path')

# >>> Кнопка продолжить в сплывающем окне возле кнопки "Войти" (АВТОРИЗАЦИЯ SBERID)
auth_with_sberid_path = get_paths_function_aub.get_path('auth_with_sberid_path')

# >>> Авторизоваться через SBERID
sber_id_btn_path = get_paths_function_aub.get_path('sber_id_btn_path')

# >>> Кнопка продолжить, после загрузки куков (авторизация SBERID)
accept_auth_btn_path = get_paths_function_aub.get_path('accept_auth_btn_path')

# >>> Согласиться с условиями бонусной программы (ПОДКЛЮЧЕНИЕ ЛОЯЛЬНОСТИ)
on_sber_bonus_path = get_paths_function_aub.get_path('on_sber_bonus_path')

# >>> Кнопка "подключить сберспасибо" (ПОДКЛЮЧЕНИЕ ЛОЯЛЬНОСТИ)
accept_on_sber_bonus_path = get_paths_function_aub.get_path('accept_on_sber_bonus_path')


# >>> Нажатие на кнопку "изменить адрес" (в карточке товара)
aleter_adres_locate_path = get_paths_function_aub.get_path('aleter_adres_locate_path')

# >>> Нажать на кнопку "Добавить адрес" (в карточке товара)
change_adres_locate_path = get_paths_function_aub.get_path('change_adres_locate_path')

# >>> Альтернативная кнопка измениения Адреса (в карточке товара)
go_change_adres_locate_btn_path = get_paths_function_aub.get_path('go_change_adres_locate_btn_path')

# >>> Ввод адреса (в карточке товара)
input_change_adres_locate_path = get_paths_function_aub.get_path('input_change_adres_locate_path')

# >>> Выбрать в выпадающем списке адрес доставки (в карточке товара)
take_menu_adres_click = get_paths_function_aub.get_path('take_menu_adres_click')

# >>> Подтвердить изменение адреса (в карточке товара)
accept_change_adres_locate_path = get_paths_function_aub.get_path('accept_change_adres_locate_path')

# >>> Обход 18+ товаров (в карточке товара)
eghteen_check_path = get_paths_function_aub.get_path('eghteen_check_path')

# >>> Нажатие на кнопку куить (в карточке товара)
buy_bag_btn_path = get_paths_function_aub.get_path('buy_bag_btn_path')

# >>> Добавить N кол-во товара (в карточке товара)
plus_product_path = get_paths_function_aub.get_path('plus_product_path')

# >>> Нажатие на кнопку "перейти в корзину" (в карточке товара)
go_to_cors_list_path = get_paths_function_aub.get_path('go_to_cors_list_path')

# >>> Нажатие на оформить заказ (в корзине)
go_to_order_create_path = get_paths_function_aub.get_path('go_to_order_create_path')

# >>> Нажатие на кнопку "закрыть" (в карточке создания заказа)
cancle_window_path = get_paths_function_aub.get_path('cancle_window_path')

# >>> Ввод подъезда (в карточке создания заказа)
entry_entrance_path = get_paths_function_aub.get_path('entry_entrance_path')

# >>> Ввод этажа (в карточке создания заказа)
entry_floor_path = get_paths_function_aub.get_path('entry_floor_path')

# >>> Ввод квартиры (в карточке создания заказа)
entry_block_path = get_paths_function_aub.get_path('entry_block_path')

# >>> Ввод домофона (в карточке создания заказа)
entry_domofon_path = get_paths_function_aub.get_path('entry_domofon_path')

# >>> Ввод коментария к заказку (в карточке создания заказа)
entry_coment_path = get_paths_function_aub.get_path('entry_coment_path')

# >>> Ввод промокода (в карточке создания заказа)
entry_promocode_path = get_paths_function_aub.get_path('entry_promocode_path')

# >>> Нажатие на кнопку применить промокод (в карточке заказа)
entry_promocode_accept_btn = get_paths_function_aub.get_path('entry_promocode_accept_btn')

# >>> Нажатие на кнопку "оплатить sberPay" (в карточке создания заказа)
sber_pay_span_path = get_paths_function_aub.get_path('sber_pay_span_path')

sber_pay_buy_path = get_paths_function_aub.get_path('sber_pay_buy_path')

# >>> Ввод номера для оплаты (ОПЛАТА ЗАКАЗА)
entry_pay_number_path = get_paths_function_aub.get_path('entry_pay_number_path')

# >>> Нажатие на кнопку "перейти к оплате" (ОПЛАТА ЗАКАЗА)
get_qr_code_path = get_paths_function_aub.get_path('get_qr_code_path')

# >>> Нажатие на кнопку "перейти к заказам" (ОПЛАТА ЗАКЗА)
go_to_order_list_path = get_paths_function_aub.get_path('go_to_order_list_path')

# >>> Нажатие на кнопку "хорошо" (ЛИСТ ЗАКАЗОВ)
accept_winodw_on_order_list_path = get_paths_function_aub.get_path('accept_winodw_on_order_list_path')


# >>> Нажатие на кнопку "активные заказы" (ЛИСТ ЗАКАЗОВ)
go_to_active_order_list_path = get_paths_function_aub.get_path('go_to_active_order_list_path')

# >>> Нжатие на карточку заказа (ЛИСТ ЗАКАЗОВ)
go_to_order_cart_path = get_paths_function_aub.get_path('go_to_order_cart_path')

# >>> Нажатие на изменить получателя (КАРТОЧКА ЗАКАЗА)
change_deliv_data_path = get_paths_function_aub.get_path('change_deliv_data_path')

# >>> Замена имени в замене получателя (КАРТОЧКА ЗАКЗА)
change_firts_name_data_path = get_paths_function_aub.get_path('change_firts_name_data_path')

# >>> Замена в замене получателя (КАРТОЧКА ЗАКЗА)
change_last_name_data_path = get_paths_function_aub.get_path('change_last_name_data_path')

# >>> Замена номера телефона в замене получателя (КАРТОЧКА ЗАКАЗА)
change_phone_number_data_path = get_paths_function_aub.get_path('change_phone_number_data_path')

# >>> Нажатие на кнопку подтверить изменение получателя (КАРТОЧКА ЗАКЗА)
change_deliv_data_btn_path = get_paths_function_aub.get_path('change_deliv_data_btn_path')
# >>> Изменение получателя

# >>> Нажатие на кнопку "мне повезет"
google_btn = '/html/body/div[1]/div[3]/form/div[1]/div[1]/div[4]/center/input[2]'


# >>> Лист для хранения всех прокси
proxy_attempts = None
proxy_list = []
proxy_host = None
proxy_port = None
proxy_password = None
proxy_username = None
path_to_dir = os.path.dirname(sys.executable)
print(path_to_dir)


def click_func(driver, path, time_for_check):
    for by, selector in path:
        try:
            button = WebDriverWait(driver, time_for_check).until(EC.element_to_be_clickable((by, selector)))
            button.click()
            break
        except:
            print(f'Ошибка в кнопке {path} {by}\nПробуем нажать другим способом')
    else:
        print('ERROR ### ERROR ### ERROR ### ERROR ### ERROR\n'
              'Все способы были провалены. Для продолжения работы с программой обратитесь к скриптеру')


def send_keys_func(driver, path, time_for_check, data):
    for by, selector in path:
        try:
            send_keys = WebDriverWait(driver, time_for_check).until(EC.element_to_be_clickable((by, selector)))
            send_keys.clear()
            send_keys.send_keys(data)
            break
        except:
            print(f'Ошибка в вводе данных {path} {by}\n пробуем ввести другим способом')
    else:
        print('ERROR ### ERROR ### ERROR ### ERROR ### ERROR\n'
              'Все способы были провалены. Для продолжения работы с программой обратитесь к скриптеру')


def generate_data():
    russian_letters = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
    random_letters = ''.join(random.choices(russian_letters, k=2))
    random_digits = ''.join(random.choices(string.digits, k=2))
    data = random_letters + random_digits
    return data


def send_data_telegram(user_n, type_message, message_data):
    with open(f'{path_to_dir}/mainData/smm_auto_buy_setting.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        telegram_api = data['telegram_api']
    bot = telebot.TeleBot(telegram_api)
    if telegram_api != '':
        if type_message == 'send_dont_grev_screan':
            account_name = message_data[0]
            photo_name = message_data[1]
            photo = open(photo_name, 'rb')
            bot.send_photo(int(user_n), photo, caption=f'Аккаунт: {account_name}\n Аккаунт не прогрет. Cookie перемещен в "Cookies не гретые"')
            photo.close()
            os.remove(photo_name)
        elif type_message == 'send_nvalid_promocode_screan':
            account_name = message_data[0]
            photo_name = message_data[1]
            photo = open(photo_name, 'rb')
            bot.send_photo(int(user_n), photo, caption=f'Аккаунт: {account_name}\nНе валидный промокод. Cookies перемешен в "Cookies в работе"')
            photo.close()
            os.remove(photo_name)
        elif type_message == 'send_scren_qr_code':
            account_name = message_data[0]
            photo_name = message_data[1]
            photo = open(photo_name, 'rb')
            bot.send_photo(int(user_n), photo, caption=f'Аккаунт: {account_name}\n QR Code для оплаты')
            photo.close()
            os.remove(photo_name)
        elif type_message == 'send_dont_change_deliv':
            account_name = message_data[0]
            photo_name = message_data[1]
            photo = open(photo_name, 'rb')
            bot.send_photo(int(user_n), photo, caption=f'Аккаунт: {account_name}\n Нет кнопки "Изменить получателя". Cookies перемещен в "Cookies без замены получателя"')
            photo.close()
            os.remove(photo_name)


def load_cookies(driver, cook_name):
    with open(f'{path_to_dir}/mainData/smm_auto_buy_setting.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        cookies_way = data['cookies_way']
        use_cookies_with_sber_id = data['use_cookies_with_sber_id']

        # >>> Загрузка JSON куков в браузер
        try:
            print('Выгрузка')
            try:
                with open(f'{cookies_way}/{cook_name}', 'r', encoding='utf-8') as f:
                    cookies = json.load(f)
            except json.JSONDecodeError as ex:
                print('Это гологин епта')
                if str(ex) == 'Unexpected UTF-8 BOM (decode using utf-8-sig): line 1 column 1 (char 0)':
                    with open(f'{cookies_way}/{cook_name}', 'r', encoding='utf-8-sig') as f:
                        cookies = json.load(f)

            # >>> Меняем Lax
            for cookie in cookies:
                if 'sameSite' in cookie:
                    cookie['sameSite'] = 'Lax'

            # >>> Вытаскиваем токены
            if use_cookies_with_sber_id == 'True':
                id_user = None
                for cookie in cookies:
                    if cookie.get('name') == 'id_user':
                        id_user = cookie
                        cookies_data = id_user
                        break
            else:
                ecom_token = None
                for cookie in cookies:
                    if cookie.get('name') == 'ecom_token':
                        ecom_token = cookie
                        cookies_data = ecom_token
                        break
            print(cookies_data)

            with open(f'{cook_name}.pkl', 'wb') as f:
                pickle.dump(cookies_data, f)

            with open(f'{cook_name}.pkl', 'rb') as f:
                cookies = pickle.load(f)

            driver.add_cookie(cookies)
            os.remove(f'{cook_name}.pkl')

            print('Выгрузка закончилась')
        except Exception as ex:
            print(ex)


def startAB(cook, list_bag_names, user_n):
    try:
        with open(f'{path_to_dir}/mainData/smm_auto_buy_setting.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            use_txt_proxy = data['use_txt_proxy']
            use_random_adres = data['use_random_adres']
            use_txt_comment = data['use_txt_comment']
            use_txt_promocode = data['use_txt_promocode']
            use_clear_bag = data['use_clear_bag']
            use_check_grev = data['use_check_grev']
            use_on_sber_spas = data['use_on_sber_spas']
            use_cookies_with_sber_id = data['use_cookies_with_sber_id']
            use_random_data_for_deliv = data['use_random_data_for_deliv']
            use_mobile_proxy = data['use_mobile_proxy']
            link_change_mobile_proxy = data['link_change_mobile_proxy']
            use_txt_adres_deliv = data['use_txt_adres_deliv']
            use_promocode_from_lk = data['use_promocode_from_lk']
            use_change_poluchatel_from_link = data['use_change_poluchatel_from_link']

            cookies_way = data['cookies_way']
            cookies_dont_grev_way = data['cookies_dont_grev_way']
            cookies_uses_way = data['cookies_uses_way']
            cookies_in_run_way = data['cookies_in_run_way']
            cookies_dont_change_way = data['cookies_dont_change_way']

            txt_comments_way = data['txt_comments_way']
            txt_promocode_way = data['txt_promocode_way']
            txt_promocode_uses_way = data['txt_promocode_uses_way']
            txt_promocode_nvalid_way = data['txt_promocode_nvalid_way']
            txt_adres_way = data['txt_adres_way']

            fixed_promocode = data['fixed_promocode']
            check_promocode_price = data['check_promocode_price']
            use_check_bonus_value = data['use_check_bonus_value']

            adres_deliv = data['adres_deliv']
            adres_entrance = data['adres_entrance']
            adres_floor = data['adres_floor']
            adres_block = data['adres_block']
            adres_domofon = data['adres_domofon']
            pay_phone = data['pay_phone']

            deliv_first_name = data['deliv_first_name']
            deliv_last_name = data['deliv_last_name']
            deliv_phone = data['deliv_phone']
    except Exception as ex:
        print(ex)

    promocode_from_lk = None
    find_name_cook = cook.split('.')
    cook_name = cook
    cook_type = find_name_cook[1]

    if cook_type == 'txt':
        # Чтение данных из файла и преобразование в JSON
        with open(f'{cookies_way}/{cook_name}', 'r') as file:
            data = file.read()
            json_data = json.loads(data)

        os.remove(f'{cookies_way}/{cook_name}')
        load_txt_cook = cook_name.split('.')
        name_txt_cook = load_txt_cook[0]

        # Запись данных в JSON-файл
        with open(f'{cookies_way}/{name_txt_cook}.json', 'w', encoding='utf-8') as f:
            json.dump(json_data, f, indent=4, ensure_ascii=False)
        cook_name = f'{name_txt_cook}.json'
    i = 0
    o = False
    print('[start]')

    # >>> Настройка драйвера перед запуском

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

        # >>> Функция вызова прокси
        if use_txt_proxy == 'True':
            PROXY = f'{proxy_host}:{proxy_port}'
            options.add_argument('--proxy-server=%s' % PROXY)
            options.add_extension('proxt_auto_auth.crx')
        else:
            pass

        if use_mobile_proxy == 'True':
            PROXY = f'{proxy_host}:{proxy_port}'
            options.add_argument('--proxy-server=%s' % PROXY)
            options.add_extension('proxt_auto_auth.crx')
        else:
            pass

        driver = webdriver.Chrome(options=options)
        return driver

    try:
        driver = get_chromedriver()
    except Exception as ex:
        print(ex)
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
            accept_proxy_settings = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#save')))
            accept_proxy_settings.click()
        except Exception as ex:
            print(ex)

        if use_mobile_proxy == 'True':
            while True:
                url = f'{link_change_mobile_proxy}'

                response = requests.get(url)
                if response.status_code == 200:
                    print('Поменялся')
                    break
                else:
                    print('Не поменялся')
        else:
            pass
    else:
        pass
    if use_mobile_proxy == 'False':
        # >>> Блок откртия Google для обхода капчи
        try:
            driver.get('https://www.google.ru/')
            driver.set_window_size(1920, 1080)
            try:
                tring = "//div[text()='Принять все']"
                trs = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, tring)))
                trs.click()
            except:
                pass
            cap = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, google_btn)))
            cap.click()
            time.sleep(5)
            driver.get(
                'https://www.google.com/search?q=%D0%BC%D0%B5%D0%B3%D0%B0%D0%BC%D0%B0%D1%80%D0%BA%D0%B5%D1%82&oq=%D0%BC%D0%B5%D0%B3%D0%B0%D0%BC%D0%B0%D1%80%D0%BA%D0%B5%D1%82&gs_lcrp=EgZjaHJvbWUyBggAEEUYOdIBCDI5NDdqMGo0qAIAsAIA&sourceid=chrome&ie=UTF-8')
            try:
                tring = "//div[text()='Принять все']"
                trs = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, tring)))
                trs.click()
            except:
                pass
            path = "//*[contains(text(), 'Мегамаркет')]"
            elements = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, path)))
            elements.click()
            time.sleep(15)
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
                time.sleep(5)
                return
        except Exception as ex:
            print(ex)
    else:
        pass

    if use_mobile_proxy == 'True':
        driver.get('https://megamarket.ru/')
        time.sleep(15)
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
            time.sleep(5)
            return
    else:
        pass

    # >>> Нажатие на кнопку авторизоваться
    if use_cookies_with_sber_id == 'True':
        click_func(driver, auth_with_sberid_path, 10)
    else:
        pass

    # >>> Нажатие на кнопку войти по сберID
    if use_cookies_with_sber_id == 'True':
        click_func(driver, sber_id_btn_path, 10)
    else:
        pass

    time.sleep(10)

    load_cookies(driver, cook_name)

    if use_cookies_with_sber_id == 'True':
        driver.refresh()
        time.sleep(1)
    else:
        pass

    # >>> Нажатие на кнопку продолжить
    if use_cookies_with_sber_id == 'True':
        click_func(driver, accept_auth_btn_path, 10)
    else:
        pass

    time.sleep(5)

    if use_promocode_from_lk == 'True':
        # >>> Проверка промокодов на аккаунте
        try:
            driver.get('https://megamarket.ru/personal/promo-codes')
            time.sleep(10)
            html_promocodes = driver.page_source
            soup_promocode = BeautifulSoup(html_promocodes, 'html.parser')
            status_elements_promocode = soup_promocode.find_all(class_='c-button__content')
            promo_values = [status.get_text(strip=True) for status in status_elements_promocode]
            valut_promocode = promo_values
            print(promo_values)
            promocode_from_lk = valut_promocode[0]
        except Exception as ex:
            print(ex)

    # >>> Блок проверки корзины на чистоту
    try:
        if use_clear_bag == 'True':
            driver.get('https://megamarket.ru/multicart/')
            time.sleep(10)
            # cart-empty__description
            html_orders = driver.page_source
            soup_order = BeautifulSoup(html_orders, 'html.parser')
            status_elements_order = soup_order.find_all(class_='cart-empty__description')
            statuses = [status.get_text(strip=True) for status in status_elements_order]
            order_status = statuses
            if order_status == []:
                print('ELSE')
                buttons = driver.find_elements(By.CLASS_NAME, "svg-icon.icon-trash")
                for button in buttons:
                    button.click()
                    print('итерация')
                    time.sleep(0.2)
                time.sleep(3)
            else:
                if order_status == 'В корзине пока пусто':
                    print('[КОРЗИНА ПУСТАЯ]')

        else:
            pass
    except Exception as ex:
        print(ex)

    # >>> Блок проверки на прогретость аккаунта
    if use_check_grev == 'True':
        driver.get('https://megamarket.ru/personal/order/')
        time.sleep(5)
        html_orders = driver.page_source
        soup_order = BeautifulSoup(html_orders, 'html.parser')
        status_elements_order = soup_order.find_all(class_='order-delivery-status')
        statuses = [status.get_text(strip=True) for status in status_elements_order]
        order_status = statuses
        if order_status[0] == 'Отменена':
            pass
        else:
            os.remove(f'{cookies_way}/{cook}')
            cookies = driver.get_cookies()
            for cookie in cookies:
                if 'sameSite' in cookie:
                    cookie['sameSite'] = 'lax'
            with open(f'{cookies_dont_grev_way}/{cook}', 'w', encoding='utf-8') as file:
                json.dump(cookies, file)
            screan_name = f'{cook}nvalid.png'
            driver.get_screenshot_as_file(screan_name)
            type_message = 'send_dont_grev_screan'
            message_data = [f'{cook}', f'{screan_name}']
            send_data_telegram(user_n, type_message, message_data)
            driver.close()
            return

    else:
        pass
    try:
        os.remove(f'{cookies_way}/{cook}')
        cookies = driver.get_cookies()
        for cookie in cookies:
            if 'sameSite' in cookie:
                cookie['sameSite'] = 'lax'
        with open(f'{cookies_in_run_way}/{cook}', 'w', encoding='utf-8') as f:
            json.dump(cookies, f)
    except Exception as ex:
        print(ex)

    print('1')
    # >>> Блок подключения бонусов спасибо
    if use_on_sber_spas == 'True':
        driver.get('https://megamarket.ru/personal/loyalty')
        click_func(driver, on_sber_bonus_path, 10)
        print('2')
        time.sleep(1)
        click_func(driver, accept_on_sber_bonus_path, 10)
        print('3')
    else:
        pass

    # >>> Добавление нового адреса

    try:
        driver.get('https://megamarket.ru/personal/address/add/')
    except Exception as ex:
        print(ex)
    if use_txt_adres_deliv == 'True':
        with open(f'{txt_adres_way}', 'r', encoding='utf-8') as f:
            data_txt_adreses = f.read()
            list_adreses = data_txt_adreses.split('\n')
            list_range = len(list_adreses)
            rand_number = random.randint(0, int(list_range - 1))
            rand_adres_deliv = list_adreses[int(rand_number)]
            send_keys_func(driver, input_change_adres_locate_path, 10, rand_adres_deliv)
            click_func(driver, take_menu_adres_click, 10)
            click_func(driver, accept_change_adres_locate_path, 10)
    else:
        send_keys_func(driver, input_change_adres_locate_path, 10, adres_deliv)
        click_func(driver, take_menu_adres_click, 10)
        click_func(driver, accept_change_adres_locate_path, 10)
        time.sleep(3)

    # >>> Блок открытия карточки товара и добавления товара в корзину
    for product in list_bag_names:
        print('4')
        try:
            with open(f'{path_to_dir}/mainData/bag_data/{product}') as f:
                data = json.load(f)
                link = data['link_bag']
                value_product = data['value_bag']
            driver.get(f'{link}')
            print('5')
        except Exception as ex:
            print(ex)
        time.sleep(4)
        # >>> Блок обхода 18+
        click_func(driver, eghteen_check_path, 10)
        driver.get(f'{link}')
        time.sleep(4)
        click_func(driver, eghteen_check_path, 10)

        # >>> Цикл добавления нужного кол-ва товара в корзину
        click_func(driver, buy_bag_btn_path, 10)

        if value_product == '1':
            print('Кол-во товара 1, + не нажимаем')
            pass
        else:
            print('while')
            while i < int(value_product) - 1:
                click_func(driver, plus_product_path, 10)
                i += 1
            else:
                time.sleep(5)
    else:
        click_func(driver, go_to_cors_list_path, 10)
        click_func(driver, go_to_order_create_path, 10)
        print('Цикл завершен, идем далее')

    # >>> Блок создания заказа
    click_func(driver, cancle_window_path, 10)

    print('Блок ввода номера подъезда')
    driver.execute_script("window.scrollTo(0, 200);")
    time.sleep(1)
    # >>> Блок ввода номера подъезда
    rand_entrance = generate_data()
    if use_random_adres == 'True':
        entrance = rand_entrance
        click_func(driver, entry_entrance_path, 10)
        send_keys_func(driver, entry_entrance_path, 10, entrance)
    else:
        click_func(driver, entry_entrance_path, 10)
        send_keys_func(driver, entry_entrance_path, 10, adres_entrance)

    print('Блок ввода номера этажа')
    # >>> Блок ввода номера этажа
    rand_floor = generate_data()
    if use_random_adres == 'True':
        floor = rand_floor
        click_func(driver, entry_floor_path, 10)
        send_keys_func(driver, entry_floor_path, 10, floor)
    else:
        click_func(driver, entry_floor_path, 10)
        send_keys_func(driver, entry_floor_path, 10, adres_floor)

    print('Блок ввода номера квартира')
    # >>> Блок ввода номера квартира
    rand_block = generate_data()
    if use_random_adres == 'True':
        block = rand_block
        click_func(driver, entry_block_path, 10)
        send_keys_func(driver, entry_block_path, 10, block)
    else:
        click_func(driver, entry_block_path, 10)
        send_keys_func(driver, entry_block_path, 10, adres_block)

    print('Блок ввода номера домофона')
    # Блок ввода номера домофона
    rand_domofon = generate_data()
    if use_random_adres == 'True':
        domofon = rand_domofon
        click_func(driver, entry_domofon_path, 10)
        send_keys_func(driver, entry_domofon_path, 10, domofon)
    else:
        click_func(driver, entry_domofon_path, 10)
        send_keys_func(driver, entry_domofon_path, 10, adres_domofon)

    driver.execute_script("window.scrollTo(0, 200);")
    # >>> Блок ввода коментария
    if use_txt_comment == 'True':
        with open(f'{txt_comments_way}', 'r', encoding='utf-8') as f:
            data_txt_comments = f.read()
            list_comments = data_txt_comments.split('\n')
            comment = list_comments[0]
            send_keys_func(driver, entry_coment_path, 10, comment)
            del list_comments[0]
            f = open(f'{txt_comments_way}', 'w', encoding='utf-8')
            for txt_comment in list_comments:
                f.write(txt_comment + '\n')
            else:
                f.close()
    else:
        pass

    # >>> Блок замены получателя
    if use_change_poluchatel_from_link == 'True':
        driver.execute_script("window.scrollTo(0, 200);")
        change_poluchatel_in_order = get_paths_function_aub.get_path('change_poluchatel_in_order')
        click_to_box = get_paths_function_aub.get_path('click_to_box')

        input_firs_name_in_order_deliv_data = get_paths_function_aub.get_path('input_firs_name_in_order_deliv_data')
        input_last_name_in_order_deliv_data = get_paths_function_aub.get_path('input_last_name_in_order_deliv_data')
        input_phone_number_in_order_deliv_data = get_paths_function_aub.get_path('input_phone_number_in_order_deliv_data')
        accept_change_in_order_deliv_data = get_paths_function_aub.get_path('accept_change_in_order_deliv_data')

        # >>> Кнопка изменить
        click_func(driver, change_poluchatel_in_order, 10)

        # >>> Чек бокс получать буду не я
        click_func(driver, click_to_box, 10)

        # >>> Ввод первого имени
        if use_random_data_for_deliv == 'True':
            fake = Faker('ru_RU')
            f_name = fake.first_name_male()
            send_keys_func(driver, input_firs_name_in_order_deliv_data, 10, f_name)
        else:
            send_keys_func(driver, input_firs_name_in_order_deliv_data, 10, deliv_first_name)

        # >>> Ввод второго имени
        if use_random_data_for_deliv == 'True':
            fake = Faker('ru_RU')
            s_name = fake.last_name_male()
            send_keys_func(driver, input_last_name_in_order_deliv_data, 10, s_name)
        else:
            send_keys_func(driver, input_last_name_in_order_deliv_data, 10, deliv_last_name)

        # >>> Телефон получателя
        send_keys_func(driver, input_phone_number_in_order_deliv_data, 10, deliv_phone)

        # >>> Подтвердить изминения
        click_func(driver, accept_change_in_order_deliv_data, 10)

    else:
        pass

    # >>> Скрол страницы создания заказа
    try:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    except Exception as ex:
        print(ex)

    # >>> Блок ввода промокода
    if use_txt_promocode == 'True':
        with open(f'{txt_promocode_way}', 'r', encoding='utf-8') as f:
            data_txt_promocodes = f.read()
            list_promocodes = data_txt_promocodes.split('\n')
            txt_promocodes = list_promocodes[0]
            # >>> Блок ввода промокода
            send_keys_func(driver, entry_promocode_path, 10, txt_promocodes)
            # >>> Блок перезаписи txt с промокодами
            del list_promocodes[0]
            file_with_txt_promocodes = open(f'{txt_promocode_way}', 'w', encoding='utf-8')
            for txt_promocode in list_promocodes:
                file_with_txt_promocodes.write(txt_promocode + '\n')
            else:
                file_with_txt_promocodes.close()
            a = open(f'{txt_promocode_uses_way}', 'r', encoding='utf-8')
            if a == '':
                with open(f'{txt_promocode_uses_way}', 'w', encoding='utf-8') as f:
                    f.write(txt_promocodes + '\n')
            else:
                with open(f'{txt_promocode_uses_way}', 'a', encoding='utf-8') as f:
                    f.write(txt_promocodes + '\n')
            a.close()

    # >>> Блок ввода фиксированого промокода
    else:
        if use_promocode_from_lk == 'True':
            send_keys_func(driver, entry_promocode_path, 10, promocode_from_lk)
        else:
            send_keys_func(driver, entry_promocode_path, 10, fixed_promocode)

    # >>> Блок нажатия на кнопку "применить промокод"
    click_func(driver, entry_promocode_accept_btn, 10)

    # >>> Блок выбора способа олпаты
    click_func(driver, sber_pay_span_path, 10)

    # Блок проверки скидки промокода
    try:
        time.sleep(8)
        if use_check_bonus_value == 'True':
            html_check_value_bonus = driver.page_source
            soup_check_value_bonus = BeautifulSoup(html_check_value_bonus, 'html.parser')
            status_elements_bonus = soup_check_value_bonus.find_all(
                class_='precheck-block__common-info-text precheck-block__common-info-text_discount')
            statuses = [status.get_text(strip=True) for status in status_elements_bonus]
            order_status = statuses
            print(order_status)
            if len(order_status) == 2:
                discount = [int(re.sub(r'[^\d]', '', s)) for s in data]
                if check_promocode_price == discount[0]:
                    pass
                else:
                    if use_txt_promocode == 'True':
                        h = open(f'{txt_promocode_nvalid_way}', 'r', encoding='utf-8')
                        if h == '':
                            with open(f'{txt_promocode_nvalid_way}', 'w', encoding='utf-8') as f:
                                f.write(txt_promocodes + '\n')
                        else:
                            with open(f'{txt_promocode_nvalid_way}', 'a', encoding='utf-8') as f:
                                f.write(txt_promocodes + '\n')
                        driver.close()
                        return
                    else:
                        time.sleep(0.5)
                        screan_name = f'{cook}nvalid_promocode.png'
                        driver.get_screenshot_as_file(screan_name)
                        message_data = [f'{cook}', f'{screan_name}']
                        type_message = 'send_nvalid_promocode_screan'
                        send_data_telegram(user_n, type_message, message_data)
                        driver.close()
                        return

            else:
                if use_txt_promocode == 'True':
                    h = open(f'{txt_promocode_nvalid_way}', 'r', encoding='utf-8')
                    if h == '':
                        with open(f'{txt_promocode_nvalid_way}', 'w', encoding='utf-8') as f:
                            f.write(txt_promocodes)
                    else:
                        with open(f'{txt_promocode_nvalid_way}', 'a', encoding='utf-8') as f:
                            f.write(txt_promocodes)
                    time.sleep(2)
                    screan_name = f'{cook}nvalid_promocode.png'
                    driver.get_screenshot_as_file(screan_name)
                    message_data = [f'{cook}', f'{screan_name}']
                    type_message = 'send_nvalid_promocode_screan'
                    send_data_telegram(user_n, type_message, message_data)
                    driver.close()
                    return

        else:
            pass
    except Exception as ex:
        print(ex)
    # >>> Блок нажатия на кнопку "оплатить"
    time.sleep(5)
    click_func(driver, sber_pay_buy_path, 10)


    # >>> Блок ввода номера телефона для оплаты
    for by, selector in entry_pay_number_path:
        print('Pay_number entry')
        print(entry_pay_number_path)
        try:
            entry_pay_number = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((by, selector)))
            entry_pay_number.clear()
            print(f'{by} entry_pay_number_path')
            time.sleep(5)
            print(pay_phone)
            action = ActionChains(driver)
            action.click(entry_pay_number)
            for char in f' {pay_phone}':
                print(char)
                action.send_keys(char)
                action.perform()
                time.sleep(0.2)
            break
        except:
            pass
    time.sleep(2)

    # >>> Блок нажатия на кнопку "оплатить" после ввода номера телефона для олпаты
    click_func(driver, get_qr_code_path, 10)

    # >>> Блок отправки QR кода в тг бота
    try:
        time.sleep(10)
        screan_name = f'{cook}qrCode_for_pay.png'
        driver.get_screenshot_as_file(screan_name)
        message_data = [f'{cook}', f'{screan_name}']
        type_message = 'send_scren_qr_code'
        send_data_telegram(user_n, type_message, message_data)
    except Exception as ex:
        print(ex)


    if use_change_poluchatel_from_link == 'False':
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

        # >>> Блок обхода всплываюшего окна (КНОПКА ХОРОШО)
        click_func(driver, accept_winodw_on_order_list_path, 10)

        # >>> Блок перехода к вкладке "активные закаы"
        click_func(driver, go_to_active_order_list_path, 10)

        # >>> Блок перехода к карточке заказа
        click_func(driver, go_to_order_cart_path, 10)

        # >>> Блок проверки наличия кнопки "изменить" в форме замены получателя
        html_check_change = driver.page_source
        soup_check_change = BeautifulSoup(html_check_change, 'html.parser')
        status_elements_check = soup_check_change.find_all(
            class_='order-delivery-details__edit-button pui-link')
        statuses = [status.get_text(strip=True) for status in status_elements_check]
        order_status = statuses
        if order_status == []:
            os.remove(f'{cookies_in_run_way}/{cook}')
            cookies = driver.get_cookies()
            for cookie in cookies:
                if 'sameSite' in cookie:
                    cookie['sameSite'] = 'lax'
            with open(f'{cookies_dont_change_way}/{cook}', 'w', encoding='utf-8') as f:
                json.dump(cookies, f)
            time.sleep(3)
            type_message = 'send_dont_change_deliv'
            photo_name = f'{cook}dont_change_deliv.png'
            driver.get_screenshot_as_file(photo_name)
            message_data = [f'{cook}', f'{photo_name}']
            send_data_telegram(user_n, type_message, message_data)
        else:
            # >>> Блок перехода к форме для замены получателя заказа
            try:
                change_deliv_data = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, "(//span[contains(text(), 'Изменить')])[2]")))
                change_deliv_data.click()
            except:
                change_deliv_data = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, "(//span[contains(text(), 'Изменить')])[1]")))
                change_deliv_data.click()

            # >>> Блок замены имени в форме для замены получателя
            if use_random_data_for_deliv == 'True':
                fake = Faker('ru_RU')
                f_name = fake.first_name_male()
                send_keys_func(driver, change_firts_name_data_path, 10, f_name)
            else:
                send_keys_func(driver, change_firts_name_data_path, 10, deliv_first_name)

            # >>> Блок замены фамилии в форме для замены получателя
            if use_random_data_for_deliv == 'True':
                fake = Faker('ru_RU')
                s_name = fake.last_name_male()
                send_keys_func(driver, change_last_name_data_path, 10, s_name)
            else:
                send_keys_func(driver, change_last_name_data_path, 10, deliv_last_name)

            # >>> Блок замены номера телефона в форме для замены получателя
            send_keys_func(driver, change_phone_number_data_path, 10, deliv_phone)

            # >>> Блок нажатия на кнопку "подтвердить" в форме подмены получателя
            click_func(driver, change_deliv_data_btn_path, 10)

            os.remove(f'{cookies_in_run_way}/{cook}')
            try:
                cookies = driver.get_cookies()
                for cookie in cookies:
                    if 'sameSite' in cookie:
                        cookie['sameSite'] = 'lax'
                with open(f'{cookies_uses_way}/{cook}', 'w', encoding='utf-8') as f:
                    json.dump(cookies, f)
            except:
                pass

            print('Работа с аккаунтом окончена')
            time.sleep(20)

    else:
        os.remove(f'{cookies_in_run_way}/{cook}')
        try:
            cookies = driver.get_cookies()
            for cookie in cookies:
                if 'sameSite' in cookie:
                    cookie['sameSite'] = 'lax'
            with open(f'{cookies_uses_way}/{cook}', 'w', encoding='utf-8') as f:
                json.dump(cookies, f)
        except:
            pass
        print('Работа с аккаунтом окончена')
        time.sleep(10)



def Pool(list_bag_names, user_n):
    global proxy_list, proxy_host, proxy_port, proxy_password, proxy_username
    with open(f'{path_to_dir}/mainData/smm_auto_buy_setting.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        cookies_way = data['cookies_way']
        pool_value = data['pool_value']
        txt_proxy = data['txt_proxy_way']
        use_txt_proxy = data['use_txt_proxy']
        txt_uses_proxy_way = data['txt_uses_proxy_way']
        use_mobile_proxy = data['use_mobile_proxy']
        mobile_proxy = data['mobile_proxy']

        cookies_list = os.listdir(f'{cookies_way}')
        if use_txt_proxy == 'True':
            with open(f'{txt_proxy}', 'r') as f:
                proxy = f.read()
                proxy_list = proxy.split('\n')
                print(proxy_list)
        else:
            pass

    def process_start(cook):
        startAB(cook, list_bag_names, user_n)

    try:
        with ThreadPoolExecutor(max_workers=int(pool_value)) as executor:
            for cook in cookies_list:
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
                    a = open(f'{txt_uses_proxy_way}', 'r', encoding='utf-8')
                    if a == '':
                        with open(f'{txt_uses_proxy_way}', 'w', encoding='utf-8') as f:
                            f.write(proxy + '\n')
                    else:
                        with open(f'{txt_uses_proxy_way}', 'a', encoding='utf-8') as f:
                            f.write(proxy + '\n')
                    a.close()
                elif use_mobile_proxy == 'True':
                    data = mobile_proxy.split(':')
                    proxy_host = data[0]
                    proxy_port = data[1]
                    proxy_username = data[2]
                    proxy_password = data[3]
                executor.submit(process_start, cook)
                time.sleep(8)
            executor.shutdown(wait=True)
    except Exception as ex:
        print(ex)
        return


