import smtplib
from email.mime.text import MIMEText


class QqEmail:
    def __init__(self, email_user='1060407136@qq.com', email_pwd='ulputtbcdwqabcbd',mail_host='smtp.qq.com', port=25):
        self.username = email_user   # 发送者账号 '1060407136@qq.com'
        self.password = email_pwd  # 发送者密码 'ekrpleslkrbrbdge'
        self.title = '欢迎加入HHHMusic，点击下面链接完成注册'

        self.mail_host = mail_host
        self.port = port
    def send(self,recv,content):
        '''
        发送邮件函数，默认使用qqsmtp
        :param username: 邮箱账号 xx@qq.com
        :param passwd: 邮箱密码
        :param recv: 邮箱接收人地址，多个账号以逗号隔开
        :param title: 邮件标题
        :param content: 邮件内容
        :param mail_host: 邮箱服务器
        :param port: 端口号
        :return:
        '''
        msg = MIMEText(*content)  # 邮件内容
        msg['Subject'] = self.title  # 邮件主题
        msg['From'] = self.username  # 发送者账号
        msg['To'] = recv  # 接收者账号列表
        smtp = smtplib.SMTP(self.mail_host, port=self.port)  # 连接邮箱，传入邮箱地址，和端口号，smtp的端口号是25
        smtp.login(self.username, self.password)  # 发送者的邮箱账号，密码
        smtp.sendmail(self.username, recv, msg.as_string())
        # 参数分别是发送者，接收者，第三个是把上面的发送邮件的内容变成字符串
        smtp.quit()  # 发送完毕后退出smtp

