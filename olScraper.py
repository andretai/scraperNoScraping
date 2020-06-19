from bs4 import BeautifulSoup
import pip._vendor.requests as requests
import json
import time



def getOthers(link):
  if(link == 'javascript:void(0)'):
    return 
  response = requests.get(link)
  soup = BeautifulSoup(response.text, 'html.parser')
  image = soup.find_all("img")[5]['src']
  if hasattr(soup.find("p", { 'property':'schema:description' }), 'get_text'):
    desc = soup.find("p", { 'property':'schema:description' }).get_text()
  else:
    desc = 'No description.'
  result = [image, desc]
  return result

def getDuration(duration):
  count = 0
  for dur in duration:
    if(count == 1):
      return dur.get_text().strip() + " hours"
    count += 1

url = "https://www.open.edu/openlearn/free-courses/full-catalogue"

response = requests.get(url)

soup = BeautifulSoup(response.text, 'html.parser')

categories = soup.find_all(class_="dropdown-box")

data = {}
data['courses'] = []

count = 0

for category in categories:
  cat = category.find("h2").get_text()
  print("Category: " + cat)
  courses = category.find_all("tr")
  for course in courses:
    if(course == courses[0]):
      continue
    title = course.find("a").get_text()
    link = "https://www.open.edu" + course.find("a")['href']
    duration = getDuration(course.find_all("td"))
    details = getOthers(link)
    image = details[0]
    desc = details[1]
    author = 'Open University'
    price = '0'
    print('Writing ' + title + ' into ol.json...')
    data['courses'].append({
      'id':count,
      'title':title,
      'desc':desc,
      'image':image,
      'author':author,
      'duration':duration,
      'link':link,
      'category':cat,
      'price':price,
      'platform':'OpenLearn'
    })
    count += 1
  time.sleep(5)

with open('ol.json', 'w') as outfile:
  json.dump(data, outfile)
