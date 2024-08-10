# CnA: Crawler & Analyst

`KaiHuang · Crawler & Analyst`, 即开荒行动中所包含的名为``“GitHub项目的爬取与分析”``的子项目。

## 说明书 How to use？

#### 食用方法1：直接本地运行flask

1. 直接运行`myapp.py`
2. 运行后点击`http://127.0.0.1:5000/`
3. 填写信息后点击“submit”按钮，稍等即可得到仓库的内容

#### 食用方法2：加上Gunicorn + Nginx (还可以加上内网穿透，代理nginx的80端口即可，即127.0.0.1:80)

1. 安装Gunicorn：`pip install gunicorn`
2. 安装Nginx：`sudo apt-get install nginx`
3. 配置Nginx：`sudo vi /etc/nginx/sites-available/default`
4. 编辑Nginx配置文件，添加以下内容：

```
server {
    listen 80;
    server_name your_domain_name;   # 改成你自己的域名

    location / {
        proxy_pass http://127.0.0.1:8000;   # 改成你自己的端口号
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

5. 重启Nginx：`sudo systemctl restart nginx`
6. 运行`app.py`：`gunicorn -w 4 -b 127.0.0.1:8000 myapp:app`
7. 打开浏览器，输入`localhost:8000`，即可得到仓库的内容


## 其他的……
有关于```analyst```的功能正在开发中……（也可能直接放弃，变成一个插件hhh）

> 声明：
> 在此之前，本人在2024.5.4已经上传了一个私有仓库，核心是其readme文件，用于声明本仓库核心代码（```app.py```（私有仓库中叫crawler.py）等）的原创性。