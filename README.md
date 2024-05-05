# CnA: Crawler & Analyst
`KaiHuang · Crawler & Analyst`, 即开荒行动中所包含的名为“GitHub项目的爬取与分析”的项目。

## 说明书 How to use？
使用方法很简单：

1. 将这个``crawler.py``放进一个文本编辑器里，最好是``pycharm``；
2. 填写好自己的GitHub tokens（个人令牌）；
3. 然后运行这个程序；
4. 终端（Terminal）会提示你输入需要爬取和解析的（public）仓库（repo）的URL（链接），输入即可；
5. 稍等片刻，在爬取好内容之后，就会有红色进度条来展示写入项目结构树的进度；
6. 当终端显示```“OVER, .min.txt已刷新”```时，代表程序结束，随后会在同目录下生成一个叫``repo_tree_with_content.min.txt``的文件，即文件树的压缩文件（此文件可以直接给GPT进行分析）。

有关于```analyst```的功能正在开发中……

> 声明：
> 在此之前，本人在2024.5.4已经上传了一个私有仓库，核心是其readme文件，用于声明代码的原创性。
