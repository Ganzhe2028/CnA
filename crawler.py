import requests
from urllib.parse import urlparse
from base64 import b64decode
from tqdm import tqdm
import re

# 替换为你的GitHub个人访问令牌
access_token = 'ghp_xxxxxxxxx-your-tokens-xxxxx'  # 这里！替换为你的GitHub个人访问令牌！
headers = {'Authorization': f'token {access_token}'}

def get_repo_contents(username, repo_name, path=''):
    url = f'https://api.github.com/repos/{username}/{repo_name}/contents/{path}'
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to retrieve contents: {response.status_code}")
        return None

def count_items(username, repo_name, path=''):
    contents = get_repo_contents(username, repo_name, path)
    count = 0
    if contents:
        for item in contents:
            count += 1
            if item['type'] == 'dir':
                count += count_items(username, repo_name, item['path'])
    return count

def build_file_tree(username, repo_name, path='', indent=0, pbar=None):
    contents = get_repo_contents(username, repo_name, path)
    tree_content = ''
    if contents:
        for item in contents:
            pbar.update(1)
            connector = '└── ' if pbar.n == pbar.total else '├── '
            tree_content += ' ' * indent + connector + item['name']
            if item['type'] == 'dir':
                tree_content += '\n' + build_file_tree(username, repo_name, item['path'], indent + 4, pbar=pbar)
            else:
                tree_content += '\n'
                # 获取文件内容
                file_content_response = requests.get(item['url'], headers=headers)
                if file_content_response.status_code == 200:
                    file_content = file_content_response.json()['content']
                    # 尝试解码文件内容为UTF-8
                    try:
                        decoded_content = b64decode(file_content).decode('utf-8')
                        tree_content += ' ' * (indent + 4) + decoded_content.replace('\n', ' ').replace(' ', '') + '\n'
                    except UnicodeDecodeError:
                        # 如果解码失败，设置decoded_content为一个错误消息
                        decoded_content = " (Error: Unable to decode content as UTF-8) "
                        tree_content += ' ' * (indent + 4) + decoded_content.replace('\n', ' ').replace(' ', '') + '\n'
    return tree_content

# 提示用户输入GitHub仓库的URL
url_input = input("Please enter the GitHub repository URL: ")

# 解析输入的URL
parsed_url = urlparse(url_input)

# 从URL中提取用户名和仓库名
match = re.match(r'^/([^/]+)/([^/]+?)(?:\.git)?$', parsed_url.path)
if match:
    username, repo_name = match.groups()
    # 输出提示信息
    print("正在爬取，请稍等", end="", flush=True)
    # 计算总项目数
    total_items = count_items(username, repo_name)

    with tqdm(total=total_items, desc=f"正在写入 {repo_name}", unit="item", ncols=80) as pbar:
        # 进度条开始时，覆盖之前的提示信息
        print("\r" + " " * 80 + "\r", end="", flush=True)
        tree_content = build_file_tree(username, repo_name, pbar=pbar)

    # 将压缩后的内容写入新文件
    with open('repo_tree_with_content.min.txt', 'w', encoding='utf-8') as file:
        file.write(''.join(tree_content.split()))

    # 进度条完成后，打印完成信息
    print("\nOVER, .min.txt已刷新")
else:
    print("\nInvalid GitHub repository URL.")