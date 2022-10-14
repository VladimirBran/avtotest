from Pet_Friends.app.api import PetFriends
from Pet_Friends.app.setting import valid_email, valid_password, invalid_email, invalid_password
import os

def test_get_api_key_valid_user(email = valid_email, password = valid_password):
    # Проверяем что запрос API ключа возвращает код статуса запроса 200, а в результате
    #  (в переменной result) содержится слово key.
    status, result = PetFriends().get_api_key(email, password)
    assert status == 200
    assert 'key' in result


def test_get_list_of_pets_valid_key(filter=''):
    # Проверка GET-запроса. Проверяем что запрос всех питомцев возвращает код статуса 200 и это не пустой
    # список.
    _, auth_key = PetFriends().get_api_key(valid_email, valid_password)
    status, result = PetFriends().get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0


def test_add_new_pet_with_valid_data(name = 'Boba', animal_type = 'Gungan', age = '15', pet_photo = 'image/photo.jpg'):
    # Проверка POST-запроса. Проверяем что добавление нового питомца возвращает код статуса 200, что список
    # с добавленными данными не пустой и что в ответе содержатся добавленные данные
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, auth_key = PetFriends().get_api_key(valid_email, valid_password)
    status, result = PetFriends().add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] == name


def test_delete_pet_successful():
    # Проверка DELETE-запроса. Проверяем что удаление существующего  питомца возвращает код статуса 200
    _, auth_key = PetFriends().get_api_key(valid_email, valid_password)
    _, my_pets = PetFriends().get_list_of_pets(auth_key, 'my_pets')

    if len(my_pets['pets']) == 0:
        PetFriends().add_new_pet(auth_key, 'Boba', 'Gungan', '15', 'image/photo.jpg')
        _, my_pets = PetFriends().get_list_of_pets(auth_key, 'my_pets')

    pet_id = my_pets['pets'][0]['id']
    status, _ = PetFriends().delete_pet(auth_key, pet_id)

    _, my_pets = PetFriends().get_list_of_pets(auth_key, 'my_pets')
    assert status == 200
    assert pet_id not in my_pets.values()


def test_update_pet_info(name = 'Боба', animal_type = 'НеГунган', age = '17'):
    # Проверка PUT-запроса. Проверяем что изменение данных, о существующем  питомце, возвращает код статуса 200
    _, auth_key = PetFriends().get_api_key(valid_email, valid_password)
    _, my_pets = PetFriends().get_list_of_pets(auth_key, 'my_pets')

    if len(my_pets['pets']) > 0:
        status, result = PetFriends().update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
        assert status == 200
        assert result['name'] == name
    else:
        raise Exception("Мои питомцы отсутствуют")



def test_add_new_pet_without_photo_with_valid_data(name = 'Boba', animal_type = 'Gungan', age = '15'):
    # Проверка POST-запроса. Проверяем что добавление нового питомца без фото возвращает код статуса 200,
    # что список с добавленными данными не пустой и что в ответе содержатся добавленные данные
    _, auth_key = PetFriends().get_api_key(valid_email, valid_password)
    status, result = PetFriends().add_new_pet_without_photo(auth_key, name, animal_type, age)
    assert status == 200
    assert result['name'] == name


def test_add_photo_of_pet(pet_photo = 'image/photo.jpg'):
    # Проверка POST-запроса. Проверяем что добавление новой фотографии существующего питомца (по pet_id)
    # возвращает код статуса 200
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = PetFriends().get_api_key(valid_email, valid_password)
    _, my_pets = PetFriends().get_list_of_pets(auth_key, 'my_pets')

    if len(my_pets['pets']) > 0:
        status, result = PetFriends().add_photo_of_pet(auth_key, my_pets['pets'][0]['id'], pet_photo)
        _, my_pets = PetFriends().get_list_of_pets(auth_key, 'my_pets')
        assert status == 200
        assert result['pet_photo'] == my_pets['pets'][0]['pet_photo']
    else:
        raise Exception("Мои питомцы отсутствуют")


