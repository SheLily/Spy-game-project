import requests


def get_id_by_name(username, token, v):
    data = {
        'access_token': token,
        'user_ids': username,
        'v': v
    }
    response = requests.get(
        'https://api.vk.com/method/users.get',
        data
    ).json()
    return response['response'][0]['id']


def get_data(token, v, method, **kwargs):
    data = {
        'access_token': token,
        'v': v
    }
    data.update(kwargs)
    response = requests.get(
        f'https://api.vk.com/method/{method}', data
        ).json()
    if 'error' not in response:
        return response['response']['items']


def get_groups_set(group_list):
    return {i['id'] for i in group_list}
