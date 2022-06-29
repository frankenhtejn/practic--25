import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from collections import Counter


@pytest.fixture(autouse=True)
def testing():
    pytest.driver = webdriver.Chrome('C:\drvchrome\chromedriver1.exe')
    pytest.driver.implicitly_wait(10)
    # Переходим на страницу авторизации
    pytest.driver.get('https://petfriends.skillfactory.ru/login')
    # Вводим email
    pytest.driver.find_element_by_id('email').send_keys('frankenhtejn@ya.ru')
    # Вводим пароль
    pytest.driver.find_element_by_id('pass').send_keys('123456')
    # Нажимаем на кнопку входа в аккаунт
    pytest.driver.find_element_by_css_selector('button[type="submit"]').click()
    # Нажимаем на кнопку "мои питомцы"
    pytest.driver.find_element_by_xpath("//a[@class='nav-link']").click()
    yield
    pytest.driver.quit()


# ПРоверка что все питомцы присутствуют"

def test_all_pets():


    # Получаем информацию профиля и записываем в переменную
    text = pytest.driver.find_element_by_xpath('/html/body/div[1]/div/div[1]').text
    s = text.rfind("Питомцев") + 10
    e = text.rfind("Друзей")
    amount = int(text[s:e:])

    # Получаем всю информацию о питомцах на странице
    pets_len = len(pytest.driver.find_elements_by_xpath('//*[@id="all_my_pets"]/table/tbody/tr'))


    assert pets_len == amount,"количество питомцев не соответсвует питомцам указаных в профиле"
# Проверка что хотя бы у половины питомцев есть фото
def test_img_pets():
    # не явное ожидание
    images = WebDriverWait(pytest.driver, 5).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'tr th img')))

    # Получаем все фотографии питомцев на странице
 #   images = pytest.driver.find_elements_by_xpath('//*[@id="all_my_pets"]/table/tbody//img')
    pets_with_photo =0
    for i in range(len(images)):
        if images[i].get_attribute('src') != '':
            pets_with_photo += 1

    assert round(len(images)/2) <= pets_with_photo,"Больше чем у половины питомцев отсутствуют фото"

# проверка что у всех питомцев есть имя порода и возраст
def test_all_name_pets():
    # не явное ожидание
    pytest.driver.implicitly_wait(10)

    # Получаем всю информацию о питомцах на странице
    pets_info = pytest.driver.find_elements_by_xpath('//*[@id="all_my_pets"]/table/tbody//td')
    # Сортируем информацию о питомцах и записываем в отдельные переменные
    names = pets_info[::4]
    breeds = pets_info[1::4]
    ages = pets_info[2::4]
    for i in range(len(names)):
        assert names[i].text != "", "не у всех питомцев есть Имя"
        assert breeds[i].text != "", "не у всех питомцев указана порода"
        assert ages[i].text != "", "не у всех питомцев указан возраст"

# проверка что у всех питомцев разные имена
def test_diff_name_pets():
    # Получаем всю информацию о питомцах на странице
    pets_info = pytest.driver.find_elements_by_xpath('//*[@id="all_my_pets"]/table/tbody//td')
    # извлекаем имена питмцев
    names = pets_info[::4]
    new_list_name =[]
    #создаем список с именами питомцев
    for i in range(len(names)):
        new_list_name.append(names[i].text)
    assert len(new_list_name) == len(set(new_list_name)) ," есть питомцы с одинаковыми именами"

#поиск питомцев дубликатов
def test_dublicate_pets():
    # Получаем всю информацию о питомцах на странице
    pets_info = pytest.driver.find_elements_by_xpath('//*[@id="all_my_pets"]/table/tbody//td')
    # Сортируем информацию о питомцах и записываем в отдельные переменные
    names = pets_info[::4]
    breeds = pets_info[1::4]
    ages = pets_info[2::4]
    list_pets=[]
    for i in range(len(names)):
        list_pets.append(names[i].text+breeds[i].text+ages[i].text)
    assert len(list_pets) == len(set(list_pets)), "Присутствуют питомцы двойники"
