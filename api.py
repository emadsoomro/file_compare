from fastapi import FastAPI, UploadFile, File, HTTPException
from file_compare import Compare_files

app = FastAPI()

@app.post("/compare-files/")
async def compare_files(Title,
    gd_file: UploadFile = File(...),
    invoice_file: UploadFile = File(...)):

    try:
        if gd_file.filename.endswith(".pdf"):
            gd_file = await gd_file.read()
            if invoice_file.filename.endswith((".xls", ".xlsx")):
                result = Compare_files(GD_file_path=gd_file, Invoice_path=invoice_file.file, Title=Title)
                return result
            else:
                raise HTTPException(status_code=400, detail="Invoice Error: Please upload an excel file.")

        else:
            raise HTTPException(status_code=400, detail="GD error: Please upload a PDF file.")

    except Exception as e:
        return {f"Error: {e}"}

