#coding=utf-8
'''
Created on 2014年12月11日
如果是选择nofree模版的一些处理方法
@author: boring2
'''
def freeshow(shipinshu,guanggaowei,paiqi):
    filepath = "static/upload/free/"
    myfile = "nofile"
    shipinshu = filter(lambda x:x.isdigit(),shipinshu)
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
    for i in range(int(shipinshu)):
        htmlstring += '<label value="'+str(i)+'">视频'+str(i+1)+'  <input type="button" value="替换小图" class="tihuan"/></label></br>'
    return htmlstring