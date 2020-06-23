from fbchat import Client
import pyautogui
import requests
import re
from bs4 import BeautifulSoup
import schedule
import time



njpeople = ['전송 명단']

wanthour = pyautogui.prompt(text="시간을 설정하세요.(ex: 06)",title="페이스북 급식알림이")
wantminute = pyautogui.prompt(text="분을 설정하세요.(ex: 45)",title="페이스북 급식알림이")
wantTime = wanthour+':'+wantminute;

date = pyautogui.prompt(title='페이스북 급식알림이', text='급식검색 요일을 입력해주세요.')
#급식
njurl = requests.get('https://search.naver.com/search.naver?sm=tab_hty.top&where=nexearch&query=남주고등학교 '+date+' 급식')
njhtml = njurl.text
njsoup = BeautifulSoup(njhtml, 'html.parser')
njmeal = njsoup.find_all("li", attrs={'class':'menu_info'})
njmeal = str(njmeal)

try:
	njlun = njmeal.split(date)[1]
	njlun = re.sub('<.+?>', '', njlun, 0).strip()
	njlun = re.sub('[0-9]+','',njlun, 0).strip()
	njlun = njlun.replace('.','\n').replace('[중식]','[중식]\n')
	njlun = re.sub('\n\n+', '\n', njlun, 0).strip()
	njlun = re.sub(' +', '', njlun, 0).strip()
	njlun = njlun.split(',')[0]

except:
	njlun = '[중식]\n중식이 검색되지 않았습니다.'

try:
	njdin = njmeal.split(date)[2].split(',')[0]
	njdin = re.sub('<.+?>', '', njdin, 0).strip()
	njdin = re.sub('[0-9]+','',njdin, 0).strip()
	njdin = njdin.replace('.','\n').replace('[석식]','[석식]\n')
	njdin = re.sub('\n\n+', '\n', njdin, 0).strip()
	njdin = re.sub(' +', '', njdin, 0).strip()
except:
	njdin = '[석식]\n석식이 검색되지 않았습니다.'

#온도
wturl = requests.get('https://search.naver.com/search.naver?sm=tab_hty.top&where=nexearch&query=%EC%84%9C%EA%B7%80%ED%8F%AC+%EB%82%A0%EC%94%A8')
wthtml = wturl.text
wtsoup = BeautifulSoup(wthtml, 'html.parser')
wttemp = wtsoup.find_all("span", attrs={'class':'todaytemp'})
wttemp = str(wttemp)
wttemp = re.sub('<.+?>', '', wttemp, 0).strip()
wttemp = wttemp.split(',')[0]
wttemp = wttemp.replace('[','')
wttemp = wttemp+"도"

#날씨
wtwea = wtsoup.find_all("p", attrs={'class':'cast_txt'})
wtwea = str(wtwea)
wtwea = re.sub('<[^>]+>','', wtwea, 0).strip()
wtwea = wtwea.split(',')[0]
wtwea = wtwea.replace('[','').replace(']','')

#미세먼지
wtdust = wtsoup.find_all("dl", attrs={'class':'indicator'})
wtdust = str(wtdust)
wtdust = re.sub('<[^>]+>','', wtdust, 0).strip()
wtdust = wtdust.split(',')[0]
wtdust = wtdust.replace('[','').replace(']','')

id = '아이디'
pw = '비번'

pyautogui.alert(title='페이스북 급식알림이', text='알림이 계정에 접속하는 중입니다 잠시만 기다려주세요.')
try:
	fc = Client(id, pw)
except:
	pyautogui.alert(title='로그인 오류', text='올바르지 않은 계정입니다 다시 입력해주세요.')
	id = pyautogui.prompt(title='페이스북 급식알림이', text='당신의 페이스북 아이디를 입력해주세요')
	pw = pyautogui.prompt(title='페이스북 급식알림이', text='당신의 페이스북 비밀번호를 입력해주세요')
	fc = Client(id, pw)

print('로그인 완료.')
#who = pyautogui.prompt(title='페이스북 급식알림이', text='누구에게 보내시겠습니까?')
pyautogui.alert(title='페이스북 급식알림이',text='해당 시간이 되면 알림이 전송됩니다.')

def notice():

	i = 0
	while i < len(njpeople):
		try:
			to = fc.searchForUsers(njpeople[i])[0]
			fc.sendMessage('[알림이]\n'+date+' 급식이 자동 공지됐어요!\n\n'+njlun+'\n\n'+njdin, thread_id=to.uid)
			fc.sendMessage('[알림이] 현재 날씨를 알려드릴게요!\n\n날씨: '+wtwea+'\n'+wtdust.replace(' 초미세먼지','\n초미세먼지').replace(' 오존지수','\n오존지수'), thread_id=to.uid)
			print('\n'+njpeople[i]+' 공지 완료.')
		except:
			print('    ['+njpeople[i]+']<<수신자 식별 오류로 건너띄어집니다.')
		i+=1



schedule.every().day.at(wantTime).do(notice)

while True:
    schedule.run_pending()
    time.sleep(1)



