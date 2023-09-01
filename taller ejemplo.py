import requests
import json
import base64

null = None
url = "https://sispasvehapp.mininter.gob.pe/api-recompensas/requisitoriados/pageandfilter"
headers = {'Content-type': 'application/json'}
output_directory = "dataset2/"

person = 1

for page in range(1, 255, 1):

    data = {"pageInfo": {"page": page, "size": 4, "sortBy": "id", "direction": "desc"},
            "search": {"nombreCompleto": null, "tipoFilter": "", "alias": null,
                       "idDepartamento": "", "idProvincia": "", "idDelito": 0, "delito": "", "sexo": ""}}

    payload = json.dumps(data)
    response = requests.request("POST", url, data=payload, headers=headers)
    d = json.loads(response.text)
    for element in d["content"]:
        if "foto" in element.keys():
            image = element["foto"]
            print("Guardando la imagen " + str(person) + ".png")
            plain_data = base64.b64decode(image)
            with open(output_directory + str(person) + ".png", 'wb') as f:
                f.write(plain_data)
            person = person + 1


