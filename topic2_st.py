import streamlit as st
import numpy as np
import pandas as pd
import seaborn as sb
import matplotlib.pyplot as plt
import datetime
import pickle
from PIL.Image import new

from cheating_def import *


with open('nhung_data.pkl','rb') as file:
    data = pickle.load(file)
    
with open('cus_gr.pkl','rb') as file:
    cus_data = pickle.load(file)

    
menu = ['RFM','Who are you?','CustomerID']
choice = st.sidebar.selectbox('Index', menu)

# =======================================================================
# *** dict ***
# =======================================================================

freq_dict = {
    '1': 1,
    '2': 1.5,
    '3 - 5': 2,
    'more than 5': 3,
    'more than 20': 4,
    'more than 30': 4
}

recency_dict = {
    range(0,17): 4,
    range(17,50): 3,
    range(50,142): 2,
    range(142,380): 1
}

monetary_dict = {
    range(1,306): 1,
    range(306,669): 2,
    range(669,1_661): 3,
    range(1_661,500_000): 4
}


nhung_dict = {
    'best': 'Nhóm best: Tập trung nhóm khách hàng chiếm % doanh thu cao nhất (trên 64%), có tần suất hoạt động cao và có hoạt động gần đây, là nhóm khách hàng giá trị nhất (444, 344, 434)',
    'good': 'Nhóm good: Có số lượng khách hàng thuộc nhóm 333, 433, 443 cao, là nhóm khách hàng trên mức trung bình về tần suất và chi tiêu, có R trên 3',
    'average': 'Nhóm average: Nhóm khách hàng mới hoặc là nhóm khách hàng chi tiêu ở mức trung bình và dưới trung bình, mua hàng 1 hay 2 lần, có R ở mức 2 và 3, tập trung cả nhóm có giao dịch gần đây, có tần suất cao nhưng M thấp; là nhóm có số khách hàng nhiều nhất (trên 21%)',
    'below average': 'Nhóm below average: Nhóm khách hàng chi tiêu thấp, có nguy cơ bỏ đi cao với R và M dưới 2, có score dưới 5',
    'gone': 'Nhóm gone: Nhóm khách hàng không hoạt động hơn 6 tháng, tập trung chủ yếu 3 nhóm 111, 121, 112, nhóm mua 1 lần và không có ý định giao dịch thêm với mức chi tiêu thấp, M bằng 1 hoặc 2',
    'great but might not come back': 'Nhóm great but might not come back: Nhóm khách hàng có tần suất hoặc/và chi tiêu tốt nhưng không hoạt động gần đây, nhóm có R=2 nhiều'
}

rfm_score_dict = {
    3: 'Tập trung nhóm khách hàng không còn hoạt động, tần suất giao dịch thấp, chi tiêu cũng thấp',
    4: 'Tập trung 3 nhóm 121, 112, 211 cũng là nhóm khách hàng không còn hoạt động, tần suất giao dịch và chi tiêu thấp',
    5: 'Nhóm 212 có số khách hàng cao nhất, là nhóm chi tiêu và tần suất hoạt động dưới trung bình, ít có hoạt động gần đây',
    6: '2 nhóm 312, 222 có số khách hàng cao nhất, 141 có số khách hàng thấp nhất',
    7: '3 nhóm 322, 223 có số khách hàng cao nhất, có sự chênh lệch rõ so với các nhóm còn lại, nhóm 142, 124 thấp nhất, tập trung nhóm khách hàng trung bình',
    8: 'Nhóm 233 cao nhất, chênh lệch nhiều so với 3 nhóm 422, 332, 323, nhóm 314, 413 thấp nhất, tập trung nhóm khách hàng chi tiêu trên trung bình',
    9: 'Nhóm 333 có số khách hàng cao nhất, hơn 2 lần nhóm 234, 4 nhóm 234, 243, 423, 432 chênh lệch nhiều so với các nhóm còn lại, nhóm khách hàng chi tiêu trên trung bình, tần suất hoạt động tốt',
    10: 'Tập trung chủ yếu 4 nhóm 433, 244, 343, 334, nhóm khách hàng hoạt động gần đây, mức chi tiêu tốt',
    11: 'Nhóm 344 cao nhất, hơn 2 lần nhóm 443, hơn 3 lần nhóm 434, nhóm khách hàng hoạt động gần đây, mức chi tiêu và tần suất tốt',
    12: 'Nhóm khách hàng giá trị nhất, có mức chi tiêu, tần suất hoạt động cao nhất trong tất cả các nhóm'
}

