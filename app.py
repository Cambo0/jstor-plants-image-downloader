#注释不会写，照葫芦画瓢写的
from flask import Flask, request, send_file
import os
import requests
import zipfile
import random
import string
from datetime import datetime
from qiniu import Auth, put_file

app = Flask(__name__)

# 存储下载图片的文件夹路径
UPLOAD_FOLDER = '/path/to/your/upload/folder'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# 七牛云对象存储配置（以下配置可按需开启）
access_key = 'your_access_key'
secret_key = 'your_secret_key'
bucket_name = 'your_bucket_name'

q = Auth(access_key, secret_key)

# 腾讯云 COS 配置
secret_id = 'YOUR_SECRET_ID'  # 替换为你的 SecretId
secret_key = 'YOUR_SECRET_KEY'  # 替换为你的 SecretKey
region = 'YOUR_REGION'  # 替换为你的存储桶所在的区域
bucket = 'YOUR_BUCKET_NAME'  # 替换为你的存储桶名称
cos_config = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key)
cos_client = CosS3Client(cos_config)

# 阿里云 OSS 配置
aliyun_access_key_id = 'YOUR_ALIYUN_ACCESS_KEY_ID'
aliyun_access_key_secret = 'YOUR_ALIYUN_ACCESS_KEY_SECRET'
aliyun_endpoint = 'YOUR_ALIYUN_ENDPOINT'
aliyun_bucket = 'YOUR_ALIYUN_BUCKET_NAME'
# 创建 Bucket 实例
auth = oss2.Auth(access_key_id, access_key_secret)
bucket = oss2.Bucket(auth, endpoint, bucket_name)

# 前端html，可将 <html>到</html>的内容分离成单文件，如下

#@app.route('/')
#def index():
    #return render_template('index.html')

@app.route('/')
def index():
    return '''
    <html lang="zh-CN">
    <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>图片下载页面</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f4f4f4;
            margin: 0;
            padding: 0;
        }
        .container {
            max-width: 600px;
            margin: 50px auto;
            background-color: #fff;
            padding: 20px;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
            border-radius: 8px;
        }
        h2 {
            color: #333;
            text-align: center;
        }
        label {
            display: block;
            margin: 15px 0 5px;
            color: #555;
        }
        input[type="text"] {
            width: 100%;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 5px;
            box-sizing: border-box;
        }
        input[type="submit"] {
            background-color: #4CAF50;
            color: white;
            padding: 10px 15px;
            margin-top: 20px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            width: 100%;
        }
        input[type="submit"]:hover {
            background-color: #45a049;
        }
        .message {
            margin-top: 20px;
            color: #555;
            text-align: center;
        }
    </style>
</head>
<body>
    <div class="container">
        <h2>图片下载页面</h2>
        <form action="/download" method="post">
            <label for="ids">请输入要下载的图片ID（多个ID用逗号分隔）：</label>
            <input type="text" id="ids" name="ids" placeholder="例如：k000884264,k000884265">
            <input type="submit" value="下载图片">
        </form>
        <div class="message">
            <p>输入多个 ID 并用逗号分隔。</p>
        </div>
    </div>
</body>
</html>
    '''

# 生成随机zip文件名
def generate_filename():
    random_part = ''.join(random.choices(string.ascii_letters + string.digits, k=4))
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    return f"{random_part}-{timestamp}.zip"

# 构建下载请求
@app.route('/download', methods=['POST'])
def download():
    ids = request.form['ids']
    id_list = ids.split(',')

    # 创建一个临时文件夹来存放下载的图片
    temp_folder = '/tmp/downloaded_images'
    if not os.path.exists(temp_folder):
        os.makedirs(temp_folder, exist_ok=True)

    zip_filename = os.path.join(app.config['UPLOAD_FOLDER'], generate_filename())
    with zipfile.ZipFile(zip_filename, 'w') as zipf:
        for id_var in id_list:
            # 构造下载图片的URL
            url = f'https://plants.jstor.org/seqapp/adore-djatoka/resolver?url_ver=Z39.88-2004&rft_id={id_var.lower()}.jp2&svc_id=info:lanl-repo/svc/getRegion&svc_val_fmt=info:ofi/fmt:kev:mtx:jpeg2000&svc.level=7'

            # 下载图片并保存到临时文件夹
            r = requests.get(url)
            if r.status_code == 200:
                image_filename = os.path.join(temp_folder, f'{id_var.lower()}.jpg')
                with open(image_filename, 'wb') as f:
                    f.write(r.content)
                
                # 将下载的图片添加到 zip 文件中
                zipf.write(image_filename, os.path.basename(image_filename))
                
                # 上传图片到七牛云
                key = f"img/{id_var.lower()}.jpg"
                token = q.upload_token(bucket_name, key, 3600)
                put_file(token, key, image_filename)
                
                # 上传到腾讯云 COS
                cos_client.upload_file(
                    Bucket=bucket,
                    LocalFilePath=image_filename,
                    Key=f"images/{os.path.basename(image_filename)}"
                )
               
                # 上传图片到阿里云 OSS
                oss_key = f"backup/{id_var.lower()}.jpg"
                bucket.put_object_from_file(oss_key, image_filename)
                
                #其他云


    # 删除临时文件夹
    for file in os.listdir(temp_folder):
        file_path = os.path.join(temp_folder, file)
        os.remove(file_path)
    os.rmdir(temp_folder)

    # 返回生成的 zip 文件给用户下载
    return send_file(zip_filename, as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)  #开发环境可加上 ,debug=True

