import pandas as pd
import numpy as np
import streamlit as st
#全局设置
st.set_page_config(
    page_title='投标报价工具-低价法 V1.0',
    layout='wide')
#侧边栏
st.sidebar.success("在上方选择一个报价工具。")
#内容
st.header('低价法报价工具')
st.info('通过将所有有效投标中的最低报价与各投标者的报价相比较，按比例计算得分。具体公式为：'
        '投标人报价得分 =（最低价 / 投标人报价）× 价格分值。此方法确保了价格竞争性，'
        '奖励了提出最低报价的投标者，同时简化了评分过程，确保了评审的公平性和透明度。')
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
def price_per(new_per,per_mean,per):
    return (per_mean/new_per)*per
# 主界面布局和输入
st1,st2=st.columns(spec=2)
price=float(st2.number_input(label='请输入最高限价：（单位:元）',min_value=0.00,step=100.00))
fraction=float(st1.number_input(label='请输入满分分值',max_value=70,min_value=10,step=10))
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
    '最高限价': [price],
    '满分分值': [fraction],
    '主标报价': [main],
    '竞争对手报价': compete,
}
mean_n=data_info['竞争对手报价']
all_data=data_info['竞争对手报价']+data_info['主标报价']
#最小值基准报价
min=np.min(all_data)
main_price=price_per(main,min,fraction)
compete_price=[price_per(mean_n[i], min, fraction) for i in range(len(mean_n))]
col1,col2=st.columns(2)
col1.info('基准价格：'+str(round(min,2))+'元')
col2.info('最高限价：'+str(price)+'元')
col = st.columns(len(mean_n))
col[0].metric('主标价格:'+str(round(main,2)),round(main_price,2),round(main_price-max(max(compete_price),main_price),2))
# 遍历每一列，显示主标报价和竞争对手报价
for i in range(0,len(mean_n)):
    # 使用 enumerate 来获取索引和对应的竞争对手报价
    col[i].metric(f'竞争报价 '+str(mean_n[i]), round(compete_price[i],2), round(compete_price[i]-max(max(compete_price),main_price),2))