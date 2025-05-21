def merge_tables(left_tables, right_tables, left_on=None, right_on=None, right_str=None):
    if left_on is None or right_on is None:
        return ValueError('Потрібно вказати left_on, right_on!')
    
    if right_str is not None:
        right_tables = right_tables.rename(lambda x: x + right_str, axis=1)
        right_on += right_str

    return left_tables.merge(
        right_tables,
        left_on=left_on,
        right_on=right_on,
        how='inner',
        suffixes=('', '_right')
    )
    
