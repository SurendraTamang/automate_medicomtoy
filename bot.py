import requests
from anticaptchaofficial.recaptchav2proxyless import *
import json
import csv
import datetime
import os
from credentails import anticapcha_key, anticaptcha_website_key
# survey 

#### DONT SHARE YOUR ANTICAPTCHA CREDENTIALS TO OTHERS 


## You can change the url and time from above 
survey_url = "http://www.medicomtoy.tv/blog/?p=65050"
survey_option = "5/22（土）　12：30-12：55"
# input file
input_file = "input_data.csv"

#### Remove the issue sith capctha



today = datetime.date.today()
yesterday = today - datetime.timedelta(days=1)
yesterday = yesterday.strftime('%Y-%m-%d')
today = today.strftime('%Y-%m-%d')

def get_proxy_cursor():
    f = open("proxy_cursor", "r")
    cursor = f.read()
    f.close()
    increment_proxy_cursor()
    return int(cursor)

def update_proxy_cursor(cursor):
    f = open("proxy_cursor", "w")
    cursor = f.write(str(cursor))
    f.close()
    return

def increment_proxy_cursor():
    f = open("proxy_cursor", "r")
    cursor = f.read()
    f.close()
    cursor = int(cursor) + 1
    update_proxy_cursor(cursor)

def get_proxy_list():
    f = open("proxies.txt", "r")
    proxies = f.read().splitlines()
    f.close()
    return proxies

def get_proxy():
    proxy_list = get_proxy_list()
    proxies_count = len(proxy_list)
    proxy = []

    cursor = get_proxy_cursor()

    if cursor >= proxies_count:
        cursor = 0
        update_proxy_cursor(cursor + 1)
    proxy_string = proxy_list[cursor]
    proxy.append(str(proxy_string.split(":")[0]))
    proxy.append(int(proxy_string.split(":")[1]))
    proxy.append(str(proxy_string.split(":")[2]))
    proxy.append(str(proxy_string.split(":")[3]))
    return proxy



def read_records_from_file(infile):
    parent_dir_path = os.path.dirname(os.path.realpath(__file__))
    filepath = os.path.join(parent_dir_path, infile)
    mode = "r"
    with open(filepath, mode, encoding='utf-8-sig') as csvfile:
        csv_reader = csv.DictReader(csvfile, quoting=csv.QUOTE_ALL)
        records = list(csv_reader)
    return records


def get_captch_response():
    '''Returns the required captca
    '''
    print("Captcha is trying to solved")
    solver = recaptchaV2Proxyless()
    solver.set_verbose(1)
    solver.set_key(anticaptcha_key)
    solver.set_website_url(survey_url)
    solver.set_website_key(anticaptcha_website_key)

    g_response = solver.solve_and_return_solution()
    if g_response != 0:
        print("g-response: " + g_response)
        print("Captcha solved")
        return g_response
    else:
        print("task finished with error " + solver.error_code)
        return None

def start_posting(record):
    g_response = get_captch_response()
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',

    }
    params = (
        ('p', '65050'),
    )
    first_name = record.get("First Name")
    last_name = record.get("Last Name")
    dob = record.get("Date of Birth (YYYY / MM / DD)")
    zip_code = record.get("Zip Code")
    address1 = record.get("Address 1 Prefecture")
    address2 = record.get("Address 2 City")
    address3 = record.get("Address 3 Building")
    phone_number = record.get("Phone number")
    email = record.get("Email address")
    email_confirm = record.get("Email address (for confirmation)")

    data = {
        '_wpcf7': '65334',
        '_wpcf7_version': '4.4.2',
        '_wpcf7_locale': 'ja',
        '_wpcf7_unit_tag': 'wpcf7-f65334-p65050-o1',
        '_wpnonce': '7fcd7a10f3',
        'visittime': f'{survey_option}',
        # 5/23（日）　18：00-18：25

        'name': f'{first_name} {last_name}',
        'birthdate': dob,
        'postalcode':zip_code,
        'address1': address1,
        'address2': address2,
        'address3': address3,
        'tel': phone_number,
        'email': email,
        'email2': email_confirm,
        'g-recaptcha-response': g_response,
        'consent[]': '注意事項を確認し、内容に同意します。/I agreed order terms、conditions',
        #'date-210522_1-6': datetime.datetime.today().strftime('%Y-%m-%d'),
        'date-210522_1-6': f'{today}',
        '_wpcf7_is_ajax_call': '1'
        }
    proxy_len = get_proxy()
    #IT will change it to our 
    proxy_format = f'{proxy_len[2]}:{proxy_len[3]}@{proxy_len[0]}:{proxy_len[1]}'
    proxies = {'http':'http://'+proxy_format,'https':'https://'+proxy_format}
    try:
        response = requests.post('http://www.medicomtoy.tv/blog/', headers=headers, params=params, data=data,proxies=proxies, verify=False)
    except:
        with open('not-success.txt','a') as sf:
            sf.write(f'{email} -- error due to proxy\n')
        response = None
    breakpoint()
    requests.get('https://httpbin.org/ip',proxies=proxies).text
    if response:
        if '"mailSent":true' in response.text:
            with open('success.txt','a') as sf:
                sf.write(f'{email}\n')
        else:
            with open('not-success.txt','a') as sf:
                sf.write(f'{email}\n')
def main():
    records = read_records_from_file(input_file)
    process_records(records)
def process_records(records):
    for record in records:

        start_posting(record)

if __name__ == '__main__':
    print("Main File started")
    main()