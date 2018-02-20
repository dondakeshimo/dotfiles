#coding:utf-8
#!/usr/bin/python3
'''
'''

import time
START=time.time()

import os
import sys
import argparse
import codecs
from collections import defaultdict
import json
from pprint import pprint
import re
import traceback
import itertools

import line_profiler
from tqdm import tqdm

from mymodule import cnvk

# Cython
# import pyximport
# pyximport.install()
# import replacement

#自ファイルが存在するディレクトリ, スクリプト名
CURRENT_DIRECTORY=os.path.dirname(os.path.abspath(__file__))
SCRIPT_NAME=re.sub('.py.?','',os.path.basename(__file__))


# line_profiler 用
if 'prof' not in dir():
    def profile(func):
        def inner(*args, **kwargs):
            return func(*args, **kwargs)
            return inner


class FormatText():

    def __init__(self,*args, **kwargs):

        self.judge_translation=kwargs['judge_translation']

        # インスタンス化
        if self.judge_translation:
            from mymodule.google import Google
            self.google=Google(project='precision_medical')


    def load_text(self,path_input):

        with codecs.open(path_input,'r','utf-8') as f:
            lines=f.readlines()

        return lines


    @profile
    def replace_by_regx(self,text):

        text=re.sub(r"［副作用］" , "[副作用]",text)
        text=re.sub(r"【副作用】" , "[副作用]",text)
        text=re.sub(r"〔副作用〕" , "[副作用]",text)
        text=re.sub(r"（副作用）" , "[副作用]",text)
        text=re.sub(r"\(副作用\)" , "[副作用]",text)

        regx=re.findall(u'^\[副作用\](.*)',text)
        if len(regx)>0:
            text=u'%s[副作用]' %(regx[0])

        text=re.sub(r"\[副作用\]" , u"副作用",text)

        text = re.sub(r"【正：(.*?)】", r"\1", text)

        # text = self.exclude_brackets(text)
        text = self.exclude_stars(text)


        text=re.sub(u"h;" , u"H:",text)
        text=re.sub(u"Ｈ；" , u"Ｈ：",text)
        text=re.sub(u"／高値" , u"／上昇",text)
        text=re.sub(u"／低値" , u"／低下",text)
        text=re.sub(u"】" , u"］",text)
        text=re.sub(u"【" , u"［",text)
        text=re.sub(u"〔" , u"［",text)
        text=re.sub(u"〕" , u"］",text)
        text=re.sub(u"([＠＝／・：])[^［]*［解釈：" , u"",text)
        text=re.sub(u"血液＝" , u"",text)
        text=re.sub(u"血清＝" , u"",text)
        text=re.sub(u"尿＝" , u"尿",text)
        # text=re.sub(u"([＠＝／・：［］])[^＊]*＊" , u"\1",text)
        # text=re.sub(r"([＠＝／・：])［([^］]*］*)］([＠＝／・：])" , u"\1\2\3",text)
        # text=re.sub(r"［([^］]*］*)］([＠＝／・：])" , u"\1\2\3",text)
        # text=re.sub(r"^［([^］]*］*)］$" , u"\1\2\3",text)
        # text=re.sub(r"([＠＝／・：])［([^］]*］*)］$" , u"\1\2\3",text)
        text=re.sub(u"\n　" , u"\n",text)
        text=re.sub(u".*［解釈：([^］]*)].*" , u"\1",text)
        text=re.sub(u".*［解釈：([^］]*)］.*" , u"\1",text)
        text=re.sub(u"／／" , u"／",text)
        text=re.sub(u"　／" , u"／",text)
        # text=re.sub(r".*［([^］]*)］.*" , r"\1",text)
        # text=re.sub(r"([＠＝／・：［］])[^＊]*＊" , u"\1",text)
        # text=re.sub(u"[^＊]*＊" , u"\1",text)
        text=re.sub(u"^wbc/" , u"白血球/",text)
        text=re.sub(u"^plt/" , u"血小板/",text)
        text=re.sub(u"^rbc/" , u"赤血球/",text)
        text=re.sub(u"^hb/" , u"赤血球/",text)
        text=re.sub(u"^hb/" , u"赤血球/",text)
        text=re.sub(u"^ht/" , u"赤血球/",text)
        text=re.sub(u"^got/" , u"AST/",text)
        text=re.sub(u"^gpt/" , u"ALT/",text)
        text=re.sub(u"^tp/" , u"蛋白/",text)
        text=re.sub(u"^cre/" , u"クレアチニン/",text)
        text=re.sub(u"^cr/" , u"クレアチニン/",text)
        text=re.sub(u"^neutro/" , u"好中球/",text)
        text=re.sub(u"^lymph/" , u"リンパ球/",text)
        text=re.sub(u"^k/" , u"カリウム/",text)
        text=re.sub(u"^na/" , u"ナトリウム/",text)
        text=re.sub(u"ＡＦＰ／高値" , u"ＡＦＰ／上昇",text)
        text=re.sub(u"ＡＮＡ／上昇" , u"ＡＮＡ／陽性",text)
        text=re.sub(u"ＣＲＰ／高値" , u"ＣＲＰ／上昇",text)
        text=re.sub(u"Ｃ−ペプチド／低下" , u"Ｃペプチド／低下",text)
        text=re.sub(u"Ｄ−ダイマ−／上昇" , u"Ｄダイマ−／上昇",text)
        text=re.sub(u"ＦＧＦ−２３／上昇" , u"ＦＧＦ２３／上昇",text)
        text=re.sub(u"Ｆ−Ｔ３／上昇" , u"ＦＴ３／上昇",text)
        text=re.sub(u"Ｆ−Ｔ４／上昇" , u"ＦＴ４／上昇",text)
        text=re.sub(u"Ｆ−Ｔ４／低下" , u"ＦＴ４／低下",text)
        text=re.sub(u"ＨｂＡ１ｃ／高値" , u"ＨｂＡ１ｃ／上昇",text)
        text=re.sub(u"ＨＢｓ−Ａｂ／陰性" , u"ＨＢｓＡｂ／陰性",text)
        text=re.sub(u"ＨＢｓ−Ａｇ／陽性" , u"ＨＢｓＡｇ／陽性",text)
        text=re.sub(u"ＨＣＯ３／低下" , u"ＨＣＯ３−／低下",text)
        text=re.sub(u"ＨＣＶＡｂ／陰性" , u"ＨＣＶ抗体／陰性",text)
        text=re.sub(u"ＨＣＶ−Ａｂ／陰性" , u"ＨＣＶ抗体／陰性",text)
        text=re.sub(u"ＨＤＬ−Ｃ／低下" , u"ＨＤＬ／低下",text)
        text=re.sub(u"ＩＧＦ−１／上昇" , u"ＩＧＦ−Ｉ／上昇",text)
        text=re.sub(u"ＩＧＦ−１／低下" , u"ＩＧＦ−Ｉ／低下",text)
        text=re.sub(u"ｉｎｔａｃｔ＿ＰＴＨ／上昇" , u"ｉｎｔａｃｔＰＴＨ／上昇",text)
        text=re.sub(u"ｉｎｔａｃｔ＿ＰＴＨ／正常" , u"ｉｎｔａｃｔＰＴＨ／正常",text)
        text=re.sub(u"ｉｎｔａｃｔ＿ＰＴＨ／低下" , u"ｉｎｔａｃｔＰＴＨ／低下",text)
        text=re.sub(u"ＩＮＴＡＣＴ−ＰＴＨ／上昇" , u"ｉｎｔａｃｔＰＴＨ／上昇",text)
        text=re.sub(u"ＬＤ／上昇" , u"ＬＤＨ／上昇",text)
        text=re.sub(u"ＰＩＶＫＡ−２／上昇" , u"ＰＩＶＫＡ−ＩＩ／上昇",text)
        text=re.sub(u"Ｔ．Ｂｉｌ／上昇" , u"Ｔ−ｂｉｌ／上昇",text)
        text=re.sub(u"Ｔ−ｃｈｏｌ／上昇" , u"Ｔ−Ｃｈｏ／上昇",text)
        text=re.sub(u"Ｔｇ−Ａｂ／上昇" , u"ＴｇＡｂ／上昇",text)
        text=re.sub(u"ＴＰＯＡｂ／上昇" , u"ＴＰＯＡｂ／陽性",text)
        text=re.sub(u"ＴＲＡｂ／上昇" , u"ＴＲＡｂ／陽性",text)
        text=re.sub(u"γ−Ｇ蛋白／上昇" , u"γＧ蛋白／上昇",text)
        text=re.sub(u"γ−Ｇ蛋白／正常" , u"γＧ蛋白／正常",text)
        text=re.sub(u"フェリチン値／上昇" , u"フェリチン／上昇",text)
        text=re.sub(u"レニン活性／低下" , u"レニン／低下",text)
        text=re.sub(u"意識レベル／低下" , u"意識／低下",text)
        text=re.sub(u"異形リンパ球／陽性" , u"異型リンパ球／陽性",text)
        text=re.sub(u"炎症／上昇" , u"炎症反応／上昇",text)
        text=re.sub(u"炎症所見／陰性" , u"炎症反応／陰性",text)
        text=re.sub(u"炎症所見／上昇" , u"炎症反応／上昇",text)
        text=re.sub(u"炎症反応／陽性" , u"炎症反応／上昇",text)
        text=re.sub(u"芽球／上昇" , u"芽球／陽性",text)
        text=re.sub(u"血液ガス分析＝ＨＣＯ３／低下" , u"血液ガス＝ＨＣＯ３−／低下",text)
        text=re.sub(u"血液ガス分析＝ｐＨ／低下" , u"血液ガス＝ｐＨ／低下",text)
        text=re.sub(u"血液ガス分析＝ｐＯ２／低下" , u"血液ガス＝ＰａＣＯ２／低下",text)
        text=re.sub(u"血小板／低下" , u"血小板／減少",text)
        text=re.sub(u"血小板数／正常" , u"血小板／正常",text)
        text=re.sub(u"血小板数／低下" , u"血小板／低下",text)
        text=re.sub(u"血清ＡＣＥ／上昇" , u"ＡＣＥ／上昇",text)
        text=re.sub(u"血清ＩｇＧ４／上昇" , u"ＩｇＧ４／上昇",text)
        text=re.sub(u"血清ＩＬ−６／上昇" , u"ＩＬ−６／上昇",text)
        text=re.sub(u"血清Ｋ／低下" , u"Ｋ／低下",text)
        text=re.sub(u"血清Ｍ蛋白／陽性" , u"Ｍ蛋白／陽性",text)
        text=re.sub(u"血清Ｎａ／正常" , u"Ｎａ／正常",text)
        text=re.sub(u"血清アミラ−ゼ／上昇" , u"アミラ−ゼ／上昇",text)
        text=re.sub(u"血清アルブミン／低下" , u"アルブミン／低下",text)
        text=re.sub(u"血清クレアチニン／上昇" , u"クレアチニン／上昇",text)
        text=re.sub(u"血清クレアチニン／正常" , u"クレアチニン／正常",text)
        text=re.sub(u"血清抗糖脂質抗体／陽性" , u"抗糖脂質抗体／陽性",text)
        text=re.sub(u"血清浸透圧／上昇" , u"浸透圧／上昇",text)
        text=re.sub(u"血清浸透圧／低下" , u"浸透圧／低下",text)
        text=re.sub(u"血清銅／低下" , u"銅／低下",text)
        text=re.sub(u"血中ＣＫ値／上昇" , u"ＣＫ／上昇",text)
        text=re.sub(u"血中ＣＰＲ／低下" , u"ＣＰＲ／低下",text)
        text=re.sub(u"血中Ｃペプチド／上昇" , u"Ｃペプチド／上昇",text)
        text=re.sub(u"血中Ｃペプチド／低下" , u"Ｃペプチド／低下",text)
        text=re.sub(u"血中インスリン／上昇" , u"インスリン／上昇",text)
        text=re.sub(u"血中総ケトン／上昇" , u"総ケトン／上昇",text)
        text=re.sub(u"血糖／上昇" , u"血糖／高値",text)
        text=re.sub(u"血糖値／上昇" , u"血糖／高値",text)
        text=re.sub(u"血糖値／低下" , u"血糖／低下",text)
        text=re.sub(u"好酸球数／上昇" , u"好酸球／上昇",text)
        text=re.sub(u"抗ＤＮＡ抗体／上昇" , u"抗ＤＮＡ抗体／陽性",text)
        text=re.sub(u"抗ｄｓ−ＤＮＡ抗体／陽性" , u"抗ｄｓＤＮＡ抗体／陽性",text)
        text=re.sub(u"抗ＧＡＤ抗体／上昇" , u"抗ＧＡＤ抗体／陽性",text)
        text=re.sub(u"抗ＲＮＰ抗体／上昇" , u"抗ＲＮＰ抗体／陽性",text)
        text=re.sub(u"抗ＳＳ−Ａ／Ｒｏ抗体" , u"抗ＳＳＡ抗体／Ｒｏ抗体",text)
        text=re.sub(u"抗ＳＳ−Ａ抗体／陽性" , u"抗ＳＳＡ抗体／陽性",text)
        text=re.sub(u"抗ＳＳ−Ｂ抗体／陰性" , u"抗ＳＳＢ抗体／陰性",text)
        text=re.sub(u"抗ＳＳ−Ｂ抗体／陽性" , u"抗ＳＳＢ抗体／陽性",text)
        text=re.sub(u"抗Ｔｇ抗体／上昇" , u"抗Ｔｇ抗体／陽性",text)
        text=re.sub(u"抗ＴＰＯ抗体／上昇" , u"抗ＴＰＯ抗体／陽性",text)
        text=re.sub(u"抗アセチルコリン受容体抗体／上昇" , u"抗アセチルコリン受容体抗体／陽性",text)
        text=re.sub(u"抗核抗体／上昇" , u"抗核抗体／陽性",text)
        text=re.sub(u"心拍／正常" , u"心拍数／正常",text)
        text=re.sub(u"神経学的異常所見／陰性" , u"神経学的異常／陰性",text)
        text=re.sub(u"神経学的所見／正常" , u"神経所見／正常",text)
        text=re.sub(u"神経症状／陰性" , u"神経所見／陰性",text)
        text=re.sub(u"神経伝導検査／正常" , u"神経伝導速度／正常",text)
        text=re.sub(u"随時血糖値／上昇" , u"随時血糖／上昇",text)
        text=re.sub(u"髄液＝細胞／上昇" , u"髄液＝細胞数／上昇",text)
        text=re.sub(u"髄液検査／正常" , u"髄液／正常",text)
        text=re.sub(u"髄液検査＝ＩＬ−６／上昇" , u"髄液＝ＩＬ−６／上昇",text)
        text=re.sub(u"髄液検査＝細胞数／上昇" , u"髄液＝細胞数／上昇",text)
        text=re.sub(u"髄液検査＝細胞数／正常" , u"髄液＝細胞数／正常",text)
        text=re.sub(u"髄液検査＝総蛋白／上昇" , u"髄液＝総蛋白／上昇",text)
        text=re.sub(u"髄液検査＝単核球／上昇" , u"髄液＝単核球／上昇",text)
        text=re.sub(u"髄液検査＝蛋白／上昇" , u"髄液＝蛋白／上昇",text)
        text=re.sub(u"髄液検査＝糖／正常" , u"髄液＝糖／正常",text)
        text=re.sub(u"髄液検査＝糖／低下" , u"髄液＝糖／低下",text)
        text=re.sub(u"髄液細胞数／上昇" , u"髄液＝細胞数／上昇",text)
        text=re.sub(u"髄液細胞数／正常" , u"髄液＝細胞数／正常",text)
        text=re.sub(u"髄液所見／正常" , u"髄液／正常",text)
        text=re.sub(u"髄液所見＝蛋白／上昇" , u"髄液＝蛋白／上昇",text)
        text=re.sub(u"髄液蛋白／上昇" , u"髄液＝蛋白／上昇",text)
        text=re.sub(u"髄液蛋白／正常" , u"髄液＝蛋白／正常",text)
        text=re.sub(u"髄膜刺激症状／陰性" , u"髄膜刺激徴候／陰性",text)
        text=re.sub(u"髄膜刺激症状／陽性" , u"髄膜刺激徴候／陽性",text)
        text=re.sub(u"髄膜刺激兆候／陰性" , u"髄膜刺激徴候／陰性",text)
        text=re.sub(u"染色体／正常" , u"染色体分析／正常",text)
        text=re.sub(u"蛋白尿／上昇" , u"蛋白尿／陽性",text)
        text=re.sub(u"尿ケトン／陰性" , u"尿ケトン体／陰性",text)
        text=re.sub(u"尿ケトン／陽性" , u"尿ケトン体／陽性",text)
        text=re.sub(u"尿検査＝ケトン／陽性" , u"尿＝ケトン／陽性",text)
        text=re.sub(u"尿中赤血球／上昇" , u"尿中赤血球／陽性",text)
        text=re.sub(u"尿中白血球／上昇" , u"尿中白血球／陽性",text)
        text=re.sub(u"白血球／低下" , u"白血球／減少",text)
        text=re.sub(u"白血球数／上昇" , u"白血球／上昇",text)
        text=re.sub(u"白血球数／正常" , u"白血球／正常",text)
        text=re.sub(u"白血球数／低下" , u"白血球／減少",text)
        text=re.sub(u"腹水ＡＤＡ／上昇" , u"腹水＝ＡＤＡ／上昇",text)
        text=re.sub(u"腹部ＣＴ検査／正常" , u"腹部ＣＴ／正常",text)
        text=re.sub(u"末梢血＝異型リンパ球／陽性" , u"異型リンパ球／陽性",text)
        text=re.sub(u"末梢血＝芽球／陽性" , u"芽球／陽性",text)
        text=re.sub(u"末梢血好酸球／上昇" , u"好酸球／上昇",text)
        text=re.sub(u"網赤血球／低下" , u"網状赤血球／低下",text)
        # text=re.sub(r"（.*?）" , "",text)
        # text=re.sub(r"\(.*?\)" , "",text)

        text = self.expand_dot(text)

        return text


    def dedupe(self,text):

        terms=[]
        if re.search(u'[=＝:：\/・@＠]',text):

            text=re.sub(u'[=＝:：\/・@＠]',u'☆☆☆',text)
            terms=text.split(u'☆☆☆')

            return terms

        else:
            return [text]


    def exclude_brackets(self, text):
        text = re.sub(u"＠", u"@", text)
        text = re.sub(u"：", u":", text)
        text = re.sub(u"／", u"/", text)
        text = re.sub(u"＝", u"=", text)
        text = re.sub(u"h;", u"H:", text)
        text = re.sub(u"@", u"＆@＆", text)
        text = re.sub(u":", u"＆:＆", text)
        text = re.sub(u"/", u"＆/＆", text)
        text = re.sub(u"=", u"＆=＆", text)
        text = re.sub(u"H:", u"＆H:＆", text)
        text = re.sub(u"PH:", u"＆PH:＆", text)
        text = re.sub(u"FH:", u"＆FH:＆", text)

        # TODO: 正規表現の\1などの表記をうまく使うスクリプトに変更
        match_obj = re.search(r"[【［〔\[].*?[】］〕\]]", text)

        if match_obj:
            repl = match_obj.group()
            repl = repl.replace(u"＆", u"")
            text = text[:match_obj.start()] + repl + text[match_obj.end():]

        text = text.split(u"＆")

        for i, s in enumerate(text):
            match_obj = re.search(r"[【［〔\[].*?[】］〕\]]", s)

            if match_obj:
                repl = match_obj.group()
                repl = repl.replace(u"【", u"")
                repl = repl.replace(u"】", u"")
                repl = repl.replace(u"［", u"")
                repl = repl.replace(u"］", u"")
                repl = repl.replace(u"〔", u"")
                repl = repl.replace(u"〕", u"")
                repl = repl.replace(u"[", u"")
                repl = repl.replace(u"]", u"")
                text[i] = repl

        text = u"".join(text)
        return text


    def exclude_stars(self, text):

        text = re.sub(u"＠", u"@", text)
        text = re.sub(u"：", u":", text)
        text = re.sub(u"／", u"/", text)
        text = re.sub(u"＝", u"=", text)
        text = re.sub(u"＊", u"*", text)
        text = re.sub(u"@", u"＆@＆", text)
        text = re.sub(u":", u"＆:＆", text)
        text = re.sub(u"/", u"＆/＆", text)
        text = re.sub(u"=", u"＆=＆", text)
        text = re.sub(u"・", u"＆・＆", text)
        text = text.split(u"＆")

        for i, s in enumerate(text):
            if s.find(u"*") > -1:
                part_tuple = s.rpartition(u"*")
                text[i] = part_tuple[2]

        text = u"".join(text)

        return text


    def load_blacklist(self, path_blacklist):
        with codecs.open(path_blacklist,'r','utf-8') as f:
            blacklist=f.read()

        blacklist = blacklist.split("\n")[:-1]

        return blacklist


    def expand_dot(self, text):
        text = re.sub(r"([ァ-ヴ]+?)・([ァ-ヴ]+?)", r"\1■\2", text)
        NS = r"[^/@・=:]*?"  # not symbol
        pat_00 = NS + r"(・" + NS + r")+"
        pat_01 = NS + r"=" + NS + r"/" + NS + r"@" + NS
        pat_02 = NS + r"=" + NS + r"@" + NS
        pat_03 = NS + r"=" + NS + r"/" + NS
        pat_04 = NS + r"@" + NS
        pat_05 = NS + r"/" + NS
        pat_06 = NS + r"/" + NS + r"@" + NS
        pat_07 = NS + r"=" + NS
        pat_08 = NS + r":" + NS

        # A1・A2・A3
        if re.match(pat_00 + r"$", text):
            text = text.replace(u"・", u"＆")
        # A1=B1/C1@D1・A2=B2/C2@D2・A3=B3/C3@D3
        elif re.match(pat_01 + r"(・" + pat_01 + r")+$", text):
            text = text.replace(u"・", u"＆")
        # A1=B1@D1・A2=B2@D2・A3=B3@D3
        elif re.match(pat_02 + r"(・" + pat_02 + r")+$", text):
            text = text.replace(u"・", u"＆")
        # A1=B1/C1・A2=B2/C2・A3=B3/C3
        elif re.match(pat_03 + r"(・" + pat_03 + r")+$", text):
            text = text.replace(u"・", u"＆")
        # B1@D1・B2@D2・B3@D3
        elif re.match(pat_04 + r"(・" + pat_04 + r")+$", text):
            text = text.replace(u"・", u"＆")
        # B1/C1・B2/C2・B3/C3
        elif re.match(pat_05 + r"(・" + pat_05 + r")+$", text):
            text = text.replace(u"・", u"＆")
        # A=B1@C1・B2@C2
        elif re.match(pat_07 + pat_04 + r"(・" + pat_04 + r")+$", text):
            text = self.product_text(text, eq=True)
        # A=B1/C1・B2/C2
        elif re.match(pat_07 + pat_05 + r"(・" + pat_05 + r")+$", text):
            text = self.product_text(text, eq=True)
        # A1・A2・A3=B/C@D
        elif re.match(pat_00 + pat_01 + r"$", text):
            text = self.product_text(text, eq=True)
        # A1・A2・A3=B@D
        elif re.match(pat_00 + pat_02 + r"$", text):
            text = self.product_text(text, at=True, sl=True, eq=True)
        # A1・A2・A3=B/C
        elif re.match(pat_00 + pat_03 + r"$", text):
            text = self.product_text(text, at=True, eq=True)
        # A1・A2・A3=B
        elif re.match(pat_00 + pat_07 + r"$", text):
            text = self.product_text(text, eq=True)
        # B1・B2・B3@D
        elif re.match(pat_00 + pat_04 + r"$", text):
            text = self.product_text(text, at=True)
        # B1・B2・B3/C
        elif re.match(pat_00 + pat_05 + r"$", text):
            text = self.product_text(text, sl=True)
        # A=B1・B2・B3/C@D
        elif re.match(pat_07 + pat_00 + pat_06 + r"$", text):
            text = self.product_text(text, at=True, sl=True, eq=True)
        # A=B1・B2・B3@D
        elif re.match(pat_07 + pat_00 + pat_04 + r"$", text):
            text = self.product_text(text, at=True, eq=True)
        # A=B1・B2・B3/C
        elif re.match(pat_07 + pat_00 + pat_05 + r"$", text):
            text = self.product_text(text, sl=True, eq=True)
        # A=D1・D2・D3
        elif re.match(pat_07 + pat_00 + r"$", text):
            text = self.product_text(text, eq=True)
        # A=B/C@D1・D2・D3
        elif re.match(pat_01 + pat_00 + r"$", text):
            text = self.product_text(text, at=True)
        # A=B@D1・D2・D3
        elif re.match(pat_02 + pat_00 + r"$", text):
            text = self.product_text(text, at=True)
        # B@D1・D2・D3
        elif re.match(pat_04 + pat_00 + r"$", text):
            text = self.product_text(text, at=True)
        # B1・B2/C@D
        elif re.match(pat_00 + pat_06 + r"$", text):
            text = self.product_text(text, at=True, sl=True)
        # B/C@D1・D2・D3
        elif re.match(pat_06 + pat_00 + r"$", text):
            text = self.product_text(text, at=True)
        # H:A1・A2・A3
        elif re.match(pat_08 + pat_00 + r"$", text):
            text = self.product_text(text, cl=True)
        # H:A1・A2・A3@C
        elif re.match(pat_08 + pat_00 + pat_04 + r"$", text):
            text = self.product_text(text, at=True, cl=True)
        # H:A1・A2・A3/C
        elif re.match(pat_08 + pat_00 + pat_05 + r"$", text):
            text = self.product_text(text, sl=True, cl=True)
        # H:A@C1・C2
        elif re.match(pat_08 + pat_04 + pat_00 + r"$", text):
            text = self.product_text(text, at=True, cl=True)
        # A1・A2・A3=B/C@D1・D2・D3
        elif re.match(pat_00 + pat_01 + pat_00 + r"$", text):
            text = self.product_text(text, at=True, eq=True)
        # A1・A2・A3=B1・B2・B3/C@D
        elif re.match(pat_00 + pat_07 + pat_00 + pat_06 + r"$", text):
            text = self.product_text(text, at=True, sl=True, eq=True)
        # A=B1・B2・B3/C@D1・D2・D3
        elif re.match(pat_07 + pat_00 + pat_06 + pat_00 + r"$", text):
            text = self.product_text(text, at=True, eq=True)
        # A1・A2=B1・B2@C
        elif re.match(pat_00 + pat_07 + pat_00 + pat_04 + r"$", text):
            text = self.product_text(text, at=True, eq=True)
        # A1・A2=B1・B2
        elif re.match(pat_00 + pat_07 + pat_00 + r"$", text):
            text = self.product_text(text, eq=True)
        # A1・A2=B1@C1・C2
        elif re.match(pat_00 + pat_02 + pat_00 + r"$", text):
            text = self.product_text(text, at=True, eq=True)
        # A=B1・B2@C1・C2
        elif re.match(pat_07 + pat_00 + pat_04 + pat_00 + r"$", text):
            text = self.product_text(text, at=True, eq=True)
        # A1・A2=B1・B2/C
        elif re.match(pat_00 + pat_07 + pat_00 + pat_05 + r"$", text):
            text = self.product_text(text, at=True, sl=True, eq=True)
        # B1・B2/C@D1・D2
        elif re.match(pat_00 + pat_06 + pat_00 + r"$", text):
            text = self.product_text(text, at=True, sl=True, eq=True)
        # A1・A2@B1・B2
        elif re.match(pat_00 + pat_04 + pat_00 + r"$", text):
            text = self.product_text(text, at=True)

        text = re.sub(u"■", u"・", text)
        return text


    def product_text(self, text, at=False, sl=False, eq=False, cl=False):
        if at:
            text = re.sub(u"@", u"＆@＆", text)
        if sl:
            text = re.sub(u"/", u"＆/＆", text)
        if eq:
            text = re.sub(u"=", u"＆=＆", text)
        if cl:
            if re.match(r"H:|PH:|FH:", text):
                text = re.sub(u":", u"＆:＆", text)
        text = text.split(u"＆")
        text_dot = []
        text_symbol = []

        for i, t in enumerate(text):
            if t == u"@" or t == u"=" or t == u"/" or t == u":":
                text_symbol.append(t)
            else:
                text_dot.append(t.split(u"・"))

        text = []
        for t in itertools.product(*text_dot):
            temp = t[0]
            for i in range(1, len(t)):
                temp += text_symbol[i-1]
                temp += t[i]
            else:
                text.append(temp)

        text = u"＆".join(text)

        return text


    def replace(self,text,processing_already,judge_cython):

        if text in processing_already:

            return processing_already[text],processing_already

        else:

            # 正規表現の処理を実行する
            text_new=self.replace_by_regx(text)

            # 秀丸の処理を実行する
            # if not judge_cython:
            #     text_new=self.replace_by_hidemaru(text_new)
            #
            # else:
            #     text_new=replacement.replace_by_hidemaru(text_new)

            processing_already[text]=text_new

            return text_new,processing_already


    @profile
    def format(self, lines, blacklist, judge_translation, judge_cython):

        text=''
        processing_already={}

        progress_bar=tqdm(range(len(lines)))
        for i,line in enumerate(lines):
            try:

                # black_flag = 0
                # for b in blacklist:
                #     if line.find(b) > -1:
                #         black_flag = 1

                # if black_flag:
                #     continue

                cols=line.rstrip('\n').split('\t')
                cols_new=[]


                if len(cols)<3:
                    continue


                # 1列目の処理
                col0,processing_already=self.replace(
                    text=cols[0],
                    processing_already=processing_already,
                    judge_cython=judge_cython
                )
                cols_new.append(col0)


                # 2列目の処理
                col1,processing_already=self.replace(
                    text=cols[1],
                    processing_already=processing_already,
                    judge_cython=judge_cython
                )
                cols_new.append(col1)


                # 3列目をそのまま格納する
                cols_new.append(cols[2])


                if len(cols)==5:
                    # 4列目と5列目をそのまま格納する
                    cols_new.append(cols[3])
                    cols_new.append(cols[4])
                elif len(cols)<5:
                    # 書き換え前の1列目と2列目を、4列目と5列目に格納する
                    cols_new.append(cols[0])
                    cols_new.append(cols[1])
                elif len(cols)==10:
                    # from_original, to_originalのみを書き換える
                    cols_new.append(cols[3])
                    cols_new.append(cols[4])
                    cols_new.append(cols[5])
                    cols_new.append(cols[6])
                    cols_new.append(cols[7])
                    cols_new.append(cols[8])
                    cols_new.append(cols[9])
                elif len(cols)==8:
                    # from_original, to_originalを左に追加する
                    cols_new.append(cols[0])
                    cols_new.append(cols[1])
                    cols_new.append(cols[3])
                    cols_new.append(cols[4])
                    cols_new.append(cols[5])
                    cols_new.append(cols[6])
                    cols_new.append(cols[7])



                # if cols_new[0]!=cols[0]:
                #     print('%s\t%s' %(cols_new[0],cols[0]))

                # if cols[0]!=cols[3]:
                #     print('%s\t%s' %(cols[0],cols[3]))

                # if cols[1]!=cols[4]:
                #     print('%s\t%s' %(cols[1],cols[4]))

                # 2列目に＆があった場合行を増やす
                if u"＆" in cols_new[0] or u"＆" in cols_new[1]:
                    temp_cols1 = cols_new[0].split(u"＆")
                    temp_cols2 = cols_new[1].split(u"＆")
                    for col_1 in temp_cols1:
                        cols_new[0] = col_1
                        for col_2 in temp_cols2:
                            cols_new[1] = col_2
                            text += "\t".join(cols_new) + "\n"
                else:
                    text += '\t'.join(cols_new) + '\n'

            except KeyboardInterrupt:
                break

            except:
                print(cols)
                print(traceback.format_exc())

            finally:
                progress_bar.update(1)
                # if i==100:
                #     break

        progress_bar.close()


        return text

    def save_text(self,path_output,text):

        with codecs.open(path_output,'w','utf-8') as f:
            f.write(text)


    @profile
    def main(self,path_input,path_output,path_blacklist,judge_cython):
        '''
        メインの処理を実行します。
        '''

        try:
            # テキストファイルを読み込む
            lines=self.load_text(
                path_input=path_input
            )


            blacklist = []
            if path_blacklist:
                # ブラックリストファイルを読み込む
                blacklist=self.load_blacklist(
                    path_blacklist=path_blacklist
                )

            # 正規表現を使って整形する
            text=self.format(
                lines=lines,
                blacklist=blacklist,
                judge_translation=self.judge_translation,
                judge_cython=judge_cython
            )

            # テキストファイルを書き出す
            self.save_text(
                path_output=path_output,
                text=text
            )

        except:
            print(traceback.format_exc())

        finally:
            pass


