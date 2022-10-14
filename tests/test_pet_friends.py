from app.api import PetFriends
from app.setting import valid_email, valid_password, invalid_email, invalid_password
import os

def test_get_api_key_valid_user(email = valid_email, password = valid_password):
    """Проверка GET-запроса. Проверяем что запрос API ключа возвращает код статуса запроса 200, а в результате
     (в переменной result) содержится слово key)"""
    status, result = PetFriends().get_api_key(email, password)  # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    assert status == 200  # Сверяем полученные данные с нашими ожиданиями
    assert 'key' in result


def test_get_list_of_pets_valid_key(filter=''):
    """Проверка GET-запроса. Проверяем что запрос всех питомцев возвращает код статуса 200 и это не пустой
    список. Для этого при помощи метода get_api_key() получаем API ключ, сохраняем его в переменной auth_key,
    затем применяем метод get_list_of_pets() и проверяем статус ответа и то, что список питомцев не пустой.
    Доступное значение параметра filter - 'my_pets', либо '' """
    _, auth_key = PetFriends().get_api_key(valid_email, valid_password)
    status, result = PetFriends().get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0 # Проверяем, что список не пустой


def test_add_new_pet_with_valid_data(name = 'Boba', animal_type = 'Gungan', age = '15', pet_photo = 'image/photo.jpg'):
    """Проверка POST-запроса. Проверяем что добавление нового питомца возвращает код статуса 200, что список
    с добавленными данными не пустой и что в ответе содержатся добавленные данные"""
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo) # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo

    _, auth_key = PetFriends().get_api_key(valid_email, valid_password) # Запрашиваем ключ API и сохраняем в переменую auth_key
    status, result = PetFriends().add_new_pet(auth_key, name, animal_type, age, pet_photo)  # Добавляем питомца
    assert status == 200  # Сверяем полученный ответ с ожидаемым результатом
    assert result['name'] == name


def test_delete_pet_successful():
    """Проверка DELETE-запроса. Проверяем что удаление существующего  питомца возвращает код статуса 200"""
    _, auth_key = PetFriends().get_api_key(valid_email, valid_password) # Запрашиваем ключ API и сохраняем в переменую auth_key
    _, my_pets = PetFriends().get_list_of_pets(auth_key, 'my_pets') # Запрашиваем список своих питомцев

    if len(my_pets['pets']) == 0: # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
        PetFriends().add_new_pet(auth_key, 'Boba', 'Gungan', '15', 'image/photo.jpg')
        _, my_pets = PetFriends().get_list_of_pets(auth_key, 'my_pets')

    pet_id = my_pets['pets'][0]['id']  # Берём id первого питомца из списка и отправляем запрос на удаление
    status, _ = PetFriends().delete_pet(auth_key, pet_id)

    _, my_pets = PetFriends().get_list_of_pets(auth_key, 'my_pets')  # Ещё раз запрашиваем список своих питомцев
    assert status == 200  # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert pet_id not in my_pets.values()


def test_update_pet_info(name = 'из', animal_type = 'измененный', age = '15'):
    """Проверка PUT-запроса. Проверяем что изменение данных о существующем  питомце возвращает код статуса 200"""
    _, auth_key = PetFriends().get_api_key(valid_email, valid_password)  # Запрашиваем ключ API и сохраняем в переменую auth_key
    _, my_pets = PetFriends().get_list_of_pets(auth_key, 'my_pets') # Запрашиваем список своих питомцев

    if len(my_pets['pets']) > 0:     # Если список не пустой, то пробуем обновить его имя, тип и возраст
        status, result = PetFriends().update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
        assert status == 200  # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert result['name'] == name
    else:
        raise Exception("Мои питомцы отсутствуют") # Если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев

##################################################################################################################

def test1_add_new_pet_without_photo_with_valid_data(name = 'Boba', animal_type = 'Gungan', age = '15'):
    """Проверка POST-запроса. Проверяем что добавление нового питомца без фото возвращает код статуса 200,
    что список с добавленными данными не пустой и что в ответе содержатся добавленные данные"""
    _, auth_key = PetFriends().get_api_key(valid_email, valid_password)  # Запрашиваем ключ API и сохраняем в переменую auth_key
    status, result = PetFriends().add_new_pet_without_photo(auth_key, name, animal_type, age)
    assert status == 200
    assert result['name'] == name


def test2_add_photo_of_pet(pet_photo = 'image/photo.jpg'):
    """Проверка POST-запроса. Проверяем что добавление новой фотографии существующего питомца (по pet_id)
    возвращает код статуса 200"""
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo) # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    _, auth_key = PetFriends().get_api_key(valid_email, valid_password)  # Запрашиваем ключ API и сохраняем в переменую auth_key
    _, my_pets = PetFriends().get_list_of_pets(auth_key, 'my_pets') # Запрашиваем список своих питомцев

    if len(my_pets['pets']) > 0: # Если список не пустой, то пробуем обновить его имя, тип и возраст
        status, result = PetFriends().add_photo_of_pet(auth_key, my_pets['pets'][0]['id'], pet_photo)
        _, my_pets = PetFriends().get_list_of_pets(auth_key, 'my_pets')  # Снова запрашиваем список своих питомцев
        assert status == 200
        assert result['pet_photo'] == my_pets['pets'][0]['pet_photo'] # Проверяем, что фото первого питомца изменилось на только что добавленное фото
    else:
        raise Exception("Мои питомцы отсутствуют")


