FROM python:3.7

# 服务将要使用的端口
EXPOSE 42843

# 工作目录
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

# 安装依赖
COPY requirements.txt /usr/src/app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENTRYPOINT ["python3", "server.py"]