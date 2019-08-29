#!/usr/bin/env python3
# ========================================================================================================================
# Author      : Mr.W.Thamba Meshach                              
# Created By  : Naveen B, Yuvaraj S
# Date Created: 01-07-2019
# Date last Modified: 08-08-2019
#
# ======================================================================================================================== 
"""The module has been built for updates the JSON file regularly
to keep the file up to date with the latest version of postgresql.It also
downloads the latest versions of postgresql"""
# ========================================================================================================================
# Imports
# ========================================================================================================================
import os
import re
import urllib.request
import json
from datetime import *
import datetime
import logging
import requests

global m
global download_loc

def getTime():
    
    time=datetime.datetime.today()
    return time

logging.basicConfig(filename='postgresql.log',level=logging.INFO)
m=[]
def webRetrieveRaw():
    """
    
    Retrieves latest version from website and stores them in a file named "x"
    """
    page=urllib.request.urlopen('https://www.postgresql.org/')
    l=page.read()#retrieve from website
    c=l.decode(encoding="utf-8")
    file=open("x.txt","w")
    file.write(c)#prints to x
    file.close()
    logging.info('{}:   Started to retrieve from website'.format(getTime()))
    
    newVer_and_rDate()
    
    
    
   
def newVer_and_rDate():
    """
    
    Gets latest version and Release date from the text file named "x"
    """
    s=open("x.txt","r")
    for line in s:
        if('<div class="col text-white text-center">' in line):
           s=open("x.txt","w")
           s.write(line)    
           
           result=re.search('/">PostgreSQL(.*)Released</a>!',line)
           global b #has web versions
           b = result.group(1)
           result=re.search('<div class="col text-white text-center">(.*): <a href="https://www.postgresql.org/about/news/',line)
           ss=(result.group(1))# has releasedate
           global releaseDatelist
           releaseDatelist=[]
           releaseDatelist=ss.split()
           
           MontoNum(releaseDatelist[1])
           
           releaseDatelist[0]=releaseDatelist[0][:-2]
           
           if(len(releaseDatelist[0])==1):
               releaseDatelist[0]="0"+releaseDatelist[0]
            
           
        
           
          
           break
    
    s.close()
    getwebList()
    
    
def getwebList():
    """
    
    Makes the latest versions into a list
    """
    global l
    l=[]
    l=b.split(",")
    writeJV_to_X()
    

    

def writeJV_to_X():
    """
   
    Reads from JSON file and write to file named "x"
    """
    a=open("postgresql.json","r")
    v=open("x.txt","w")
    for line in a:
       if('minorVersion' in line or 'majorVersion' in line):
           v.write(line)
           continue
           break
    a.close()
    v.close()
    noline()
    
           
def retrieveJsonlist():
   """
   
   Gets all the versions from JSON file
   """
   p=open("x.txt","r")
   file_lines=p.readlines()
   for zz in range(0,num_lines):
       loc = file_lines[zz].strip()
       
       
       m.append(loc)
   #m has all minorversions from json
   hh=[]
   global ll,moo
   ll=[]
   moo=[]
   global mjVersions_no_x
   mjVersions_no_x=[]
   for i in range(0,len(m)):
       
       result=re.search('"majorVersion": "(.*)"',m[i])
       
       try:
           ll.append(result.group(1))
           
           for i in range(0,len(ll)):
          
               
               kkk=re.search('(.*).X',ll[i])
               
               moo.append(kkk.group(1))
       except AttributeError:
           continue

           
   
   #our new json list mjVersions_no_x
   
  
   for i in moo:
       if i not in mjVersions_no_x:
           mjVersions_no_x.append(i)

   global jl
   jl=[]
   global jsonList
   jsonList=[]
   o=""
  
   for i in range(0,len(mjVersions_no_x)):
   
           
           try:
              
              
              
              s=[w for w in m if 'minorVersion": "{}'.format(int(mjVersions_no_x[i])) in w]
              
              if s==[]:
                  appnew(0,0)
              else:
                  
                  h=[s[0].split(":")]
                  
                  y=re.search(' "(.*)"',h[0][1])
      
                  jl.append(y.group(1))
                  
              
           except ValueError:
                  
                  
                  ee=mjVersions_no_x[i]
                  s=[w for w in m if 'minorVersion": "{}'.format(float(ee)) in w]
                  if s==[]:
                      appnew(0,0)
                  else:
                      h=[s[0].split(":")]
                      y=re.search(' "(.*)"',h[0][1])
                      
                      jl.append(y.group(1))
   for i in jl:
       if i not in jsonList:
           jsonList.append(i)
   
   p.close()
   checkCondition()
      
