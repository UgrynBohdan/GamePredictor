def show_table_info(table, str_table='table', all_info=None):
    print(table.info())
    print(f'Shape = {table.shape}')
    
    null_counts = table.isnull().sum()
    print(f"Null rows in columns:\n{null_counts[null_counts != 0]}")
    print("Nunique:\n", table.nunique())

    if all_info is not None:
        print(f'id col: {table[[col for col in table.columns if 'id' in col]].columns}')
        print(f'Null columns:\n{null_counts[null_counts == len(table)]}')
        print(f'Nunique categorical:\n{table.select_dtypes(exclude=['int', 'float']).nunique()}')

    print()