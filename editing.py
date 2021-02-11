# LINEグループトーク履歴のフォーマットに合わせて
# scraping.pyでダウンロードしたtxtファイル（statementsフォルダに移動済み）
# を全て編集し、1つのテキストファイルに出力する

import datetime
import glob

# LINEトーク履歴冒頭の形式に合わせてタイトルと保存日時を出力
print('[LINE] 第201回国会（衆議院）のトーク履歴\n保存日時：2020/11/16 00:00',end='')

# 曜日表記（英語:日本語）のディクショナリ
Japan_days = {'Mon':'月','Tue':'火','Wed':'水','Thu':'木','Fri':'金','Sat':'土','Sun':'日'}

pre = (0,0)
# statementsフォルダ内のtxtファイルパスをファイル名順で一括取得
for PATH in sorted(glob.glob('statements/*.txt'),reverse=True):
    # txtファイルを読み込みモードで開く
    f = open(PATH, 'r', encoding='UTF-8',errors='ignore')
    
    # 日付のフォーマットがLINEと一致するように編集して出力する
    # 例）「令和2年1月28日」→「2020/01/28 (火)」に直すだけ
    month,date = 0,0
    for data in f:
        data_ = list(data.split())
        month,date = map(str,data_[1].replace('令和2年','').replace('月',' ').replace('日','').split())
        dt = datetime.datetime(2020, int(month), int(date))
        day = Japan_days[dt.strftime('%a')]
        if (month,date) != pre:
            print('\n')
            print(f'2020/{month.zfill(2)}/{date.zfill(2)} ({day})',end='')  # 日付を出力
        pre = (month,date)
        break
    
    # 9:00からトークが始まったと仮定して現在時刻を設定
    now = datetime.datetime(year=2020,month=int(month),day=int(date),hour=9,minute=0)
    
    # 発言者名の前に付く'o'が既出かどうかのフラッグ
    flag = False

    for data in f:  # 1行ずつチェックしていく
        data_ = list(data.split())
        if not data_:  # 空行の場合
            continue
        if data[0].startswith("○"):  # 誰かの発言の行の場合
            # 時刻と、'o'を除いた発言内容を出力
            print('\n' + str(now)[11:16] + ' ' + data[0][1:] + ' ' + ''.join(data[1:len(data)-1]),end='')
            now += datetime.timedelta(minutes=1)  # 1つの発言ごとに1分だけ時間を進める
            if not flag:
                flag = True
        elif flag:  # 誰かの発言の途中で改行されていた場合
            print(''.join(data[:len(data)-1]),end='')