def noline():
    """
    
    Counts the number of line of "x"
    """
    global num_lines
    num_lines= 0
    with open('x.txt', 'r') as f:
        for line in f:
            num_lines += 1
    f.close()
    
    
    retrieveJsonlist()
def checkCondition():
    """
    
    Checks Condition to append or to create a new structure  """
    for i in range(0,len(l[-1])):

        if l[-1][i].isalpha()==True:
            l.remove(l[-1])
        
            break
    tmpl=[]
    for i in range(0,len(l)):
           bh=l[i]
           tmpl.append(bh[1:][:-2])
    
    
    weblist_no_pt=[]
    for i in range(0,len(tmpl)):
        if len(tmpl[i]) >= 3:
            weblist_no_pt.append(tmpl[i][:-1])
        else:
            weblist_no_pt.append(tmpl[i])
    
    for i in range(0,len(weblist_no_pt)):
            
            try:
                
                if weblist_no_pt[i] in mjVersions_no_x:
                    pos=mjVersions_no_x.index(weblist_no_pt[i])
                    
                    if l[i][1:]==jsonList[pos]:
                        word="notupdated"
                       
                       
                    else:
                        appendVersion(mjVersions_no_x.index(weblist_no_pt[i]),i)
                      
                        
                else:
                    appnew(0)
                   
                    
            except ValueError:
                if weblist_no_pt[i] in mjVersions_no_x:
                    
                    
                    if l[i][1:]==jsonList[j]:
                        word="notupdated"                       
                    else:
                        appendVersion(mjVersions_no_x.index(weblist_no_pt[i]),i)
                        
                else:
                    appnew(0)
    try:
        if(word=="notupdated"):
           logging.info('{}:   No new versions found'.format(getTime()))
    except  UnboundLocalError:
        q()
        a=bin(1)
def appendVersion(p1,p2):
    """
    Appends a newer version into JSON.
    Parameters:
    p1(int): Positional value to append into JSON
    p2(int): Position of the  version inside weblist
    """
    global flag
    flag=1
    with open('postgresql.json') as file:
        f=json.loads(file.read())
       
    tp=l[p2]
    
    tmpvar=releaseDatelist[0]
    currDate=datetime.date.today()
    


    
    ob={
        'minorVersion': '{}'.format(tp[1:]),
        'releaseDate': '{}-{}-{}'.format(releaseDatelist[2],releaseDatelist[1],tmpvar)

        }
    f['majorVersions'][p1]['minorVersions'].insert(0,ob)

 
    with open('postgresql.json','w') as q:
         json.dump(f,q,indent=4)
    q.close()
   
    file.close()
    logging.info('{}:   Appended {} version'.format(getTime(),tp[1:]))
    

def appnew(p1):
    """
    Appends a new structure into JSON
    Parameters:
    p1(int): Positional value to append into JSON
    """
    global flag
    flag=1
    try:
        with open('postgresql.json') as file:
            f=json.loads(file.read())
        tp=l[p1]
        eol=strtoDate()
        ob={
            'majorVersion': '{}.X'.format(int(tp[1:][:-2])),
            
          "advisory": {
            "update": [
              "{}".format(tp[1:])
            ],
            "endOfLife": "{}".format(str(eol[0])[:-9]),
            "documents": [
              {
                "documentName": "Installation guide",
                "downloadURL": "https://oss.nic.in/docs.pdf",
                "docType": "application/x-pdf"
              }
            ],
            "isoImage": "",
            "templateName": ""
          },
          "minorVersions": [
              {
                  'minorVersion': '{}'.format(tp[1:]),
                  'releaseDate': '{}-{}-{}'.format(releaseDatelist[2],releaseDatelist[1],releaseDatelist[0])
                  
                  }]
            }
        f['majorVersions'].insert(0,ob)
        with open('postgresql.json','w') as q:
            json.dump(f,q,indent=4)
        q.close()
        file.close()
        
        logging.info('{}:   Appended {} version'.format(getTime(),tp[1:]))
    except ValueError:
        with open('postgresql.json') as file:
            f=json.loads(file.read())
        tp=l[p1]
        eol=strtoDate()
        ob={
            'majorVersion': '{}.X'.format(float(tp[1:][:-2])),
            
          "advisory": {
            "update": [
              "{}".format(tp[1:])
            ],
            "endOfLife": "{}".format(str(eol[0])[:-9]),
            "documents": [
              {
                "documentName": "Installation guide",
                "downloadURL": "https://oss.nic.in/docs.pdf",
                "docType": "application/x-pdf"
              }
            ],
            "isoImage": "",
            "templateName": ""
          },
          "minorVersions": [
              {
                  'minorVersion': '{}'.format(tp[1:]),
                  'releaseDate': '{}-{}-{}'.format(releaseDatelist[2],releaseDatelist[1],releaseDatelist[0])
                  
                  }]
            }
        f['majorVersions'].insert(0,ob)
        with open('postgresql.json','w') as q:
            json.dump(f,q,indent=4)
        q.close()
        file.close()
       
        logging.info('{}:   Appended {} version'.format(getTime(),tp[1:]))
        
    updmjVersions_no_x()


    
