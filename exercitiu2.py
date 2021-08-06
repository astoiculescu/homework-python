import requests
from flask import Flask, jsonify, json, render_template

url = "https://www.colorhexa.com/color-names"

data = requests.get(url)

format = data.text.split("tbody")

format2 = format[1].split("\n")

lista = []

for linie in format2:
    lista.append(linie.replace('\t', ''))

#lista coduri culoare
culori_tag = []

for i in lista:
    if "a href" in i:
        culori_tag.append(i.replace('<td><a href="/', '')[:6])
print(culori_tag)

#lista nume culori
culori_name = []
for i in format2:
    if  "<td style=\"background-color:" in i:
        culori_name.append(i.replace('</a></td>', '').split('>')[-1])

#print(culori_name)

#dictionar = dict(zip(culori_tag, culori_name))
dictionar = {k: v for k, v in zip(culori_tag, culori_name)}
dictionar_sortat = {k: v for k, v in sorted(dictionar.items(), key=lambda item: item[1])}

#print(dictionar_sortat)

#scrie rezultatul in fisierul json
# with open("result.json", "w") as outfile:
#      json.dump(dictionar, outfile)

#jinja 2 template
from jinja2 import Template
with open('templates/template.html') as f:
    tmpl = Template(f.read())

print(tmpl.render(item_list = dictionar_sortat))

#flask
app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template('template.html', item_list = dictionar_sortat)

if __name__ == "__main__":
    app.run(debug=True)