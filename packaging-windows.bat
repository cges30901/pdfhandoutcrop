pyinstaller -y -w -n pdfhandoutcrop ^
-i icons\pdfhandoutcrop.ico ^
--add-data pdfhandoutcrop\language\*;pdfhandoutcrop\language ^
--add-data pdfhandoutcrop\pdfhandoutcrop.png;pdfhandoutcrop ^
--add-data="LICENSE.txt;." ^
pdfhandoutcrop\__init__.py

pause