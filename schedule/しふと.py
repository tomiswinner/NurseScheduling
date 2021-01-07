# !pip install ortoolpy
# !pip install pulp

from calendar import Calendar
import datetime
import pandas as pd # pandasにグラフとか扱えるものがあるっぽい
import ortoolpy as op
import numpy as np
import io
import pulp as pp
import openpyxl as opxl
import jpholiday #土日はカウントされない。祝日のみ>


フォーマット = opxl.load_workbook(r'C:\Users\mouse\Desktop\Python\計休.xlsx')
シート1 = フォーマット['format']



def makeDateSetOfMonth():
    today = datetime.datetime.now()
    cl = Calendar(firstweekday=0)
    list1 = list(cl.itermonthdates(today.year,today.month))
    list2 = []
    for elem in reversed(list1):
        if not elem.month == today.month:
            list1.remove(elem) 

    days = ["(月)","(火)","(水)","(木)","(金)","(土)","(日)"]
    for elem in list1:
        list2.append(str(elem.month) + "月" + str(elem.day) + "日" + days[elem.weekday()])

    # print(list2)
    return list2

def makeDaysSetOfMonth():
    today = datetime.datetime.now()
    cl = Calendar(firstweekday=0)
    list1 = list(cl.itermonthdates(today.year,today.month))
    for elem in reversed(list1):
        if not elem.month == today.month:
            list1.remove(elem) 
    
    list2 = []

    for _,elem in enumerate(list1):
        
        if jpholiday.is_holiday(elem) or elem.weekday() >= 5:
            list2.append(1)
        else:
            list2.append(0)
        #休みの日なら1、そうでなければ0が入る
        
    # print(list2)
    return list2



def getHolidayReq():
    global シート1
    希望休リスト =[]
    for i in range(2,7):
        
        tempList = []
        
        for i2,elem in enumerate(シート1[i]):
            if elem.value:
                tempList.append(elem.value)
        
        希望休リスト.append(tempList)
    
    # print(希望休リスト
    return 希望休リスト

def getNumOfMemberWorkingWeekDay():
    global シート1
    print(シート1[15][1].value)
    return シート1[15][1].value

def getNumOfMemberWorkingWeekEnd():
    global シート1
    return シート1[16][1].value



def getWorkdayReq():
    global シート1
    マスト勤務リスト =[]
    
    for i in range(9,14):
        tempList= []
        for _, elem in enumerate(シート1[i]):
            if elem.value:
                tempList.append(elem.value)
        
        マスト勤務リスト.append(tempList)
    
    print(マスト勤務リスト,'yeah')
    return マスト勤務リスト

getWorkdayReq()


# getHolidayReq()

def decideWorkMem():
    global シート1
    workMembersList = []
    for i in range(2,7):    
        workMembersList.append(シート1[i][0].value)
    
    # if isListHasDuplicate(workMembersList):
    #ここ、excel側でエラーを投げたい。どうやろう？
    return workMembersList


def isListHasDuplicate(sequence):
    return len(sequence) == len(set(sequence))


def convertNameIntoNum(array,workArray):
    for _,elem in enumerate(array):
        # print(elem) # 一次元めの配列が返ってくる
        elem[0] = workArray.index(elem[0])  #workmemの順番に対応した位置が返ってくる（重複がなければ）
        # print(array) #これで順番の数字に変わった


def Main():
    
    global workMembers
    workMembers = decideWorkMem()
    global 希望休リスト
    希望休リスト = getHolidayReq()
    convertNameIntoNum(希望休リスト,workMembers)





Main()

dateset = makeDateSetOfMonth()
listLenDateset = list(range(0,len(dateset)))
df = pd.DataFrame(index= listLenDateset,columns= workMembers)
df['日付'] = dateset
df['曜日'] = makeDaysSetOfMonth()
# print(df)



v割当 = np.array(op.addbinvars(df.shape[0],df.shape[1]-2))
# 希望休に関しては、V割当の中の、一部を固定する方向でとりあえずいこうか？qiitaの希望不可扱いでいってしまえばよい

#制約

#   //必要な条件はなんでしょうか？
#   //① 平日は2人基本的に必要 => 定数y行 のxの合計が3となればよい
c平日 = 100
c平日必要人数 = getNumOfMemberWorkingWeekDay()
c平日soft = 50
v平日不足 = op.addvars(len(dateset))
v平日不足soft = op.addvars(len(dateset))

#dateset分配列を作るが、平日以外の部分に0以外の数字が入る可能性がないので問題なし。＝＞本当に？？？？？？？？

#   //② 土日は4人必要  => 定数y行 のxの合計が5
c休日 = 100
c休日必要人数 = getNumOfMemberWorkingWeekEnd()
v休日不足 = op.addvars(len(dateset))
c休日soft = 50
v休日不足soft = op.addvars(len(dateset))
#   //③ 希望休の場所には0固定でいれるようにする  => 指定した[y][x]の値が0固定
c希望休 = 100
#   //④ メンバそれぞれに休みが10日必要  => xの列はそれぞれ、合計20とならなければならない（有給がある場合は19）  必要な休日数はそれぞれ設定できたほうがよいね（月によっても違うので） なので、月の日数 - 必要休日数 = あるxの列の必要値
c計休 = 100
v計休不足 = op.addvars(len(workMembers))  #休暇はメンバごとに日数がちがうな。。。とりあえず10日としとこう

