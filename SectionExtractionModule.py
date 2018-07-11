from pdfminer.pdfparser import PDFParser
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams, LTTextBox,LTChar, LTFigure
import sys
import os
import pandas as pd
class PdfMinerWrapper(object):
    def __init__(self, pdf_doc, pdf_pwd=""):
        self.pdf_doc = pdf_doc
        self.pdf_pwd = pdf_pwd
   
    def __enter__(self):
        #open the pdf file
        self.fp = open(self.pdf_doc, 'rb')
        # create a parser object associated with the file object
        parser = PDFParser(self.fp)
        # create a PDFDocument object that stores the document structure
        doc = PDFDocument(parser, password=self.pdf_pwd)
        # connect the parser and document objects
        parser.set_document(doc)
        self.doc=doc
        return self
    
    def _parse_pages(self):
        rsrcmgr = PDFResourceManager()
        laparams = LAParams(char_margin=3.5, all_texts = True)
        device = PDFPageAggregator(rsrcmgr, laparams=laparams)
        interpreter = PDFPageInterpreter(rsrcmgr, device)
    
        for page in PDFPage.create_pages(self.doc):
            interpreter.process_page(page)
            # receive the LTPage object for this page
            layout = device.get_result()
            # layout is an LTPage object which may contain child objects like LTTextBox, LTFigure, LTImage, etc.
            yield layout
            
    def __iter__(self): 
        return iter(self._parse_pages())
    
    def __exit__(self, _type, value, traceback):
        self.fp.close()
            
    def page_height():
        doc=self.pdf_doc
        for page in doc:     
            print 'Page no.', page.pageid, 'Size',  (page.height, page.width) 
        return

def PDFData(obj):
    with PdfMinerWrapper(obj) as doc:
        i=1
        ans={}
        for page in doc:     
            #print 'Page no.', page.pageid, 'Size',  (page.height, page.width)      
            for tbox in page:
                if not isinstance(tbox, LTTextBox):
                    continue
                #print ' '*1, 'Block', 'bbox=(%0.2f, %0.2f, %0.2f, %0.2f)'% tbox.bbox
                key=i
                i+=1
                value=[]
                for obj in tbox:
                    text=obj.get_text().encode('UTF-8')[:-1] 
                    #print text
                    #value.append(text)
                    x=1
                    for c in obj:
                        if not isinstance(c, LTChar):
                            continue
                        if x==1:
                            #print c.fontname,"   ", c.size,
                            value.append((text,c.fontname,round(c.size,2)))
                            x=0
                ans[key]=value
    return ans                

def RefineData(f):
    ans={}
    cnt=1
    for each in f.keys():
        value=f[each]
        val=[]
        for every in value:
            if len(every[0].strip())!=0:
                val.append(every)
        if len(val)>0:
            ans[cnt]=val
            cnt+=1   
    #print ans
    final={}
    #print "UNIQUEVALUE"
    for each in ans.keys():
        key=(each)
        #print ans[key]
        
        value=Split(ans[each])
        #print value
        final[key]=value
    return final

def Split(listOfTuples):
    key=1
    sub={}
    sent=[]
    #print listOfTuples[0]
    if (len(listOfTuples))>=2:
        for each in range(len(listOfTuples)-1):
            #first=listOfTuples[each][]
            if listOfTuples[each][2]==listOfTuples[each+1][2] :
                
                sent.append(listOfTuples[each][0])
                #print sent
            else:
                sent.append(listOfTuples[each][0])
                sent=" ".join(sent)
                font=listOfTuples[each][1]
                size=listOfTuples[each][2]
                sub[(key)]=(sent,font,size)
                sent=[]
                key=key+1
        sent.append(listOfTuples[each+1][0])
        sent=" ".join(sent)
        font=listOfTuples[each+1][1]
        size=listOfTuples[each+1][2]
        sub[(key)]=(sent,font,size)
        return sub
    else:
        return {(1):(listOfTuples[0][0],listOfTuples[0][1],listOfTuples[0][2])}


def Merge(d):
    #print d
    l=len(d)
    small_letters = map(chr, range(ord('a'), ord('z')+1))
    big_letters = map(chr, range(ord('A'), ord('Z')+1))
    new={}
    ran=range(1,len(d))
    #print d
    for each in ran:
        #print each
        try:
            fir=list(d[each])[0]

            sec=list(d[each+1])[0]
        except:
            break
        #print fir
        #print each,type(each),each+1
        pos='A'
        for eac in sec:
            if eac in small_letters or eac in big_letters:
                pos=eac
                #print 'letter',pos
                break
 
        if pos.islower():
            #print 'hy'
            fir=fir+" "+sec
            #print each
            
            d[each]=(fir,d[each][1],d[each][2])
            prev=len(d)
            del d[each+1]
            #print each+1
            ff=range(each+1,prev)
            #print ff
            for i in ff:
                #print i
                d[i] = d.pop(i+1)
            #print d
            #ran=range(i,len(d))
        else:
            #print 'f'
            d[each]=(fir,d[each][1],d[each][2])
            #print d[each]
            #print d[each+1]
            d[each+1]=(sec,d[each+1][1],d[each+1][2])
            
    return d


