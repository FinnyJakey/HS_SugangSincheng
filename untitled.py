import sys
import requests
import os
from bs4 import BeautifulSoup as bs
from PyQt5.QtWidgets import *
from PyQt5 import uic
import time
from PyQt5.QtCore import *



def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

form = resource_path('untitled.ui')

form_class = uic.loadUiType(form)[0]



class WindowClass(QMainWindow, form_class) :
    def __init__(self) :
        super().__init__()
        self.setupUi(self)

        self.pushButtonLogin.clicked.connect(self.pushButtonLoginFunc)
        self.listWidgetBasket.itemClicked.connect(self.listWidgetBasketFunc)
        self.pushButtonPost.clicked.connect(self.pushButtonPostFunc)
        self.pushButtonManualAdd.clicked.connect(self.pushButtonManualAddFunc)
        self.pushButtonManualDel.clicked.connect(self.pushButtonManualDelFunc)
        self.pushButtonManualPost.clicked.connect(self.pushButtonManualPostFunc)
        self.pushButtonCancel.clicked.connect(self.pushButtonCancelFunc)

        # dothome 연동

        self.pushButtonRegister_2.clicked.connect(self.pushButtonRegister_2Func)
        self.pushButtonLogin_2.clicked.connect(self.pushButtonLogin_2Func)
        self.pushButtonCode_2.clicked.connect(self.pushButtonCode_2Func)

    
    def pushButtonRegister_2Func(self) :
        with requests.session() as s:
            register = s.get('http://site-ruined.000webhostapp.com/main.php?param=Register&id=' + self.lineEditID_2.text() + '&pw=' + self.lineEditPW_2.text() + '&rpw=' + self.lineEditPW_2.text())
            
        if str(100) in register.text :
            self.textBrowserResult.append("회원가입 완료")
        else :
            self.textBrowserResult.append("회원가입 실패")
        

    def pushButtonLogin_2Func(self) :
        with requests.session() as s:
            login = s.get('http://site-ruined.000webhostapp.com/main.php?param=Login&id=' + self.lineEditID_2.text() + '&pw=' + self.lineEditPW_2.text())
        
        if str(100) in login.text :
            self.textBrowserResult.append("로그인 성공")
            self.lineEditID.setEnabled(True)
            self.lineEditPW.setEnabled(True)
            self.pushButtonLogin.setEnabled(True)

            self.lineEditID_2.setEnabled(False)
            self.lineEditPW_2.setEnabled(False)
            self.pushButtonRegister_2.setEnabled(False)
            self.pushButtonLogin_2.setEnabled(False)
        else :
            self.textBrowserResult.append("로그인 실패")


    def pushButtonCode_2Func(self) :
        with requests.session() as s:
            code = s.get('http://site-ruined.000webhostapp.com/main.php?param=useCode&id=' + self.lineEditID_2.text() + '&pw=' + self.lineEditPW_2.text() + '&code=' + self.lineEditCode_2.text())
        
        if str(100) in code.text :
            self.textBrowserResult.append("코드 충전 완료")
        else :
            self.textBrowserResult.append("코드가 올바르지 않습니다.")



            
        
        
        
        
    
    def pushButtonLoginFunc(self) :
        LOGIN_INFO = {
            'id' : self.lineEditID.text(),
            'passwd' : self.lineEditPW.text()
            }
        
        with requests.session() as s:
            
            s.get('https://info.hansung.ac.kr/servlet/s_gong.gong_login_ssl', verify = False)
            s.post('https://info.hansung.ac.kr/servlet/s_gong.gong_login_ssl', data=LOGIN_INFO)
            your_basket = s.get('https://info.hansung.ac.kr/jsp/pre_sugang/h_sugang_sincheong_i01_bottom_pre.jsp')
            soup = bs(your_basket.text, 'html.parser')
            

            login_test = str(soup).find("divSugangTitle")

            
            

            if not login_test == -1 :

        
                basket_list = soup.findAll("span", "divSugangTitle")
                
                self.textBrowserResult.append("종정시 로그인 성공")

                
            

                try :
                    for x in range(0, 10) :
                        self.listWidgetBasket.addItem(basket_list[x].text)
                        


                except :
                        self.lineEditID.setEnabled(False)
                        self.lineEditPW.setEnabled(False)
                        self.pushButtonLogin.setEnabled(False)
                        self.pushButtonPost.setEnabled(True) # PushButtonPostFunc -> ManualPost처럼 작성하고 True로 바꿀 것!
                        self.pushButtonManualPost.setEnabled(True)
            else :
                self.textBrowserResult.append("종정시 로그인 실패")


    def listWidgetBasketFunc(self) :
        try :
            LOGIN_INFO = {
            'id' : self.lineEditID.text(),
            'passwd' : self.lineEditPW.text()
            }

            with requests.session() as s:
                s.post('https://info.hansung.ac.kr/servlet/s_gong.gong_login_ssl', data=LOGIN_INFO)
                your_basket = s.get('https://info.hansung.ac.kr/jsp/pre_sugang/h_sugang_sincheong_i01_bottom_pre.jsp')
                soup = bs(your_basket.text, 'html.parser')

                basket_info = soup.findAll("span", "pleft20")
                
                

                self.textBrowserInfo.clear()
                x = int(self.listWidgetBasket.currentRow())

                y = basket_info[x].text
                
                z = y.split('|')
                
                self.textBrowserInfo.append("분반 : " + z[0])
                self.textBrowserInfo.append("\n")
                self.textBrowserInfo.append("이수 : " + z[1])
                self.textBrowserInfo.append("\n")
                self.textBrowserInfo.append("학점 :" + z[2])
                self.textBrowserInfo.append("\n")
                self.textBrowserInfo.append("담당교수 : " + z[3])
                
                


                


        except :
            print("Error")

    def pushButtonPostFunc(self) :
        LOGIN_INFO = {
            'id' : self.lineEditID.text(),
            'passwd' : self.lineEditPW.text()
            }

        


        with requests.session() as s:

            HEADERS = {
            'User-Agent' : ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36'),
            'Referer' : 'https://info.hansung.ac.kr/jsp/sugang/h_sugang_sincheong_main.jsp',
            'Accept' : 'text/html, */*; q=0.01'
            }
            s.get('https://info.hansung.ac.kr/servlet/s_gong.gong_login_ssl', verify = False)
            s.post('https://info.hansung.ac.kr/servlet/s_gong.gong_login_ssl', data=LOGIN_INFO)
        
            your_basket = s.get('https://info.hansung.ac.kr/jsp/pre_sugang/h_sugang_sincheong_i01_bottom_pre.jsp')
            soup = bs(your_basket.text, 'html.parser')
            basket_info = soup.findAll("span", "pleft20")

            x = int(self.listWidgetBasket.count())

            global Check
            Check = 1



            while not Check == 0 :
                
                tm = time.localtime()
                time.sleep(0.5)
                QApplication.processEvents()
                time.sleep(0.5)
                
                
                
                if tm.tm_min == 59 :
                    if tm.tm_sec == 58 :
                        while True :

                            
                            for t in range(0, x) :
                                y = basket_info[t].text
                                z = y.split('|')

                                w = self.listWidgetBasket.item(t).text()[1:8]
                                

                                TEST_PARAMS = {
                                'gwamok' : w,
                                'bunban' : str(z[0])[1:2],
                                'track' : 'undefined',
                                'year' : '1',
                                'cert' : '1'
                                }
                
                                s.get('https://info.hansung.ac.kr/jsp/sugang/h_sugang_sincheong_i02_s_20160128.jsp', params=TEST_PARAMS, headers=HEADERS)
                                
                                self.textBrowserResult.append("Initiating...")
                                self.textBrowserResult.append("Loop for 10sec...")
                                
                                QApplication.processEvents()
                                
                            tm = time.localtime()    
                                

                            
                            if tm.tm_sec == 10 :
                                Check = 0
                                self.textBrowserResult.append("정상처리 완료")
                                break
                                
                                
                                    
                                
                    else :
                        
                        self.textBrowserResult.append(str(tm.tm_min) + "분 "+ str(tm.tm_sec) + "초")
                        QApplication.processEvents()
                        
                        
                            
                else :
                    
                    self.textBrowserResult.append(str(tm.tm_min) + "분 " + str(tm.tm_sec) + "초")
                    QApplication.processEvents()

            

    def pushButtonManualAddFunc(self) :

        if not self.lineEditCode.text() == '' :
            if not self.lineEditClass.text() == '' :
                self.listWidgetManual.addItem('[' + self.lineEditCode.text() + '-' + self.lineEditClass.text() + ']')
                self.lineEditCode.clear()
                self.lineEditClass.clear()
        
    def pushButtonManualDelFunc(self) :
        self.listWidgetManual.takeItem(self.listWidgetManual.currentRow())

    def pushButtonManualPostFunc(self) :
        LOGIN_INFO = {
            'id' : self.lineEditID.text(),
            'passwd' : self.lineEditPW.text()
            }

        


        with requests.session() as s:

            HEADERS = {
            'User-Agent' : ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36'),
            'Referer' : 'https://info.hansung.ac.kr/jsp/sugang/h_sugang_sincheong_main.jsp',
            'Accept' : 'text/html, */*; q=0.01'
            }
            s.get('https://info.hansung.ac.kr/servlet/s_gong.gong_login_ssl', verify = False)
            s.post('https://info.hansung.ac.kr/servlet/s_gong.gong_login_ssl', data=LOGIN_INFO)


            

            global Check
            Check = 1
            



            while not Check == 0 :
                
                tm = time.localtime()
                time.sleep(0.5)
                QApplication.processEvents()
                time.sleep(0.5)
                
                
                
                if tm.tm_min == 59 :
                    if tm.tm_sec == 58 :
                        while True :
                            for x in range(0, self.listWidgetManual.count()) :
                                mList = self.listWidgetManual.item(x).text()
                                mListCode = mList[1:8]
                                mListClass = mList[9:10]

                                TEST_PARAMS = {
                                    'gwamok' : mListCode,
                                    'bunban' : mListClass,
                                    'track' : 'undefined',
                                    'year' : '1',
                                    'cert' : '1'
                                }
                                s.get('https://info.hansung.ac.kr/jsp/sugang/h_sugang_sincheong_i02_s_20160128.jsp', params=TEST_PARAMS, headers=HEADERS)
                                
                                self.textBrowserResult.append("Initiating...")
                                self.textBrowserResult.append("Loop for 10sec...")
                                
                                QApplication.processEvents()
                                
                            tm = time.localtime()
                                

                            
                            if tm.tm_sec == 10 :
                                Check = 0
                                self.textBrowserResult.append("정상처리 완료")
                                break
                                
                                
                                    
                                
                    else :
                        
                        self.textBrowserResult.append(str(tm.tm_min) + "분 "+ str(tm.tm_sec) + "초")
                        QApplication.processEvents()
                        
                        
                            
                else :
                    
                    self.textBrowserResult.append(str(tm.tm_min) + "분 " + str(tm.tm_sec) + "초")
                    QApplication.processEvents()


    def pushButtonCancelFunc(self) :

        global Check
        Check = 0
        self.textBrowserResult.append("취소")                 
                    
                    
                    
                        

    
    



                    




if __name__ == "__main__" :
    app = QApplication(sys.argv)
    #app.setStyle('Breeze')
    
    myWindow = WindowClass()

    myWindow.show()

    app.exec_()

# 1. Python Request Module
# 2. 08/13 LoginButton 구현/ 장바구니 및 로그인 그룹 Enabled/Disabled
# 3. Request Speed / 학점 조회
# 4. 수동 신청 클릭했을 때 textBrowserInfo 에 분반 / 이수 / 학점 / 담당교수 append
# 5. 수동 추가 시 성공 / 실패 (성공하면 과목 이름 가져오기)
# 6. request module Class화
