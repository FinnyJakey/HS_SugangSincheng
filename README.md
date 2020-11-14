# HS_SugangSincheng
Univ. Subject Auto Sign Up


#### #Module List
sys, requests, os, BeautifulSoup4, PyQt, time


#### #Func.
Login, Univ. Login, 장바구니 목록, 장바구니에 담겨져 있는 과목 정보, 장바구니 자동 신청, 수동 추가 및 신청, 정각이 되기 2초 전부터 수강신청 패킷을 여러번 날림


#### #How to build
pyinstaller --windowed -F --icon=test.ico TicketingMacro.spec

--windowed -> 콘솔 창이 나오지 않게
-F -> 하나의 파일로
--icon -> 파일 아이콘 지정
py가 아닌 spec으로 컴파일
