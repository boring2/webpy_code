#coding=utf-8
'''
Created on 2014年11月27日-12月3日-12月4日
Version 2.2
@author: boring2
增加修改用户上传图片名字的功能
增加预览功能

Created on 2014年12月09日
Version 2.3
@author: boring2
增加同步五个服务器功能

Created on 2014年12月17日
Version 3.0
@author: boring2
修改同步五个服务器功能---先同步到服务器缓存,点同步按键再同步

'''
import web
import os
import glob
import sys
import traceback
import mysshutils
import freemethod
import datetime
import json
import codecs

abspath = os.path.dirname(__file__)
sys.path.append(abspath)
os.chdir(abspath)
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8' 
user = "dhmiepgv2"
pw = "dhmiepgv2"
dbname = "10.4.72.87/RAC"
dbtype = "oracle"
resource_dict={}
relfile = ""
server_ip = ['10.4.72.210']
server_ip1 = ['10.4.72.210']
dpdb="/home/iepg/iepg-jetty/webapps/iepg/iPG/T-nsp_N9101/dpdb/"
dpdbimages = "/home/iepg/iepg-jetty/webapps/iepg/iPG/T-nsp_N9101/images/"
vodDetail = "/home/iepg/iepg-jetty/webapps/iepg/iPG/T-nsp_N9101/vodDetail/"
vodDetailimages = "/home/iepg/iepg-jetty/webapps/iepg/iPG/T-nsp_N9101/vodDetail/images/"
haibaoimages= '/usr/local/jboss-4.2.3.GA/server/default/deploy/zttg.war/'
usernamelist = ['admin','shichang',"boring2","chenhuacan"]

urls = (
        '/','login',
        '/uploadbg','uploadbg',
        '/search','search',
        "/testsearch","testsearch",
        "/tijiao","tijiao",
        "/pmidtihuan","pmidtihuan",
        "/uploadxiaotu","uploadxiaotu",
        "/uploadhaibao","uploadhaibao",
        '/tongbufuwuqi','tongbufuwuqi',
        '/tongbufuwuqi1','tongbufuwuqi1'
        )
render = web.template.render('templates/', cache=False)
app = web.application(urls,globals(),autoreload=True)
class pmidtihuan:
    def POST(self):
        web.header('pragma', 'no-cache')
        web.header('cache-control', 'no-cache,must-revalidate')
        web.header('expires', '0')
        web.header('content-type','text/json')
#         pmid1,pmid2,pmid3,pmid4,pmid5,pmid6 = web.input().pmid1,web.input().pmid2,\
#                                 web.input().pmid3,web.input().pmid4,\
#                                 web.input().pmid5,web.input().pmid6
        pmid = web.input()
        temppath = "static/temp/nofree/"
        content = []
        pmidlist=[]
        videonamelist=[]
        if "pmid1" in pmid:
            pmidlist.append(pmid.pmid1)
        if "pmid2" in pmid:
            pmidlist.append(pmid.pmid2)
        if "pmid3" in pmid:
            pmidlist.append(pmid.pmid3)
        if "pmid4" in pmid:
            pmidlist.append(pmid.pmid4)
        if "pmid5" in pmid:
            pmidlist.append(pmid.pmid5)
        if "pmid6" in pmid:
            pmidlist.append(pmid.pmid6)
#         print pmidlist
        global relfile
#         print "relfile   "+relfile
        try:
            if relfile:
                with open(relfile) as f:
                    for eline in f:
                        if '"pmId"' in eline:
                            string,numid = eline.strip().split(':')
                            eline = eline.replace(numid,pmidlist.pop(0))
                            content.append(eline)
                        else:
                            content.append(eline)
                with open(relfile,'w') as f:
                    f.writelines(content)
                    f.close()
                basename = temppath+os.path.basename(relfile)
                print basename
                fi = open(basename,'w')
                fi.writelines(content)
                fi.close()
#                 同步服务器
#                 for eip in server_ip:
#                     ssh = mysshutils.Myssh(eip)
#                     ssh.win_to_linux(relfile, vodDetail)
        except:
            f=open("log.txt",'a') 
            traceback.print_exc(file=f) 
            f.flush() 
            f.close()
        return 1
        
