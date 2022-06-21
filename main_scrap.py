from bs4 import BeautifulSoup
import re
import pandas as pd


def number_scrap():
    fetch_style = soup.find_all('style')
    for s in fetch_style:
        if '@font-face' in s.text:
            style = s.text
            f = re.split("icon-", style)
            count = 0
            for i in f:
                if ':before' in i:
                    a = i.split(':')[0]
                    data[a] = count
                    count += 1


def find_number(l):
    number = str()
    try:
        scrap_1 = l.find('p', class_='contact-info')
        try:
            scrap_2 = scrap_1.find('b')
            for z in scrap_2:
                s = str(z)
                a = s.find('-') + 1
                b = s.find('"', a)
                num = data.get(s[a:b])
                number = number + str(num)
            return number
        except:
            scrap_2 = scrap_1.find('a')
            for z in scrap_2:
                s = str(z)
                if '<' in s:
                    a = s.find('-') + 1
                    b = s.find('"', a)
                    num = data.get(s[a:b])
                    number = number + str(num)
                else:
                    number = number + s
            return number
    except:
        return None


with open('web.html', 'r', encoding="utf8") as f:
    contents = f.read()

soup = BeautifulSoup(contents, 'lxml')
list = soup.find_all('li', class_='cntanr')

writer = pd.ExcelWriter('data.xlsx', engine='xlsxwriter')

data = dict()
number_scrap()
main_df = pd.DataFrame()

for l in list:
    name = l.find('span', class_='lng_cont_name').text
    rating = l.find('span', class_='green-box').text
    address = l.find('span', class_='cont_fl_addr').text
    website_find = l.find('span', class_='jcn')
    website = website_find.find('a').get('href')
    phone_number = find_number(l)
    # print(name)
    # print(rating)
    # print(phone_number)
    # print(data)
    # print(address)
    # print(website)

    df = pd.DataFrame({'Name': [name],
                       'Rating': [rating],
                       'Phone Number': [phone_number],
                       'Address':[address],
                       'Website':[website]})
    main_df = pd.concat([main_df, df])

main_df.to_excel(writer, sheet_name='Sheet1', index=False)
writer.save()
