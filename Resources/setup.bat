call powershell -command "Expand-Archive .\Resources\Tesseract-OCR.zip .\Resources"

call powershell -command "Expand-Archive .\Resources\bin.zip .\Resources"

call powershell -command "Expand-Archive .\Resources\data.zip .\Resources\bin"
call powershell -command "Expand-Archive .\Resources\tesseract.zip .\Resources\bin"


call mkdir .\Resources\temp

call exit