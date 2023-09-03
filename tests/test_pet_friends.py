from api import PetFriends
from settings import valid_email, valid_password

pf = PetFriends()


def test_api_key_for_valid_user(email=valid_email, password=valid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result

def test_api_key_for_invalid_user(email='admiral040', password=valid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert 'key' not in result

def test_get_all_pets_with_valid_auth_key(filter=''):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0

def test_get_all_pets_with_filter_mypets(filter='my_pets'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 200
    assert len(result['pets']) > 0

def test_get_all_pets_with_invalid_filter(filter='no_my_pets'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 500

def test_add_new_pet_with_valid_data(name='Шелдон', animal_type='Ирландский кот',
                                     age='2', pet_photo='images/cat2.jpg'):

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] == name

def test_add_new_pet_with_empty_name(animal_type='Ирландский кот',
                                     age='2', pet_photo='images/cat2.jpg'):

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key,animal_type, age, pet_photo)
    assert status == 200
    assert result['age'] == age

def test_update_info_pet_with_valid_data(name='Шерлок', animal_type='Ирландский кот',
                                         age='10'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) > 0:
        status, result = pf.update_info_pet(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        assert status == 200
        assert result['name'] == name
    else:
        raise Exception("There is no my pets")

def test_delete_pet_in_list():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Суперкот", "кот", "3", "images/cat1.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    pet_id = my_pets['pets'][0]['id']

    status, _ = pf.delete_pet(auth_key, pet_id)

    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    assert status == 200
    assert pet_id not in my_pets.values()

def test_create_pet_without_photo(name= 'Чарли', animal_type = 'Немецкая овчарка', age= '4'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.create_pet_without_photo(auth_key, name, animal_type, age)
    assert status == 200
    assert result['name'] == name

def test_set_photo_for_pet(pet_photo='images/dog1.jpg'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) > 0:
        status, result = pf.set_photo(auth_key, my_pets['pets'][0]['id'], pet_photo)

        assert status == 200
        assert result['pet_photo'] != None
    else:
        raise Exception("There is no my pets")

