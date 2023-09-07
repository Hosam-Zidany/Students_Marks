from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler,filters
import requests
from bs4 import BeautifulSoup
import locale
import re
from server import server
locale.setlocale(locale.LC_ALL, "")



Token = '6330027964:AAHyCL76G4_iCY5Wmyap6D0Hrr8jWsrS8DA'

async def start (ubdate: Update, context: ContextTypes.DEFAULT_TYPE):
	await context.bot.send_message(chat_id = ubdate.effective_chat.id, text = "ارسل الرقم الجامعي")

async def help (ubdate: Update, context: ContextTypes.DEFAULT_TYPE):
	await context.bot.send_message(chat_id = ubdate.effective_chat.id, text = "بوت غير رسمي للحصول على علامات كلية طب الأسنان في جامعة حماه")

async def the_mark (num):
	headers ={
	'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.203'
	}

	url = f"http://app.hama-univ.edu.sy/StdMark/Student/{num}?college=3"
	page = requests.get(url,headers=headers)
	src = page.content
	subjects = []
	marks = []
	new_marks = [] 
	result = []*len(marks)
	tmpp = ["0.00","1.00","2.00","3.00","4.00","5.00","6.00","7.00","8.00","9.00","10.00","11.00","12.00","13.00","14.00","15.00","16.00","17.00","18.00","19.00","20.00","21.00","22.00","23.00","24.00","25.00","26.00","27.00","28.00","29.00","30.00","31.00","32.00","33.00","34.00","35.00","36.00","37.00","38.00","39.00","40.00","41.00","42.00","43.00","44.00","45.00","46.00","47.00","48.00","49.00","50.00","51.00","52.00","53.00","54.00","55.00","56.00","57.00","58.00","59.00"]
	tmp = ["60.00","61.00","62.00","63.00","64.00","65.00","66.00","67.00","68.00","69.00","70.00","71.00","72.00","73.00","74.00","75.00","76.00","77.00","78.00","79.00","80.00","81.00","82.00","83.00","84.00","85.00","86.00","87.00","88.00","89.00","90.00","91.00","92.00","93.00","94.00","95.00","96.00","97.00","98.00","99.00","100.00","101.00","102.00","103.00","104.00","105.00","106.00","107.00","108.00","109.00","110.00","111.00","112.00","113.00","114.00","115.00","116.00","117.00","118.00","119.00"]
	soup = BeautifulSoup(src,"lxml")
	table_std=soup.find("table",{"class":"table-striped"})
	name = soup.find('span',{'class':'bottom'}).text
	for val in table_std.find_all('tbody'):
		rows=val.find_all('tr')
		for row in rows:
			tds = row.find_all('td')
			subject = row.find('td').text.strip()
			mark = tds[2].text.strip().replace(',','')
			rr="."
			cc=" :  "
			for i in range (len(subjects)):
				if  subject==subjects[i]:
					marks[i]=mark
					subject=""
					mark=""
					rr=""
					cc=""
			result.append(rr)
			marks.append(mark)
			subjects.append(subject)
			new_marks.append(cc)
			for i in range(len(marks)):
				for j in range(len(tmpp)):
					if marks[i]==tmp[j]:
						result[i]=("     \u2705")
					elif marks[i]==tmpp[j]:
						result[i]=("     \u274c")
				

		
	new_list = [x for pair in zip(subjects,new_marks, marks, result) for x in pair]
	new_list.insert(0,"الاسم :  ")
	new_list.insert(1,name)
	new_list.insert(2," ")
	new_list.insert(3,"\n")
	while "" in new_list:
		new_list.remove("")
		if "" in new_list:
			new_list.remove("")
	f_list = []
	for i in range(0,len(new_list),4):
	    f_list.extend(new_list[i:i+4])
	    f_list.append("\n\n")
	#f_list[-4]= ""
	#f_list[-2]=""
	return u''.join(f_list)

async def mark (ubdate: Update, context: ContextTypes.DEFAULT_TYPE):
	await context.bot.send_message(chat_id = ubdate.effective_chat.id, text = "جاري العمل.....")
	num = ubdate.message.text
	def arabic (num):
		pattern = re.compile(r'[٠-٩]')
		match = re.search(pattern, num)
		return match is not None
	if any(i.isalpha()for i in num) | arabic(num):
		await context.bot.send_message(chat_id = ubdate.effective_chat.id, text = "يجب أن يتكون الرقم من الأرقام 0-9 فقط")
	else:
		#await context.bot.send_message(chat_id = ubdate.effective_chat.id, text = "ubdate")
		mm = await the_mark(num)
		await context.bot.send_message(chat_id = ubdate.effective_chat.id, text = mm)
	



if __name__ == '__main__':

	application = ApplicationBuilder().token(Token).build()
	#handler
	start_handler = CommandHandler('start', start)
	help_handler = CommandHandler('help', help)
	message_handler = MessageHandler(filters.ALL, mark)


	#reg
	application.add_handler(start_handler)
	application.add_handler(help_handler)
	application.add_handler(message_handler)
	server()
	application.run_polling()

