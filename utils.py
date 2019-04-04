import time
import os
import sys

from lookup_dict import lookup_dict

def get_command_line_arguments(input_argument_list):
    # get company name
    if len(input_argument_list) >= 2 and input_argument_list[1] not in lookup_dict.keys():
        print(input_argument_list[1], "not in DB.")
        print("2nd argument should be company name. It should also be in DB.")
        sys.exit()
    company = input_argument_list[1]
    current_company = lookup_dict[company]

    # defaults to send 10 invitation
    invitation_count = 10
    if len(input_argument_list) >= 3:
        try:
            invitation_count = int(input_argument_list[2])
        except ValueError:
            print("3rd argument should be integer. Now setting invitation_count to 10.")

    # defaults to scroll 10 times
    scroll_times = 10
    if len(input_argument_list) >= 4:
        try:
            scroll_times = int(input_argument_list[3])
        except ValueError:
            print("4th argument should be integer. Now setting scroll_times to 10.")

    return current_company, invitation_count, scroll_times

def signin_to_linkedin(driver):
    # Open LinkedIn 
    driver.get('https://www.linkedin.com/')

    # Load and WAIT for 3 seconds 
    time.sleep(3)

    # Find the email or username input  
    email = driver.find_element_by_id("login-email")

    # Find password input 
    password = driver.find_element_by_id("login-password")

    # Set your login Credentials  
    email.send_keys('xxxxx')
    password.send_keys('xxxxx')


    # Find and Click upon the Login Button 
    driver.find_element_by_xpath('//*[@id="login-submit"]').click()

    # Logging In happens here and wait 
    time.sleep(10)

def get_a_person_to_connect(already_connected_list, 
                            file, driver, scroll_times):
        
        someone_to_connect = []
        scroll_amount = 0

        time.sleep(10)
        
        keywords_in_status_list = ['hiring', 'recruiting', 'technical recruiter', \
                                    'data engineering manager']
        # run this loop until at least 1 person is found
        while not someone_to_connect and scroll_times:
            scroll_times -= 1
            
            a = driver.find_elements_by_xpath('//*[@class="org-people-profiles-module ember-view"]/ul/li')

            for a_link in a:
                if a_link.text.endswith('Connect') and any(kw in a_link.text.lower() for kw in keywords_in_status_list):
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

def send_invitations(url, file, my_message, invitation_count, scroll_times, driver):
    if not os.path.exists(file): 
        print(file, " doesn't exist. Creating one.")
        with open(file, 'w'): pass
    already_connected_list = [line.strip() for line in open(file, 'r')]
    someone_to_connect = get_a_person_to_connect(already_connected_list, file, driver, scroll_times)

    while someone_to_connect and invitation_count:
        invitation_count -= 1
        a_link = someone_to_connect[0]
        hiring_person = a_link.text.split("\n")[0].strip('.').split()[0]
        full_name = a_link.text.split("\n")[0].strip('.')
        print("Connecting to ", full_name)

        time.sleep(5)
        # click connect
        print("Click connect button!")
        try:
            a_link.find_element_by_xpath('.//button').click()
        except Exception as e:
            # auto scroll to element
            driver.execute_script("arguments[0].scrollIntoView();", a_link)
            time.sleep(3)
            a_link.find_element_by_xpath('.//button').click()

        time.sleep(5)

        # add note
        print("Click add note")

        try:
            driver.find_element_by_xpath('//button[@class="button-secondary-large mr1"]').click()
        except:
            driver.find_element_by_xpath('//button[@class="artdeco-button artdeco-button--secondary artdeco-button--3 mr1"]').click()
        time.sleep(3)

        # write message
        print("Adding in my message")
        inputElement = driver.find_element_by_xpath('//textarea')
        message = "Hi " + hiring_person + my_message
        inputElement.send_keys(message)
        time.sleep(1)

        # send invitation
        print("Click send invitation")
        try:
            driver.find_element_by_xpath('//button[@class="button-primary-large ml1"]').click()
        except:
            driver.find_element_by_xpath('//button[@class="artdeco-button artdeco-button--3 ml1"]').click()
        already_connected_list.append(full_name)

        # refresh the page
        time.sleep(5)
#         driver.get("https://www.linkedin.com/company/uber-com/people/?keywords=hiring")
#         time.sleep(15)
#         a = driver.find_elements_by_xpath('//*[@class="org-people-profiles-module ember-view"]/ul/li')

        # invitation sent list is put to uber.txt
        with open(file, 'w') as f:
            for item in set(already_connected_list):
                f.write("%s\n" % item)

        someone_to_connect = get_a_person_to_connect(already_connected_list, file, driver, scroll_times)
        print("-"*45)
    return invitation_count