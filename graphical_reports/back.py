#!/usr/bin/env python
#encoding:utf8


from qiniu import Auth, put_file, etag, urlsafe_base64_encode
import datetime
import qiniu.config,os


#需要填写你的 Access Key 和 Secret Key
access_key = 'ezodf71HW35_51My2JFQGlamBgJ-uz9ngyTk83Pd'
secret_key = 'mR6zuDF92YuK0BJRXyezk4n6VLveaH9xEQbr0yAV'
today = datetime.datetime.now().strftime("%Y-%m-%d")
clean_exec = '''rm -rf /root/app/leanote/db_backup/'''
dump_exec = '''mongodump -h 127.0.0.1 -d leanote -o /root/app/leanote/db_backup/'''
tar_exec = '''tar -cvf leanoteback.tar leanote/'''
note_exec = '''curl http://sc.ftqq.com/SCU2576T92d53a9a490494c01c81d626cd8ba8b857eb67a12ecb8.send?text=服务器备份''' + today + '''成功！！'''
sce = '''<Response [200]>'''

print(os.popen(clean_exec))
print(os.popen(dump_exec))
print(os.popen(tar_exec))





#构建鉴权对象
q = Auth(access_key, secret_key)

#要上传的空间
bucket_name = 'yahui1105'

#上传到七牛后保存的文件名
key = 'leanote_' + today + '.tar'

#生成上传 Token，可以指定过期时间等
token = q.upload_token(bucket_name, key, 3600)

#要上传文件的本地路径
localfile = '/root/app/leanoteback.tar'

ret, info = put_file(token, key, localfile)
print(info)
if info.status_code == 200:
    os.popen(note_exec)
assert ret['key'] == key
assert ret['hash'] == etag(localfile)