class tijiao:
    def POST(self):
        web.header('content-type','text/json')
        shipintype,guanggaowei,paiqi,shipinshu=web.input().shipintype,\
                                web.input().guanggaowei,web.input().paiqi,web.input().shipinshu
        if shipintype == "free":
            filepath = "static/upload/free/"
            myfile = "nofile"
            shipinshu_copy = filter(lambda x:x.isdigit(),shipinshu)
            htmlstring='''
                    <script>
                    $(".tihuan").click(function(){
                     $.upload({
                    // 上传地址
                    url: '/uploadxiaotu',
                    // 文件域名字
                    fileName: 'xiaotu',
                    // 其他表单数据
                    params: {
                        shipintype:$(".type").val(),
                        guanggaowei:$(".guanggaowei").val(),
                        paiqi:$(".paiqi").val(),
                        shipinshu:$(".shipinshu").val(),
                        dijige:$(this).parent().attr("value")
                    },
                    // 上传完成后, 返回json, text
                    dataType: 'text',
                    // 上传之前回调,return true表示可继续上传
                    onSend: function() {
                            return true;
                    },
                    // 上传之后回调
                    onComplate: function(data) {
                            alert(data);
                    }
                        });
                    });
                    </script>'''
            for i in range(int(shipinshu_copy)):
                htmlstring += '<label value="'+str(i)+'">视频'+str(i+1)+'  <input type="button" value="替换小图" class="tihuan"/></label></br>'  
            if "news" not in shipinshu:
                #recommend3_2.htm
                paiqi = '_'+paiqi if paiqi != '0' else ""
                filename = "recommend"+shipinshu+'_'+filter(lambda x:x.isdigit(),guanggaowei)+paiqi+".htm"
            elif "news" in shipinshu:
                #recommendnew4_2_1.htm
                paiqi = '_' + paiqi if paiqi != '0' else ""
                filename = "recommendnew"+filter(lambda x:x.isdigit(),shipinshu)+'_'+filter(lambda x:x.isdigit(),guanggaowei)+paiqi+".htm"
            jsondata = json.dumps({"htmlstring":htmlstring,"filename":filename})
            return jsondata
                
        elif shipintype == "nofree":
            filepath = "static/upload/nofree/"
            myfile = "index"+shipinshu+'_'+filter(lambda x:x.isdigit(),guanggaowei)+'_'+paiqi+".htm"
            global relfile
            relfile = filepath + myfile
            if os.path.exists(relfile):
                numidlist=[]
                namelist=[]
                htmlstring='''
                <script>
                $(":button").bind("click",function(){
                  if($(this).attr("id")=="tihuanpmid"){
                      $.post("/pmidtihuan",
                          {
                        //videoname:$("#videoname1").val(),
                         pmid1:$("#pmid1").val(),
                         pmid2:$("#pmid2").val(),
                         pmid3:$("#pmid3").val(),
                         pmid4:$("#pmid4").val(),
                         pmid5:$("#pmid5").val(),
                         pmid6:$("#pmid6").val()
                          },    
                          function(data,status){
                              if(status=="success"){
                                  alert("修改pmid成功");
                                 //$("#yulanlabel").html(data.yulan);
                              }
                              else
                                  alert("提交出错");
                      },"json");
                  }
                  
                  if($(this).attr("id")=="tihuan"){
                     $.upload({
                    // 上传地址
                    url: '/uploadxiaotu',
                    // 文件域名字
                    fileName: 'xiaotu',
                    // 其他表单数据
                    params: {
                        shipintype:$(".type").val(),
                            guanggaowei:$(".guanggaowei").val(),
                            paiqi:$(".paiqi").val(),
                            shipinshu:$(".shipinshu").val(),
                            dijige:$(this).parent().attr("value")
                    },
                    // 上传完成后, 返回json, text
                    dataType: 'text',
                    // 上传之前回调,return true表示可继续上传
                    onSend: function() {
                            return true;
                    },
                    // 上传之后回调
                    onComplate: function(data) {
                            alert(data);
                    }
                        });
                  }
                  
                 
                  
                  });</script>
                  '''
                with open(relfile) as f:
                    for eline in f:
                        if '"pmId"' in eline:
                            #print('4333333333333')
                            string,numid = eline.strip().split(':')
                            numidlist.append(numid)
                        if '"titleName"' in eline:
                            string,name = eline.strip().split(':',1)
                            namelist.append(name)
        #                 print numidlist
        #                 print namelist
                    for i in range(len(numidlist)):
                        htmlstring += '<div style="margin-bottom:5px;"><label>视频'+str(int(i+1))+'<input type="text" readonly id="videoname'+str(int(i+1))+'" value='+namelist[i]+'></label>\
                                        <label>PMID<input id="pmid'+str(int(i+1))+'" type="text" value="'+numidlist[i]+'"/></label>\
                                        <label value="'+str(i)+'">小图片<input type="button" value="替换小图" id="tihuan"/></label>\
                                        <br/>'
        #                 print htmlstring
                    htmlstring += '<br/><label><input type="button" value="替换pmid" id="tihuanpmid"/></label>\
                                   <label id="yulanlabel"></label></div><br/>'
                f.close()
                filename = "index"+filter(lambda x:x.isdigit(),shipinshu)+'_'+filter(lambda x:x.isdigit(),guanggaowei)+"_"+paiqi+".htm"
                jsondata = json.dumps({"htmlstring":htmlstring,"filename":filename})
                return jsondata
            else:
                htmlstring = '<p style="color:red;">没有该文件</p>'
                jsondata = json.dumps({"htmlstring":htmlstring})
                return jsondata
            
                
