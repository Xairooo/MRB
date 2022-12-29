_A6='return _w.rewardsQuizRenderInfo.currentQuestionNumber'
_A5='https://rewards.microsoft.com'
_A4='return _G.IG'
_A3='iscorrectoption'
_A2='return _w.rewardsQuizRenderInfo.numberOfOptions'
_A1='//*[@id="currentQuestionContainer"]'
_A0='Your account has been suspended'
_z='Linux'
_y='--headless'
_x='%H:%M'
_w='userStatus'
_v='urlreward'
_u='rqAnswerOption1'
_t='//*[@id="QuestionPane0"]/div[2]'
_s='return _w.rewardsQuizRenderInfo.maxQuestions'
_r='destinationUrl'
_q='[BING]'
_p='fly_id_rc'
_o='https://rewards.microsoft.com/dashboard'
_n='phoneverification'
_m='ban'
_l='withdrawal'
_k='r'
_j='quiz'
_i='rqAnswerOption0'
_h='bnp_container'
_g='lock'
_f='//*[@id="currentQuestionContainer"]/div/div[1]'
_e='bnp_hfly_cta2'
_d='b_notificationContainer_bop'
_c='password'
_b='More promotions'
_a='Punch cards'
_Z='Daily'
_Y='pointProgress'
_X='return _w.rewardsQuizRenderInfo.correctAnswer'
_W='true'
_V='complete'
_U='https://rewards.microsoft.com/'
_T='id_rc'
_S='Points'
_R="Today's points"
_Q='PC searches'
_P='data-option'
_O='/'
_N='bnp_btn_accept'
_M='mHamburger'
_L='promotionType'
_K='rqAnswerOption'
_J='//*[@id="rqStartQuiz"]'
_I=','
_H='[LOGIN]'
_G='username'
_F=None
_E='innerHTML'
_D='Last check'
_C='pointProgressMax'
_B=True
_A=False
import json,os,platform,random,subprocess,sys,time,urllib.parse
from pathlib import Path
from argparse import ArgumentParser
from datetime import date,datetime,timedelta
import traceback,ipapi,requests
from func_timeout import FunctionTimedOut,func_set_timeout
from random_word import RandomWords
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.common.exceptions import ElementNotInteractableException,NoAlertPresentException,NoSuchElementException,SessionNotCreatedException,TimeoutException,UnexpectedAlertPresentException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from email.message import EmailMessage
import ssl,smtplib,re
PC_USER_AGENT='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.24'
MOBILE_USER_AGENT='Mozilla/5.0 (Linux; Android 12; SM-N9750) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36 EdgA/107.0.1418.28'
POINTS_COUNTER=0
FINISHED_ACCOUNTS=[]
ERROR=_B
MOBILE=_B
CURRENT_ACCOUNT=_F
LOGS={}
FAST=_A
def browserSetup(isMobile,user_agent=PC_USER_AGENT,proxy=_F):
	from selenium.webdriver.chrome.options import Options;options=Options()
	if ARGS.session:
		if not isMobile:options.add_argument(f"--user-data-dir={Path(__file__).parent}/Profiles/{CURRENT_ACCOUNT}/PC")
		else:options.add_argument(f"--user-data-dir={Path(__file__).parent}/Profiles/{CURRENT_ACCOUNT}/Mobile")
	options.add_argument('user-agent='+user_agent);options.add_argument('lang='+LANG.split('-')[0]);options.add_argument('--disable-blink-features=AutomationControlled');prefs={'profile.default_content_setting_values.geolocation':2,'credentials_enable_service':_A,'profile.password_manager_enabled':_A,'webrtc.ip_handling_policy':'disable_non_proxied_udp','webrtc.multiple_routes_enabled':_A,'webrtc.nonproxied_udp_enabled':_A};options.add_experimental_option('prefs',prefs);options.add_experimental_option('useAutomationExtension',_A);options.add_experimental_option('excludeSwitches',['enable-automation'])
	if ARGS.headless:options.add_argument(_y)
	options.add_argument('log-level=3');options.add_argument('--start-maximized')
	if platform.system()==_z:options.add_argument('--no-sandbox');options.add_argument('--disable-dev-shm-usage')
	if proxy:options.add_argument(f"--proxy-server={proxy}")
	chrome_browser_obj=_F
	try:chrome_browser_obj=webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)
	except Exception:chrome_browser_obj=webdriver.Chrome(options=options)
	finally:return chrome_browser_obj
def login(browser,email,pwd,isMobile=_A):
	K='Unknown error !';J='loginHeader';I='[ERROR] Your account has been locked !';H='Your account has been locked !';G='Your account has been temporarily suspended';F='iNext';E='iAccrualForm';D="We're updating our terms";C='i0118';B='Ensuring login on Bing...';A='idSIButton9'
	if ARGS.session:
		time.sleep(2)
		if len(browser.window_handles)>1:
			current_window=browser.current_window_handle
			for handler in browser.window_handles:
				if handler!=current_window:browser.switch_to.window(handler);time.sleep(0.5);browser.close()
			browser.switch_to.window(current_window)
	browser.get('https://login.live.com/')
	if ARGS.session:
		if browser.title==D or isElementExists(browser,By.ID,E):time.sleep(2);browser.find_element(By.ID,F).click();time.sleep(5)
		if browser.title=='Microsoft account | Home'or isElementExists(browser,By.ID,'navs_container'):prGreen('[LOGIN] Account already logged in !');RewardsLogin(browser);print(_H,B);checkBingLogin(browser,isMobile);return
		elif browser.title==G:
			LOGS[CURRENT_ACCOUNT][_D]=H;FINISHED_ACCOUNTS.append(CURRENT_ACCOUNT)
			if ARGS.emailalerts:prRed('[EMAIL SENDER] This account has been locked! Sending email...');send_email(CURRENT_ACCOUNT,_g)
			updateLogs();cleanLogs();raise Exception(prRed(I))
		elif isElementExists(browser,By.ID,'mectrl_headerPicture')or'Sign In or Create'in browser.title:
			if isElementExists(browser,By.ID,C):browser.find_element(By.ID,C).send_keys(pwd);time.sleep(2);browser.find_element(By.ID,A).click();time.sleep(5);prGreen('[LOGIN] Account logged in again !');RewardsLogin(browser);print(_H,B);checkBingLogin(browser,isMobile);return
	waitUntilVisible(browser,By.ID,J,10);print(_H,'Writing email...');browser.find_element(By.NAME,'loginfmt').send_keys(email);browser.find_element(By.ID,A).click();time.sleep(5 if not FAST else 2);waitUntilVisible(browser,By.ID,J,10);browser.find_element(By.ID,C).send_keys(pwd);print(_H,'Writing password...');browser.find_element(By.ID,A).click();time.sleep(5)
	try:
		if browser.title==D or isElementExists(browser,By.ID,E):time.sleep(2);browser.find_element(By.ID,F).click();time.sleep(5)
		if ARGS.session:browser.find_element(By.ID,A).click()
		else:browser.find_element(By.ID,'idBtn_Back').click()
	except NoSuchElementException:
		if browser.title==G or isElementExists(browser,By.CLASS_NAME,'serviceAbusePageContainer  PageContainer'):LOGS[CURRENT_ACCOUNT][_D]=H;FINISHED_ACCOUNTS.append(CURRENT_ACCOUNT);updateLogs();cleanLogs();raise Exception(prRed(I))
		elif browser.title=='Help us protect your account':prRed('[ERROR] Unusual activity detected !');LOGS[CURRENT_ACCOUNT][_D]='Unusual activity detected !';FINISHED_ACCOUNTS.append(CURRENT_ACCOUNT);updateLogs();cleanLogs();os._exit(0)
		elif LOGS[CURRENT_ACCOUNT][_D]==K:FINISHED_ACCOUNTS.append(CURRENT_ACCOUNT);updateLogs();cleanLogs();raise Exception(prRed('[ERROR] Unknown error !'))
		else:LOGS[CURRENT_ACCOUNT][_D]=K;updateLogs();login(browser,email,pwd,isMobile);return
	time.sleep(5);print(_H,'Passing security checks...')
	try:browser.find_element(By.ID,'iLandingViewAction').click()
	except (NoSuchElementException,ElementNotInteractableException)as e:pass
	try:waitUntilVisible(browser,By.ID,'KmsiCheckboxField',10)
	except TimeoutException as e:pass
	try:browser.find_element(By.ID,A).click();time.sleep(5)
	except (NoSuchElementException,ElementNotInteractableException)as e:pass
	print(_H,'Logged-in !');print('[LOGIN] Logging into Microsoft Rewards...');RewardsLogin(browser);print(_H,B);checkBingLogin(browser,isMobile)