if __name__ == '__main__':

    # コマンドライン引数を取得する
    parser=argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description='''

1. relations.txtを整形する。
    例) python3 format_text.py -i "data/relations_source.txt" -o "data/relations_new.txt"


2. 各単語の変換テストをする。
    例) python3 format_text.py -i "data/relations_source.txt" -k "[インスリン副作用]"


3. 処理速度を計測する。
    例）kernprof -l -v format_text.py -i "data/relations_source.txt" -o "data/relations_new.txt"

''')
    parser.add_argument('-i','--path_input',help='読み込みたいファイルのパス',default=False)
    parser.add_argument('-o','--path_output',help='出力したいファイルのパス',default=False)
    parser.add_argument('-b','--path_blacklist',help='ブラックリストのファイルのパス',default=False)
    parser.add_argument('-k','--keyword',help='デバッグしたいキーワード',default=False)
    parser.add_argument('-t','--judge_translation',help='翻訳をするか否か',default=False,action='store_true')
    parser.add_argument('-c','--cython',help='Cythonを使うか否か',default=False,action='store_true')
    kwargs=vars(parser.parse_args())


    if not kwargs['keyword']:
        # 1.relations.txt を整形する場合

        response=FormatText(**kwargs)
        response.main(
            path_input=kwargs['path_input'],
            path_output=kwargs['path_output'],
            path_blacklist=kwargs['path_blacklist'],
            judge_cython=kwargs['cython']
        )

    elif kwargs['keyword']:
        # 2.単語のテストをする場合

        for keyword in kwargs['keyword'].split(','):
            keyword = keyword.decode("utf-8")

            text_modified=FormatText(**kwargs).replace_by_regx(
                text=keyword
            )

            text_modified=FormatText(**kwargs).replace_by_hidemaru(
                text=text_modified
            )

            if u"＆" in text_modified:
                text_modified = text_modified.split(u"＆")

            print('%s => %s' %(keyword,text_modified))
