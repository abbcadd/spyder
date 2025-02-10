from DrissionPage import ChromiumOptions, ChromiumPage
import time
import pandas as pd

# 初始化数据字典
data = {
    '时间': [],
    '评论内容': [],
}
url = 'https://www.taobao.com/'
chrome_options = ChromiumOptions()
chrome_options.headless(False)
chrome_options.set_user_agent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')

# 添加更多反爬虫参数
chrome_options.ignore_certificate_errors(True)
chrome_options.no_imgs(False)
chrome_options.incognito(True)  # 隐身模式

page = ChromiumPage()
page.get(url)

# 输入搜索关键词
search_input = page.ele('#q')
search_input.input('助眠产品')

# 点击搜索按钮
page.ele('xpath://button[contains(text(), "搜索")]').click()
page.scroll.down(2500) # 滑动到底部，确保数据加载完成
a = page.eles('xpath://div[@class="tbpc-col search-content-col tbpc-col-lg-12 tbpc-col-xl-12 tbpc-col-xxl-10 tbpc-col tbpc-col-horizon-8 search-content-col tbpc-col-lg-12 tbpc-col-xl-12 tbpc-col-xxl-10"]')
for i in a:
    i.click()
    break