def RewardsLogin(browser):
	B='N/A';A='//*[@id="error"]/h1';browser.get(_o)
	try:time.sleep(10 if not FAST else 5);browser.find_element(By.ID,'raf-signin-link-id').click()
	except:pass
	time.sleep(10 if not FAST else 5)
	try:
		browser.find_element(By.ID,'error').is_displayed()
		if browser.find_element(By.XPATH,A).get_attribute(_E)==' Uh oh, it appears your Microsoft Rewards account has been suspended.':LOGS[CURRENT_ACCOUNT][_D]=_A0;LOGS[CURRENT_ACCOUNT][_R]=B;LOGS[CURRENT_ACCOUNT][_S]=B;cleanLogs();updateLogs();FINISHED_ACCOUNTS.append(CURRENT_ACCOUNT);raise Exception(prRed('[ERROR] Your Microsoft Rewards account has been suspended !'))
		elif browser.find_element(By.XPATH,A).get_attribute(_E)=='Microsoft Rewards is not available in this country or region.':
			prRed('[ERROR] Microsoft Rewards is not available in this country or region !')
			if sys.stdout.isatty():input('[ERROR] Press any key to close...')
			os._exit()
	except NoSuchElementException:pass
@func_set_timeout(300)
def checkBingLogin(browser,isMobile=_A):
	B='https://bing.com/';A='id_s';global POINTS_COUNTER;browser.get(B);time.sleep(15 if not FAST else 5)
	if ARGS.session:
		try:
			if not isMobile:
				try:POINTS_COUNTER=int(browser.find_element(By.ID,_T).get_attribute(_E))
				except ValueError:
					if browser.find_element(By.ID,A).is_displayed():browser.find_element(By.ID,A).click();time.sleep(15);checkBingLogin(browser,isMobile)
					time.sleep(2);POINTS_COUNTER=int(browser.find_element(By.ID,_T).get_attribute(_E).replace(_I,''))
			else:browser.find_element(By.ID,_M).click();time.sleep(1);POINTS_COUNTER=int(browser.find_element(By.ID,_p).get_attribute(_E))
		except:pass
		else:return _F
	try:browser.find_element(By.ID,_N).click()
	except:pass
	if isMobile:
		if isElementExists(browser,By.ID,'bnp_rich_div'):
			try:browser.find_element(By.XPATH,'//*[@id="bnp_bop_close_icon"]/img').click()
			except NoSuchElementException:pass
		try:time.sleep(1);browser.find_element(By.ID,_M).click()
		except:
			try:browser.find_element(By.ID,_N).click()
			except:pass
			time.sleep(1)
			if isElementExists(browser,By.XPATH,'//*[@id="bnp_ttc_div"]/div[1]/div[2]/span'):browser.execute_script("var element = document.evaluate('/html/body/div[1]', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;\n                                        element.remove();");time.sleep(5)
			time.sleep(1)
			try:browser.find_element(By.ID,_M).click()
			except:pass
		try:time.sleep(1);browser.find_element(By.ID,'HBSignIn').click()
		except:pass
		try:time.sleep(2);browser.find_element(By.ID,'iShowSkip').click();time.sleep(3)
		except:
			if str(browser.current_url).split('?')[0]=='https://account.live.com/proofs/Add':prRed('[LOGIN] Please complete the Security Check on '+CURRENT_ACCOUNT);FINISHED_ACCOUNTS.append(CURRENT_ACCOUNT);LOGS[CURRENT_ACCOUNT][_D]='Requires manual check!';updateLogs();exit()
	time.sleep(5);browser.get(B);time.sleep(15 if not FAST else 5)
	try:
		if not isMobile:
			try:POINTS_COUNTER=int(browser.find_element(By.ID,_T).get_attribute(_E))
			except:
				if browser.find_element(By.ID,A).is_displayed():browser.find_element(By.ID,A).click();time.sleep(15);checkBingLogin(browser,isMobile)
				time.sleep(5);POINTS_COUNTER=int(browser.find_element(By.ID,_T).get_attribute(_E).replace(_I,''))
		else:
			try:browser.find_element(By.ID,_M).click()
			except:
				try:browser.find_element(By.ID,'bnp_close_link').click();time.sleep(4);browser.find_element(By.ID,_N).click()
				except:pass
				time.sleep(1);browser.find_element(By.ID,_M).click()
			time.sleep(1);POINTS_COUNTER=int(browser.find_element(By.ID,_p).get_attribute(_E))
	except:checkBingLogin(browser,isMobile)
def waitUntilVisible(browser,by_,selector,time_to_wait=10):WebDriverWait(browser,time_to_wait).until(ec.visibility_of_element_located((by_,selector)))
def waitUntilClickable(browser,by_,selector,time_to_wait=10):WebDriverWait(browser,time_to_wait).until(ec.element_to_be_clickable((by_,selector)))
def waitUntilQuestionRefresh(browser):
	tries=0;refreshCount=0
	while _B:
		try:browser.find_elements(By.CLASS_NAME,'rqECredits')[0];return _B
		except:
			if tries<10:tries+=1;time.sleep(0.5)
			elif refreshCount<5:browser.refresh();refreshCount+=1;tries=0;time.sleep(5)
			else:return _A
def waitUntilQuizLoads(browser):
	tries=0;refreshCount=0
	while _B:
		try:browser.find_element(By.XPATH,_A1);return _B
		except:
			if tries<10:tries+=1;time.sleep(0.5)
			elif refreshCount<5:browser.refresh();refreshCount+=1;tries=0;time.sleep(5)
			else:return _A
def findBetween(s,first,last):
	try:start=s.index(first)+len(first);end=s.index(last,start);return s[start:end]
	except ValueError:return''
