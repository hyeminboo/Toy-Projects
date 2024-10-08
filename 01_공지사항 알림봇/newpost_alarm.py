import requests
import subprocess
from bs4 import BeautifulSoup

url = "https://ai.ewha.ac.kr/deptai/board/notice.do" # 이화여대 인공지능학과 공지사항 게시판

def load_latest_num(file_path):
    try:
        with open(file_path, 'r') as file:
            latest_num = int(file.read().strip())
            return latest_num
    except (FileNotFoundError, ValueError):
        return 90

def save_latest_num(file_path, latest_num):
    with open(file_path, 'w') as file:
        file.write(str(latest_num))


file_path = '/Users/boohyemin/Desktop/latest_num.txt'
latest_num = load_latest_num(file_path)


r = requests.get(url)

soup = BeautifulSoup(r.text, 'html.parser')

rows = soup.find_all('tr', attrs={'class': 'b-top-box'})

for row in rows:
    numbers = row.find_all('td', attrs={'class': 'b-num-box'})
    for num in numbers:
        n = num.get_text(strip=True)
        if n.isdigit():
            if int(n) > latest_num:
                title_tag = row.find('a', class_='b-title')
                title = title_tag.get_text(strip=True)
                #href = title_tag['href']
                print(title)
                subprocess.run(['osascript', '-e', f'display notification "{title}"'])
                latest_num = int(n)
            else:
                break
        else:
            continue
        break

save_latest_num(file_path, latest_num)

print(latest_num)