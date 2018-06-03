#!/usr/bin/python
# -*- coding:utf-8 -*-
'''
一、读取源程序，识别词素，过滤程序中的注释和空白
二、将生成的错误信息与源程序的位置联系，记录换行符的个数，给每个出错消息付一个行号

'''
import sys
import os

class compile():
	def __init__(self):
		self.keywords = ["auto","break","case","char","const","continue","default",  
	  
	"do","double","else","enum","extern","float","for",  
	  
	"goto","if","int","long","register","return","short",  
	  
	"signed","static","sizeof","struct","switch","typedef","union",  
	  
	"unsigned","void","volatile","while"]
	

	def lexer(self,file_name):
		file_name = file_name
		print file_name
		f_read = open(file_name,'r')
		symbol = []
		annotate = []
		error = []
		lineNumber = 0
		#记录状态state
		state = 0
		for line in f_read.readlines():
			line = line.strip('\n')
			lineNumber += 1#行号
			length = len(line)
			#print line
			i = 0
			string = ''#存储字符
			while i < length:
				x = line[i]
				#print x,state
				i += 1
				if state == 0:
					string = x
					if x == ' ':
						#state = 38
						continue
					elif x == '/':
						state = 1
						starti = i-1
					elif x.isalpha() or x == '_':#关键字或标识符
						state = 2 
					elif x == '=':#判断等号
						state = 4
					elif x.isdigit():
						state = 5
						
					#************************************
					elif x == '(':
						state = 7
						i -= 1
					elif x == ')':
						state = 8
						i -= 1
					elif x == '[':
						state = 9
					elif x == ']':
						state = 10
					elif x == '{':
						state = 11
						i -= 1
					elif x == '}':
						state = 12
						i -= 1
					elif x == ';':
						state = 13
					#elif x == '.':
						#state = 14
					elif x == ':':
						state = 15
					elif x == '\'':
						state = 16
					elif x == '\"':
						state = 17
					elif x == '%':
						state = 18
					elif x == '&':
						state = 19
					elif x == ',':
						state = 20
					elif x == '*':
						state = 21
					elif x == '-':
						state = 22
					elif x == '!':
						state = 23
					elif x == '+':
						state = 24
					else:
						state = 100
						i -= 1
				#elif state == 38:
					#state = 0
				elif state == 1:#判断注释
					if x == '/':#----------------//
						content = u'(符号,'+string+x+')'
						print content
						symbol.append(content)
						content = u'(注释,'+line[i:]+')'
						print content
						annotate.append(content)
						string = ''#回到初始态
						i = length
					elif x == '*':#--------------/*
						content = u'(符号,'+string+')'
						#print content
						state = 99
						string = ''
						i -= 1
					else:#----------------------/...
						content = u'(符号,'+string+')'
						print content
						symbol.append(content)
						state = 0
						string = ''
						i-= 1
				elif state == 99:#--------------/*...*
					if x == '*':
						content = u'(符号,'+x+')'
						#print content
						state = 98
						i -= 1
					else:
						pass
				elif state == 98:#-------------/*...*/
					if x == '/':
						endi = i
						content = line[starti:endi]#注释里的内容
						print u'(注释,'+content+')'
						#i -= 1
						state = 0
					elif x == '*':#----------------/*...**
						pass
					else :#-----------------------/*...*...
						state = 99
				elif state == 2:#判断关键字或标识符
					#在while中判断接下来的字符，若不是字母数字或者_则退出
					while x.isalpha() or x.isdigit() or x == '_':
						string += x
						#遍历后面的字符，对得到的x判断
						if i < length:
							x = line[i]
							i += 1
						else:
							break
					state = 3
					#在while中只有x=line[i]为空格时不满足条件，此时i的指针指向空格符，再加一，所以要减2才能指到
					#空格的前一个字符，即string的最后一个处
					i -= 2
				elif state == 3:
					if string in self.keywords:
						content = u'(关键字,'+string+')'
						print content
					else:
						content = u'(标识符,'+string+')'
						print content
					symbol.append(content)
					string = ''
					state = 0
				elif state == 4:# == 或 =
					if x == '=':
						string += x
						content = u'(符号,'+string+')'
						print content
						symbol.append(content)
					else:
						content = u'(符号,'+string+')'
						print content
						symbol.append(content)
					#检测完=后回退一位
					i-= 1
					string = ''
					state = 0
				elif state == 5:#数字
					if x.isalpha():
						while x.isalpha():
							string += x
							if i < length:
								x = line[i]
								i += 1
							else:
								break
						state = 77
						i -= 2
					elif x.isdigit() or x == '.':
						while x.isdigit() or x == '.':
							string += x
							if i < length:
								x = line[i]
								i += 1
							else:
								break
						state = 6
						i -= 2
					else:
						state = 0

				elif state == 6:
					content = u'(number,'+string+')'
					print content
					string = ''
					state = 0
				elif state == 7:
					content = u'(符号,()'
					symbol.append(content)
					print content
					string = ''
					state = 0
				elif state == 8:
					content = u'(符号,))'
					symbol.append(content)
					print content
					string = ''
					state = 0
				elif state == 11:
					content = u'(符号,{)'
					symbol.append(content)
					print content
					string = ''
					state = 0
				elif state == 12:
					content = u'(符号,})'
					symbol.append(content)
					print content
					string = ''
					state = 0
				elif state == 13:
					content = u'(符号,;)'
					symbol.append(content)
					print content
					string = ''
					state = 0
				elif state == 15:
					content = u'(符号,:)'
					symbol.append(content)
					print content
					string = ''
					state = 0
				elif state == 16:
					content = u'(符号,\')'
					symbol.append(content)
					print content
					string = ''
					state = 0
					i -= 1
				elif state == 17:
					content = u'(符号,\")'
					symbol.append(content)
					print content
					string = ''
					state = 0
					i -= 1
				elif state == 18:
					content = u'(符号,%)'
					symbol.append(content)
					print content
					string = ''
					state = 0
					i -= 1
				elif state == 19:
					content = u'(符号,&)'
					symbol.append(content)
					print content
					string = ''
					state = 0
					i -= 1
				elif state == 20:
					content = u'(符号,,)'
					symbol.append(content)
					print content
					string = ''
					state = 0
					i -= 1
				elif state == 21:
					content = u'(符号,*)'
					symbol.append(content)
					print content
					string = ''
					state = 0
					i -= 1
				elif state == 22:
					if x == '-':#---------- --
						state = 28  
						i -= 1  
					elif x == '=':#----------- -= 
						state = 29  
						i -= 1  
					else:#------------- -
						state = 30  
						i -= 2
				elif state == 23:
					content = u'(符号,!)'
					symbol.append(content)
					print content
					string = ''
					state = 0
					i -= 1
				elif state == 24:
					if x == '+':#----------++
						state = 25  
						i -= 1  
					elif x == '=':#-----------+= 
						state = 26  
						i -= 1  
					else:#------------- +
						state = 27  
						i -= 2
				elif state == 25:#判断++  
					content = u'(符号,' + string + x + ')'  
					symbol.append(content)  
					print content  
					string = ''  
					state = 0  
				elif state == 26:#判断+=  
					content = u'(符号,' + string + x + ')'  
					symbol.append(content)  
					print content   
					string = '' 
					state = 0 
				elif state == 27:#判断+  
					content = u'(符号,' + x + ')'  
					symbol.append(content)  
					print content  
					string = ''
					state = 0  
				
				elif state == 28:#判断-- 
					content = u'(符号,' + string + x + ')'  
					symbol.append(content) 
					print content  
					string = ''  
					state = 0 
				elif state == 29:#判断-=  
					content = u'(符号,' + string + x + ')'  
					symbol.append(content)  
					print content   
					string = '' 
					state = 0 
				elif state == 30:#判断-  
					content = u'(符号,' + x + ')'  
					symbol.append(content)  
					print content  
					string = '' 
					state = 0  
					
				elif state == 77:#检测数字开头的错误字符串
					content = u'(Error,行号,'+str(lineNumber)+':'+string+')'
					symbol.append(content)
					print content
					string = ''
					state = 0
				
				elif state == 100:#检测错误加上行号
					content = u'(Error,行号,'+str(lineNumber)+':'+x+')'
					symbol.append(content)
					print content
					string = ''
					state = 0
				
	def main(self):
		
		if len(sys.argv) < 2:  #len(sys.argv) = 1时表示只有lexer.py，sys.argv表示脚本所有参数
			print 'Please Input FileName'
		else :
			self.lexer(sys.argv[1])
	
if __name__ == '__main__':
	c = compile()
	c.main()