def getCCodeLangAndOffset():
	try:nfo=ipapi.location();lang=nfo['languages'].split(_I)[0];geo=nfo['country'];tz=str(round(int(nfo['utc_offset'])/100*60));return lang,geo,tz
	except:return'en-US','US','-480'
def getGoogleTrends(numberOfwords):
	A='query';search_terms=[];i=0
	while len(search_terms)<numberOfwords:
		i+=1;r=requests.get('https://trends.google.com/trends/api/dailytrends?hl='+LANG+'&ed='+str((date.today()-timedelta(days=i)).strftime('%Y%m%d'))+'&geo='+GEO+'&ns=15');google_trends=json.loads(r.text[6:])
		for topic in google_trends['default']['trendingSearchesDays'][0]['trendingSearches']:
			search_terms.append(topic['title'][A].lower())
			for related_topic in topic['relatedQueries']:search_terms.append(related_topic[A].lower())
		search_terms=list(set(search_terms))
	del search_terms[numberOfwords:len(search_terms)+1];return search_terms
def getRelatedTerms(word):
	try:r=requests.get('https://api.bing.com/osjson.aspx?query='+word,headers={'User-agent':PC_USER_AGENT});return r.json()[1]
	except:return[]
def resetTabs(browser):
	try:
		curr=browser.current_window_handle
		for handle in browser.window_handles:
			if handle!=curr:browser.switch_to.window(handle);time.sleep(0.5);browser.close();time.sleep(0.5)
		browser.switch_to.window(curr);time.sleep(0.5);browser.get(_U)
	except:browser.get(_U)
def getAnswerCode(key,string):
	t=0
	for i in range(len(string)):t+=ord(string[i])
	t+=int(key[-2:],16);return str(t)
def bingSearches(browser,numberOfSearches,isMobile=_A):
	global POINTS_COUNTER;i=0;R=RandomWords();search_terms=R.get_random_words(limit=numberOfSearches)
	if search_terms==_F:search_terms=getGoogleTrends(numberOfSearches)
	for word in search_terms:
		i+=1;print(_q,str(i)+_O+str(numberOfSearches));points=bingSearch(browser,word,isMobile)
		if points<=POINTS_COUNTER:
			relatedTerms=getRelatedTerms(word)
			for term in relatedTerms:
				points=bingSearch(browser,term,isMobile)
				if points>=POINTS_COUNTER:break
		if points>0:POINTS_COUNTER=points
		else:break
def bingSearch(browser,word,isMobile):
	B='https://bing.com';A='sb_form_q'
	try:
		if not isMobile:browser.find_element(By.ID,A).clear();time.sleep(1)
		else:browser.get(B)
	except:browser.get(B)
	time.sleep(2);searchbar=browser.find_element(By.ID,A)
	if FAST:searchbar.send_keys(word);time.sleep(1)
	else:
		for char in word:searchbar.send_keys(char);time.sleep(0.33)
	searchbar.submit();time.sleep(random.randint(12,24)if not FAST else random.randint(6,9));points=0
	try:
		if not isMobile:
			try:points=int(browser.find_element(By.ID,_T).get_attribute(_E))
			except ValueError:points=int(browser.find_element(By.ID,_T).get_attribute(_E).replace(_I,''))
		else:
			try:browser.find_element(By.ID,_M).click()
			except UnexpectedAlertPresentException:
				try:browser.switch_to.alert.accept();time.sleep(1);browser.find_element(By.ID,_M).click()
				except NoAlertPresentException:pass
			time.sleep(1);points=int(browser.find_element(By.ID,_p).get_attribute(_E))
	except:pass
	return points
def completePromotionalItems(browser):
	try:
		item=getDashboardData(browser)['promotionalItem']
		if(item[_C]==100 or item[_C]==200)and item[_V]==_A and item[_r]==_U:browser.find_element(By.XPATH,'//*[@id="promo-item"]/section/div/div/div/a').click();time.sleep(1);browser.switch_to.window(window_name=browser.window_handles[1]);time.sleep(8);browser.close();time.sleep(2);browser.switch_to.window(window_name=browser.window_handles[0]);time.sleep(2)
	except:pass
def completeDailySetSearch(browser,cardNumber):time.sleep(5);browser.find_element(By.XPATH,f'//*[@id="app-host"]/ui-view/mee-rewards-dashboard/main/div/mee-rewards-daily-set-section/div/mee-card-group/div/mee-card[{str(cardNumber)}]/div/card-content/mee-rewards-daily-set-item-content/div/a/div/span').click();time.sleep(1);browser.switch_to.window(window_name=browser.window_handles[1]);time.sleep(random.randint(13,17)if not FAST else random.randint(6,9));browser.close();time.sleep(2);browser.switch_to.window(window_name=browser.window_handles[0]);time.sleep(2)
def completeDailySetSurvey(browser,cardNumber):
	time.sleep(5);browser.find_element(By.XPATH,f'//*[@id="app-host"]/ui-view/mee-rewards-dashboard/main/div/mee-rewards-daily-set-section/div/mee-card-group/div/mee-card[{str(cardNumber)}]/div/card-content/mee-rewards-daily-set-item-content/div/a/div/span').click();time.sleep(1);browser.switch_to.window(window_name=browser.window_handles[1]);time.sleep(8 if not FAST else 5)
	if isElementExists(browser,By.ID,_h):browser.find_element(By.ID,_N).click();time.sleep(2)
	if isElementExists(browser,By.ID,_d):browser.find_element(By.ID,_e).click();time.sleep(2)
	browser.find_element(By.ID,'btoption'+str(random.randint(0,1))).click();time.sleep(random.randint(10,15)if not FAST else 7);browser.close();time.sleep(2);browser.switch_to.window(window_name=browser.window_handles[0]);time.sleep(2)
def completeDailySetQuiz(browser,cardNumber):
	time.sleep(5);browser.find_element(By.XPATH,f'//*[@id="app-host"]/ui-view/mee-rewards-dashboard/main/div/mee-rewards-daily-set-section[1]/div/mee-card-group[1]/div[1]/mee-card[{str(cardNumber)}]/div[1]/card-content[1]/mee-rewards-daily-set-item-content[1]/div[1]/a[1]/div[3]/span[1]').click();time.sleep(3);browser.switch_to.window(window_name=browser.window_handles[1]);time.sleep(12 if not FAST else random.randint(5,8))
	if not waitUntilQuizLoads(browser):resetTabs(browser);return
	if isElementExists(browser,By.ID,_h):browser.find_element(By.ID,_N).click();time.sleep(2)
	browser.find_element(By.XPATH,_J).click();waitUntilVisible(browser,By.XPATH,_f,10);time.sleep(3);numberOfQuestions=browser.execute_script(_s);numberOfOptions=browser.execute_script(_A2)
	for question in range(numberOfQuestions):
		if numberOfOptions==8:
			answers=[]
			for i in range(8):
				if browser.find_element(By.ID,_K+str(i)).get_attribute(_A3).lower()==_W:answers.append(_K+str(i))
			for answer in answers:
				if isElementExists(browser,By.ID,_d):browser.find_element(By.ID,_e).click();time.sleep(2)
				browser.find_element(By.ID,answer).click();time.sleep(5)
				if not waitUntilQuestionRefresh(browser):return
			time.sleep(5)
		elif numberOfOptions==4:
			correctOption=browser.execute_script(_X)
			for i in range(4):
				if browser.find_element(By.ID,_K+str(i)).get_attribute(_P)==correctOption:
					if isElementExists(browser,By.ID,_d):browser.find_element(By.ID,_e).click();time.sleep(2)
					browser.find_element(By.ID,_K+str(i)).click();time.sleep(5)
					if not waitUntilQuestionRefresh(browser):return
					break
			time.sleep(5)
	time.sleep(5);browser.close();time.sleep(2);browser.switch_to.window(window_name=browser.window_handles[0]);time.sleep(2)