class testsearch:
    def POST(self):
        resource_name=[]
        resource_id=[]
        column_id = []
        shangjia_id = []
        column_name=[]
        resource_dict={}
        searchname = web.input().inputsearch
          
        #print searchname
#         searchname="马达加斯加"
        try:
            db = web.database(dbn=dbtype,db=dbname,user=user,pw=pw)
#         查询资源ID（resource_id）：
            sql1 = "select ASSET_NAME,RESOURCE_ID from t_iepg_asset t where ASSET_NAME like $name \
            and ROWNUM <= 100"
       
    #         查询栏目ID（column_id）：
            sql2 = "select column_id from t_res_cloumn_map t where resource_id = $id"
       
    #         查询影片上架ID：
            sql3 = "select t.ID from T_RES_CLOUMN_MAP t where t.RESOURCE_ID = $r_id and t.COLUMN_ID = $c_id"
    #         查询栏目名称:
            sql4 = "select t.ALIAS from T_COLUMN t where t.COLUMN_ID = $c_id"
            firstresult = db.query(sql1,vars={'name':'%'+searchname+'%'})
        except:
            f=open("log.txt",'a') 
            traceback.print_exc(file=f) 
            f.flush() 
            f.close()
            return "连接数据库超时,请检查网络"
        for r in firstresult:
            resource_name.append(r['ASSET_NAME'])
            resource_id.append(int(r['RESOURCE_ID'])+1)
#         print "resource_name" + str(resource_name)
#         print "resource_id" + str(resource_id)
        for i in range(len(resource_id)):
            secondresult = db.query(sql2,vars={'id':resource_id[i]})
            for s in secondresult:
                column_id.append(s['COLUMN_ID'])
            copy_column_id = column_id[:]
            resource_dict[resource_name[i]] = [resource_id[i],copy_column_id]
            for c in range(len(column_id)):
                column_id.pop()          
        for k in resource_dict:
            for i in resource_dict[k][1]:
                thirdresult = db.query(sql3,vars={'r_id':resource_dict[k][0],'c_id':i})
                forthresult = db.query(sql4,vars={'c_id':i})
                for i in thirdresult:
                    shangjia_id.append(i["ID"])
                for i in forthresult:
                    column_name.append(i['ALIAS'])
            copy_shangjia_id = shangjia_id[:]
            copy_column_name = column_name[:]
            resource_dict[k].append(copy_shangjia_id)
            resource_dict[k].append(copy_column_name)
            lenth = len(shangjia_id)
            if lenth:
                for i in range(lenth):
                    shangjia_id.pop()
            if column_name:
                column_name.pop()
        result = resource_dict.copy()
