import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

def read_links_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    links_dict = {}
    current_key = None
    
    for line in lines:
        line = line.strip()
        if line.startswith("Page:"):
            current_key = line.split("Page: ")[1].strip()
            links_dict[current_key] = []
        elif line.startswith("-"):
            if current_key:
                links_dict[current_key].append(line[2:].strip())
    
    return links_dict

def save_html_content_selenium(url, dir_path, filename):
    if os.path.exists(dir_path + "/" + filename):
        return
    driver.get(url)
    time.sleep(0.1)  
    
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    content = soup.find(class_='mw-parser-output')
    
    if content:
        file_path = os.path.join(dir_path, filename)
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(str(content))
    

def process_links(links_dict):
    for page_url, links in links_dict.items():
        last_segment = page_url.split('/')[-1]
        dir_path = os.path.join('AMC/htmls', last_segment)
        os.makedirs(dir_path, exist_ok=True)
        
        for link in links:
            if link.endswith("_Problems"):
                save_html_content_selenium(link, dir_path, 'problems.html')
            if link.endswith("_Answer_Key"):
                save_html_content_selenium(link, dir_path, 'answers.html')

if __name__ == "__main__":
    links_path = 'AMC/links.txt'
    links_dict = read_links_file(links_path)
    process_links(links_dict)

    driver.quit()
