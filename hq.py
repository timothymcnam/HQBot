from getpass import getpass

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import sys

import threading

from PIL import ImageGrab
import win32gui

import pytesseract

import re

resList = [0,0,0]
resListF = [0,0,0]
qa_text = ["", "", "", ""]
question_glob = ""

def load_n_scrub(driver, search_text, i):
	search = driver.find_element_by_id("sb_form_q")
	search.clear()
	search.send_keys(search_text)
	driver.find_element_by_id("sb_form_go").click()

	countFull = driver.find_element_by_class_name("sb_count")
	countTemp = ''
	for j in range(0, len(countFull.text)):
		if countFull.text[j].isnumeric():
			countTemp = countTemp + countFull.text[j]
	resList[i] = int(countTemp)

def print_answer(driver, search_text):
	search = driver.find_element_by_id("sb_form_q")
	search.clear()
	search.send_keys(search_text)
	driver.find_element_by_id("sb_form_go").click()

	# first_p = driver.find_element_by_css_selector("p").text
	# print(first_p + "\n")

	html_source = driver.page_source
	html_source = html_source.lower()

	regex = qa_text[1].lower()
	resListF[0] = len(re.findall(regex, html_source))

	regex = qa_text[2].lower()
	resListF[1] = len(re.findall(regex, html_source))

	regex = qa_text[3].lower()
	resListF[2] = len(re.findall(regex, html_source))

	if "NOT" in question_glob:
		for i in range(0, len(resListF)):
			resListF[i] = resListF[i] * -1.0

	print("First Page:")

	if(resListF[0] >= resListF[1] and resListF[0] >= resListF[2]):
		print("1. Choice 1 - " + str(resListF[0]))
	elif(resList[1] >= resList[0] and resListF[1] >= resListF[2]):
		print("1. Choice 2 - " + str(resListF[1]))
	elif(resListF[2] >= resListF[0] and resListF[2] >= resListF[1]):
		print("1. Choice 3 - " + str(resListF[2]))

	if((resListF[0] > resListF[1] and resListF[0] < resListF[2]) or (resListF[0] < resListF[1] and resListF[0] > resListF[2])):
		print("2. Choice 1 - " + str(resListF[0]))
	elif((resListF[1] > resListF[0] and resListF[1] < resListF[2]) or (resListF[1] < resListF[0] and resListF[1] > resListF[2])):
		print("2. Choice 2 - " + str(resListF[1]))
	elif((resListF[2] > resListF[0] and resListF[2] < resListF[1]) or (resListF[2] < resListF[0] and resListF[2] > resListF[1])):
		print("2. Choice 3 - " + str(resListF[2]))

	if(resListF[0] < resListF[1] and resListF[0] < resListF[2]):
		print("3. Choice 1 - " + str(resListF[0]))
	elif(resList[1] < resList[0] and resListF[1] < resListF[2]):
		print("3. Choice 2 - " + str(resListF[1]))
	elif(resListF[2] < resListF[0] and resListF[2] < resListF[1]):
		print("3. Choice 3 - " + str(resListF[2]))

	print("")