#         print result 
#         result={'HD_\xe5\x86\xb0\xe9\x9b\xaa\xe5\xa5\x87\xe7\xbc\x98': [20899092, [20031001, 20058009], [20648135, 20653677], ['\xe5\xa4\xa7\xe7\x89\x87', '\xe7\x83\xad\xe9\x97\xa8\xe7\x82\xb9\xe6\x92\xad']], 'HD_\xe5\x86\xb0\xe9\x9b\xaa\xe5\xa5\x87\xe7\xbc\x98\xef\xbc\x88\xe5\x9b\xbd\xe8\xaf\xad\xef\xbc\x89': [20903403, [20031001], [20647229], ['\xe5\xa4\xa7\xe7\x89\x87']]}
        htmlstring = '''<script>
        $(':checkbox').click(function(){
        if($(this).is(":checked")){
            if($(".type").val()=="free"){
            var link = $("#yulanlink").attr("href");
            var laststr = link.indexOf("=");
            if(link.substring(laststr) == "="){
            $("#yulanlink").attr("href",link + $(this).val());
            $("#yulanlink").text(link + $(this).val());
            }
            }
            }
        else{
            if($(".type").val()=="free"){
            var link = $("#yulanlink").attr("href");
            var laststr = link.indexOf("=");
            var link2 = link.substring(0,laststr+1);
            $("#yulanlink").attr("href",link2);
            $("#yulanlink").text(link2);
        }
        }
            
        if($(this).parents('div').attr("id")=="jieguo1"){
            if($(this).is(":checked")){
            
             $("#pmid1").attr("value",$(this).val());
            }
            else
            $("#pmid1").attr("value","");
            }
        else if($(this).parents('div').attr("id")=="jieguo2"){
            if($(this).is(":checked")){
             $("#pmid2").attr("value",$(this).val());
            }
            else
            $("#pmid2").attr("value","");
            }
        else if($(this).parents('div').attr("id")=="jieguo3"){
            if($(this).is(":checked")){
             $("#pmid3").attr("value",$(this).val());
            }
            else
            $("#pmid3").attr("value","");
            }
        else if($(this).parents('div').attr("id")=="jieguo4"){
            if($(this).is(":checked")){
             $("#pmid4").attr("value",$(this).val());
            }
            else
            $("#pmid4").attr("value","");
            }
        else if($(this).parents('div').attr("id")=="jieguo5"){
            if($(this).is(":checked")){
             $("#pmid5").attr("value",$(this).val());
            }
            else
            $("#pmid5").attr("value","");
            }
        else if($(this).parents('div').attr("id")=="jieguo6"){
            if($(this).is(":checked")){
             $("#pmid6").attr("value",$(this).val());
            }
            else
            $("#pmid6").attr("value","");
            }
            });
        </script>
        <table style="clear:both;">
    <tr>
        <td>影片名称</td>
        <td>栏目名称</td>
        <td>上架ID</td>
        <td>选中</td>
    </tr>'''
#         print 'result>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>'+str(result)
#         for r in result:
#             lenth = len(result[r][1])
#             if lenth:
#                 for i in range(lenth):
#                     htmlstring += '<tr><td>'+r+'</td><td>'+str(result[r][3][i])+'</td>\
#                         <td>'+str(result[r][2][i])+'</td>\
#                         <td><input class="demo" type="checkbox" value="'+str(result[r][2][i]).strip()+'" name="checkbox">\
#                         </td></tr>'
#             else:
#                 htmlstring += '<tr><td colspan="4">没有上架</td></tr>'
#                 break
        for r in result:
            #print 'result[r]>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>'+str(result[r])
            lenth = len(result[r][1])
            if not lenth:
                continue
            else:
                for i in range(lenth):
                    htmlstring += '<tr><td>'+r+'</td><td>'+str(result[r][3][i])+'</td>\
                                  <td>'+str(result[r][2][i])+'</td>\
                                  <td><input class="demo" type="checkbox" value="'+str(result[r][2][i]).strip()+'" name="checkbox">\
                                  </td></tr>'
        htmlstring += '</table>'  
        db.ctx.db.close()
        return htmlstring
        
