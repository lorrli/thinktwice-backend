import pandas as pd


def parse_excel():
    df_brands = pd.read_excel(
        r'C:\Users\lli99\Documents\workspace\thinktwice-backend\src\database_connection\IndexData.xlsx',
        'Fashion Report 2019 DB Ver',
        header=27,
        index_col=None,
        na_values=['NA'],
        usecols="A:D",
        engine='openpyxl')
    # print(df_brands.columns.ravel())
    print(df_brands)
    final_brands = []
    for index, row in df_brands.iterrows():
        final_brands.append([
            index, row['brand'], row['transparency'], row['worker_emp'],
            row['env_manage']
        ])
    return final_brands


print(parse_excel())
