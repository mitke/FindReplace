import zipfile
import glob
import os
import requests
from requests.auth import HTTPBasicAuth
import re


def main():

    ### download zip file from rfzo portal
    file_url = "http://portal.rfzo.rs/zus/EFsekundarna/XMLPrikazSifarnikazaSZZ.zip"
    username = "zus"
    password = "ustanova"
    download_file(file_url, username, password)

    ### Extrakt two files
    zip_file_path = "downloaded_file.zip"
    file_in_zip = 'S_Sekundar_'
    file_in_zip1 = "Pozicija_Sekunda"
    where_to_unzip = "./"
    unzip(zip_file_path, where_to_unzip, file_in_zip)
    unzip(zip_file_path, where_to_unzip, file_in_zip1)

    ### remove archive
    os.remove(zip_file_path)

    ### Change S_Sekundar... file
    file_path = glob.glob('S_Sekundar_*.xml')[0]
    file_path_poz = glob.glob('Pozicija_Sekundar_*.xml')[0]
    output_zip_file = os.path.splitext(os.path.basename(file_path))[0] + '.zip'
    output_zip_file_poz = os.path.splitext(os.path.basename(file_path_poz))[0] + '.zip'

    replacements = {
        'Z00</ID_dijagnoza>\n    <NazivD>Opšti pregled i ispitivanje osoba bez tegoba ili postavljene dijagnoze</NazivD>\n    <NazivLatinski>Opšti pregled i ispitivanje osoba bez tegoba ili postavljene dijagnoze</NazivLatinski>\n    <Vazi_od>2008-12-24T16:51:13.543+01:00</Vazi_od>': 'Z00</ID_dijagnoza>\n    <NazivD>Opšti pregled i ispitivanje osoba bez tegoba ili postavljene dijagnoze</NazivD>\n    <NazivLatinski>Opšti pregled i ispitivanje osoba bez tegoba ili postavljene dijagnoze</NazivLatinski>\n    <Vazi_od>2008-12-24T16:51:13.543+01:00</Vazi_od>\n    <Vazi_do>2015-06-28T00:00:00+01:00</Vazi_do>',
        'Z01</ID_dijagnoza>\n    <NazivD>Drugi posebni pregledi i ispitivanja osoba bez tegoba ili ranije dijagnoze</NazivD>\n    <NazivLatinski>Drugi posebni pregledi i ispitivanja osoba bez tegoba ili ranije dijagnoze</NazivLatinski>\n    <Vazi_od>2008-12-24T16:51:13.543+01:00</Vazi_od>': 'Z01</ID_dijagnoza>\n    <NazivD>Drugi posebni pregledi i ispitivanja osoba bez tegoba ili ranije dijagnoze</NazivD>\n    <NazivLatinski>Drugi posebni pregledi i ispitivanja osoba bez tegoba ili ranije dijagnoze</NazivLatinski>\n    <Vazi_od>2008-12-24T16:51:13.543+01:00</Vazi_od>\n    <Vazi_do>2015-06-28T00:00:00+01:00</Vazi_do>',
        'Z03</ID_dijagnoza>\n    <NazivD>Medicinsko posmatranje i praćenje zbog sumnje na neke bolesti ili stanja</NazivD>\n    <NazivLatinski>Medicinsko posmatranje i praćenje zbog sumnje na neke bolesti ili stanja</NazivLatinski>\n    <Vazi_od>2008-12-24T16:51:13.543+01:00</Vazi_od>': 'Z03</ID_dijagnoza>\n    <NazivD>Medicinsko posmatranje i praćenje zbog sumnje na neke bolesti ili stanja</NazivD>\n    <NazivLatinski>Medicinsko posmatranje i praćenje zbog sumnje na neke bolesti ili stanja</NazivLatinski>\n    <Vazi_od>2008-12-24T16:51:13.543+01:00</Vazi_od>\n    <Vazi_do>2015-06-28T00:00:00+01:00</Vazi_do>',
        'Z000</ID_dijagnoza>\n    <NazivD>Opšti medicinski pregled</NazivD>\n    <NazivLatinski>Opšti medicinski pregled</NazivLatinski>\n    <Vazi_od>2008-12-24T16:51:13.543+01:00</Vazi_od>': 'Z000</ID_dijagnoza>\n    <NazivD>Opšti medicinski pregled</NazivD>\n    <NazivLatinski>Opšti medicinski pregled</NazivLatinski>\n    <Vazi_od>2008-12-24T16:51:13.543+01:00</Vazi_od>\n    <Vazi_do>2015-06-28T00:00:00+01:00</Vazi_do>',
        'Z001</ID_dijagnoza>\n    <NazivD>Rutinski zdravstveni pregled dece</NazivD>\n    <NazivLatinski>Rutinski zdravstveni pregled dece</NazivLatinski>\n    <Vazi_od>2008-12-24T16:51:13.543+01:00</Vazi_od>': 'Z001</ID_dijagnoza>\n    <NazivD>Rutinski zdravstveni pregled dece</NazivD>\n    <NazivLatinski>Rutinski zdravstveni pregled dece</NazivLatinski>\n    <Vazi_od>2008-12-24T16:51:13.543+01:00</Vazi_od>\n    <Vazi_do>2015-06-28T00:00:00+01:00</Vazi_do>',
        'Z008</ID_dijagnoza>\n    <NazivD>Drugi opšti pregledi</NazivD>\n    <NazivLatinski>Drugi opšti pregledi</NazivLatinski>\n    <Vazi_od>2008-12-24T16:51:13.543+01:00</Vazi_od>': 'Z008</ID_dijagnoza>\n    <NazivD>Drugi opšti pregledi</NazivD>\n    <NazivLatinski>Drugi opšti pregledi</NazivLatinski>\n    <Vazi_od>2008-12-24T16:51:13.543+01:00</Vazi_od>\n    <Vazi_do>2015-06-28T00:00:00+01:00</Vazi_do>',
        'Z016</ID_dijagnoza>\n    <NazivD>Radiološki pregled, neklasifikovan na drugom mestu</NazivD>\n    <NazivLatinski>Radiološki pregled, neklasifikovan na drugom mestu</NazivLatinski>\n    <Vazi_od>2008-12-24T16:51:13.543+01:00</Vazi_od>': 'Z016</ID_dijagnoza>\n    <NazivD>Radiološki pregled, neklasifikovan na drugom mestu</NazivD>\n    <NazivLatinski>Radiološki pregled, neklasifikovan na drugom mestu</NazivLatinski>\n    <Vazi_od>2008-12-24T16:51:13.543+01:00</Vazi_od>\n    <Vazi_do>2015-06-28T00:00:00+01:00</Vazi_do>',
        'Z017</ID_dijagnoza>\n    <NazivD>Laboratorijski pregledi</NazivD>\n    <NazivLatinski>Laboratorijski pregledi</NazivLatinski>\n    <Vazi_od>2008-12-24T16:51:13.543+01:00</Vazi_od>': 'Z017</ID_dijagnoza>\n    <NazivD>Laboratorijski pregledi</NazivD>\n    <NazivLatinski>Laboratorijski pregledi</NazivLatinski>\n    <Vazi_od>2008-12-24T16:51:13.543+01:00</Vazi_od>\n    <Vazi_do>2015-06-28T00:00:00+01:00</Vazi_do>',
        'Z018</ID_dijagnoza>\n    <NazivD>Drugi označeni posebni pregledi</NazivD>\n    <NazivLatinski>Drugi označeni posebni pregledi</NazivLatinski>\n    <Vazi_od>2008-12-24T16:51:13.543+01:00</Vazi_od>': 'Z018</ID_dijagnoza>\n    <NazivD>Drugi označeni posebni pregledi</NazivD>\n    <NazivLatinski>Drugi označeni posebni pregledi</NazivLatinski>\n    <Vazi_od>2008-12-24T16:51:13.543+01:00</Vazi_od>\n    <Vazi_do>2015-06-28T00:00:00+01:00</Vazi_do>',
        'Z019</ID_dijagnoza>\n    <NazivD>Posebni pregled, neoznačen</NazivD>\n    <NazivLatinski>Posebni pregled, neoznačen</NazivLatinski>\n    <Vazi_od>2008-12-24T16:51:13.543+01:00</Vazi_od>': 'Z019</ID_dijagnoza>\n    <NazivD>Posebni pregled, neoznačen</NazivD>\n    <NazivLatinski>Posebni pregled, neoznačen</NazivLatinski>\n    <Vazi_od>2008-12-24T16:51:13.543+01:00</Vazi_od>\n    <Vazi_do>2015-06-28T00:00:00+01:00</Vazi_do>',
        'Z038</ID_dijagnoza>\n    <NazivD>Posmatranje zbog sumnje na druge bolesti ili stanja</NazivD>\n    <NazivLatinski>Posmatranje zbog sumnje na druge bolesti ili stanja</NazivLatinski>\n    <Vazi_od>2008-12-24T16:51:13.543+01:00</Vazi_od>': 'Z038</ID_dijagnoza>\n    <NazivD>Posmatranje zbog sumnje na druge bolesti ili stanja</NazivD>\n    <NazivLatinski>Posmatranje zbog sumnje na druge bolesti ili stanja</NazivLatinski>\n    <Vazi_od>2008-12-24T16:51:13.543+01:00</Vazi_od>\n    <Vazi_do>2015-06-28T00:00:00+01:00</Vazi_do>',
        'Z039</ID_dijagnoza>\n    <NazivD>Posmatranje zbog sumnje na bolesti ili stanja, neoznačeno</NazivD>\n    <NazivLatinski>Posmatranje zbog sumnje na bolesti ili stanja, neoznačeno</NazivLatinski>\n    <Vazi_od>2008-12-24T16:51:13.543+01:00</Vazi_od>': 'Z039</ID_dijagnoza>\n    <NazivD>Posmatranje zbog sumnje na bolesti ili stanja, neoznačeno</NazivD>\n    <NazivLatinski>Posmatranje zbog sumnje na bolesti ili stanja, neoznačeno</NazivLatinski>\n    <Vazi_od>2008-12-24T16:51:13.543+01:00</Vazi_od>\n    <Vazi_do>2015-06-28T00:00:00+01:00</Vazi_do>'
    }
    find_replace(file_path, replacements)

    ### Zip two xml files
    make_zip(file_path, output_zip_file)
    make_zip(file_path_poz, output_zip_file_poz)

    ### remove files
    os.remove(file_path)
    os.remove(file_path_poz)


def download_file(url, user, passw):
    auth = HTTPBasicAuth(user, passw)
    response = requests.get(url, auth=auth)

    if response.status_code == 200:
        file_content = response.content
        with open("downloaded_file.zip", "wb") as f:
            f.write(file_content)
        print("File downloaded successfully.")
    else:
        print("Failed to download file. Status code:", response.status_code)


def unzip(zip_file_path, where_to_unzip, file_in_zip):
    with zipfile.ZipFile(zip_file_path, "r") as zipFile:
        files = zipFile.namelist()
        for file in files:
            fileName, extension = os.path.splitext(file)
            patern = re.escape(file_in_zip)
            match = re.search(patern, fileName)
            if match:
                zipFile.extract(file, where_to_unzip)

def find_replace(file_path, replacements):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    for old, new in replacements.items():
        content = content.replace(old, new)

    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)


def make_zip(file_path, output_zip_file):
    with zipfile.ZipFile(output_zip_file, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=6) as zipf:
        zipf.write(file_path, arcname=file_path)


if __name__ == '__main__':
    main()
    