def updmjVersions_no_x():
   """
   Updates majorVersion_no_x variable after updating JSON
   """
   a=open("postgresql.json","r")
   v=open("x.txt","w")
   for line in a:
       if('minorVersion' in line or 'majorVersion' in line):
           v.write(line)
           continue
           break
   a.close()
   v.close()
   tmpmin=[]
   tmpll=[]
   p=open("x.txt","r")
   file_lines=p.readlines()
   for zz in range(0,num_lines):
       loc = file_lines[zz].strip()
    
       
       tmpmin.append(loc)
   for i in range(0,len(tmpmin)):
       
       result=re.search('"majorVersion": "(.*)"',tmpmin[i])
       
       try:
           tmpll.append(result.group(1))
          
           for i in range(0,len(tmpll)):
               
               
               kkk=re.search('(.*).X',tmpll[i])
               
               moo.append(kkk.group(1))
       except AttributeError:
           continue
        
   
   #our new json list mjVersions_no_x
   
  
   for i in moo:
       if i not in mjVersions_no_x:
           mjVersions_no_x.insert(0,i)
   
   p.close()
      

           
def MontoNum(month):
    """
    Changes releaseDate variable's month into number.
    Parameters:
    month(String): Month that we need to change into number
    """
   
    if month=="January":
        releaseDatelist[1]='01'
        
    if month=="February":
        releaseDatelist[1]='02'
    
    if month=="March":
        releaseDatelist[1]='03'
    
    if month=="April":
        releaseDatelist[1]='04'
        
    if month=="May":
        releaseDatelist[1]='05'

    if month=="June":
        releaseDatelist[1]='06'
    
    if month=="July":
        releaseDatelist[1]='07'
        
    if month=="August":
        releaseDatelist[1]='08'
        
    if month=="September":
        releaseDatelist[1]='09'
        
    if month=="October":
        releaseDatelist[1]='10'
        
    if month=="November":
        releaseDatelist[1]='11'

    if month=="December":
        releaseDatelist[1]='12'
    

def updatejsonList():
   """
   Updates jsonList variable after updation of JSON.
   """
   mm=[]
   p=open("x.txt","r")
   file_lines=p.readlines()
   for zz in range(0,num_lines):
       loc = file_lines[zz].strip()
       
       
       mm.append(loc)

   hh=[]
   global ll,moo
   ll=[]
   moo=[]
   global mjVersions_no_x
   mjVersions_no_x=[]
   for i in range(0,len(mm)):
       
       result=re.search('"majorVersion": "(.*)"',mm[i])
       
       try:
           ll.append(result.group(1))
           
           for i in range(0,len(ll)):
          
               
               kkk=re.search('(.*).X',ll[i])
               
               moo.append(kkk.group(1))
       except AttributeError:
           continue

           
   
   #our new json list mjVersions_no_x

  
   for i in moo:
       if i not in mjVersions_no_x:
           mjVersions_no_x.append(i)

   global jl
   jl=[]
   global jsonList1
   jsonList1=[]  
   o=""
  
   for i in range(0,len(mjVersions_no_x)):
   
           
           try:
              
              
              
              s=[w for w in mm if 'minorVersion": "{}'.format(int(mjVersions_no_x[i])) in w]
              
              if s==[]:
                  a=1
              else:
                  
                  h=[s[0].split(":")]
                  
                  y=re.search(' "(.*)"',h[0][1])
                
                  
                  
                  jl.append(y.group(1))
                  
              
           except ValueError:
                  
                  
                  ee=mjVersions_no_x[i]
                  s=[w for w in mm if 'minorVersion": "{}'.format(float(ee)) in w]
                  if s==[]:
                      a=1
                  else:
                      h=[s[0].split(":")]
                      y=re.search(' "(.*)"',h[0][1])
                      
                      jl.append(y.group(1))
   for i in jl:
       if i not in jsonList1:
           jsonList1.append(i)
   #has json latest version
   
   p.close()
   
           
               
   
   
