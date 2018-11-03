# ！/usr/bin/env python
# -*- coding:utf-8 -*-
from scrapy.selector import Selector
from scrapy.http import HtmlResponse

text = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
    <h1>Hello World</h1>
    <h1>Hello Scrapy</h1>
    <h1>Hello Python</h1>
    <ul>
        <li>C++学习手册 <b>价格:99.00元</b></li>
        <li>Java核心编程 <b>价格:88.00元</b></li>
        <li>Python基础教程 <b>价格:80.00元</b></li>
    </ul>
    <div id="images">
        <a href="image1.html">Name:Image 1 <br/> <img src="image1.jpg"></a>
        <a href="image2.html">Name:Image 2 <br/> <img src="image2.jpg"></a>
        <a href="image3.html">Name:Image 3 <br/> <img src="image3.jpg"></a>
        <a href="image4.html">Name:Image 4 <br/> <img src="image4.jpg"></a>
    </div>
</body>
</html>
"""

selector = Selector(text=text)  # 注入要解析的HTML代码，然后断电调试注入
pass