def completeDailySetVariableActivity(browser,cardNumber):
	time.sleep(2);browser.find_element(By.XPATH,f'//*[@id="app-host"]/ui-view/mee-rewards-dashboard/main/div/mee-rewards-daily-set-section/div/mee-card-group/div/mee-card[{str(cardNumber)}]/div/card-content/mee-rewards-daily-set-item-content/div/a/div/span').click();time.sleep(1);browser.switch_to.window(window_name=browser.window_handles[1]);time.sleep(8)
	if isElementExists(browser,By.ID,_h):browser.find_element(By.ID,_N).click();time.sleep(2)
	try:browser.find_element(By.XPATH,_J).click();waitUntilVisible(browser,By.XPATH,_f,3)
	except (NoSuchElementException,TimeoutException):
		try:
			counter=str(browser.find_element(By.XPATH,_t).get_attribute(_E))[:-1][1:];numberOfQuestions=max([int(s)for s in counter.split()if s.isdigit()])
			for question in range(numberOfQuestions):
				if isElementExists(browser,By.ID,_d):browser.find_element(By.ID,_e).click();time.sleep(2)
				browser.execute_script(f"document.evaluate(\"//*[@id='QuestionPane{str(question)}']/div[1]/div[2]/a[{str(random.randint(1,3))}]/div\", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.click()");time.sleep(8)
			time.sleep(5);browser.close();time.sleep(2);browser.switch_to.window(window_name=browser.window_handles[0]);time.sleep(2);return
		except NoSuchElementException:time.sleep(random.randint(5,9));browser.close();time.sleep(2);browser.switch_to.window(window_name=browser.window_handles[0]);time.sleep(2);return
	time.sleep(3);correctAnswer=browser.execute_script(_X)
	if browser.find_element(By.ID,_i).get_attribute(_P)==correctAnswer:browser.find_element(By.ID,_i).click()
	else:browser.find_element(By.ID,_u).click()
	time.sleep(10);browser.close();time.sleep(2);browser.switch_to.window(window_name=browser.window_handles[0]);time.sleep(2)
def completeDailySetThisOrThat(browser,cardNumber):
	time.sleep(2);browser.find_element(By.XPATH,f'//*[@id="app-host"]/ui-view/mee-rewards-dashboard/main/div/mee-rewards-daily-set-section/div/mee-card-group/div/mee-card[{str(cardNumber)}]/div/card-content/mee-rewards-daily-set-item-content/div/a/div/span').click();time.sleep(1);browser.switch_to.window(window_name=browser.window_handles[1]);time.sleep(15 if not FAST else random.randint(5,8))
	if isElementExists(browser,By.ID,_h):browser.find_element(By.ID,_N).click();time.sleep(2)
	if not waitUntilQuizLoads(browser):resetTabs(browser);return
	browser.find_element(By.XPATH,_J).click();waitUntilVisible(browser,By.XPATH,_f,10);time.sleep(5)
	for question in range(10):
		if isElementExists(browser,By.ID,_d):browser.find_element(By.ID,_e).click();time.sleep(2)
		answerEncodeKey=browser.execute_script(_A4);answer1=browser.find_element(By.ID,_i);answer1Title=answer1.get_attribute(_P);answer1Code=getAnswerCode(answerEncodeKey,answer1Title);answer2=browser.find_element(By.ID,_u);answer2Title=answer2.get_attribute(_P);answer2Code=getAnswerCode(answerEncodeKey,answer2Title);correctAnswerCode=browser.execute_script(_X)
		if answer1Code==correctAnswerCode:answer1.click();time.sleep(15 if not FAST else 7)
		elif answer2Code==correctAnswerCode:answer2.click();time.sleep(15 if not FAST else 7)
	time.sleep(5);browser.close();time.sleep(2);browser.switch_to.window(window_name=browser.window_handles[0]);time.sleep(2)
def getDashboardData(browser):dashboard=findBetween(browser.find_element(By.XPATH,'/html/body').get_attribute(_E),'var dashboard = ',';\n        appDataModule.constant("prefetchedDashboard", dashboard);');dashboard=json.loads(dashboard);return dashboard
def completeDailySet(browser):
	B='Completing quiz of card ';A='[DAILY SET]';print(A,'Trying to complete the Daily Set...');d=getDashboardData(browser);error=_A;todayDate=datetime.today().strftime('%m/%d/%Y');todayPack=[]
	for (date,data) in d['dailySetPromotions'].items():
		if date==todayDate:todayPack=data
	for activity in todayPack:
		try:
			if activity[_V]==_A:
				cardNumber=int(activity['offerId'][-1:])
				if activity[_L]==_v:print(A,'Completing search of card '+str(cardNumber));completeDailySetSearch(browser,cardNumber)
				if activity[_L]==_j:
					if activity[_C]==50 and activity[_Y]==0:print(A,'Completing This or That of card '+str(cardNumber));completeDailySetThisOrThat(browser,cardNumber)
					elif(activity[_C]==40 or activity[_C]==30)and activity[_Y]==0:print(A,B+str(cardNumber));completeDailySetQuiz(browser,cardNumber)
					elif activity[_C]==10 and activity[_Y]==0:
						searchUrl=urllib.parse.unquote(urllib.parse.parse_qs(urllib.parse.urlparse(activity[_r]).query)['ru'][0]);searchUrlQueries=urllib.parse.parse_qs(urllib.parse.urlparse(searchUrl).query);filters={}
						for filter in searchUrlQueries['filters'][0].split(' '):filter=filter.split(':',1);filters[filter[0]]=filter[1]
						if'PollScenarioId'in filters:print(A,'Completing poll of card '+str(cardNumber));completeDailySetSurvey(browser,cardNumber)
						else:print(A,B+str(cardNumber));completeDailySetVariableActivity(browser,cardNumber)
		except:error=_B;resetTabs(browser)
	if not error:prGreen('[DAILY SET] Completed the Daily Set successfully !')
	else:prYellow('[DAILY SET] Daily Set did not completed successfully ! Streak not increased')
	LOGS[CURRENT_ACCOUNT][_Z]=_B;updateLogs()