def get_answer(driverList, searches):
	resList[0] = 0
	resList[1] = 0
	resList[2] = 0

	# for i in range(0, 4):
	# 	load_n_scrub(driverList[i], searches[i], i)
	t0 = threading.Thread(target=load_n_scrub, args=(driverList[0],searches[0],0,))
	t1 = threading.Thread(target=load_n_scrub, args=(driverList[1],searches[1],1,))
	t2 = threading.Thread(target=load_n_scrub, args=(driverList[2],searches[2],2,))
	t3 = threading.Thread(target=print_answer, args=(driverList[3],question_glob,))

	t0.start()
	t1.start()
	t2.start()
	t3.start()

	t0.join()
	t1.join()
	t2.join()
	t3.join()


	if "NOT" in question_glob:
		for i in range(0, len(resList)):
			resList[i] = resList[i] * -1.0

	print("Q&A:")
	if(resList[0] >= resList[1] and resList[0] >= resList[2]):
		print("1. Choice 1 - " + str(resList[0]))
	elif(resList[1] >= resList[0] and resList[1] >= resList[2]):
		print("1. Choice 2 - " + str(resList[1]))
	elif(resList[2] >= resList[0] and resList[2] >= resList[1]):
		print("1. Choice 3 - " + str(resList[2]))

	if((resList[0] > resList[1] and resList[0] < resList[2]) or (resList[0] < resList[1] and resList[0] > resList[2])):
		print("2. Choice 1 - " + str(resList[0]))
	elif((resList[1] > resList[0] and resList[1] < resList[2]) or (resList[1] < resList[0] and resList[1] > resList[2])):
		print("2. Choice 2 - " + str(resList[1]))
	elif((resList[2] > resList[0] and resList[2] < resList[1]) or (resList[2] < resList[0] and resList[2] > resList[1])):
		print("2. Choice 3 - " + str(resList[2]))

	if(resList[0] < resList[1] and resList[0] < resList[2]):
		print("3. Choice 1 - " + str(resList[0]))
	elif(resList[1] < resList[0] and resList[1] < resList[2]):
		print("3. Choice 2 - " + str(resList[1]))
	elif(resList[2] < resList[0] and resList[2] < resList[1]):
		print("3. Choice 3 - " + str(resList[2]))

def img_and_text(box, i):
	img_temp = ImageGrab.grab(box)
	img_text = pytesseract.image_to_string(img_temp)
	qa_text[i] = img_text

def get_img_text():

	w_start = 1410
	w_end = 1890

	# bbox = (w_start, h_start, w_end, h_end)
	question_box = (w_start, 150, w_end, 290)
	ans1_box = (w_start, 295, w_end, 334)
	ans2_box = (w_start, 351, w_end, 390)
	ans3_box = (w_start, 407, w_end, 446)

	t0 = threading.Thread(target=img_and_text, args=(question_box,0,))
	t1 = threading.Thread(target=img_and_text, args=(ans1_box,1,))
	t2 = threading.Thread(target=img_and_text, args=(ans2_box,2,))
	t3 = threading.Thread(target=img_and_text, args=(ans3_box,3,))

	t0.start()
	t1.start()
	t2.start()
	t3.start()

	t0.join()
	t1.join()
	t2.join()
	t3.join()
	
if __name__ == '__main__':
	driver1 = webdriver.Firefox()
	driver2 = webdriver.Firefox()
	driver3 = webdriver.Firefox()
	driver4 = webdriver.Firefox()

	driverList = [driver1, driver2, driver3, driver4]

	for d in driverList:
		d.implicitly_wait(3)

	for d in driverList:
		d.get("https://www.bing.com")
		search = d.find_element_by_id("sb_form_q")
		search.clear()
		search.send_keys("test")
		d.find_element_by_id("sb_form_go").click()


	toplist, winlist = [], []
	def enum_cb(hwnd, results):
	    winlist.append((hwnd, win32gui.GetWindowText(hwnd)))
	win32gui.EnumWindows(enum_cb, toplist)

	b_stacks = [(hwnd, title) for hwnd, title in winlist if 'bluestacks' in title.lower()]
	# just grab the hwnd for first window matching firefox
	b_stacks = b_stacks[0]
	hwnd = b_stacks[0]

	print("Ready To Run")

	while(True):
		#Wait for some sort of use input
		print("")
		input("Press Enter When Ready...")
		print("")

		#Get Image of Game
		win32gui.SetForegroundWindow(hwnd)

		get_img_text()

		question = qa_text[0]
		question_glob = question
		answer1 = qa_text[1]
		answer2 = qa_text[2]
		answer3 = qa_text[3]

		searches = [question + " \"" + answer1 + "\"", question + " \"" + answer2 + "\"", question + " \"" + answer3 + "\""]

		get_answer(driverList, searches)