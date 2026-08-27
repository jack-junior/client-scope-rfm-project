import numpy as np


def get_stock_code(code : object) -> int:
    if type(code)== str:
        for char in code:
            if not str.isnumeric(char):
                code = code.replace(char, "")

        if len(code)==0:
            return np.nan

        code= str.strip(code)
        return int(code)
    if type(code)== int:
        return code

print(get_stock_code("79323W"))