#   //⑤二連休が欲しい人  =>これは希望休みに組み込めるからどうでもよい

#   //⑥最大連勤数nの設定が必要 => これには縦列のx1~x30を、nずつ区切り、そこの和がn-1以下にならなければならない。（つまりどこかで休みがないといけない)
#5連勤がないようにする（つまりn = 4)
c連勤 = 100

# v連勤違反 = op.addvars()

#   //⑦最大連勤数は前の月からも考慮しなきゃいけないので、前の月が終わった段階での連続出勤数を計算に組み込んで置く必要がある。

dfWeekend = df[(df['曜日'] == 1)] #この書きかたは、trueが返る場所だけを取得できる
dfWeekday = df[(df['曜日'] == 0)] 
dfWork = df.iloc[:,:len(workMembers)]


# 目的関数
m = pp.LpProblem(sense = pp.LpMinimize)
m += c平日 * pp.lpSum(v平日不足) +\
c平日soft * pp.lpSum(v平日不足soft) +\
c休日 * pp.lpSum(v休日不足) +\
c休日soft * pp.lpSum(v休日不足soft) +\
c計休 * pp.lpSum(v計休不足)

#制約関数

#dfWeekday の　行ごと（日にちごと）のV割当変数のseriesが2以上になるようにする。dfWeekendなら4以上
#V割当は二次元配列。
for _,elem in dfWeekday.iterrows():
    # print(v平日不足[elem.name])
    m += pp.lpSum(v割当[elem.name]) + v平日不足[elem.name] >= c平日必要人数 -1 # V割当の合計が、2以上でないとき、V平日不足が自動的に補うように設定され、スコアが大きくなってしまう

for _,elem in dfWeekday.iterrows():
    m += pp.lpSum(v割当[elem.name]) + v平日不足soft[elem.name] >= c平日必要人数

for _,elem in dfWeekend.iterrows():
    m += pp.lpSum(v割当[elem.name]) + v休日不足[elem.name] >= c休日必要人数 -1 #同上。休日ver

for _,elem in dfWeekend.iterrows():
    m += pp.lpSum(v割当[elem.name]) + v休日不足soft[elem.name] >= c休日必要人数

#従業員ごとの計休が出されてるか。チェック（列ごと）
def fuckingFunc():
    fuckingN = 0
    global m #python ではグローバル変数を関数内で操るためには、global宣言が必要
    for colName,series in dfWork.iteritems():
        #elemにはseriesが返ってきてる。colNameにはseriesの列名。
        m += pp.lpSum(v割当[:,fuckingN]) == len(dateset) -10
        # m += pp.lpSum(v割当[:,fuckingN]) - v計休不足[fuckingN] 
        fuckingN += 1
fuckingFunc()

#n連勤チェック
#V割当から、1日~30-n日目までの配列。1+1 ~30-(n+1)日目までの配列・・・・n日~30日目までの配列を用意する。
#=>この1日目 v + 2日目 v +  .... + n日目 vが一つ一つの要素(Xとする)となる。連勤チェック配列が出来上がる。
#この要素Xが、n以上にならないようにすれば、n連勤にならないようチェックができる。
for i,elem in enumerate(workMembers):
    print(elem,i)
    for n,elem in enumerate((v割当[:-4,i] + v割当[1:-3,i] + v割当[2:-2,i] + v割当[3:-1,i] + v割当[4:,i]).flat):
        m += elem <= 4 #これで5つの要素すべてに1が入る（5連勤する)と5を超える

#希望休。希望休をいれる部分と対応するv割当に、1を確定でいれる。

#はまだ 12,1,26
#まつもと 19,20,5
#えんどう　26,27,13
#たなか 19,12,20
#ほうせい　13,5,6
# workMembers = ["浜田","松本","田中","遠藤","方正"]


def holidayRequest(array2d):
    global m
    for i,elem in enumerate(array2d):
        for i2,elem2 in enumerate(elem):
            if i2 == 0:
                continue # 0番目名前管理用の番号なのでスキップ

            m += v割当[elem2-1][elem[0]] == 0

holidayRequest(希望休リスト)

status = m.solve()
print(pp.LpStatus[status])

funcH = np.vectorize(pp.value)
result = funcH(v割当).astype(int)


Res = result.astype(str)
for i in range(0,Res.shape[0]):
    for j in range(0,Res.shape[1]):
        if Res[i][j] == '1':
            Res[i][j] = '〇'
        else:
            Res[i][j] = '×'




# numでしっかり個々の値を拾えてるけど、なんでnoneになっちゃうんだろう。。。。。
#=> ndarrayが同じデータ型しか保持できないから。....ではないらしい。DFにつっこんでもだめ。
# astypeでキャストしてからでもだめ。=>キャストは、copyを作るものなので、代入しないといけない。
#とにもかくにもできた！mapとかvectorizeじゃできんかったわ。。。

df.iloc[:,0:len(workMembers)] = Res #結果をdfに代入
print(df)
df.index = df['日付']
df.drop(df.columns[[5,6]],axis= 1,inplace=True) #日付を一番左にもってきて、右のいらない曜日と日付を消す


#日付の部分がセル空白狭いので、そこの整形と、土日祝の色付け
#あとエクセル出力した際、条件つけれるように？、


# print(df)

df.to_excel(r'C:\Users\mouse\Desktop\Python\シフト出力.xlsx',sheet_name='シフト結果')
