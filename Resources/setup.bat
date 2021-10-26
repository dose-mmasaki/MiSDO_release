start powershell -command "Expand-Archive .\Resources\Tesseract-OCR.zip .\Resources"
start powershell -command "Expand-Archive .\Resources\DoNuTS.zip .\Resources"
start powershell -command "Expand-Archive .\Resources\out_csv.zip .\Resources"
start powershell -command "Expand-Archive .\Resources\show_low_data.zip .\Resources"
start powershell -command "Expand-Archive .\Resources\analyze.zip .\Resources"
start powershell -command "Expand-Archive .\Resources\make_projection_data.zip .\Resources"

call powershell -command "Expand-Archive .\Resources\ChuRROs.zip .\Resources"
call powershell -command "Expand-Archive .\Resources\data.zip .\Resources\ChuRROs"
call powershell -command "Expand-Archive .\Resources\tesseract.zip .\Resources\ChuRROs"


call mkdir .\Resources\temp

call exit