def upgrade():
    """
    Updates 'upgrade' structure's value after updation of JSON.
    If no 'upgrade' structure found, then it creates one.
    """
    updmjVersions_no_x()
    updatejsonList()
    
    with open('postgresql.json') as file:
         f=json.loads(file.read())
    temp=f['majorVersions']
    file.close()
 
    for i in range(0,len(temp)-1):
        try:
            with open('postgresql.json') as file:
                 f=json.loads(file.read())

            
            f['majorVersions'][i]['advisory']['update'][0]=jsonList1[i]
            with open('postgresql.json','w') as q:
                        json.dump(f,q,indent=4)
            file.close()
            
          
            
        except KeyError:
            a=bin(1)
    try:
        for i in range(1,len(f['majorVersions'])-1):
            try:
                f['majorVersions'][i]['advisory']['upgrade'][0]=jsonList1[0]
                f['majorVersions'][i]['advisory']['upgrade'][1]=jsonList1[1]
                f['majorVersions'][i]['advisory']['upgrade'][2]=jsonList1[2]
                
                with open('postgresql.json','w') as q:
                     json.dump(f,q,indent=4)
    
            except IndexError:
                a=bin(1)
            except KeyError:
               #insert upgrade box
               datelist=strtoDate()
               
               ob={  "update": [
                          "{}".format(jsonList1[0])
                        ],
                        "upgrade": ['{}'.format(jsonList1[0])],
                        "endOfLife": "{}".format(str(datelist[1])[:-9]),
                        "documents": [
                          {
                            "documentName": "Installation guide",
                            "downloadURL": "https://oss.nic.in/docs.pdf",
                            "docType": "application/x-pdf"
                          }
                        ],
                        "isoImage": "",
                        "templateName": ""
                    }
               
                   
               f['majorVersions'][1]['advisory']=ob
               with open('postgresql.json','w') as q:
                     json.dump(f,q,indent=4)
               a=1
                
        with open('postgresql.json','w') as q:
            json.dump(f,q,indent=4)
    except IndexError:
        a=bin(1)
        
def findEndOfUse():
   """
   Finds and returns the latest version's end of use.
   """
   mm=[]
   p=open("x.txt","r")
   file_lines=p.readlines()
   for zz in range(0,num_lines):
       loc = file_lines[zz].strip()
       
       
       mm.append(loc)
   
   eolList=[]
   for i in range(0,len(mm)):
       
       result=re.search('"minorVersion": "(.*)"',mm[i])
       
       try:
           eolList.append(result.group(1))
           
           
       except AttributeError:
           continue
   p.close()
   return(eolList)

def strtoDate():
    """
    Converts releaseDate list into datetime format for comparison.
    Returns DateList as datetime format.
    """
    dateList=getEOU()
    for i in range(0,len(dateList)):
        try:

            dateList[i]=datetime.datetime.strptime(dateList[i],'%Y-%d-%m')
        except ValueError:
            kuy=bin(1)
 
    return(dateList)
    
        
def updateEOU():
    """
    Updates EndOfUSe,ColorCode,Remark,Alert in JSON.
    """
    finalDate=strtoDate()
    
    currDate=datetime.datetime.today()
    
    
    
    with open('postgresql.json') as file:
        f=json.loads(file.read())

    
    for i in range(0,len(f['majorVersions'])):
        for j in range(0,len(f['majorVersions'][i]['minorVersions'])):
            try:
                if(currDate<finalDate[i]):
                      endOfUse='FALSE'
                else:
                      endOfUse='TRUE'
            
                f['majorVersions'][i]['minorVersions'][j]['endOfUse']=endOfUse
                if(endOfUse=='TRUE'):
                    f['majorVersions'][i]['minorVersions'][j]['colourCode']='RED'
                    f['majorVersions'][i]['minorVersions'][j]['alert']='UnSupported Version'
                    f['majorVersions'][i]['minorVersions'][j]['remark']='Version Upgrade Mandatory'
                else:
                    f['majorVersions'][i]['minorVersions'][j]['colourCode']='AMBER'
                    f['majorVersions'][i]['minorVersions'][j]['remark']='Advisable to Update to Newer Version'
                if j==0:
                    if f['majorVersions'][i]['minorVersions'][j]['endOfUse']=='FALSE':
                          f['majorVersions'][i]['minorVersions'][j]['colourCode']='GREEN'
                          del f['majorVersions'][i]['minorVersions'][j]['remark']
                if (f['majorVersions'][i]['minorVersions'][j]['colourCode']=='AMBER'):
                    try :
                       del f['majorVersions'][i]['minorVersions'][j]['alert']
                    except KeyError:
                        a=bin(1)
            except IndexError:
                a=bin(1)
    

    with open('postgresql.json','w') as q:
                json.dump(f,q,indent=4)

    q.close()
    file.close()
   