def getAccountPoints(browser):return getDashboardData(browser)[_w]['availablePoints']
def completePunchCard(browser,url,childPromotions):
	A="document.getElementsByClassName('offer-cta')[0].click()";browser.get(url)
	for child in childPromotions:
		if child[_V]==_A:
			if child[_L]==_v:browser.execute_script(A);time.sleep(1);browser.switch_to.window(window_name=browser.window_handles[1]);time.sleep(random.randint(13,17));browser.close();time.sleep(2);browser.switch_to.window(window_name=browser.window_handles[0]);time.sleep(2)
			if child[_L]==_j and child[_C]>=50:
				browser.find_element(By.XPATH,'//*[@id="rewards-dashboard-punchcard-details"]/div[2]/div[2]/div[7]/div[3]/div[1]/a').click();time.sleep(1);browser.switch_to.window(window_name=browser.window_handles[1]);time.sleep(15)
				try:browser.find_element(By.XPATH,_J).click()
				except:pass
				time.sleep(5);waitUntilVisible(browser,By.XPATH,_A1,10);numberOfQuestions=browser.execute_script(_s);AnswerdQuestions=browser.execute_script('return _w.rewardsQuizRenderInfo.CorrectlyAnsweredQuestionCount');numberOfQuestions-=AnswerdQuestions
				for question in range(numberOfQuestions):answer=browser.execute_script(_X);browser.find_element(By.XPATH,f'//input[@value="{answer}"]').click();time.sleep(15)
				time.sleep(5);browser.close();time.sleep(2);browser.switch_to.window(window_name=browser.window_handles[0]);time.sleep(2);browser.refresh();break
			elif child[_L]==_j and child[_C]<50:
				browser.execute_script(A);time.sleep(1);browser.switch_to.window(window_name=browser.window_handles[1]);time.sleep(8);counter=str(browser.find_element(By.XPATH,_t).get_attribute(_E))[:-1][1:];numberOfQuestions=max([int(s)for s in counter.split()if s.isdigit()])
				for question in range(numberOfQuestions):browser.execute_script('document.evaluate("//*[@id=\'QuestionPane'+str(question)+"']/div[1]/div[2]/a["+str(random.randint(1,3))+']/div", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.click()');time.sleep(10)
				time.sleep(5);browser.close();time.sleep(2);browser.switch_to.window(window_name=browser.window_handles[0]);time.sleep(2);browser.refresh();break
def completePunchCards(browser):
	D='https://account.microsoft.com/rewards/dashboard/';C='https://rewards.microsoft.com/dashboard/';B='childPromotions';A='parentPromotion';print('[PUNCH CARDS]','Trying to complete the Punch Cards...');punchCards=getDashboardData(browser)['punchCards']
	for punchCard in punchCards:
		try:
			if punchCard[A]!=_F and punchCard[B]!=_F and punchCard[A][_V]==_A and punchCard[A][_C]!=0:
				url=punchCard[A]['attributes']['destination']
				if browser.current_url.startswith('https://rewards.'):path=url.replace(_A5,'');new_url=C;userCode=path[11:15];dest=new_url+userCode+path.split(userCode)[1]
				else:path=url.replace(D,'');new_url=D;userCode=path[:4];dest=new_url+userCode+path.split(userCode)[1]
				completePunchCard(browser,dest,punchCard[B])
		except:resetTabs(browser)
	time.sleep(2);browser.get(C);time.sleep(2);LOGS[CURRENT_ACCOUNT][_a]=_B;updateLogs();prGreen('[PUNCH CARDS] Completed the Punch Cards successfully !')
def completeMorePromotionSearch(browser,cardNumber):browser.find_element(By.XPATH,f'//*[@id="app-host"]/ui-view/mee-rewards-dashboard/main/div/mee-rewards-more-activities-card/mee-card-group/div/mee-card[{str(cardNumber)}]/div/card-content/mee-rewards-more-activities-card-item/div/a/div/span').click();time.sleep(1);browser.switch_to.window(window_name=browser.window_handles[1]);time.sleep(random.randint(13,17)if not FAST else random.randint(5,8));browser.close();time.sleep(2);browser.switch_to.window(window_name=browser.window_handles[0]);time.sleep(2)
def completeMorePromotionQuiz(browser,cardNumber):
	browser.find_element(By.XPATH,f'//*[@id="app-host"]/ui-view/mee-rewards-dashboard/main/div/mee-rewards-more-activities-card/mee-card-group/div/mee-card[{str(cardNumber)}]/div/card-content/mee-rewards-more-activities-card-item/div/a/div/span').click();time.sleep(1);browser.switch_to.window(window_name=browser.window_handles[1]);time.sleep(8 if not FAST else 5)
	if not waitUntilQuizLoads(browser):resetTabs(browser);return
	CurrentQuestionNumber=browser.execute_script(_A6)
	if CurrentQuestionNumber==1 and isElementExists(browser,By.XPATH,_J):browser.find_element(By.XPATH,_J).click()
	waitUntilVisible(browser,By.XPATH,_f,10);time.sleep(3);numberOfQuestions=browser.execute_script(_s);Questions=numberOfQuestions-CurrentQuestionNumber+1;numberOfOptions=browser.execute_script(_A2)
	for question in range(Questions):
		if numberOfOptions==8:
			answers=[]
			for i in range(8):
				if browser.find_element(By.ID,_K+str(i)).get_attribute(_A3).lower()==_W:answers.append(_K+str(i))
			for answer in answers:
				browser.find_element(By.ID,answer).click();time.sleep(5)
				if not waitUntilQuestionRefresh(browser):return
			time.sleep(5)
		elif numberOfOptions==4:
			correctOption=browser.execute_script(_X)
			for i in range(4):
				if browser.find_element(By.ID,_K+str(i)).get_attribute(_P)==correctOption:
					browser.find_element(By.ID,_K+str(i)).click();time.sleep(5)
					if not waitUntilQuestionRefresh(browser):return
					break
			time.sleep(5)
	time.sleep(5);browser.close();time.sleep(2);browser.switch_to.window(window_name=browser.window_handles[0]);time.sleep(2)
def completeMorePromotionABC(browser,cardNumber):
	browser.find_element(By.XPATH,f'//*[@id="app-host"]/ui-view/mee-rewards-dashboard/main/div/mee-rewards-more-activities-card/mee-card-group/div/mee-card[{str(cardNumber)}]/div/card-content/mee-rewards-more-activities-card-item/div/a/div/span').click();time.sleep(1);browser.switch_to.window(window_name=browser.window_handles[1]);time.sleep(8 if not FAST else 5);counter=str(browser.find_element(By.XPATH,_t).get_attribute(_E))[:-1][1:];numberOfQuestions=max([int(s)for s in counter.split()if s.isdigit()])
	for question in range(numberOfQuestions):browser.execute_script(f"document.evaluate(\"//*[@id='QuestionPane{str(question)}']/div[1]/div[2]/a[{str(random.randint(1,3))}]/div\", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.click()");time.sleep(8 if not FAST else 5)
	time.sleep(5);browser.close();time.sleep(2);browser.switch_to.window(window_name=browser.window_handles[0]);time.sleep(2)