class login:
    def GET(self):
        return render.login('')
    def POST(self):
        errors = []
        web.header('pragma', 'no-cache')
        web.header('cache-control', 'no-cache,must-revalidate')
        web.header('expires', '0')
        username,passwd = web.input().username,web.input().password
        if username in usernamelist:
            if passwd == 'admin':
                now = datetime.datetime.now()
                f=codecs.open("login_log.txt",'a',encoding="utf-8")
                mystr = u"登录了系统"
                #print '登录了系统'.encode('utf-8')
                f.write(now.strftime('%Y-%m-%d %H:%M:%S')+' ')
                f.write(username+" "+mystr+"\n") 
                return render.main()
            else:
                errors.append(u"密码错误,请确认")
                return render.login(errors)
        else:
            errors.append(u"没有该用户")
            return render.login(errors)
    
class uploadbg:
    def POST(self):
        shipintype,guanggaowei,paiqi,shipinshu=web.input().shipintype,\
                                web.input().guanggaowei,web.input().paiqi,web.input().shipinshu
        x =  web.input(beijing={})
#         print shipintype,guanggaowei,paiqi,shipinshu
        if shipintype == "nofree":
            filepath = "static/upload/nofree/images/"
            temppath = "static/temp/nofree/images/"
            if not os.path.exists(filepath):
                os.makedirs(filepath)
            filedir = filepath
            filename = "portal"+shipinshu+'_'+filter(lambda x:x.isdigit(),guanggaowei)+'_'+paiqi+"_ad.jpg"
            try: 
                if "beijing" in x: 
    #                 filepath=x.beijing.filename.replace('\\','/') 
    #                 filename=filepath.split('/')[-1] 
                    fout = open(filedir +'/'+ filename,'wb') 
                    fout.write(x.beijing.file.read())
                    tempfile = open(temppath + filename,'wb')
                    x.beijing.file.seek(0)
                    tempfile.write(x.beijing.file.read())
#                     同步服务器
#                     for eip in server_ip:
#                         ssh = mysshutils.Myssh(eip)
#                         ssh.win_to_linux(filedir +'/'+ filename, vodDetailimages)
                    return "上传背景成功,目录为"+filedir.encode()
            except:
                f=open("log.txt",'a') 
                traceback.print_exc(file=f) 
                f.flush() 
                f.close()
                return "上传出错,请联系管理员"
            finally:
                fout.close()
        elif shipintype == "free":
            filepath = "static/upload/images/"
            temppath = "static/temp/free/images/"
            if not os.path.exists(filepath):
                os.makedirs(filepath)
            filedir = filepath
            if "news" not in shipinshu:
                paiqi = paiqi+'_' if paiqi != '0' else ""
                filename = "portal"+shipinshu+'_'+filter(lambda x:x.isdigit(),guanggaowei)+'_'+paiqi+"ad.jpg"
            elif "news" in shipinshu:
                #portal3_5_ad_new.jpg
                paiqi = paiqi+'_' if paiqi != '0' else ""
                filename = "portal"+filter(lambda x:x.isdigit(),shipinshu)+'_'+filter(lambda x:x.isdigit(),guanggaowei)+'_'+paiqi+"ad_new.jpg"
#             print "bk" + filename
            try: 
                if "beijing" in x: 
                    fout = open(filedir +'/'+ filename,'wb') 
                    fout.write(x.beijing.file.read())
                    tempfile = open(temppath + filename,'wb')
                    x.beijing.file.seek(0)
                    tempfile.write(x.beijing.file.read())
