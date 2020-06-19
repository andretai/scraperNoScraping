from bs4 import BeautifulSoup
import pip._vendor.requests as requests
import json

#FUTURELEARN

def getCat (course_link) :
  response = requests.get(course_link)
  soup = BeautifulSoup(response.text, 'html.parser')
  cat = soup.find_all('span', { 'class': 'LinkStyles-link_2v8n4 LinkStyles-left_3Y6oH LinkStyles-small_od-Hs LinkStyles-isBold_2ZPpu'})
  p = soup.find_all('span', { 'class': 'keyInfo-content_1iwSZ'})
  price = p[2].get_text()
  author = soup.find('h2', { 'class': 'heading-wrapper_1at_r heading-sBreakpointAlignmentleft_Gh9ud heading-sBreakpointSizelarge_1a0Mj heading-black_6_KIa heading-isRegular_1inPG'})
  arr = [cat[1].get_text(), price, author.get_text()]
  return arr

url = 'https://www.futurelearn.com/courses?filter_category=open&filter_course_type=open&filter_availability=started&all_courses=1'

response = requests.get(url)

soup = BeautifulSoup(response.text, 'html.parser')

courses = soup.find_all(class_='m-card Container-wrapper_GWW4X Container-grey_3ORsI')

data = {}
data['courses'] = []

i = 0

for course in courses:
  image = course.find(class_='image-cover_3Epqi')['src']
  author = course.find(class_='itemTitle-wrapper_xY1xc itemTitle-secondary_2XmB2 itemTitle-isLight_2ZMrO itemTitle-isSmall_3O3U2').get_text()
  title = course.find(class_='heading-wrapper_1at_r heading-sBreakpointAlignmentleft_Gh9ud heading-sBreakpointSizemedium_1jCHr heading-black_6_KIa heading-isCompact_-IxFi').get_text()
  desc = course.find(class_='text-wrapper_osDIP text-mediumGrey_iJRmO text-sBreakpointSizexsmall_1urEo text-sBreakpointAlignmentleft_1CA1S text-isRegular_1-QX9').get_text()
  weeks = int(course.find(class_='text-wrapper_osDIP text-coolGrey_1w2As text-sBreakpointSizexsmall_1urEo text-sBreakpointAlignmentleft_1CA1S text-isRegular_1-QX9').get_text()[0])
  hours = int(course.find(class_='text-wrapper_osDIP text-coolGrey_1w2As text-sBreakpointSizexsmall_1urEo text-sBreakpointAlignmentleft_1CA1S text-isRegular_1-QX9').get_text()[0])
  totalHrs = weeks * hours
  link = course.find(class_='link-wrapper_3VSCt')['href']
  dur = course.find_all(class_='text-wrapper_osDIP text-coolGrey_1w2As text-sBreakpointSizexsmall_1urEo text-sBreakpointAlignmentleft_1CA1S text-isRegular_1-QX9')
  duration = dur[1].get_text() + ' for ' + dur[0].get_text()
  print(i+1)
  print(title)
  print(duration)
  arr = getCat('https://futurelearn.com'+link)
  category = arr[0]
  if arr[1] == 'Free':
    price = '0'
  else:
    price = arr[1]
  author = arr[2]
  data['courses'].append({
    'id': i,
    'title': title,
    'desc': desc,
    'image': image,
    'author': author,
    'duration': totalHrs,
    'link': 'https://futurelearn.com'+link,
    'category': category,
    'duration': duration,
    'price': price,
    'platform': 'FutureLearn'
  })
  print("Category fetched: " + category)
  i += 1

with open('fl.json', 'w') as outfile:
  json.dump(data, outfile)
