import requests
from bs4 import BeautifulSoup

url = "https://www.glassdoor.com/Interview/marne-la-vallee-data-engineer-interview-questions-SRCH_IL.0,15_IC4990386_KO16,29.htm"
session = requests.Session()

page = session.get(url, headers={
    'Accept': 'text/html',
    'Cookie': 'gdsid=1699274867516:1699274867516:94B9FAAB923E1DB7E35B2CE1ACB9D4A8; asst=1699274867.0; gdId=e46c59bb-b682-4279-80e6-ef9c649b566c; bs=czDzzSjVT3vUs-hPx41siQ:czK73ChsSlT6JmrENVevCuLt0lFXRGGWzm-i3KLngoRuLu-efUw5A2-fmjQZDnfuuIUu047CX54BAZFQnGHImILjBBclT9XZRrwV9fP5ax0:v4envVAIWhjRyWKfTa9kmo6i4GA7OlBdjK7KR2oMIhI; __cf_bm=N7vz4CshcxnGQqiZXBkZwIkHULjGgBAHXx5IpkKF8bc-1699274867-0-AVHiR64ioL+/5kfBGcBkElOkeN3uSYjFcG4f7h7ezkt1bd/T1+Dsj/18r5wHX4CKtuuueHQsVJ+8eVbayCX5YxnYaG6kbmukZWyQDXN07C9F; _cfuvid=ICNLxzuUB_qEzZkEagqryHV2dFoiaTG6USMxN5yL8Ow-1699274867618-0-604800000; GSESSIONID=undefined; rl_user_id=RudderEncrypt%3AU2FsdGVkX1%2B9O8FI%2FEqgeke4vJrbNMxF5Yh6CPsnglo%3D; rl_trait=RudderEncrypt%3AU2FsdGVkX19%2Bw8k%2FRFNn%2FgWSLEjqCTJ4Ql1lTXYAbuY%3D; rl_group_id=RudderEncrypt%3AU2FsdGVkX19lEbGsGksP77r5JXvIUqR9teU8wEbavOs%3D; rl_group_trait=RudderEncrypt%3AU2FsdGVkX1%2F%2Be2%2FvEnXKIQ5pgA5VPEBB3gXH2jM9dH4%3D; rl_page_init_referrer=RudderEncrypt%3AU2FsdGVkX1%2Frntl41Hwod8Tmyi1qEpvvq2mLiK4GioU%3D; rl_page_init_referring_domain=RudderEncrypt%3AU2FsdGVkX1%2FNyhyPa9j%2FVRXOrfgk71rl3zyS5f502eU%3D; rsReferrerData={"currentPageRollup":"/interview/interview-questions-srch","previousPageRollup":null,"currentPageAbstract":"/Interview/[LOC]-[OCC]-interview-questions-SRCH_[PRM].htm","previousPageAbstract":null,"currentPageFull":"https://www.glassdoor.com/Interview/marne-la-vallee-data-engineer-interview-questions-SRCH_IL.0,15_IC4990386_KO16,29.htm","previousPageFull":null}; rl_anonymous_id=RudderEncrypt%3AU2FsdGVkX1%2BN2YmgggLI4rKI2Vcfvgsn%2FVTP%2FHnQTRYbBZkkL19gfSDeXs6fZJqNJllU5kN0TtpGSi5BTOf4gw%3D%3D; rsSessionId=1699274869070; rl_session=RudderEncrypt%3AU2FsdGVkX19kkHjE24iMyJ1KoZVpFzJo4%2BIEqkyybnuepB6UavjOWkXgXYTyM1Kc6ukbH7esMD3RN%2FSGcskdjIG2f%2F%2FBPfIhOovidJ0uRIIQrJS%2BjnDTTkWAIv%2FLj3BUbdtppAvZEzKTQEV0Y0Ueqw%3D%3D; _ga=GA1.2.385605950.1699274870; _gid=GA1.2.353318523.1699274870; _dc_gtm_UA-2595786-1=1; _optionalConsent=true; _gcl_au=1.1.1996775636.1699274870; _rdt_uuid=1699274870524.61a2112e-4ba7-4503-8ad5-70b6759cdacc; __pdst=bc3b04ac2f6a414994ff2a6f7db89411; _fbp=fb.1.1699274870568.586206113; _tt_enable_cookie=1; _ttp=l-_1fXhFAF5HKQ4AUTYTlMPtpjJ; _pin_unauth=dWlkPU1ERXlNRFkxWldNdE1tSXhaUzAwTXpOaExUaGtNemN0T0dRMlptWTRaR05oTmpVNQ; ki_t=1699274871127%3B1699274871127%3B1699274871127%3B1%3B1; ki_r=; OptanonConsent=isGpcEnabled=0&datestamp=Mon+Nov+06+2023+14%3A48%3A06+GMT%2B0200+(Eastern+European+Standard+Time)&version=202306.2.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=6ea74077-9560-4430-8d32-d7f82f7b9968&interactionCount=1&landingPath=https%3A%2F%2Fwww.glassdoor.com%2FInterview%2Fmarne-la-vallee-data-engineer-interview-questions-SRCH_IL.0%2C15_IC4990386_KO16%2C29.htm&groups=C0001%3A1%2CC0003%3A1%2CC0002%3A1%2CC0004%3A1%2CC0017%3A1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    'Accept-Encoding':'gzip, deflate, br',
    'Accept-Language':'en',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Ch-Ua' : '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"'
})

print(page.status_code)
print(page.text)

with open('text.html', 'w') as f :
    f.write(page.text)


