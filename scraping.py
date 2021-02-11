# 国会会議録検索システムから「第201回 常会」の会議録テキスト（半年分）
# を自動でダウンロードする

from selenium import webdriver
import chromedriver_binary
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep

# WebDriverのインスタンス作成
driver = webdriver.Chrome(executable_path='{your_chromedriver_path}')

# URLを指定してブラウザを開く
target_url = 'https://kokkai.ndl.go.jp/#/?back'
driver.get(target_url)
sleep(3)


try:
    # 「第　回」のリストを開くボタンを特定しクリックする
    times_button = driver.find_element_by_xpath('/html/body/div[1]/div/main/section/form/div/div[2]/div[1]/div/span[2]/button')
    times_button.click()
    sleep(3)

    # リスト内から「第201回 常会 令和2(2020)年1月20日～令和2(2020)年6月17日」を特定しクリックする
    # Xpathで指定しているのでHTMLに変更があるとずれる可能性がある
    button_201 = driver.find_element_by_xpath('/html/body/div[1]/div/main/section/form/div/div[2]/div[1]/div/span[2]/div/div/div/div[2]/div[2]/ul/li[3]')
    button_201.click()
    sleep(3)

    # 「院の指定」のリストを開くボタンを特定しクリックする
    in_button = driver.find_element_by_xpath('/html/body/div[1]/div/main/section/form/div/div[2]/fieldset/div[1]/div/select')
    in_button.click()
    sleep(3)

    # リスト内から「衆議院」を特定しクリックする
    syugiin_button = driver.find_element_by_xpath('/html/body/div[1]/div/main/section/form/div/div[2]/fieldset/div[1]/div/select/option[2]')
    syugiin_button.click()
    sleep(3)

    # 「表示する」ボタンを特定しクリックする
    hyoji_button = driver.find_element_by_xpath('/html/body/div[1]/div/main/section/form/div/div[2]/div[2]/button')
    hyoji_button.click()
    sleep(3)

except Exception:
    print('error')
    exit()


while True:
    # 現在のページ内で、class名が「itemTitle」であるノードをリストで取得
    Buttons = driver.find_elements_by_class_name("itemTitle")

    for i in range(len(Buttons)):  # 現在のページ内で、class名が「itemTitle」であるノードの個数分だけループ
        
        # class名が「itemTitle」であるノードの中からi番目の要素を指定
        buttons = driver.find_elements_by_class_name("itemTitle")
        button = buttons[i]

        try:  # 特定したi番目のボタンをクリックする
            button.click()
        except Exception:  # 上手く行かなかった（i番目ボタンが画面内に映っていない）場合
            # 画面を下までスクロールしてから画面内に映ったボタンをクリックする
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            sleep(2)
            button.click()
        sleep(5)

        # 「検索結果一覧」→「会議録テキスト表示」への画面遷移

        # 「全選択/解除」ボタンを特定し、その要素まで画面をスクロールさせてからクリックする
        all_button = driver.find_element_by_xpath('/html/body/div[1]/div/div[5]/div[1]/div[5]/div/div/div[2]/div[1]/label/span[1]')
        ActionChains(driver).move_to_element(all_button).click().perform()
        sleep(2)

        # 「選択した発言をダウンロード」ボタンを特定してクリックする
        download_button = driver.find_element_by_xpath('/html/body/div[1]/div/div[5]/div[1]/div[5]/div/div/div[2]/div[1]/button')
        download_button.click()
        sleep(5)

        # Chromeで設定されたダウンロード先フォルダに会議録テキストファイルが保存される

        # ブラウザバックする
        driver.back()
        sleep(3)
    
    # 「次のページ」ボタンを特定してクリックする
    next_button = driver.find_element_by_xpath('//*[@title="次のページ"]')
    next_button.click()
    sleep(5)

    # この作業を「次のページ」が無くなるまで続ける