def test_get_api_key_invalid_user_email(email = invalid_email, password = valid_password):
    # Проверка GET-запроса. Проверяем что запрос API ключа c неверным e-mail не возвращает код статуса
    # запроса 200, а в результате (в переменной result) не содержится слово key)
    status, result = PetFriends().get_api_key(email, password)
    assert status != 200
    assert 'key' not in result


def test_get_api_key_invalid_user_password(email = valid_email, password = invalid_password):
    # Проверка GET-запроса. Проверяем что запрос API ключа c неверным password не возвращает код статуса
    # запроса 200, а в результате (в переменной result) не содержится слово key
    status, result = PetFriends().get_api_key(email, password)
    assert status != 200
    assert 'key' not in result


def test_get_api_key_invalid_user(email = invalid_email, password = invalid_password):
    # Проверка GET-запроса. Проверяем что запрос API ключа c неверным email и password не возвращает код
    # статуса запроса 200, а в результате (в переменной result) не содержится слово key
    status, result = PetFriends().get_api_key(email, password)
    assert status != 200
    assert 'key' not in result


def test_add_new_pet_with_empty_name(name = '', animal_type = 'Gungan', age = '15', pet_photo = 'image/photo.jpg'):
    # Проверка POST-запроса. Проверяем что добавление нового питомца c пустым значением в поле name невозможно.
    # Тест не будет пройден если питомец будет добавлен на сайт с пустым значением в поле name
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, auth_key = PetFriends().get_api_key(valid_email, valid_password)
    status, result = PetFriends().add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status != 200
    assert result['name'] != ''


def test_add_new_pet_with_special_symbols_name(name = '$i$yn', animal_type = 'Gungan', age = '15', pet_photo = 'image/photo.jpg'):
   # Проверка POST-запроса. Проверяем что добавление нового питомца c со спецсимволами в поле name невозможно.
   #  После выполнения теста питомец дабавляется на сайт со спецсимволами в поле name.
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, auth_key = PetFriends().get_api_key(valid_email, valid_password)
    status, result = PetFriends().add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status != 200
    assert result['name'] != '$i$yn' 


def test_add_new_pet_with_empty_animal_type(name = 'Boba', animal_type = '', age = '15', pet_photo = 'image/photo1.jpg'):
    # Проверка POST-запроса. Проверяем что добавление нового питомца c пустым значением в поле animal_type
    # невозможно. Тест не будет пройден если питомец будет добавлен на сайт с пустым значением в поле
    # animal_type
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, auth_key = PetFriends().get_api_key(valid_email, valid_password)
    status, result = PetFriends().add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status != 200
    assert result['animal_type'] != ''


def test_add_new_pet_with_special_symbols_animal_type(name = 'Byba', animal_type = 'G@ng@n', age = '15', pet_photo = 'image/photo.jpg'):
    # Проверка POST-запроса. Проверяем что добавление нового питомца c со спецсимволами в поле animal_type
    # невозможно. Тест не будет пройден если питомец будет добавлен на сайт с типом животного, имеющим
    # спецсимволы
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, auth_key = PetFriends().get_api_key(valid_email, valid_password)
    status, result = PetFriends().add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status != 200
    assert result['animal_type'] != 'G@ng@n'

def test_add_new_pet_negative_age(name = 'Boba', animal_type = 'Gungan', age = '-15', pet_photo = 'image/photo.jpg'):
    # Проверка POST-запроса. Проверяем что добавление нового питомца с отрицательным числом в поле age
    # невозможно. Тест не будет пройден если питомец будет добавлен на сайт с отрицательным числом в поле age
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, auth_key = PetFriends().get_api_key(valid_email, valid_password)
    status, result = PetFriends().add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status != 200
    assert age not in result['age']