#                     同步服务器
#                     for eip in server_ip:
#                         ssh = mysshutils.Myssh(eip)
#                         ssh.win_to_linux(filedir +'/'+ filename, dpdbimages)
                    return "上传背景成功,目录为"+filedir.encode()
            except:
                f=open("log.txt",'a') 
                traceback.print_exc(file=f) 
                f.flush() 
                f.close()
                return "上传出错,请联系管理员"
            finally:
                fout.close()
class uploadxiaotu:
    def POST(self):
        shipintype,guanggaowei,paiqi,shipinshu=web.input().shipintype,\
                                web.input().guanggaowei,web.input().paiqi,web.input().shipinshu
        dijige = web.input().dijige   
        x =  web.input(xiaotu={})                  
        if shipintype == "nofree":
            filepath = "static/upload/nofree/images/"
            temppath = "static/temp/nofree/images/"
            if not os.path.exists(filepath):
                os.makedirs(filepath)
            filedir = filepath 
            filename = "listpic"+shipinshu+'_'+filter(lambda x:x.isdigit(),guanggaowei)+'_'+paiqi+'_ad'+dijige+'.jpg'
            #print filename
            try: 
                if "xiaotu" in x: 
                    fout = open(filedir +'/'+ filename,'wb') 
                    fout.write(x.xiaotu.file.read())
                    tempfile = open(temppath + filename,'wb')
                    x.xiaotu.file.seek(0)
                    tempfile.write(x.xiaotu.file.read())
#                     同步服务器
#                     for eip in server_ip:
#                         ssh = mysshutils.Myssh(eip)
#                         ssh.win_to_linux(filedir +'/'+ filename, vodDetailimages)
                    return "上传小图成功,目录为"+filedir.encode()
            except:
                f=open("log.txt",'a') 
                traceback.print_exc(file=f) 
                f.flush() 
                f.close()
                return "上传出错,请联系管理员"
            finally:
                fout.close()
        elif shipintype == "free":
            filepath = "static/upload/images/"
            temppath = "static/temp/free/images/"
            if not os.path.exists(filepath):
                os.makedirs(filepath)
            filedir = filepath 
#             list6_4_1_ad0.jpg
            if "news" not in shipinshu:
                paiqi = paiqi+'_' if paiqi != '0' else ""
                filename = "list"+shipinshu+'_'+filter(lambda x:x.isdigit(),guanggaowei)+'_'+paiqi+"ad"+dijige+".jpg"
            elif "news" in shipinshu:
                #portal3_5_ad_new.jpg
                paiqi = paiqi+'_' if paiqi != '0' else ""
                filename = "list"+filter(lambda x:x.isdigit(),shipinshu)+'_'+filter(lambda x:x.isdigit(),guanggaowei)+'_'+paiqi+"ad_new"+dijige+".jpg"
            #print "filename"+filename
            try: 
                if "xiaotu" in x: 
                    fout = open(filedir +'/'+ filename,'wb') 
                    fout.write(x.xiaotu.file.read())
                    tempfile = open(temppath + filename,'wb')
                    x.xiaotu.file.seek(0)
                    tempfile.write(x.xiaotu.file.read())
#                     同步文件
#                     for eip in server_ip:
#                         ssh = mysshutils.Myssh(eip)
#                         ssh.win_to_linux(filedir +'/'+ filename, dpdbimages)
                    return "上传小图成功,目录为"+filedir.encode()
            except:
                f=open("log.txt",'a') 
                traceback.print_exc(file=f) 
                f.flush() 
                f.close()
                return "上传出错,请联系管理员"
            finally:
                fout.close()
                
class uploadhaibao:
    def POST(self):
        shipintype,guanggaowei,paiqi,shipinshu=web.input().shipintype,\
                                web.input().guanggaowei,web.input().paiqi,web.input().shipinshu
        x =  web.input(haibao={})                  
        if shipintype == "free":
            filepath = "static/upload/images/"
            temppath = "static/temp/free/newsimages/"
            if not os.path.exists(filepath):
                os.makedirs(filepath)
            filedir = filepath 
            now = datetime.datetime.now()
            filename = str(now.year) + str(now.month) + str(now.day) + "NEWS_" + filter(lambda x:x.isdigit(),guanggaowei) + '.jpg'
            #print filename
            try: 
                if "haibao" in x: 
    #                 filepath=x.xiaotu.filename.replace('\\','/') 
    #                 filename=filepath.split('/')[-1] 
                    fout = open(filedir +'/'+ filename,'wb')
                    fout.write(x.haibao.file.read())
                    tempfile = open(temppath + filename,'wb')
                    x.haibao.file.seek(0)
                    tempfile.write(x.haibao.file.read())
