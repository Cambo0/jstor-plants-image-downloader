# jstor-plants-image-downloader

# JSTOR植物图片下载和多云备份

利用Flask应用程序允许用户通过提供 ID 快速简便地下载 plants.jstor.org 网站上的图片，并自动将下载的图片上传到多种对象存储产品（如腾讯云、阿里云、七牛云）进行备份。下载的图片也会压缩成带有唯一文件名格式的 ZIP 文件存储到本地或在前端供用户下载。

## 功能

- 使用用户提供的 ID 批量下载图片。
- 将下载的图片存储到本地。
- 自动将下载的图片上传到多个对象存储（腾讯云、阿里云、七牛云）进行备份。
- 将下载的图片压缩成带有唯一文件名格式的 ZIP 文件（例如，`abcd-20240701-123456.zip`）。

## 安装环境

- Python 3.6+
- Flask
- 腾讯云 COS SDK for Python
- 阿里云 OSS SDK for Python
- 七牛云 SDK for Python
- Requests
- Zipfile

## 安装

1. 克隆代码库：

    ```bash
    git clone https://github.com/your-repo/flask-image-downloader.git
    cd flask-image-downloader
    ```

2. 创建虚拟环境并激活：

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. 安装所需的依赖：

    ```bash
    pip install -r requirements.txt
    ```

4. 安装云存储 SDK：

    ```bash
    pip install cos-python-sdk-v5  # 腾讯云
    pip install aliyun-python-sdk-oss  # 阿里云
    pip install qiniu  # 七牛云
    ```

## 配置

1. 在 `app.py` 中用你的对象存储凭证和存储桶信息替换占位符：

    ```python
    # 腾讯云 COS 配置
    tencent_secret_id = 'YOUR_TENCENT_SECRET_ID'
    tencent_secret_key = 'YOUR_TENCENT_SECRET_KEY'
    tencent_region = 'YOUR_TENCENT_REGION'
    tencent_bucket = 'YOUR_TENCENT_BUCKET_NAME'

    # 阿里云 OSS 配置
    aliyun_access_key_id = 'YOUR_ALIYUN_ACCESS_KEY_ID'
    aliyun_access_key_secret = 'YOUR_ALIYUN_ACCESS_KEY_SECRET'
    aliyun_endpoint = 'YOUR_ALIYUN_ENDPOINT'
    aliyun_bucket = 'YOUR_ALIYUN_BUCKET_NAME'

    # 七牛云 配置
    qiniu_access_key = 'YOUR_QINIU_ACCESS_KEY'
    qiniu_secret_key = 'YOUR_QINIU_SECRET_KEY'
    qiniu_bucket = 'YOUR_QINIU_BUCKET_NAME'
    ```

2. 设置 `UPLOAD_FOLDER` 变量为存储下载图片的本地目录：

    ```python
    UPLOAD_FOLDER = '/path/to/your/upload/folder'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    ```

## 运行应用程序

1. 启动 Flask 应用程序：

    ```bash
    python app.py
    ```

2. 打开你的浏览器并导航到 `http://127.0.0.1:5000`。

## 使用方法

1. 在提供的输入框中输入要下载的图片 ID，用逗号分隔多个 ID。
2. 点击“下载图片”按钮下载图片。
3. 下载的图片将显示在网页上，并压缩成带有唯一文件名的 ZIP 文件。该 ZIP 文件将提供下载。
4. 图片还将自动上传到多个对象存储进行备份。

## 可选步骤：配置 Nginx 以支持 HTTPS

1. 安装 Nginx：

    ```bash
    sudo yum install nginx
    ```

2. 安装 Certbot 以获取 SSL 证书：

    ```bash
    sudo yum install epel-release
    sudo yum install certbot python-certbot-nginx
    ```

3. 使用 Certbot 获取 SSL 证书：

    ```bash
    sudo certbot --nginx -d your_domain.com
    ```

4. 通过创建或修改 `/etc/nginx/conf.d/flask_app.conf` 文件来配置 Nginx 以支持 HTTPS：

    ```nginx
    server {
        listen 80;
        server_name your_domain.com;
        return 301 https://$host$request_uri;
    }

    server {
        listen 443 ssl;
        server_name your_domain.com;

        ssl_certificate /etc/letsencrypt/live/your_domain.com/fullchain.pem;
        ssl_certificate_key /etc/letsencrypt/live/your_domain.com/privkey.pem;

        ssl_protocols TLSv1.2 TLSv1.3;
        ssl_ciphers 'ECDHE-RSA-AES128-GCM-SHA256:ECDHE-RSA-AES256-GCM-SHA384';

        location / {
            proxy_pass http://127.0.0.1:5000;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;

            client_max_body_size 10m;
            client_body_buffer_size 128k;
        }
    }
    ```

5. 检查并重新加载 Nginx：

    ```bash
    sudo nginx -t
    sudo systemctl reload nginx
    ```

## License

此项目基于 MIT 许可证。详细信息请参阅 [LICENSE](LICENSE) 文件。

## 致谢

- [Global Plants on JSTOR](https://plants.jstor.org/)
- [Flask](https://flask.palletsprojects.com/)
- [腾讯云 COS SDK for Python](https://cloud.tencent.com/document/product/436/12266)
- [阿里云 OSS SDK for Python](https://www.alibabacloud.com/help/doc-detail/32097.htm)
- [七牛云 SDK for Python](https://developer.qiniu.com/kodo/sdk/1242/python)
- [Requests](https://docs.python-requests.org/en/latest/)
