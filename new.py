# PythonでSeleniumのwebdriverモジュールをインポート
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
#　操作するbrowserを開く
chrome = webdriver.Chrome(executable_path="./driver/chromedriver")
word = "soccer"
cnt=5
chrome.execute_script("window.open('','_blank');")

at = "2fjlhKhSN5dpACtVdIDrSYn5A"
ass = "TeyQTaqWcU5vaYTgsUgUt0vmjbzs762K3E4022hLXiU474qzbW"
ats = "1176969024980176900-8myi9qYXIw4w54RGgYZADRctUwJJNN"
atts = "QZ8wg1v5pJa5ks5JHxnXMBaxBp7daxqFAzu2PKAkr9R1Y"
# 操作するページを開く
chrome.get("https://tweetlikes.herokuapp.com")

# 検索ワード入力
search_a= chrome.find_element_by_name("a")
search_b = chrome.find_element_by_name("b")
search_c = chrome.find_element_by_name("c")
search_d = chrome.find_element_by_name("d")
search_a.send_keys(at)
search_b.send_keys(ass)
search_c.send_keys(ats)
search_d.send_keys(atts)

# 検索実行
search_d.send_keys(Keys.RETURN)
# print(chrome.title)
search_e= chrome.find_element_by_name("query")
search_f= chrome.find_element_by_name("count")
search_e.send_keys(" ".join(word))
search_f.send_keys(" ".join("5"))
chrome.find_element_by_id('2').click()
# # 先頭のタブに戻る
# chrome.switch_to.window(chrome.window_handles[0])
# 基本設定はここまで。↑は使い回し可能。ここから下は、やりたい動作によって増える
#
# # 3.操作する要素を指定
# driver.find_elements_by_link_text('API確認')
# # 4.その要素を操作する
# # クリックする１
# driver.find_element_by_id('ID').click()
# # テキストを入力する
# driver.find_element_by_id('ID').send_keys('')