def test3_get_api_key_invalid_user_email(email = invalid_email, password = valid_password):
    """Проверка GET-запроса. Проверяем что запрос API ключа c неверным e-mail не возвращает код статуса
    запроса 200, а в результате (в переменной result) не содержится слово key)"""
    status, result = PetFriends().get_api_key(email, password)  # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    assert status != 200  # Сверяем полученные данные с нашими ожиданиями
    assert 'key' not in result


def test4_get_api_key_invalid_user_password(email = valid_email, password = invalid_password):
    """Проверка GET-запроса. Проверяем что запрос API ключа c неверным password не возвращает код статуса
    запроса 200, а в результате (в переменной result) не содержится слово key)"""
    status, result = PetFriends().get_api_key(email, password)  # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    assert status != 200  # Сверяем полученные данные с нашими ожиданиями
    assert 'key' not in result


def test5_get_api_key_invalid_user(email = invalid_email, password = invalid_password):
    """Проверка GET-запроса. Проверяем что запрос API ключа c неверным email и password не возвращает код
    статуса запроса 200, а в результате (в переменной result) не содержится слово key)"""
    status, result = PetFriends().get_api_key(email, password)  # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    assert status != 200  # Сверяем полученные данные с нашими ожиданиями
    assert 'key' not in result


def test6_add_new_pet_with_empty_name(name = '', animal_type = 'Gungan', age = '15', pet_photo = 'image/photo.jpg'):
    """Проверка POST-запроса. Проверяем что добавление нового питомца c пустым значением в поле name невозможно.
    Тест не будет пройден если питомец будет добавлен на сайт с пустым значением в поле name"""
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo) # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo

    _, auth_key = PetFriends().get_api_key(valid_email, valid_password) # Запрашиваем ключ API и сохраняем в переменую auth_key
    status, result = PetFriends().add_new_pet(auth_key, name, animal_type, age, pet_photo)  # Добавляем питомца
    assert status != 200 # Ожидаем, что код статуса запроса будет не равен 200
    assert result['name'] != '' # Ожидаем, что питомец не будет добавлен на сайт с пустым значением в поле name


def test7_add_new_pet_with_special_symbols_name(name = '$i$yn', animal_type = 'Gungan', age = '15', pet_photo = 'image/photo.jpg'):
    """Проверка POST-запроса. Проверяем что добавление нового питомца c со спецсимволами в поле name невозможно.
    Тест не будет пройден если питомец будет добавлен на сайт с именем, имеющим спецсимволы"""
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, auth_key = PetFriends().get_api_key(valid_email, valid_password)
    status, result = PetFriends().add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status != 200 # Ожидаем, что код статуса запроса будет не равен 200
    assert result['name'] != '$i$yn' # Ожидаем, что питомец не будет добавлен на сайт со спецсимволами в поле name


def test8_add_new_pet_with_empty_animal_type(name = 'Boba', animal_type = '', age = '15', pet_photo = 'images/photo1.jpg'):
    """Проверка POST-запроса. Проверяем что добавление нового питомца c пустым значением в поле animal_type
    невозможно. Тест не будет пройден если питомец будет добавлен на сайт с пустым значением в поле
    animal_type"""
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo) # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo

    _, auth_key = PetFriends().get_api_key(valid_email, valid_password) # Запрашиваем ключ API и сохраняем в переменую auth_key
    status, result = PetFriends().add_new_pet(auth_key, name, animal_type, age, pet_photo)  # Добавляем питомца
    assert status != 200 # Ожидаем, что код статуса запроса будет не равен 200
    assert result['animal_type'] != '' # Ожидаем, что питомец не будет добавлен на сайт с пустым значением в поле name


def test9_add_new_pet_with_special_symbols_animal_type(name = 'Byba', animal_type = 'G@ng@n', age = '15', pet_photo = 'image/photo.jpg'):
    """Проверка POST-запроса. Проверяем что добавление нового питомца c со спецсимволами в поле animal_type
    невозможно. Тест не будет пройден если питомец будет добавлен на сайт с типом животного, имеющим
    спецсимволы"""
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, auth_key = PetFriends().get_api_key(valid_email, valid_password)
    status, result = PetFriends().add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status != 200 # Ожидаем, что код статуса запроса будет не равен 200
    assert result['animal_type'] != 'G@ng@n' # Ожидаем, что питомец не будет добавлен на сайт со спецсимволами в поле name


def test10_add_new_pet_negative_age(name = 'Boba', animal_type = 'Gungan', age = '-15', pet_photo = 'image/photo.jpg'):
    """Проверка POST-запроса. Проверяем что добавление нового питомца с отрицательным числом в поле age
    невозможно. Тест не будет пройден если питомец будет добавлен на сайт с отрицательным числом в поле age"""
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, auth_key = PetFriends().get_api_key(valid_email, valid_password)
    status, result = PetFriends().add_new_pet(auth_key, name, animal_type, age, pet_photo)

    assert status != 200 # Ожидаем, что код статуса запроса будет не равен 200
    assert age not in result['age'] # Ожидаем, что питомец не будет добавлен на сайт с отрицательным возрастом