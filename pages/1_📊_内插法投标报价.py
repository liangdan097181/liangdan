import pandas as pd
import numpy as np
import streamlit as st
#全局设置
st.set_page_config(
    page_title='投标报价工具-内插法 V1.0',
    layout='wide')
#侧边栏
st.sidebar.success("在上方选择一个报价工具。")
#内容
st.header('内插法报价工具')
st.info('当有效投标报价大于【报价系数】家数时：'
        '去掉一个最高价和一个最低价，以剩余投标报价的算术平均值为基准价；'
        '当有效投标报价小于等于【投标系数】家数时：'
        '以投标报价的算术平均值为基准价'
        '投标报价为基准价的得满分，每高于基准价1%扣相应的分，每低于基准价1%扣相应的分，按内插法计算，计算到小数点后两位。')
# 定义输入检查函数
def check_input(value, name):
    if value is None or value == '':
        st.error(f'{name}不能为空')
        return False
    else:
        return True
#检查数字输入框
def check_num(value,name):
    if value==0:
        st.error(f'请输入正确的{name}')
        return False
    else:
        return True
#检查报价
def check_price(new_price,price,name):
    if new_price>price:
        st.error(f'最高限价为{price},{name}已超出限价！')
        st.stop()
        return False
    else:
        return True
# 定义价格得分计算函数
def price_per(new_per, per_mean, fraction, hight, lower, per):
    if new_per > per_mean:
        score_change = ((new_per - per_mean) / (per_mean * per) )* hight
        return fraction - score_change
    elif new_per < per_mean:
        score_change = ((per_mean-new_per) / (per_mean * per) )* lower
        return fraction - score_change
    return fraction
# 主界面布局和输入
st1,st2=st.columns(spec=2)
num = st1.number_input(label='请输入报价系数：大于系数去掉最高和最低价',min_value=4,step=10)
price=float(st2.number_input(label='请输入最高限价：（单位:元）',min_value=0.00,step=100.00))
fraction=float(st1.number_input(label='请输入满分分值',max_value=70,min_value=10,step=10))
per=float(st2.number_input(label='请输入基准价的百分比：（小数表示）',min_value=0.01,max_value=0.1))
hight=float(st1.number_input(label='高于基准价百分比扣分分值',min_value=0.5,step=0.5))
lower=float(st2.number_input(label='低于基准价百分比扣分分值',min_value=0.5,step=0.5))
main=float(st1.number_input(label='请输入主标报价：（单位:元）',min_value=0.00,step=100.00,max_value=price))
check_num(main,'主标价格')
check_price(main,price,'主标价格')
compete=st2.text_input('请输入竞争对手报价，逗号分隔：（单位:元）',  max_chars=100, help='最大长度为100字符')
if compete=='':
    st.stop()
else:
    compete=compete.split(',')
    compete = [float(x.strip()) for x in compete]
    for i in compete:
        check_price(i,price,'竞争对手')
# 收集输入数据
data_info = {
    '投标系数': [num],
    '最高限价': [price],
    '满分分值': [fraction],
    '基准价比例': [per],
    '高于基准价扣分': [hight],
    '低于基准价扣分': [lower],
    '主标报价': [main],
    '竞争对手报价': compete,
}
mean_n=data_info['竞争对手报价']
all_data=data_info['竞争对手报价']+data_info['主标报价']
if len(all_data)>num:
    mean_sort=[i for i in mean_n if i!=max(all_data) and i!=min(all_data)]
    mean=np.mean(mean_sort)
else:
    mean=np.mean(all_data)
main_price=price_per(main,mean,fraction,hight,lower,per)
compete_price=[price_per(mean_n[i], mean, fraction, hight, lower, per) for i in range(len(mean_n))]
col1,col2=st.columns(2)
col1.info('基准价格：'+str(round(mean,2))+'元')
col2.info('基准价1%：'+str(round(mean*per,2))+'元')
col = st.columns(len(mean_n))
col[0].metric('主标价格:'+str(round(main,2)),round(main_price,2),round(main_price-max(max(compete_price),main_price),2))
# 遍历每一列，显示主标报价和竞争对手报价
for i in range(0,len(mean_n)):
    # 使用 enumerate 来获取索引和对应的竞争对手报价
    col[i].metric(f'竞争报价 '+str(mean_n[i]), round(compete_price[i],2), round(compete_price[i]-max(max(compete_price),main_price),2))