def completeMorePromotionThisOrThat(browser,cardNumber):
	browser.find_element(By.XPATH,f'//*[@id="app-host"]/ui-view/mee-rewards-dashboard/main/div/mee-rewards-more-activities-card/mee-card-group/div/mee-card[{str(cardNumber)}]/div/card-content/mee-rewards-more-activities-card-item/div/a/div/span').click();time.sleep(1);browser.switch_to.window(window_name=browser.window_handles[1]);time.sleep(8 if not FAST else 5)
	if not waitUntilQuizLoads(browser):resetTabs(browser);return
	CrrentQuestionNumber=browser.execute_script(_A6);NumberOfQuestionsLeft=10-CrrentQuestionNumber+1
	if CrrentQuestionNumber==1 and isElementExists(browser,By.XPATH,_J):browser.find_element(By.XPATH,_J).click()
	waitUntilVisible(browser,By.XPATH,_f,10);time.sleep(3)
	for question in range(NumberOfQuestionsLeft):
		answerEncodeKey=browser.execute_script(_A4);answer1=browser.find_element(By.ID,_i);answer1Title=answer1.get_attribute(_P);answer1Code=getAnswerCode(answerEncodeKey,answer1Title);answer2=browser.find_element(By.ID,_u);answer2Title=answer2.get_attribute(_P);answer2Code=getAnswerCode(answerEncodeKey,answer2Title);correctAnswerCode=browser.execute_script(_X)
		if answer1Code==correctAnswerCode:answer1.click();time.sleep(8 if not FAST else 5)
		elif answer2Code==correctAnswerCode:answer2.click();time.sleep(8 if not FAST else 5)
	time.sleep(5);browser.close();time.sleep(2);browser.switch_to.window(window_name=browser.window_handles[0]);time.sleep(2)
def completeMorePromotions(browser):
	print('[MORE PROMO]','Trying to complete More Promotions...');morePromotions=getDashboardData(browser)['morePromotions'];i=0
	for promotion in morePromotions:
		try:
			i+=1
			if promotion[_V]==_A and promotion[_C]!=0:
				if promotion[_L]==_v:completeMorePromotionSearch(browser,i)
				elif promotion[_L]==_j:
					if promotion[_C]==10:completeMorePromotionABC(browser,i)
					elif promotion[_C]==30 or promotion[_C]==40:completeMorePromotionQuiz(browser,i)
					elif promotion[_C]==50:completeMorePromotionThisOrThat(browser,i)
				elif promotion[_C]==100 or promotion[_C]==200:completeMorePromotionSearch(browser,i)
			if promotion[_V]==_A and promotion[_C]==100 and promotion[_L]==''and promotion[_r]==_A5:completeMorePromotionSearch(browser,i)
		except:resetTabs(browser)
	LOGS[CURRENT_ACCOUNT][_b]=_B;updateLogs();prGreen('[MORE PROMO] Completed More Promotions successfully !')
def getRemainingSearches(browser):
	B='mobileSearch';A='pcSearch';dashboard=getDashboardData(browser);searchPoints=1;counters=dashboard[_w]['counters']
	if not A in counters:return 0,0
	progressDesktop=counters[A][0][_Y]+counters[A][1][_Y];targetDesktop=counters[A][0][_C]+counters[A][1][_C]
	if targetDesktop==33:searchPoints=3
	elif targetDesktop==55:searchPoints=5
	elif targetDesktop==102:searchPoints=3
	elif targetDesktop>=170:searchPoints=5
	remainingDesktop=int((targetDesktop-progressDesktop)/searchPoints);remainingMobile=0
	if dashboard[_w]['levelInfo']['activeLevel']!='Level1':progressMobile=counters[B][0][_Y];targetMobile=counters[B][0][_C];remainingMobile=int((targetMobile-progressMobile)/searchPoints)
	return remainingDesktop,remainingMobile
def isElementExists(browser,_by,element):
	try:browser.find_element(_by,element)
	except NoSuchElementException:return _A
	return _B
def validateTime(time):
	try:t=datetime.strptime(time,_x).strftime(_x)
	except ValueError:return _F
	else:return t
def argumentParser():
	B='*';A='store_true';parser=ArgumentParser(description='Microsoft Rewards Farmer V2.1',allow_abbrev=_A,usage='You may use execute the program with the default config or use arguments to configure available options.');parser.add_argument('--everyday',metavar='HH:MM',help='[Optional] This argument takes an input as time in 24h format (HH:MM) to execute the program at the given time everyday.',type=str,required=_A);parser.add_argument(_y,help='[Optional] Enable headless browser.',action=A,required=_A);parser.add_argument('--session',help='[Optional] Creates session for each account and use it.',action=A,required=_A);parser.add_argument('--error',help='[Optional] Display errors when app fails.',action=A,required=_A);parser.add_argument('--fast',help="[Optional] Reduce delays where ever it's possible to make script faster.",action=A,required=_A);parser.add_argument('--accounts',help='[Optional] Add accounts.',nargs=B,required=_A);parser.add_argument('--proxies',help='[Optional] Add proxies.',nargs=B,required=_A);parser.add_argument('--privacy',help='[Optional] Enable privacy mode.',action=A,required=_A);parser.add_argument('--emailalerts',help='[Optional] Enable GMAIL email alerts.',action=A,required=_A);parser.add_argument('--redeem',help='[Optional] Enable auto-redeem rewards based on accounts.json goals.',action=A,required=_A);args=parser.parse_args()
	if args.everyday:
		if isinstance(validateTime(args.everyday),str):args.everyday=validateTime(args.everyday)
		else:parser.error(f'"{args.everyday}" is not valid. Please use (HH:MM) format.')
	if args.fast:global FAST;FAST=_B
	if len(sys.argv)>1:
		for arg in vars(args):
			if'accounts'in arg or'proxies'in arg:
				if args.privacy:continue
			prBlue(f"[INFO] {arg} : {getattr(args,arg)}")
	return args
def logs():
	global LOGS;shared_items=[]
	try:
		LOGS=json.load(open(f"logs.txt",_k))
		for user in ACCOUNTS:
			shared_items.append(user[_G])
			if not user[_G]in LOGS.keys():LOGS[user[_G]]={_D:'',_R:0,_S:0}
		if shared_items!=LOGS.keys():
			diff=LOGS.keys()-shared_items
			for accs in list(diff):del LOGS[accs]
		for account in LOGS.keys():
			if LOGS[account][_D]==str(date.today())and list(LOGS[account].keys())==[_D,_R,_S]:FINISHED_ACCOUNTS.append(account)
			elif LOGS[account][_D]==_A0:FINISHED_ACCOUNTS.append(account)
			elif LOGS[account][_D]==str(date.today())and list(LOGS[account].keys())==[_D,_R,_S,_Z,_a,_b,_Q]:continue
			else:LOGS[account][_Z]=_A;LOGS[account][_a]=_A;LOGS[account][_b]=_A;LOGS[account][_Q]=_A
		updateLogs();prGreen('\n[LOGS] Logs loaded successfully.\n')
	except FileNotFoundError:
		prRed(f'\n[LOGS] "logs.txt" file not found.');LOGS={}
		for account in ACCOUNTS:LOGS[account[_G]]={_D:'',_R:0,_S:0,_Z:_A,_a:_A,_b:_A,_Q:_A}
		updateLogs();prGreen(f'[LOGS] "logs.txt" created.\n')
