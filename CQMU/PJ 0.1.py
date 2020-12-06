from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from time import sleep

name=''
password=''
wd = webdriver.Edge(r'F:/Python/edgedriver.exe')#声明浏览器
actionOpenLinkInNewTab = ActionChains(wd)#加入动作
wd.implicitly_wait(2)
wd.get('https://jiaowu.cqmu.edu.cn:8080/eams/manageLogin.action')
wd.find_element_by_css_selector('input[name="username"]').send_keys(name)
wd.find_element_by_css_selector('input[name="password"]').send_keys(password)
sleep(6)
wd.find_element_by_link_text('量化评教').click()
sleep(0.5)
wd.find_element_by_link_text('学生评教(新)').click()
sleep(0.5)
LIST1=[]#存储各科地址
for i in wd.find_elements_by_css_selector("a[onclick='return bg.Go(this,null)']"):
    LIST1.append(i.get_attribute('href'))
for list1 in LIST1:
    print(list1)
    wd.get(list1)
    sleep(1)
    teachers_list=wd.find_elements_by_css_selector('img[alt]')
    for t in teachers_list:
        t.click()
        n = wd.window_handles  # 这个时候会生成一个新窗口或新标签页的句柄，代表这个窗口的模拟driver
        # print('当前句柄: ', n)  # 会打印所有的句柄
        wd.switch_to_window(n[-1])  # driver切换至最新生产的页面
        sleep(1)
        #———————教师评教——————
        evaluate1 = wd.find_elements_by_xpath("//input[@value='2']")
        for i in evaluate1:
            i.click()
        evaluate2 = wd.find_elements_by_xpath("//input[@value='1']")#列表，Xpath大法好！！！！！
        evaluate2[-1].click()#因为不能全优，故把最后一个A换为B，是否考虑随机？？？？？？？？？
        # evaluate = wd.find_elements_by_xpath("/html/body/div//table/tbody/tr/td/input[@value='2']")
        # evaluate=wd.find_elements_by_css_selector('input[value=''2'']')
        # 我也不知道为啥css选不了
        cofirm_button=wd.find_element_by_id("saveButton").click()
        wd.switch_to.alert.accept()#确认保存
        wd.close()#关闭当前标签页
        wd.switch_to_window(n[0])
    #——————课程评价——————

    sleep(1.5)
    for i in wd.find_elements_by_xpath("//input[@value='2']"):
        i.click()
    evaluate = wd.find_elements_by_xpath("//input[@value='1']")
    evaluate[1].click()
    cofirm_button=wd.find_element_by_id("submitButton").click()
    wd.switch_to.alert.accept()#确认保存
# 教师评教='img[alt]'
# 评分=AAA====find_elements_by_css_selector('input[value='2']')
#      BBB====find_elements_by_css_selector('input[value='1']')
# 提交按钮= button[id="saveButton"]
#     确定=wd.switch_to.alert.accept()