# In[25]:
def CapitalizeCount(st):
    st=st.strip("-")
    st=st.strip(" ")
    #st=st.strip("")
    l=st.split(" ")
    #l=['Fexofenadine', '', 'hydrochloride,', '', 'the', '', 'active', '', 'ingredient', '', 'of', '', 'ALLEGRA,', '', 'is', '', 'a', '', 'histamine', '', 'H1-receptor', 'antagonist', '', 'with', '', 'the', '', 'chemical', '', 'name', '', '(\xc2\xb1)-4-[1', '', 'hydroxy-4-[4-(hydroxydiphenylmethyl)-1-', 'piperidinyl]-butyl]-\xce\xb1,', '', '\xce\xb1-dimethyl', '', 'benzeneacetic', '', 'acid', '', 'hydrochloride.', '', 'It', '', 'has', '', 'the', '', 'following', 'chemical', 'structure']
    #print l 
    cnt=0
    for each in l:
        if len(each.strip())!=0 and each[0].isupper():
            cnt+=1
            
    return cnt

def NumberOfWords(st):
    return len(st.strip().split(" "))


def MaximumFontSize(df):
    col=df['FontSize']
    print col
    return max(col)

def ContainsBold(s):
    s=s.lower()
    c=s.count("bold")
    if c>=1:
        return 1.0
    else:
        return 0.0


import pandas as pd
import xml.etree.cElementTree as ET
def GetCustomisedXML(inputfile):
    f=(PDFData(inputfile))
    #print f
    final=RefineData(f)
    #print final
    #return
    for ea in final.keys():
        final[ea]=Merge(final[ea])
    dictio=final
    l=[]
    for each in dictio.keys():
        di=dictio[each]
        for every in di.keys():
            subsection=di[every]
            row=(each,every,subsection[0],subsection[1],subsection[2])
            l.append(row)
    df=pd.DataFrame(l,columns=['Section','SubSection','Content','FontName','FontSize'])
    df['IsBold']=map(lambda x:ContainsBold(x),df['FontName'])
    df['CapitalizeCount']=map(lambda x:CapitalizeCount(x),df['Content'])
    df['NumberOfWords']=map(lambda x:NumberOfWords(x),df['Content'])
    df['PercentageOfCapitalizeCount']=df['CapitalizeCount']*1.0/df['NumberOfWords']
    df['RatioToMaximumSizeInEntireDocument']=df['FontSize']/([MaximumFontSize(df)]*len(df))
    #return df
    numberOfSections=max(df['Section'])
    root = ET.Element("root")
    tag=[]
    for each in range(1,numberOfSections+1):
        sub=df[df['Section']==each]
        sub.index=range(0,len(sub))
        #print len(sub)
        #doc = ET.SubElement(root, "h1 ")
        if len(sub)==1:
            sub['IsMaxFontSize']=sub['FontSize']*1.0/max(sub['FontSize'])
            if (float(sub['RatioToMaximumSizeInEntireDocument'][0])==1.0 or float(sub['IsBold'][0]==1.0)) and float(sub['PercentageOfCapitalizeCount'][0])>=0.50:
                ET.SubElement(root, "title").text = sub['Content'][0].decode('utf-8')
                tag.append("Title")
                #ET.SubElement(root, "para").text = ("No Paragraph").decode('utf-8')
            else:
                #ET.SubElement(root, "title").text = ("No Title").decode('utf-8')
                ET.SubElement(root, "para").text = sub['Content'][0].decode('utf-8')
                tag.append("Para")
                
        else:
            sub['IsMaxFontSize']=sub['FontSize']*1.0/max(sub['FontSize'])
            for l in range(len(sub)):
                if (float(sub['RatioToMaximumSizeInEntireDocument'][l])==1.0 or float(sub['IsBold'][l]==1.0)) and float(sub['PercentageOfCapitalizeCount'][l])>=0.50:
                    ET.SubElement(root, "title").text = sub['Content'][l].decode('utf-8')
                    tag.append("Title")
                    #titlethere=1
                    #ET.SubElement(doc, "p").text = ("No Paragraph").decode('utf-8')
                else:
                    ET.SubElement(root, "para").text = sub['Content'][l].decode('utf-8')
                    tag.append("Para")
                    #ET.SubElement(doc, "div").text = ("No Title").decode('utf-8')
                
                
                
    
    tree = ET.ElementTree(root)
    #tree.write(outputfile)
    df['Tag']=tag
    #print "Get your file at OutputFile Location" 
    return df

def GetOutput(inputFile,outputFile):
    df=GetCustomisedXML(inputFile)
    flag=False
    con=""
    title="No Title"
    t=[]
    for i,row in df.iterrows():
        tag=row['Tag']
        content=row['Content']

        if tag=="Title":
            t.append((title,con))
            con=""
            title=content

        else:
            con+=" "+content
    root = ET.Element("root")
    for each in t:
        ET.SubElement(root, "title").text = each[0].decode('utf-8')
        ET.SubElement(root, "para").text = each[1].decode('utf-8')
    tree = ET.ElementTree(root)
    tree.write(outputFile)
    print "Done"
        



