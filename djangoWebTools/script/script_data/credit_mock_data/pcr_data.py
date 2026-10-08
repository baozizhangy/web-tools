import pandas as pd
"""
华融征信mock数据生成
"""

def convert_to_nested_structure(data):
    result = {}
    current_index = 0  # 初始化递增索引

    for _, row in data.iterrows():
        parent1 = row[0]  # 第一列
        parent2 = row[1]  # 第二列
        key = row[2]      # 第三列的键（如 A21, A43 等）

        # 跳过 NaN 值
        if pd.isna(parent1) or pd.isna(parent2) or pd.isna(key):
            continue

        # 初始化父级
        if parent1 not in result:
            result[parent1] = {}

        # 初始化第二级
        if parent2 not in result[parent1]:
            result[parent1][parent2] = {}

        # 设置递增值
        result[parent1][parent2][key] = str(current_index)
        current_index += 1  # 递增索引

    return result


def get_pcr_field(df):
    # 获取字段名、人行字段与输入项字段名一致
    # 使用列号进行操作
    if 1 in df.columns and 2 in df.columns:
        # 将第1列和第2列的值用_连接
        df['BC_combined'] = df[1].astype(str) + '_' + df[2].astype(str)

        # 打印连接后的值，每行一个
        for index, row in df.iterrows():
            print(row['BC_combined'].lower())
    else:
        print("Columns 1 and/or 2 not found in the DataFrame.")


if __name__ == '__main__':
    file_path = r"需求字段.xlsx"
    data = pd.read_excel(file_path, header=None)
    data.ffill(axis=0, inplace=True)  # 向前填充，处理合并单元格
    print(data)
    data0 = data[0]
    # print(data0)
    # 取首列
    data1 = data[[0]]
    # print(data1)
    # nested_structure = convert_to_nested_structure(data)
    # print(nested_structure)
    field_res = get_pcr_field(data)
    # print(field_res)