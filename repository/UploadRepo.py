from xlrd import open_workbook
from utils.general_func import generate_date
from utils.sqlpool import Mysql

def insert_excel_data(content):
    workbook = open_workbook(file_contents=content)
    sheet = workbook.sheet_by_index(0)
    data = []
    list_products = []

    for row in range(1, sheet.nrows):
        data.append(sheet.row_values(row))

    for product_data in data:
        obj_product = {
            "fund_code": product_data[1],
            "fund_name": product_data[2],
            "fund_type": product_data[3],
            "fund_type_description": product_data[4],
            "fund_sid": product_data[5],
            "sharia_compliance": product_data[6],
            "im_code": product_data[7],
            "im_name": product_data[8],
            "cb_code": product_data[9],
            "cb_name": product_data[10],
            "status": product_data[11],
            "launching_date": generate_date(product_data[12]),
            "deactivation_date": generate_date(product_data[13]),
        }
        list_products.append(obj_product)
    
    _conn = Mysql()
    try:
        insert_product = _conn.insert_rows(tbl='product', param=list_products)
    except Exception as e:
        _conn.dispose(0)
        resp = {
            "status": "failed",
            "message": str(e)
        }
        return resp
    
    _conn.dispose()
    _conn.closing()

    resp = {
        "status": "success",
        "message": "product data inserted to db",
        "total data from excel": len(list_products),
        "data": list_products
    }
    return resp
