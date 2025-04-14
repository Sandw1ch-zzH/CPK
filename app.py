import streamlit as st
import pandas as pd
from io import BytesIO

st.title("材料属性比对工具")

st.markdown("""
1. 上传 **第一个表**（含“标准名称”“材料属性名称”等多列）  
2. 上传 **第二个表**（“标准名称”+ 正确的“材料属性名称”）  
3. 点击运行，下载带“对照材料属性名称” & “是否一致” 的结果。
""")

uploaded1 = st.file_uploader("上传第一个表 (Excel 或 CSV)", type=["xlsx", "xls", "csv"], key="1")
uploaded2 = st.file_uploader("上传第二个表 (Excel 或 CSV)", type=["xlsx", "xls", "csv"], key="2")

if uploaded1 and uploaded2:
    # 读取表格
    if uploaded1.name.endswith(("xls","xlsx")):
        df1 = pd.read_excel(uploaded1, dtype=str)
    else:
        df1 = pd.read_csv(uploaded1, dtype=str, encoding='utf-8-sig')

    if uploaded2.name.endswith(("xls","xlsx")):
        df2 = pd.read_excel(uploaded2, dtype=str)
    else:
        df2 = pd.read_csv(uploaded2, dtype=str, encoding='utf-8-sig')

    # 核心处理逻辑
    mapping = df2.set_index('标准名称')['材料属性名称']
    df1['对照材料属性名称'] = df1['标准名称'].map(mapping).fillna('未知')

    # 调整列顺序：紧跟在“标准名称”后
    cols = list(df1.columns)
    cols.remove('对照材料属性名称')
    pos = cols.index('标准名称') + 1
    cols.insert(pos, '对照材料属性名称')
    df1 = df1[cols]

    # 是否一致
    df1['是否一致'] = (df1['材料属性名称'] == df1['对照材料属性名称'])
    df1['是否一致'] = df1['是否一致'].map({True: '是', False: '否'})

    st.success("处理完成！下面是预览：")
    st.dataframe(df1)

    # 生成可下载的 Excel
    buffer = BytesIO()
    df1.to_excel(buffer, index=False)
    buffer.seek(0)
    st.download_button(
        label="下载结果 Excel",
        data=buffer,
        file_name="table1_with_compare.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )