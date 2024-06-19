import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

URL = "http://localhost:5000/"

driver = webdriver.Chrome(service=Service('chromedriver.exe'))


def check_item_adding():
    driver.get(URL)

    # Check the title
    title = driver.find_element(By.XPATH, '/html/body/div/h1').text
    print(f"the title is {title}")
    assert "Yuval's To-Do List" in title

    # Check the adding task
    task_title = driver.find_element(By.XPATH, '/html/body/div/form/input')
    task_title.send_keys("item1")

    task_description = driver.find_element(By.XPATH, '/html/body/div/form/textarea')
    task_description.send_keys("the first item")

    add_task_button = driver.find_element(By.XPATH, '/html/body/div/form/button')
    add_task_button.click()

    # Check that the item was added -
    tasks = driver.find_elements(By.XPATH, "//ul/li")
    task_texts = [task.text for task in tasks]
    print(f"Current tasks: {task_texts}")

    task_found = False
    for task_text in task_texts:
        if "item1" in task_text and "the first item" in task_text:
            task_found = True
            break

    assert task_found

    return True


def check_item_deleting():
    # Check the deleting task
    delete_item_button = driver.find_element(By.XPATH, '/html/body/div/ul/li/form/button')
    delete_item_button.click()

    WebDriverWait(driver, 10).until(EC.staleness_of(delete_item_button))

    # Check that the item was deleted
    tasks_after_deletion = driver.find_elements(By.XPATH, "//ul/li")
    task_texts_after_deletion = [task.text for task in tasks_after_deletion]
    print(f"Current tasks after deletion: {task_texts_after_deletion}")

    assert "item1" not in task_texts_after_deletion

    return True



def main_function():
    if check_item_adding() and check_item_deleting():
        print('Test passed: adding and deleting tasks worked successfully')
    else:
        print("Test failed")


    driver.quit()


main_function()




















