from flask import Flask,request, jsonify
from . import api, response
from .. import app, db, blacklist, mail
from app.models.chat import Chat
from app.models.specific_period import SpecificPeriod
from app.models.research import Research
from app.models.specific_period_research import SpecificPeriodResearch
from flask import session
# import sys
# sys.path.append(r"/home/test/software_engineering/pair/ccu_ai_lab_backend/app/api/chatbot")
from .chatbot import get_res
import string
import time
import datetime
from .decorators import token_required
import os
import json
#import distance
import Levenshtein
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'



#@token_required

@api.route('/chat/reply_error', methods = ['POST'])
def reply_error():
	msg_id = request.json.get('id')
	info = Chat.query.filter_by(id=msg_id).all()
	if(len(info)>0):
		info[0].status = 1
		db.session.commit()
	return response.success(msg_id)
	
@api.route('/chat/get_response', methods = ['POST'])
def get_response():
	user_id = request.json.get('user_id')
	cookie = request.json.get('token')
	user_content = request.json.get('msg')



	jsonInfo = get_res.send_msg(user_content)
	if jsonInfo is None:
		jsonInfo = {}
		jsonInfo['response'] = "sorry I can't get it. Please try to input much detail...QQ"
		jsonInfo['flag']=" "
		jsonInfo['project_types']=" "
		jsonInfo['time']=" "
		jsonInfo['country'] = " "
		jsonInfo['member'] = " "
		jsonInfo['department'] = " "
	
	###############test code################
	#jsonInfo['flag']="1"
	#jsonInfo['project_types']="C++ AI"
	#jsonInfo['time']="1~3"
	'''
	jsonInfo = {}
	jsonInfo['response'] = " "
	jsonInfo['flag']="1"
	jsonInfo['project_types']=" "
	jsonInfo['time']=" "
	jsonInfo['country'] = " "
	jsonInfo['member'] = " "
	jsonInfo['department'] = "trash"
	
	'''
	###############         ################
	ai_content = jsonInfo['response']
	flag = jsonInfo['flag']
	project_types = jsonInfo['project_types']
	if(project_types != " "):
		project_types=project_types.lstrip()
		project_types = project_types.split(' ')
	project_types_num = len(project_types)
	department = jsonInfo['department']
	country = jsonInfo['country']
	member = jsonInfo['member']
	time_ = jsonInfo['time']
	
	
	
	head_msg="Here are some guides:<br/><br/>"
	project_info_msg="Project fields (AI, IOT)<br/>"
	project_duration_msg="Project duration<br/>"
	project_departments_msg="Project departments (Computer Science)<br/>"
	country_msg="Country (India, Taiwan)<br/>"
	end_msg="<br/>If you want to show it again, please type 'help'<br/>"
	allcnt=4
	cnt = allcnt
	if(user_content == "help"):
		ai_content = head_msg
		if(project_types == " "):
			cnt -= 1
			ai_content += str(allcnt-cnt) + ". " + project_info_msg
		if(time_ == " "):
			cnt -= 1
			ai_content += str(allcnt-cnt) + ". " + project_duration_msg
		if(department == " "):
			cnt -= 1
			ai_content += str(allcnt-cnt) + ". " + project_departments_msg
		if(country == " "):
			cnt -= 1
			ai_content += str(allcnt-cnt) + ". " + country_msg
		ai_content += end_msg
		if(cnt == allcnt):
			ai_content = "you have already set the whole condition. <br/>You can still add another project_fields and departments."
	else:
		if(project_types == " "):
			cnt -= 1
		if(time_ == " "):
			cnt -= 1
		if(department == " "):
			cnt -= 1
		if(country == " "):
			cnt -= 1
		#"flag": " ", "project_types": " ", "department": " ", "time": " ", "member": " " , "country":" " , "response":" "}'
	#ai_content = "content from AI."
	if(flag=="2"):
		get_search = Research.query.filter_by().order_by(Research.id.desc()).all()
		count=1
		if(ai_content==""):
			ai_content="There are what you want."
		for ans in get_search:
			ans = ans.to_json()
			ai_content = ai_content + "<br>" + str(count) + ". " + ans['name']
			count+=1
	if(flag=="1"):
		alldata = {}
		get_search=""
		status=0
		if(time_!=" "):
			time_=time_.lstrip()
			during=time_.split('~')
			get_search = SpecificPeriod.query.order_by(SpecificPeriod.id.desc()).all()
			for ans in get_search:
				ans = ans.to_json()
				if(time.strptime(ans['apply_copi_end_date'], "%Y-%m-%d %H:%M:%S")<time.localtime()):
						continue
				endtime=time.strptime(ans['end_date'], "%Y-%m-%d %H:%M:%S")
				begintime=time.strptime(ans['start_date'], "%Y-%m-%d %H:%M:%S")
				time_during=((endtime.tm_year-begintime.tm_year)*12+(endtime.tm_mon-begintime.tm_mon))*30+(endtime.tm_mday-begintime.tm_mday)
				begin=int(during[0])*30
				end=int(during[1])*30
				if(time_during<begin or time_during>end):
					continue
				if(ans['id'] in alldata):
					alldata[ans['id']]+=100
				else:
					alldata[ans['id']]=100
		if(project_types!=" "):
			for i in range(0,project_types_num):
				get_search = Research.query.filter_by(name=project_types[i]).order_by(Research.id.desc()).all()
				for ans in get_search:
					ans = ans.to_json()
					temp = SpecificPeriodResearch.query.filter_by(research_id=ans['id']).order_by(SpecificPeriodResearch.id.desc()).all()
					for ans2 in temp:
						ans2 = ans2.to_json()
						temp2 = SpecificPeriod.query.filter_by(id=ans2['specific_period_id']).order_by(SpecificPeriod.id.desc()).first()
						temp2 = temp2.to_json()
						if(time.strptime(temp2['apply_copi_end_date'], "%Y-%m-%d %H:%M:%S")<time.localtime()):
							continue
						if(ans2['specific_period_id'] in alldata):
							if(alldata[ans2['specific_period_id']]%100>0):
								alldata[ans2['specific_period_id']]+=1
							else:
								alldata[ans2['specific_period_id']]+=101
						else:
							alldata[ans2['specific_period_id']]=101
		if(department!=" "):
			get_search = SpecificPeriod.query.all()	
			for ans in get_search:
				ans = ans.to_json()
				if(time.strptime(ans['apply_copi_end_date'], "%Y-%m-%d %H:%M:%S")<time.localtime()):
					continue
				xlen=len(department)+len(ans['department'])
				department = department.replace(' ', '_')
				department_abbr_array = department.split('_')
				department_abbr = ""
				for item in department_abbr_array:
					department_abbr += item[0]
					
				
				ans_abbr_array = ans['department'].split(' ')
				ans_abbr = ""
				for item in ans_abbr_array:
					ans_abbr += item[0]
					
				x=Levenshtein.distance(department.lower(), ans['department'].lower())
				y=Levenshtein.ratio(department.lower(), ans['department'].lower())
				a=100
				b=0
				c=100
				d=0
				e=100
				f=0
				if(len(department_abbr)>=2 and len(ans_abbr)>=2):
					a=Levenshtein.distance(department_abbr.lower(), ans_abbr.lower())
					b=Levenshtein.ratio(department_abbr.lower(), ans_abbr.lower())
				if(len(department_abbr)>=2):
					e=Levenshtein.distance(department_abbr.lower(), ans['department'].lower())
					f=Levenshtein.ratio(department_abbr.lower(), ans['department'].lower())
				if(len(ans_abbr)>=2):
					c=Levenshtein.distance(department.lower(), ans_abbr.lower())
					d=Levenshtein.ratio(department.lower(), ans_abbr.lower())
				if(x<=2 or y>=0.8 or a<=1 or b>=0.8 or c<=1 or d>=0.8 or e<=1 or f>=0.8):
					if(ans['id'] in alldata):
						alldata[ans['id']]+=100
					else:
						alldata[ans['id']]=100
		if(country!=" "):
			get_search = SpecificPeriod.query.filter_by(country=country).all()
			x=0
			for ans in get_search:
				ans = ans.to_json()
				x=1
				if(time.strptime(ans['apply_copi_end_date'], "%Y-%m-%d %H:%M:%S")<time.localtime()):
					continue
				if(ans['id'] in alldata):
					alldata[ans['id']]+=100
				else:
					alldata[ans['id']]=100
			if(x==0):
				get_search = SpecificPeriod.query.all()
				catch=get_country()
				for ans in get_search:
					ans = ans.to_json()
					if ans['country'] in catch.keys():
						a=Levenshtein.distance(country.lower(),catch[ans['country']].lower())
						b=Levenshtein.ratio(country.lower(),catch[ans['country']].lower())
						if(time.strptime(ans['apply_copi_end_date'], "%Y-%m-%d %H:%M:%S")<time.localtime()):
							continue
						if(a<=1 or b>=0.8):
							if(ans['id'] in alldata):
								alldata[ans['id']]+=100
							else:
								alldata[ans['id']]=100
		
		count=0
		sort_temp=list(alldata.values())
		sort_temp.sort(reverse=True)
		dist_sort={}
		for i in sort_temp:
			for j in alldata.keys():
				if(alldata[j]==i):
					dist_sort[j]=i
		for i in range(cnt,0,-1):
			if(count<6):
				for temp in dist_sort.keys():
					if((int)(dist_sort[temp]/100)==i):
						count+=1
						get_search = SpecificPeriod.query.filter_by(id=temp).order_by(SpecificPeriod.id.desc()).first()
						get_search = get_search.to_json()
						ai_content = ai_content + "<br>" + "<a href=\"http://localhost:8080/#/projects/" + str(temp) + "\" target='_blank' >" + str(count) + ". " + get_search['project_title'] + "</a>"
			else:
				break		
	info = Chat(user_id=user_id,cookie=cookie,user_content=user_content,ai_content=ai_content)
	db.session.add(info)
	db.session.commit()
	data = Chat.query.filter_by(user_id=user_id,cookie=cookie,user_content=user_content, ai_content=ai_content).order_by(Chat.id.desc()).first()
	
	return response.success({"id": data.id, "msg": ai_content})

