from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

def scrape_aops_amc_selenium():
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

    
    url = "https://artofproblemsolving.com/wiki/index.php/AMC_10_Problems_and_Solutions"
    driver.get(url)

    
    time.sleep(0.5)

    
    links = driver.find_elements(By.TAG_NAME, 'a')

    
    relevant_links = [link.get_attribute('href') for link in links if link.get_attribute('href') and 
                      (link.get_attribute('href').endswith("AMC_10A") or 
                       link.get_attribute('href').endswith("AMC_10B") or 
                       link.get_attribute('href').endswith("2001_AMC_10") or 
                       link.get_attribute('href').endswith("2000_AMC_10"))]

    
    final_results = {}

    
    for link in relevant_links:
        driver.get(link)
        time.sleep(0.5)  

        
        sub_links = driver.find_elements(By.TAG_NAME, 'a')
        sub_links_filtered = [sub_link.get_attribute('href') for sub_link in sub_links if sub_link.get_attribute('href') and 
                              (sub_link.get_attribute('href').endswith("_Problems") or 
                               sub_link.get_attribute('href').endswith("_Answer_Key"))]
        
        final_results[link] = sub_links_filtered

    driver.quit()
    return final_results


if __name__ == "__main__":
    results = scrape_aops_amc_selenium()
    for key, value in results.items():
        print(f"Page: {key}")
        for v in value:
            print(f"  - {v}")
