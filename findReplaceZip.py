import zipfile
import glob
import os

file_path = glob.glob('S_Sekundar_*.xml')[0]
file_path_poz = glob.glob('Pozicija_Sekundar_*.xml')[0]

output_zip_file = os.path.splitext(os.path.basename(file_path))[0] + '.zip'
output_zip_file_poz = os.path.splitext(os.path.basename(file_path_poz))[0] + '.zip'

replacements = {
    'Z00</ID_dijagnoza>\n    <NazivD>Opšti pregled i ispitivanje osoba bez tegoba ili postavljene dijagnoze</NazivD>\n    <NazivLatinski>Opšti pregled i ispitivanje osoba bez tegoba ili postavljene dijagnoze</NazivLatinski>\n    <Vazi_od>2008-12-24T16:51:13.543+01:00</Vazi_od>': 'Z00</ID_dijagnoza>\n    <NazivD>Opšti pregled i ispitivanje osoba bez tegoba ili postavljene dijagnoze</NazivD>\n    <NazivLatinski>Opšti pregled i ispitivanje osoba bez tegoba ili postavljene dijagnoze</NazivLatinski>\n    <Vazi_od>2008-12-24T16:51:13.543+01:00</Vazi_od>\n    <Vazi_do>2015-06-28T00:00:00+01:00</Vazi_do>',
    'Z000</ID_dijagnoza>\n    <NazivD>Opšti medicinski pregled</NazivD>\n    <NazivLatinski>Opšti medicinski pregled</NazivLatinski>\n    <Vazi_od>2008-12-24T16:51:13.543+01:00</Vazi_od>': 'Z000</ID_dijagnoza>\n    <NazivD>Opšti medicinski pregled</NazivD>\n    <NazivLatinski>Opšti medicinski pregled</NazivLatinski>\n    <Vazi_od>2008-12-24T16:51:13.543+01:00</Vazi_od>\n    <Vazi_do>2015-06-28T00:00:00+01:00</Vazi_do>',
    'Z001</ID_dijagnoza>\n    <NazivD>Rutinski zdravstveni pregled dece</NazivD>\n    <NazivLatinski>Rutinski zdravstveni pregled dece</NazivLatinski>\n    <Vazi_od>2008-12-24T16:51:13.543+01:00</Vazi_od>': 'Z001</ID_dijagnoza>\n    <NazivD>Rutinski zdravstveni pregled dece</NazivD>\n    <NazivLatinski>Rutinski zdravstveni pregled dece</NazivLatinski>\n    <Vazi_od>2008-12-24T16:51:13.543+01:00</Vazi_od>\n    <Vazi_do>2015-06-28T00:00:00+01:00</Vazi_do>',
    'Z008</ID_dijagnoza>\n    <NazivD>Drugi opšti pregledi</NazivD>\n    <NazivLatinski>Drugi opšti pregledi</NazivLatinski>\n    <Vazi_od>2008-12-24T16:51:13.543+01:00</Vazi_od>': 'Z008</ID_dijagnoza>\n    <NazivD>Drugi opšti pregledi</NazivD>\n    <NazivLatinski>Drugi opšti pregledi</NazivLatinski>\n    <Vazi_od>2008-12-24T16:51:13.543+01:00</Vazi_od>\n    <Vazi_do>2015-06-28T00:00:00+01:00</Vazi_do>',
    'Z01</ID_dijagnoza>\n    <NazivD>Drugi posebni pregledi i ispitivanja osoba bez tegoba ili ranije dijagnoze</NazivD>\n    <NazivLatinski>Drugi posebni pregledi i ispitivanja osoba bez tegoba ili ranije dijagnoze</NazivLatinski>\n    <Vazi_od>2008-12-24T16:51:13.543+01:00</Vazi_od>': 'Z01</ID_dijagnoza>\n    <NazivD>Drugi posebni pregledi i ispitivanja osoba bez tegoba ili ranije dijagnoze</NazivD>\n    <NazivLatinski>Drugi posebni pregledi i ispitivanja osoba bez tegoba ili ranije dijagnoze</NazivLatinski>\n    <Vazi_od>2008-12-24T16:51:13.543+01:00</Vazi_od>\n    <Vazi_do>2015-06-28T00:00:00+01:00</Vazi_do>',
    'Z039</ID_dijagnoza>\n    <NazivD>Posmatranje zbog sumnje na bolesti ili stanja, neoznačeno</NazivD>\n    <NazivLatinski>Posmatranje zbog sumnje na bolesti ili stanja, neoznačeno</NazivLatinski>\n    <Vazi_od>2008-12-24T16:51:13.543+01:00</Vazi_od>': 'Z039</ID_dijagnoza>\n    <NazivD>Posmatranje zbog sumnje na bolesti ili stanja, neoznačeno</NazivD>\n    <NazivLatinski>Posmatranje zbog sumnje na bolesti ili stanja, neoznačeno</NazivLatinski>\n    <Vazi_od>2008-12-24T16:51:13.543+01:00</Vazi_od>\n    <Vazi_do>2015-06-28T00:00:00+01:00</Vazi_do>',
    'Z038</ID_dijagnoza>\n    <NazivD>Posmatranje zbog sumnje na druge bolesti ili stanja</NazivD>\n    <NazivLatinski>Posmatranje zbog sumnje na druge bolesti ili stanja</NazivLatinski>\n    <Vazi_od>2008-12-24T16:51:13.543+01:00</Vazi_od>': 'Z038</ID_dijagnoza>\n    <NazivD>Posmatranje zbog sumnje na druge bolesti ili stanja</NazivD>\n    <NazivLatinski>Posmatranje zbog sumnje na druge bolesti ili stanja</NazivLatinski>\n    <Vazi_od>2008-12-24T16:51:13.543+01:00</Vazi_od>\n    <Vazi_do>2015-06-28T00:00:00+01:00</Vazi_do>',
    'Z03</ID_dijagnoza>\n    <NazivD>Medicinsko posmatranje i praćenje zbog sumnje na neke bolesti ili stanja</NazivD>\n    <NazivLatinski>Medicinsko posmatranje i praćenje zbog sumnje na neke bolesti ili stanja</NazivLatinski>\n    <Vazi_od>2008-12-24T16:51:13.543+01:00</Vazi_od>': 'Z03</ID_dijagnoza>\n    <NazivD>Medicinsko posmatranje i praćenje zbog sumnje na neke bolesti ili stanja</NazivD>\n    <NazivLatinski>Medicinsko posmatranje i praćenje zbog sumnje na neke bolesti ili stanja</NazivLatinski>\n    <Vazi_od>2008-12-24T16:51:13.543+01:00</Vazi_od>\n    <Vazi_do>2015-06-28T00:00:00+01:00</Vazi_do>',
    'Z016</ID_dijagnoza>\n    <NazivD>Radiološki pregled, neklasifikovan na drugom mestu</NazivD>\n    <NazivLatinski>Radiološki pregled, neklasifikovan na drugom mestu</NazivLatinski>\n    <Vazi_od>2008-12-24T16:51:13.543+01:00</Vazi_od>': 'Z016</ID_dijagnoza>\n    <NazivD>Radiološki pregled, neklasifikovan na drugom mestu</NazivD>\n    <NazivLatinski>Radiološki pregled, neklasifikovan na drugom mestu</NazivLatinski>\n    <Vazi_od>2008-12-24T16:51:13.543+01:00</Vazi_od>\n    <Vazi_do>2015-06-28T00:00:00+01:00</Vazi_do>',
    'Z017</ID_dijagnoza>\n    <NazivD>Laboratorijski pregledi</NazivD>\n    <NazivLatinski>Laboratorijski pregledi</NazivLatinski>\n    <Vazi_od>2008-12-24T16:51:13.543+01:00</Vazi_od>': 'Z017</ID_dijagnoza>\n    <NazivD>Laboratorijski pregledi</NazivD>\n    <NazivLatinski>Laboratorijski pregledi</NazivLatinski>\n    <Vazi_od>2008-12-24T16:51:13.543+01:00</Vazi_od>\n    <Vazi_do>2015-06-28T00:00:00+01:00</Vazi_do>',
    'Z018</ID_dijagnoza>\n    <NazivD>Drugi označeni posebni pregledi</NazivD>\n    <NazivLatinski>Drugi označeni posebni pregledi</NazivLatinski>\n    <Vazi_od>2008-12-24T16:51:13.543+01:00</Vazi_od>': 'Z018</ID_dijagnoza>\n    <NazivD>Drugi označeni posebni pregledi</NazivD>\n    <NazivLatinski>Drugi označeni posebni pregledi</NazivLatinski>\n    <Vazi_od>2008-12-24T16:51:13.543+01:00</Vazi_od>\n    <Vazi_do>2015-06-28T00:00:00+01:00</Vazi_do>',
    'Z019</ID_dijagnoza>\n    <NazivD>Posebni pregled, neoznačen</NazivD>\n    <NazivLatinski>Posebni pregled, neoznačen</NazivLatinski>\n    <Vazi_od>2008-12-24T16:51:13.543+01:00</Vazi_od>': 'Z019</ID_dijagnoza>\n    <NazivD>Posebni pregled, neoznačen</NazivD>\n    <NazivLatinski>Posebni pregled, neoznačen</NazivLatinski>\n    <Vazi_od>2008-12-24T16:51:13.543+01:00</Vazi_od>\n    <Vazi_do>2015-06-28T00:00:00+01:00</Vazi_do>'    
}

def find_replace(file_path, replacements):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    for old, new in replacements.items():
        content = content.replace(old, new)

    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)


find_replace(file_path, replacements)

with zipfile.ZipFile(output_zip_file, 'w') as zipf:
    zipf.write(file_path, arcname=file_path)
    
with zipfile.ZipFile(output_zip_file_poz, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=6) as zipf:
    zipf.write(file_path_poz, arcname=file_path_poz)




