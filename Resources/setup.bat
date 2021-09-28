call .\Resources\python-3.7.8-amd64.exe

call powershell -command "Expand-Archive .\Resources\Tesseract-OCR.zip .\Resources"


call mkdir donuts_env
call mkdir .\Resources\temp
call py -3.7 -m venv donuts_env
call .\donuts_env\Scripts\activate
call py -3.7 -m pip install --no-deps .\Resources\moduls\colorama-0.4.4-py2.py3-none-any.whl
call py -3.7 -m pip install --no-deps .\Resources\moduls\numpy-1.21.2-cp37-cp37m-win_amd64.whl
call py -3.7 -m pip install --no-deps .\Resources\moduls\pandas-1.3.2-cp37-cp37m-win_amd64.whl
call py -3.7 -m pip install --no-deps .\Resources\moduls\Pillow-8.3.1-cp37-cp37m-win_amd64.whl
call py -3.7 -m pip install --no-deps .\Resources\moduls\pydicom-2.2.0-py3-none-any.whl
call py -3.7 -m pip install --no-deps .\Resources\moduls\python_dateutil-2.8.2-py2.py3-none-any.whl
call py -3.7 -m pip install --no-deps .\Resources\moduls\pytz-2021.1-py2.py3-none-any.whl
call py -3.7 -m pip install --no-deps .\Resources\moduls\six-1.16.0-py2.py3-none-any.whl
call py -3.7 -m pip install --no-deps .\Resources\moduls\tqdm-4.62.1-py2.py3-none-any.whl
call py -3.7 -m pip install --no-deps .\Resources\moduls\matplotlib-3.4.2-cp37-cp37m-win_amd64.whl
call py -3.7 -m pip install --no-deps .\Resources\moduls\scipy-1.7.1-cp37-cp37m-win_amd64.whl
call py -3.7 -m pip install --no-deps .\Resources\moduls\seaborn-0.11.2-py3-none-any.whl

call py -3.7 -m pip install --no-deps --find-links=.\Resources\moduls python-Levenshtein
call py -3.7 -m pip install --no-deps --find-links=.\Resources\moduls pyocr
call exit