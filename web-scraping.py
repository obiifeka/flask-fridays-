import requests
from bs4 import BeautifulSoup

res =  requests.get("https://www.codewithtomi.com") 

soup = BeautifulSoup(res.content,'html.parser')

s = soup.find_all('h2', class_='post-title')
for data  in s:
    print(data.text)
print(s)
#print(res.text)



# Create Custom Error Pages.
@app.errorhandler(404)
def page_not_found():
    return render_template("404.html"),404

@app.errorhandler(500)
def page_not_found():
    return render_template("500.html"),500