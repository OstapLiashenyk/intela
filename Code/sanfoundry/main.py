import requests

cookies = {
    '_ga': 'GA1.1.336755034.1700077105',
    'JSESSIONID': '853F4D7B8F8353F62DC872ECC7DF3A62',
    '_ga_SP1BF98DYC': 'GS1.1.1701256655.4.1.1701256718.0.0.0',
}

headers = {
    'authority': 'www.pskills.org',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en,uk;q=0.9,en-US;q=0.8,uk-UA;q=0.7',
    'cache-control': 'max-age=0',
    'content-type': 'application/x-www-form-urlencoded',
    # 'cookie': '_ga=GA1.1.336755034.1700077105; JSESSIONID=853F4D7B8F8353F62DC872ECC7DF3A62; _ga_SP1BF98DYC=GS1.1.1701256655.4.1.1701256718.0.0.0',
    'origin': 'https://www.pskills.org',
    'referer': 'https://www.pskills.org/test.jsp?test=coretest1',
    'sec-ch-ua': '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
}

data = {
    'mins': '24',
    'secs': '30',
}

response = requests.post('https://www.pskills.org/testresult.jsp', cookies=cookies, headers=headers, data=data)
print(response)