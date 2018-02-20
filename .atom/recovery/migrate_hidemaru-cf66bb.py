#!/usr/bin/python3
#coding:utf-8

import time
START=time.time()

import os
import sys
import argparse
import codecs
from collections import defaultdict
import copy
import json
from pprint import pprint
from prettyprint import pp
import re
import traceback

from tqdm import tqdm

from mymodule.basic import Basic
from mymodule.basic_super import BasicSuper
from mymodule import cnvk

CURRENT_DIRECTORY=os.path.dirname(os.path.abspath(__file__)) #自ファイルが存在するディレクトリ
SCRIPT_NAME=re.sub('.py.?','',os.path.basename(__file__)) #スクリプト名

class UnmatchError(Exception):
	pass

class MigrateHidemaru(BasicSuper):

	def __init__(self,*args, **kwargs):

		BasicSuper.__init__(self,script_name=SCRIPT_NAME)


	def load_text(self,path_text):

		data=[]
		already=[]
		with codecs.open(path_text,'r','utf-8') as f:

			for i,line in enumerate(f.readlines()):

				if i==0:
					continue

				cols=line.rstrip('\r\n').split('\t')

				# 1.fromの場合
				if cols[0]!=cols[1]:

					id_='%s=>%s' %(cols[1],cols[0])
					if id_ in already:
						continue


					data.append(
						{
							'correct':cols[0],
							'source':cols[1]
						}
					)

					already.append(id_)

				# 2.toの場合
				if cols[2]!=cols[3]:

					id_='%s=>%s' %(cols[3],cols[2])
					if id_ in already:
						continue


					data.append(
						{
							'correct':cols[2],
							'source':cols[3]
						}
					)

					already.append(id_)

		return data


	def load_nodes(self,path_text):

		with codecs.open(path_text,'r','utf-8') as f:
			lines=f.readlines()

			return lines

	def replace_by_hidemaru(self,text):

		text_source=text


		#英数字・記号・空白を全角に変換する
		text = cnvk.convert(text, cnvk.Z_ALPHA, cnvk.Z_NUM, cnvk.Z_KIGO, cnvk.Z_SPACE)

		text = re.compile(u"h;" ,re.I).sub( u"H:" ,text) #nocasesense
		text = re.compile(u"Ｈ；" ,re.I).sub( u"Ｈ：" ,text) #nocasesense
		text = re.compile(u"＝／" ,re.I).sub( u"／" ,text) #nocasesense
		text = re.compile(u"＝異常なし" ,re.I).sub( u"／正常" ,text) #nocasesense
		text = re.compile(u"＝正常" ,re.I).sub( u"／正常" ,text) #nocasesense
		text = re.compile(u"＝異常" ,re.I).sub( u"／異常" ,text) #nocasesense
		text = re.compile(u"＝上昇" ,re.I).sub( u"／上昇" ,text) #nocasesense
		text = re.compile(u"＝高値" ,re.I).sub( u"／高値" ,text) #nocasesense
		text = re.compile(u"＝陽性" ,re.I).sub( u"／陽性" ,text) #nocasesense
		text = re.compile(u"＝陰性" ,re.I).sub( u"／陰性" ,text) #nocasesense
		text = re.compile(u"＝低値" ,re.I).sub( u"／低値" ,text) #nocasesense
		text = re.compile(u"＝低下" ,re.I).sub( u"／低下" ,text) #nocasesense
		text = re.compile(u"／高値" ,re.I).sub( u"／上昇" ,text) #nocasesense
		text = re.compile(u"＝高値" ,re.I).sub( u"＝上昇" ,text) #nocasesense
		text = re.compile(u"／低値" ,re.I).sub( u"／低下" ,text) #nocasesense
		text = re.compile(u"＝低値" ,re.I).sub( u"＝低下" ,text) #nocasesense
		text = re.compile(u"】" ,re.I).sub( u"］" ,text) #nocasesense
		text = re.compile(u"【" ,re.I).sub( u"［" ,text) #nocasesense
		text = re.compile(u"〔" ,re.I).sub( u"［" ,text) #nocasesense
		text = re.compile(u"〕" ,re.I).sub( u"］" ,text) #nocasesense
		text = re.compile(u"＿*([＠＝／・：])＿*" ,re.I).sub( u"\\1" ,text) #nocasesense
		text = re.compile(u"^=-" ,re.I).sub( u"" ,text) #nocasesense
		text = re.compile(u"^血中＝" ,re.I).sub( u"" ,text) #nocasesense
		text = re.compile(u"^血液＝" ,re.I).sub( u"" ,text) #nocasesense
		text = re.compile(u"^血清＝" ,re.I).sub( u"" ,text) #nocasesense
		text = re.compile(u"^尿＝" ,re.I).sub( u"尿" ,text) #nocasesense
		text = re.compile(u"^正：" ,re.I).sub( u"\\1" ,text) #nocasesense
		text = re.compile(u"^解釈：" ,re.I).sub( u"\\1" ,text) #nocasesense



		#英数字・記号・空白を半角に変換する
		text = cnvk.convert(text, cnvk.H_ALPHA, cnvk.H_NUM, cnvk.H_KIGO, cnvk.H_SPACE)

		text = re.compile(u"(\\d)_+([^\\d])" ,re.I).sub(u"\\1\\2" ,text) #nocasesense
		text = re.compile(u"([A-Za-z])_+([^A-Za-z])",re.I).sub(u"\\1\\2" ,text) #nocasesense
		text = re.compile(u"^白血球数\/" ,re.I).sub(u"白血球/" ,text) #nocasesense
		text = re.compile(u"^wbc\/" ,re.I).sub(u"白血球/" ,text) #nocasesense
		text = re.compile(u"^plt\/" ,re.I).sub(u"血小板/" ,text) #nocasesense
		text = re.sub(u"血小板数\/" , u"血小板\/" ,text) #casesense
		text = re.sub(u"^rbc\/",u"赤血球/" ,text, flags=re.I) #nocasesense
		text = re.compile(u"^hb\/" ,re.I).sub(u"赤血球/" ,text) #nocasesense
		text = re.compile(u"^ht\/" ,re.I).sub(u"赤血球/" ,text) #nocasesense
		text = re.compile(u"^赤血球数\/" ,re.I).sub(u"赤血球/" ,text) #nocasesense
		text = re.compile(u"^got\/" ,re.I).sub(u"AST/" ,text) #nocasesense
		text = re.compile(u"^gpt\/" ,re.I).sub(u"ALT/" ,text) #nocasesense
		text = re.compile(u"^tp\/" ,re.I).sub(u"蛋白/" ,text) #nocasesense
		text = re.compile(u"^neutro\/" ,re.I).sub(u"好中球/" ,text) #nocasesense
		text = re.compile(u"^lymph\/" ,re.I).sub(u"リンパ球/" ,text) #nocasesense
		text = re.compile(u"AST\/ALT=" ,re.I).sub(u"AST\/ALT比=" ,text) #nocasesense
		text = re.sub(u"^K\/" , u"カリウム/" ,text) #casesense
		text = re.sub(u"^NA\/" , u"ナトリウム/" ,text) #casesense
		text = re.sub(u"^CPK\/" , u"CK/" ,text) #casesense
		text = re.sub(u"^P\/" , u"リン/" ,text) #casesense
		text = re.sub(u"^NH3\/" , u"アンモニア/" ,text) #casesense
		text = re.sub(u"^LD\/" , u"LDH/" ,text) #casesense
		text = re.sub(u"^Mg\/" , u"マグネシウム/" ,text) #casesense
		text = re.sub(u"^TG\/" , u"トリグリセライド/" ,text) #casesense
		text = re.compile(u"^hba1c\/",re.I).sub(u"HbA1c/" ,text) #nocasesense
		text = re.compile(u"T-Bil",re.I).sub(u"T-Bil" ,text) #nocasesense
		text = re.compile(u"TBil",re.I).sub(u"T-Bil" ,text) #nocasesense
		text = re.compile(u"T\.Bil",re.I).sub(u"T-Bil" ,text) #nocasesense
		text = re.sub(u"t-RNA" , u"tRNA" ,text) #casesense
		text = re.sub(u"m-RNA" , u"mRNA" ,text) #casesense
		text = re.compile(u"T_cell" ,re.I).sub( u"T-cell" ,text) #nocasesense
		text = re.compile(u"T-cell" ,re.I).sub( u"T-cell" ,text) #nocasesense
		text = re.compile(u"B_cell" ,re.I).sub( u"B-cell" ,text) #nocasesense
		text = re.compile(u"B-cell" ,re.I).sub( u"B-cell" ,text) #nocasesense
		text = re.sub(u"蛋白尿" , u"尿蛋白" ,text) #casesense
		text = re.sub(u"尿タンパク" , u"尿蛋白" ,text) #casesense
		text = re.sub(u"凝固能異常" , u"凝固障害" ,text) #casesense
		text = re.sub(u"結核症" , u"結核" ,text) #casesense
		text = re.sub(u"血管炎" , u"血管炎症候群" ,text) #casesense
		text = re.sub(u"胸部単純撮影" , u"胸部X線" ,text) #casesense
		text = re.sub(u"胸部単純レントゲン" , u"胸部X線" ,text) #casesense
		text = re.sub(u"胸部単純X線" , u"胸部X線" ,text) #casesense
		text = re.sub(u"胸部X線写真" , u"胸部X線" ,text) #casesense
		text = re.sub(u"胸部X線像" , u"胸部X線" ,text) #casesense
		text = re.sub(u"胸部画像" , u"胸部X線" ,text) #casesense
		text = re.sub(u"胸部正面単純写真" , u"胸部X線" ,text) #casesense
		text = re.sub(u"胸部レントゲン" , u"胸部X線" ,text) #casesense
		text = re.sub(u"胸部Xp" , u"胸部X線" ,text) #casesense
		text = re.sub(u"レントゲン写真" , u"胸部X線" ,text) #casesense
		text = re.sub(u"胸部X線写真" , u"胸部X線" ,text) #casesense
		text = re.sub(u"胸部単純写真" , u"胸部X線" ,text) #casesense
		text = re.sub(u"胸部単純X線" , u"胸部X線" ,text) #casesense
		text = re.sub(u"エックス線=" , u"X線=" ,text) #casesense
		text = re.sub(u"CT検査=" , u"CT=" ,text) #casesense
		text = re.sub(u"CT画像=" , u"CT=" ,text) #nocasesense
		text = re.sub(u"^レントゲン=" , u"X線=" ,text) #casesense
		text = re.compile(u"@膵臓$" ,re.I).sub( u"@膵" ,text) #nocasesense
		text = re.compile(u"@肝臓$" ,re.I).sub( u"@肝" ,text) #nocasesense
		text = re.compile(u"@腎臓$" ,re.I).sub( u"@腎" ,text) #nocasesense
		text = re.compile(u"@肺野$" ,re.I).sub( u"@肺" ,text) #nocasesense
		text = re.compile(u"=腹水貯留$" ,re.I).sub( u"腹水" ,text) #nocasesense
		text = re.compile(u"=胸水貯留$" ,re.I).sub( u"胸水" ,text) #nocasesense
		text = re.compile(u"超音波=" ,re.I).sub( u"エコー=" ,text) #nocasesense
		text = re.compile(u"スリガラス" ,re.I).sub( u"すりガラス" ,text) #nocasesense
		text = re.compile(u"すりがらす" ,re.I).sub( u"すりガラス" ,text) #nocasesense
		text = re.compile(u"すりガラス状(影|陰影)" ,re.I).sub( u"すりガラス\\1" ,text) #nocasesense
		text = re.compile(u"すりガラス様(影|陰影)" ,re.I).sub( u"すりガラス\\1" ,text) #nocasesense
		text = re.compile(u"すりガラス陰影" ,re.I).sub( u"すりガラス影" ,text) #nocasesense
		text = re.compile(u"すりガラス陰影" ,re.I).sub( u"すりガラス影" ,text) #nocasesense
		text = re.compile(u"単純(CT|MRI|エコー|エコー)=" ,re.I).sub( u"\\1=" ,text) #nocasesense
		text = re.compile(u"(腫瘤|粒状|網状)陰影@" ,re.I).sub( u"\\1影@" ,text) #nocasesense
		text = re.compile(u"(CT|MRI|エコー|エコー)=([^@]*)(腫瘤|結節)@" ,re.I).sub( u"\\1=\\2\\3影@" ,text) #nocasesense
		text = re.compile(u"(CT|MRI|エコー|エコー)=([^@]*)(腫瘍)@" ,re.I).sub( u"\\1=\\2腫瘤影@" ,text) #nocasesense
		text = re.compile(u"胸腹*部(CT|MRI|エコー|エコー)=(すりガラス影|腫瘤影|粒状影|網状影)$" ,re.I).sub( u"\\1=\\2@肺" ,text) #nocasesense
		text = re.compile(u"胸腹*部造影(CT|MRI|エコー|エコー)=(すりガラス影|腫瘤影|粒状影|網状影)$" ,re.I).sub( u"造影\\1=\\2@肺" ,text) #nocasesense
		text = re.compile(u"び漫性" ,re.I).sub( u"びまん性" ,text) #nocasesense

		pattern = re.compile(u"(.*?)腫大@(両側|両)*(びまん性)*(膵|下垂体|甲状腺|副腎|副甲状腺|腎|下垂体茎|糸球体|膵頭部|膵尾部|肝|顎下腺|手指|唾液腺|扁桃|胆嚢|臓器|糸球体)$" ,re.I)
		regx = pattern.findall(text)
		if len(regx)>0:
			text = u"%s%s%s%s腫大" %(regx[0][0],regx[0][1],regx[0][2],regx[0][3])


		pattern = re.compile(u"(.*?)腫大/陰性@(両側|両)*(びまん性)*(膵|下垂体|甲状腺|副腎|副甲状腺|腎|下垂体茎|糸球体|膵頭部|膵尾部|肝|顎下腺|手指|唾液腺|扁桃|胆嚢|臓器|糸球体)$",re.I)
		regx = pattern.findall(text)
		if len(regx)>0:
			text = u"%s%s%s%s腫大/陰性" %(regx[0][0],regx[0][1],regx[0][2],regx[0][3])


		pattern = re.compile(u"(.*?)(膵|下垂体|甲状腺|副腎|副甲状腺|腎|下垂体茎|糸球体|膵頭部|膵尾部|肝|顎下腺|手指|唾液腺|扁桃)(びまん性)腫大$" ,re.I) #nocasesense
		regx = pattern.findall(text)
		if len(regx)>0:
			text = u"%s%s%s腫大" %(regx[0][0],regx[0][2],regx[0][1])
			# .sub( u"\\2\\1腫大" ,text)


		pattern = re.compile(u"(.*?)胸*腹部(CT|MRI|エコー|エコー)=([^@]*)@(膵臓|副腎|肝|腹腔内|腎)$" ,re.I)
		regx = pattern.findall(text)
		if len(regx)>0:
			text = u"%s%s=%s@%s" %(regx[0][0],regx[0][1],regx[0][2],regx[0][3])
			# .sub( u"\\1=\\2@\\3" ,text) #nocasesense


		pattern = re.compile(u"(.*?)胸*腹部造影(CT|MRI|エコー|エコー)=([^@]*)@(膵臓|副腎|肝|腹腔内|腎)$" ,re.I)
		regx = pattern.findall(text)
		if len(regx)>0:
			text = u"%s造影%s=%s@%s" %(regx[0][0],regx[0][1],regx[0][2],regx[0][3])
			# .sub( u"造影\\1=\\2@\\3" ,text) #nocasesense


		pattern = re.compile(u"(.*?)胸腹*部(CT|MRI|エコー|エコー)=([^@]*)@(肺|縦隔|肺門)$" ,re.I)
		regx = pattern.findall(text)
		if len(regx)>0:
			text = u"%s%s=%s@%s" %(regx[0][0],regx[0][1],regx[0][2],regx[0][3])
			# .sub( u"\\1=\\2@\\3" ,text) #nocasesense


		pattern = re.compile(u"(.*?)胸腹*部造影(CT|MRI|エコー|エコー)=([^@]*)@(肺|縦隔|肺門)$" ,re.I)
		regx = pattern.findall(text)
		if len(regx)>0:
			text = u"%s造影%s=%s@%s" %(regx[0][0],regx[0][1],regx[0][2],regx[0][3])
			# .sub( u"造影\\1=\\2@\\3" ,text) #nocasesense


		pattern = re.compile(u"(.*?)胸腹*部(CT|MRI|エコー|エコー)=(胸水|胸膜肥厚)$" ,re.I)
		regx = pattern.findall(text)
		if len(regx)>0:
			text = u"%s%s=%s" %(regx[0][0],regx[0][1],regx[0][2])
			# .sub( u"\\1=\\2" ,text) #nocasesense


		pattern = re.compile(u"(.*?)胸腹*部造影(CT|MRI|エコー|エコー)=(胸水|胸膜肥厚)$" ,re.I)
		regx = pattern.findall(text)
		if len(regx)>0:
			text = u"%s造影%s=%s" %(regx[0][0],regx[0][1],regx[0][2])
			# .sub( u"造影\\1=\\2" ,text) #nocasesense


		pattern = re.compile(u"(.*?)胸*腹部(CT|MRI|エコー|エコー)=(腹水|肝脾腫|脾腫|脂肪肝|水腎症|膵腫大|副腎腫大|肝腫大)$" ,re.I)
		regx = pattern.findall(text)
		if len(regx)>0:
			text = u"%s%s=%s" %(regx[0][0],regx[0][1],regx[0][2])
			# .sub( u"\\1=\\2" ,text) #nocasesense


		pattern = re.compile(u"(.*?)胸*腹部造影(CT|MRI|エコー|エコー)=(腹水|肝脾腫|脾腫|脂肪肝|水腎症|膵腫大|副腎腫大|肝腫大)$" ,re.I)
		regx = pattern.findall(text)
		if len(regx)>0:
			text = u"%s造影%s=%s" %(regx[0][0],regx[0][1],regx[0][2])
			# .sub( u"造影\\1=\\2" ,text) #nocasesense


		pattern = re.compile(u"(.*?)頭部(CT|MRI|エコー|エコー)=(下垂体腫大|下垂体茎腫大)$" ,re.I)
		regx = pattern.findall(text)
		if len(regx)>0:
			text = u"%s%s=%s" %(regx[0][0],regx[0][1],regx[0][2])
			# .sub( u"\\1=\\2" ,text) #nocasesense


		pattern = re.compile(u"(.*?)頭部造影(CT|MRI|エコー|エコー)=(下垂体腫大|下垂体茎腫大)$" ,re.I)
		regx = pattern.findall(text)
		if len(regx)>0:
			text = u"%s造影%s=%s" %(regx[0][0],regx[0][1],regx[0][2])
			# .sub( u"造影\\1=\\2" ,text) #nocasesense

		text = re.compile(u"=腫大\/陰性@(甲状腺)" ,re.I).sub( u"\\1腫大\/陰性" ,text) #nocasesense
		text = re.sub(u"病理診断\=" , u"病理\=" ,text) #casesense
		text = re.sub(u"病理検査\=" , u"病理\=" ,text) #casesense
		text = re.sub(u"病理所見\=" , u"病理\=" ,text) #casesense
		text = re.sub(u"病理組織\=" , u"病理\=" ,text) #casesense
		text = re.sub(u"病理組織検査\=" , u"病理\=" ,text) #casesense
		text = re.sub(u"培養検査\=" , u"培養\=" ,text) #casesense
		text = re.sub(u"腎病理所見\=" , u"腎生検\=" ,text) #casesense
		text = re.sub(u"^髄液検査\\=" , u"髄液\=" ,text) #casesense
		text = re.sub(u"^脳脊髄液\\=" , u"髄液\=" ,text) #casesense
		text = re.sub(u"^腰椎穿刺\\=" , u"髄液\=" ,text) #casesense
		text = re.sub(u"^脳脊髄液検査\\=" , u"髄液\=" ,text) #casesense
		text = re.sub(u"骨髄穿刺\=" , u"骨髄\=" ,text) #casesense
		text = re.sub(u"骨髄検査\=" , u"骨髄\=" ,text) #casesense
		text = re.sub(u"骨髄生検\=" , u"骨髄\=" ,text) #casesense
		text = re.sub(u"髄液検査" , u"髄液\=" ,text) #casesense
		text = re.sub(u"内視鏡検査\=" , u"内視鏡\=" ,text) #casesense
		text = re.sub(u"超音波\=" , u"エコー\=" ,text) #casesense
		text = re.sub(u"胸部CT検査" , u"胸部CT" ,text) #casesense
		text = re.sub(u"心臓超音波検査" , u"心エコー" ,text) #casesense
		text = re.sub(u"UCG" , u"心エコー" ,text) #casesense
		text = re.sub(u"心エコー検査" , u"心エコー" ,text) #casesense
		text = re.sub(u"心エコー図" , u"心エコー" ,text) #casesense
		text = re.sub(u"心臓超音波" , u"心エコー" ,text) #casesense
		text = re.sub(u"経胸壁心エコー" , u"心エコー" ,text) #casesense
		text = re.sub(u"Ferritin" , u"フェリチン" ,text) #casesense
		text = re.sub(u"Basedow病" , u"バセドウ病" ,text) #casesense
		text = re.sub(u"冠動脈造影検査" , u"冠動脈造影" ,text) #casesense
		text = re.sub(u"CAG" , u"冠動脈造影" ,text) #casesense
		text = re.sub(u"歩行障害" , u"歩行困難" ,text) #casesense
		text = re.sub(u"痺れ" , u"しびれ" ,text) #casesense
		text = re.sub(u"しびれ感" , u"しびれ" ,text) #casesense
		text = re.sub(u"腎障害" , u"腎機能障害" ,text) #casesense
		text = re.sub(u"抗生剤" , u"抗菌薬" ,text) #casesense
		text = re.sub(u"cortisol" , u"コルチゾール" ,text) #casesense
		text = re.sub(u"aPTT" , u"APTT" ,text) #casesense
		text = re.sub(u"肝機能異常" , u"肝機能障害" ,text) #casesense
		text = re.sub(u"肝機能異常" , u"肝障害" ,text) #casesense
		text = re.sub(u"頚部" , u"頸部" ,text) #casesense
		text = re.sub(u"可溶性IL-2R" , u" 可溶性IL-2レセプター " ,text) #casesense
		text = re.sub(u"食思不振" , u"食欲不振" ,text) #casesense
		text = re.sub(u"肝障害" , u"肝機能障害" ,text) #casesense
		text = re.sub(u"食欲不振" , u"食欲低下" ,text) #casesense
		text = re.sub(u"食思不振" , u"食欲低下" ,text) #casesense
		text = re.sub(u"息切れ" , u"呼吸困難" ,text) #casesense
		text = re.sub(u"呼吸苦" , u"呼吸困難" ,text) #casesense
		text = re.sub(u"呼吸困難感" , u"呼吸困難" ,text) #casesense
		text = re.sub(u"呼吸苦" , u"息切れ" ,text) #casesense
		text = re.sub(u"意識混濁" , u"意識障害" ,text) #casesense
		text = re.sub(u"意識消失" , u"意識障害" ,text) #casesense
		text = re.sub(u"全身倦怠感" , u"倦怠感" ,text) #casesense
		text = re.sub(u"易疲労感" , u"倦怠感" ,text) #casesense
		text = re.sub(u"ナトリウム" ,u"Na" ,text) #casesense
		text = re.sub(u"カルシウム" ,u"Ca" ,text) #casesense
		text = re.sub(u"カリウム" ,u"K" ,text) #casesense
		text = re.sub(u"クロール" ,u"Cl" ,text) #casesense
		text = re.sub(u"アンモニア" ,u"NH3" ,text) #casesense
		text = re.sub(u"炭酸ガス" ,u"CO2" ,text) #casesense
		text = re.sub(u"プロラクチン" ,u"PRL" ,text) #casesense
		text = re.sub(u"マグネシウム" ,u"Mg" ,text) #casesense
		text = re.sub(u"トリグリセライド" ,u"TG" ,text) #casesense
		text = re.sub(u"トリグリセリド" ,u"TG" ,text) #casesense
		text = re.sub(u"プロラクチン" ,u"PRL" ,text) #casesense
		text = re.sub(u"ホモシスティン" ,u"ホモシスチン" ,text) #casesense
		text = re.compile(u"感染$" ,re.I).sub( u"感染症" ,text) #nocasesense
		text = re.compile(u"^QT延長$" ,re.I).sub( u"QT延長症候群" ,text) #nocasesense
		text = re.compile(u"^インフルエンザ$" ,re.I).sub( u"インフルエンザウイルス感染症" ,text) #nocasesense
		text = re.compile(u"^サイトメガロウイルス$" ,re.I).sub( u"サイトメガロウイルス感染症" ,text) #nocasesense
		text = re.compile(u"^サイトメガロ感染症$" ,re.I).sub( u"サイトメガロウイルス感染症" ,text) #nocasesense
		text = re.compile(u"^横紋筋融解$" ,re.I).sub( u"横紋筋融解症" ,text) #nocasesense
		text = re.compile(u"クモ膜" ,re.I).sub( u"くも膜" ,text) #nocasesense
		text = re.compile(u"欠乏$" ,re.I).sub( u"欠乏症" ,text) #nocasesense
		text = re.compile(u"ベーチェット$" ,re.I).sub( u"ベーチェット病" ,text) #nocasesense
		text = re.compile(u"悪性高血圧$" ,re.I).sub( u"悪性高血圧症" ,text) #nocasesense
		text = re.compile(u"脂質異常$" ,re.I).sub( u"脂質異常症" ,text) #nocasesense
		text = re.compile(u"^可逆性後頭葉白質脳症$" ,re.I).sub( u"可逆性後部白質脳症症候群" ,text) #nocasesense
		text = re.compile(u"^過換気$" ,re.I).sub( u"過換気症候群" ,text) #nocasesense
		text = re.compile(u"^冠攣縮$" ,re.I).sub( u"冠動脈攣縮" ,text) #nocasesense
		text = re.compile(u"^感染$" ,re.I).sub( u"感染症" ,text) #nocasesense
		text = re.compile(u"^肝硬変症$" ,re.I).sub( u"肝硬変" ,text) #nocasesense
		text = re.compile(u"^偽膜性大腸炎$" ,re.I).sub( u"偽膜性腸炎" ,text) #nocasesense
		text = re.compile(u"^急性腎不全$" ,re.I).sub( u"急性腎機能障害" ,text) #nocasesense
		text = re.compile(u"^慢性腎不全$" ,re.I).sub( u"慢性腎臓病" ,text) #nocasesense
		text = re.compile(u"B細胞性リンパ腫" ,re.I).sub( u"B細胞リンパ腫" ,text) #nocasesense
		text = re.compile(u"ブドウ膜炎" ,re.I).sub( u"ぶどう膜炎" ,text) #nocasesense
		text = re.compile(u"^ショックバイタル$" ,re.I).sub( u"ショック" ,text) #nocasesense
		text = re.compile(u"^自己免疫性多内分泌腺症候群$" ,re.I).sub( u"多腺性自己免疫症候群" ,text) #nocasesense
		text = re.compile(u"^血栓性微小血管症$" ,re.I).sub( u"血栓性微小血管障害症" ,text) #nocasesense
		text = re.compile(u"^血栓性微小血管障害$" ,re.I).sub( u"血栓性微小血管障害症" ,text) #nocasesense
		text = re.compile(u"^顕微鏡的多発性血管炎$" ,re.I).sub( u"顕微鏡的多発血管炎" ,text) #nocasesense
		text = re.compile(u"^心停止$" ,re.I).sub( u"心肺停止" ,text) #nocasesense
		text = re.compile(u"^伝染性単核症$" ,re.I).sub( u"伝染性単核球症" ,text) #nocasesense
		text = re.compile(u"型肝炎ウイルス感染$" ,re.I).sub( u"型肝炎" ,text) #nocasesense
		text = re.compile(u"型肝炎ウイルス再活性化$" ,re.I).sub( u"型肝炎再活性化" ,text) #nocasesense
		text = re.compile(u"^アナフィラクトイド紫斑$" ,re.I).sub( u"アナフィラクトイド紫斑病" ,text) #nocasesense
		text = re.compile(u"^(原発性胆汁性肝硬変|水中毒|僧帽弁閉鎖不全)症$" ,re.I).sub( u"\\1" ,text) #nocasesense
		text = re.compile(u"^好酸球増多症$" ,re.I).sub( u"好酸球増多症候群" ,text) #nocasesense
		text = re.compile(u"^甲状腺機能低下$" ,re.I).sub( u"甲状腺機能低下症" ,text) #nocasesense
		text = re.compile(u"^甲状腺機能亢進$" ,re.I).sub( u"甲状腺機能亢進症" ,text) #nocasesense
		text = re.compile(u"^(心室中隔欠損)$" ,re.I).sub( u"\\1症" ,text) #nocasesense
		text = re.compile(u"^(心房中隔欠損|腎血管性高血圧|脱水|脳塞栓|肺高血圧|肺塞栓|汎下垂体機能低下|非閉塞性腸管虚血|副腎機能低下|副腎皮質機能低下|甲状腺機能低下|甲状腺機能亢進)$" ,re.I).sub( u"\\1症" ,text) #nocasesense
		text = re.compile(u"^(播種性血管内凝固)$" ,re.I).sub( u"\\1症候群" ,text) #nocasesense
		text = re.compile(u"^敗血症ショック$" ,re.I).sub( u"敗血症性ショック" ,text) #nocasesense
		text = re.compile(u"薬物性" ,re.I).sub( u"薬剤性" ,text) #nocasesense
		text = re.compile(u"薬物性" ,re.I).sub( u"薬剤性" ,text) #nocasesense
		text = re.compile(u"^高血糖性高浸透圧症候群$" ,re.I).sub( u"高血糖高浸透圧症候群" ,text) #nocasesense
		text = re.compile(u"^高浸透圧高血糖症候群$" ,re.I).sub( u"高血糖高浸透圧症候群" ,text) #nocasesense
		text = re.compile(u"^薬剤過敏症症候群$" ,re.I).sub( u"薬剤性過敏症症候群" ,text) #nocasesense
		text = re.compile(u"^薬剤性肝炎$" ,re.I).sub( u"薬剤性肝機能障害" ,text) #nocasesense
		text = re.compile(u"^輸血後急性肺障害$" ,re.I).sub( u"輸血関連急性肺障害" ,text) #nocasesense
		text = re.compile(u"^溶血性尿毒症性症候群$" ,re.I).sub( u"溶血性尿毒症症候群" ,text) #nocasesense
		text = re.compile(u"^たこつぼ心筋症$" ,re.I).sub( u"たこつぼ型心筋症" ,text) #nocasesense
		text = re.compile(u"^赤芽球癆$" ,re.I).sub( u"赤芽球ろう" ,text) #nocasesense
		text = re.compile(u"^耐糖能悪化$" ,re.I).sub( u"耐糖能異常" ,text) #nocasesense
		text = re.compile(u"^蛋白漏出胃腸症$" ,re.I).sub( u"蛋白漏出性胃腸症" ,text) #nocasesense
		text = re.compile(u"^痛風発作$" ,re.I).sub( u"痛風" ,text) #nocasesense
		text = re.compile(u"^続発性副腎不全$" ,re.I).sub( u"続発性副腎皮質機能低下症" ,text) #nocasesense
		text = re.compile(u"(高|低)Ca(血症|症|尿症|症候群)" ,re.I).sub( u"\\1カルシウム\\2" ,text) #nocasesense
		text = re.sub(u"(高|低)K(血症|症|尿症|症候群)" , u"\\1カリウム\\2" ,text) #casesense
		text = re.compile(u"(高|低)NA(血症|症|尿症|症候群)",re.I).sub(u"\\1ナトリウム\\2" ,text) #nocasesense
		text = re.sub(u"(高|低)CPK(血症|症|尿症|症候群)" , u"\\1CK\\2" ,text) #casesense
		text = re.sub(u"(高|低)P(血症|症|尿症|症候群)" , u"\\1リン\\2" ,text) #casesense
		text = re.sub(u"(高|低)IP(血症|症|尿症|症候群)" , u"\\1リン\\2" ,text) #casesense
		text = re.sub(u"(高|低)NH3(血症|症|尿症|症候群)" , u"\\1アンモニア\\2" ,text) #casesense
		text = re.sub(u"(高|低)LD(血症|症|尿症|症候群)" , u"\\1LDH\\2" ,text) #casesense
		text = re.sub(u"(高|低)Mg(血症|症|尿症|症候群)" , u"\\1マグネシウム\\2" ,text) #casesense
		text = re.sub(u"(高|低)TG(血症|症|尿症|症候群)" , u"\\1トリグリセライド\\2" ,text) #casesense
		text = re.sub(u"(高|低)CPK(血症|症|尿症|症候群)" , u"\\1CK\\2" ,text) #casesense
		text = re.sub(u"(高|低)HDL-C(血症|症|尿症|症候群)" , u"\\1HDLコレステロール\\2" ,text) #casesense
		text = re.sub(u"(高|低)HDL(血症|症|尿症|症候群)" , u"\\1HDLコレステロール\\2" ,text) #casesense
		text = re.sub(u"(高|低)LDL(血症|症|尿症|症候群)" , u"\\1LDLコレステロール\\2" ,text) #casesense
		text = re.sub(u"(高|低)LDL-C(血症|症|尿症|症候群)" , u"\\1LDLコレステロール\\2" ,text) #casesense
		text = re.sub(u"(高|低)CO2(血症|症|尿症|症候群)" , u"\\1二酸化炭素\\2" ,text) #casesense
		text = re.sub(u"(高|低)PRL(血症|症|尿症|症候群)" , u"\\1プロラクチン\\2" ,text) #casesense
		text = re.sub(u"(高|低)Cl(血症|症|尿症|症候群)" , u"\\1クロール\\2" ,text) #casesense
		text = re.sub(u"ガンマ" , u"γ" ,text) #casesense
		text = re.sub(u"アルファ" , u"α" ,text) #casesense
		text = re.sub(u"ベータ" , u"β" ,text) #casesense
		text = re.sub(u"イプシロン" , u"ε" ,text) #casesense
		text = re.sub(u"デルタ" , u"δ" ,text) #casesense
		text = re.sub(u"γ-" , u"γ" ,text) #casesense
		text = re.sub(u"α-" , u"α" ,text) #casesense
		text = re.sub(u"β-" , u"β" ,text) #casesense
		text = re.sub(u"ε-" , u"ε" ,text) #casesense
		text = re.sub(u"δ-" , u"δ" ,text) #casesense
		text = re.sub(u"γ-グロブリン" , u"γグロブリン" ,text) #casesense
		text = re.sub(u"HDL-コレステロール" , u"HDLコレステロール" ,text) #casesense
		text = re.sub(u"Lupus腎炎" , u"ループス腎炎" ,text) #casesense
		text = re.sub(u"γ-GTP" , u"γGTP" ,text) #casesense
		text = re.sub(u"([A-Za-z]+)" , u"↑\\1↑" ,text)  #nocasesense
		text = re.compile(u"↑cre↑", re.I).sub(u"クレアチニン",text)
		text = re.compile(u"↑cr↑" ,re.I).sub(u"クレアチニン" ,text) #nocasesense
		text = re.sub(u"血清↑Cr↑" , u"クレアチニン" ,text) #casesense
		text = re.sub(u"↑S↑-↑Cr↑" , u"クレアチニン" ,text) #casesense
		text = re.sub(u"↑P↑-↑ANCA↑" , u"MPO-ANCA" ,text) #casesense
		text = re.compile(u"↑IV型↑" ,re.I).sub( u"4型" ,text) #nocasesense
		text = re.compile(u"↑III型↑" ,re.I).sub( u"3型" ,text) #nocasesense
		text = re.compile(u"↑II型↑" ,re.I).sub( u"2型" ,text) #nocasesense
		text = re.compile(u"↑I型↑" ,re.I).sub( u"1型" ,text) #nocasesense
		text = re.compile(u"^(\d型)自己免疫性多内分泌腺症候群$" ,re.I).sub( u"多腺性自己免疫症候群\\1" ,text) #nocasesense
		text = re.compile(u"↑Alb↑" ,re.I).sub( u"↑ALB↑" ,text) #nocasesense
		text = re.sub(u"↑Xp↑" , u"X線" ,text) #casesense
		text = re.sub(u"↑ANA↑" , u"抗核抗体" ,text) #casesense
		text = re.sub(u"↑UN↑" , u"BUN" ,text) #casesense
		text = re.sub(u"尿素窒素" , u"BUN" ,text) #casesense
		text = re.sub(u"↑BP↑" , u"血圧" ,text) #casesense
		text = re.sub(u"↑EBV↑" , u"EBウイルス" ,text) #casesense
		text = re.sub(u"↑GCSF↑" , u"G-CSF" ,text) #casesense
		text = re.sub(u"↑EBV↑" , u"EBウイルス" ,text) #casesense
		text = re.sub(u"↑HBV↑" , u"B型肝炎ウイルス" ,text) #casesense
		text = re.sub(u"↑HCV↑" , u"C型肝炎ウイルス" ,text) #casesense
		text = re.sub(u"↑HHV-6↑" , u"ヒトヘルペスウイルス6型" ,text) #casesense
		text = re.sub(u"↑MTX↑" , u"メトトレキサート" ,text) #casesense
		text = re.sub(u"↑MINO↑" , u"ミノマイシン" ,text) #casesense
		text = re.sub(u"↑ACS↑" ,u"急性冠症候群" ,text) #casesense
		text = re.sub(u"↑HUS↑" ,u"溶血性尿毒素症候群" ,text) #casesense
		text = re.sub(u"↑AIH↑" ,u"自己免疫性肝炎" ,text) #casesense
		text = re.sub(u"↑AIHA↑" ,u"自己免疫性溶血性貧血" ,text) #casesense
		text = re.sub(u"↑AKI↑" ,u"急性腎障害" ,text) #casesense
		text = re.sub(u"↑ALL↑" ,u"急性リンパ性白血病" ,text) #casesense
		text = re.sub(u"↑AMI↑" ,u"急性心筋梗塞" ,text) #casesense
		text = re.sub(u"↑AML↑" ,u"急性骨髄性白血病" ,text) #casesense
		text = re.sub(u"↑APL↑" ,u"急性前骨髄球性白血病" ,text) #casesense
		text = re.sub(u"↑APS↑" ,u"多腺性自己免疫症候群" ,text) #casesense
		text = re.sub(u"↑ARDS↑" ,u"成人呼吸窮迫症候群" ,text) #casesense
		text = re.sub(u"↑CADM↑" ,u"clinically_amyopathic_dermatomyositis" ,text) #casesense
		text = re.sub(u"↑CGM↑" ,u"持続血糖測定モニター" ,text) #casesense
		text = re.sub(u"↑CKD↑" ,u"慢性腎臓病" ,text) #casesense
		text = re.sub(u"↑CLL↑" ,u"慢性リンパ性白血病" ,text) #casesense
		text = re.sub(u"↑CML↑" ,u"慢性骨髄性白血病" ,text) #casesense
		text = re.sub(u"↑CMV↑" ,u"サイトメガロウイルス" ,text) #casesense
		text = re.sub(u"↑COPD↑" ,u"慢性閉塞性肺疾患" ,text) #casesense
		text = re.sub(u"↑HCC↑" ,u"肝細胞癌" ,text) #casesense
		text = re.sub(u"↑CTEPH↑" ,u"慢性血栓塞栓性肺高血圧症" ,text) #casesense
		text = re.sub(u"↑DKA↑" ,u"糖尿病性ケトアシドーシス" ,text) #casesense
		text = re.sub(u"↑DLBCL↑" ,u"びまん性大細胞性B細胞性リンパ腫" ,text) #casesense
		text = re.sub(u"↑DVT↑" ,u"深部静脈血栓症" ,text) #casesense
		text = re.sub(u"↑EGPA↑" ,u"好酸球性多発血管炎肉芽腫症" ,text) #casesense
		text = re.sub(u"↑ERCP↑" ,u"内視鏡的逆行性膵胆管造影" ,text) #casesense
		text = re.sub(u"↑GERD↑" ,u"胃食道逆流症" ,text) #casesense
		text = re.sub(u"↑GIST↑" ,u"消化管間質腫瘍" ,text) #casesense
		text = re.sub(u"↑GVHD↑" ,u"慢性移植片対宿主病" ,text) #casesense
		text = re.sub(u"↑HCC↑" ,u"肝細胞癌" ,text) #casesense
		text = re.sub(u"↑HES↑" ,u"特発性好酸球増多症候群" ,text) #casesense
		text = re.sub(u"↑HHS↑" ,u"高浸透圧高血糖症候群" ,text) #casesense
		text = re.sub(u"↑HSP↑" ,u"ヘノッホ・シェーンライン紫斑病" ,text) #casesense
		text = re.sub(u"↑HUS↑" ,u"溶血性尿毒素症候群" ,text) #casesense
		text = re.sub(u"↑ITP↑" ,u"免疫性血小板減少症" ,text) #casesense
		text = re.sub(u"↑LCDD↑" ,u"免疫グロブリンＬ鎖沈着症" ,text) #casesense
		text = re.sub(u"↑MCTD↑" ,u"混合性結合組織病" ,text) #casesense
		text = re.sub(u"↑MDS↑" ,u"骨髄異形成症候群" ,text) #casesense
		text = re.sub(u"↑MELAS↑" ,u"ミトコンドリア病" ,text) #casesense
		text = re.sub(u"↑MRHE↑" ,u"鉱質コルチコイド反応性低ナトリウム血症" ,text) #casesense
		text = re.sub(u"↑NASH↑" ,u"非アルコール性脂肪性肝炎" ,text) #casesense
		text = re.sub(u"↑NOMI↑" ,u"非閉塞性腸管虚血症" ,text) #casesense
		text = re.sub(u"↑NPPV↑" ,u"非侵襲的陽圧換気療法" ,text) #casesense
		text = re.sub(u"↑PBC↑" ,u"原発性胆汁性肝硬変症" ,text) #casesense
		text = re.sub(u"↑PEA↑" ,u"無脈性電気活動" ,text) #casesense
		text = re.sub(u"↑PRES↑" ,u"可逆性白質脳症" ,text) #casesense
		text = re.sub(u"↑PSC↑" ,u"原発性硬化性胆管炎" ,text) #casesense
		text = re.sub(u"↑RPGN↑" ,u"急速進行性糸球体腎炎" ,text) #casesense
		text = re.sub(u"↑RS3PE↑" ,u"Remitting_Seronegative_Symmetrical_Synovitis_with_Pitting_Edema" ,text) #casesense
		text = re.sub(u"↑RTA↑" ,u"尿細管性アシドーシス" ,text) #casesense
		text = re.sub(u"↑SAS↑" ,u"睡眠時無呼吸症候群_" ,text) #casesense
		text = re.sub(u"↑SIRS↑" ,u"全身性炎症反応症候群" ,text) #casesense
		text = re.sub(u"↑SPIDDM↑" ,u"緩徐進行1型糖尿病" ,text) #casesense
		text = re.sub(u"↑SVR↑" ,u"ウイルス学的著効" ,text) #casesense
		text = re.sub(u"↑TACE↑" ,u"肝動脈塞栓術" ,text) #casesense
		text = re.sub(u"↑TMA↑" ,u"血栓性微小血管障害症" ,text) #casesense
		text = re.sub(u"↑TRALI↑" ,u"輸血後急性肺障害" ,text) #casesense
		text = re.sub(u"↑TTP↑" ,u"難治性血栓性血小板減少性紫斑病" ,text) #casesense
		text = re.sub(u"↑UIP↑" ,u"通常型間質性肺炎" ,text) #casesense
		text = re.sub(u"^↑GAD↑抗体" , u"抗GAD抗体" ,text) #casesense
		text = re.sub(u"超音波検査" , u"エコー" ,text) #casesense
		text = re.sub(u"↑US↑" , u"エコー" ,text) #casesense
		text = re.sub(u"↑DIC↑" , u"播種性血管内凝固症候群" ,text) #casesense
		text = re.sub(u"↑SLE↑" , u"全身性エリテマトーデス" ,text) #casesense
		text = re.sub(u"↑SIADH↑" , u"抗利尿ホルモン不適合分泌症候群" ,text) #casesense
		text = re.sub(u"↑AIDS↑" , u"後天性免疫不全症候群" ,text) #casesense
		text = re.compile(u"↑" ,re.I).sub( u"" ,text)  #nocasesense



		#英数字・記号・空白を全角に変換する
		text = cnvk.convert(text, cnvk.Z_ALPHA, cnvk.Z_NUM, cnvk.Z_KIGO, cnvk.Z_SPACE)
		text = text.replace(u'￥','') #追加


		text = re.compile(u"ＡＦＰ／高値" ,re.I).sub( u"ＡＦＰ／上昇" ,text) #nocasesense
		text = re.compile(u"ＡＮＡ／上昇" ,re.I).sub( u"ＡＮＡ／陽性" ,text) #nocasesense
		text = re.compile(u"ＣＲＰ／高値" ,re.I).sub( u"ＣＲＰ／上昇" ,text) #nocasesense
		text = re.compile(u"炎症／上昇" ,re.I).sub( u"炎症反応／上昇" ,text) #nocasesense
		text = re.compile(u"炎症所見／陰性" ,re.I).sub( u"炎症反応／陰性" ,text) #nocasesense
		text = re.compile(u"炎症所見／上昇" ,re.I).sub( u"炎症反応／上昇" ,text) #nocasesense
		text = re.compile(u"炎症反応／陽性" ,re.I).sub( u"炎症反応／上昇" ,text) #nocasesense
		text = re.compile(u"炎症反応／上昇" ,re.I).sub( u"ＣＲＰ／上昇" ,text) #nocasesense
		text = re.compile(u"Ｃ‐ペプチド／低下" ,re.I).sub( u"Ｃペプチド／低下" ,text) #nocasesense
		text = re.compile(u"Ｄ[‐−]ダイマ‐／上昇" ,re.I).sub( u"Ｄダイマー／上昇" ,text) #nocasesense
		text = re.compile(u"ＦＧＦ‐２３／上昇" ,re.I).sub( u"ＦＧＦ２３／上昇" ,text) #nocasesense
		text = re.compile(u"Ｆ‐Ｔ３／上昇" ,re.I).sub( u"ＦＴ３／上昇" ,text) #nocasesense
		text = re.compile(u"Ｆ‐Ｔ４／上昇" ,re.I).sub( u"ＦＴ４／上昇" ,text) #nocasesense
		text = re.compile(u"Ｆ‐Ｔ４／低下" ,re.I).sub( u"ＦＴ４／低下" ,text) #nocasesense
		text = re.compile(u"ＨｂＡ１ｃ／高値" ,re.I).sub( u"ＨｂＡ１ｃ／上昇" ,text) #nocasesense
		text = re.compile(u"ＨＢｓ‐Ａｂ／陰性" ,re.I).sub( u"ＨＢｓ抗体／陰性" ,text) #nocasesense
		text = re.compile(u"ＨＢｓ‐Ａｇ／陽性" ,re.I).sub( u"ＨＢｓ抗原／陽性" ,text) #nocasesense
		text = re.compile(u"ＨＣＯ３／低下" ,re.I).sub( u"ＨＣＯ３‐／低下" ,text) #nocasesense
		text = re.compile(u"ＨＣＶＡｂ／陰性" ,re.I).sub( u"ＨＣＶ抗体／陰性" ,text) #nocasesense
		text = re.compile(u"ＨＣＶ‐Ａｂ／陰性" ,re.I).sub( u"ＨＣＶ抗体／陰性" ,text) #nocasesense
		text = re.compile(u"ＨＤＬ‐Ｃ／低下" ,re.I).sub( u"ＨＤＬ／低下" ,text) #nocasesense
		text = re.compile(u"ＩＧＦ‐１／上昇" ,re.I).sub( u"ＩＧＦ‐Ｉ／上昇" ,text) #nocasesense
		text = re.compile(u"ＩＧＦ‐１／低下" ,re.I).sub( u"ＩＧＦ‐Ｉ／低下" ,text) #nocasesense
		text = re.compile(u"ｉｎｔａｃｔ＿ＰＴＨ／上昇" ,re.I).sub( u"ｉｎｔａｃｔＰＴＨ／上昇" ,text) #nocasesense
		text = re.compile(u"ｉｎｔａｃｔ＿ＰＴＨ／正常" ,re.I).sub( u"ｉｎｔａｃｔＰＴＨ／正常" ,text) #nocasesense
		text = re.compile(u"ｉｎｔａｃｔ＿ＰＴＨ／低下" ,re.I).sub( u"ｉｎｔａｃｔＰＴＨ／低下" ,text) #nocasesense
		text = re.compile(u"ＩＮＴＡＣＴ‐ＰＴＨ／上昇" ,re.I).sub( u"ｉｎｔａｃｔＰＴＨ／上昇" ,text) #nocasesense
		text = re.compile(u"ＬＤ／上昇" ,re.I).sub( u"ＬＤＨ／上昇" ,text) #nocasesense
		text = re.compile(u"ＬＤＬ／上昇" ,re.I).sub( u"ＬＤＬ‐Ｃ／上昇" ,text) #nocasesense
		text = re.compile(u"ＰＩＶＫＡ‐２／上昇" ,re.I).sub( u"ＰＩＶＫＡ‐ＩＩ／上昇" ,text) #nocasesense
		text = re.compile(u"Ｔ．Ｂｉｌ／上昇" ,re.I).sub( u"Ｔ−ｂｉｌ／上昇" ,text) #nocasesense
		text = re.compile(u"Ｔ‐ｃｈｏｌ／上昇" ,re.I).sub( u"Ｔ−Ｃｈｏ／上昇" ,text) #nocasesense
		text = re.compile(u"Ｔｇ‐Ａｂ／上昇" ,re.I).sub( u"Ｔｇ抗体／上昇" ,text) #nocasesense
		text = re.compile(u"ＴＰＯＡｂ／上昇" ,re.I).sub( u"ＴＰＯ抗体／陽性" ,text) #nocasesense
		text = re.compile(u"ＴＲＡｂ／上昇" ,re.I).sub( u"ＴＲ抗体／陽性" ,text) #nocasesense
		text = re.compile(u"γ‐Ｇ蛋白／上昇" ,re.I).sub( u"γＧ蛋白／上昇" ,text) #nocasesense
		text = re.compile(u"γ‐Ｇ蛋白／正常" ,re.I).sub( u"γＧ蛋白／正常" ,text) #nocasesense
		text = re.compile(u"フェリチン値／上昇" ,re.I).sub( u"フェリチン／上昇" ,text) #nocasesense
		text = re.compile(u"レニン活性／低下" ,re.I).sub( u"レニン／低下" ,text) #nocasesense
		text = re.compile(u"意識レベル／低下" ,re.I).sub( u"意識／低下" ,text) #nocasesense
		text = re.compile(u"異形リンパ球／陽性" ,re.I).sub( u"異型リンパ球／陽性" ,text) #nocasesense
		text = re.compile(u"芽球／上昇" ,re.I).sub( u"芽球／陽性" ,text) #nocasesense
		text = re.compile(u"血液ガス分析＝ＨＣＯ３／低下" ,re.I).sub( u"血液ガス＝ＨＣＯ３−／低下" ,text) #nocasesense
		text = re.compile(u"血液ガス分析＝ｐＨ／低下" ,re.I).sub( u"血液ガス＝ｐＨ／低下" ,text) #nocasesense
		text = re.compile(u"血液ガス分析＝ｐＯ２／低下" ,re.I).sub( u"血液ガス＝ＰａＣＯ２／低下" ,text) #nocasesense
		text = re.compile(u"血小板／低下",re.I).sub( u"血小板／減少" ,text) #nocasesense
		text = re.compile(u"血小板数／正常" ,re.I).sub( u"血小板／正常" ,text) #nocasesense
		text = re.compile(u"血小板数／低下" ,re.I).sub( u"血小板／低下" ,text) #nocasesense
		text = re.compile(u"血清ＡＣＥ／上昇" ,re.I).sub( u"ＡＣＥ／上昇" ,text) #nocasesense
		text = re.compile(u"血清ＩｇＧ４／上昇" ,re.I).sub( u"ＩｇＧ４／上昇" ,text) #nocasesense
		text = re.compile(u"血清ＩＬ‐６／上昇" ,re.I).sub( u"ＩＬ‐６／上昇" ,text) #nocasesense
		text = re.compile(u"血清Ｋ／低下" ,re.I).sub( u"Ｋ／低下" ,text) #nocasesense
		text = re.compile(u"血清Ｍ蛋白／陽性" ,re.I).sub( u"Ｍ蛋白／陽性" ,text) #nocasesense
		text = re.compile(u"血清Ｎａ／正常" ,re.I).sub( u"Ｎａ／正常" ,text) #nocasesense
		text = re.compile(u"血清アミラ‐ゼ／上昇" ,re.I).sub( u"アミラーゼ／上昇" ,text) #nocasesense
		text = re.compile(u"血清アルブミン／低下" ,re.I).sub( u"アルブミン／低下" ,text) #nocasesense
		text = re.compile(u"血清クレアチニン／上昇" ,re.I).sub( u"クレアチニン／上昇" ,text) #nocasesense
		text = re.compile(u"血清クレアチニン／正常" ,re.I).sub( u"クレアチニン／正常" ,text) #nocasesense
		text = re.compile(u"血清抗糖脂質抗体／陽性" ,re.I).sub( u"抗糖脂質抗体／陽性" ,text) #nocasesense
		text = re.compile(u"血清浸透圧／上昇" ,re.I).sub( u"浸透圧／上昇" ,text) #nocasesense
		text = re.compile(u"血清浸透圧／低下" ,re.I).sub( u"浸透圧／低下" ,text) #nocasesense
		text = re.compile(u"血清銅／低下" ,re.I).sub( u"銅／低下" ,text) #nocasesense
		text = re.compile(u"血中ＣＫ値／上昇" ,re.I).sub( u"ＣＫ／上昇" ,text) #nocasesense
		text = re.compile(u"血中ＣＰＲ／低下" ,re.I).sub( u"ＣＰＲ／低下" ,text) #nocasesense
		text = re.compile(u"血中Ｃペプチド／上昇" ,re.I).sub( u"Ｃペプチド／上昇" ,text) #nocasesense
		text = re.compile(u"血中Ｃペプチド／低下" ,re.I).sub( u"Ｃペプチド／低下" ,text) #nocasesense
		text = re.compile(u"血中インスリン／上昇" ,re.I).sub( u"インスリン／上昇" ,text) #nocasesense
		text = re.compile(u"血中総ケトン／上昇" ,re.I).sub( u"総ケトン／上昇" ,text) #nocasesense
		text = re.compile(u"血糖／上昇" ,re.I).sub( u"血糖／高値" ,text) #nocasesense
		text = re.compile(u"血糖値／上昇" ,re.I).sub( u"血糖／高値" ,text) #nocasesense
		text = re.compile(u"血糖値／低下" ,re.I).sub( u"血糖／低下" ,text) #nocasesense
		text = re.compile(u"好酸球数／上昇" ,re.I).sub( u"好酸球／上昇" ,text) #nocasesense
		text = re.compile(u"抗ＤＮＡ抗体／上昇" ,re.I).sub( u"抗ＤＮＡ抗体／陽性" ,text) #nocasesense
		text = re.compile(u"抗ｄｓ‐ＤＮＡ抗体／陽性" ,re.I).sub( u"抗ｄｓＤＮＡ抗体／陽性" ,text) #nocasesense
		text = re.compile(u"抗ＧＡＤ抗体／上昇" ,re.I).sub( u"抗ＧＡＤ抗体／陽性" ,text) #nocasesense
		text = re.compile(u"抗ＲＮＰ抗体／上昇" ,re.I).sub( u"抗ＲＮＰ抗体／陽性" ,text) #nocasesense
		text = re.compile(u"抗ＳＳ‐Ａ／Ｒｏ抗体" ,re.I).sub( u"抗ＳＳＡ抗体／Ｒｏ抗体" ,text) #nocasesense
		text = re.compile(u"抗ＳＳ‐Ａ抗体／陽性" ,re.I).sub( u"抗ＳＳＡ抗体／陽性" ,text) #nocasesense
		text = re.compile(u"抗ＳＳ‐Ｂ抗体／陰性" ,re.I).sub( u"抗ＳＳＢ抗体／陰性" ,text) #nocasesense
		text = re.compile(u"抗ＳＳ‐Ｂ抗体／陽性" ,re.I).sub( u"抗ＳＳＢ抗体／陽性" ,text) #nocasesense
		text = re.compile(u"抗Ｔｇ抗体／上昇" ,re.I).sub( u"抗Ｔｇ抗体／陽性" ,text) #nocasesense
		text = re.compile(u"抗ＴＰＯ抗体／上昇" ,re.I).sub( u"抗ＴＰＯ抗体／陽性" ,text) #nocasesense
		text = re.compile(u"抗アセチルコリン受容体抗体／上昇" ,re.I).sub( u"抗アセチルコリン受容体抗体／陽性" ,text) #nocasesense
		text = re.compile(u"抗核抗体／上昇" ,re.I).sub( u"抗核抗体／陽性" ,text) #nocasesense
		text = re.compile(u"心拍／正常" ,re.I).sub( u"心拍数／正常" ,text) #nocasesense
		text = re.compile(u"神経学的異常所見／陰性" ,re.I).sub( u"神経学的異常／陰性" ,text) #nocasesense
		text = re.compile(u"神経学的所見／正常" ,re.I).sub( u"神経所見／正常" ,text) #nocasesense
		text = re.compile(u"神経症状／陰性" ,re.I).sub( u"神経所見／陰性" ,text) #nocasesense
		text = re.compile(u"神経伝導検査／正常" ,re.I).sub( u"神経伝導速度／正常" ,text) #nocasesense
		text = re.compile(u"随時血糖値／上昇" ,re.I).sub( u"随時血糖／上昇" ,text) #nocasesense
		text = re.compile(u"髄液＝細胞／上昇" ,re.I).sub( u"髄液＝細胞数／上昇" ,text) #nocasesense
		text = re.compile(u"髄液検査／正常" ,re.I).sub( u"髄液／正常" ,text) #nocasesense
		text = re.compile(u"髄液検査＝ＩＬ‐６／上昇" ,re.I).sub( u"髄液＝ＩＬ‐６／上昇" ,text) #nocasesense
		text = re.compile(u"髄液検査＝細胞数／上昇" ,re.I).sub( u"髄液＝細胞数／上昇" ,text) #nocasesense
		text = re.compile(u"髄液検査＝細胞数／正常" ,re.I).sub( u"髄液＝細胞数／正常" ,text) #nocasesense
		text = re.compile(u"髄液検査＝総蛋白／上昇" ,re.I).sub( u"髄液＝総蛋白／上昇" ,text) #nocasesense
		text = re.compile(u"髄液検査＝単核球／上昇" ,re.I).sub( u"髄液＝単核球／上昇" ,text) #nocasesense
		text = re.compile(u"髄液検査＝蛋白／上昇" ,re.I).sub( u"髄液＝蛋白／上昇" ,text) #nocasesense
		text = re.compile(u"髄液検査＝糖／正常" ,re.I).sub( u"髄液＝糖／正常" ,text) #nocasesense
		text = re.compile(u"髄液検査＝糖／低下" ,re.I).sub( u"髄液＝糖／低下" ,text) #nocasesense
		text = re.compile(u"髄液細胞数／上昇" ,re.I).sub( u"髄液＝細胞数／上昇" ,text) #nocasesense
		text = re.compile(u"髄液細胞数／正常" ,re.I).sub( u"髄液＝細胞数／正常" ,text) #nocasesense
		text = re.compile(u"髄液所見／正常" ,re.I).sub( u"髄液／正常" ,text) #nocasesense
		text = re.compile(u"髄液所見＝蛋白／上昇" ,re.I).sub( u"髄液＝蛋白／上昇" ,text) #nocasesense
		text = re.compile(u"髄液蛋白／上昇" ,re.I).sub( u"髄液＝蛋白／上昇" ,text) #nocasesense
		text = re.compile(u"髄液蛋白／正常" ,re.I).sub( u"髄液＝蛋白／正常" ,text) #nocasesense
		text = re.compile(u"髄膜刺激症状／陰性" ,re.I).sub( u"髄膜刺激徴候／陰性" ,text) #nocasesense
		text = re.compile(u"髄膜刺激症状／陽性" ,re.I).sub( u"髄膜刺激徴候／陽性" ,text) #nocasesense
		text = re.compile(u"髄膜刺激兆候／陰性" ,re.I).sub( u"髄膜刺激徴候／陰性" ,text) #nocasesense
		text = re.compile(u"染色体／正常" ,re.I).sub( u"染色体分析／正常" ,text) #nocasesense
		text = re.compile(u"蛋白尿／上昇" ,re.I).sub( u"蛋白尿／陽性" ,text) #nocasesense
		text = re.compile(u"尿ケトン／陰性" ,re.I).sub( u"尿ケトン体／陰性" ,text) #nocasesense
		text = re.compile(u"尿ケトン／陽性" ,re.I).sub( u"尿ケトン体／陽性" ,text) #nocasesense
		text = re.compile(u"尿検査＝ケトン／陽性" ,re.I).sub( u"尿＝ケトン／陽性" ,text) #nocasesense
		text = re.compile(u"尿中赤血球／上昇" ,re.I).sub( u"尿中赤血球／陽性" ,text) #nocasesense
		text = re.compile(u"尿中白血球／上昇" ,re.I).sub( u"尿中白血球／陽性" ,text) #nocasesense
		text = re.compile(u"白血球／低下" ,re.I).sub( u"白血球／減少" ,text) #nocasesense
		text = re.compile(u"白血球数／上昇" ,re.I).sub( u"白血球／上昇" ,text) #nocasesense
		text = re.compile(u"白血球数／正常" ,re.I).sub( u"白血球／正常" ,text) #nocasesense
		text = re.compile(u"白血球数／低下" ,re.I).sub( u"白血球／減少" ,text) #nocasesense
		text = re.compile(u"腹水ＡＤＡ／上昇" ,re.I).sub( u"腹水＝ＡＤＡ／上昇" ,text) #nocasesense
		text = re.compile(u"腹部ＣＴ検査／正常" ,re.I).sub( u"腹部ＣＴ／正常" ,text) #nocasesense
		text = re.compile(u"末梢血＝異型リンパ球／陽性" ,re.I).sub( u"異型リンパ球／陽性" ,text) #nocasesense
		text = re.compile(u"末梢血＝芽球／陽性" ,re.I).sub( u"芽球／陽性" ,text) #nocasesense
		text = re.compile(u"末梢血好酸球／上昇" ,re.I).sub( u"好酸球／上昇" ,text) #nocasesense
		text = re.compile(u"網赤血球／低下" ,re.I).sub( u"網状赤血球／低下" ,text) #nocasesense
		text = re.compile(u"筋力／低下" ,re.I).sub( u"筋力低下" ,text) #nocasesense
		text = re.compile(u"リンパ節腫大" ,re.I).sub( u"リンパ節腫脹" ,text) #nocasesense
		text = re.compile(u"リンパ腫大" ,re.I).sub( u"リンパ節腫脹" ,text) #nocasesense
		text = re.compile(u"リンパ腫脹" ,re.I).sub( u"リンパ節腫脹" ,text) #nocasesense
		text = re.compile(u"(全身|顎下|鼠径|鎖骨下|頸部|腋窩|表在|縦隔)性*リンパ節腫脹" ,re.I).sub( u"リンパ節腫脹＠\\1" ,text) #nocasesense
		text = re.compile(u"（[^）]*）" ,re.I).sub( u"" ,text) #nocasesense, inselect


		#英数字・記号・空白を半角に変換する
		text = cnvk.convert(text, cnvk.H_ALPHA, cnvk.H_NUM, cnvk.H_KIGO, cnvk.H_SPACE)

		text = re.compile(u" " ,re.I).sub( u"_"  ,text) #nocasesense
		text = re.compile(u"__" ,re.I).sub( u"_"  ,text) #nocasesense
		text = re.compile(u"__" ,re.I).sub( u"_"  ,text) #nocasesense
		text = re.compile(u"_\n" ,re.I).sub( u"\n"  ,text) #nocasesense
		text = re.compile(u"_\n" ,re.I).sub( u"\n"  ,text) #nocasesense
		text = re.compile(u"_\n" ,re.I).sub( u"\n"  ,text) #nocasesense
		text = re.compile(u"_\n" ,re.I).sub( u"\n"  ,text) #nocasesense
		text = re.compile(u"\n_" ,re.I).sub( u"\n"  ,text) #nocasesense
		text = re.compile(u"\n_" ,re.I).sub( u"\n"  ,text) #nocasesense
		text = re.compile(u"\n_" ,re.I).sub( u"\n"  ,text) #nocasesense
		text = re.compile(u"\n_" ,re.I).sub( u"\n"  ,text) #nocasesense
		text = re.compile(u"([ァ-ヴ])-" ,re.I).sub( u"\\1ー"  ,text) #nocasesense
		text = re.compile(u"([ァ-ヴ])-" ,re.I).sub( u"\\1ー"  ,text) #nocasesense
		text = re.compile(u"_+([\\/\\=\\@\\・\\:])" ,re.I).sub( u"\\1"  ,text) #nocasesense
		text = re.compile(u"([\\/\\=\\@\\・\\:])_+" ,re.I).sub( u"\\1"  ,text) #nocasesense
		text = re.compile(u"^_+" ,re.I).sub( u""  ,text) #nocasesense
		text = re.compile(u"Cushing症候群" ,re.I).sub(u"クッシング症候群"  ,text) #nocasesense
		text = re.compile(u"Adenocarcinomatous" ,re.I).sub(u"腺癌性"  ,text) #nocasesense
		text = re.compile(u"Adenocarcinoma" ,re.I).sub(u"腺癌"  ,text) #nocasesense
		text = re.compile(u"pituitary_tumor" ,re.I).sub(u"下垂体腫瘍"  ,text) #nocasesense
		text = re.compile(u"Cushing病" ,re.I).sub(u"クッシング病"  ,text) #nocasesense
		text = re.compile(u"Wegener肉芽腫症" ,re.I).sub(u"ウェゲナー肉芽腫症"  ,text) #nocasesense
		text = re.compile(u"Sheehan症候群" ,re.I).sub(u"シーハン症候群"  ,text) #nocasesense
		text = re.compile(u"systemic_mastocytosis" ,re.I).sub(u"全身性肥満細胞症"  ,text) #nocasesense
		text = re.compile(u"overlap症候群" ,re.I).sub(u"オーバーラップ症候群"  ,text) #nocasesense
		text = re.compile(u"Aspergillus感染症" ,re.I).sub(u"アスペルギルス感染症"  ,text) #nocasesense
		text = re.compile(u"azathioprine副作用" ,re.I).sub(u"アザチオプリン副作用"  ,text) #nocasesense
		text = re.compile(u"Castleman病" ,re.I).sub(u"キャッスルマン病"  ,text) #nocasesense
		text = re.compile(u"尿中myoglobin" ,re.I).sub(u"尿中ミオグロビン"  ,text) #nocasesense
		text = re.compile(u"Methotrexate副作用" ,re.I).sub(u"メトトレキセート副作用"  ,text) #nocasesense
		text = re.compile(u"Non-Hodgkin_lymphoma" ,re.I).sub(u"非ホジキンリンパ腫"  ,text) #nocasesense
		text = re.compile(u"Donepezil" ,re.I).sub(u"ドネペジル"  ,text) #nocasesense
		text = re.compile(u"Trousseau徴候" ,re.I).sub(u"トルソー徴候"  ,text) #nocasesense
		text = re.compile(u"Parathyroidadenoma" ,re.I).sub(u"副甲状腺腫"  ,text) #nocasesense
		text = re.compile(u"Stent内" ,re.I).sub(u"ステント内"  ,text) #nocasesense
		text = re.compile(u"Gottoron徴候" ,re.I).sub(u"ゴトロン徴候"  ,text) #nocasesense
		text = re.compile(u"Fisher症候群" ,re.I).sub(u"フィッシャー症候群"  ,text) #nocasesense
		text = re.compile(u"adenocarcinoma" ,re.I).sub(u"腺癌"  ,text) #nocasesense
		text = re.compile(u"intravascular_lymphoma" ,re.I).sub(u"血管内リンパ腫"  ,text) #nocasesense
		text = re.compile(u"thrombotic_microangiopathy" ,re.I).sub(u"血栓性微小血管症"  ,text) #nocasesense
		text = re.compile(u"成人Still病" ,re.I).sub(u"成人スティル病"  ,text) #nocasesense
		text = re.compile(u"Fabry病" ,re.I).sub(u"ファブリー病"  ,text) #nocasesense
		text = re.compile(u"成人発症Still病" ,re.I).sub(u"成人発症スティル病"  ,text) #nocasesense
		text = re.compile(u"Fibrillary_glomerulonephritis" ,re.I).sub(u"糸球体腎炎"  ,text) #nocasesense
		text = re.compile(u"Raynaud現象" ,re.I).sub(u"レイノー現象"  ,text) #nocasesense
		text = re.compile(u"Crohn病" ,re.I).sub(u"クローン病"  ,text) #nocasesense
		text = re.compile(u"T-cell_lymphoma" ,re.I).sub(u"T細胞リンパ腫"  ,text) #nocasesense
		text = re.compile(u"methotrexate副作用" ,re.I).sub(u"メトトレキセート副作用"  ,text) #nocasesense
		text = re.compile(u"mesalazine副作用" ,re.I).sub(u"メサラジン副作用"  ,text) #nocasesense
		text = re.compile(u"胸部ct" ,re.I).sub(u"胸部CT"  ,text) #nocasesense
		text = re.compile(u"Salmonella菌血症" ,re.I).sub(u"サルモネラ菌血症"  ,text) #nocasesense
		text = re.compile(u"Behcet病" ,re.I).sub(u"ベーチェット病"  ,text) #nocasesense
		text = re.compile(u"IgG4-related_disease" ,re.I).sub(u"IgG4関連疾患"  ,text) #nocasesense
		text = re.compile(u"Azacitidine副作用" ,re.I).sub(u"アザシチジン副作用"  ,text) #nocasesense
		text = re.compile(u"follicular_lymphoma" ,re.I).sub(u"濾胞リンパ腫"  ,text) #nocasesense
		text = re.compile(u"Choledochocele" ,re.I).sub(u"胆石症"  ,text) #nocasesense
		text = re.compile(u"高cortisol血症" ,re.I).sub(u"高コルチゾール血症"  ,text) #nocasesense
		text = re.compile(u"thromboticmicroangiopathy" ,re.I).sub(u"血栓性微小血管症"  ,text) #nocasesense
		text = re.compile(u"T-cellリンパ腫" ,re.I).sub(u"T細胞リンパ腫"  ,text) #nocasesense
		text = re.compile(u"Gottron徴候" ,re.I).sub(u"ゴトロン徴候"  ,text) #nocasesense
		text = re.compile(u"Tolvaptan" ,re.I).sub(u"トルバプタン"  ,text) #nocasesense
		text = re.compile(u"Guillain-Barre症候群" ,re.I).sub(u"ギラン・バレー症候群"  ,text) #nocasesense
		text = re.compile(u"多中心性Castleman病" ,re.I).sub(u"多中心性キャッスルマン病"  ,text) #nocasesense
		text = re.compile(u"Rituximab" ,re.I).sub(u"リツキシマブ"  ,text) #nocasesense
		text = re.compile(u"Ceftriaxone" ,re.I).sub(u"セフトリアキソン"  ,text) #nocasesense
		text = re.compile(u"Hodgkin病" ,re.I).sub(u"ホジキン病"  ,text) #nocasesense
		text = re.compile(u"Lupus腸炎" ,re.I).sub(u"ループス腸炎"  ,text) #nocasesense
		text = re.compile(u"Lupus膀胱炎" ,re.I).sub(u"ループス膀胱炎"  ,text) #nocasesense
		text = re.compile(u"Lupus膀胱炎" ,re.I).sub(u"ループス腎炎"  ,text) #nocasesense
		text = re.compile(u"神経Behcet病" ,re.I).sub(u"神経ベーチェット病"  ,text) #nocasesense
		text = re.compile(u"hepatitis" ,re.I).sub(u"肝炎"  ,text) #nocasesense
		text = re.compile(u"parathyroid_adenoma" ,re.I).sub(u"副甲状腺腫"  ,text) #nocasesense
		text = re.compile(u"低albumin血症" ,re.I).sub(u"低アルブミン血症"  ,text) #nocasesense
		text = re.compile(u"低fibrinogen血症" ,re.I).sub(u"低フィブリノゲン血症"  ,text) #nocasesense
		text = re.compile(u"Acromegaly" ,re.I).sub(u"先端巨大症"  ,text) #nocasesense
		text = re.compile(u"Adalimumab" ,re.I).sub(u"アダリムマブ"  ,text) #nocasesense
		text = re.compile(u"pittng_edema" ,re.I).sub(u"水疱"  ,text) #nocasesense
		text = re.compile(u"Hypothyroid_Graves’_disease" ,re.I).sub(u"甲状腺機能低下症"  ,text) #nocasesense
		text = re.compile(u"nivolumab" ,re.I).sub(u"ニボルマブ"  ,text) #nocasesense
		text = re.compile(u"diffuse_large_B-cell_lymphoma" ,re.I).sub(u"びまん性大細胞型B細胞リンパ腫"  ,text) #nocasesense
		text = re.compile(u"AngioimmunoblasticT-cell_lymphoma" ,re.I).sub(u"血管免疫芽球性T細胞リンパ腫"  ,text) #nocasesense
		text = re.compile(u"moon_face" ,re.I).sub(u"丸顔"  ,text) #nocasesense
		text = re.compile(u"Trousseau症候群" ,re.I).sub(u"トルソー症候群"  ,text) #nocasesense
		text = re.compile(u"wheeze聴取" ,re.I).sub(u"喘鳴聴取"  ,text) #nocasesense
		text = re.compile(u"parvo_virus感染症" ,re.I).sub(u"パルボウイルス感染"  ,text) #nocasesense
		text = re.compile(u"neuroendocrine_tumor" ,re.I).sub(u"神経内分泌腫瘍"  ,text) #nocasesense
		text = re.compile(u"Pituitaryadenoma" ,re.I).sub(u"下垂体腺腫"  ,text) #nocasesense
		text = re.compile(u"chorea-ballism" ,re.I).sub(u"舞踏病"  ,text) #nocasesense
		text = re.compile(u"Barre徴候" ,re.I).sub(u"バレー徴候"  ,text) #nocasesense
		text = re.compile(u"Gemella" ,re.I).sub(u"貧血"  ,text) #nocasesense
		text = re.compile(u"salazosulfapyridine副作用" ,re.I).sub(u"サラゾスルファピリジン副作用"  ,text) #nocasesense
		text = re.compile(u"chronic_lymphocytic_leukemia" ,re.I).sub(u"慢性リンパ性白血病"  ,text) #nocasesense
		text = re.compile(u"ＨbA1c" ,re.I).sub(u"HbA1c"  ,text) #nocasesense
		text = re.compile(u"Follicular_lymphoma" ,re.I).sub(u"濾胞リンパ腫"  ,text) #nocasesense
		text = re.compile(u"rituximab併用化学療法" ,re.I).sub(u"リツキシマブ併用化学療法"  ,text) #nocasesense
		text = re.compile(u"Raynaud徴候" ,re.I).sub(u"レイノー徴候"  ,text) #nocasesense
		text = re.compile(u"plasmacytoma" ,re.I).sub(u"形質細胞腫"  ,text) #nocasesense
		text = re.compile(u"Osler病" ,re.I).sub(u"オスラー病"  ,text) #nocasesense
		text = re.compile(u"lymphoma" ,re.I).sub(u"リンパ腫"  ,text) #nocasesense
		text = re.compile(u"多腺性自己免疫症候群type3" ,re.I).sub(u"多腺性自己免疫症候群3型"  ,text) #nocasesense
		text = re.compile(u"B-cell_lymphoma" ,re.I).sub(u"B細胞リンパ腫"  ,text) #nocasesense
		text = re.compile(u"abnormalcell" ,re.I).sub(u"異常細胞"  ,text) #nocasesense
		text = re.compile(u"糖尿病性Chorea-Ballism" ,re.I).sub(u"糖尿病性舞踏病"  ,text) #nocasesense
		text = re.compile(u"sepsis" ,re.I).sub(u"敗血症"  ,text) #nocasesense
		text = re.compile(u"Thiamazole副作用" ,re.I).sub(u"チアマゾール副作用"  ,text) #nocasesense
		text = re.compile(u"Hodgkinリンパ腫" ,re.I).sub(u"ホジキンリンパ腫"  ,text) #nocasesense
		text = re.compile(u"inflammatory_pseudotumor" ,re.I).sub(u"炎症性偽腫瘍"  ,text) #nocasesense
		text = re.compile(u"penicilinG" ,re.I).sub(u"ペニシリンG"  ,text) #nocasesense
		text = re.compile(u"Guillain-Barre症候群" ,re.I).sub(u"ギラン・バレー症候群"  ,text) #nocasesense
		text = re.compile(u"cortisol日内変動消失" ,re.I).sub(u"コルチゾール日内変動消失"  ,text) #nocasesense
		text = re.compile(u"Henoch-Schonlein紫斑病" ,re.I).sub(u"ヘノッホ・シェーンライン紫斑病"  ,text) #nocasesense
		text = re.compile(u"malignancy" ,re.I).sub(u"悪性腫瘍"  ,text) #nocasesense
		text = re.compile(u"parvovirusB19感染" ,re.I).sub(u"パルボウイルスB19感染"  ,text) #nocasesense
		text = re.compile(u"adalimumab" ,re.I).sub(u"アダリムマブ"  ,text) #nocasesense
		text = re.compile(u"Septic_embolism" ,re.I).sub(u"敗血症性塞栓症"  ,text) #nocasesense
		text = re.compile(u"plasmablasticlymphoma" ,re.I).sub(u"血栓塞栓症"  ,text) #nocasesense
		text = re.compile(u"Stiff-Person症候群" ,re.I).sub(u"スティッフパーソン症候群"  ,text) #nocasesense
		text = re.compile(u"Wheezing" ,re.I).sub(u"喘鳴"  ,text) #nocasesense
		text = re.compile(u"VitaminB12欠乏" ,re.I).sub(u"ビタミンB12欠乏症"  ,text) #nocasesense
		text = re.compile(u"bortezomib副作用" ,re.I).sub(u"ボルテゾミブ副作用"  ,text) #nocasesense
		text = re.compile(u"vasculitis" ,re.I).sub(u"血管炎"  ,text) #nocasesense
		text = re.compile(u"moon_face" ,re.I).sub(u"丸顔"  ,text) #nocasesense
		text = re.compile(u"Reiter症候群" ,re.I).sub(u"ライター症候群"  ,text) #nocasesense
		text = re.compile(u"septic_emboli" ,re.I).sub(u"敗血症性塞栓症"  ,text) #nocasesense
		text = re.compile(u"Rituximab副作用" ,re.I).sub(u"リツキシマブ副作用"  ,text) #nocasesense
		text = re.compile(u"Imatinib副作用" ,re.I).sub(u"イマチニブ副作用"  ,text) #nocasesense
		text = re.compile(u"dasatinib副作用" ,re.I).sub(u"ダサチニブ副作用"  ,text) #nocasesense
		text = re.compile(u"parathyroidadenoma" ,re.I).sub(u"副甲状腺腫"  ,text) #nocasesense
		text = re.compile(u"Guillain-Barre_syndrome" ,re.I).sub(u"ギランバレー症候群"  ,text) #nocasesense
		text = re.compile(u"Gitelman症候" ,re.I).sub(u"ギッテルマン症候群"  ,text) #nocasesense
		text = re.compile(u"Salazosulfapyridine副作用" ,re.I).sub(u"サラゾスルファピリジン副作用"  ,text) #nocasesense
		text = re.compile(u"adenoma" ,re.I).sub(u"腺腫"  ,text) #nocasesense
		text = re.compile(u"Langerhans細胞組織球症" ,re.I).sub(u"ランゲルハンス細胞組織球症"  ,text) #nocasesense
		text = re.compile(u"dysesthesia" ,re.I).sub(u"感覚異常"  ,text) #nocasesense
		text = re.compile(u"Intravascular_lymphoma" ,re.I).sub(u"血管内リンパ腫"  ,text) #nocasesense
		text = re.compile(u"Hodgkin_lymphoma" ,re.I).sub(u"ホジキンリンパ腫"  ,text) #nocasesense
		text = re.compile(u"rituximab" ,re.I).sub(u"リツキシマブ"  ,text) #nocasesense
		text = re.compile(u"steatohepatitis" ,re.I).sub(u"脂肪性肝炎"  ,text) #nocasesense
		text = re.compile(u"amyopathic_Dermatomyositis" ,re.I).sub(u"筋萎縮性側索硬化症"  ,text) #nocasesense
		text = re.compile(u"Tichropidine副作用" ,re.I).sub(u"チクロピジン副作用"  ,text) #nocasesense
		text = re.compile(u"Lupus_nephritis" ,re.I).sub(u"ループス腎炎"  ,text) #nocasesense
		text = re.compile(u"predonisolone" ,re.I).sub(u"プレドニゾロン"  ,text) #nocasesense
		text = re.compile(u"acute_respiratory_distress_syndrome" ,re.I).sub(u"急性呼吸窮迫症候群"  ,text) #nocasesense
		text = re.compile(u"septic_embolism" ,re.I).sub(u"敗血症"  ,text) #nocasesense
		text = re.compile(u"graft-versus-host_disease" ,re.I).sub(u"移植片対宿主病"  ,text) #nocasesense
		text = re.compile(u"thymoma" ,re.I).sub(u"胸腺腫"  ,text) #nocasesense
		text = re.compile(u"Hyperparathyroidism" ,re.I).sub(u"副甲状腺機能亢進症"  ,text) #nocasesense
		text = re.compile(u"shock_vital" ,re.I).sub(u"ショックバイタル"  ,text) #nocasesense
		text = re.compile(u"Overlap症候群" ,re.I).sub(u"重複症候群"  ,text) #nocasesense
		text = re.compile(u"Bortezomib副作用" ,re.I).sub(u"ボルテゾミブ副作用"  ,text) #nocasesense
		text = re.compile(u"wheezes" ,re.I).sub(u"喘鳴"  ,text) #nocasesense
		text = re.compile(u"_amyloidosis" ,re.I).sub(u"アミロイドーシス"  ,text) #nocasesense
		text = re.compile(u"reversible_posterior_leukoencephalopathy_syndrome" ,re.I).sub(u"可逆性後部白質脳症症候群"  ,text) #nocasesense
		text = re.compile(u"myeloid_sarcoma" ,re.I).sub(u"骨髄肉腫"  ,text) #nocasesense
		text = re.compile(u"myeloidsarcoma" ,re.I).sub(u"骨髄肉腫"  ,text) #nocasesense
		text = re.compile(u"Sarcoidosis" ,re.I).sub(u"サルコイドーシス"  ,text) #nocasesense
		text = re.compile(u"amiodarone" ,re.I).sub(u"アミオダロン"  ,text) #nocasesense
		text = re.compile(u"Parkinson病" ,re.I).sub(u"パーキンソン病"  ,text) #nocasesense
		text = re.compile(u"Lymphoplasmacytic_lymphoma" ,re.I).sub(u"リンパ形質細胞性リンパ腫"  ,text) #nocasesense
		text = re.compile(u"Reversible_posterior_leukoencephalopathy_syndrome" ,re.I).sub(u"可逆性後部白質脳症症候群"  ,text) #nocasesense
		text = re.compile(u"Sjogren_syndrome" ,re.I).sub(u"シェーグレン症候群"  ,text) #nocasesense
		text = re.compile(u"低alb血症" ,re.I).sub(u"低血圧症"  ,text) #nocasesense
		text = re.compile(u"myokymicdischarge" ,re.I).sub(u"筋萎縮"  ,text) #nocasesense
		text = re.compile(u"B-celllymphoma" ,re.I).sub(u"B細胞リンパ腫"  ,text) #nocasesense
		text = re.compile(u"肺Carcinoid" ,re.I).sub(u"肺カルチノイド"  ,text) #nocasesense
		text = re.compile(u"Tangier病" ,re.I).sub(u"タンジール病"  ,text) #nocasesense
		text = re.compile(u"propylthiouracil" ,re.I).sub(u"プロピルチオウラシル"  ,text) #nocasesense
		text = re.compile(u"prednisolone" ,re.I).sub(u"プレドニゾロン"  ,text) #nocasesense
		text = re.compile(u"Campylobacter腸炎" ,re.I).sub(u"カンピロバクター腸炎"  ,text) #nocasesense
		text = re.compile(u"neuroendocrine_carcinoma" ,re.I).sub(u"神経内分泌癌"  ,text) #nocasesense
		text = re.compile(u"Alzheimer病" ,re.I).sub(u"アルツハイマー病"  ,text) #nocasesense
		text = re.compile(u"telaprevir" ,re.I).sub(u"テラプレビル"  ,text) #nocasesense
		text = re.compile(u"wheeze" ,re.I).sub(u"喘鳴"  ,text) #nocasesense
		text = re.compile(u"ParvovirusB19感染" ,re.I).sub(u"パルボウイルスB19感染"  ,text) #nocasesense
		text = re.compile(u"Gemcitabine副作用" ,re.I).sub(u"ゲムシタビン副作用"  ,text) #nocasesense
		text = re.compile(u"dry_mouth" ,re.I).sub(u"ドライマウス"  ,text) #nocasesense
		text = re.compile(u"dry_eye" ,re.I).sub(u"ドライアイ"  ,text) #nocasesense
		text = re.compile(u"proteinuria" ,re.I).sub(u"蛋白尿"  ,text) #nocasesense
		text = re.compile(u"Vancomycin副作用" ,re.I).sub(u"バンコマイシン副作用"  ,text) #nocasesense
		text = re.compile(u"Adult_T-cell_leukemia" ,re.I).sub(u"成人T細胞白血病"  ,text) #nocasesense
		text = re.compile(u"Creutzfeld-Jakob病" ,re.I).sub(u"クロイツフェルト・ヤコブ病"  ,text) #nocasesense
		text = re.compile(u"Metformin" ,re.I).sub(u"メトホルミン"  ,text) #nocasesense
		text = re.compile(u"lymphangiomatosis" ,re.I).sub(u"リンパ管腫症"  ,text) #nocasesense
		text = re.compile(u"non-Hodgkinlymphoma" ,re.I).sub(u"非ホジキンリンパ腫"  ,text) #nocasesense
		text = re.compile(u"Graves’病" ,re.I).sub(u"グレーブス病"  ,text) #nocasesense
		text = re.compile(u"B-cell_lymphoma" ,re.I).sub(u"B細胞リンパ腫"  ,text) #nocasesense
		text = re.compile(u"Bosentan" ,re.I).sub(u"ボセンタン"  ,text) #nocasesense
		text = re.compile(u"pituitary_adenoma" ,re.I).sub(u"下垂体腺腫"  ,text) #nocasesense
		text = re.compile(u"phenitoin" ,re.I).sub(u"フェニトイン"  ,text) #nocasesense
		text = re.compile(u"cyclosporine" ,re.I).sub(u"シクロスポリン"  ,text) #nocasesense
		text = re.compile(u"actinomycosis" ,re.I).sub(u"放線菌症"  ,text) #nocasesense
		text = re.compile(u"Henoch-Schonlein紫斑病" ,re.I).sub(u"ヘノッホ・シェーンライン紫斑病"  ,text) #nocasesense
		text = re.compile(u"Castleman_disease" ,re.I).sub(u"キャッスルマン病"  ,text) #nocasesense
		text = re.compile(u"Parkinson症候群" ,re.I).sub(u"パーキンソン症候群"  ,text) #nocasesense
		text = re.compile(u"Creutzfeldt-Jakob病" ,re.I).sub(u"クロイツフェルト・ヤコブ病"  ,text) #nocasesense
		text = re.compile(u"valaciclovir" ,re.I).sub(u"バラシクロビル"  ,text) #nocasesense
		text = re.compile(u"Neuroendocrine_carcinoma" ,re.I).sub(u"神経内分泌癌"  ,text) #nocasesense
		text = re.compile(u"reversible_posterior_leukoencephalopathy" ,re.I).sub(u"可逆性後部白質脳症"  ,text) #nocasesense
		text = re.compile(u"Heparin" ,re.I).sub(u"ヘパリン"  ,text) #nocasesense
		text = re.compile(u"entecavir" ,re.I).sub(u"エンテカビル"  ,text) #nocasesense
		text = re.compile(u"Cushing兆候" ,re.I).sub(u"クッシング兆候"  ,text) #nocasesense
		text = re.compile(u"paraneoplastic_syndrome" ,re.I).sub(u"腫瘍随伴症候群"  ,text) #nocasesense
		text = re.compile(u"Insulin" ,re.I).sub(u"インスリン"  ,text) #nocasesense
		text = re.compile(u"Salmonella感染症" ,re.I).sub(u"サルモネラ感染症"  ,text) #nocasesense
		text = re.compile(u"Amiodarone" ,re.I).sub(u"アミオダロン"  ,text) #nocasesense
		text = re.compile(u"Lupus腎炎" ,re.I).sub(u"ループス腎炎"  ,text) #nocasesense
		text = re.compile(u"hypothyroid_myopathy" ,re.I).sub(u"甲状腺機能低下症"  ,text) #nocasesense
		text = re.compile(u"Myeloid_sarcoma" ,re.I).sub(u"骨髄肉腫"  ,text) #nocasesense
		text = re.compile(u"malignant_lymphoma" ,re.I).sub(u"悪性リンパ腫"  ,text) #nocasesense
		text = re.compile(u"castleman病" ,re.I).sub(u"キャッスルマン病"  ,text) #nocasesense
		text = re.compile(u"Thrombotic_microangiopathy" ,re.I).sub(u"血栓性微小血管症"  ,text) #nocasesense
		text = re.compile(u"Wegener" ,re.I).sub(u"ウェゲナー"  ,text) #nocasesense
		text = re.compile(u"低Na血症" ,re.I).sub( u"低ナトリウム血症"  ,text) #nocasesense
		text = re.compile(u"Cushing症候群" ,re.I).sub( u"クッシング症候群"  ,text) #nocasesense
		text = re.compile(u"Basedow病" ,re.I).sub( u"バセドウ病"  ,text) #nocasesense
		text = re.compile(u"成人Still病" ,re.I).sub( u"成人スティル病"  ,text) #nocasesense
		text = re.compile(u"Wegener肉芽腫症" ,re.I).sub( u"ウェジナー肉芽腫"  ,text) #nocasesense
		text = re.compile(u"Churg-Strauss症候群" ,re.I).sub( u"チャーグ・ストラウス症候群"  ,text) #nocasesense
		text = re.compile(u"Gitelman症候群" ,re.I).sub( u"ギッテルマン症候群"  ,text) #nocasesense
		text = re.compile(u"Castleman病" ,re.I).sub( u"キャッスルマン病"  ,text) #nocasesense
		text = re.compile(u"Fisher症候群" ,re.I).sub( u"フィッシャー症候群"  ,text) #nocasesense
		text = re.compile(u"Klinefelter症候群" ,re.I).sub( u"クラインフェルター症候群"  ,text) #nocasesense
		text = re.compile(u"Sjogren症候群" ,re.I).sub( u"シェーグレン症候群"  ,text) #nocasesense
		text = re.compile(u"Fanconi症候群" ,re.I).sub( u"ファンコニ症候群"  ,text) #nocasesense
		text = re.compile(u"Wernicke脳症" ,re.I).sub( u"ウェルニッケ脳症"  ,text) #nocasesense
		text = re.compile(u"Lemierre症候群" ,re.I).sub( u"レミエール症候群"  ,text) #nocasesense
		text = re.compile(u"Trousseau症候群" ,re.I).sub( u"トルーソー症候群"  ,text) #nocasesense
		text = re.compile(u"Elsberg症候群" ,re.I).sub( u"エルスバーグ症候群"  ,text) #nocasesense
		text = re.compile(u"Evans症候群" ,re.I).sub( u"エヴァンズ症候群"  ,text) #nocasesense
		text = re.compile(u"低Mg血症" ,re.I).sub( u"低マグネシウム血症"  ,text) #nocasesense
		text = re.compile(u"Prader-Willi症候群" ,re.I).sub( u"プラダー・ウィリ症候群"  ,text) #nocasesense
		text = re.compile(u"CREST症候群" ,re.I).sub( u"クレスト症候群"  ,text) #nocasesense
		text = re.compile(u"toxic_shock_syndrome" ,re.I).sub( u"毒素性ショック症候群"  ,text) #nocasesense
		text = re.compile(u"Cushing病" ,re.I).sub( u"クッシング病"  ,text) #nocasesense
		text = re.compile(u"Graves病" ,re.I).sub( u"グレーブス病"  ,text) #nocasesense
		text = re.compile(u"Fitz-Hugh-Curtis症候群" ,re.I).sub( u"フィッツ・ヒュー・カーティス症候群"  ,text) #nocasesense
		text = re.compile(u"Wilson病" ,re.I).sub( u"ウィルソン病"  ,text) #nocasesense
		text = re.compile(u"Guillain-Barre症候群" ,re.I).sub( u"ギラン・バレー症候群"  ,text) #nocasesense
		text = re.compile(u"高K血症" ,re.I).sub( u"高カリウム血症"  ,text) #nocasesense
		text = re.compile(u"後天性von_Willebrand症候群" ,re.I).sub( u"後天性フォン・ウィルブランド症候群"  ,text) #nocasesense


		# −を‐に変更する

		# 追加
		text = re.sub(u'\s+$',u'',text)
		text = re.sub(u'_+$',u'',text)
		text = re.sub('^"','',text)
		text = re.sub('"$','',text)
		text = text.replace(u'\=','=')
		text = text.replace(u'\/','/')
		text = text.replace(u'−',u'-')
		text = re.sub(u'心エコ-',u'心エコー',text)


		return text


	def judge(self,data):

		all_=0
		errors=0

		progress_bar=tqdm(range(len(data)))
		for i,line in enumerate(data):

			try:
				# if i<6500:
				# 	continue

				cols=line.rstrip('\n').split('\t')
				text_correct=cols[0] # 正解データ
				text_source=cols[1] # 元データ


				# 正解データの整形
				text_correct=re.sub('^"','',text_correct)
				text_correct=re.sub('"$','',text_correct)
				text_correct=text_correct.replace('""','"')


				# 秀丸の処理を加える
				text_changed=self.replace_by_hidemaru(text_source)


				if text_changed==text_correct:
					# 適切に変換された場合はスキップする
					continue

				# print([line['source'].rstrip(u' ')])
				# print([line['source']])
				# print('元)%s => %s \n正)%s\n' %(
				# 		line['source'].encode('utf-8'),
				# 		text_changed.encode('utf-8'),
				# 		line['correct'].encode('utf-8')
				# 	)
				# )

				print('%s\t%s\t%s' %(
						text_source.encode('utf-8'),
						text_changed.encode('utf-8'),
						text_correct.encode('utf-8')
					)
				)
				# pprint('%s\t%s\t%s' %(
				# 		cols[1],
				# 		text_changed,
				# 		cols[0]
				# 	)
				# )

				raise UnmatchError


			except KeyboardInterrupt:
				break

			except UnmatchError:
				errors+=1

			except:
				errors+=1
				print(cols[1])
				print(traceback.format_exc())

			finally:
				pass
				all_+=1
				# if i==1000:
				# 	break
				progress_bar.update(1)


		progress_bar.close()
		print('エラーの件数：%s/%s' %(errors,all_))

	def main(self):
		'''
		メインの処理を実行します。
		'''

		try:

			# 正解データとソースデータを取得する
			# data=self.load_text(path_text='data/hidemaru/relations_20180131_hidemaru.txt')
			data=self.load_nodes(path_text='data/hidemaru/nodes.txt')

			# for i,row in enumerate(data):
			# 	print('%s\t%s' %(row['correct'].encode('utf-8'),row['source'].encode('utf-8')))

				# if i==10:
				# 	break

			# 適切に変換されているかを判定する
			self.judge(data=data)


		except:
			print(traceback.format_exc())

		finally:
			pass


	def each(self,text_source):
		'''
		メインの処理を実行します。
		'''

		try:

			# 正解データとソースデータを取得する
			data=self.load_nodes(path_text='data/hidemaru/nodes.txt')


			# 正解データを取得する
			for line in data:
				cols=line.rstrip('\n').split('\t')
				if cols[1]==text_source:
					text_correct=cols[0] # 正解データ


			# 正解データの整形
			text_correct=re.sub('^"','',text_correct)
			text_correct=re.sub('"$','',text_correct)
			text_correct=text_correct.replace('""','"')


			# 変換する
			text_changed=self.replace_by_hidemaru(text_source)

			if text_changed==text_correct:
				print('OK')
			else:
				print('NG')

			print('%s\t%s\t%s' %(
					text_source.encode('utf-8'),
					text_changed.encode('utf-8'),
					text_correct.encode('utf-8')
				)
			)

		except:
			print(traceback.format_exc())

		finally:
			pass


if __name__ == '__main__':

	# コマンドライン引数を取得する
	parser=argparse.ArgumentParser(
		formatter_class=argparse.RawDescriptionHelpFormatter,
		description='''秀丸のスクリプトを移行します。

例）python2 migrate_hidemaru.py
		'''
	)
	parser.add_argument('-k','--keyword' ,help='個別確認したいキーワード',default=None)
	kwargs=vars(parser.parse_args())

	if kwargs['keyword']:
		text=MigrateHidemaru(**kwargs).each(text_source=kwargs['keyword'].decode('utf-8'))


	else:

		response=MigrateHidemaru(**kwargs).main()
	# pp(response)
