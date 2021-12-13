import MySQLdb
import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sns

plt.rc('font', family = 'malgun gothic')

config = {

    'host':'127.0.0.1',
    'user':'root',
    'password':'123',
    'database':'elder',
    'port':3306,
    'charset':'utf8',
    'use_unicode':True

}

try:
    conn = MySQLdb.connect(**config)
    print(conn)
    
    cursor = conn.cursor()
  
    sql = " select * from godok "
    cursor.execute(sql)
    
    godok_df = pd.read_sql(sql, conn)
    godok_df.columns = ['번호', '년도', '사망자수']
    
    
    sql = "select * from seoul_center"
    center_df = pd.read_sql(sql,conn)
    center_df.columns = ['번호', '년도', '자치구명', '노인복지관', '경로당', '노인교실']
    
    sql = "select * from seoul_elder"
    elder_df = pd.read_sql(sql,conn)
    elder_df.columns = ['번호', '기간', '자치구명', '기초생활수급', '저소득', '일반']
    
    sql = "select * from seoul_people"
    people_df = pd.read_sql(sql,conn)
    people_df.columns = ['번호', '기간', '자치구명', '전체인구', '65세이상 노인']
 
    sql = "select * from seoul_people"
    people_df = pd.read_sql(sql,conn)
    people_df.columns = ['번호', '기간', '자치구명', '전체인구', '65세이상 노인']
    
    sql = "select * from seoul_center"
    center_df = pd.read_sql(sql,conn)
    center_df.columns = ['번호', '기간', '자치구명', '복지관', '경로당', '노인교실']
    
    elder_df['합'] = elder_df.iloc[:, 3:].sum(axis=1)
    edg = pd.DataFrame(elder_df.groupby(['기간'])['합'].sum()).reset_index()
    print(edg.columns)
    print(edg)
    
    center_df['시설수'] = center_df.iloc[:, 3:].sum(axis=1)
    cdg = pd.DataFrame(center_df.groupby(['기간'])['시설수'].sum()).reset_index()
    print(cdg.columns)
    print(cdg)
    
    merge_df = pd.merge(cdg, edg)
    year = merge_df['기간']
    #print(year)
    df1 = edg['합']
    df2 = cdg['시설수']
    print(df1)
    print(df2)
    
    # 노인수에 비해 시설수가 적다는걸 더 보여줄 수 있는 명확한 그래프.
    fig = plt.figure(figsize=(8,8)) ## Figure 생성 
    fig.set_facecolor('white') ## Figure 배경색 지정
    ax1 = fig.add_subplot() ## axes 생성
     
    colors = sns.color_palette('summer', len(year)) ## 바 차트 색상
     
    xtick_label_position = list(range(len(year))) ## x축 눈금 라벨이 표시될 x좌표
    ax1.set_xticks(xtick_label_position) ## x축 눈금 
    ax1.set_xticklabels(year) ## x축 눈금 라벨
    ax1.bar(xtick_label_position, df1, color=colors) ## 바차트 출력
     
    color = 'blue'
    ax2 = ax1.twinx() ## 새로운 axis 생성
    ax2.plot(xtick_label_position, df2, color=color, linestyle='--', marker='o') ## 선 그래프 
    ax2.tick_params(axis='y', labelcolor=color) ## 눈금 라벨 색상 지정
     
    plt.title('Sales Icecream and Temperature for Days', fontsize=20)
    plt.show()
    
    
    
    
    
    
    
    
    
    
    
    # plt.style.use('default')
    # ax1 = plt.subplot()
    #
    # plt.bar(year, df1)
    # # ax1.tick_params(axis ='both',direction='in')
    # # ax2 = ax1.twinx()
    # plt.plot(year, df1)
    # #ax2.tick_params(axis='y', direction='in')
    # plt.show()
    # # plt.bar(year, df1)
    # plt.twin(plt.plot(year, df2))
    #
    # plt.xlabel('Feature Importance Score')
    # plt.ylabel('Features')
    # plt.title("Visualizing Important Features")
    # plt.show()
    #

    # # 참고용 
    # plt.twinx()
    # y2_value = (1.6, 4.1, 10.2, 17.6, 22.8, 26.9, 28.8, 29.5, 25.6, 19.7, 11.5, 4.2)
    # plt.plot(index, y2_value, 'r.-')
    # plt.ylabel('avg. max. temperature ($^oC$)')
    # plt.ylim( -40, 35)
    # # 데이터 확인용.   
    # print(godok_df)
    # print(center_df)
    # print(elder_df)
    # print(people_df)
    
    # elder_df 합 컬럼을 추가한다.
    # elder_df의 3번쨰부터 출력.(0번부터시작해야함) 후 열을 더한다 sum(axis=1) 
    #elder_df['합'] = elder_df.iloc[:, 3:].sum(axis=1)       
    #print(elder_df)
    
    # elder_df를 groupby하여 if = 기간(2021) 이면 2021의 데이터를 더한다(sum)
    # 해당의 경우 to_frame()은 데이터프레임으로 즉시 변환시켜줘 그래프에 문제 없게 만듬.
    # 왜 그래프가 안그려져 ㅠ
    # edg = pd.DataFrame(elder_df.groupby(['기간','자치구명'])['합'].sum()).reset_index()
    # print(edg.columns)

