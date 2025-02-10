from DrissionPage import ChromiumOptions, Chromium
import time
import pandas as pd
import random
from DrissionPage.common import Keys

# 设置浏览器选项
options = ChromiumOptions().headless(False)  # 调试时关闭无头模式

# 创建浏览器对象
driver = Chromium(options)  
tab = driver.latest_tab

def random_sleep(min=2, max=5):
    """随机延迟"""
    time.sleep(random.uniform(min, max))

def debug_screenshot(name='debug'):
    """调试截图（可选）"""
    tab.get_screenshot(path=f'{name}_{int(time.time())}.png', full_page=True)

def search_operation():
    """执行搜索操作"""
    # tab.wait.load_complete()
    search_box = tab.ele('@id=key', timeout=10)
    search_box.input('助眠产品')
    search_btn = tab.ele('@text()=搜索', timeout=5)
    search_btn.click()
    # tab.wait.ele_displayed('xpath://div[@id="J_goodsList"]', timeout=15)
    random_sleep(2, 4)

def human_scroll():
    """模拟人类滚动"""
    prev_count = len(tab.eles('xpath://li[@class="gl-item"]'))
    
    for _ in range(random.randint(3, 5)):
        current_height = tab.run_js('return document.documentElement.scrollHeight')
        random_scroll = random.uniform(0.3 * current_height, 0.8 * current_height)
        random_sleep(1, 2)
        tab.run_js(f'window.scrollTo(0, {random_scroll})')
        random_sleep(1, 2)
        
        current_count = len(tab.eles('xpath://li[@class="gl-item"]'))
        if current_count > prev_count:
            print(f"加载了 {current_count - prev_count} 个新商品")
            prev_count = current_count
        else:
            break
    
    tab.scroll.to_bottom()
    time.sleep(1)
    # tab.wait.ele_loaded('xpath://div[@class="p-price"]', timeout=10)

def get_product_info():
    """获取商品信息"""
    time.sleep(2)
    products = []
    prices = tab.eles('xpath://ul[@class="gl-warp clearfix"]/li//div[@class="p-price"]//i')
    names = tab.eles('xpath://ul[@class="gl-warp clearfix"]/li//div[@class="p-name p-name-type-2"]//em')
    comments = tab.eles('xpath://ul[@class="gl-warp clearfix"]/li//div[@class="p-commit"]//a')
    
    for i in range(len(prices)):
        try:
            product = {
                'price': prices[i].text,
                'name': names[i].text,
                'comment_numbers': comments[i].text if comments[i] else '无评论'
            }
            products.append(product)
            print(product)
        except Exception as e:
            print(f"提取第{i+1}个商品信息出错: {e}")
            continue
    return products

def click_next_page():
    """翻页操作"""
    next_btn = tab.ele('xpath://a[@class="pn-next"]', timeout=5)
    next_btn.click()
    print("已点击下一页")
    time.sleep(2)
    return True

try:
    tab.get('https://www.jd.com/')
    random_sleep(3, 5)
    
    search_operation()
    
    all_products = []
    for page in range(1, 45):  # 获取45页数据
        print(f"正在处理第 {page} 页...")
        human_scroll()
        products = get_product_info()
        all_products.extend(products)
        print(f"第 {page} 页获取到 {len(products)} 条记录")
        
        # 每页保存一次
        df = pd.DataFrame(all_products)
        df.to_excel(f'jd_products_page_{page}.xlsx', index=False)
        print(f"已保存到第 {page} 页，当前共 {len(df)} 条数据")
        
        if page < 45:
            click_next_page()
            random_sleep(3, 5)
    
    # 最终保存所有数据
    df_final = pd.DataFrame(all_products)
    df_final.to_excel('jd_products_all.xlsx', index=False)
    print(f"成功保存所有数据，共 {len(df_final)} 条")

except Exception as e:
    # 异常时保存已获取的数据
    if all_products:
        df_error = pd.DataFrame(all_products)
        df_error.to_excel('jd_products_error.xlsx', index=False)
        print(f"异常终止，已保存 {len(df_error)} 条数据")
    print(f"程序异常终止: {str(e)}")
    debug_screenshot('final_error')
finally:
    driver.quit()