def updateLogs():
	global LOGS
	with open(time.strftime('log-%Y_%m_%d.txt'),'w')as file:file.write(json.dumps(LOGS,indent=4))
def cleanLogs():del LOGS[CURRENT_ACCOUNT][_Z];del LOGS[CURRENT_ACCOUNT][_a];del LOGS[CURRENT_ACCOUNT][_b];del LOGS[CURRENT_ACCOUNT][_Q]
def checkInternetConnection():
	C='8.8.8.8';B='1';A='ping';system=platform.system()
	while _B:
		try:
			if system=='Windows':subprocess.check_output([A,'-n',B,C],timeout=5)
			elif system==_z:subprocess.check_output([A,'-c',B,C],timeout=5)
			return
		except (subprocess.CalledProcessError,subprocess.TimeoutExpired):prRed('[ERROR] No internet connection.');time.sleep(1)
def prRed(prt):print(f"[91m{prt}[00m")
def prGreen(prt):print(f"[92m{prt}[00m")
def prYellow(prt):print(f"[93m{prt}[00m")
def prBlue(prt):print(f"[94m{prt}[00m")
def prPurple(prt):print(f"[95m{prt}[00m")
def loadAccounts():
	A='accounts.json';global ACCOUNTS
	if ARGS.accounts:
		ACCOUNTS=[]
		for account in ARGS.accounts:ACCOUNTS.append({_G:account.split(':')[0],_c:account.split(':')[1]})
	else:
		try:ACCOUNTS=json.load(open(A,_k))
		except FileNotFoundError:
			with open(A,'w')as f:f.write(json.dumps([{_G:'Your Email',_c:'Your Password'}],indent=4))
			prPurple(f'\n        [ACCOUNT] Accounts credential file "accounts.json" created.\n        [ACCOUNT] Edit with your credentials and save, then press any key to continue...\n            ');input();ACCOUNTS=json.load(open(A,_k))
def send_email(account,type):
	D='receiver';C='sender';B='email.json';A='false';email_info=[]
	try:email_info=json.load(open(B,_k))
	except FileNotFoundError:
		with open(B,'w')as f:f.write(json.dumps([{C:'sender@example.com',_c:'GoogleAppPassword',D:'receiver@example.com',_l:_W,_g:_W,_m:_W,_n:_W}],indent=4))
	email_sender=email_info[0][C];email_password=email_info[0][_c];email_receiver=email_info[0][D]
	if type==_l:
		if email_info[0][_l]==A:return
		email_subject=account+' has redeemed a card in Microsoft Rewards!';email_body="Check that account's mail!"
	elif type==_g:
		if email_info[0][_g]==A:return
		email_subject=account+' has been locked from Microsoft Rewards!';email_body='Fix it by logging in through this link: https://rewards.microsoft.com/'
	elif type==_m:
		if email_info[0][_m]==A:return
		email_subject=account+' has been shadow banned from Microsoft Rewards!';email_body='You can either close your account or try contacting support: https://support.microsoft.com/en-US'
	elif type==_n:
		if email_info[0][_n]==A:return
		email_subject=account+' needs phone verification for redeeming rewards!';email_body='Fix it by manually redeeming a reward: https://rewards.microsoft.com/'
	else:return
	email_message=EmailMessage();email_message['From']=email_sender;email_message['To']=email_receiver;email_message['Subject']=email_subject;email_message.set_content(email_body);ssl_context=ssl.create_default_context()
	with smtplib.SMTP_SSL('smtp.gmail.com',465,context=ssl_context)as smtp:
		try:smtp.login(email_sender,email_password)
		except:return
		smtp.sendmail(email_sender,email_receiver,email_message.as_string())
def redeem(browser,goal):
	D='[REDEEM] ';C='/html/body/div[1]/div[2]/main/div/ui-view/mee-rewards-dashboard/main/div/mee-rewards-redeem-info-card/div/mee-card-group/div/div[1]/mee-card/div/card-content/mee-rewards-redeem-goal-card/div/div[2]/div/a/span/ng-transclude';B='/html/body/div[1]/div[2]/main/div/ui-view/mee-rewards-dashboard/main/div/mee-rewards-redeem-info-card/div/mee-card-group/div/div[1]/mee-card/div/card-content/mee-rewards-redeem-goal-card/div/div[2]/p';A='[REDEEM] Ran into an exception trying to redeem!';goal=goal.lower();browser.get(_U)
	try:
		goal_name=browser.find_element(By.XPATH,value='/html/body/div[1]/div[2]/main/div/ui-view/mee-rewards-dashboard/main/div/mee-rewards-redeem-info-card/div/mee-card-group/div/div[1]/mee-card/div/card-content/mee-rewards-redeem-goal-card/div/div[2]/h3');goal_progress=browser.find_element(By.XPATH,value=B)
		if _O not in goal_progress.text.lower()or goal not in goal_name.text.lower():
			if _O in goal_progress.text.lower()and goal not in goal_name.text.lower():
				goal_progress=browser.find_element(By.XPATH,value=B).text.replace(' ','').split(_O);points=int(goal_progress[0].replace(_I,''));total=int(goal_progress[1].replace(_I,''))
				if points==total:element=browser.find_element(By.XPATH,value='/html/body/div[1]/div[2]/main/div/ui-view/mee-rewards-dashboard/main/div/mee-rewards-redeem-info-card/div/mee-card-group/div/div[1]/mee-card/div/card-content/mee-rewards-redeem-goal-card/div/div[2]/div/a[2]/span/ng-transclude')
				else:element=browser.find_element(By.XPATH,value=C)
				element.click();time.sleep(3);element=browser.find_element(By.XPATH,value=C)
			else:element=browser.find_element(By.XPATH,value=C)
			element.click();time.sleep(3);elements=browser.find_elements(By.CLASS_NAME,'c-image');goal_found=_A
			for e in elements:
				if goal in e.get_attribute('alt').lower():e.click();goal_found=_B;break
			if not goal_found:prRed('[REDEEM] Specified goal not found! Search for any typos in your accounts.json...');return
	except:print(traceback.format_exc());prRed(A);return
	finally:browser.get(_U)
	try:
		goal_progress=browser.find_element(By.XPATH,value=B).text
		if not _O in goal_progress:redeem(browser,goal);return
		else:goal_progress=goal_progress.replace(' ','').split(_O)
		points=int(goal_progress[0].replace(_I,''));total=int(goal_progress[1].replace(_I,''));goal=browser.find_element(By.XPATH,value='//*[@id="dashboard-set-goal"]/mee-card/div/card-content/mee-rewards-redeem-goal-card/div/div[2]/h3').text
		if points<total:print(D+str(total-points)+' points left to redeem your goal!');return
		elif points>=total:print('[REDEEM] points are ready to be redeemed!')
	except Exception as e:print(traceback.format_exc());prRed(A);return
	try:
		try:browser.find_element(By.XPATH,value='/html/body/div[1]/div[2]/main/div/ui-view/mee-rewards-dashboard/main/div/mee-rewards-redeem-info-card/div/mee-card-group/div/div[1]/mee-card/div/card-content/mee-rewards-redeem-goal-card/div/div[2]/div/a[1]/span/ng-transclude').click();time.sleep(random.uniform(2,4))
		except:time.sleep(random.uniform(3,5));browser.find_element(By.XPATH,value='/html/body/div[1]/div[2]/main/div/ui-view/mee-rewards-dashboard/main/div/mee-rewards-redeem-info-card/div/mee-card-group/div/div[1]/mee-card/div/card-content/mee-rewards-redeem-goal-card/div/div[2]/div/a[1]').click()
		try:
			url=browser.current_url;url=url.split(_O);id=url[-1]
			try:browser.find_element(By.XPATH,value=f'//*[@id="redeem-pdp_{id}"]').click();time.sleep(random.uniform(3,5))
			except:browser.find_element(By.XPATH,value=f'//*[@id="redeem-pdp_{id}"]/span[1]').click()
			try:browser.find_element(By.XPATH,value='//*[@id="redeem-checkout-review-confirm"]').click();time.sleep(random.uniform(3,5))
			except:browser.find_element(By.XPATH,value='//*[@id="redeem-checkout-review-confirm"]/span[1]').click()
		except Exception as e:browser.get(_U);print(traceback.format_exc());prRed(A);return
		try:
			veri=browser.find_element(By.XPATH,value='//*[@id="productCheckoutChallenge"]/form/div[1]').text
			if veri.lower()=='phone verification':
				prRed('[REDEEM] Phone verification required!')
				if ARGS.emailalerts:prRed('[EMAIL SENDER] Phone verification is required for redeeming a reward in this account! Sending email...');send_email(CURRENT_ACCOUNT,_n)
				return
		except:pass
		finally:time.sleep(random.uniform(5,10))
		try:
			error=browser.find_element(By.XPATH,value='//*[@id="productCheckoutError"]/div/div[1]').text
			if'issue with your account or order'in error.lower():
				message=f"\n[REDEEM] {CURRENT_ACCOUNT} has encountered the following message while attempting to auto-redeem rewards:\n{error}\nUnfortunately, this likely means this account has been shadow-banned. You may test your luck and contact support or just close the account and try again on another account.";prRed(message)
				if ARGS.emailalerts:prRed('[EMAIL SENDER] This account has been banned! Sending email...');send_email(CURRENT_ACCOUNT,_m)
				return
		except:pass
		prGreen(D+CURRENT_ACCOUNT+' points redeemed!')
		if ARGS.emailalerts:prGreen('[EMAIL SENDER] This account has redeemed a reward! Sending email...');send_email(CURRENT_ACCOUNT,_l)
		return
	except Exception as e:print(traceback.format_exc());prRed(A);return
