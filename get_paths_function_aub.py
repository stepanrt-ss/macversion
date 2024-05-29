import pymysql
from selenium.webdriver.common.by import By
from config import host, password, user, db_name


con = pymysql.connect(
                host=host,
                port=3306,
                user=user,
                password=password,
                database=db_name,
                cursorclass=pymysql.cursors.DictCursor
            )


def get_path(name_path):
    with con.cursor() as cursor:
        command_for_db = 'SELECT * FROM AUTO_BUY_PATHS'
        cursor.execute(command_for_db)
        data_sql = cursor.fetchall()
        for data in data_sql:
            if data['name_path'] == str(name_path):
                if data['priority'] == 'xpath':
                    path = [
                        (By.XPATH, f"{data['xpath_value']}"),
                        (By.CSS_SELECTOR, f"{data['css_value']}"),
                        (By.CLASS_NAME, f"{data['calss_value']}")
                    ]
                    return path
                elif data['priority'] == 'css':
                    path = [
                        (By.CSS_SELECTOR, f"{data['css_value']}"),
                        (By.XPATH, f"{data['xpath_value']}"),
                        (By.CLASS_NAME, f"{data['calss_value']}")
                    ]
                    return path
                elif data['priority'] == 'class':
                    path = [
                        (By.CLASS_NAME, f"{data['calss_value']}"),
                        (By.XPATH, f"{data['xpath_value']}"),
                        (By.CSS_SELECTOR, f"{data['css_value']}")
                    ]
                    return path
