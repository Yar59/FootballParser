import numpy
from time import sleep
from pprint import pprint

import pandas
from environs import Env
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service


def main():
    env = Env()
    env.read_env()
    chromedriver_path = env('CHROME_DRIVER_PATH')
    output_file_path = env('OUTPUT_FILE_PATH')

    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    service = Service(chromedriver_path)
    browser = webdriver.Chrome(service=service, options=chrome_options)

    link = 'https://www.flashscore.com.ua/'
    browser.get(link)
    with open('classnames.txt', 'r') as file:
        class_names = file.read()

    class_content = browser.find_elements(By.CLASS_NAME, class_names)
    table_content = [element.text.splitlines() for element in class_content]
    pprint(table_content)

    dataframe = pandas.DataFrame(
        table_content,
        columns=[
            'status',
            'first_team',
            'second_team',
            'goals_one',
            'goals_two',
            'not_used',
            'not_used',
            'not_used',
        ]
    ).drop(['not_used', ], axis=1)

    dataframe = dataframe.query("status == 'Завершен'")
    dataframe.to_excel(output_file_path, index=False)


if __name__ == '__main__':
    main()
