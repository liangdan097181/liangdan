# 投标报价工具源码

这是一个专为投标过程中的报价评分设计的工具，实现了两种计算投标得分的方法：内插法和低价法。源码提供了这两种方法的实现，帮助用户更加公正和科学地评估投标报价。

## 特性

<b>内插法：</b>适用于报价数量较多的情况。当有效投标报价数量超过设定的报价系数时，本方法将删除一个最高价和一个最低价，然后计算剩余投标报价的算术平均值作为基准价。如果有效投标报价数量小于或等于报价系数，将直接使用所有投标报价的算术平均值作为基准价。

<b>低价法：</b>此方法通过比较所有有效投标中的最低报价与各投标者的报价，来按比例计算得分。得分计算公式为：投标人报价得分 = (最低价 / 投标人报价) × 价格分值。

## 使用场景

该工具适用于需要进行投标评估的企业或组织，尤其是在建筑、工程采购、政府采购等行业中，可以有效地帮助决策者选择性价比最高的投标方案。

## 克隆仓库

```
git clone [仓库链接]
```

## 安装依赖

```
pip install Streamlit
```

## 运行程序

```
python main.py
```
