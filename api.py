from fastapi import FastAPI, UploadFile, File, HTTPException
from file_compare import Compare_files
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/compare-files/")
async def compare_files(Title,
    gd_file: UploadFile = File(...),
    invoice_file: UploadFile = File(...)):

    result = {"matched": {}, "not_matched": {"gd_data":{}, "invoice_data":{}}}
    try:
        # return {"file_data_gd": gd_file, "file_data_invoice" : invoice_file }
        if gd_file.filename.endswith(".pdf"):
            gd_file = await gd_file.read()
            if invoice_file.filename.endswith((".xls", ".xlsx")):
                # try:
                result = Compare_files(GD_file_path=gd_file, Invoice_path=invoice_file.file, Title=Title)
                return result
                # except:
                #     return {"result":result, "error": "Invalid files"}
            else:
                raise HTTPException(status_code=400, detail="Invoice Error: Please upload an excel file.")

        else:
            raise HTTPException(status_code=400, detail="GD error: Please upload a PDF file.")

    except Exception as e:
        return {f"Error: {e}"}

