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



## 任务4: 玩家流失的预测模型