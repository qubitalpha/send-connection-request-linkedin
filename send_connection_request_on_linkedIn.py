import time
import re
import csv
import string
import os

from selenium import webdriver
from selenium.webdriver.chrome.options import Options


options = Options()
# options.add_argument('--headless')
options.add_argument('--disable-gpu')  # Last I checked this was necessary.
CHROMEDRIVER_PATH = '/Users/channa/Downloads/chromedriver'
driver = webdriver.Chrome(CHROMEDRIVER_PATH, chrome_options=options)

def signin_to_linkedin():
    # Open LinkedIn 
    driver.get('https://www.linkedin.com/')

    # Load and WAIT for 3 seconds 
    time.sleep(3)

    # Find the email or username input  
    email = driver.find_element_by_id("login-email")

    # Find password input 
    password = driver.find_element_by_id("login-password")

    # Set your login Credentials  
    email.send_keys("EMAIL")
    password.send_keys("PASSWORD")

    # Find and Click upon the Login Button 
    driver.find_element_by_xpath('//*[@id="login-submit"]').click()

    # Logging In happens here and wait 
    time.sleep(10)

def get_a_person_to_connect(already_connected_list, 
                            file = './uber.txt'):
        scroll_times = 10
        if not os.path.exists(file): 
            print(file, " doesn't exist!")
            assert(False)
        
        someone_to_connect = []
        scroll_amount = 0

        time.sleep(10)
        
        # run this loop until at least 1 person is found
        while not someone_to_connect and scroll_times:
            scroll_times -= 1
            
            a = driver.find_elements_by_xpath('//*[@class="org-people-profiles-module ember-view"]/ul/li')

            for a_link in a:
                if a_link.text.endswith('Connect'):
                    full_name = a_link.text.split("\n")[0].strip('.')
                    if full_name not in already_connected_list:
                        someone_to_connect.append(a_link)
                        break

            # scroll a bit
            if not someone_to_connect:
                print("Scrolling!")
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(10)
        return someone_to_connect

def send_invitations(file, invitation_count):
    already_connected_list = [line.strip() for line in open(file, 'r')]
    someone_to_connect = get_a_person_to_connect(already_connected_list, file)

    while someone_to_connect and invitation_count:
        invitation_count -= 1
        a_link = someone_to_connect[0]
        hiring_person = a_link.text.split("\n")[0].strip('.').split()[0]
        full_name = a_link.text.split("\n")[0].strip('.')
        print("Connecting to ", full_name)

        time.sleep(5)

        # click connect
        print("Clicking Connect button!")
        try:
            a_link.find_element_by_xpath('.//button').click()
        except Exception as e:
            # auto scroll to element
            driver.execute_script("arguments[0].scrollIntoView();", a_link)
            a_link.find_element_by_xpath('.//button').click()

        time.sleep(5)

        # add note
        print("Clicking Add note")
        driver.find_element_by_xpath('//button[@class="button-secondary-large mr1"]').click()
        time.sleep(3)

        # write message
        print("Adding in my message")
        inputElement = driver.find_element_by_xpath('//textarea')
        message = "Hello " + hiring_person + my_message
        inputElement.send_keys(message)
        time.sleep(1)

        # send invitation
        print("Clicking Send invitation")
        driver.find_element_by_xpath('//button[@class="button-primary-large ml1"]').click()
        already_connected_list.append(full_name)

        # refresh the page
        time.sleep(5)

        # invitation sent list is put to uber.txt
        with open('uber.txt', 'w') as f:
            for item in set(already_connected_list):
                f.write("%s\n" % item)

        someone_to_connect = get_a_person_to_connect(already_connected_list, file)
        print("-"*45)

if __name__ == '__main__':

	my_message = ", I'm connecting to you because \
	I found a role at Uber (SWE - Data) \
	where in my skill set (I'm fluent \
	with Python and have experience on \
	new technologies around ETL) can \
	help your team reach it's goal. \
	Please kindly have a look into my \
	skills and I hope even you feel the \
	same."

	# page this script will target is all the people in a company who have put 'hiring' as there status
	custom_url = "https://www.linkedin.com/company/uber-com/people/?keywords=hiring"
	file = './uber.txt' # file to store all the invitations already sent
	invitation_count = 15 # number of invitations to send in this session

	signin_to_linkedin()

	# load the page
	driver.get(custom_url)
	time.sleep(15)

	send_invitations(file, invitation_count)

	print("Sent invitation for " +str(invitation_count)+ " people. Done and dusted!")