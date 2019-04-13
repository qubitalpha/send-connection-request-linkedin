from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import time
import sys

# imports related to this project
import utils

if __name__ == '__main__':
    current_company, invitation_count, scroll_times = utils.get_command_line_arguments(sys.argv)
    
    ## open browser
    options = Options()
    # options.add_argument('--headless')
    options.add_argument('--disable-gpu')  # Last I checked this was necessary.
    CHROMEDRIVER_PATH = '/Users/channa/Downloads/chromedriver'
    driver = webdriver.Chrome(CHROMEDRIVER_PATH, chrome_options=options)

    ## signin
    utils.signin_to_linkedin(driver)

    my_message, url, file = current_company['my_message'], current_company['url'], current_company['file']

    ## load the company page
    driver.get(url)
    time.sleep(15)

    ## send invitations
    ret_invitation_count = utils.send_invitations(url, file, my_message, invitation_count, scroll_times, driver)

    if ret_invitation_count == 0:
        print("Sent invitation for " +str(invitation_count)+ " people. Done and dusted!")
    else:
        print("Sent invitation for " +str(invitation_count - ret_invitation_count)+ \
            ". Could not find " +str(ret_invitation_count)+ " more people.")
    driver.quit()