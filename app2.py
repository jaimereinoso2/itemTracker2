import os
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential

# use your `key` and `endpoint` environment variables
endpoint = "https://it2.cognitiveservices.azure.com/"
key = "27672530983c417c888690a09fd8b6b8"
path_to_sample_documents = "imagen3.jpg"

from fastapi import FastAPI, File, UploadFile
import uvicorn
from typing import Annotated

document_analysis_client = DocumentAnalysisClient(
        endpoint=endpoint, credential=AzureKeyCredential(key)
    )


def analyze_receipts(archivo):

    

    # with open(path_to_sample_documents, "rb") as f:
    #     poller = document_analysis_client.begin_analyze_document(
    #     "prebuilt-receipt", document=f, locale="en-US"
    # )
        
    poller = document_analysis_client.begin_analyze_document(
        "prebuilt-receipt", document=archivo, locale="en-US")

    receipts = poller.result()
    for idx, receipt in enumerate(receipts.documents):

        print("--------Analysis of receipt #{}--------".format(idx  + 1))
        print("Receipt type: {}".format(receipt.doc_type or "N/A"))

        merchant_name = receipt.fields.get("MerchantName")
        if merchant_name:
            print(
                "Merchant Name: {} has confidence: {}".format(
                    merchant_name.value, merchant_name.confidence
                )
            )
        
        merchant_address = receipt.fields.get("MerchantAddress")
        if merchant_address:
            print(
                "Merchant Adress: {} has confidence: {}".format(
                    merchant_address.value, merchant_address.confidence
                )
            )

        transaction_date = receipt.fields.get("TransactionDate")
        if transaction_date:
            print(
                "Transaction Date: {} has confidence: {}".format(
                    transaction_date.value, transaction_date.confidence
                )
            )
        if receipt.fields.get("Items"):
            print("Receipt items:")
            for idx, item in enumerate(receipt.fields.get("Items").value):
                print("...Item #{}".format(idx  + 1))

                item_productCode = item.value.get("ProductCode")
                if item_productCode:
                    print(
                        "......Item ProductCode: {} has confidence: {}".format(
                            item_productCode.value, item_productCode.confidence
                        )
                    )

                item_description = item.value.get("Description")
                if item_description:
                    print(
                        "......Item Description: {} has confidence: {}".format(
                            item_description.value, item_description.confidence
                        )
                    )
                item_quantity = item.value.get("Quantity")
                if item_quantity:
                    print(
                        "......Item Quantity: {} has confidence: {}".format(
                            item_quantity.value, item_quantity.confidence
                        )
                    )
                item_price = item.value.get("Price")
                if item_price:
                    print(
                        "......Individual Item Price: {} has confidence: {}".format(
                            item_price.value, item_price.confidence
                        )
                    )
                item_total_price = item.value.get("TotalPrice")
                if item_total_price:
                    print(
                        "......Total Item Price: {} has confidence: {}".format(
                            item_total_price.value, item_total_price.confidence
                        )
                    )
        subtotal = receipt.fields.get("Subtotal")
        if subtotal:
            print(
                "Subtotal: {} has confidence: {}".format(
                    subtotal.value, subtotal.confidence
                )
            )
        tax = receipt.fields.get("TotalTax")
        if tax:
            print("Total tax: {} has confidence: {}".format(tax.value, tax.confidence))
        tip = receipt.fields.get("Tip")
        if tip:
            print("Tip: {} has confidence: {}".format(tip.value, tip.confidence))
        total = receipt.fields.get("Total")
        if total:
            print("Total: {} has confidence: {}".format(total.value, total.confidence))
        print("--------------------------------------")


app = FastAPI()

@app.get("/")
def read_root():
    return {"Hola":"Mundo"}

@app.post("/files/")
async def create_file(miArchivo: Annotated[bytes, File()]):
    analyze_receipts(miArchivo)
    return {"file_size": len(miArchivo)}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)