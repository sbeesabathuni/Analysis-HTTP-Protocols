import sys
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
import time


def get_clear_browsing_button(driver):
    # Find the "CLEAR BROWSING BUTTON" on the Chrome settings page.
    return driver.find_element_by_css_selector('* /deep/ #clearBrowsingDataConfirm')


def clear_cache(driver, timeout=60):
    # Clear the cookies and cache for the ChromeDriver instance
    # Navigate to the settings page
    driver.get('chrome://settings/clearBrowserData')
    # Wait for the button to appear
    wait = WebDriverWait(driver, timeout)
    wait.until(get_clear_browsing_button)
    # Click the button to clear the cache
    get_clear_browsing_button(driver).click()
    # Wait for the button to be gone before returning
    wait.until_not(get_clear_browsing_button)


def get_request(driver, hostname, server_port, web_env):
    clear_cache(driver)

    url = 'http://' + hostname + ':' + server_port + '/' + web_env
    print('Timestamp ', time.time())
    print('Get Request', web_env)
    plt_start = time.time()
    driver.get(url)
    plt_end = time.time()
    plt = plt_end - plt_start
    print('PLT-------------------------------', plt)
    print('Request Finished')


def run(hostname, server_port, chromedriver_path, env):
    print('Starting chrome browser. Path: {}'.format(chromedriver_path))
    browser = webdriver.Chrome(chromedriver_path)
    web_settings = {'env1': 'lessobjectslesssize',
                    'env2': 'moreobjectslesssize',
                    'env3': 'lessobjectsmoresize',
                    'env4': 'moreobjectsmoresize'}

    print('----------------------------------------')
    for j in range(1, 5):
        print('Web Setting: ', web_settings['env' + str(j)])
        for k in range(10):
            print('-----------------{}{}-------------------'.format(j, k))
            start = time.time()
            get_request(browser, hostname, server_port, web_settings['env' + str(j)])
            time_diff = time.time() - start
            sleep_time = int(20 * (env+1) * (j + 1) - time_diff)
            time.sleep(sleep_time)


if __name__ == "__main__":
    if len(sys.argv) < 5:
        print('Incorrect command')
        sys.exit(1)

    hostname = sys.argv[1]
    server_port = sys.argv[2]
    chromedriver_path = sys.argv[3]
    env = int(sys.argv[4])

    run(hostname, server_port, chromedriver_path, env)