kim_dict = kim_dict = {
    'REGULAR':'Nhóm REGULAR: chiếm tỉ lệ 18.79% cao nhất, chỉ mua hàng 3 lần với số tiền chi ít hơn nhóm LOYAL khoảng 3 lần => Cần thêm các hoạt động chăm sóc và quảng bá dịch vụ để tăng lượng đơn hàng cho nhóm này.',        
     'LOYAL':'Nhóm LOYAL: chiếm tỉ lệ 17.84%, nhóm khách hàng này mang lại doanh thu cao thứ nhì của cửa hàng, trung bình sau 1 tháng sẽ mua hàng lại 1 lần, số lượng đơn hàng ít hơn nhóm VIP một nửa. => Cần tiếp tục duy trì chăm sóc tốt, cung cấp nhiều hơn các giải pháp mua hàng, để đưa nhóm này lên VIP.',        
    'LOST':'Nhóm LOST: chiếm tỉ lệ 18.26%, cho thấy cửa hàng có thu hút được khách hàng mới nhưng chưa giữ chân được khách => Ưu tiên các hoạt động quảng bá giới thiệu thêm sản phẩm cho nhóm này để họ quay lại mua hàng.',
    'VIP':'Nhóm VIP: chỉ chiếm tỉ lệ 11.09%, tuy nhiên mang lại doanh thu cao nhất cho cửa hàng, cao hơn gần gấp 3 lần nhóm khách hàng LOYAL, và cũng thường xuyên mua hàng với trung bình 7 ngày một đơn hàng => Cần thêm các hoạt động chăm sóc đặc biệt cho nhóm này để duy trì doanh thu, có thể có thêm giá ưu đãi để duy trì hoặc tăng số lượng đơn hàng.',
    'NEW':'Nhóm NEW: chiếm tỉ lệ khá cao là 34.02%, cũng dễ hiểu vì dữ liệu chỉ có khoảng 1 năm, nhiều khách hàng nhóm này là nhóm tiềm năng, sau 3 tháng rưỡi sẽ quay lại mua hàng. => Cần thêm các hoạt động quảng bá dịch vụ để thu hút nhóm này, để tỉ lệ quay lại mua hàng nhiều hơn.'
}

# =======================================================================
# *** RFM ***
# =======================================================================

if choice == 'RFM':
    
#     st.dataframe(cus_data)
    st.write('## Topic 2: Customer Segmentation')
    
    with st.expander('RFM score'):
        st.image('score_all.png')        
        score_info2(data,'score',rfm_score_dict)
        
    with st.expander('Phân khúc khách hàng của Kim'):
        rmf_info(data,'kim',kim_dict)
        
    with st.expander('Phân khúc khách hàng của Nhung'):
        rmf_info(data,'nhung',nhung_dict)
        

# =======================================================================
# *** Who are you? ***
# =======================================================================

elif choice == 'Who are you?':
    st.write('### Who are you?')
    
    # input
    rec_opt = st.date_input('The latest transaction date:',datetime.date(2011, 12, 10),
                            max_value=datetime.date(2011, 12, 10),
                            min_value=datetime.date(2010, 12, 1))
    
    freq_opt = st.selectbox('Frequency:',tuple(freq_dict.keys()))
    mone_opt = st.number_input('Monetary value:',step=0.1, max_value=500_000.00)
    
    d = (datetime.date(2011, 12, 10) - rec_opt).days
    
    r = score_converting(recency_dict,d)
    f = freq_dict[freq_opt]
    m = score_converting(monetary_dict,int(mone_opt))
    
    st.write(r,f,m,d)
    
    if m is not None:
        rfm_score = r+f+m
        #-----------------------------------------------
        k_level = kim_rfm_level(rfm_score)
        st.write('###',k_level)
        st.write(kim_dict[k_level])
        
        # ----------------------------------------------
        n_level = nhung_rfm_level(r,f,m,d,rfm_score)
        st.write('###',n_level)
        st.write(nhung_dict[n_level])
        st.dataframe(data.describe()[['recency', 'frequency', 'monetary']])
        
    else:
        st.write('no result')
          

# =======================================================================
# *** CustomerID ***
# =======================================================================

elif choice == 'CustomerID':
    
    cus_id = st.text_input("Enter CustomerID for Customer's information (ex: 17450):")
    
    # output
    cus_info = customer(data,cus_id)
    
    if cus_info is not None:
        st.table(cus_info)
        with st.expander('More details'):
            cus_type(cus_info,'kim',kim_dict) # kim
            cus_type(cus_info,'nhung',nhung_dict) # RFM_Level
            
            score(data,cus_info,'score',rfm_score_dict) # score
            
        with st.expander("Customer's transaction history"):
            st.table(cus_data[cus_data['CustomerID']== int(cus_id)])
        
    else:
        st.write('no result')

    
    