# 테스트용 확인하고 걍 지워야함
# sns.boxplot(x="day", y="total_bill", data=tips)
# plt.title("요일 별 전체 팁의 Box Plot")
# plt.show()        
    
    #sns.boxplot(x=edg['기간'],y=edg['자치구명'],data=edg['합'])
    #sns.relplot(x=edg['기간'],y=edg['자치구명'],data=edg['합'])
    
    
    #edg = edg.iloc[225:,] # 구가 25개 단위로 되어 있음
    #print(edg)

    # edg.pivot(index= '자치구명',columns='기간',values ='합').plot(kind='area')    
    # plt.show()

    

    # plt.bar(edg,edg['합'])
    # plt.bar(godok_df['년도'],godok_df['사망자수'])    
    #  참고용 people_df.columns = ['번호', '기간', '자치구명', '전체인구', '65세이상 노인']
    #concat 안해도 될듯?
    # pdg = pd.DataFrame(people_df.groupby('기간')['전체인구','65세이상 노인'].sum()).reset_index()
    # print(pdg)

    #
    # sns.set_theme(style="dark")

    #Load the example mpg dataset 데이터 가져오는용도
    #mpg = sns.load_dataset("mpg")

    # Plot miles per gallon against horsepower with other semantics
    # sns.relplot(x=pdg['전체인구'], y=pdg['기간'], size=pdg['65세이상 노인'],
    # sizes=(40, 400), alpha=.5, palette="muted",
    # height=6, data=pdg)
    #
    # plt.show()
    #

    
    # people_df_group = people_df.groupby('기간')['전체인구'].sum().to_frame()
    # people_df_group2 = people_df.groupby('기간')['65세이상 노인'].sum().to_frame()
    # #
    # print(people_df_group.info)
    # print(people_df_group)
    # print(people_df_group2)
    #
    # plt.bar(people_df_group['기간'],people_df_group['65세이상 노인'])
    
    #data = pd.concat([people_df_group,people_df_group2],axis = 1)
    #print(data.info())
    
    #print('------------')
    #print(x,y,z)
    
    
    # 막대그래프를 그린다 (년도를 기준(가로) 사망자수를 나타낸다 (세로))
    # plt.bar(godok_df['년도'],godok_df['사망자수'])

    
    # 해당 그래프 제목 정해주기.
    #plt.title('연도별 서울시 고독자 사망자 수')
    
    
    # plt.plot()
    # plt.show()
    
    # 해당 그래프 이미지 파일로 저장시키기.
    #fig = plt.gcf()
    #fig.savefig('HJproject/HJ_app/static/testimage/test.png')
    

    
    
    
    
    
# SQL문의 데이터 출력 방식 ( 어차피 데이터프레임 화 시킬꺼라 필요 없을수있음.
    # for a in cursor.fetchall():
    #     print(a)
        
        
        
except Exception as e:
    print('오류는 : ' , e) 
    conn.rollback()
finally:
    cursor.close()
    conn.close()    
    