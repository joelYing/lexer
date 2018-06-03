# lexer
A simple lexical analyzer implemented by Python  
简单操作：  
    安装python2.7  
    用notepad++打开py文件，注意测试文件与py文件应在同一目录下  
    在命令提示符窗口输入路径，运行：python lexer.py lexer-test.txt  

实现功能：  
    通过读入外部文件的c代码，逐行对代码进行词法分析，每读入一个字符对其进行判断，跳转到不同的状态  
    能实现整数与小数的区别匹配  
    新添加state77通过区别number后一位是字母还是数字或“.”来进行例如1int、7floatb的报错（未添加至下图中，在此以文字说明）  
    能够区分标识符与c语言关键字  
