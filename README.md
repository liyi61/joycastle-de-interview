# JoyCastle - 数据工程与分析能力测试项目

## 任务1: 模拟数据集生成
Was able to execute the provided generate_events.py file to obtain the required CSV file  
对所提供的脚本做了以下修改：
- NUM_PLAYERS 从 100 改成 100，000  
- SIMULATION_TIME 从90天 改成 180天  
- 由于sqlite是本地数据库，为了避免数据量过大造成内存溢出，做如下改动
	- changed Session duration to be between 5 minutes and 24 hours. 
	- changed Wait time b/t events to be between 10 seconds to 10 minutes  
	- changed delay between sessions to be between 6 hours and 180 days

## 任务2: 数据管道和ETL过程
**数据源**：previously generated csv file (*game_events.csv*)  
- summary about the data:
  - 1，265，110 rows
  - 7 columns
    - EventID: Object, Not null
    - PlayerID: Object, Not null
    - EventTimestamp: Object, Not null
    - EventType: Object, Not null
    - EventDetails: Object, Not null
    - DeviceType: Object, Not null
    - Location: Object, Not null

**数据destination**：sqlite db  
  - 数据库名字: *joycastle*  
  - table名字: *game_events*

### Data Extraction
通过pandas的read_csv读取csv的数据到dataframe。

### Data Cleaning
由于是模拟脚本生成，数据很干净，没有缺失数据，没有duplicates。

### Data Transformation
1. 通过使用df_events.info()语句可以发现EventTimestamp的数据类型是object，
我使用了pandas的to_datetime把它更改成了datetime数据类型。
2. 使用了set_index把EventID设置成了index  

### Data Load
1. import sqlite3，建立连接后，新建一个数据库命名为*joycastle*
2. 使用to_sql把数据先存入一个temp table
- 先存入temp table是因为sqlite3不支持对已存在的表进行加primary key或者更改column数据类型的操作
- 我使用的解决办法是先把数据写进temp table，另外再建立一个表（命名为game_events)基于正确的table schema (EventID作为primary key，EventTimestamp数据类型为datetime），然后把数据从temp table拷贝进game_events


## 任务3: 分析仪表板开发  
仪表板工具：Power BI  
数据源：使用sqlite作为数据源，使用ODBC connection，选择SQLite3 Datasource，具体设置如下图：  
![ODBCConnector](https://github.com/liyi61/joycastle-de-interview/assets/39036575/8d1dc666-3bfb-4eb7-b808-6f2c368a39fd)  

交互式仪表板截图如下（.pbix文件已经push到GitHub）：
![任务3-BI仪表盘截图](https://github.com/liyi61/joycastle-de-interview/assets/39036575/5b108d4f-c05b-4c33-8e30-b393d4f4f323)  

包含的可视化有：  
- 每日活跃用户数（DAU)  
- DAU走势
- 平均会话时长（分钟）
- in-app purchase总收入  
- 每次会话平均消费金额  
- in-app purchase over time (month)  
- 180天内消费排名前10玩家  
- 玩家来自的国家分部情况
- deivces使用情况
- 玩家的活跃情况分布  
- 每次会话的社交互动次数  


## 任务4: 玩家流失的预测模型  
### 详细步骤注释请见jupyter notebook

1. Getting data from the game_events.csv file  

2. Feature Engineering:  
- 总会话次数  
- 每月会话次数  
- 设备类型  

Target: column 'lost' (0 = 不停止玩游戏；1 = 停止玩游戏)  
Detailed explanation is included in the jupyter notebook

3. 模型选用：分类问题，选用随机森林作为我们的模型 (n_estimator = 100) 

4. 模型评估：

- Precision(positive predictive value): tp / (tp + fp); Total number of true predictive churn divided by the total number of predictive churn; High Precision means low fp, not many return users were predicted as churn users.  
- Recall(sensitivity, true positive rate): tp / (tp + fn) Predict most postive or churn user correctly. High recall means low fn, not many churn users were predicted as return users.  

<img width="475" alt="evaluation" src="https://github.com/liyi61/joycastle-de-interview/assets/39036575/494b4c0a-ac05-48ef-ac44-88dcfbbbd96d">

<img width="381" alt="confusionmatrix" src="https://github.com/liyi61/joycastle-de-interview/assets/39036575/ebfada4a-8f0d-4fd2-90da-ee7e42f76ab0">

（由于是模拟生成数据，特征不足，类别不平衡都会导致模型效果不好，以及考虑到时间问题没有做模型优化，这个Jupyter notebook主要是作为流程展示）
