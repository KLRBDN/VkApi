import requests
import vk_api
import argparse


def parse_args():
    parser = argparse.ArgumentParser(description='Скрипт, позволяющий по id пользователя получить список его друзей')
    parser.add_argument('id', metavar='user_id', type=int, nargs=1, help='ID пользователя, друзей которого вы хотите '
                                                                         'получить')
    args = parser.parse_args()
    return args.id


def check_if_profile_exists(session, uid):
    try:
        session.users.get(user_id=uid)
    except:
        raise vk_api.AccountBlocked('Такой пользователь не существует или его страница была удалена')


def get_friends(session, uid):
    try:
        return session.friends.get(user_id=uid, fields=['country', 'city'])
    except:
        raise vk_api.AccessDenied('Профиль этого пользователя является приватным, поэтому у него нельзя получить ' +
                                  'список друзей')


def print_friends(friends):
    print(f'Количество друзей пользователя: {friends["count"]}')

    for friend in friends['items']:
        if "country" in friend:
            if "city" in friend:
                print(
                    f'{friend["first_name"]} {friend["last_name"]}, {friend["country"]["title"]}, {friend["city"]["title"]}')
            else:
                print(f'{friend["first_name"]} {friend["last_name"]}, {friend["country"]["title"]}')
        else:
            print(f'{friend["first_name"]} {friend["last_name"]}')


def get_session(app_id, token):
    try:
        return vk_api.VkApi(app_id=app_id, token=token)
    except requests.exceptions.ConnectionError:
        raise requests.exceptions.ConnectionError('Проблемы с подключением к серверам Vk. Проверьте, нет ли у вас' +
                                                  'проблем с интернет соединением ')


def main(uid):
    # Введите id своего приложения
    app_id = 8180440
    # Введите свой token, так как этот срок действия этого токена к моменту проверки задания может истечь
    token = 'a6beba2774a33f546ef70768e65450def8baa8a8875f019f87acad3101105cf31a276a28d635be0c1bbfb'

    vk_session = get_session(app_id, token)
    vk = vk_session.get_api()

    check_if_profile_exists(vk, uid)
    friends = get_friends(vk, uid)

    print_friends(friends)


if __name__ == "__main__":
    user_id = parse_args()
    main(user_id)
