from subprocess import call
import time

company_list = ['zillow']

for a_company in company_list:
    print('*'*45, a_company, '*'*45)
    call(['python', "send_connection_request_on_linkedIn.py", a_company, "60", "150"])
    print('\n'*10)
    time.sleep(120)