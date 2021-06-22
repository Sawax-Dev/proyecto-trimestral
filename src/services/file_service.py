import os
import pandas as pd

class FileService:

    __filePath: str = "C:\\Users\\Swyme\\Desktop\\proyecto-semestral\\src\\services\\file\\products.xlsx"

    def load(self):
        data: list = []
        try:
            xlsFile = pd.read_excel(
                os.path.join(self.__filePath),
                sheet_name='Inventario',
                engine='openpyxl',
                date_parser=''
            )
            data = xlsFile.values
        except:
            data = None
        return data