def farmer():
	F='\n';E='goal';D='[LOGIN] Logged-in successfully !';C='Logging-in...';B='********************';A='***';global ERROR,MOBILE,CURRENT_ACCOUNT
	try:
		for account in ACCOUNTS:
			CURRENT_ACCOUNT=account[_G]
			if CURRENT_ACCOUNT in FINISHED_ACCOUNTS:continue
			if LOGS[CURRENT_ACCOUNT][_D]!=str(date.today()):LOGS[CURRENT_ACCOUNT][_D]=str(date.today());updateLogs()
			if ARGS.privacy:m=re.search('(\\w{3})(.*)(@\\w{3})(.*)(\\..*)',CURRENT_ACCOUNT);prYellow('******************** '+m.group(1)+A+m.group(3)+A+m.group(5)+' ********************')
			else:prYellow(B+CURRENT_ACCOUNT+B)
			if not LOGS[CURRENT_ACCOUNT][_Q]:
				browser=browserSetup(_A,PC_USER_AGENT,random.choice(ARGS.proxies)if ARGS.proxies else _F);print(_H,C);login(browser,account[_G],account[_c]);prGreen(D);startingPoints=POINTS_COUNTER;prGreen('[POINTS] You have '+str(POINTS_COUNTER)+' points on your account !');browser.get(_o)
				if not LOGS[CURRENT_ACCOUNT][_Z]:completeDailySet(browser)
				if not LOGS[CURRENT_ACCOUNT][_a]:completePunchCards(browser)
				if not LOGS[CURRENT_ACCOUNT][_b]:completeMorePromotions(browser)
				remainingSearches,remainingSearchesM=getRemainingSearches(browser);MOBILE=bool(remainingSearchesM)
				if remainingSearches!=0:print(_q,'Starting Desktop and Edge Bing searches...');bingSearches(browser,remainingSearches);prGreen('[BING] Finished Desktop and Edge Bing searches !');LOGS[CURRENT_ACCOUNT][_Q]=_B;updateLogs();ERROR=_A
				if ARGS.redeem:
					if E in account:goal=account[E]
					else:print('[REEDEM] Goal has not been defined for this account, defaulting to Amazon Giftcard...');goal='Amazon';redeem(browser,goal)
				browser.quit()
			if MOBILE:
				browser=browserSetup(_B,account.get('mobile_user_agent',MOBILE_USER_AGENT),random.choice(ARGS.proxies)if ARGS.proxies else _F);print(_H,C);login(browser,account[_G],account[_c],_B);prGreen(D)
				if LOGS[account[_G]][_Q]and ERROR:startingPoints=POINTS_COUNTER;browser.get(_o);remainingSearches,remainingSearchesM=getRemainingSearches(browser)
				if remainingSearchesM!=0:print(_q,'Starting Mobile Bing searches...');bingSearches(browser,remainingSearchesM,_B)
				prGreen('[BING] Finished Mobile Bing searches !');browser.quit()
			New_points=POINTS_COUNTER-startingPoints;prGreen('[POINTS] You have earned '+str(New_points)+' points today !');prGreen('[POINTS] You are now at '+str(POINTS_COUNTER)+' points !\n');FINISHED_ACCOUNTS.append(CURRENT_ACCOUNT);LOGS[CURRENT_ACCOUNT][_R]=New_points;LOGS[CURRENT_ACCOUNT][_S]=POINTS_COUNTER;cleanLogs();updateLogs()
	except FunctionTimedOut:prRed('[ERROR] Time out raised.\n');ERROR=_B;browser.quit();farmer()
	except KeyboardInterrupt:ERROR=_B;browser.quit();input('\n\x1b[94m[INFO] Farmer paused. Press enter to continue...\x1b[00m\n');farmer()
	except Exception as e:print(e,F)if ARGS.error else print(F);ERROR=_B;browser.quit();checkInternetConnection();farmer()
	else:FINISHED_ACCOUNTS.clear()
def main():
	global LANG,GEO,TZ,ARGS;start=time.time()
	if os.name=='nt':os.system('color')
	ARGS=argumentParser();LANG,GEO,TZ=getCCodeLangAndOffset();loadAccounts()
	if ARGS.everyday is not _F:
		while _B:
			if datetime.now().strftime(_x)==ARGS.everyday:logs();farmer()
			time.sleep(30)
	else:logs();farmer()
	end=time.time();delta=end-start;hour,remain=divmod(delta,3600);min,sec=divmod(remain,60);print(f"The script took : {hour:02.0f}:{min:02.0f}:{sec:02.0f}");LOGS['Elapsed time']=f"{hour:02.0f}:{min:02.0f}:{sec:02.0f}";updateLogs()
if __name__=='__main__':main()