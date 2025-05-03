'''
该脚本除了依赖代码中所使用到的包以外，还依赖git、pandoc
该脚本依赖Windows系统运行
'''

import os
import stat
import shutil

'''
有关使用该脚本生成网站的具体流程是：
先将仓库拉取到workspace，将Markdown文档转换成html并存入到指定的文件夹中
最后生成gitlog记录
'''

def gen_index_html(src: str, dst: str, title: str) -> None:
    # 扫描src路径下的所有文件，将其列出并存入到dst/index.html，标题为title
    print('making index.html...',end='',flush=True)
    
    files = os.listdir(src)
    fout = open(os.path.join(dst, 'index.md'), 'w', encoding='utf8')
    fout.write(title + '\n')
    for f in files:
        if os.path.isfile(os.path.join(src, f)):
            fout.write('['+f[0:-3]+']('+f[0:-3]+'.html'+')'+'\n<br>\n')
    fout.close()
    os.system('pandoc -f markdown -t html -s '+os.path.join(dst,'index.md')+' -o '+os.path.join(dst,'index.html'))
    os.system('del /Q '+os.path.join(dst,'index.md'))
    
    print('done')

def add_gitlog_url(src: str) -> None:
    # 遍历src目录下的markdown，为每个文件的结尾加上提交记录的链接
    print('adding gitlog-url...',end='',flush=True)
    
    files = os.listdir(src)
    for f in files:
        if os.path.isfile(os.path.join(src, f)):
            fin = open(os.path.join(src, f), 'r', encoding='utf8')
            text = fin.read()
            fin.close()
            
            fout = open(os.path.join(src, f), 'w', encoding='utf8')
            fout.write(text+'\n\n<br>\n\n[查看该文件的提交记录]('+f[0:-3]+'.gitlog.html)')
            fout.close()
    
    print('done')

def gen_gitlog(src: str) -> None:
    # 遍历workspace/src目录下的markdown，为每个文件生成git log信息，生成的文件存在src目录下，文件同名，但后缀为gitlog.md
    print('making gitlog...',end='',flush=True)
    
    files = os.listdir(os.path.join('workspace', src))
    for f in files:
        if os.path.isfile(os.path.join('workspace', src, f)):
            gitlog_name = f[0:-3]+'.gitlog.md'
            os.system('cd workspace&&git log -- ' + os.path.join(src,f) + '>' + os.path.join(src,gitlog_name) + '&&cd ..')

    print('done')

def gen_htmls(src: str, dst: str) -> None:
    # 遍历src目录下的markdown，生成html并存入到dst目录下
    # 生成html时会附加stamon-doc.md
    
    print('converting to html...',end='',flush=True)
    
    files = os.listdir(src)
    for f in files:
        if os.path.isfile(os.path.join(src, f)):
            os.system('pandoc -f markdown -t html -s stamon-doc.md '+os.path.join(src, f)+' -o '+os.path.join(dst, f[0:-3]+'.html'))

    print('done')

def del_dir(path: str) -> None:
    # 优雅的删除文件夹
    if os.path.exists(path):
        os.system('rmdir /S /Q '+path)

if __name__=='__main__':
    print('-----CLEAN-----')
    
    del_dir('workspace')
    del_dir('log')
    del_dir('doc')
    
    os.makedirs('log')
    os.makedirs('doc')
    
    print('-----CLONE-----')
    
    os.system('git clone https://github.com/CLimber-Rong/stamon.git workspace')
    
    # 先生成工作日志
    print('-----MAKE LOG-----')
    gen_index_html('workspace/doc/工作日志', 'log', '<h1 style="font-family: Arial; color: #00BBFF; text-align:center;"><i>Stamon 文档站</i></h1>\n\n[回到首页](../index.html)\n\n## 工作日志集\n')
    add_gitlog_url('workspace/doc/工作日志')
    gen_gitlog('doc/工作日志')
    gen_htmls('workspace/doc/工作日志', 'log')
    
    # 再生成技术文档
    print('-----MAKE DOC-----')
    gen_index_html('workspace/doc', 'doc', '<h1 style="font-family: Arial; color: #00BBFF; text-align:center;"><i>Stamon 文档站</i></h1>\n\n[回到首页](../index.html)\n\n## 技术文档集\n')
    add_gitlog_url('workspace/doc')
    gen_gitlog('doc')
    gen_htmls('workspace/doc', 'doc')
    
    print('-----CLEAN-----')
    del_dir('workspace')
    
    print('-----PUSH-----')
    opt = input('Everything has done, do you wanna push it to github? (Y/N)')
    
    if opt=='Y':
        os.system('git add .')
        os.system('git commit -m \"update website by make.py\"')
        os.system('git push -u origin main')

    print('-----DONE-----')