@api.route('/chat/get_record', methods = ['POST'])
#@token_required
def get_record():
	user_id = request.json.get('user_id')
	cookie = request.json.get('token')
	get_res.init(user_id)
	chats = Chat.query.filter_by(user_id=user_id,cookie=cookie).all()
	data = []
	guide = "Hi, I am Bot.<br/>I am here to help you easly find projects.<br/><br/>Here are some guides:<br/>1. Project fields (AI, IOT)<br/>2. Project duration<br/>3. Project departments (Computer Science)<br/>4. Country (India, Taiwan)<br/><br/>If you need more guidelines, please type 'help'<br/>"

	for chat in chats:
		chat = chat.to_json()
		data.append({'id': chat['id'], 'ai_content': chat['ai_content'], 'user_content': chat['user_content']})
	
	return response.success({"guide": guide, "msg": data})
def get_country():
	return {
 "AL":"Albania",
 "AX":"Aland Islands",
 "DZ":"Algeria",
 "AS":"American Samoa",
 "AD":"Andorra",
 "AO":"Angola",
 "AI":"Anguilla",
 "AQ":"Antarctica",
 "AG":"Antigua and Barbuda",
 "AR":"Argentina",
 "AM":"Armenia",
 "AW":"Aruba",
 "AU":"Australia",
 "AT":"Austria",
 "AZ":"Azerbaijan",
 "BS":"Bahamas",
 "BH":"Bahrain",
 "BD":"Bangladesh",
 "BB":"Barbados",
 "BY":"Belarus",
 "BE":"Belgium",
 "BZ":"Belize",
 "BJ":"Benin",
 "BM":"Bermuda",
 "BT":"Bhutan",
 "BO":"Bolivia",
 "BQ":"Bonaire, Sint Eustatius and Saba",
 "BA":"Bosnia and Herzegovina",
 "BW":"Botswana",
 "BV":"Bouvet Island",
 "BR":"Brazil",
 "IO":"British Indian Ocean Territory",
 "BN":"Brunei Darussalam",
 "BG":"Bulgaria",
 "BF":"Burkina Faso",
 "BI":"Burundi",
 "CV":"Cabo Verde",
 "KH":"Cambodia",
 "CM":"Cameroon",
 "CA":"Canada",
 "KY":"Cayman Islands",
 "CF":"Central African Republic",
 "TD":"Chad",
 "CL":"Chile",
 "CN":"China",
 "CX":"Christmas Island",
 "CC":"Cocos Islands",
 "CO":"Colombia",
 "KM":"Comoros",
 "CD":"Congo",
 "CG":"Congo",
 "CK":"Cook Islands",
 "CR":"Costa Rica",
 "HR":"Croatia",
 "CU":"Cuba",
 "CW":"Curaçao",
 "CY":"Cyprus",
 "CZ":"Czechia",
 "CI":"Côte d'Ivoire",
 "DK":"Denmark",
 "DJ":"Djibouti",
 "DM":"Dominica",
 "DO":"Dominican Republic",
 "EC":"Ecuador",
 "EG":"Egypt",
 "SV":"El Salvador",
 "GQ":"Equatorial Guinea",
 "ER":"Eritrea",
 "EE":"Estonia",
 "SZ":"Eswatini",
 "ET":"Ethiopia",
 "FK":"Falkland Islands [Malvinas]",
 "FO":"Faroe Islands ",
 "FJ":"Fiji",
 "FI":"Finland",
 "FR":"France",
 "GF":"French Guiana",
 "PF":"French Polynesia",
 "TF":"French Southern Territories",
 "GA":"Gabon",
 "GM":"Gambia",
 "GE":"Georgia",
 "DE":"Germany",
 "GH":"Ghana",
 "GI":"Gibraltar",
 "GR":"Greece",
 "GL":"Greenland",
 "GD":"Grenada",
 "GP":"Guadeloupe",
 "GU":"Guam",
 "GT":"Guatemala",
 "GG":"Guernsey",
 "GN":"Guinea",
 "GW":"Guinea-Bissau",
 "GY":"Guyana",
 "HT":"Haiti",
 "HM":"Heard Island and McDonald Islands",
 "VA":"Holy See",
 "HN":"Honduras",
 "HK":"Hong Kong",
 "HU":"Hungary",
 "IS":"Iceland",
 "IN":"India",
 "ID":"Indonesia",
 "IR":"Iran",
 "IQ":"Iraq",
 "IE":"Ireland",
 "IM":"Isle of Man",
 "IL":"Israel",
 "IT":"Italy",
 "JM":"Jamaica",
 "JP":"Japan",
 "JE":"Jersey",
 "JO":"Jordan",
 "KZ":"Kazakhstan",
 "KE":"Kenya",
 "KI":"Kiribati",
 "KR":"Korea",
 "KW":"Kuwait",
 "KG":"Kyrgyzstan",
 "LA":"Lao People's Democratic Republic",
 "LV":"Latvia",
 "LB":"Lebanon",
 "LS":"Lesotho",
 "LR":"Liberia",
 "LY":"Libya",
 "LI":"Liechtenstein",
 "LT":"Lithuania",
 "LU":"Luxembourg",
 "MO":"Macao",
 "MG":"Madagascar",
 "MW":"Malawi",
 "MY":"Malaysia",
 "MV":"Maldives",
 "ML":"Mali",
 "MT":"Malta",
 "MH":"Marshall Islands",
 "MQ":"Martinique",
 "MR":"Mauritania",
 "MU":"Mauritius",
 "YT":"Mayotte",
 "MX":"Mexico",
 "FM":"Micronesia",
 "MD":"Moldova",
 "MC":"Monaco",
 "MN":"Mongolia",
 "ME":"Montenegro",
 "MS":"Montserrat",
 "MA":"Morocco",
 "MZ":"Mozambique",
 "MM":"Myanmar",
 "NA":"Namibia",
 "NR":"Nauru",
 "NP":"Nepal",
 "NL":"Netherlands",
 "NC":"New Caledonia",
 "NZ":"New Zealand",
 "NI":"Nicaragua",
 "NE":"Niger",
 "NG":"Nigeria",
 "NU":"Niue",
 "NF":"Norfolk Island",
 "MP":"Northern Mariana Islands",
 "NO":"Norway",
 "OM":"Oman",
 "PK":"Pakistan",
 "PW":"Palau",
 "PS":"Palestine, State of",
 "PA":"Panama",
 "PG":"Papua New Guinea",
 "PY":"Paraguay",
 "PE":"Peru",
 "PH":"Philippines",
 "PN":"Pitcairn",
 "PL":"Poland",
 "PT":"Portugal",
 "PR":"Puerto Rico",
 "QA":"Qatar",
 "MK":"Republic of North Macedonia",
 "RO":"Romania",
 "RU":"Russian Federation",
 "RW":"Rwanda",
 "RE":"Réunion",
 "BL":"Saint Barthélemy",
 "SH":"Saint Helena, Ascension and Tristan da Cunha",
 "KN":"Saint Kitts and Nevis",
 "LC":"Saint Lucia",
 "MF":"Saint Martin",
 "PM":"Saint Pierre and Miquelon",
 "VC":"Saint Vincent and the Grenadines",
 "WS":"Samoa",
 "SM":"San Marino",
 "ST":"Sao Tome and Principe",
 "SA":"Saudi Arabia",
 "SN":"Senegal",
 "RS":"Serbia",
 "SC":"Seychelles",
 "SL":"Sierra Leone",
 "SG":"Singapore",
 "SX":"Sint Maarten",
 "SK":"Slovakia",
 "SI":"Slovenia",
 "SB":"Solomon Islands",
 "SO":"Somalia",
 "ZA":"South Africa",
 "GS":"South Georgia and the South Sandwich Islands",
 "SS":"South Sudan",
 "ES":"Spain",
 "LK":"Sri Lanka",
 "SD":"Sudan",
 "SR":"Suriname",
 "SJ":"Svalbard and Jan Mayen",
 "SE":"Sweden",
 "CH":"Switzerland",
 "SY":"Syrian Arab Republic",
 "TW":"Taiwan",
 "TJ":"Tajikistan",
 "TZ":"Tanzania, United Republic of",
 "TH":"Thailand",
 "TL":"Timor-Leste",
 "TG":"Togo",
 "TK":"Tokelau",
 "TO":"Tonga",
 "TT":"Trinidad and Tobago",
 "TN":"Tunisia",
 "TR":"Turkey",
 "TM":"Turkmenistan",
 "TC":"Turks and Caicos Islands",
 "TV":"Tuvalu",
 "UG":"Uganda",
 "UA":"Ukraine",
 "AE":"United Arab Emirates",
 "GB":"United Kingdom of Great Britain and Northern Ireland",
 "UM":"United States Minor Outlying Islands",
 "US":"United States of America",
 "UY":"Uruguay",
 "UZ":"Uzbekistan",
 "VU":"Vanuatu",
 "VE":"Venezuela",
 "VN":"Viet Nam",
 "VG":"Virgin Islands",
 "WF":"Wallis and Futuna",
 "EH":"Western Sahara",
 "YE":"Yemen",
 "ZM":"Zambia",
 "ZW":"Zimbabwe"
}





















