import zipfile
import glob
import os

file_to_zip = glob.glob('S_Sekundar_*.xml')[0]
#file_to_zip = os.path.splitext(os.path.basename(glob.glob('S_Sekundar_*.xml')[0]))[0]
output_zip_file = os.path.splitext(os.path.basename(file_to_zip))[0] + '.zip'

with zipfile.ZipFile(output_zip_file, 'w') as zipf:
    # Write the file you want to zip into the archive.
    zipf.write(file_to_zip, arcname=file_to_zip)
  

