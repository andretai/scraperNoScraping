from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

url = 'https://www.edx.org/course/?subject=Art%20%26%20Culture'
driver = webdriver.Chrome('D:/andre/Installers/chromedriver_win32/chromedriver.exe')
driver.get(url)

try:
  WebDriverWait(driver, 120).until(EC.presence_of_element_located((By.CLASS_NAME, 'js-card-list filtered')))
except TimeoutException:
  print('Page timed out after 120 seconds.')

soup = BeautifulSoup(driver.page_source, 'html.parser')
driver.quit()

courses = soup.find_all(class_='discovery-card course-card shadow verified')

print(len(courses))

i = 0

# for course in courses:
#   image = course.find('img')['src']
#   title = course.find(class_='title-heading ellipsis-overflowing-child').get_text()
#   author = course.find(class_='label').get_text()
#   i += 1
#   print(i, image, title, author)