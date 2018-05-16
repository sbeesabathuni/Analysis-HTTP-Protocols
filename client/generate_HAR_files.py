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


def get_request(driver, host_url, web_env):
    clear_cache(driver)

    time.sleep(10)
    url = host_url + '/' + web_env
    print('Get Request', web_env)
    plt_start = time.time()
    driver.get(url)
    plt = time.time() - plt_start
    print('PLT-------------------------------', plt)
    print('Request Finished')
    time.sleep(15)


def run(host_url, chromedriver_path, env):
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
            print('-----------------{}{}-------------------'.format(env, j, k))
            get_request(browser, host_url, web_settings['env' + str(j)])


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print('Incorrect command')
        sys.exit(1)

    chromedriver_path = sys.argv[1]
    host_url = sys.argv[2]
    env = sys.argv[3]

    run(host_url, chromedriver_path, env)
