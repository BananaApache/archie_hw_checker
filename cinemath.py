
import requests
from bs4 import BeautifulSoup as bs

base_url = "http://cinemath.archimedean.org/index.php"
payload = {
    "username": "danielli",
    "password": "1234567890"
}


def getClasses():
    """Returns a dictionary of classes with their class code"""
    with requests.Session() as s:
        r = s.post(base_url, data=payload)
        r = s.get("http://cinemath.archimedean.org/menu.php?school=auc")
        soup = bs(r.content, 'html.parser')

        classes = {}

        for a in soup.findAll("a"):
            if str(a).split()[2].startswith("onclick=\"load_lesson("):
                classes.update({a.text: a['onclick'].split("'")[1]})
    
    return classes


def getCinemath(class_name="M7X"):
    r = requests.get(
        f"http://cinemath.archimedean.org/toc_generic.php?class_name={class_name}")
    soup = bs(r.content, 'html.parser')

    total_lessons = soup.findAll('a')[-1].text.split()[-1]

    for i in range(2, int(total_lessons) + 1):
        r = requests.get(
            f"http://cinemath.archimedean.org/load_jpeg.php?class_name=M7X&lesson_number={i}")
        soup = bs(r.content, 'html.parser')

        if soup.prettify().strip() != "There is no teacher notes for this lesson":
            for img in soup.findAll('img'):
                src = img['src']
                img_data = requests.get(src).content
                lesson = src.split("/")[7]
                with open(f'cinemath/AP_Calculus_AB/{lesson}.jpg', 'wb') as handler:
                    handler.write(img_data)


i = 1
classes = getClasses()

for cls in classes:
    print(i, " = ", cls)
    i += 1

print()
usr_num = int(input("Which class to choose? "))
class_name = list(classes.items())[usr_num - 1][1]

getCinemath(class_name=class_name)
