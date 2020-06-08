import time
import tqdm
import vk_spy
import file_ops
import settings


def main():
    user = vk_spy.get_id_by_name(settings.user, settings.token, settings.v)

    usr_groups = vk_spy.get_data(
        settings.token,
        settings.v,
        'groups.get',
        user_id=user,
        extended=1,
        fields='members_count',
    )

    set_usr_group = vk_spy.get_groups_set(usr_groups)

    usr_friends = vk_spy.get_data(
        settings.token,
        settings.v,
        'friends.get',
        user_id=user,
    )

    pbar = tqdm.tqdm(usr_friends)
    for i in pbar:
        start = time.time()
        frnd_groups = vk_spy.get_data(
            settings.token,
            settings.v,
            'groups.get',
            user_id=i,
            extended=1,
            fields='members_count',
        )

        if frnd_groups:
            set_usr_group -= vk_spy.get_groups_set(frnd_groups[:1000])
        sleeptime = 1 / 3 - (time.time() - start)
        if sleeptime > 0:
            time.sleep(sleeptime)

    usr_groups = [i for i in usr_groups if i['id'] in set_usr_group]
    for i in usr_groups:
        if 'members_count' not in i:
            i['members_count'] = 0
    usr_groups = [
            {
                'name': i['name'],
                'gid': i['id'],
                'members_count': i['members_count']}
            for i in usr_groups
        ]

    file_ops.save_results(usr_groups, 'groups.json')


if __name__ == '__main__':
    main()
