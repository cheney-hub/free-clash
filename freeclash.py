import requests
from bs4 import BeautifulSoup
import base64

# Step 1: 提取网页中的 URL
url = "https://github.com/crossxx-labs/free-proxy"
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')


# 定位到包含 URL 的 <tr> 标签
table_rows = soup.find_all('tr')

# 提取 URL
vmess_url = None
for row in table_rows:
    cells = row.find_all('td')
    if len(cells) > 2 and '免费 vmess' in cells[0].text:
        vmess_url = cells[2].text.strip()  # 提取第三个 <td> 中的 URL
        break

if vmess_url:
    print(f"提取到的 URL: {vmess_url}")

    vmess_response = requests.get(vmess_url)

    # 检查请求是否成功
    if vmess_response.status_code == 200:
        # 打印返回的内容
        print("内容提取成功：")
        print(vmess_response.text)  # 或者使用 response.content 以获取字节内容
        print(vmess_response.content)

        # Step 4: 保存到免费的网络存储地址
        with open('free_clash.yaml', 'wb') as file:
            file.write(vmess_response.content)

        print("free_clash.yaml 文件已成功下载并保存。")
    else:
        print(f"请求失败，状态码：{vmess_response.status_code}")



else:
    print("未找到指定的 URL。")

    

# GitHub API URL
repo = "cheney-hub/free-clash"
file_path = "free_clash.yaml"
url = f"https://api.github.com/repos/{repo}/contents/{file_path}"

# GitHub 个人访问令牌
access_token = "key"  # 替换为您的访问令牌

# Step 1: 获取当前文件的 SHA 值
headers = {
    "Authorization": f"token {access_token}",
    "Accept": "application/vnd.github.v3+json"
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    file_info = response.json()
    sha = file_info['sha']  # 获取当前文件的 SHA 值

    # Step 2: 读取 y.yaml 文件内容
    with open('free_clash.yaml', 'rb') as file:
        yaml_content = file.read()

    # 将内容编码为 base64
    encoded_content = base64.b64encode(yaml_content).decode('utf-8')

    # 创建请求数据
    data = {
        "message": "Update free_clash.yaml file",
        "content": encoded_content,
        "sha": sha,  # 包含 SHA 值
        "branch": "main"  # 替换为您的默认分支名称
    }

    # Step 3: 发送 PUT 请求更新文件
    response = requests.put(url, json=data, headers=headers)

    if response.status_code == 200:
        print("文件已成功上传到 GitHub。")
    else:
        print("上传失败:", response.json())
else:
    print("获取文件信息失败:", response.json())

