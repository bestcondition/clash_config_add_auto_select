import yaml
import requests

from config import config


def get_text(file_url, proxy_url=config.PROXY_URL):
    """下载文件"""
    try:
        # 先直接下载, 下载不了再代理下载
        response = requests.get(file_url)
        assert response.ok, "直接下载失败了!"
        return response.text
    except Exception as e:
        proxies = {
            'http': proxy_url,
            'https': proxy_url
        }
        response = requests.get(file_url, proxies=proxies)
        assert response.ok, "代理下载也失败了!"
        return response.text


def get_json(text):
    """yaml to dict"""
    json_dict = yaml.load(text, yaml.SafeLoader)
    return json_dict


def pick_main_proxy_group(proxy_groups):
    """挑出最主要的代理组"""
    if len(proxy_groups) == 0:
        return None
    name_to_group = {
        group['name']: group
        for group in proxy_groups
    }
    all_group_name_count = {
        group['name']: 0
        for group in proxy_groups
    }
    for group in proxy_groups:
        for proxy in group.get('proxies', []):
            if proxy in all_group_name_count:
                all_group_name_count[proxy] += 1
    group_name = max(all_group_name_count.items(), key=lambda x: x[1])[0]
    group = name_to_group[group_name]
    return group


def get_group_of_type(proxy_groups, type_name="url-test"):
    for group in proxy_groups:
        if group.get('type') == type_name:
            return group


def make_url_test_group(
        group_name,
        all_proxies,
        group_type="url-test",
        ping_url=config.PING_URL,
        internal=60 * 60,
):
    all_proxies_name = [
        proxy['name']
        for proxy in all_proxies
    ]
    group = {
        'name': group_name,
        'type': group_type,
        'proxies': all_proxies_name,
        'url': ping_url,
        'interval': internal
    }
    return group


def unique_str_value(base_value, value_set):
    value_set = set(value_set)
    if base_value not in value_set:
        return base_value
    suffix = 0
    while f'{base_value}{suffix}' in value_set:
        suffix += 1
    return f'{base_value}{suffix}'


def transfer_logic(file_or_url):
    text = get_text(file_or_url)
    clash_config = get_json(text)
    proxies = clash_config['proxies']
    proxy_groups = clash_config['proxy-groups']
    if get_group_of_type(proxy_groups, 'url-test'):
        return text
    else:
        new_group_name = unique_str_value('auto', [group['name'] for group in proxy_groups])
        new_group = make_url_test_group(new_group_name, proxies, 'url-test')
        proxy_groups.append(new_group)
        main_group = pick_main_proxy_group(proxy_groups)
        main_group['proxies'].insert(0, new_group_name)
        new_config_test = yaml.dump(clash_config, None, allow_unicode=True, sort_keys=False)
        return new_config_test
