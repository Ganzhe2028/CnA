from flask import Flask, request, render_template, send_file
import requests
from urllib.parse import urlparse
from base64 import b64decode
import re
import os

app = Flask(__name__)

def get_repo_contents(username, repo_name, path='', access_token=''):
    url = f'https://api.github.com/repos/{username}/{repo_name}/contents/{path}'
    headers = {'Authorization': f'token {access_token}'}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to retrieve contents: {response.status_code}")
        return None

def count_items(username, repo_name, path='', access_token=''):
    contents = get_repo_contents(username, repo_name, path, access_token)
    count = 0
    if contents:
        for item in contents:
            count += 1
            if item['type'] == 'dir':
                count += count_items(username, repo_name, item['path'], access_token)
    return count

def build_file_tree(username, repo_name, path='', indent=0, access_token=''):
    contents = get_repo_contents(username, repo_name, path, access_token)
    tree_content = ''
    if contents:
        for item in contents:
            tree_content += ' ' * indent + item['name'] + '\n'
            if item['type'] == 'dir':
                tree_content += build_file_tree(username, repo_name, item['path'], indent + 4, access_token)
            else:
                file_content_response = requests.get(item['url'], headers={'Authorization': f'token {access_token}'})
                if file_content_response.status_code == 200:
                    file_content = file_content_response.json()['content']
                    try:
                        decoded_content = b64decode(file_content).decode('utf-8')
                        tree_content += ' ' * (indent + 4) + decoded_content.replace('\n', ' ').replace(' ', '') + '\n'
                    except UnicodeDecodeError:
                        decoded_content = " (Error: Unable to decode content as UTF-8) "
                        tree_content += ' ' * (indent + 4) + decoded_content.replace('\n', ' ').replace(' ', '') + '\n'
    return tree_content

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        access_token = request.form['access_token']
        url_input = request.form['repo_url']
        parsed_url = urlparse(url_input)
        match = re.match(r'^/([^/]+)/([^/]+?)(?:\.git)?$', parsed_url.path)
        if match:
            username, repo_name = match.groups()
            total_items = count_items(username, repo_name, access_token=access_token)
            tree_content = build_file_tree(username, repo_name, access_token=access_token)
            
            # Use an absolute path to ensure the file is created correctly
            file_path = os.path.join(os.getcwd(), 'repo_content.txt')
            try:
                with open(file_path, 'w') as file:
                    file.write(tree_content)
                print(f"File created at: {file_path}")
            except Exception as e:
                print(f"Error writing file: {e}")

            return render_template('index.html', repo_url=url_input, access_token=access_token, tree_content=tree_content)
        else:
            return render_template('index.html', repo_url=url_input, access_token=access_token, tree_content="Invalid GitHub repository URL.")
    return render_template('index.html', repo_url='', access_token='', tree_content='')

@app.route('/download')
def download():
    file_path = os.path.join(os.getcwd(), 'repo_content.txt')
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    else:
        return "File not found", 404

if __name__ == '__main__':
    app.run(debug=True)
