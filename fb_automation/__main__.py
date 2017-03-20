import traceback
import time
from datetime import date

from selenium import webdriver
from selenium.common import exceptions
import xvfbwrapper

from selenium_util import navigate
from selenium_util import element

SEARCH_QUERY = "najdeni ključi"
GROUP_HREF = "https://www.facebook.com/najdenikljuci/?fref=nf"
FACEBOOK_HEADER_SIZE = 200
CHROME_PROFILE_PATH = "resources/chrome_profile"
CHROMEDRIVER_PATH = "resources/chromedriver"


def get_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-save-password-bubble")
    options.add_argument("user-data-dir=" + CHROME_PROFILE_PATH)
    return webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, chrome_options=options)


def get_results_url_for_current_month():
    d = date.today()
    current_year = d.year
    current_month = d.month
    current_month_str = "0" + str(current_month) if current_month < 10 else str(current_month)
    curent_dt_url_formatted = str(current_year) + "-" + current_month_str
    res = "https://www.facebook.com/search/posts/?q=Najdeni%20klju%C4%8Di&filters_rp_creation_time=%7B%22" \
          "start_month%22%3A%22{year_month}%22%2C%22end_month%22%3A%22{year_month}%22%7D"\
        .format(year_month=curent_dt_url_formatted)
    return res


def process_all_posts(driver):
    while True:
        posts = driver.find_elements_by_css_selector('[data-bt=\'{"module":"PUBLIC_POSTS"}\']>div')

        for post in posts:
            try:
                # check if the post is already shared else share it
                title_href = post.find_element_by_css_selector(".clearfix>a").get_attribute("href")
                if GROUP_HREF in title_href:
                    # [data-bt='{"module":"PUBLIC_POSTS"}']>div>div>div h5>span>span>a
                    continue
                else:
                    button_share = post.find_element_by_css_selector(".share_action_link>em")
                    element.scroll_into_view(driver, button_share, FACEBOOK_HEADER_SIZE)

                    # open menu
                    button_share.click()
                    time.sleep(3)

                    # select from dropdown "share to a page"
                    driver.find_element_by_css_selector(
                        ".uiLayer:not(.hidden_elem) .uiContextualLayer>div>div>ul>li:nth-child(5)").click()
                    time.sleep(3)   # wait for the modal to open

                    # click on the post button
                    driver.find_element_by_css_selector(
                        '.uiLayer:not(.hidden_elem) [data-testid="react_share_dialog_post_button"] '
                        '[data-intl-translation="Post"]')\
                        .click()
                    time.sleep(3)

                # load all data
                navigate.scroll_to_page_bottom(driver)
                time.sleep(3)   # wait for the posts to load
            except Exception as e:
                traceback.print_exc()
                print(2)

        # check if we loaded all data
        try:
            end_of_results = driver.find_element_by_css_selector("#browse_end_of_results_footer >div>div>div")
            if "End of results" in end_of_results.text:
                break
        except exceptions.NoSuchElementException as e:
            continue

if __name__ == "__main__":


    # we don't need to login since we're using chrome with a logged in user profile
    #driver.get("https://www.facebook.com")
    #driver.find_element_by_css_selector("#email").send_keys("terryww2@gmail.com")
    #driver.find_element_by_css_selector("#pass").send_keys("Čurimuri")
    #driver.find_element_by_id("loginbutton").click()

    # search
    """
    time.sleep(2)
    search_box = driver.find_element_by_css_selector("form .wrap")
    search_box.click()
    search_box.send_keys("najdeni ključi")
    search_box.send_keys(u'\ue007')     # send enter
    """

    check_interval = 8 * 3600

    # get the results
    while True:
        driver = get_driver()

        try:
            # check results for current year-month
            url_posts = get_results_url_for_current_month()
            driver.get(url_posts)
            process_all_posts(driver)
        except Exception as e:
            traceback.print_exc()
            print(2)
        finally:
            driver.quit()

        time.sleep(check_interval)
