import numpy as np
import pandas as pd
import seaborn as sb
import matplotlib.pyplot as plt
import pickle
import streamlit as st
import squarify

# ---------------------------------------------------------

def id_num(x):
    if x.isnumeric():
        return int(x)
    else:
        return None
    
# ---------------------------------------------------------

def customer(data,cus_id):
    cus_id = id_num(cus_id)
    if cus_id is not None:
        df = data[data.CustomerID == cus_id]
        if len(df)>0:
            return df
    else:
        return None

# ---------------------------------------------------------

def cus_type(df,col,your_dict):
    cus_type = df[col].values[0]
    st.write('### ', cus_type)
    st.write(your_dict[cus_type])
    

# ---------------------------------------------------------

def score_info(data,col,score_dict): # score_info(data,'score',rfm_score_dict) # score all
    lst = list(score_dict.keys())
    for cus_type in lst:
        m_std = data[data[col]==cus_type].groupby([col,'RFM_Segment'],as_index=False)\
        .count().agg({'CustomerID':['mean','std']}).round(1)

        st.write('### Score:', str(cus_type))
        st.write('mean: %.2f - std: %.2f' % (m_std.loc['mean'][0],m_std.loc['std'][0]))

        st.write(score_dict[cus_type])

        df_new = pd.DataFrame(data[data[col]==cus_type]['RFM_Segment'].value_counts())
        fig, ax = plt.subplots()
        sb.barplot(y=df_new.RFM_Segment,x=df_new.index,ax=ax)
        ax.set_ylabel('Count')
        ax.set_xlabel('RFM_Segment')
        ax.grid()
        st.pyplot(fig)


def score_info2(data,col,score_dict): # score_info(data,'score',rfm_score_dict) # only text
    lst = list(score_dict.keys())
    for cus_type in lst:
        m_std = data[data[col]==cus_type].groupby([col,'RFM_Segment'],as_index=False)\
        .count().agg({'CustomerID':['mean','std']}).round(1)

        st.write('**>>> Score', str(cus_type),
                 '(mean: %.2f - std: %.2f):**' % (m_std.loc['mean'][0],m_std.loc['std'][0]),
                 score_dict[cus_type])
#         st.write('- mean: %.2f - std: %.2f' % (m_std.loc['mean'][0],m_std.loc['std'][0]))
#         st.write('-',score_dict[cus_type])
        
        
def score(data,df,col,score_dict): # score(data,cus_info,'score',rfm_score_dict)
    
    cus_type = df[col].values[0]
    st.write('### Score:', str(cus_type))
    
    st.write(score_dict[cus_type])
    
    df_new = pd.DataFrame(data[data[col]==cus_type]['RFM_Segment'].value_counts())
    fig, ax = plt.subplots()
    sb.barplot(y=df_new.RFM_Segment,x=df_new.index,ax=ax)
    ax.set_ylabel('Count')
    ax.set_xlabel('RFM_Segment')
    ax.grid()
    st.pyplot(fig)

    
def score_converting(score_dict,value):
    n = len(score_dict)
    i = 0
    for i in range(0,n):
        key = list(score_dict.keys())[i]
        if value in key:
            return score_dict[key]
        
# ---------------------------------------------------------
    
def kim_rfm_level(rfm_score):
    
    if rfm_score == 12:
        return 'VIP'
    
    elif (rfm_score >= 10 and rfm_score < 12):
        return 'LOYAL'
    
    elif (rfm_score >= 8 and rfm_score < 10):
        return 'REGULAR'
    
    elif (rfm_score >= 5 and rfm_score < 8):
        return 'NEW'
    
    else:
        return 'LOST'


def nhung_rfm_level(r,f,m,d,rfm_score):

    if (rfm_score >= 11) & (m == 4):
        return 'best'
    
    elif d >= 200: 
        return 'gone'
    
    elif (rfm_score >= 9) & (r >= 3) & (m >= 3):
        return 'good'
    
    elif (r <= 2) & (m >= 3):
        return 'great but might not come back'
    
    elif (rfm_score <=5) | (r == 1):
        return 'below average'
    
    else:
        return 'average'    
    

# ---------------------------------------------------------
    
def rmf_info(data,col,your_dict):
    df_new = data[['recency', 'frequency','monetary','nhung', 'kim']]\
    .groupby(col,as_index=False).agg({
        'recency':'mean',
        'frequency':'mean',
        'monetary':['mean', 'sum', 'count']}).round(2)

    df_new.columns = ['RFM_Level','RecencyMean','FrequencyMean','MonetaryMean',
                       'MonetarySum', 'Count']
    df_new['Percent'] = round((df_new['Count']/df_new.Count.sum())*100, 2)
    df_new['%income'] = round((df_new['MonetarySum']/df_new.MonetarySum.sum())*100, 2)
    df_new.drop('MonetarySum',axis=1,inplace=True)
    st.table(df_new)
    # ----------------------------------
    
    fig, ax = plt.subplots()
    colors_dict = ['red','gold','blue','purple','green','pink','brown','orange']
    squarify.plot(sizes=df_new['Count'],
                  color=colors_dict,
                  label=['{} \n{:.0f} days \n{:.0f} orders \n{:.0f} \n{:.0f} customers \n ({}%)'\
                         .format(*df_new.iloc[i]) for i in range(0, len(df_new))], alpha=0.5 )
                          

    ax.set_title("Customers Segments",fontsize=18,fontweight="bold")
    ax.set_axis_off()
    st.pyplot(fig)
     # ----------------------------------
    
    score_info(data,col,your_dict)
    
    