def getEOU():
    """
    Retrieves and returns end of use for all majorversions.
    """
    page=urllib.request.urlopen('https://www.postgresql.org/support/versioning/')
    l=page.read()
    c=l.decode("ASCII")
    file=open("z.txt","w")
    file.write(c)
    file.close()
    num_line= 0
    with open('z.txt', 'r') as f:
        for line in f:
            num_line += 1
    f.close()
    verlist=[]
    tEOlist=[]
    EOlist=[]
    s=open("z.txt","r")
    for line in s: 
       verlist.append(line)
    i=verlist.index("  <tbody>\n")
    for line in range(0,num_line):
       result=re.search('       <td>(.*)</td>',verlist[line])
       try:
           tEOlist.append(result.group(1))
       except AttributeError:
           c=bin(0)
    i=0
    while(i<len(tEOlist)):
        EOlist.append(tEOlist[i+4])
        i=i+5

    Finallist=[]
    for i in range(0,len(EOlist)):
        tlist=EOlist[i].split()
        
        tlist[0]=m2n(tlist[0])
        tstr=""
        tlist.reverse()
        for j in range(0,len(tlist)):
            if j!=len(tlist)-1:
               tstr+=tlist[j]+"-"
            else:
                tstr+=tlist[j]
        Finallist.append(tstr)

    for i in range(0,len(Finallist)):
        Finallist[i]=Finallist[i].replace(',','')
    #end of use of all majorversions
    s.close()

    return(Finallist)

def m2n(month):
    """
    Returns numerical format of a given month but does not alter releaseDate list.
    """
    if month=="January":
        mon='01'
    
    if month=="February":
        mon='02'
    
    if month=="March":
        mon='03'
    
    if month=="April":
        mon='04'

    if month=="May":
        mon='05'
    
    if month=="June":
        mon='06'
    
    if month=="July":
        mon='07'
    
    if month=="August":
        mon='08'
    
    if month=="September":
        mon='09'
    
    if month=="October":
        mon='10'
    
    if month=="November":
        mon='11'
    
    if month=="December":
        mon='12'

    return mon

def download():
    """
    Downloads the latest version from website.
    """
    #downlod from website

    try:
        if(flag==1):

            for i in range(0,len(l)):
                
                
                url='https://ftp.postgresql.org/pub/source/v{}/postgresql-{}.tar.gz'.format(l[i][1:],l[i][1:])
                with open('postgresql-{}.tar.gz'.format(l[i][1:]),'wb') as dd:
                    r=requests.get(url)
                    dd.write(r.content)
                url='https://ftp.postgresql.org/pub/source/v{}/postgresql-{}.tar.gz.md5'.format(l[i][1:],l[i][1:])
                with open('postgresql-{}.tar.gz.md5'.format(l[i][1:]),'wb') as dd:
                    r=requests.get(url)
                    dd.write(r.content)

                    logging.info('{}:   Downloaded {}'.format(getTime(),l[i][1:]))

    except NameError:
     a=bin(1)
def q():
    """
    Downloads the latest version from website.
    """
    a=str(getTime())
    a=a[:10]
    with open('postgresql.json') as file:
         f=json.loads(file.read())

            
         f["infoAsOn"]=a
         with open('postgresql.json','w') as q:
             json.dump(f,q,indent=4)
    file.close()
   
   
try: 
   webRetrieveRaw()
   upgrade()
   updateEOU()
   upgrade()
   download()
   
except urllib.error.URLError:
   logging.warning('{}:  No Internet Access'.format(getTime()))
   logging.warning('{}:  Check Internet and try again'.format(getTime()))

logging.info('{}:   Process ended'.format(getTime()))

try:
  os.remove("x.txt")
  os.remove("z.txt")

except:
  a=bin(1)