#                     同步文件
#                     for eip in server_ip:
#                         ssh = mysshutils.Myssh(eip)
#                         ssh.win_to_linux(filedir +'/'+ filename, haibaoimages)
                    return "上传海报成功,目录为"+filedir.encode()+filename.encode()
            except:
                f=open("log.txt",'a') 
                traceback.print_exc(file=f)
                f.flush() 
                f.close()
                return "上传出错,请联系管理员"
            finally:
                fout.close()
        else:
            return 0
        
class tongbufuwuqi:
    def POST(self):
        allpath = ["static/temp/nofree/","static/temp/nofree/images/","static/temp/free/images/","static/temp/free/newsimages/"]
        serverpath = [vodDetail,vodDetailimages,dpdbimages,haibaoimages]
        lenth = len(allpath)
        i = 0
        try:
            for eip in server_ip:
                ssh = mysshutils.Myssh(eip)
                for epath in allpath:
                    filelist = glob.glob(epath+"*")
                    filelist =[f.replace("\\","/") for f in filelist if os.path.isfile(f)]
                    print "filelist>>>>>>>>>>>>>>>>>>>>"+str(filelist) 
                    if filelist:
                        for efile in filelist:
                            ssh.win_to_linux(efile, serverpath[i])
                        ssh.ssh_disconnect()
                        i += 1
                    else:
                        i += 1
                        continue
                
        except:
            f=open("log.txt",'a') 
            traceback.print_exc(file=f) 
            f.flush() 
            f.close() 
            return "同步出错,请联系管理员"   
        else:
            return "同步成功"
        finally:
            
            now = datetime.datetime.now()
            f=codecs.open("login_log.txt",'a',encoding="utf-8")
            mystr = u"同步了五台服务器"
            f.write(now.strftime('%Y-%m-%d %H:%M:%S')+' ')
            f.write(mystr+"\n") 
            for epath in allpath:
                filelist = glob.glob(epath+"*")
                filelist =[f.replace("\\","/") for f in filelist if os.path.isfile(f)]
                for f in filelist:
                    if f:
                        os.remove(f)
                        
class tongbufuwuqi1:
    def POST(self):
        allpath = ["static/temp/nofree/","static/temp/nofree/images/","static/temp/free/images/","static/temp/free/newsimages/"]
        serverpath = [vodDetail,vodDetailimages,dpdbimages,haibaoimages]
        lenth = len(allpath)
        i = 0
        try:
            for eip in server_ip:
                ssh = mysshutils.Myssh(eip)
                for epath in allpath:
                    filelist = glob.glob(epath+"*")
                    filelist =[f.replace("\\","/") for f in filelist if os.path.isfile(f)]
                    print "filelist>>>>>>>>>>>>>>>>>>>>"+str(filelist) 
                    if filelist:
                        for efile in filelist:
                            ssh.win_to_linux(efile, serverpath[i])
                        ssh.ssh_disconnect()
                        i += 1
                    else:
                        i += 1
                        continue
                
        except:
            f=open("log.txt",'a') 
            traceback.print_exc(file=f) 
            f.flush() 
            f.close() 
            return "同步出错,请联系管理员"   
        else:
            return "同步成功"
        finally:
            now = datetime.datetime.now()
            f=codecs.open("login_log.txt",'a',encoding="utf-8")
            mystr = u"同步了服务器1测试"
            f.write(now.strftime('%Y-%m-%d %H:%M:%S')+' ')
            f.write(mystr+"\n") 
            
if __name__ == '__main__':
    app.run()