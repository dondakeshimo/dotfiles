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

CURRENT_DIRECTORY=os.path.dirname(os.path.abspath(__file__)) #自ファイルが存在するディレクトリ
SCRIPT_NAME=re.sub('.py.?','',os.path.basename(__file__)) #スクリプト名


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
    def replace_by_hidemaru(self,text):

        text_source=text


        #英数字・記号・空白を全角に変換する
        text = cnvk.convert(text, cnvk.Z_ALPHA, cnvk.Z_NUM, cnvk.Z_KIGO, cnvk.Z_SPACE)

        text = re.compile(u"^Ｈ：経皮的冠動脈形成術（ＰＣＩ）$", re.I).sub(u"Ｈ：経皮的冠動脈形成術", text)
        text = re.compile(u"^無脈性電気活動（ＰＥＡ）$", re.I).sub(u"無脈性電気活動", text)
        text = re.compile(u"^心エコ−＝左室駆出率（ＥＦ）／低下$", re.I).sub(u"心エコ−＝左室駆出率／低下", text)
        text = re.compile(u"^Ｈ：大動脈内バル−ンパンピング（ＩＡＢＰ）$", re.I).sub(u"Ｈ：大動脈内バル−ンパンピング", text)
        text = re.compile(u"^Ｈ：経皮的心肺補助装置（ＰＣＰＳ）$", re.I).sub(u"Ｈ：経皮的心肺補助装置", text)
        text = re.compile(u"^多発血管炎性肉芽腫症（ＧＰＡ）$", re.I).sub(u"多発血管炎性肉芽腫症", text)
        text = re.compile(u"^ＰＣＲ＝Ｅｐｓｔｅｉｎ−ＢａｒｒＶｉｒｕｓ（ＥＢＶ）／陽性$", re.I).sub(u"ＰＣＲ＝Ｅｐｓｔｅｉｎ−ＢａｒｒＶｉｒｕｓ／陽性", text)
        text = re.compile(u"^Ｈ：部分的＊脾動脈塞栓術（ＰＳＥ）／有効$", re.I).sub(u"Ｈ：部分的＊脾動脈塞栓術／有効", text)
        text = re.compile(u"^Ｈ：ｄｅｇｒａｄａｂｌｅ＿ｓｔａｒｃｈｍｉｃｒｏｓｐｈｅｒｅｓ併用肝動注化学塞栓療法（ＤＳＭ−ＴＡＣＥ）／有効$", re.I).sub(u"Ｈ：ｄｅｇｒａｄａｂｌｅ＿ｓｔａｒｃｈｍｉｃｒｏｓｐｈｅｒｅｓ併用肝動注化学塞栓療法／有効", text)
        text = re.compile(u"^染色体ＦＩＳＨ＝ｔ（９；２２）／陽性$", re.I).sub(u"染色体ＦＩＳＨ＝ｔ（９；２２）／陽性", text)
        text = re.compile(u"^肺癌（扁平上皮癌）$", re.I).sub(u"肺扁平上皮癌", text)
        text = re.compile(u"^ＭＲＩ＝造影遅延（ＬＧＥ）／陰性$", re.I).sub(u"ＭＲＩ＝造影遅延／陰性", text)
        text = re.compile(u"^ＭＲＩ＝造影遅延（ＬＧＥ）／陽性$", re.I).sub(u"ＭＲＩ＝造影遅延／陽性", text)
        text = re.compile(u"^ｐｕｌｍｏｎａｒｙｔｕｍｏｒｔｈｒｏｍｂｏｔｉｃ＿ｍｉｃｒｏａｎｇｉｏｐａｔｈｙ（ＰＴＴＭ）$", re.I).sub(u"ｐｕｌｍｏｎａｒｙｔｕｍｏｒｔｈｒｏｍｂｏｔｉｃ＿ｍｉｃｒｏａｎｇｉｏｐａｔｈｙ", text)
        text = re.compile(u"^ＨｂＡ１ｃ値（酵素法）／正常$", re.I).sub(u"ＨｂＡ１ｃ値／正常", text)
        text = re.compile(u"^ＨｂＡ１ｃ（ＮＧＳＰ）／高値$", re.I).sub(u"ＨｂＡ１ｃ／高値", text)
        text = re.compile(u"^染色体検査＝ｔ（８；２１）（ｑ２２；ｑ２２）／ＲＵＮＸ１−ＲＵＮＸ１Ｔ１$", re.I).sub(u"染色体検査＝ｔ（８；２１）（ｑ２２；ｑ２２）／ＲＵＮＸ１−ＲＵＮＸ１Ｔ１", text)
        text = re.compile(u"^Ｈ：多発性骨髄腫（ＩｇＧ−λ型）　$", re.I).sub(u"Ｈ：多発性骨髄腫（ＩｇＧ−λ型）　", text)
        text = re.compile(u"^病理＝肺腫瘍血栓性微小血管症（ＰＴＴＭ）$", re.I).sub(u"病理＝肺腫瘍血栓性微小血管症", text)
        text = re.compile(u"^Ｈ：カテ−テル大動脈弁置換術（ＴＡＶＩ）／有効$", re.I).sub(u"Ｈ：カテ−テル大動脈弁置換術／有効", text)
        text = re.compile(u"^Ｈ：ステントグラフト内挿術（ＥＶＡＲ）$", re.I).sub(u"Ｈ：ステントグラフト内挿術", text)
        text = re.compile(u"^電気生理学的検査＝房室結節リエントリ−性頻拍（ＡＶＮＲＴ）$", re.I).sub(u"電気生理学的検査＝房室結節リエントリ−性頻拍", text)
        text = re.compile(u"^染色体検査＝４６，　ＸＹ，　ｄｅｌ（５）$", re.I).sub(u"染色体検査＝４６，　ＸＹ，　ｄｅｌ（５）", text)
        text = re.compile(u"^２５（ＯＨ）ＶＤ／高値$", re.I).sub(u"２５（ＯＨ）ＶＤ／高値", text)
        text = re.compile(u"^１−２５（ＯＨ）２Ｄ３／正常$", re.I).sub(u"１−２５（ＯＨ）２Ｄ３／正常", text)
        text = re.compile(u"^ＰＨ：ＳＴ上昇型急性心筋梗塞の診断で経皮的冠動脈形成術（ＰＣＩ）$", re.I).sub(u"ＰＨ：ＳＴ上昇型急性心筋梗塞の診断で経皮的冠動脈形成術", text)
        text = re.compile(u"^糖尿病性ケトアシド−シス（ＤＫＡ）$", re.I).sub(u"糖尿病性ケトアシド−シス", text)
        text = re.compile(u"^１．２５−（ＯＨ）２ＶＤ／低値$", re.I).sub(u"１．２５−（ＯＨ）２ＶＤ／低値", text)
        text = re.compile(u"^Ｈ：高用量黄体ホルモン（ＭＰＡ）療法の急な中止$", re.I).sub(u"Ｈ：高用量黄体ホルモン療法の急な中止", text)
        text = re.compile(u"^ＨＳＶ１による増殖性（過形成性）ＨＳＶ感染症$", re.I).sub(u"ＨＳＶ１による増殖性ＨＳＶ感染症", text)
        text = re.compile(u"^染色体分析＝ｔ（１４；１８）を含む複雑な異常／陽性$", re.I).sub(u"染色体分析＝ｔ（１４；１８）を含む複雑な異常／陽性", text)
        text = re.compile(u"^Ｇ−ｂａｎｄ法＝４６，ＸＹ，ｄｅｌ（５）（ｑ）＊ｄｅｌ（９）（ｑ）$", re.I).sub(u"Ｇ−ｂａｎｄ法＝４６，ＸＹ，ｄｅｌ（５）（ｑ）＊ｄｅｌ（９）（ｑ）", text)
        text = re.compile(u"^ドパミントランスポ−タ−（ＤＡＴ）シンチグラフィ＝取り込み／低下$", re.I).sub(u"ドパミントランスポ−タ−シンチグラフィ＝取り込み／低下", text)
        text = re.compile(u"^［第Ｖ因子活性］第Ｖ因子（ＦＶ）凝固活性／低下$", re.I).sub(u"［第Ｖ因子活性］第Ｖ因子凝固活性／低下", text)
        text = re.compile(u"^迅速ＡＣＴＨ負荷試験（２５０μｇ）／正常$", re.I).sub(u"迅速ＡＣＴＨ負荷試験／正常", text)
        text = re.compile(u"^迅速少量ＡＣＴＨ負荷試験（１μｇ）／正常$", re.I).sub(u"迅速少量ＡＣＴＨ負荷試験／正常", text)
        text = re.compile(u"^細胞診＝びまん性大細胞型Ｂ細胞リンパ腫（ＤＬＢＣＬ）＠〔胸水〕$", re.I).sub(u"細胞診＝びまん性大細胞型Ｂ細胞リンパ腫＠〔胸水〕", text)
        text = re.compile(u"^骨髄検査＝骨髄異形成症候群（ＭＤＳ）$", re.I).sub(u"骨髄検査＝骨髄異形成症候群", text)
        text = re.compile(u"^ペア血清＝Ａ型（Ｈ１Ｎ１）インフルエンザ抗体価／上昇$", re.I).sub(u"ペア血清＝Ａ型（Ｈ１Ｎ１）インフルエンザ抗体価／上昇", text)
        text = re.compile(u"^ＨＢＶ＿ＤＮＡ定量　（ＲＴ−ＰＣＲ）／陽性$", re.I).sub(u"ＨＢＶ＿ＤＮＡ定量　／陽性", text)
        text = re.compile(u"^Ｈ：アセトアミノフェン（ルル）大量内服$", re.I).sub(u"Ｈ：アセトアミノフェン大量内服", text)
        text = re.compile(u"^皮膚生検＝コレステロ−ル塞栓症（ＣＣＥ）$", re.I).sub(u"皮膚生検＝コレステロ−ル塞栓症", text)
        text = re.compile(u"^Ｈ：インタ−フェロン（ＩＦＮ）療法$", re.I).sub(u"Ｈ：インタ−フェロン療法", text)
        text = re.compile(u"^播種性血管内凝固（ＤＩＣ）$", re.I).sub(u"播種性血管内凝固", text)
        text = re.compile(u"^化膿性髄膜炎（細菌性髄膜炎）$", re.I).sub(u"化膿性髄膜炎", text)
        text = re.compile(u"^Ｈ：非ステロイド系抗炎症剤（ＮＳＡＩＤ）／有効$", re.I).sub(u"Ｈ：非ステロイド系抗炎症剤／有効", text)
        text = re.compile(u"^１型尿細管性アシド−シス（１型ＲＴＡ）$", re.I).sub(u"１型尿細管性アシド−シス", text)
        text = re.compile(u"^Ｏｎｅ−ａｎｄ−ａ−ｈａｌｆ−ｓｙｎｄｒｏｍｅ（ＯＡＡＨ）$", re.I).sub(u"Ｏｎｅ−ａｎｄ−ａ−ｈａｌｆ−ｓｙｎｄｒｏｍｅ", text)
        text = re.compile(u"^ＭＲＩ＝脳梗塞＠左＊橋正中腹側・傍正中橋網様体（ＰＰＲＦ）$", re.I).sub(u"ＭＲＩ＝脳梗塞＠左＊橋正中腹側・傍正中橋網様体", text)
        text = re.compile(u"^スティッフパ−ソン症候群（ＳＰＳ）$", re.I).sub(u"スティッフパ−ソン症候群", text)
        text = re.compile(u"^末梢神経伝導速度検査（ＮＣＳ）＝軸索障害$", re.I).sub(u"末梢神経伝導速度検査＝軸索障害", text)
        text = re.compile(u"^長谷川式痴呆スケ−ル（ＨＤＳ−Ｒ）／低値$", re.I).sub(u"長谷川式痴呆スケ−ル／低値", text)
        text = re.compile(u"^深在性エリテマト−デス（ｌｕｐｕｓ　ｐｒｏｆｕｎｄｕｓ）$", re.I).sub(u"深在性エリテマト−デス", text)
        text = re.compile(u"^リウマトイド因子（ＲＦ）／陽性$", re.I).sub(u"リウマトイド因子／陽性", text)
        text = re.compile(u"^［解釈：意識障害］意識レベル２（ＪＣＳ）$", re.I).sub(u"［解釈：意識障害］意識レベル２", text)
        text = re.compile(u"^急性呼吸窮迫症候群（ＡＲＤＳ）$", re.I).sub(u"急性呼吸窮迫症候群", text)
        text = re.compile(u"^好酸球塩基性蛋白（ＥＣＰ）／高値$", re.I).sub(u"好酸球塩基性蛋白／高値", text)
        text = re.compile(u"^イレウス（ａｎｔｉｃｏａｇｕｌａｎｔ＿ｉｌｅｕｓ）$", re.I).sub(u"イレウス（ａｎｔｉｃｏａｇｕｌａｎｔ＿ｉｌｅｕｓ）", text)
        text = re.compile(u"^ｖａｒｉｃｅｌｌａ−ｚｏｓｔｅｒｖｉｒｕｓ（ＶＺＶ）抗体／上昇$", re.I).sub(u"ｖａｒｉｃｅｌｌａ−ｚｏｓｔｅｒｖｉｒｕｓ抗体／上昇", text)
        text = re.compile(u"^抗血小板抗体（ＰＡＩｇＧ）／陽性$", re.I).sub(u"抗血小板抗体／陽性", text)
        text = re.compile(u"^急性骨髄性白血病（Ｍ５ａ）$", re.I).sub(u"急性骨髄性白血病", text)
        text = re.compile(u"^骨髄穿刺＝急性骨髄性白血病（Ｍ５ａ）$", re.I).sub(u"骨髄穿刺＝急性骨髄性白血病", text)
        text = re.compile(u"^フルニエ壊疽（壊死性筋膜炎）　$", re.I).sub(u"フルニエ壊疽　", text)
        text = re.compile(u"^Ｈ：ミコフェノ−ル酸モフェチル（ＭＭＦ）／有効$", re.I).sub(u"Ｈ：ミコフェノ−ル酸モフェチル／有効", text)
        text = re.compile(u"^ＭＲＩ（Ｔ２強調）＝高信号＠脳白質$", re.I).sub(u"ＭＲＩ＝Ｔ２強調　高信号＠脳白質", text)
        text = re.compile(u"^ＭＲＩ＝ＦＬＡＩＲ　高信号＠脳白質　$", re.I).sub(u"ＭＲＩ＝高信号＠脳白質　", text)
        text = re.compile(u"^傍腫瘍性小脳変性症（ＰＣＤ）$", re.I).sub(u"傍腫瘍性小脳変性症", text)
        text = re.compile(u"^培養＝スエヒロタケ（Ｓｃｈｉｚｏｐｈｙｌｌｕｍ＿ｃｏｍｍｕｎｅ）　$", re.I).sub(u"培養＝スエヒロタケ　", text)
        text = re.compile(u"^Ｈ：インタ−フェロン（ＩＦＮ）α　$", re.I).sub(u"Ｈ：インタ−フェロンα　", text)
        text = re.compile(u"^１．２５（ＯＨ）ＶＤ３／高値$", re.I).sub(u"１．２５（ＯＨ）ＶＤ３／高値", text)
        text = re.compile(u"^ＨＬＡ＝Ａ２４（９）／陽性・Ｂ５９／陽性・Ｂ５２（５）／陽性・Ｃｗ１／陽性・ＤＲ４／陽性・ＤＲ２／陽性$", re.I).sub(u"ＨＬＡ＝Ａ２４（９）／陽性・Ｂ５９／陽性・Ｂ５２（５）／陽性・Ｃｗ１／陽性・ＤＲ４／陽性・ＤＲ２／陽性", text)
        text = re.compile(u"^間質性肺炎（ＮＳＩＰ）$", re.I).sub(u"間質性肺炎", text)
        text = re.compile(u"^肺生検＝間質性肺炎像（ＮＳＩＰ）$", re.I).sub(u"肺生検＝間質性肺炎像", text)
        text = re.compile(u"^［解釈：低身長］身長１４９．６ｃｍ（−３．５ＳＤ）$", re.I).sub(u"［解釈：低身長］身長１４９．６ｃｍ", text)
        text = re.compile(u"^生検＝悪性リンパ腫（Ｄｉｆｆｕｓｅ　ｌａｒｇｅ　Ｂ　ｃｅｌｌ　ｌｙｍｐｈｏｍａ）$", re.I).sub(u"生検＝悪性リンパ腫", text)
        text = re.compile(u"^急性呼吸促迫症候群（ＡＲＤＳ）$", re.I).sub(u"急性呼吸促迫症候群", text)
        text = re.compile(u"^ホジキン病（ホジキンリンパ腫）$", re.I).sub(u"ホジキン病", text)
        text = re.compile(u"^Ｈ：経皮的心肺補助装置（ＰＣＰＳ）／有効$", re.I).sub(u"Ｈ：経皮的心肺補助装置／有効", text)
        text = re.compile(u"^染色体＝ｔ（９；２２）（ｑ３４；ｑ１１）$", re.I).sub(u"染色体＝ｔ（９；２２）（ｑ３４；ｑ１１）", text)
        text = re.compile(u"^ｆｉｎｅ　ｃｒａｃｋｌｅ（捻髪音）$", re.I).sub(u"ｆｉｎｅ　ｃｒａｃｋｌｅ", text)
        text = re.compile(u"^Ａｍｙｏｐａｔｈｉｃ　Ｄｅｒｍａｔｏｍｙｏｓｉｔｉｓ（ＡＭＤＭ）$", re.I).sub(u"Ａｍｙｏｐａｔｈｉｃ　Ｄｅｒｍａｔｏｍｙｏｓｉｔｉｓ", text)
        text = re.compile(u"^血管免疫芽球性Ｔ細胞リンパ腫（ａｎｇｉｏｉｍｍｕｎｏｂｌａｓｔｉｃ　Ｔ−ｃｅｌｌ　ｌｙｍｐｈｏｍａ）$", re.I).sub(u"血管免疫芽球性Ｔ細胞リンパ腫", text)
        text = re.compile(u"^生検＝血管免疫芽球性Ｔ細胞リンパ腫（　ａｎｇｉｏｉｍｍｕｎｏｂｌａｓｔｉｃ　Ｔ−ｃｅｌｌ　ｌｙｍｐｈｏｍａ）＠　リンパ節$", re.I).sub(u"生検＝血管免疫芽球性Ｔ細胞リンパ腫＠　リンパ節", text)
        text = re.compile(u"^生検＝悪性リンパ腫（濾胞性リンパ腫）＠腋窩リンパ節$", re.I).sub(u"生検＝悪性リンパ腫＠腋窩リンパ節", text)
        text = re.compile(u"^リウマチ性多発筋痛症（ＰＭＲ）$", re.I).sub(u"リウマチ性多発筋痛症", text)
        text = re.compile(u"^髄液培養＝Ｓｔｒｅｐｔｏｃｏｃｃｕｓ＿ａｇａｌａｃｔｉａｅ（Ｇｒｏｕｐ＿Ｂ　Ｓｔｒｅｐｔｏｃｏｃｃｕｓ）／陽性$", re.I).sub(u"髄液培養＝Ｓｔｒｅｐｔｏｃｏｃｃｕｓ＿ａｇａｌａｃｔｉａｅ／陽性", text)
        text = re.compile(u"^血液培養＝Ｓｔｒｅｐｔｏｃｏｃｃｕｓ＿ａｇａｌａｃｔｉａｅ（Ｇｒｏｕｐ＿Ｂ　Ｓｔｒｅｐｔｏｃｏｃｃｕｓ）／陽性$", re.I).sub(u"血液培養＝Ｓｔｒｅｐｔｏｃｏｃｃｕｓ＿ａｇａｌａｃｔｉａｅ／陽性", text)
        text = re.compile(u"^可逆性後頭葉白質脳症（ＰＲＥＳ）$", re.I).sub(u"可逆性後頭葉白質脳症", text)
        text = re.compile(u"^肺動脈楔入圧（Ｐｃｗｐ）／上昇$", re.I).sub(u"肺動脈楔入圧／上昇", text)
        text = re.compile(u"^緩徐進行型インスリン依存性糖尿病（ＳＰＩＤＤＭ）　$", re.I).sub(u"緩徐進行型インスリン依存性糖尿病　", text)
        text = re.compile(u"^内視鏡＝食道癌（扁平上皮癌）$", re.I).sub(u"内視鏡＝食道癌", text)
        text = re.compile(u"^病理＝肺癌（腺癌）$", re.I).sub(u"病理＝肺癌", text)
        text = re.compile(u"^生検＝亜急性壊死性リンパ節炎（菊池氏病）$", re.I).sub(u"生検＝亜急性壊死性リンパ節炎", text)
        text = re.compile(u"^ｔ（９；２２）／陽性$", re.I).sub(u"ｔ（９；２２）／陽性", text)
        text = re.compile(u"^病変径１〜４８ｍｍ（中央値１５ｍｍ）$", re.I).sub(u"病変径１〜４８ｍｍ（中央値１５ｍｍ）", text)
        text = re.compile(u"^施術時間＿２６〜３００分（中央値５６分）$", re.I).sub(u"施術時間＿２６〜３００分（中央値５６分）", text)
        text = re.compile(u"^Ｈ：遠位側胃切除術（Ｂ−Ｉ再建）$", re.I).sub(u"Ｈ：遠位側胃切除術", text)
        text = re.compile(u"^腹部単純ＣＴ＝脂肪織濃度上昇＠上腸間膜動脈（ＳＭＡ）周囲$", re.I).sub(u"腹部単純ＣＴ＝脂肪織濃度上昇＠上腸間膜動脈周囲", text)
        text = re.compile(u"^Ｈ：肝動脈化学塞栓術（ＴＡＣＥ）$", re.I).sub(u"Ｈ：肝動脈化学塞栓術", text)
        text = re.compile(u"^Ｈ：プレドニゾロン（ＰＳＬ）／有効$", re.I).sub(u"Ｈ：プレドニゾロン／有効", text)
        text = re.compile(u"^ＰＴ（％）／低値$", re.I).sub(u"ＰＴ／低値", text)
        text = re.compile(u"^ＡＭＡ（Ｍ２）陽性化$", re.I).sub(u"ＡＭＡ陽性化", text)
        text = re.compile(u"^ＭＲＩ＝Ｇｄ造影　両側神経根のガドリニウム（Ｇｄ）増強効果＠頸椎・腰椎$", re.I).sub(u"ＭＲＩ＝Ｇｄ造影　両側神経根のガドリニウム増強効果＠頸椎・腰椎", text)
        text = re.compile(u"^Ｍ蛋白血症（ＩｇＧ−κ型）／陽性$", re.I).sub(u"Ｍ蛋白血症（ＩｇＧ−κ型）／陽性", text)
        text = re.compile(u"^Ｈ：Ｐｅｇ−ＩＦＮ（１２０μｇ）／Ｒｉｂａｖｉｒｉｎ＿（８００ｍｇ）／無効　$", re.I).sub(u"Ｈ：Ｐｅｇ−ＩＦＮ／Ｒｉｂａｖｉｒｉｎ＿／無効　", text)
        text = re.compile(u"^病理組織＝ｄｉｆｆｕｓｅ　ｌａｒｇｅ　Ｂ−ｃｅｌｌ　ｌｙｍｐｈｏｍａ（ＤＬＢＣＬ）　$", re.I).sub(u"病理組織＝ｄｉｆｆｕｓｅ　ｌａｒｇｅ　Ｂ−ｃｅｌｌ　ｌｙｍｐｈｏｍａ　", text)
        text = re.compile(u"^デキサメタゾン抑制試験（１ｍｇおよび８ｍｇ）＝コルチゾ−ル抑制なし$", re.I).sub(u"デキサメタゾン抑制試験＝コルチゾ−ル抑制なし", text)
        text = re.compile(u"^筋検体の遺伝子解析＝ｍ．３２４３Ａ＞Ｇ（変異率８５％）$", re.I).sub(u"筋検体の遺伝子解析＝ｍ．３２４３Ａ＞Ｇ（変異率８５％）", text)
        text = re.compile(u"^遺伝子検査　＝ＣＰＴ２遺伝子変異（ｐ．Ｒ１５１Ｑ、ｐ．Ｒ５０３Ｈ）・長鎖アシルカルニチン／上昇$", re.I).sub(u"遺伝子検査　＝ＣＰＴ２遺伝子変異（ｐ．Ｒ１５１Ｑ、ｐ．Ｒ５０３Ｈ）・長鎖アシルカルニチン／上昇", text)
        text = re.compile(u"^経皮的肝生検＝神経内分泌腫瘍（Ｇｒａｄｅ２）$", re.I).sub(u"経皮的肝生検＝神経内分泌腫瘍", text)
        text = re.compile(u"^ＥＵＳ−ＦＮＡ＝神経内分泌腫瘍（Ｇｒａｄｅ２）$", re.I).sub(u"ＥＵＳ−ＦＮＡ＝神経内分泌腫瘍", text)
        text = re.compile(u"^ＰＲＥＳ（ｐｏｓｔｅｒｉｏｒ＿ｒｅｖｅｒｓｉｂｌｅ＿ｅｎｃｅｐｈａｌｏｐａｔｈｙ＿ｓｙｎｄｒｏｍｅ）$", re.I).sub(u"ＰＲＥＳ", text)
        text = re.compile(u"^Ｈ：ロキソプロフェンナトリウム水和物（ロキソニン）／無効$", re.I).sub(u"Ｈ：ロキソプロフェンナトリウム水和物／無効", text)
        text = re.compile(u"^Ｈ：ジクロフェナクナトリウム（ボルタレン）／有効$", re.I).sub(u"Ｈ：ジクロフェナクナトリウム／有効", text)
        text = re.compile(u"^サイトメガロウィルス（ＣＭＶ）腸炎$", re.I).sub(u"サイトメガロウィルス腸炎", text)
        text = re.compile(u"^神経内分泌腫瘍（ＮＥＴ）$", re.I).sub(u"神経内分泌腫瘍", text)
        text = re.compile(u"^Ｈ：肝動脈塞栓術（ＴＡＣＥ）　３回／有効$", re.I).sub(u"Ｈ：肝動脈塞栓術　３回／有効", text)
        text = re.compile(u"^心嚢穿刺＝細胞診ｃｌａｓｓＶ（腺癌）$", re.I).sub(u"心嚢穿刺＝細胞診ｃｌａｓｓＶ", text)
        text = re.compile(u"^抗体（ＰＡ法）ペア血清／上昇$", re.I).sub(u"抗体ペア血清／上昇", text)
        text = re.compile(u"^生検＝血管内悪性リンパ腫（ＩＶＬ）$", re.I).sub(u"生検＝血管内悪性リンパ腫", text)
        text = re.compile(u"^Ｈ：術後化学療法　（５−ＦＵ＋ＬＶ療法）　$", re.I).sub(u"Ｈ：術後化学療法　　", text)
        text = re.compile(u"^病理＝ＣＫ７（−）・ＣＫ２０（＋）・ＴＴＦ−１（＋）$", re.I).sub(u"病理＝ＣＫ７・ＣＫ２０・ＴＴＦ−１", text)
        text = re.compile(u"^国際診断基準（ＩＡＩＨＧ、１９９９）＝９点$", re.I).sub(u"国際診断基準＝９点", text)
        text = re.compile(u"^生検＝びまん性大細胞型Ｂ細胞性リンパ腫（ＤＬＢＣＬ）$", re.I).sub(u"生検＝びまん性大細胞型Ｂ細胞性リンパ腫", text)
        text = re.compile(u"^消化管間質腫瘍（Ｇａｓｔｒｏｉｎｔｅｓｔｉｎａｌ＿Ｓｔｒｏｍａｌ＿Ｔｕｍｏｒ；ＧＩＳＴ）＠胃・Ｌｉｔｔｏｒａｌ＿ｃｅｌｌ＿ａｎｇｉｏｍａ（ＬＣＡ）＠脾$", re.I).sub(u"消化管間質腫瘍＠胃・Ｌｉｔｔｏｒａｌ＿ｃｅｌｌ＿ａｎｇｉｏｍａ＠脾", text)
        text = re.compile(u"^病理＝消化管間質腫瘍（Ｇａｓｔｒｏｉｎｔｅｓｔｉｎａｌ＿Ｓｔｒｏｍａｌ＿Ｔｕｍｏｒ；ＧＩＳＴ）＠胃・Ｌｉｔｔｏｒａｌ＿ｃｅｌｌ＿ａｎｇｉｏｍａ（ＬＣＡ）＠脾$", re.I).sub(u"病理＝消化管間質腫瘍＠胃・Ｌｉｔｔｏｒａｌ＿ｃｅｌｌ＿ａｎｇｉｏｍａ＠脾", text)
        text = re.compile(u"^Ｈ：サラゾスルファピリジン（ＳＡＳＰ）／有効$", re.I).sub(u"Ｈ：サラゾスルファピリジン／有効", text)
        text = re.compile(u"^低アルブミン（Ａｌｂ）血症　$", re.I).sub(u"低アルブミン血症　", text)
        text = re.compile(u"^Ｔｏｘｉｃ　Ｓｈｏｃｋ　Ｌｉｋｅ　Ｓｙｎｄｒｏｍｅ　（ＴＳＬＳ）$", re.I).sub(u"Ｔｏｘｉｃ　Ｓｈｏｃｋ　Ｌｉｋｅ　Ｓｙｎｄｒｏｍｅ　", text)
        text = re.compile(u"^急性大動脈解離（ｓｔａｎｆｏｒｄ＿Ｂ）$", re.I).sub(u"急性大動脈解離", text)
        text = re.compile(u"^〔胃前庭部毛細血管拡張症（Ｇａｓｔｒｉｃ＿ａｎｔｒａｌ＿ｖａｓｃｕｌａｒ＿ｅｃｔａｓｉａ）〕$", re.I).sub(u"〔胃前庭部毛細血管拡張症〕", text)
        text = re.compile(u"^可逆性後頭葉白質脳（ＰＲＥＳ）$", re.I).sub(u"可逆性後頭葉白質脳", text)
        text = re.compile(u"^可逆性脳血管攣縮症候群（ＲＣＶＳ）$", re.I).sub(u"可逆性脳血管攣縮症候群", text)
        text = re.compile(u"^病理＝悪性リンパ腫（びまん性大細胞型Ｂ細胞リンパ腫）$", re.I).sub(u"病理＝悪性リンパ腫", text)
        text = re.compile(u"^捻髪音（Ｃｒｅｐｉｔａｔｉｏｎ＿Ｒａｌｅ）$", re.I).sub(u"捻髪音", text)
        text = re.compile(u"^ｃｒｏｗｎｅｄ　ｄｅｎｓ症候群（頸椎偽痛風）$", re.I).sub(u"ｃｒｏｗｎｅｄ　ｄｅｎｓ症候群", text)
        text = re.compile(u"^慢性好酸球性肺炎（ＣＥＰ）$", re.I).sub(u"慢性好酸球性肺炎", text)
        text = re.compile(u"^ＭＡＣ症（肺Ｍ．　ａｖｉｕｍ　ｃｏｍｐｌｅｘ）$", re.I).sub(u"ＭＡＣ症", text)
        text = re.compile(u"^Ｈ：ＡＦ（心房細動）$", re.I).sub(u"Ｈ：ＡＦ", text)
        text = re.compile(u"^病理解剖＝肺癌（ａｄｅｎｏｓｑｕａｍａｏｕｓ＿ｃｅｌｌ＿ｃａｒｃｉｎｏｍａ）$", re.I).sub(u"病理解剖＝肺癌", text)
        text = re.compile(u"^Ｈ：ＣＰＦＸ投与・ＥＭ（１０００ｍｇ／日）併用／有効$", re.I).sub(u"Ｈ：ＣＰＦＸ投与・ＥＭ併用／有効", text)
        text = re.compile(u"^１，２５−（ＯＨ）２Ｄ３／低値$", re.I).sub(u"１，２５−（ＯＨ）２Ｄ３／低値", text)
        text = re.compile(u"^２５−（ＯＨ）Ｄ３／低値$", re.I).sub(u"２５−（ＯＨ）Ｄ３／低値", text)
        text = re.compile(u"^Ｈ：抗菌薬（メロペネム、クリンダマイシン）／有効$", re.I).sub(u"Ｈ：抗菌薬／有効", text)
        text = re.compile(u"^Ｈ：化学療法（ＢＥＰ療法：ブレオマイシン、エトポシド、シスプラチン）／有効$", re.I).sub(u"Ｈ：化学療法／有効", text)
        text = re.compile(u"^Ｈ：化学療法（ＣＤＤＰ＋ＶＰ−１６）／有効$", re.I).sub(u"Ｈ：化学療法／有効", text)
        text = re.compile(u"^ａｍｉｏｄａｒｏｎｅ−ｉｎｄｕｃｅｄ−ｔｈｙｒｏｔｏｘｉｃｏｓｉｓ（ＴｙｐｅＩＩ破壊性甲状腺炎型）$", re.I).sub(u"ａｍｉｏｄａｒｏｎｅ−ｉｎｄｕｃｅｄ−ｔｈｙｒｏｔｏｘｉｃｏｓｉｓ", text)
        text = re.compile(u"^肝生検＝線維化＊（Ｆ３）$", re.I).sub(u"肝生検＝線維化", text)
        text = re.compile(u"^肝細胞癌（ＨＣＣ）$", re.I).sub(u"肝細胞癌", text)
        text = re.compile(u"^Ｈ：部分的脾動脈塞栓術（ＰＳＥ）　$", re.I).sub(u"Ｈ：部分的脾動脈塞栓術　", text)
        text = re.compile(u"^特異的ＩｇＥ（ＩｇＥ＿ＲＡＳＴ）／陽性$", re.I).sub(u"特異的ＩｇＥ／陽性", text)
        text = re.compile(u"^Ａｓｐｅｒｇｉｌｌｕｓ（Ａ）・Ｐｅｎｉｃｉｌｌｉｕｍ（Ｐ）＿ＩｇＥ＿ＲＡＳＴ／陽性$", re.I).sub(u"Ａｓｐｅｒｇｉｌｌｕｓ・Ｐｅｎｉｃｉｌｌｉｕｍ＿ＩｇＥ＿ＲＡＳＴ／陽性", text)
        text = re.compile(u"^Ａ＿ｎｉｇｅｒ（ｎｉｇ）・Ｐｅｎｉｃｉｌｌｉｕｍ（Ｐ）＿沈降抗体／陽性$", re.I).sub(u"Ａ＿ｎｉｇｅｒ・Ｐｅｎｉｃｉｌｌｉｕｍ＿沈降抗体／陽性", text)
        text = re.compile(u"^喀痰・気管痰培養＝Ａ＿ｎｉｇｅｒ（ｎｉｇ）・Ｐｅｎｉｃｉｌｌｉｕｍ（Ｐ）／陽性$", re.I).sub(u"喀痰・気管痰培養＝Ａ＿ｎｉｇｅｒ・Ｐｅｎｉｃｉｌｌｉｕｍ／陽性", text)
        text = re.compile(u"^Ｈ：プロスタサイクリン　（ＰＧＩ２）　誘導体徐放性製／有効$", re.I).sub(u"Ｈ：プロスタサイクリン　　誘導体徐放性製／有効", text)
        text = re.compile(u"^染色体検査＝４６，ＸＹ＋１，ｄｅｒ（１；７）（ｑ１０；ｐ１０）／陽性$", re.I).sub(u"染色体検査＝４６，ＸＹ＋１，ｄｅｒ／陽性", text)
        text = re.compile(u"^骨髄＝ｄｅｌ（２０）（ｑ１１．２ｑ１３．３）$", re.I).sub(u"骨髄＝ｄｅｌ（２０）（ｑ１１．２ｑ１３．３）", text)
        text = re.compile(u"^脳波＝周期性同期性放電（ＰＳＤ）／陰性$", re.I).sub(u"脳波＝周期性同期性放電／陰性", text)
        text = re.compile(u"^遺伝子検索＝３２４３（Ａ−Ｇ）点変異／陽性$", re.I).sub(u"遺伝子検索＝３２４３（Ａ−Ｇ）点変異／陽性", text)
        text = re.compile(u"^神経伝導検査＝複合筋活動電位（ＣＭＡＰ）の減弱＠正中・尺骨・橈骨神経$", re.I).sub(u"神経伝導検査＝複合筋活動電位の減弱＠正中・尺骨・橈骨神経", text)
        text = re.compile(u"^１，２５−（ＯＨ）２ＶｉｔＤ／正常$", re.I).sub(u"１，２５−（ＯＨ）２ＶｉｔＤ／正常", text)
        text = re.compile(u"^染色体＝ｔ（３；１４）（ｑ２７；ｑ３２）$", re.I).sub(u"染色体＝ｔ（３；１４）（ｑ２７；ｑ３２）", text)
        text = re.compile(u"^脳波＝両側独立性周期性一側性てんかん型放電（ＢＩＰＬＥＤｓ）$", re.I).sub(u"脳波＝両側独立性周期性一側性てんかん型放電", text)
        text = re.compile(u"^骨髄穿刺＝ＭＤＳ（ＲＡＲＳ）　$", re.I).sub(u"骨髄穿刺＝ＭＤＳ（ＲＡＲＳ）　", text)
        text = re.compile(u"^宿便性大腸炎（Ｓｔｅｒｃｏｒａｌ　ｃｏｌｉｔｉｓ）$", re.I).sub(u"宿便性大腸炎", text)
        text = re.compile(u"^電気生理検査（ＥＰＳ）＝ＡＨ時間／上昇$", re.I).sub(u"電気生理検査＝ＡＨ時間／上昇", text)
        text = re.compile(u"^電気生理検査（ＥＰＳ）＝ＨＶ時間／上昇$", re.I).sub(u"電気生理検査＝ＨＶ時間／上昇", text)
        text = re.compile(u"^術中所見＝ｐｅｎｅｔｒａｔｉｎｇ＿ａｔｈｅｒｏｓｃｌｅｒｏｔｉｃ＿ｕｌｃｅｒ（ＰＡＵ）＠大弯側$", re.I).sub(u"術中所見＝ｐｅｎｅｔｒａｔｉｎｇ＿ａｔｈｅｒｏｓｃｌｅｒｏｔｉｃ＿ｕｌｃｅｒ＠大弯側", text)
        text = re.compile(u"^Ｈ：修正型電気痙攀療法（ｍＥＣＴ）$", re.I).sub(u"Ｈ：修正型電気痙攀療法", text)
        text = re.compile(u"^Ｈ：スミチオン（Ｒ）（フェニトロチオン）服毒$", re.I).sub(u"Ｈ：スミチオン服毒", text)
        text = re.compile(u"^血漿レニン活性（ＰＲＡ）／低下$", re.I).sub(u"血漿レニン活性／低下", text)
        text = re.compile(u"^１，２５＿（ＯＨ）２ＶｉｔＤ／低下$", re.I).sub(u"１，２５＿（ＯＨ）２ＶｉｔＤ／低下", text)
        text = re.compile(u"^左上肢（Ｃ５−６レベル）帯状疱疹後神経痛$", re.I).sub(u"左上肢帯状疱疹後神経痛", text)
        text = re.compile(u"^心エコ−＝デルタＰ（ＴＲ）／高値$", re.I).sub(u"心エコ−＝デルタＰ／高値", text)
        text = re.compile(u"^頭部ＭＲＩ＝拡散強調画像（ＤＷＩ）高信号病変＠両側＊高位円蓋部$", re.I).sub(u"頭部ＭＲＩ＝拡散強調画像高信号病変＠両側＊高位円蓋部", text)
        text = re.compile(u"^ＤＮＡ解析＝変異型ｆｏｌｌｉｃｕｌｉｎ遺伝子（ｅｘｏｎ１１のｃ．１２８５ｄｕｐＣ）$", re.I).sub(u"ＤＮＡ解析＝変異型ｆｏｌｌｉｃｕｌｉｎ遺伝子（ｅｘｏｎ１１のｃ．１２８５ｄｕｐＣ）", text)
        text = re.compile(u"^ＣＴ（単純）＝腫瘤＠肝　$", re.I).sub(u"単純ＣＴ＝腫瘤＠肝　", text)
        text = re.compile(u"^血液培養・カテ先培養＝Ｓｔａｐｈｙｌｏｃｏｃｃｕｓ（ＣＮＳ）／陽性$", re.I).sub(u"血液培養・カテ先培養＝Ｓｔａｐｈｙｌｏｃｏｃｃｕｓ／陽性", text)
        text = re.compile(u"^血液培養＝Ｓｔｒｅｐｔｏｃｏｃｃｕｓ＿ｐｙｏｇｅｎｅｓ（Ａ群）／陽性$", re.I).sub(u"血液培養＝Ｓｔｒｅｐｔｏｃｏｃｃｕｓ＿ｐｙｏｇｅｎｅｓ／陽性", text)
        text = re.compile(u"^ウイルス関連血球貪食症候群（ＶＨＡＳ）$", re.I).sub(u"ウイルス関連血球貪食症候群", text)
        text = re.compile(u"^上部消化管内視鏡検査＝食道カンジダ（ｇｒａｄｅ２）$", re.I).sub(u"上部消化管内視鏡検査＝食道カンジダ", text)
        text = re.compile(u"^〔腹腔−静脈シャント（Ｐ−Ｖシャント）副作用〕$", re.I).sub(u"〔腹腔−静脈シャント副作用〕", text)
        text = re.compile(u"^Ｂｉｒｔ−Ｈｏｇｇ−Ｄｕｂ＿症候群（ＢＨＤ）$", re.I).sub(u"Ｂｉｒｔ−Ｈｏｇｇ−Ｄｕｂ＿症候群", text)
        text = re.compile(u"^肺リンパ脈管筋腫症（ＬＡＭ）$", re.I).sub(u"肺リンパ脈管筋腫症", text)
        text = re.compile(u"^ＥＧＦＲｍｕｔａｎｔ（ｄｅｌｅｔｉｏｎ１９）　$", re.I).sub(u"ＥＧＦＲｍｕｔａｎｔ（ｄｅｌｅｔｉｏｎ１９）　", text)
        text = re.compile(u"^結核菌遺伝子増幅法（ＰＣＲ法）／陽性$", re.I).sub(u"結核菌遺伝子増幅法／陽性", text)
        text = re.compile(u"^Ｈ：肝動脈化学塞栓療法（ＴＡＣＥ）・ラジオ波焼灼療法の施行困難$", re.I).sub(u"Ｈ：肝動脈化学塞栓療法・ラジオ波焼灼療法の施行困難", text)
        text = re.compile(u"^ａｐｎｅａｈｙｐｏｐｎｅａｉｎｄｅｘ（ＡＨＩ）／陽性$", re.I).sub(u"ａｐｎｅａｈｙｐｏｐｎｅａｉｎｄｅｘ／陽性", text)
        text = re.compile(u"^気管支肺胞洗浄（ＢＡＬ）＝淡血性$", re.I).sub(u"気管支肺胞洗浄＝淡血性", text)
        text = re.compile(u"^気管支肺胞洗浄（ＢＡＬ）＝リンパ球優位$", re.I).sub(u"気管支肺胞洗浄＝リンパ球優位", text)
        text = re.compile(u"^ｐｄｍ＿ＰＣＲ＝インフルエンザＡ（Ｈ１Ｎ１）／陽性$", re.I).sub(u"ｐｄｍ＿ＰＣＲ＝インフルエンザＡ／陽性", text)
        text = re.compile(u"^血液培養＝Ａ群β溶連菌（Ｓｔｒｅｐｔｏｃｏｃｃｕｓ＿ｐｙｏｇｅｎｅｓ）／陽性　　$", re.I).sub(u"血液培養＝Ａ群β溶連菌／陽性　　", text)
        text = re.compile(u"^Ｈ：大動脈弁置換術（ＡＶＲ）$", re.I).sub(u"Ｈ：大動脈弁置換術", text)
        text = re.compile(u"^ＰＴ（％）／低下$", re.I).sub(u"ＰＴ／低下", text)
        text = re.compile(u"^Ｈ：内視鏡的粘膜下層剥離術（ＥＳＤ）$", re.I).sub(u"Ｈ：内視鏡的粘膜下層剥離術", text)
        text = re.compile(u"^ヘリコバクタ−ピロリ（ＨＰ）菌／陽性$", re.I).sub(u"ヘリコバクタ−ピロリ菌／陽性", text)
        text = re.compile(u"^心筋シンチグラフィ−（安静Ｔｃ）＝低潅流$", re.I).sub(u"心筋シンチグラフィ−＝低潅流", text)
        text = re.compile(u"^上腸間膜動脈（ＳＭＡ）閉塞$", re.I).sub(u"上腸間膜動脈閉塞", text)
        text = re.compile(u"^下腸間膜動脈（ＩＭＡ）狭窄$", re.I).sub(u"下腸間膜動脈狭窄", text)
        text = re.compile(u"^心エコ−＝僧房弁の収縮期前方運動（ＳＡＭ）$", re.I).sub(u"心エコ−＝僧房弁の収縮期前方運動", text)
        text = re.compile(u"^大動脈弁狭窄症（ＡＳ）$", re.I).sub(u"大動脈弁狭窄症", text)
        text = re.compile(u"^Ｈ：家族性アミロイドポリニュ−ロパチ−（ＴＴＲ−ＦＡＰ）$", re.I).sub(u"Ｈ：家族性アミロイドポリニュ−ロパチ−", text)
        text = re.compile(u"^〔胸部レントゲン〕＝心胸郭比（ＣＴＲ）／上昇$", re.I).sub(u"〔胸部レントゲン〕＝心胸郭比／上昇", text)
        text = re.compile(u"^〔心エコ−〕＝左室駆出率（ＬＶＥＦ）／低下$", re.I).sub(u"〔心エコ−〕＝左室駆出率／低下", text)
        text = re.compile(u"^僧帽弁閉鎖不全症（ｔｒｉｖｉａｌ）$", re.I).sub(u"僧帽弁閉鎖不全症", text)
        text = re.compile(u"^ＦＩＳＨ＝ｄｅｌ（５ｑ）$", re.I).sub(u"ＦＩＳＨ＝ｄｅｌ（５ｑ）", text)
        text = re.compile(u"^骨髄穿刺＝ＭＤＳ（ＲＡＲＳ）$", re.I).sub(u"骨髄穿刺＝ＭＤＳ", text)
        text = re.compile(u"^１，２５（ＯＨ）２　ビタミンＤ／低値$", re.I).sub(u"１，２５（ＯＨ）２　ビタミンＤ／低値", text)
        text = re.compile(u"^１．２５−（ＯＨ）Ｖｉｔ．Ｄ／低値$", re.I).sub(u"１．２５−（ＯＨ）Ｖｉｔ．Ｄ／低値", text)
        text = re.compile(u"^染色体検査＝ｄｅｒ（１４）ｔ（６；１４）（ｐ２１；ｑ３２）$", re.I).sub(u"染色体検査＝ｄｅｒ（１４）ｔ（６；１４）（ｐ２１；ｑ３２）", text)
        text = re.compile(u"^ｉｎｆｌａｍｍａｔｏｒｙ＿ｍｙｏｇｌａｎｄｕｌａｒ＿ｐｏｌｙｐ（$", re.I).sub(u"ｉｎｆｌａｍｍａｔｏｒｙ＿ｍｙｏｇｌａｎｄｕｌａｒ＿ｐｏｌｙｐ", text)
        text = re.compile(u"^１，２５（ＯＨ）２Ｄ３／上昇$", re.I).sub(u"１，２５（ＯＨ）２Ｄ３／上昇", text)
        text = re.compile(u"^１，２５（ＯＨ）２ｖｉｔ．Ｄ３／上昇$", re.I).sub(u"１，２５（ＯＨ）２ｖｉｔ．Ｄ３／上昇", text)
        text = re.compile(u"^１，２５−（ＯＨ）２＿Ｖｉｔ．Ｄ／上昇$", re.I).sub(u"１，２５−（ＯＨ）２＿Ｖｉｔ．Ｄ／上昇", text)
        text = re.compile(u"^ＭＲＩ（Ｔ１強調画像）＝後葉高信号／消失$", re.I).sub(u"ＭＲＩ＝Ｔ１強調画像　後葉高信号／消失", text)
        text = re.compile(u"^Ｇ−ｂａｎｄ＝ｔ（１６；１６）$", re.I).sub(u"Ｇ−ｂａｎｄ＝ｔ（１６；１６）", text)
        text = re.compile(u"^Ｇ−ｂａｎｄ＝ｉｎｖ（１６）$", re.I).sub(u"Ｇ−ｂａｎｄ＝ｉｎｖ（１６）", text)
        text = re.compile(u"^［インフルエンザＡ（Ｈ１Ｎ１）抗体価］Ａ型Ｈ１Ｎ１に対する抗体価／上昇＝４倍以上$", re.I).sub(u"［インフルエンザＡ抗体価］Ａ型Ｈ１Ｎ１に対する抗体価／上昇＝４倍以上", text)
        text = re.compile(u"^２５（ＯＨ）ｖｉｔａｍｉｎ＿Ｄ／低値$", re.I).sub(u"２５（ＯＨ）ｖｉｔａｍｉｎ＿Ｄ／低値", text)
        text = re.compile(u"^血液＝２５（ＯＨ）Ｄ／低値$", re.I).sub(u"血液＝２５（ＯＨ）Ｄ／低値", text)
        text = re.compile(u"^２５（ＯＨ）Ｄ／低値$", re.I).sub(u"２５（ＯＨ）Ｄ／低値", text)
        text = re.compile(u"^免疫染色＝ｓｙｎａｐｔｏｐｈｙｓｉｎ（＋）＠隆起性病変＠十二指腸球部$", re.I).sub(u"免疫染色＝ｓｙｎａｐｔｏｐｈｙｓｉｎ（＋）＠隆起性病変＠十二指腸球部", text)
        text = re.compile(u"^Ｈ：胃癌（Ｓｔａｇｅ＿ＩＩＩＡ）$", re.I).sub(u"Ｈ：胃癌", text)
        text = re.compile(u"^ＰＨ：腎不全（糖尿病性腎症）$", re.I).sub(u"ＰＨ：腎不全", text)
        text = re.compile(u"^肝生検＝Ｃ−ＣＨ（Ａ１、Ｆ１）$", re.I).sub(u"肝生検＝Ｃ−ＣＨ（Ａ１、Ｆ１）", text)
        text = re.compile(u"^ＦＩＰ１Ｌ１−ＰＤＧＦＲα（ＦＰ）遺伝子／陽性$", re.I).sub(u"ＦＩＰ１Ｌ１−ＰＤＧＦＲα遺伝子／陽性", text)
        text = re.compile(u"^ｔ（１１；１４）（ｑ１３；ｑ３２）／陽性$", re.I).sub(u"ｔ（１１；１４）（ｑ１３；ｑ３２）／陽性", text)
        text = re.compile(u"^甲状腺ペルオキシダ−ゼ抗体（／陽性$", re.I).sub(u"甲状腺ペルオキシダ−ゼ抗体／陽性", text)
        text = re.compile(u"^４６，ＸＸ＿ｔ（８；２１）（ｑ２２：ｑ２２）２０／２０$", re.I).sub(u"４６，ＸＸ＿ｔ（８；２１）（ｑ２２：ｑ２２）２０／２０", text)
        text = re.compile(u"^免疫染色＝ＣＤ１９・ＣＤ２０（＋）／陽性$", re.I).sub(u"免疫染色＝ＣＤ１９・ＣＤ２０（＋）／陽性", text)
        text = re.compile(u"^デキサメサゾン（ＤＥＸ）１ｍｇ＝有意に抑制$", re.I).sub(u"デキサメサゾン１ｍｇ＝有意に抑制", text)
        text = re.compile(u"^上部内視鏡検査＝２型進行癌（ｔｕｂ２）＠胃前庭部後壁$", re.I).sub(u"上部内視鏡検査＝２型進行癌＠胃前庭部後壁", text)
        text = re.compile(u"^高カルシウム（Ｃａ）血症$", re.I).sub(u"高カルシウム血症", text)
        text = re.compile(u"^左右ＰＡＣ／コルチゾル（Ｆ）比／上昇$", re.I).sub(u"左右ＰＡＣ／コルチゾル比／上昇", text)
        text = re.compile(u"^肝生検＝Ｃ−ＣＨ（Ｆ１／Ａ１）$", re.I).sub(u"肝生検＝Ｃ−ＣＨ（Ｆ１／Ａ１）", text)
        text = re.compile(u"^右＊胸膜生検＝悪性中皮腫（びまん性、上皮型、早期浸潤）$", re.I).sub(u"右＊胸膜生検＝悪性中皮腫", text)
        text = re.compile(u"^四者負荷試験（ＣＲＨ，ＴＲＨ，ＣＲＨ，＿ＬＨＲＨ）＝ＡＣＴＨのみ無反応$", re.I).sub(u"四者負荷試験＝ＡＣＴＨのみ無反応", text)
        text = re.compile(u"^肝生検＝ＣＨ（Ａ１／Ｆ２）$", re.I).sub(u"肝生検＝ＣＨ（Ａ１／Ｆ２）", text)
        text = re.compile(u"^抗アクアポリン（ＡＱＰ）４抗体／陽性$", re.I).sub(u"抗アクアポリン４抗体／陽性", text)
        text = re.compile(u"^染色体分析＝ｔ（９；２２；４；１２；７）／陽性$", re.I).sub(u"染色体分析＝ｔ（９；２２；４；１２；７）／陽性", text)
        text = re.compile(u"^原発性胆汁性胆管炎（ＰＢＣ）$", re.I).sub(u"原発性胆汁性胆管炎", text)
        text = re.compile(u"^肝生検＝慢性非化膿性破壊性胆管炎（ＣＮＳＤＣ）$", re.I).sub(u"肝生検＝慢性非化膿性破壊性胆管炎", text)
        text = re.compile(u"^ｔ（８；２１）（ｑ２２，ｑ２２）／陽性$", re.I).sub(u"ｔ（８；２１）（ｑ２２，ｑ２２）／陽性", text)
        text = re.compile(u"^髄液ＨＳＶＤＮＡ（ＰＣＲ）／陰性$", re.I).sub(u"髄液ＨＳＶＤＮＡ／陰性", text)
        text = re.compile(u"^染色体検査＝ｔ（８；１４）（ｑ２４；ｑ３２）／陽性$", re.I).sub(u"染色体検査＝ｔ（８；１４）（ｑ２４；ｑ３２）／陽性", text)
        text = re.compile(u"^１，２５−（ＯＨ）２ビタミンＤ／正常$", re.I).sub(u"１，２５−（ＯＨ）２ビタミンＤ／正常", text)
        text = re.compile(u"^染色体分析＝ｔ（８；２１）（ｑ２２；ｑ２２）／陽性$", re.I).sub(u"染色体分析＝ｔ（８；２１）（ｑ２２；ｑ２２）／陽性", text)
        text = re.compile(u"^１α、２５（ＯＨ）ビタミンＤ／正常$", re.I).sub(u"１α、２５（ＯＨ）ビタミンＤ／正常", text)
        text = re.compile(u"^２５（ＯＨ）ビタミンＤ／低値$", re.I).sub(u"２５（ＯＨ）ビタミンＤ／低値", text)
        text = re.compile(u"^染色体検査＝ｔ（８；２１）$", re.I).sub(u"染色体検査＝ｔ（８；２１）", text)
        text = re.compile(u"^染色体検査＝ｔ（９：２２）／陽性$", re.I).sub(u"染色体検査＝ｔ（９：２２）／陽性", text)
        text = re.compile(u"^１α・２５−（ＯＨ）２／正常$", re.I).sub(u"１α・２５−（ＯＨ）２／正常", text)
        text = re.compile(u"^Ｇ−ｂａｎｄｉｎｇ＝ｔ（５；１７；１５）・ｉｄｅｍ，ａｄｄ（１３）（ｐ１１）$", re.I).sub(u"Ｇ−ｂａｎｄｉｎｇ＝ｔ（５；１７；１５）・ｉｄｅｍ，ａｄｄ（１３）（ｐ１１）", text)
        text = re.compile(u"^染色体分析＝ｔ（１４；１８）（ｑ３２；ｑ２１）$", re.I).sub(u"染色体分析＝ｔ（１４；１８）（ｑ３２；ｑ２１）", text)
        text = re.compile(u"^染色体分析＝４６，ＸＹ，ｔｒｐ（１）（ｑ２１ｑ３２）、４６，ＸＹ，ｄｕｐ（１）（ｑ２１ｑ３２）$", re.I).sub(u"染色体分析＝４６，ＸＹ，ｔｒｐ（１）（ｑ２１ｑ３２）、４６，ＸＹ，ｄｕｐ（１）（ｑ２１ｑ３２）", text)
        text = re.compile(u"^ｉｎｔａｃｔ−ＰＴＨ・ＰＴＨｒＰ・１，２５−（ＯＨ）２ビタミンＤ／正常$", re.I).sub(u"ｉｎｔａｃｔ−ＰＴＨ・ＰＴＨｒＰ・１，２５−（ＯＨ）２ビタミンＤ／正常", text)
        text = re.compile(u"^ＭＲＩ（ＤＷＩ）＝高信号＠左延髄内側$", re.I).sub(u"ＭＲＩ＝高信号＠左延髄内側", text)
        text = re.compile(u"^抗核抗体（ｄｉｓｃｒｅｔｅｓｐｅｃｋｌｅｄｔｙｐｅ）／上昇$", re.I).sub(u"抗核抗体（ｄｉｓｃｒｅｔｅｓｐｅｃｋｌｅｄｔｙｐｅ）／上昇", text)
        text = re.compile(u"^染色体分析＝ｔ（９；２２）（ｑ３４；ｑ１１）$", re.I).sub(u"染色体分析＝ｔ（９；２２）（ｑ３４；ｑ１１）", text)
        text = re.compile(u"^染色体＝４４，ＸＹ、ａｄｄ（３）（ｑ２７）、−４，ａｄｄ（８）（ｐ１１．２）、−９，ａｄｄ（９）（ｐｌ３）$", re.I).sub(u"染色体＝４４，ＸＹ・ａｄｄ（３）（ｑ２７）・−４，ａｄｄ（８）（ｐ１１．２）・−９，ａｄｄ（９）（ｐｌ３）", text)
        text = re.compile(u"^ｔ（１５；１７）／陽性$", re.I).sub(u"ｔ（１５；１７）／陽性", text)
        text = re.compile(u"^骨髄染色体分析＝ｔ（４；２１；８）（ｑ２５；ｑ２２；ｑ２２）$", re.I).sub(u"骨髄染色体分析＝ｔ（４；２１；８）（ｑ２５；ｑ２２；ｑ２２）", text)
        text = re.compile(u"^染色体検査＝ｔ（８；２１）（ｑ２２；ｑ２２）$", re.I).sub(u"染色体検査＝ｔ（８；２１）（ｑ２２；ｑ２２）", text)
        text = re.compile(u"^ＩｇＥ（ＲＩＳＴ）／高値$", re.I).sub(u"ＩｇＥ／高値", text)
        text = re.compile(u"^ベ−タ鎖のＤＮＡ塩基配列の解析＝ＣＤ６１＿ＡＡＧ（Ｌｙｓ）変異$", re.I).sub(u"ベ−タ鎖のＤＮＡ塩基配列の解析＝ＣＤ６１＿ＡＡＧ変異", text)
        text = re.compile(u"^１，２５（ＯＨ）２ＶＤ３／正常$", re.I).sub(u"１，２５（ＯＨ）２ＶＤ３／正常", text)
        text = re.compile(u"^遺伝子検査＝１９ｐ１３（ＬＹＬ）・染色体異常・ＴＣＲβ遺伝子再構成$", re.I).sub(u"遺伝子検査＝１９ｐ１３（ＬＹＬ）・染色体異常・ＴＣＲβ遺伝子再構成", text)
        text = re.compile(u"^生検＝表面形質　ＣＤ１３８・ＩｇＭ（λ）／陽性＠形質細胞$", re.I).sub(u"生検＝表面形質　ＣＤ１３８・ＩｇＭ（λ）／陽性＠形質細胞", text)
        text = re.compile(u"^抗ＳＳ−Ａ（＋）、／陽性$", re.I).sub(u"抗ＳＳ−Ａ／陽性", text)
        text = re.compile(u"^培養＝カンジダ（Ｃ．＿ａｌｂｉｃａｎｓ）＠咽頭$", re.I).sub(u"培養＝カンジダ＠咽頭", text)
        text = re.compile(u"^培養＝レンサ球菌（Ｓ．＿ｇｏｒｄｏｎｉｉ）＠咽頭$", re.I).sub(u"培養＝レンサ球菌＠咽頭", text)
        text = re.compile(u"^ＭＲＩ（ＤＷＩ）＝高信号＠左前頭葉運動野$", re.I).sub(u"ＭＲＩ＝高信号＠左前頭葉運動野", text)
        text = re.compile(u"^血液＝血清アルドステロン値（ＰＡＣ）／高値$", re.I).sub(u"血液＝血清アルドステロン値／高値", text)
        text = re.compile(u"^血液＝血漿レニン活性（ＰＲＡ）／正常$", re.I).sub(u"血液＝血漿レニン活性／正常", text)
        text = re.compile(u"^１，２５−（ＯＨ）２ビタミンＤ／低値$", re.I).sub(u"１，２５−（ＯＨ）２ビタミンＤ／低値", text)
        text = re.compile(u"^病理＝Ａｄｅｎｏｃａｒｃｉｎｏｍａ，ｔｕｂ１，ｐＴｉｓ（Ｍ）、＿ｌｙ０，＿ｖ０，＿ｐＨＭ０，＿ｐＶＭ０$", re.I).sub(u"病理＝Ａｄｅｎｏｃａｒｃｉｎｏｍａ，ｔｕｂ１，ｐＴｉｓ（Ｍ）、＿ｌｙ０，＿ｖ０，＿ｐＨＭ０，＿ｐＶＭ０", text)
        text = re.compile(u"^抗利尿ホルモン不適合分泌症候群（ＳＩＡＤＨ）$", re.I).sub(u"抗利尿ホルモン不適合分泌症候群", text)
        text = re.compile(u"^Ｈ：ｓｉｍｅｐｒｅｖｉｒ（ＳＭＶ）＋ＰＥＧ−ＩＦＮ＋ＲＢＶ３剤併用療法／無効$", re.I).sub(u"Ｈ：ｓｉｍｅｐｒｅｖｉｒ＋ＰＥＧ−ＩＦＮ＋ＲＢＶ３剤併用療法／無効", text)
        text = re.compile(u"^Ｈ：ｓｏｆｏｓｂｕｖｉｒ（ＳＯＦ）＋ｌｅｄｉｐａｓｖｉｒ＿（ＬＤＶ）併用療法／無効$", re.I).sub(u"Ｈ：ｓｏｆｏｓｂｕｖｉｒ＋ｌｅｄｉｐａｓｖｉｒ＿併用療法／無効", text)
        text = re.compile(u"^デキサメサゾン（１ｍｇ、８ｍｇ）抑制試験＝性腺ホルモン／正常$", re.I).sub(u"デキサメサゾン抑制試験＝性腺ホルモン／正常", text)
        text = re.compile(u"^〔高Ｌｐ（ａ）血症＊家族歴〕$", re.I).sub(u"〔高Ｌｐ（ａ）血症＊家族歴〕", text)
        text = re.compile(u"^高Ｌｐ（ａ）血症$", re.I).sub(u"高Ｌｐ（ａ）血症", text)
        text = re.compile(u"^染色体＝Ｄｏｕｂｌｅ＿ｔ（１５；１７）$", re.I).sub(u"染色体＝Ｄｏｕｂｌｅ＿ｔ（１５；１７）", text)
        text = re.compile(u"^染色体検査＝ｔ（１１；１９）（ｑ２３；ｐ１３．１）$", re.I).sub(u"染色体検査＝ｔ（１１；１９）（ｑ２３；ｐ１３．１）", text)
        text = re.compile(u"^２５（ＯＨ）ビタミンＤ／低下$", re.I).sub(u"２５（ＯＨ）ビタミンＤ／低下", text)
        text = re.compile(u"^１，２５（ＯＨ）２ｖＤ／正常$", re.I).sub(u"１，２５（ＯＨ）２ｖＤ／正常", text)
        text = re.compile(u"^蛋白尿（＋／−）$", re.I).sub(u"蛋白尿", text)
        text = re.compile(u"^１，２５（ＯＨ）２Ｄ３／正常$", re.I).sub(u"１，２５（ＯＨ）２Ｄ３／正常", text)
        text = re.compile(u"^２５（ＯＨ）Ｄ３／低下$", re.I).sub(u"２５（ＯＨ）Ｄ３／低下", text)
        text = re.compile(u"^ＰＴ（ＩＮＲ）／上昇$", re.I).sub(u"ＰＴ／上昇", text)
        text = re.compile(u"^ＰＴ（ＩＮＲ）／正常$", re.I).sub(u"ＰＴ／正常", text)
        text = re.compile(u"^骨髄＝４６，ＸＸ，ｄｅｌ（２０）（ｑ１１ｑ１３．３）$", re.I).sub(u"骨髄＝４６，ＸＸ，ｄｅｌ（２０）（ｑ１１ｑ１３．３）", text)
        text = re.compile(u"^ヒトパルボウイルス（ＨＰＶ）Ｂ１９−ＩｇＭ抗体／陽性$", re.I).sub(u"ヒトパルボウイルスＢ１９−ＩｇＭ抗体／陽性", text)
        text = re.compile(u"^遺伝子検査＝βグロビン遺伝子変異β２６（Ｂ８）＿Ｇｌｕ→Ｌｙｓ　／陽性$", re.I).sub(u"遺伝子検査＝βグロビン遺伝子変異β２６（Ｂ８）＿Ｇｌｕ→Ｌｙｓ　／陽性", text)
        text = re.compile(u"^免疫組織化学染色＝ＣＤ４（−）$", re.I).sub(u"免疫組織化学染色＝ＣＤ４（−）", text)
        text = re.compile(u"^免疫組織化学染色＝ＣＤ８（＋）$", re.I).sub(u"免疫組織化学染色＝ＣＤ８（＋）", text)
        text = re.compile(u"^免疫組織化学染色＝ＣＤ５６（−）$", re.I).sub(u"免疫組織化学染色＝ＣＤ５６（−）", text)
        text = re.compile(u"^免疫組織化学染色＝ＣＴＭ（＋）$", re.I).sub(u"免疫組織化学染色＝ＣＴＭ（＋）", text)
        text = re.compile(u"^骨髄＝ｔ（９；２１）（ｑ３４；ｑ１１．２）　$", re.I).sub(u"骨髄＝ｔ（９；２１）（ｑ３４；ｑ１１．２）　", text)
        text = re.compile(u"^リンパ節生検＝ｔ（９；２１）（ｑ３４；ｑ１１．２）$", re.I).sub(u"リンパ節生検＝ｔ（９；２１）（ｑ３４；ｑ１１．２）", text)
        text = re.compile(u"^特発性血小板減少性紫斑病（ＩＴＰ）$", re.I).sub(u"特発性血小板減少性紫斑病", text)
        text = re.compile(u"^ＨＰＶＢ１９ＤＮＡ（ＰＣＲ）／陽性$", re.I).sub(u"ＨＰＶＢ１９ＤＮＡ／陽性", text)
        text = re.compile(u"^尿中Ｂｅｎｓ＿Ｊｏｎｅｓ蛋白（ＩｇＧ−κ）／陽性$", re.I).sub(u"尿中Ｂｅｎｓ＿Ｊｏｎｅｓ蛋白（ＩｇＧ−κ）／陽性", text)
        text = re.compile(u"^生検＝ＨＥＲ−２（ＩＨＣ２＋、ＦＩＳＨ−）$", re.I).sub(u"生検＝ＨＥＲ−２（ＩＨＣ２＋、ＦＩＳＨ−）", text)
        text = re.compile(u"^ＣＤ２０（＋）、ＣＤ５（＋）$", re.I).sub(u"ＣＤ２０（＋）、ＣＤ５（＋）", text)
        text = re.compile(u"^ＩＣＧ（１５）／高値$", re.I).sub(u"ＩＣＧ／高値", text)
        text = re.compile(u"^抗ミエリンオリゴデンドロサイト糖タンパク質（ＭＯＧ）抗体／陽性$", re.I).sub(u"抗ミエリンオリゴデンドロサイト糖タンパク質抗体／陽性", text)
        text = re.compile(u"^染色体検査＝ａｄｄ（３）（ｐ２１）／陽性$", re.I).sub(u"染色体検査＝ａｄｄ（３）（ｐ２１）／陽性", text)
        text = re.compile(u"^１，２５（ＯＨ）２Ｄ３／低値$", re.I).sub(u"１，２５（ＯＨ）２Ｄ３／低値", text)
        text = re.compile(u"^リンパ節生検＝Ｔ−ＬＢＬ（ＴｄＴ＋、ＣＤ４＋、ＣＤ８＋）$", re.I).sub(u"リンパ節生検＝Ｔ−ＬＢＬ", text)
        text = re.compile(u"^Ｍ蛋白血症（ＩｇＧλ）／陽性$", re.I).sub(u"Ｍ蛋白血症（ＩｇＧλ）／陽性", text)
        text = re.compile(u"^免疫染色＝ＣＸＣＬ１３（±）、ＰＤ−１（＋）$", re.I).sub(u"免疫染色＝ＣＸＣＬ１３、ＰＤ−１", text)
        text = re.compile(u"^免疫染色＝ＣＤ３、ＣＤ８、ＥＢＥＲ（ＩＳＨ）、ＴＩＡ−１、Ｇｒａｎｚｙｍｅ＿Ｂ、Ｐｅｒｆｏｒｉｎ、ＴＣＲγδ／陽性$", re.I).sub(u"免疫染色＝ＣＤ３、ＣＤ８、ＥＢＥＲ（ＩＳＨ）、ＴＩＡ−１、Ｇｒａｎｚｙｍｅ＿Ｂ、Ｐｅｒｆｏｒｉｎ、ＴＣＲγδ／陽性", text)
        text = re.compile(u"^腹部ＣＴ検査（単純）＝低吸収域＊肝占拠性病変$", re.I).sub(u"腹部単純ＣＴ検査＝低吸収域＊肝占拠性病変", text)
        text = re.compile(u"^膵外腫瘍性＊低血糖症（ＮＩＣＴＨ）$", re.I).sub(u"膵外腫瘍性＊低血糖症", text)
        text = re.compile(u"^原発性色素性結節状副腎皮質病変（ＰＰＮＡＤ）$", re.I).sub(u"原発性色素性結節状副腎皮質病変", text)
        text = re.compile(u"^２５−（ＯＨ）Ｄ／低値$", re.I).sub(u"２５−（ＯＨ）Ｄ／低値", text)
        text = re.compile(u"^１，２５−（ＯＨ）２Ｄ／低値$", re.I).sub(u"１，２５−（ＯＨ）２Ｄ／低値", text)
        text = re.compile(u"^骨髄＝ｔ（９；２２）$", re.I).sub(u"骨髄＝ｔ（９；２２）", text)
        text = re.compile(u"^染色体検査＝ｉｎｖ（１６）・関連遺伝子ＣＢＦＢ−ＭＹＨ１１$", re.I).sub(u"染色体検査＝ｉｎｖ・関連遺伝子ＣＢＦＢ−ＭＹＨ１１", text)
        text = re.compile(u"^ＨＥＶ抗体（ＩｇＭ／ＩｇＧ）／上昇$", re.I).sub(u"ＨＥＶ抗体／上昇", text)
        text = re.compile(u"^血液＝１．２５−（ＯＨ）２Ｄ３／低値$", re.I).sub(u"血液＝１．２５−２Ｄ３／低値", text)
        text = re.compile(u"^病理診断＝胆嚢癌（高分化型＊粘液癌）$", re.I).sub(u"病理診断＝胆嚢癌", text)
        text = re.compile(u"^遺伝子解析＝点変異／陽性＠ｈｅｐａｔｏｃｙｔｅ＿ｎｕｃｌｅａｒ＿ｆａｃｔｏｒ（ＨＮＦ）−１α$", re.I).sub(u"遺伝子解析＝点変異／陽性＠ｈｅｐａｔｏｃｙｔｅ＿ｎｕｃｌｅａｒ＿ｆａｃｔｏｒ−１α", text)
        text = re.compile(u"^肝生検＝〔慢性肝炎（中等度線維化／中等度壊死）〕・肉芽腫／陰性$", re.I).sub(u"肝生検＝〔慢性肝炎〕・肉芽腫／陰性", text)
        text = re.compile(u"^ＡＬＰ／高値（アイソザイム骨型優位）$", re.I).sub(u"ＡＬＰ／高値（アイソザイム骨型優位）", text)
        text = re.compile(u"^染色体検査＝ｔ（１１；１９）（ｑ２３；ｐ１３．１）／異常$", re.I).sub(u"染色体検査＝ｔ（１１；１９）（ｑ２３；ｐ１３．１）／異常", text)
        text = re.compile(u"^染色体分析＝ｉｎｖ（１６）・ＷＴ１・ＣＢＦβ−ＭＹＨ１１ｍＲＮＡ$", re.I).sub(u"染色体分析＝ｉｎｖ（１６）・ＷＴ１・ＣＢＦβ−ＭＹＨ１１ｍＲＮＡ", text)
        text = re.compile(u"^肝生検＝ＣＨ（Ｃ）Ａ１Ｆ２　$", re.I).sub(u"肝生検＝ＣＨＡ１Ｆ２　", text)
        text = re.compile(u"^１．２５−（ＯＨ）２ビタミンＤ／正常$", re.I).sub(u"１．２５−（ＯＨ）２ビタミンＤ／正常", text)
        text = re.compile(u"^血液＝１，２５−（ＯＨ）２ビタミンＤ／高値$", re.I).sub(u"血液＝１，２５−（ＯＨ）２ビタミンＤ／高値", text)
        text = re.compile(u"^頚部リンパ節生検＝悪性リンパ腫（末梢Ｔ細胞型）$", re.I).sub(u"頚部リンパ節生検＝悪性リンパ腫", text)
        text = re.compile(u"^ＷＢＣ＿１，０００（Ｓｅｇ１９％）〔好中球減少〕$", re.I).sub(u"ＷＢＣ＿１，０００〔好中球減少〕", text)
        text = re.compile(u"^Ｈ：グルカゴン−インスリン（Ｇ−Ｉ）療法／有効$", re.I).sub(u"Ｈ：グルカゴン−インスリン療法／有効", text)
        text = re.compile(u"^血液＝２５−（ＯＨ）２　Ｖ．Ｄ／低値$", re.I).sub(u"血液＝２５−（ＯＨ）２　Ｖ．Ｄ／低値", text)
        text = re.compile(u"^〔低酸素血症〕ＳｐＯ２８７％（１Ｌ／ｍｉｎＮＣ）$", re.I).sub(u"〔低酸素血症〕ＳｐＯ２８７％", text)
        text = re.compile(u"^１，２５−（ＯＨ）２Ｖｉｔ．Ｄ／高値$", re.I).sub(u"１，２５−（ＯＨ）２Ｖｉｔ．Ｄ／高値", text)
        text = re.compile(u"^Ｉｇ（Ｈ）ＪＨ再構成／陰性$", re.I).sub(u"Ｉｇ（Ｈ）ＪＨ再構成／陰性", text)
        text = re.compile(u"^Ｊａｎｕｓ＿Ｋｉｎａｓｅ＿２（ＪＡＫ２）Ｖ６１７Ｆ遺伝子変異$", re.I).sub(u"Ｊａｎｕｓ＿Ｋｉｎａｓｅ＿２（ＪＡＫ２）Ｖ６１７Ｆ遺伝子変異", text)
        text = re.compile(u"^末梢血ＦＩＰ１Ｌ１−ＰＤＧＦＲαキメラ遺伝子（ＲＴ−ＰＣＲ）／陽性$", re.I).sub(u"末梢血ＦＩＰ１Ｌ１−ＰＤＧＦＲαキメラ遺伝子／陽性", text)
        text = re.compile(u"^１，２５（ＯＨ）２ＶｉｔＤ／上昇$", re.I).sub(u"１，２５（ＯＨ）２ＶｉｔＤ／上昇", text)
        text = re.compile(u"^骨髄クロット標本＝ＣＤ１０（＋）、ＣＤ７９ａ（＋）、ＣＤ１３８（−）$", re.I).sub(u"骨髄クロット標本＝ＣＤ１０（＋）、ＣＤ７９ａ（＋）、ＣＤ１３８（−）", text)
        text = re.compile(u"^血液＝血漿レニン活性（ＰＲＡ）／低値$", re.I).sub(u"血液＝血漿レニン活性／低値", text)
        text = re.compile(u"^血球貪食症候群（ＨＰＳ）$", re.I).sub(u"血球貪食症候群", text)
        text = re.compile(u"^染色体検査＝４６，ＸＹ・＋１，ｄｅｒ（１；７）（ｑ１０；ｐ１０）$", re.I).sub(u"染色体検査＝４６，ＸＹ・＋１，ｄｅｒ（１；７）（ｑ１０；ｐ１０）", text)
        text = re.compile(u"^骨髄検体＝染色体検査　ｄｅｌ（１３）$", re.I).sub(u"骨髄検体＝染色体検査　ｄｅｌ（１３）", text)
        text = re.compile(u"^ク−ムステスト（±）$", re.I).sub(u"ク−ムステスト（±）", text)
        text = re.compile(u"^４６ＸＸ、ｔ（９；２２）（ｑ３４；ｑ１１．２）／陽性$", re.I).sub(u"４６ＸＸ、ｔ（９；２２）（ｑ３４；ｑ１１．２）／陽性", text)
        text = re.compile(u"^培養＝ＭＲＳＡ（ＴＳＳＴ−１産生株）＠左＊下腿$", re.I).sub(u"培養＝ＭＲＳＡ＠左＊下腿", text)
        text = re.compile(u"^病理＝ＧＥ＿Ｌｅｓｓ＿ｔｙｐｅ１＿８０×４５ｍｍ＿ｐＰＭ０＿ｐＤＭ０＿ｐＴ２（ｐＭＰ）＿ｔｕｂ１＿ＩＮＦａ＿ｉｎｔ＿ｌｙ１＿ｖ１ｐＮ０ｓｔａｇｅ１Ｂ$", re.I).sub(u"病理＝ＧＥ＿Ｌｅｓｓ＿ｔｙｐｅ１＿８０×４５ｍｍ＿ｐＰＭ０＿ｐＤＭ０＿ｐＴ２（ｐＭＰ）＿ｔｕｂ１＿ＩＮＦａ＿ｉｎｔ＿ｌｙ１＿ｖ１ｐＮ０ｓｔａｇｅ１Ｂ", text)
        text = re.compile(u"^ＰＴＨ・ＰＴＨｒＰ・１．２５（ＯＨ）２Ｖｉｔ．Ｄ・２５（ＯＨ）＿Ｖｉｔ．Ｄ・ＦＧＦ−２３／正常$", re.I).sub(u"ＰＴＨ・ＰＴＨｒＰ・１．２５（ＯＨ）２Ｖｉｔ．Ｄ・２５（ＯＨ）＿Ｖｉｔ．Ｄ・ＦＧＦ−２３／正常", text)
        text = re.compile(u"^頭部ＭＲＩ＝ｐｏｓｔｅｒｉｏｒ＿ｒｅｖｅｒｓｉｂｌｅ＿ｅｎｃｅｐｈａｌｏｐａｔｈｙｓｙｎｄｒｏｍｅ（ＰＲＥＳ）$", re.I).sub(u"頭部ＭＲＩ＝ｐｏｓｔｅｒｉｏｒ＿ｒｅｖｅｒｓｉｂｌｅ＿ｅｎｃｅｐｈａｌｏｐａｔｈｙｓｙｎｄｒｏｍｅ", text)
        text = re.compile(u"^骨髄検査＝急性骨髄性白血病（Ｍ０）$", re.I).sub(u"骨髄検査＝急性骨髄性白血病（Ｍ０）", text)
        text = re.compile(u"^染色体検査＝ｔ（３；１４）／異常　$", re.I).sub(u"染色体検査＝ｔ（３；１４）／異常　", text)
        text = re.compile(u"^染色体検査＝（ｑ２７；ｑ３２）／異常$", re.I).sub(u"染色体検査＝（ｑ２７；ｑ３２）／異常", text)
        text = re.compile(u"^特発性器質化肺炎（ＣＯＰ）$", re.I).sub(u"特発性器質化肺炎", text)
        text = re.compile(u"^１，２５（ＯＨ）２ビタミンＤ／上昇$", re.I).sub(u"１，２５（ＯＨ）２ビタミンＤ／上昇", text)
        text = re.compile(u"^抗ＤＮＡ抗体（ＲＩＡ）／陽性$", re.I).sub(u"抗ＤＮＡ抗体／陽性", text)
        text = re.compile(u"^ＡＣＥ・１．２５（ＯＨ）２−ＶｉｔＤ／上昇$", re.I).sub(u"ＡＣＥ・１．２５（ＯＨ）２−ＶｉｔＤ／上昇", text)
        text = re.compile(u"^ＨｂＡ１ｃ（ＮＧＳＰ値）／高値$", re.I).sub(u"ＨｂＡ１ｃ／高値", text)
        text = re.compile(u"^表面抗原＝ＣＤ５（＋／−）・ＣＤ１０／陰性・ＣＤ１９／陽性・ＣＤ２０／陽性$", re.I).sub(u"表面抗原＝ＣＤ５（＋／−）・ＣＤ１０／陰性・ＣＤ１９／陽性・ＣＤ２０／陽性", text)
        text = re.compile(u"^Ａｌｂｒｉｇｈｔ遺伝性骨異栄養症（ＡＨＯ）$", re.I).sub(u"Ａｌｂｒｉｇｈｔ遺伝性骨異栄養症", text)
        text = re.compile(u"^デキサメタゾン抑制（１ｍｇ）＝コルチゾ−ル抑制／陰性$", re.I).sub(u"デキサメタゾン抑制＝コルチゾ−ル抑制／陰性", text)
        text = re.compile(u"^大量デキサメタゾン抑制（８ｍｇ）＝抑制／陰性$", re.I).sub(u"大量デキサメタゾン抑制＝抑制／陰性", text)
        text = re.compile(u"^グルタミン酸脱炭酸酵素（ＧＡＤ）抗体／陽性$", re.I).sub(u"グルタミン酸脱炭酸酵素抗体／陽性", text)
        text = re.compile(u"^腎病理＝ル−プス腎炎（ＩＳＮ／ＲＰＳ−ｃｌａｓｓ４）$", re.I).sub(u"腎病理＝ル−プス腎炎", text)
        text = re.compile(u"^頭部ＭＲＩ＝浸透圧性脱髄症候群（ＯＤＳ）／陰性$", re.I).sub(u"頭部ＭＲＩ＝浸透圧性脱髄症候群／陰性", text)
        text = re.compile(u"^高血糖高浸透圧症候群（ＨＨＳ）$", re.I).sub(u"高血糖高浸透圧症候群", text)
        text = re.compile(u"^骨髄穿刺＝びまん性大細胞型Ｂ細胞性リンパ腫（ＤＬＢＣＬ）$", re.I).sub(u"骨髄穿刺＝びまん性大細胞型Ｂ細胞性リンパ腫", text)
        text = re.compile(u"^１，２５（ＯＨ）２ＶｉｔＤ３／正常$", re.I).sub(u"１，２５（ＯＨ）２ＶｉｔＤ３／正常", text)
        text = re.compile(u"^甲状腺機能低下症（橋本病）／陽性$", re.I).sub(u"甲状腺機能低下症／陽性", text)
        text = re.compile(u"^サイトメガロウイルス（ＣＭＶ）染色／陽性$", re.I).sub(u"サイトメガロウイルス染色／陽性", text)
        text = re.compile(u"^ＦＧＦ（ｆｉｂｒｏｂｌａｓｔ＿ｇｒｏｗｔｈ＿ｆａｃｔｏｒ）−２３／上昇$", re.I).sub(u"ＦＧＦ−２３／上昇", text)
        text = re.compile(u"^ｈｕｍｏｒａｌ＿ｈｙｐｅｒｃａｌｃｅｍｉａ＿ｏｆ＿ｍａｌｉｇｎａｎｃｙ（ＨＨＭ）$", re.I).sub(u"ｈｕｍｏｒａｌ＿ｈｙｐｅｒｃａｌｃｅｍｉａ＿ｏｆ＿ｍａｌｉｇｎａｎｃｙ", text)
        text = re.compile(u"^〔遺伝子〕＝ｍｔＤＮＡ３２４３（Ａ→Ｇ）変異$", re.I).sub(u"〔遺伝子〕＝ｍｔＤＮＡ３２４３（Ａ→Ｇ）変異", text)
        text = re.compile(u"^染色体検査＝４６ＸＸ＿ｉｓｈ＿ｄｅｒ（Ｘ）＿ｔ（Ｘ；Ｙ）$", re.I).sub(u"染色体検査＝４６ＸＸ＿ｉｓｈ＿ｄｅｒ（Ｘ）＿ｔ（Ｘ；Ｙ）", text)
        text = re.compile(u"^Ｈ：ダクラタスビル（ＤＣＶ）／アスナプレビル（ＡＳＶ）併用療法／有効$", re.I).sub(u"Ｈ：ダクラタスビル／アスナプレビル併用療法／有効", text)
        text = re.compile(u"^Ｈ：筋萎縮性側索硬化症（ＡＬＳ）$", re.I).sub(u"Ｈ：筋萎縮性側索硬化症", text)
        text = re.compile(u"^２５（ＯＨ）Ｄ／低下$", re.I).sub(u"２５（ＯＨ）Ｄ／低下", text)
        text = re.compile(u"^腹水細胞診・フロ−サイトメトリ−＝異型形質細胞の増加（ｃｌａｓｓＶ）$", re.I).sub(u"腹水細胞診・フロ−サイトメトリ−＝異型形質細胞の増加（ｃｌａｓｓＶ）", text)
        text = re.compile(u"^１，２５−（ＯＨ）２ビタミンＤ活性／正常$", re.I).sub(u"１，２５−（ＯＨ）２ビタミンＤ活性／正常", text)
        text = re.compile(u"^２８か月後ｂｒｅａｋｔｈｒｏｕｇｈｈｅｐａｔｉｔｉｓ（ＢＴＨ）出現$", re.I).sub(u"２８か月後ｂｒｅａｋｔｈｒｏｕｇｈｈｅｐａｔｉｔｉｓ出現", text)
        text = re.compile(u"^Ｈ：強力ネオミノファ−ゲンＣ（ＳＮＭＣ）$", re.I).sub(u"Ｈ：強力ネオミノファ−ゲンＣ", text)
        text = re.compile(u"^３年後ＨＢｅ抗原ｓｅｒｏｃｏｎｖｅｒｓｉｏｎ（ＳＣ）$", re.I).sub(u"３年後ＨＢｅ抗原ｓｅｒｏｃｏｎｖｅｒｓｉｏｎ", text)
        text = re.compile(u"^２４か月後ｂｒｅａｋｔｈｒｏｕｇｈｈｅｐａｔｉｔｉｓ（ＢＴＨ）出現$", re.I).sub(u"２４か月後ｂｒｅａｋｔｈｒｏｕｇｈｈｅｐａｔｉｔｉｓ出現", text)
        text = re.compile(u"^１５か月後ｂｒｅａｋｔｈｒｏｕｇｈｈｅｐａｔｉｔｉｓ（ＢＴＨ）出現$", re.I).sub(u"１５か月後ｂｒｅａｋｔｈｒｏｕｇｈｈｅｐａｔｉｔｉｓ出現", text)
        text = re.compile(u"^Ｈ：アデフォビルピボキシル（ヘプセラ）$", re.I).sub(u"Ｈ：アデフォビルピボキシル", text)
        text = re.compile(u"^２年後ｓｅｒｏｃｏｎｖｅｒｓｉｏｎ（ＳＣ）$", re.I).sub(u"２年後ｓｅｒｏｃｏｎｖｅｒｓｉｏｎ", text)
        text = re.compile(u"^ＴＣＲγ遺伝子再構成（ＰＣＲ法）／陽性$", re.I).sub(u"ＴＣＲγ遺伝子再構成／陽性", text)
        text = re.compile(u"^ＩｇＨ遺伝子再構成（ＰＣＲ法）／陰性$", re.I).sub(u"ＩｇＨ遺伝子再構成／陰性", text)
        text = re.compile(u"^赤血球表面抗原解析＝ＣＤ５５（−）ＣＤ５９（−）／陽性$", re.I).sub(u"赤血球表面抗原解析＝ＣＤ５５（−）ＣＤ５９（−）／陽性", text)
        text = re.compile(u"^切除病理標本＝新犬山分類でＣＨ（Ａ３／Ｆ２）　$", re.I).sub(u"切除病理標本＝新犬山分類でＣＨ　", text)
        text = re.compile(u"^ＡＳＶＳ（選択的動脈内カルシウム注入）＝インスリノ−マ＠膵体部$", re.I).sub(u"ＡＳＶＳ＝インスリノ−マ＠膵体部", text)
        text = re.compile(u"^Ｈ：白球血除去（ＧＣＡＰ）／無効$", re.I).sub(u"Ｈ：白球血除去／無効", text)
        text = re.compile(u"^Ｈ：経皮的胆汁ドレナ−ジ術（ＰＴＣＤ）　$", re.I).sub(u"Ｈ：経皮的胆汁ドレナ−ジ術　", text)
        text = re.compile(u"^Ｈ：血漿交換（ＰＥ）／無効$", re.I).sub(u"Ｈ：血漿交換／無効", text)
        text = re.compile(u"^Ｈ：持続的血液濾過透析（ＣＨＤＦ）／無効$", re.I).sub(u"Ｈ：持続的血液濾過透析／無効", text)
        text = re.compile(u"^筋原性酵素（ＣＫ、ミオグロビン）／正常$", re.I).sub(u"筋原性酵素／正常", text)
        text = re.compile(u"^悪性症候群（ＭＬＳ）$", re.I).sub(u"悪性症候群", text)
        text = re.compile(u"^免疫電気泳動＝Ｍ蛋白（ＩｇＡ＿λｔｙｐｅ）／陽性$", re.I).sub(u"免疫電気泳動＝Ｍ蛋白（ＩｇＡ＿λｔｙｐｅ）／陽性", text)
        text = re.compile(u"^４６，ＸＹ，ｔ（９；２２）$", re.I).sub(u"４６，ＸＹ，ｔ（９；２２）", text)
        text = re.compile(u"^骨髄検査＝染色体検査４６ＸＸ，ｔ（９；１１）（ｐ２２；ｑ２３）・ＭＬＬ／ＡＦ９遺伝子$", re.I).sub(u"骨髄検査＝染色体検査４６ＸＸ，ｔ（９；１１）（ｐ２２；ｑ２３）・ＭＬＬ／ＡＦ９遺伝子", text)
        text = re.compile(u"^染色体検査＝ｔ（９；２２）転座・ｔ（１；３）（ｐ３６；ｐ２１）転座$", re.I).sub(u"染色体検査＝ｔ（９；２２）転座・ｔ（１；３）（ｐ３６；ｐ２１）転座", text)
        text = re.compile(u"^末梢血中リンパ球＝ｌａｒｇｅ＿ｇｒａｎｕｌａｒｌｙｍｐｈｏｃｙｔｅ（ＬＧＬ）$", re.I).sub(u"末梢血中リンパ球＝ｌａｒｇｅ＿ｇｒａｎｕｌａｒｌｙｍｐｈｏｃｙｔｅ", text)
        text = re.compile(u"^１，２５（ＯＨ）２Ｄ３活性化障害$", re.I).sub(u"１，２５（ＯＨ）２Ｄ３活性化障害", text)
        text = re.compile(u"^染色体Ｇ−ｂａｎｄｉｎｇ＝　４６，ＸＸ，ｉｎｖ（９）$", re.I).sub(u"染色体Ｇ−ｂａｎｄｉｎｇ＝　４６，ＸＸ，ｉｎｖ（９）", text)
        text = re.compile(u"^サイトメガロウイルス（ＣＭＶ）腸炎$", re.I).sub(u"サイトメガロウイルス腸炎", text)
        text = re.compile(u"^ｄｅｒ（１；７）（ｑ１０；ｐ１０）$", re.I).sub(u"ｄｅｒ（１；７）（ｑ１０；ｐ１０）", text)
        text = re.compile(u"^リンパ節生検＝ｄｉｆｆｕｓｅ　ｌａｒｇｅ　Ｂ　ｃｅｌｌ　ｌｙｍｐｈｏｍａ（ＤＬＢＣＬ）$", re.I).sub(u"リンパ節生検＝ｄｉｆｆｕｓｅ　ｌａｒｇｅ　Ｂ　ｃｅｌｌ　ｌｙｍｐｈｏｍａ", text)
        text = re.compile(u"^リンパ節生検＝ＴＣＲ＿Ｃβ１遺伝子再構成（サザン）／陰性$", re.I).sub(u"リンパ節生検＝ＴＣＲ＿Ｃβ１遺伝子再構成／陰性", text)
        text = re.compile(u"^リンパ節生検＝ＨＴＬＶ−１プロウイルスＤＮＡクロナリティ（サザン）／陰性$", re.I).sub(u"リンパ節生検＝ＨＴＬＶ−１プロウイルスＤＮＡクロナリティ／陰性", text)
        text = re.compile(u"^染色体分析＝４６・ＸＹ・ｔ（９；２２）（ｑ３４；ｑ１１．２）／陽性$", re.I).sub(u"染色体分析＝４６・ＸＹ・ｔ（９；２２）（ｑ３４；ｑ１１．２）／陽性", text)
        text = re.compile(u"^〔低酸素血症〕ＳｐＯ２９０％（酸素１０Ｌ／ｍｉｎリザ−バ−マスク）$", re.I).sub(u"〔低酸素血症〕ＳｐＯ２９０％", text)
        text = re.compile(u"^遺伝子検査＝新規＊ミスセンス変異＊（ヘテロ接合体）／陽性$", re.I).sub(u"遺伝子検査＝新規＊ミスセンス変異＊／陽性", text)
        text = re.compile(u"^フロ−サイトメトリ−＝ＣＤ２（＋）・ＣＤ３（＋）・ＣＤ５（＋）・ＣＤ７（＋）・ＣＤ８（＋）・ＣＤ２０（−）$", re.I).sub(u"フロ−サイトメトリ−＝ＣＤ２（＋）・ＣＤ３（＋）・ＣＤ５（＋）・ＣＤ７（＋）・ＣＤ８（＋）・ＣＤ２０（−）", text)
        text = re.compile(u"^慢性炎症性脱髄性多発神経炎（ＣＩＤＰ）$", re.I).sub(u"慢性炎症性脱髄性多発神経炎", text)
        text = re.compile(u"^ｇｅｒｍｉｎａｌｃｅｎｔｅｒＢ　ｃｅｌｌ（ＧＣＢ）型$", re.I).sub(u"ｇｅｒｍｉｎａｌｃｅｎｔｅｒＢ　ｃｅｌｌ型", text)
        text = re.compile(u"^ｔ（１４；１８）転座$", re.I).sub(u"ｔ（１４；１８）転座", text)
        text = re.compile(u"^脳生検＝ＣＤ４（＋）単核球主体の炎症細胞浸潤$", re.I).sub(u"脳生検＝ＣＤ４（＋）単核球主体の炎症細胞浸潤", text)
        text = re.compile(u"^腎生検＝ル−プス腎炎Ｖ＋ＩＶ型Ｇ（Ａ）／陽性$", re.I).sub(u"腎生検＝ル−プス腎炎Ｖ＋ＩＶ型Ｇ（Ａ）／陽性", text)
        text = re.compile(u"^血液ＰＣＲ検査＝Ｏｒｉｅｎｔｉａｔｓｕｔｓｕｇａｍｕｓｈｉ（Ｋａｗａｓａｋｉ型）／陽性$", re.I).sub(u"血液ＰＣＲ検査＝Ｏｒｉｅｎｔｉａｔｓｕｔｓｕｇａｍｕｓｈｉ／陽性", text)
        text = re.compile(u"^痂疲ＰＣＲ検査＝Ｏｒｉｅｎｔｉａｔｓｕｔｓｕｇａｍｕｓｈｉ（Ｋａｗａｓａｋｉ型）／陽性$", re.I).sub(u"痂疲ＰＣＲ検査＝Ｏｒｉｅｎｔｉａｔｓｕｔｓｕｇａｍｕｓｈｉ／陽性", text)
        text = re.compile(u"^炎症性サイトカイン（ＩＬ−１・ＩＬ−６・ＩＬ−８・ＩＬ−１２・ＴＮＦ−α・ＩＦＮ−γ）／高値$", re.I).sub(u"ＩＬ−１・ＩＬ−６・ＩＬ−８・ＩＬ−１２・ＴＮＦ−α・ＩＦＮ−γ／高値", text)
        text = re.compile(u"^ケモカイン（ＩＰ−１０・ＭＣＰ−１・ＭＩＰ−１α・ＭＩＰ−１β）／高値$", re.I).sub(u"ＩＰ−１０・ＭＣＰ−１・ＭＩＰ−１α・ＭＩＰ−１β／高値", text)
        text = re.compile(u"^免疫染色＝ＣＤ２０（＋）・ＣＤ３（−）・ＣＤ５（＋）・ＣＤ１０（−）・ｃｙｃｌｉｎＤ１（ｐ＋）・ＭＩＢ−１：ｈｉｇｈ・ｔ（１１；１４）（ｑ１３；ｑ３２）$", re.I).sub(u"免疫染色＝ＣＤ２０（＋）・ＣＤ３（−）・ＣＤ５（＋）・ＣＤ１０（−）・ｃｙｃｌｉｎＤ１（ｐ＋）・ＭＩＢ−１：ｈｉｇｈ・ｔ（１１；１４）（ｑ１３；ｑ３２）", text)
        text = re.compile(u"^リンパ球幼若化試験（ＤＬＳＴ）／陽性$", re.I).sub(u"リンパ球幼若化試験／陽性", text)
        text = re.compile(u"^ＨＴＬＶ−１プロウイルスＤＮＡ（サザンブロット法）＝急性型ＡＴＬＬ$", re.I).sub(u"ＨＴＬＶ−１プロウイルスＤＮＡ＝急性型ＡＴＬＬ", text)
        text = re.compile(u"^血液ＰＣＲ検査＝　Ｏｒｉｅｎｔｉａ　ｔｓｕｔｓｕｇａｍｕｓｈｉ（Ｋａｒｐ型）／陽性$", re.I).sub(u"血液ＰＣＲ検査＝　Ｏｒｉｅｎｔｉａ　ｔｓｕｔｓｕｇａｍｕｓｈｉ（Ｋａｒｐ型）／陽性", text)
        text = re.compile(u"^腎生検＝ル−プス腎炎ＩＶ−Ｇ（Ａ）$", re.I).sub(u"腎生検＝ル−プス腎炎ＩＶ−Ｇ", text)
        text = re.compile(u"^放射性ヨ−ド（ＲＩ）全身サ−ベイ＝異常集積＠頸部$", re.I).sub(u"放射性ヨ−ド全身サ−ベイ＝異常集積＠頸部", text)
        text = re.compile(u"^骨髄穿刺・骨髄生検＝免疫染色　ＰＡＸ５・ＣＤ３０・Ｂｏｂ．１・ＣＤ１５・ＥＢＥＲ（ＩＳＨ）$", re.I).sub(u"骨髄穿刺・骨髄生検＝免疫染色　ＰＡＸ５・ＣＤ３０・Ｂｏｂ．１・ＣＤ１５・ＥＢＥＲ", text)
        text = re.compile(u"^ＦＩＳＨ＝　ｄｅｌ（１７ｐ）$", re.I).sub(u"ＦＩＳＨ＝　ｄｅｌ（１７ｐ）", text)
        text = re.compile(u"^腹水細胞＝Ｉｇ（Ｇ）ＪＨ（サザン）遺伝子再構成$", re.I).sub(u"腹水細胞＝ＩｇＪＨ遺伝子再構成", text)
        text = re.compile(u"^染色体＝４５、Ｘ、−Ｙ（７／２０）$", re.I).sub(u"染色体＝４５、Ｘ、−Ｙ（７／２０）", text)
        text = re.compile(u"^骨髄異形成症候群（ＲＡ）$", re.I).sub(u"骨髄異形成症候群", text)
        text = re.compile(u"^病理組織検査＝ｄｉｆｆｕｓｅ＿ｌａｒｇｅ＿ｃｅｌｌ＿ｌｙｍｐｈｏｍａ（Ｐｌａｓｍａｂｌａｓｔｉｃｔｙｐｅ）$", re.I).sub(u"病理組織検査＝ｄｉｆｆｕｓｅ＿ｌａｒｇｅ＿ｃｅｌｌ＿ｌｙｍｐｈｏｍａ", text)
        text = re.compile(u"^ＥＢＶ（ＶＣＡ）−ＩｇＧ／上昇$", re.I).sub(u"ＥＢＶ−ＩｇＧ／上昇", text)
        text = re.compile(u"^骨髄＝ａｄｄ（１４）・ｄｅｒ（１４）ｔ（８；１４）（ｑ２４；ｑ３２）　／陽性$", re.I).sub(u"骨髄＝ａｄｄ（１４）・ｄｅｒ（１４）ｔ（８；１４）（ｑ２４；ｑ３２）　／陽性", text)
        text = re.compile(u"^１、２５（ＯＨ）Ｄ／低下$", re.I).sub(u"１、２５（ＯＨ）Ｄ／低下", text)
        text = re.compile(u"^ＦＩＳＨ＝ｔ（１４；１８）／陰性$", re.I).sub(u"ＦＩＳＨ＝ｔ（１４；１８）／陰性", text)
        text = re.compile(u"^ＦＩＳＨ法＝ｔ（８；１４）（ｑ２４；ｑ３２）／陰性$", re.I).sub(u"ＦＩＳＨ法＝ｔ（８；１４）（ｑ２４；ｑ３２）／陰性", text)
        text = re.compile(u"^染色体検査＝ｔ（１５；１７）（ｑ２２：ｑ２１）$", re.I).sub(u"染色体検査＝ｔ（１５；１７）（ｑ２２：ｑ２１）", text)
        text = re.compile(u"^骨髄＝ｔ（１５；１７）・ＰＭＬ／ＲＡＲＡ融合／陽性$", re.I).sub(u"骨髄＝ｔ（１５；１７）・ＰＭＬ／ＲＡＲＡ融合／陽性", text)
        text = re.compile(u"^遺伝子検査＝ｔ（１４；１８）（ｑ３２；ｑ２１）・複雑染色体異常$", re.I).sub(u"遺伝子検査＝ｔ（１４；１８）（ｑ３２；ｑ２１）・複雑染色体異常", text)
        text = re.compile(u"^遺伝子検査＝ｔ（１４；１８）$", re.I).sub(u"遺伝子検査＝ｔ（１４；１８）", text)
        text = re.compile(u"^染色体＝ｔ（３；１４）（ｑ２７；ｑ３２）$", re.I).sub(u"染色体＝ｔ（３；１４）（ｑ２７；ｑ３２）", text)
        text = re.compile(u"^ｔ（１４；１８）（１４ｑ３２，１８ｑ２１）／陽性$", re.I).sub(u"ｔ（１４；１８）（１４ｑ３２，１８ｑ２１）／陽性", text)
        text = re.compile(u"^重症筋無力症（全身型）　$", re.I).sub(u"重症筋無力症　", text)
        text = re.compile(u"^腰椎穿刺＝細胞数（単核球優位）・蛋白数増加$", re.I).sub(u"腰椎穿刺＝細胞数・蛋白数増加", text)
        text = re.compile(u"^慢性腎不全（透析中）$", re.I).sub(u"慢性腎不全", text)
        text = re.compile(u"^染色体検査＝４６ＸＹ・ｔ（１５；１７）（ｑ２２；ｑ１２）$", re.I).sub(u"染色体検査＝４６ＸＹ・ｔ（１５；１７）（ｑ２２；ｑ１２）", text)
        text = re.compile(u"^ＳＫＹＦＩＳＨ＝　ｔ（５；１７；１５；２０）（ｑ３３；ｑ１２；ｑ２２；ｑ１１．２）／陽性$", re.I).sub(u"ＳＫＹＦＩＳＨ＝　ｔ（５；１７；１５；２０）（ｑ３３；ｑ１２；ｑ２２；ｑ１１．２）／陽性", text)
        text = re.compile(u"^蛍光抗体法（腎生検）＝ＩｇＭ、Ｃ３のメサンギウムへの沈着$", re.I).sub(u"腎生検　蛍光抗体法＝ＩｇＭ、Ｃ３のメサンギウムへの沈着", text)
        text = re.compile(u"^２５（ＯＨ）ＶｉｔＤ３／低値$", re.I).sub(u"２５（ＯＨ）ＶｉｔＤ３／低値", text)
        text = re.compile(u"^染色体＝ｔ（６；８）＠胸水$", re.I).sub(u"染色体＝ｔ（６；８）＠胸水", text)
        text = re.compile(u"^遺伝子検査＝ｔ（８；１４）$", re.I).sub(u"遺伝子検査＝ｔ（８；１４）", text)
        text = re.compile(u"^骨髄穿刺＝染色体検査　ｔ（２；１３）$", re.I).sub(u"骨髄穿刺＝染色体検査　ｔ（２；１３）", text)
        text = re.compile(u"^ＭＤＳ（ＲＣＭＤ）$", re.I).sub(u"ＭＤＳ（ＲＣＭＤ）", text)
        text = re.compile(u"^骨髄検査＝ｔ（１５；１７）（ｑ２２；ｑ２１）$", re.I).sub(u"骨髄検査＝ｔ（１５；１７）（ｑ２２；ｑ２１）", text)
        text = re.compile(u"^父親（結核で死亡）$", re.I).sub(u"父親", text)
        text = re.compile(u"^リンパ節標本＝ｔ（１０；１４）（ｑ１１；ｑ３２）染色体異常・ＩｇＨ鎖遺伝子再構成$", re.I).sub(u"リンパ節標本＝ｔ（１０；１４）（ｑ１１；ｑ３２）染色体異常・ＩｇＨ鎖遺伝子再構成", text)
        text = re.compile(u"^Ｒｉｃｋｅｔｔｓｉａ＿ｊａｐｏｎｉｃａ（ＹＨ株）ＩｇＭ／上昇$", re.I).sub(u"Ｒｉｃｋｅｔｔｓｉａ＿ｊａｐｏｎｉｃａＩｇＭ／上昇", text)
        text = re.compile(u"^Ｒｉｃｋｅｔｔｓｉａ＿ｊａｐｏｎｉｃａ（ＹＨ株）ＩｇＧ／上昇$", re.I).sub(u"Ｒｉｃｋｅｔｔｓｉａ＿ｊａｐｏｎｉｃａＩｇＧ／上昇", text)
        text = re.compile(u"^骨髄穿刺＝染色体分析　ｔ（６；９）$", re.I).sub(u"骨髄穿刺＝染色体分析　ｔ（６；９）", text)
        text = re.compile(u"^気管支肺胞洗浄液（ＢＡＬＦ）＝リンパ球優位$", re.I).sub(u"気管支肺胞洗浄液＝リンパ球優位", text)
        text = re.compile(u"^頚動脈エコ−＝頚動脈スコア（ＣＡＳ）／高値$", re.I).sub(u"頚動脈エコ−＝頚動脈スコア／高値", text)
        text = re.compile(u"^〔冠動脈検査〕＝冠動脈予備能（ＣＦＲ）＠前下行枝／低下$", re.I).sub(u"〔冠動脈検査〕＝冠動脈予備能＠前下行枝／低下", text)
        text = re.compile(u"^染色体分析＝４６，＿ＸＸ，＿ｔ（９；２２；１６）（ｑ３４；ｑ１１；ｑ２４）$", re.I).sub(u"染色体分析＝４６，＿ＸＸ，＿ｔ（９；２２；１６）（ｑ３４；ｑ１１；ｑ２４）", text)
        text = re.compile(u"^染色体検査＝ｔ（１５；１７）$", re.I).sub(u"染色体検査＝ｔ（１５；１７）", text)
        text = re.compile(u"^右心カテ＝肺動脈圧９３／１５（４５）ｍｍＨｇ〔肺高血圧$", re.I).sub(u"右心カテ＝肺動脈圧９３／１５ｍｍＨｇ〔肺高血圧", text)
        text = re.compile(u"^Ｈ：上室性期外収縮（ＰＡＣ）$", re.I).sub(u"Ｈ：上室性期外収縮", text)
        text = re.compile(u"^１，２５（ＯＨ）２Ｄ／低下$", re.I).sub(u"１，２５（ＯＨ）２Ｄ／低下", text)
        text = re.compile(u"^Ｃ−ＡＮＣＡ（／陽性$", re.I).sub(u"Ｃ−ＡＮＣＡ／陽性", text)
        text = re.compile(u"^免疫染色＝ＣＤ６８（／陽性$", re.I).sub(u"免疫染色＝ＣＤ６８／陽性", text)
        text = re.compile(u"^染色体＝４６、ＸＹ，ｔ（３；１２）（ｑ２１；ｑ２２）$", re.I).sub(u"染色体＝４６、ＸＹ，ｔ（３；１２）（ｑ２１；ｑ２２）", text)
        text = re.compile(u"^胸水＝染色体検査　ｔ（１１；１８）（ｑ２１；２１）$", re.I).sub(u"胸水＝染色体検査　ｔ（１１；１８）（ｑ２１；２１）", text)
        text = re.compile(u"^〔γ３−ＭＳＨ＿ＡＣＴＨ（１−３９）濃度比上昇〕$", re.I).sub(u"〔γ３−ＭＳＨ＿ＡＣＴＨ（１−３９）濃度比上昇〕", text)
        text = re.compile(u"^遺伝子検査＝ＨＬＡ−ＤＲ４・ＨＬＡ−ＤＱＢ１（０４０１）／陽性$", re.I).sub(u"遺伝子検査＝ＨＬＡ−ＤＲ４・ＨＬＡ−ＤＱＢ１（０４０１）／陽性", text)
        text = re.compile(u"^Ｉｎｔａｃｔ−ＰＴＨ・１，２５−（ＯＨ）２Ｄ／低下$", re.I).sub(u"Ｉｎｔａｃｔ−ＰＴＨ・１，２５−（ＯＨ）２Ｄ／低下", text)
        text = re.compile(u"^脾臓染色体＝４４，Ｘ・−Ｘ・−１，ａｄｄ（４）（ｐ１６）・ａｄｄ（３）（ｐ１１）・ｄｅｌ（１１）（ｑ７）・−２２・＋ｍａｒｌ$", re.I).sub(u"脾臓染色体＝４４，Ｘ・−Ｘ・−１，ａｄｄ（４）（ｐ１６）・ａｄｄ（３）（ｐ１１）・ｄｅｌ（１１）（ｑ７）・−２２・＋ｍａｒｌ", text)
        text = re.compile(u"^ＦＩＳＨ法＝　ｔ（１１；１４）転座／陰性$", re.I).sub(u"ＦＩＳＨ法＝　ｔ（１１；１４）転座／陰性", text)
        text = re.compile(u"^生検（免疫染色）＝ＩｇＧ４陽性形質細胞の浸潤＠胃壁・眼窩$", re.I).sub(u"生検＝ＩｇＧ４陽性形質細胞の浸潤＠胃壁・眼窩", text)
        text = re.compile(u"^ＰＥＴ（ＦＤＧ）＝集積／陽性＠大動脈・頸動脈$", re.I).sub(u"ＦＤＧ−ＰＥＴ＝集積／陽性＠大動脈・頸動脈", text)
        text = re.compile(u"^ＰＥＴ（ＦＤＧ）＝異常集積＠大動脈・頸動脈$", re.I).sub(u"ＦＤＧ−ＰＥＴ＝異常集積＠大動脈・頸動脈", text)
        text = re.compile(u"^染色体分析＝４６，＿ＸＸ，＿ｔ（１；３）（ｐ３６．３；ｑ２１）$", re.I).sub(u"染色体分析＝４６，＿ＸＸ，＿ｔ（１；３）（ｐ３６．３；ｑ２１）", text)
        text = re.compile(u"^下垂体前葉負荷（ＣＲＨ，ＧＲＨ，ＴＲＨ，＿ＬＨ−ＲＨ）＝ＡＣＴＨピ−ク値反応／異常$", re.I).sub(u"下垂体前葉負荷（ＣＲＨ，ＧＲＨ，ＴＲＨ，＿ＬＨ−ＲＨ）＝ＡＣＴＨピ−ク値反応／異常", text)
        text = re.compile(u"^下垂体前葉負荷（ＣＲＨ，ＧＲＨ，ＴＲＨ，＿ＬＨ−ＲＨ）＝下垂体前葉ホルモン反応性分泌／正常$", re.I).sub(u"下垂体前葉負荷（ＣＲＨ，ＧＲＨ，ＴＲＨ，＿ＬＨ−ＲＨ）＝下垂体前葉ホルモン反応性分泌／正常", text)
        text = re.compile(u"^Ｈ：渡航歴（ウガンダ）$", re.I).sub(u"Ｈ：渡航歴（ウガンダ）", text)
        text = re.compile(u"^４者負荷試験（ＴＲＨ、ＣＲＨ、ＬＨ−ＲＨ、ＧＲＨ）＝ＡＣＴＨ／異常$", re.I).sub(u"４者負荷試験（ＴＲＨ、ＣＲＨ、ＬＨ−ＲＨ、ＧＲＨ）＝ＡＣＴＨ／異常", text)
        text = re.compile(u"^気管支肺胞洗浄液（ＢＡＬＦ）＝リンパ球比／上昇$", re.I).sub(u"気管支肺胞洗浄液＝リンパ球比／上昇", text)
        text = re.compile(u"^体重（ＤＷ）／低下$", re.I).sub(u"体重／低下", text)
        text = re.compile(u"^体重（ＤＷ）減少$", re.I).sub(u"体重減少", text)
        text = re.compile(u"^発疹（多形紅斑）＠上腕部・体幹部$", re.I).sub(u"発疹＠上腕部・体幹部", text)
        text = re.compile(u"^コルチゾ−ル（Ｆ）日内変動消失$", re.I).sub(u"コルチゾ−ル日内変動消失", text)
        text = re.compile(u"^ＨｂＡ１ｃ（ＪＤＳ値）／高値$", re.I).sub(u"ＨｂＡ１ｃ／高値", text)
        text = re.compile(u"^ＧＡＤＡｂ（−）、ＩＡ２Ａｂ（＋）、ＩＣＡＩｇＧ（＋）$", re.I).sub(u"ＧＡＤＡｂ（−）、ＩＡ２Ａｂ（＋）、ＩＣＡＩｇＧ（＋）", text)
        text = re.compile(u"^骨髄検査＝染色体分析　ｔ（８；２１）転座$", re.I).sub(u"骨髄検査＝染色体分析　ｔ（８；２１）転座", text)
        text = re.compile(u"^染色体＝４６，＿ＸＹ，＿ｄｅｌ（１３）（ｑ１２ｑ２２）$", re.I).sub(u"染色体＝４６，＿ＸＹ，＿ｄｅｌ（１３）（ｑ１２ｑ２２）", text)
        text = re.compile(u"^ＨｂＡ１ｃ（ＪＤＳ）／高値$", re.I).sub(u"ＨｂＡ１ｃ／高値", text)
        text = re.compile(u"^気管支肺胞洗浄（ＢＡＬ）液＝リンパ球／上昇$", re.I).sub(u"気管支肺胞洗浄液＝リンパ球／上昇", text)
        text = re.compile(u"^気管支肺胞洗浄（ＢＡＬ）＝好酸球／上昇$", re.I).sub(u"気管支肺胞洗浄＝好酸球／上昇", text)
        text = re.compile(u"^便培養＝病原性大腸菌（Ｏ−４４）$", re.I).sub(u"便培養＝病原性大腸菌（Ｏ−４４）", text)
        text = re.compile(u"^Ｃｈｌａｍｙｄｏｐｈｉｌａ＿ＩｇＧ（−）・Ｃｈｌａｍｙｄｏｐｈｉｌａ＿ＩｇＭ／陰性$", re.I).sub(u"Ｃｈｌａｍｙｄｏｐｈｉｌａ＿ＩｇＧ（−）・Ｃｈｌａｍｙｄｏｐｈｉｌａ＿ＩｇＭ／陰性", text)
        text = re.compile(u"^１α２５（ＯＨ）２Ｄ３／上昇$", re.I).sub(u"１α２５（ＯＨ）２Ｄ３／上昇", text)
        text = re.compile(u"^尿中Ｂｅｎｃｅ−Ｊｏｎｅｓ蛋白（κ型）／陽性$", re.I).sub(u"尿中Ｂｅｎｃｅ−Ｊｏｎｅｓ蛋白（κ型）／陽性", text)
        text = re.compile(u"^〔アシデミア〕ｐＨ：７．３５（Ｖ−ｇａｓ）$", re.I).sub(u"〔アシデミア〕ｐＨ：７．３５", text)
        text = re.compile(u"^血液＝ＣＰＲ（空腹時）／低下$", re.I).sub(u"血液＝ＣＰＲ／低下", text)
        text = re.compile(u"^病理検査＝ＣＤ４５（ＬＣＡ）、ＣＤ２０、ＣＤ７９ａ、ｂｃｌ−２／陽性$", re.I).sub(u"病理検査＝ＣＤ４５、ＣＤ２０、ＣＤ７９ａ、ｂｃｌ−２／陽性", text)
        text = re.compile(u"^抗Ｅ抗体、抗ｃ抗体、抗Ｄｉ（ｂ）抗体／陽性$", re.I).sub(u"抗Ｅ抗体、抗ｃ抗体、抗Ｄｉ抗体／陽性", text)
        text = re.compile(u"^バレニクリン酒石酸塩（チャンピックス＿）$", re.I).sub(u"バレニクリン酒石酸塩", text)
        text = re.compile(u"^骨髄検査＝花弁（様）細胞$", re.I).sub(u"骨髄検査＝花弁細胞", text)
        text = re.compile(u"^蛍光免疫染色＝ＩｇＭ（＋ｎｏｄｕｌｅ＆ｌｏｏｐ）、Ｃ１ｑ（＋ｎｏｄｕｌｅ）、Ｆｉｂ（＋）、κｃｈａｉｎ（＋）$", re.I).sub(u"蛍光免疫染色＝ＩｇＭ（＋ｎｏｄｕｌｅ＆ｌｏｏｐ）、Ｃ１ｑ（＋ｎｏｄｕｌｅ）、Ｆｉｂ（＋）、κｃｈａｉｎ（＋）", text)
        text = re.compile(u"^ＨＩＴ（Ｔｙｐｅ２）$", re.I).sub(u"ＨＩＴ（Ｔｙｐｅ２）", text)
        text = re.compile(u"^腹腔内腫瘤＝ＡＭＬ髄外腫瘤（Ｇｒａｎｕｌｏｃｙｔｉｃ＿ｓａｒｃｏｍａ；ＧＳ）$", re.I).sub(u"腹腔内腫瘤＝ＡＭＬ髄外腫瘤", text)
        text = re.compile(u"^染色体検査＝ｉｎｖ（１６）$", re.I).sub(u"染色体検査＝ｉｎｖ（１６）", text)
        text = re.compile(u"^髄質嚢胞性腎疾患（ＭＣＫＤ）$", re.I).sub(u"髄質嚢胞性腎疾患", text)
        text = re.compile(u"^無呼吸低呼吸指数　（ＡＨＩ）／上昇$", re.I).sub(u"無呼吸低呼吸指数　／上昇", text)
        text = re.compile(u"^染色体分析＝ｄｅｌ（２０ｑ）$", re.I).sub(u"染色体分析＝ｄｅｌ（２０ｑ）", text)
        text = re.compile(u"^染色体検査＝ｔ（９；２２）（ｑ３４；ｑ１１．２）$", re.I).sub(u"染色体検査＝ｔ（９；２２）（ｑ３４；ｑ１１．２）", text)
        text = re.compile(u"^リンパ節生検＝　ＣＤ２０（−）・ＣＤ３０（＋）ホジキン様巨細胞$", re.I).sub(u"リンパ節生検＝　ＣＤ２０（−）・ＣＤ３０（＋）ホジキン様巨細胞", text)
        text = re.compile(u"^リンパ節生検＝ＣＤ１５（−）・ＣＤ２０（＋）・ＣＤ３０（−）異型細胞びまん性結節状増殖$", re.I).sub(u"リンパ節生検＝ＣＤ１５（−）・ＣＤ２０（＋）・ＣＤ３０（−）異型細胞びまん性結節状増殖", text)
        text = re.compile(u"^溶連菌感染後糸球体腎炎（ＰＳＡＧＮ）$", re.I).sub(u"溶連菌感染後糸球体腎炎", text)
        text = re.compile(u"^免疫染色＝ＣＤ２０（＋）$", re.I).sub(u"免疫染色＝ＣＤ２０（＋）", text)
        text = re.compile(u"^免疫染色＝ＣＤ３（−）$", re.I).sub(u"免疫染色＝ＣＤ３（−）", text)
        text = re.compile(u"^骨髄穿刺＝　ｄｅｒ（９）ｔ（１；９）$", re.I).sub(u"骨髄穿刺＝　ｄｅｒ（９）ｔ（１；９）", text)
        text = re.compile(u"^骨髄＝アウエル小体・ｔ（８；２１）$", re.I).sub(u"骨髄＝アウエル小体・ｔ（８；２１）", text)
        text = re.compile(u"^Ｈ：慢性炎症性脱髄性多発神経炎（ＣＩＤＰ）$", re.I).sub(u"Ｈ：慢性炎症性脱髄性多発神経炎", text)
        text = re.compile(u"^サプリメント（エビオス錠）$", re.I).sub(u"サプリメント", text)
        text = re.compile(u"^染色体検査＝４６，ＸＹ，ｔ（９；２２）（ｑ３４；ｑ１１．２）$", re.I).sub(u"染色体検査＝４６，ＸＹ，ｔ（９；２２）（ｑ３４；ｑ１１．２）", text)
        text = re.compile(u"^１．２５（ＯＨ）２Ｖｉｔ．Ｄ／上昇$", re.I).sub(u"１．２５（ＯＨ）２Ｖｉｔ．Ｄ／上昇", text)
        text = re.compile(u"^血液＝血漿レニン活性（ＰＲＡ）／高値$", re.I).sub(u"血液＝血漿レニン活性／高値", text)
        text = re.compile(u"^血液＝アルドステロン（ＰＡＣ）／高値$", re.I).sub(u"血液＝アルドステロン／高値", text)
        text = re.compile(u"^不適切ＴＳＨ分泌症候群（ＳＩＴＳＨ）$", re.I).sub(u"不適切ＴＳＨ分泌症候群", text)
        text = re.compile(u"^染色体＝４６・ＸＹ・ｉｎｖ（３）（ｑ２１ｑ２６．２）［２０／２０］$", re.I).sub(u"染色体＝４６・ＸＹ・ｉｎｖ（３）（ｑ２１ｑ２６．２）［２０／２０］", text)
        text = re.compile(u"^ｆｒｏｍ＿ｏｒｉｇｉｎａｌ$", re.I).sub(u"ｆｒｏｍ＿ｏｒｉｇｉｎａｌ", text)
        text = re.compile(u"^限局性結節性過形成（ＦＮＨ）$", re.I).sub(u"限局性結節性過形成", text)
        text = re.compile(u"^周産期心筋症（産褥期心筋症）$", re.I).sub(u"周産期心筋症", text)
        text = re.compile(u"^乳房外パジェット（ＥＭＰＤ）$", re.I).sub(u"乳房外パジェット", text)
        text = re.compile(u"^〔穿通性大動脈潰瘍〕（　ｐｅｎｅｔｒａｔｉｎｇ＿ａｔｈｅｒｏｓｃｌｅｒｏｔｉｃ＿ｕｌｃｅｒ）$", re.I).sub(u"〔穿通性大動脈潰瘍〕", text)
        text = re.compile(u"^ミトコンドリア病（ＭＥＬＡＳ）$", re.I).sub(u"ミトコンドリア病", text)
        text = re.compile(u"^肺腫瘍血栓性微小血管症（Ｐｕｌｍｏｎａｒｙ　ｔｕｍｏｒ　ｔｈｒｏｍｂｏｔｉｃ　ｍｉｃｒｏａｎｇｉｏｐａｔｈｙ）（ＰＴＴＭ）$", re.I).sub(u"肺腫瘍血栓性微小血管症", text)
        text = re.compile(u"^房室結節リエントリ−性頻拍（ＡＶＮＲＴ）$", re.I).sub(u"房室結節リエントリ−性頻拍", text)
        text = re.compile(u"^古典的ホジキンリンパ腫（ＣＨＬ、混合細胞性）$", re.I).sub(u"古典的ホジキンリンパ腫", text)
        text = re.compile(u"^ボセンタン（副作用）$", re.I).sub(u"ボセンタン副作用", text)
        text = re.compile(u"^トルバプタン（副作用）$", re.I).sub(u"トルバプタン副作用", text)
        text = re.compile(u"^トルバプタン（効果）$", re.I).sub(u"トルバプタン副作用", text)
        text = re.compile(u"^ベプリジル（副作用）$", re.I).sub(u"ベプリジル副作用", text)
        text = re.compile(u"^［抗生物質（副作用）］$", re.I).sub(u"［抗生物質副作用］", text)
        text = re.compile(u"^２次性Ｃｏｍｐｏｓｉｔｅ　ｌｙｍｐｈｏｍａ（ＡＩＴＬ＋ＤＬＢＣＬ）　$", re.I).sub(u"２次性Ｃｏｍｐｏｓｉｔｅ　ｌｙｍｐｈｏｍａ（ＡＩＴＬ＋ＤＬＢＣＬ）　", text)
        text = re.compile(u"^ＰＴＣＬ＿（ＮＯＳ）$", re.I).sub(u"ＰＴＣＬ＿（ＮＯＳ）", text)
        text = re.compile(u"^Ｂｌａｓｔｉｃ＿Ｐｌａｓｍａｃｙｔｏｉｄ＿Ｄｅｎｄｒｉｔｉｃ＿Ｃｅｌｌ＿Ｎｅｏｐｌａｓｍ（ＢＰＤＣＮ）$", re.I).sub(u"Ｂｌａｓｔｉｃ＿Ｐｌａｓｍａｃｙｔｏｉｄ＿Ｄｅｎｄｒｉｔｉｃ＿Ｃｅｌｌ＿Ｎｅｏｐｌａｓｍ", text)
        text = re.compile(u"^骨髄異形成症候群（ＭＤＳ）$", re.I).sub(u"骨髄異形成症候群", text)
        text = re.compile(u"^急性汎骨髄症（ＡＰＭＦ）$", re.I).sub(u"急性汎骨髄症", text)
        text = re.compile(u"^［１Ａ型糖尿病］１型糖尿病（自己免疫性）$", re.I).sub(u"［１Ａ型糖尿病］１型糖尿病", text)
        text = re.compile(u"^赤芽球癆（ｐｕｒｅ＿ｒｅｄ＿ｃｅｌｌ＿ａｐｌａｓｉａ）$", re.I).sub(u"赤芽球癆", text)
        text = re.compile(u"^血栓性血小板減少性紫斑病（ＴＴＰ）$", re.I).sub(u"血栓性血小板減少性紫斑病", text)
        text = re.compile(u"^急性リンパ性白血病（ＡＬＬ）$", re.I).sub(u"急性リンパ性白血病", text)
        text = re.compile(u"^顆粒球性肉腫（Ｇｒａｎｕｌｏｃｙｔｉｃ　ｓａｒｃｏｍａ）$", re.I).sub(u"顆粒球性肉腫", text)
        text = re.compile(u"^アレルギ−性肉芽腫性血管炎（Ｃｈｕｒｇ　Ｓｔｒａｕｓｓ症候群）$", re.I).sub(u"アレルギ−性肉芽腫性血管炎", text)
        text = re.compile(u"^コレステロ−ル塞栓症（ｂｌｕｅ　ｔｏｅ　ｓｙｎｄｒｏｍｅ）$", re.I).sub(u"コレステロ−ル塞栓症", text)
        text = re.compile(u"^亜急性壊死性リンパ節炎（菊池病）$", re.I).sub(u"亜急性壊死性リンパ節炎", text)
        text = re.compile(u"^全身性エリテマト−デス（ＳＬＥ）$", re.I).sub(u"全身性エリテマト−デス", text)
        text = re.compile(u"^悪性リンパ腫（非ホジキンリンパ腫）$", re.I).sub(u"悪性リンパ腫", text)
        text = re.compile(u"^リンパ管腫症（ｌｙｍｐｈａｎｇｉｏｍａｔｏｓｉｓ）$", re.I).sub(u"リンパ管腫症", text)
        text = re.compile(u"^Ｖ−Ｐシャント（脳室−腹腔）感染$", re.I).sub(u"Ｖ−Ｐシャント感染", text)
        text = re.compile(u"^悪性リンパ腫（大細胞型Ｂ細胞リンパ腫）$", re.I).sub(u"悪性リンパ腫", text)
        text = re.compile(u"^好酸球増加症候群（ＨＥＳ）$", re.I).sub(u"好酸球増加症候群", text)
        text = re.compile(u"^強皮症（ＣＲＥＳＴ症候群）$", re.I).sub(u"強皮症", text)
        text = re.compile(u"^好酸球増多症候群（ＨＥＳ）$", re.I).sub(u"好酸球増多症候群", text)
        text = re.compile(u"^ミトコンドリア脳筋症（ＭＥＬＡＳ）$", re.I).sub(u"ミトコンドリア脳筋症", text)
        text = re.compile(u"^急性胃粘膜病変（ＡＧＭＬ）$", re.I).sub(u"急性胃粘膜病変", text)
        text = re.compile(u"^移植片対宿主病（ＧＶＨＤ）　$", re.I).sub(u"移植片対宿主病　", text)
        text = re.compile(u"^ｉｎｔｒａｖａｓｃｕｌａｒ＿ｍａｌｉｇｎａｎｔ＿ｌｙｍｐｈｏｍａｔｏｓｉｓ（ＩＭＬ）$", re.I).sub(u"ｉｎｔｒａｖａｓｃｕｌａｒ＿ｍａｌｉｇｎａｎｔ＿ｌｙｍｐｈｏｍａｔｏｓｉｓ", text)
        text = re.compile(u"^ｍｕｌｔｉｃｅｎｔｒｉｃ＿Ｃａｓｔｌｅｍａｎ＿ｄｉｓｅａｓｅ（ＭＣＤ）　$", re.I).sub(u"ｍｕｌｔｉｃｅｎｔｒｉｃ＿Ｃａｓｔｌｅｍａｎ＿ｄｉｓｅａｓｅ　", text)
        text = re.compile(u"^サイトメガロウイルス（ＣＭＶ）感染$", re.I).sub(u"サイトメガロウイルス感染", text)
        text = re.compile(u"^悪性リンパ腫（ｄｉｆｆｕｓｅ　ｌａｒｇｅ　Ｂｃｅｌｌ　ｔｙｐｅ）$", re.I).sub(u"悪性リンパ腫", text)
        text = re.compile(u"^抗糸球体基底膜抗体腎炎（抗ＧＢＭ抗体腎炎）$", re.I).sub(u"抗糸球体基底膜抗体腎炎", text)
        text = re.compile(u"^ＡＮＣＡ関連腎炎（顕微鏡的多発性血管炎）$", re.I).sub(u"ＡＮＣＡ関連腎炎", text)
        text = re.compile(u"^悪性リンパ腫（濾胞性リンパ腫）$", re.I).sub(u"悪性リンパ腫", text)
        text = re.compile(u"^多巣性線維硬化症（Ｍｕｌｔｉｆｏｃａｌ＿ｆｉｂｒｏｓｃｒｅｌｏｓｉｓ）$", re.I).sub(u"多巣性線維硬化症", text)
        text = re.compile(u"^膵管内乳頭状腫瘍（ＩＭＰＴ）$", re.I).sub(u"膵管内乳頭状腫瘍", text)
        text = re.compile(u"^亜急性壊死性リンパ節炎（菊池氏病）$", re.I).sub(u"亜急性壊死性リンパ節炎", text)
        text = re.compile(u"^膀胱癌（小細胞癌）$", re.I).sub(u"膀胱癌", text)
        text = re.compile(u"^血管内大細胞型Ｂ細胞性リンパ腫（ＩＶＬ）$", re.I).sub(u"血管内大細胞型Ｂ細胞性リンパ腫", text)
        text = re.compile(u"^びまん性大細胞型Ｂ細胞リンパ腫（ＤＬＢＣＬ）$", re.I).sub(u"びまん性大細胞型Ｂ細胞リンパ腫", text)
        text = re.compile(u"^膵Ｓｏｌｉｄ−ｐｓｅｕｄｏｐａｐｉｌｌａｒｙ＿ｎｅｏｐｌａｓｍ（ＳＰＮ）$", re.I).sub(u"膵Ｓｏｌｉｄ−ｐｓｅｕｄｏｐａｐｉｌｌａｒｙ＿ｎｅｏｐｌａｓｍ", text)
        text = re.compile(u"^カルニチンパルミトイルトランスフェラ−ゼ（ＣＰＴ）２欠損症$", re.I).sub(u"カルニチンパルミトイルトランスフェラ−ゼ２欠損症", text)
        text = re.compile(u"^成人発症スティル病（ＡＯＳＤ）$", re.I).sub(u"成人発症スティル病", text)
        text = re.compile(u"^Ｃｌｏｓｔｒｉｄｉｕｍ＿ｄｉｆｆｉｃｉｌｅｃｏｌｉｔｉｓ（ＣＤＣ）$", re.I).sub(u"Ｃｌｏｓｔｒｉｄｉｕｍ＿ｄｉｆｆｉｃｉｌｅｃｏｌｉｔｉｓ", text)
        text = re.compile(u"^逆流性食道炎（ＬＡ分類＿ｇｒａｄｅ＿Ｄ）$", re.I).sub(u"逆流性食道炎", text)
        text = re.compile(u"^好酸球性胃腸炎（ＥＧＥ）$", re.I).sub(u"好酸球性胃腸炎", text)
        text = re.compile(u"^好酸球増加症候群（ＨＥＳ）$", re.I).sub(u"好酸球増加症候群", text)
        text = re.compile(u"^血管内悪性リンパ腫（ＩＶＬ）$", re.I).sub(u"血管内悪性リンパ腫", text)
        text = re.compile(u"^薬物性肝障害（ＤＩＬＩ）$", re.I).sub(u"薬物性肝障害", text)
        text = re.compile(u"^自己免疫性肝炎（ＡＩＨ）$", re.I).sub(u"自己免疫性肝炎", text)
        text = re.compile(u"^びまん性大細胞型Ｂ細胞性リンパ腫（ＤＬＢＣＬ）$", re.I).sub(u"びまん性大細胞型Ｂ細胞性リンパ腫", text)
        text = re.compile(u"^シェ−ンラインヘノッホ紫斑病（ＨＳＰ）$", re.I).sub(u"シェ−ンラインヘノッホ紫斑病", text)
        text = re.compile(u"^ｓｏｌｉｄ−ｐｓｕｄｏｐａｐｉｌｌａｒｙ＿ｎｅｏｐｌａｓｍ（ＳＰＮ）$", re.I).sub(u"ｓｏｌｉｄ−ｐｓｕｄｏｐａｐｉｌｌａｒｙ＿ｎｅｏｐｌａｓｍ", text)
        text = re.compile(u"^ｃｏｌｌａｇｅｎｏｕｓ＿ｃｏｌｉｔｉｓ（ＣＣ）$", re.I).sub(u"ｃｏｌｌａｇｅｎｏｕｓ＿ｃｏｌｉｔｉｓ", text)
        text = re.compile(u"^アイザックス症候群（Ｉｓａａｃｓ症候群）$", re.I).sub(u"アイザックス症候群", text)
        text = re.compile(u"^Ｈｅｒｍａｎｓｋｙ−Ｐｕｄｌａｋ症候群（ＨＰＳ）$", re.I).sub(u"Ｈｅｒｍａｎｓｋｙ−Ｐｕｄｌａｋ症候群", text)
        text = re.compile(u"^全身性エリテマト−デス（ＳＬＥ）$", re.I).sub(u"全身性エリテマト−デス", text)
        text = re.compile(u"^巣状分節性糸球体硬化症（ＦＳＧＳ）$", re.I).sub(u"巣状分節性糸球体硬化症", text)
        text = re.compile(u"^黄色爪症候群（Ｙｅｌｌｏｗ＿ｎａｉｌ＿ｓｙｎｄｒｏｍｅ）$", re.I).sub(u"黄色爪症候群", text)
        text = re.compile(u"^黄色爪症候群（Ｙｅｌｌｏｗ　ｎａｉｌ　ｓｙｎｄｒｏｍｅ）$", re.I).sub(u"黄色爪症候群", text)
        text = re.compile(u"^ＤｉＧｅｏｒｇｅ症候群（２２ｑ１１．２欠失症候群）$", re.I).sub(u"ＤｉＧｅｏｒｇｅ症候群", text)
        text = re.compile(u"^坐滅症候群（クラッシュ症候群）$", re.I).sub(u"坐滅症候群", text)
        text = re.compile(u"^Ｌｉｐｏｍａｔｏｕｓ　Ｐｓｅｕｄｏｈｙｐｅｒｔｒｏｐｈｙ　ｏｆ　ｔｈｅ　Ｐａｎｃｒｅａｓ（ＬＰＰ）$", re.I).sub(u"Ｌｉｐｏｍａｔｏｕｓ　Ｐｓｅｕｄｏｈｙｐｅｒｔｒｏｐｈｙ　ｏｆ　ｔｈｅ　Ｐａｎｃｒｅａｓ", text)
        text = re.compile(u"^フルニエ症候群（壊疽性筋膜炎）$", re.I).sub(u"フルニエ症候群", text)
        text = re.compile(u"^手術部位感染（ＳＳＩ）$", re.I).sub(u"手術部位感染", text)
        text = re.compile(u"^ヘノッホ・シェ−ンライン紫斑病（ＨＳＰ）$", re.I).sub(u"ヘノッホ・シェ−ンライン紫斑病", text)
        text = re.compile(u"^催不整脈性右室心筋症（ＡＲＶＣ）$", re.I).sub(u"催不整脈性右室心筋症", text)
        text = re.compile(u"^後天性免疫不全症候群＊（ＡＩＤＳ）$", re.I).sub(u"後天性免疫不全症候群＊", text)
        text = re.compile(u"^多腺性自己免疫症候群（ＡＰＳ）３型$", re.I).sub(u"多腺性自己免疫症候群３型", text)
        text = re.compile(u"^特発性好酸球増多症候群（ＨＥＳ）$", re.I).sub(u"特発性好酸球増多症候群", text)
        text = re.compile(u"^ＡＡＡ症候群（トリプルＡ症候群）$", re.I).sub(u"ＡＡＡ症候群", text)
        text = re.compile(u"^顕微鏡的多発血管炎（ＭＰＡ）$", re.I).sub(u"顕微鏡的多発血管炎", text)
        text = re.compile(u"^ＡＴ−３欠損症（１型）$", re.I).sub(u"ＡＴ−３欠損症", text)
        text = re.compile(u"^多発血管炎性肉芽腫症（Ｗｅｇｅｎｅｒ肉芽腫症）$", re.I).sub(u"多発血管炎性肉芽腫症", text)
        text = re.compile(u"^特発性アルドステロン症（ＩＨＡ）$", re.I).sub(u"特発性アルドステロン症", text)
        text = re.compile(u"^Ｓｅｇｍｅｎｔａｌ＿ａｒｔｅｒｉａｌ＿ｍｅｄｉｏｌｙｓｉｓ（ＳＡＭ）$", re.I).sub(u"Ｓｅｇｍｅｎｔａｌ＿ａｒｔｅｒｉａｌ＿ｍｅｄｉｏｌｙｓｉｓ", text)
        text = re.compile(u"^ニュ−モシスチス肺炎（ＰＣＰ）$", re.I).sub(u"ニュ−モシスチス肺炎", text)
        text = re.compile(u"^関節リウマチ（ＲＡ）$", re.I).sub(u"関節リウマチ", text)
        text = re.compile(u"^非結核性抗酸菌症（ＮＴＭ）$", re.I).sub(u"非結核性抗酸菌症", text)
        text = re.compile(u"^Ａ型インフルエンザ（Ｈ１Ｎ１）肺炎$", re.I).sub(u"Ａ型インフルエンザ肺炎", text)
        text = re.compile(u"^Ｃｌｉｎｉｃａｌｌｙ＿Ａｍｙｏｐａｔｈｉｃ＿Ｄｅｒｍａｔｏｍｙｏｓｉｔｉｓ（ＣＡＤＭ）$", re.I).sub(u"Ｃｌｉｎｉｃａｌｌｙ＿Ａｍｙｏｐａｔｈｉｃ＿Ｄｅｒｍａｔｏｍｙｏｓｉｔｉｓ", text)
        text = re.compile(u"^後天性免疫不全症候群（ＡＩＤＳ）$", re.I).sub(u"後天性免疫不全症候群", text)
        text = re.compile(u"^Ｐｕｌｍｏｎａｒｙ＿Ｔｕｍｏｒ＿Ｔｈｒｏｍｂｏｔｉｃ＿Ｍｉｃｒｏａｎｇｉｏｐａｔｈｙ（ＰＴＴＭ）$", re.I).sub(u"Ｐｕｌｍｏｎａｒｙ＿Ｔｕｍｏｒ＿Ｔｈｒｏｍｂｏｔｉｃ＿Ｍｉｃｒｏａｎｇｉｏｐａｔｈｙ", text)
        text = re.compile(u"^膵Ｓｏｌｉｄ＿ｐｓｅｕｄｏｐａｐｉｌｌａｒｙｎｅｏｐｌａｓｍ（ＳＰＮ）$", re.I).sub(u"膵Ｓｏｌｉｄ＿ｐｓｅｕｄｏｐａｐｉｌｌａｒｙｎｅｏｐｌａｓｍ", text)
        text = re.compile(u"^大腸ｄｉｆｆｕｓｅ　ｌａｒｇｅ　Ｂ　ｃｅｌｌ　ｌｙｍｐｈｏｍａ（ＤＬＢＣＬ）$", re.I).sub(u"大腸ｄｉｆｆｕｓｅ　ｌａｒｇｅ　Ｂ　ｃｅｌｌ　ｌｙｍｐｈｏｍａ", text)
        text = re.compile(u"^Ｓｙｓｔｅｍｉｃ＿ｌｕｐｕｓｅｒｙｔｈｅｍａｔｏｕｓ（ＳＬＥ）$", re.I).sub(u"Ｓｙｓｔｅｍｉｃ＿ｌｕｐｕｓｅｒｙｔｈｅｍａｔｏｕｓ", text)
        text = re.compile(u"^Ｓｔｅｖｅｎｓ−Ｊｏｈｎｓｏｎ症候群（ＳＪＳ）$", re.I).sub(u"Ｓｔｅｖｅｎｓ−Ｊｏｈｎｓｏｎ症候群", text)
        text = re.compile(u"^大動脈炎症候群（高安病）$", re.I).sub(u"大動脈炎症候群", text)
        text = re.compile(u"^後天性ｖｏｎ＿Ｗｉｌｌｅｂｒａｎｄ病（Ｈｅｙｄｅ症候群）$", re.I).sub(u"後天性ｖｏｎ＿Ｗｉｌｌｅｂｒａｎｄ病", text)
        text = re.compile(u"^早期再分極症候群（Ｊ波症候群）$", re.I).sub(u"早期再分極症候群", text)
        text = re.compile(u"^自己免疫性多内分泌腺症候群（ＡＰＳ３型）$", re.I).sub(u"自己免疫性多内分泌腺症候群", text)
        text = re.compile(u"^肝原発神経内分泌癌（小細胞癌）$", re.I).sub(u"肝原発神経内分泌癌", text)
        text = re.compile(u"^完全４倍体（９２，ＸＸＸＸ）白血病$", re.I).sub(u"完全４倍体白血病", text)
        text = re.compile(u"^肺癌（腺癌）$", re.I).sub(u"肺癌", text)
        text = re.compile(u"^筋萎縮性側索硬化症（ＡＬＳ）$", re.I).sub(u"筋萎縮性側索硬化症", text)
        text = re.compile(u"^混合性結合組織病（ＭＣＴＤ）$", re.I).sub(u"混合性結合組織病", text)
        text = re.compile(u"^〔漢方薬（甘草）・飲酒　副作用〕$", re.I).sub(u"〔漢方薬・飲酒　副作用〕", text)
        text = re.compile(u"^自己免疫性膵炎（ＡＩＰ）　$", re.I).sub(u"自己免疫性膵炎　", text)
        text = re.compile(u"^家族性高Ｌｐ（ａ）血症$", re.I).sub(u"家族性高Ｌｐ血症", text)
        text = re.compile(u"^ｃｌｉｎｉｃａｌｌｙ＿ａｍｙｏｐａｔｈｉｃｄｅｒｍａｔｏｍｙｏｓｉｔｉｓ（$", re.I).sub(u"ｃｌｉｎｉｃａｌｌｙ＿ａｍｙｏｐａｔｈｉｃｄｅｒｍａｔｏｍｙｏｓｉｔｉｓ（", text)
        text = re.compile(u"^カ−ニ−複合（Ｃａｒｎｅｙ　ｃｏｍｐｌｅｘ）$", re.I).sub(u"カ−ニ−複合", text)
        text = re.compile(u"^ＭａｌｉｇｎａｎｔＬｙｍｐｈｏｍａ（ｄｕｆｆｕｓｅｌａｒｇｅＢ＿ｃｅｌｌ）$", re.I).sub(u"ＭａｌｉｇｎａｎｔＬｙｍｐｈｏｍａ", text)
        text = re.compile(u"^自己免疫性多内分泌腺症候群（ＡＰＳ）２型$", re.I).sub(u"自己免疫性多内分泌腺症候群２型", text)
        text = re.compile(u"^高トリグリセリド（ＴＧ）血症$", re.I).sub(u"高トリグリセリド血症", text)
        text = re.compile(u"^Ｐｈ陽性急性骨髄性白血病（ＡＭＬ）$", re.I).sub(u"Ｐｈ陽性急性骨髄性白血病", text)
        text = re.compile(u"^フィラデルフィア染色体陽性急性骨髄性白血病（Ｐｈ＋ＡＭＬ）$", re.I).sub(u"フィラデルフィア染色体陽性急性骨髄性白血病", text)
        text = re.compile(u"^急性好酸球性肺炎（ＡＥＰ）$", re.I).sub(u"急性好酸球性肺炎", text)
        text = re.compile(u"^血栓性血小板減少性紫斑病　（ＴＴＰ）$", re.I).sub(u"血栓性血小板減少性紫斑病　", text)
        text = re.compile(u"^脳梗塞（左＊放線冠）$", re.I).sub(u"脳梗塞", text)
        text = re.compile(u"^バゾプレシン分泌異常症（ＳＩＡＤＨ）$", re.I).sub(u"バゾプレシン分泌異常症", text)
        text = re.compile(u"^Ｐｒａｄｅｒ−Ｗｉｌｌｉ症候群（ＰＷＳ）$", re.I).sub(u"Ｐｒａｄｅｒ−Ｗｉｌｌｉ症候群", text)
        text = re.compile(u"^偽性副甲状腺機能低下症（ＰＨＰ＿Ｉｂ）$", re.I).sub(u"偽性副甲状腺機能低下症", text)
        text = re.compile(u"^鉱質コルチコイド反応性低Ｎａ血症（ＭＲＨＥ）$", re.I).sub(u"鉱質コルチコイド反応性低Ｎａ血症", text)
        text = re.compile(u"^非閉塞性腸管虚血症（ＮＯＭＩ）$", re.I).sub(u"非閉塞性腸管虚血症", text)
        text = re.compile(u"^血栓性微小血管障害（ＴＭＡ）$", re.I).sub(u"血栓性微小血管障害", text)
        text = re.compile(u"^多腺性自己免疫症候群（ＡＰＳ）$", re.I).sub(u"多腺性自己免疫症候群", text)
        text = re.compile(u"^遠位型腎尿細管性アシド−シス（１型）　$", re.I).sub(u"遠位型腎尿細管性アシド−シス　", text)
        text = re.compile(u"^抗ＡＱＰ４抗体関連視神経脊髄炎（ＮＭＯ）$", re.I).sub(u"抗ＡＱＰ４抗体関連視神経脊髄炎", text)
        text = re.compile(u"^びまん性レビ−小体病（ＤＬＢＤ）$", re.I).sub(u"びまん性レビ−小体病", text)
        text = re.compile(u"^全身性アミロ−ドシス（ＡＡ型）$", re.I).sub(u"全身性アミロ−ドシス", text)
        text = re.compile(u"^Ｔ細胞前リンパ性白血病（Ｔ−ＰＬＬ）$", re.I).sub(u"Ｔ細胞前リンパ性白血病", text)
        text = re.compile(u"^ａｓｉａｎ＿ｖａｒｉａｎｔｏｆｉｎｔｒａｖａｓｃｕｌａｒ＿ｌａｒｇｅ＿Ｂ−ｃｅｌｌ＿ｌｙｍｐｈｏｍａ（ＡＶＩＬＢＣＬ）$", re.I).sub(u"ａｓｉａｎ＿ｖａｒｉａｎｔｏｆｉｎｔｒａｖａｓｃｕｌａｒ＿ｌａｒｇｅ＿Ｂ−ｃｅｌｌ＿ｌｙｍｐｈｏｍａ", text)
        text = re.compile(u"^溶血性尿毒症症候群（ＨＵＳ）$", re.I).sub(u"溶血性尿毒症症候群", text)
        text = re.compile(u"^骨髄異形成症候群（芽球増加型不応性貧血）$", re.I).sub(u"骨髄異形成症候群", text)
        text = re.compile(u"^ヘアリ−細胞白血病（ＨＣＬ）$", re.I).sub(u"ヘアリ−細胞白血病", text)
        text = re.compile(u"^慢性骨髄単球性白血病（ＣＭＭＬ）$", re.I).sub(u"慢性骨髄単球性白血病", text)
        text = re.compile(u"^骨髄異型性症候群（ＭＤＳ）$", re.I).sub(u"骨髄異型性症候群", text)
        text = re.compile(u"^出血性大腸炎（Ｏ−１５７）$", re.I).sub(u"出血性大腸炎", text)
        text = re.compile(u"^抗リン脂質抗体症候群（ＡＰＳ）$", re.I).sub(u"抗リン脂質抗体症候群", text)
        text = re.compile(u"^蜂窩織炎（Ａ群溶血性連鎖球菌）$", re.I).sub(u"蜂窩織炎", text)
        text = re.compile(u"^ｈｅｒｐｅｓ＿ｚｏｓｔｅｒ＿ｅｎｃｅｐｈａｌｉｔｉｓ（ＨＺＥ）$", re.I).sub(u"ｈｅｒｐｅｓ＿ｚｏｓｔｅｒ＿ｅｎｃｅｐｈａｌｉｔｉｓ", text)
        text = re.compile(u"^劇症型肺炎（〔レジオネラ疑い〕）$", re.I).sub(u"劇症型肺炎", text)
        text = re.compile(u"^原発性マクログロブリン血症（ＷＭ$", re.I).sub(u"原発性マクログロブリン血症（ＷＭ", text)
        text = re.compile(u"^血管内リンパ腫（ＩＶＬ）$", re.I).sub(u"血管内リンパ腫", text)
        text = re.compile(u"^ｄｉｆｆｕｓｅｌａｒｇｅＢｃｅｌｌ＿ｌｙｍｐｈｏｍａ（ＤＬＢＣＬ）$", re.I).sub(u"ｄｉｆｆｕｓｅｌａｒｇｅＢｃｅｌｌ＿ｌｙｍｐｈｏｍａ", text)
        text = re.compile(u"^Ｐｕｒｅｗｈｉｔｅｃｅｌｌａｐｌａｓｉａ（ＰＷＣＡ）$", re.I).sub(u"Ｐｕｒｅｗｈｉｔｅｃｅｌｌａｐｌａｓｉａ", text)
        text = re.compile(u"^急速進行性糸球体腎炎（抗ＧＢＭ抗体陽性・ＭＰＯ−ＡＮＣＡ陽性）$", re.I).sub(u"急速進行性糸球体腎炎", text)
        text = re.compile(u"^急性散在性脳脊髄炎（ＡＤＥＭ）$", re.I).sub(u"急性散在性脳脊髄炎", text)
        text = re.compile(u"^新型インフルエンザＡ（Ｈ１Ｎ１）脳症$", re.I).sub(u"新型インフルエンザＡ脳症", text)
        text = re.compile(u"^骨髄異形成症候群（ＭＤＳ）　$", re.I).sub(u"骨髄異形成症候群　", text)
        text = re.compile(u"^食中毒（セレウス菌・毒素型）$", re.I).sub(u"食中毒", text)
        text = re.compile(u"^骨髄異形成症候群（ＲＣＭＤ）$", re.I).sub(u"骨髄異形成症候群", text)
        text = re.compile(u"^幼虫移行症（蛔虫）$", re.I).sub(u"幼虫移行症", text)
        text = re.compile(u"^好酸球増多症候群（ＨＥＳ）$", re.I).sub(u"好酸球増多症候群", text)
        text = re.compile(u"^肺吸虫症（ウエステルマン肺吸虫・宮崎肺吸虫）$", re.I).sub(u"肺吸虫症", text)
        text = re.compile(u"^内臓幼虫移行症（回虫）$", re.I).sub(u"内臓幼虫移行症", text)
        text = re.compile(u"^細菌性髄膜炎（嫌気性菌）$", re.I).sub(u"細菌性髄膜炎", text)
        text = re.compile(u"^間質性肺炎（ＮＳＩＰあるいはＣＯＰ）$", re.I).sub(u"間質性肺炎", text)
        text = re.compile(u"^膠原病性間質性肺炎（皮膚筋炎）$", re.I).sub(u"膠原病性間質性肺炎", text)
        text = re.compile(u"^緩徐進行型１型糖尿病（ＳＰＩＤＤＭ）$", re.I).sub(u"緩徐進行型１型糖尿病", text)
        text = re.compile(u"^心外膜胸膜炎（ａｃｔｉｎｏｍｙｃｅｓ＿ｓｐ）$", re.I).sub(u"心外膜胸膜炎", text)
        text = re.compile(u"^非閉塞性腸間膜虚血症（ＮＯＭＩ）$", re.I).sub(u"非閉塞性腸間膜虚血症", text)
        text = re.compile(u"^〔インタ−フェロン療法（ＩＦＮ）副作用〕$", re.I).sub(u"〔インタ−フェロン療法副作用〕", text)
        text = re.compile(u"^アルコ−ル性ケトアシド−シス（ＡＫＡ）$", re.I).sub(u"アルコ−ル性ケトアシド−シス", text)
        text = re.compile(u"^好酸球性肉芽腫性多発血管炎（Ｃｈｕｒｇ−Ｓｔｒａｕｓｓ症候群）$", re.I).sub(u"好酸球性肉芽腫性多発血管炎", text)
        text = re.compile(u"^ミネラルコルチコイド反応性低Ｎａ血症（ＭＲＨＥ）　$", re.I).sub(u"ミネラルコルチコイド反応性低Ｎａ血症　", text)
        text = re.compile(u"^無筋炎型皮膚筋炎（ＡＤＭ）$", re.I).sub(u"無筋炎型皮膚筋炎", text)
        text = re.compile(u"^急性骨髄性白血病（ＡＭＬ，Ｍ２）$", re.I).sub(u"急性骨髄性白血病", text)
        text = re.compile(u"^Ｈａｉｒｙ　ｃｅｌｌ　ｌｅｕｋｅｍｉａ（ＨＣＬ　Ｊａｐａｎｅｓｅ　ｖａｒｉａｎｔ）$", re.I).sub(u"Ｈａｉｒｙ　ｃｅｌｌ　ｌｅｕｋｅｍｉａ", text)
        text = re.compile(u"^閉塞性睡眠時無呼吸低呼吸症候群　（ＯＳＡＨＳ）　$", re.I).sub(u"閉塞性睡眠時無呼吸低呼吸症候群　　", text)
        text = re.compile(u"^抗リン脂質抗体症候群（ＡＰＳ）腎症$", re.I).sub(u"抗リン脂質抗体症候群腎症", text)
        text = re.compile(u"^骨髄異形成症候群（ＲＡＥＢ−１）$", re.I).sub(u"骨髄異形成症候群（ＲＡＥＢ−１）", text)

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
        text = re.sub(u"鬱", u"うつ", text)
        text = re.sub(u"&#039;", u"'", text)



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
        text = re.compile(u"↑IV↑型" ,re.I).sub( u"4型" ,text) #nocasesense
        text = re.compile(u"↑III↑型" ,re.I).sub( u"3型" ,text) #nocasesense
        text = re.compile(u"↑II↑型" ,re.I).sub( u"2型" ,text) #nocasesense
        text = re.compile(u"↑I↑型" ,re.I).sub( u"1型" ,text) #nocasesense
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
        text = re.compile(u"リンパ腫張" ,re.I).sub( u"リンパ節腫脹" ,text) #nocasesense
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
        text = re.compile(u"^マクロファージ活性化症候群/血球貪食症$", re.I).sub(u"マクロファージ活性化症候群／血球貪食症", text)
        text = re.compile(u"^KSHV/HHV8に関連しない原発性滲出性リンパ腫様リンパ腫$", re.I).sub(u"KSHV／HHV8に関連しない原発性滲出性リンパ腫様リンパ腫", text)
        text = re.compile(u"^NK/T細胞リンパ腫$", re.I).sub(u"NK／T細胞リンパ腫", text)
        text = re.compile(u"^自己免疫性肝炎/原発性胆汁性肝硬変オーバーラップ症候群$", re.I).sub(u"自己免疫性肝炎／原発性胆汁性肝硬変オーバーラップ症候群", text)
        text = re.compile(u"^T-cell/histiocyte_rich", re.I).sub(u"T-cell／histiocyte_rich", text)
        text = re.compile(u"^再生不良性貧血/骨髄異形成症候群$", re.I).sub(u"再生不良性貧血／骨髄異形成症候群", text)
        text = re.compile(u"^one-and-a-half_syndrome$", re.I).sub(u"1と2分の1症候群", text)
        text = re.compile(u"^One-and-a-half-syndrome$", re.I).sub(u"1と2分の1症候群", text)
        text = re.compile(u"^22q11.2欠失症候群$", re.I).sub(u"22q11.2欠失症候群", text)
        text = re.compile(u"^biclonal_gammopathy$", re.I).sub(u"2クローン性高ガンマグロブリン血症", text)
        text = re.compile(u"^Autoimmune_Polyglandular_Syndrome_TypeIII$", re.I).sub(u"3型多腺性自己免疫症候群", text)
        text = re.compile(u"^46XX_male$", re.I).sub(u"46XX男性", text)
        text = re.compile(u"^5q-症候群$", re.I).sub(u"5q-症候群", text)
        text = re.compile(u"^eight-and-a-half_syndrome$", re.I).sub(u"8と2分の1症候群", text)
        text = re.compile(u"^ACTH-independent_Macronodular_Adrenal_Hyperplasia$", re.I).sub(u"ACTH-独立大結節性副腎過形成", text)
        text = re.compile(u"^Group_A_streptococcus感染症$", re.I).sub(u"A群レンサ球菌感染症", text)
        text = re.compile(u"^HBV_reverse_seroconversion$", re.I).sub(u"B型肝炎ウイルス回復セロコンバージョン", text)
        text = re.compile(u"^B-cellリンパ腫$", re.I).sub(u"B細胞リンパ腫", text)
        text = re.compile(u"^B-cell_リンパ腫$", re.I).sub(u"B細胞リンパ腫", text)
        text = re.compile(u"^B-cell_悪性腫瘍$", re.I).sub(u"B細胞悪性腫瘍", text)
        text = re.compile(u"^C1q腎症$", re.I).sub(u"C1q腎症", text)
        text = re.compile(u"^CD20陽性IgD-λ型多発性骨髄腫$", re.I).sub(u"CD20陽性IgD-λ型多発性骨髄腫", text)
        text = re.compile(u"^CD4+、CD33+、CD56+acute_leukemia、リンパ腫$", re.I).sub(u"CD4抗原+、CD33抗原+、CD56抗原+急性白血病リンパ腫", text)
        text = re.compile(u"^GluRε2抗体陽性辺縁系脳炎$", re.I).sub(u"GluRε2抗体陽性辺縁系脳炎", text)
        text = re.compile(u"^Group_G_Streptococcus菌血症$", re.I).sub(u"G群レンサ球菌血症", text)
        text = re.compile(u"^H:osimertinib投与歴$", re.I).sub(u"H:オシメルチニブ投与歴", text)
        text = re.compile(u"^HIV関連Diffuse_large_B_cell_リンパ腫$", re.I).sub(u"HIV関連びまん性大細胞型B細胞リンパ腫", text)
        text = re.compile(u"^HLA-DRantigen-negativeAML$", re.I).sub(u"HLA-DR抗原陰性の急性骨髄性白血病", text)
        text = re.compile(u"^HTLV-1_associated_myelopathy$", re.I).sub(u"HTLV-1関連脊髄症", text)
        text = re.compile(u"^HTLV_asssciated_bronchopneumopathy$", re.I).sub(u"HTLV関連気管支肺症", text)
        text = re.compile(u"^ICU-Aquired_Weekness$", re.I).sub(u"ICU入院による衰弱", text)
        text = re.compile(u"^IgA_腎症$", re.I).sub(u"IgA_腎症", text)
        text = re.compile(u"^IgA血管炎$", re.I).sub(u"IgA血管炎", text)
        text = re.compile(u"^IgA腎炎$", re.I).sub(u"IgA腎炎", text)
        text = re.compile(u"^IgA腎症$", re.I).sub(u"IgA腎症", text)
        text = re.compile(u"^IgA単独欠損症$", re.I).sub(u"IgA単独欠損症", text)
        text = re.compile(u"^IgD型骨髄腫$", re.I).sub(u"IgD型骨髄腫", text)
        text = re.compile(u"^IgD型多発性骨髄腫$", re.I).sub(u"IgD型多発性骨髄腫", text)
        text = re.compile(u"^IGF-2産生胸腔内Solitary_fibrous_tumor$", re.I).sub(u"IGF-2産生胸腔内孤在性線維性腫瘍", text)
        text = re.compile(u"^IgG_H鎖Fcフラグメント病$", re.I).sub(u"IgG_H鎖Fcフラグメント病", text)
        text = re.compile(u"^IgG_λ型monoclonalgammopathy$", re.I).sub(u"IgG_λ型単クローン性免疫グロブリン血症", text)
        text = re.compile(u"^IgG2欠損症$", re.I).sub(u"IgG2欠損症", text)
        text = re.compile(u"^IgG4陰性自己免疫性膵炎$", re.I).sub(u"IgG4陰性自己免疫性膵炎", text)
        text = re.compile(u"^IgG4関連リンパ節症$", re.I).sub(u"IgG4関連リンパ節症", text)
        text = re.compile(u"^IgG4関連リンパ増殖症$", re.I).sub(u"IgG4関連リンパ増殖症", text)
        text = re.compile(u"^IgG4関連リンパ増殖性疾患$", re.I).sub(u"IgG4関連リンパ増殖性疾患", text)
        text = re.compile(u"^IgG4関連炎症性偽腫瘍$", re.I).sub(u"IgG4関連炎症性偽腫瘍", text)
        text = re.compile(u"^IgG4関連炎症性大動脈瘤$", re.I).sub(u"IgG4関連炎症性大動脈瘤", text)
        text = re.compile(u"^IgG4関連下垂体炎$", re.I).sub(u"IgG4関連下垂体炎", text)
        text = re.compile(u"^IgG4関連間質性腎炎$", re.I).sub(u"IgG4関連間質性腎炎", text)
        text = re.compile(u"^IgG4関連間質性肺炎$", re.I).sub(u"IgG4関連間質性肺炎", text)
        text = re.compile(u"^IgG4関連眼症$", re.I).sub(u"IgG4関連眼症", text)
        text = re.compile(u"^IgG4関連呼吸器疾患$", re.I).sub(u"IgG4関連呼吸器疾患", text)
        text = re.compile(u"^IgG4関連後腹膜繊維症$", re.I).sub(u"IgG4関連後腹膜線維症", text)
        text = re.compile(u"^IgG4関連後腹膜線維症$", re.I).sub(u"IgG4関連後腹膜線維症", text)
        text = re.compile(u"^IgG4関連硬化性疾患$", re.I).sub(u"IgG4関連硬化性疾患", text)
        text = re.compile(u"^IgG4関連硬化性胆管炎$", re.I).sub(u"IgG4関連硬化性胆管炎", text)
        text = re.compile(u"^IgG4関連視床下部下垂体炎$", re.I).sub(u"IgG4関連視床下部下垂体炎", text)
        text = re.compile(u"^IgG4関連自己免疫性膵炎$", re.I).sub(u"IgG4関連自己免疫性膵炎", text)
        text = re.compile(u"^IgG4関連自己免疫性膵炎・硬化性胆管炎$", re.I).sub(u"IgG4関連自己免疫性膵炎・硬化性胆管炎", text)
        text = re.compile(u"^IgG4関連疾患$", re.I).sub(u"IgG4関連疾患", text)
        text = re.compile(u"^IgG4関連疾患@肺$", re.I).sub(u"IgG4関連疾患@肺", text)
        text = re.compile(u"^IgG4関連疾患縦隔腫瘤$", re.I).sub(u"IgG4関連疾患縦隔腫瘤", text)
        text = re.compile(u"^IgG4関連収縮性心膜炎$", re.I).sub(u"IgG4関連収縮性心膜炎", text)
        text = re.compile(u"^IgG4関連症候群$", re.I).sub(u"IgG4関連症候群", text)
        text = re.compile(u"^IgG4関連腎炎$", re.I).sub(u"IgG4関連腎炎", text)
        text = re.compile(u"^IgG4関連腎症$", re.I).sub(u"IgG4関連腎症", text)
        text = re.compile(u"^IgG4-RKD$", re.I).sub(u"IgG4関連腎臓病", text)
        text = re.compile(u"^IgG4関連腎臓病$", re.I).sub(u"IgG4関連腎臓病", text)
        text = re.compile(u"^IgG4関連線維性縦隔炎$", re.I).sub(u"IgG4関連線維性縦隔炎", text)
        text = re.compile(u"^IgG4関連多臓器リンパ増殖症候群$", re.I).sub(u"IgG4関連多臓器リンパ増殖症候群", text)
        text = re.compile(u"^IgG4関連多臓器リンパ増殖性疾患$", re.I).sub(u"IgG4関連多臓器リンパ増殖性疾患", text)
        text = re.compile(u"^IgG4関連唾液腺炎$", re.I).sub(u"IgG4関連唾液腺炎", text)
        text = re.compile(u"^IgG4関連胆管炎$", re.I).sub(u"IgG4関連胆管炎", text)
        text = re.compile(u"^IgG4関連尿細管間質性腎炎$", re.I).sub(u"IgG4関連尿細管間質性腎炎", text)
        text = re.compile(u"^IgG4関連肺偽腫瘍、胸膜炎$", re.I).sub(u"IgG4関連肺偽腫瘍、胸膜炎", text)
        text = re.compile(u"^IgG4関連肺疾患$", re.I).sub(u"IgG4関連肺疾患", text)
        text = re.compile(u"^IgG4関連肺病変$", re.I).sub(u"IgG4関連肺病変", text)
        text = re.compile(u"^IgG4関連肥厚性硬膜炎$", re.I).sub(u"IgG4関連肥厚性硬膜炎", text)
        text = re.compile(u"^IgG4関連漏斗下垂体炎$", re.I).sub(u"IgG4関連漏斗下垂体炎", text)
        text = re.compile(u"^IgG4関連膵病変$", re.I).sub(u"IgG4関連膵病変", text)
        text = re.compile(u"^IgG4症候群$", re.I).sub(u"IgG4症候群", text)
        text = re.compile(u"^IgG4陽性形質細胞浸潤$", re.I).sub(u"IgG4陽性形質細胞浸潤", text)
        text = re.compile(u"^IgG-λ型monoclonal_gammopathy_of_undermined_significance$", re.I).sub(u"IgG-λ型の意義不明の単クローン性免疫グロブリン血症", text)
        text = re.compile(u"^IgG-λ型多発性骨髄腫$", re.I).sub(u"IgG-λ型多発性骨髄腫", text)
        text = re.compile(u"^IgM-κ型M蛋白$", re.I).sub(u"IgM-κ型M蛋白", text)
        text = re.compile(u"^IgM_monoclonal_gammopathy_of_undetermined_significance$", re.I).sub(u"IgMの意義不明の単クローン性免疫グロブリン血症", text)
        text = re.compile(u"^IgMパラプロテイン血症を伴うニューロパチー$", re.I).sub(u"IgMパラプロテイン血症を伴うニューロパチー", text)
        text = re.compile(u"^IgM型のM蛋白単クローン血症$", re.I).sub(u"IgM型のM蛋白単クローン血症", text)
        text = re.compile(u"^IgM型多発性骨髄腫$", re.I).sub(u"IgM型多発性骨髄腫", text)
        text = re.compile(u"^KSHV/HHV8-unrelated_Primary_effusion_リンパ腫_like_リンパ腫$", re.I).sub(u"KSHV/HHV8に関連しない原発性滲出性リンパ腫様リンパ腫", text)
        text = re.compile(u"^L-asparaginase副作用$", re.I).sub(u"L-アスパラギナーゼ副作用", text)
        text = re.compile(u"^Light_chain_proximal_tubulopathy$", re.I).sub(u"L鎖近位細尿管症", text)
        text = re.compile(u"^M5b$", re.I).sub(u"M5b", text)
        text = re.compile(u"^Extranodal_marginal_zone_リンパ腫ofMALT_type$", re.I).sub(u"MALT型節外性辺縁帯リンパ腫", text)
        text = re.compile(u"^MDS_overt_leukemia$", re.I).sub(u"MDSから発症した白血病", text)
        text = re.compile(u"^mFOLFOX6療法副作用$", re.I).sub(u"mFOLFOX6療法副作用", text)
        text = re.compile(u"^MonoMAC症候群$", re.I).sub(u"MonoMAC症候群", text)
        text = re.compile(u"^Myeloid_NK_cell_precursor_acute_leukemia$", re.I).sub(u"Myeloid/NK前駆細胞性急性白血病", text)
        text = re.compile(u"^PBC-AIH_overlap_syndrome$", re.I).sub(u"PBC-AIHオーバーラップ症候群", text)
        text = re.compile(u"^pH/低下$", re.I).sub(u"pH/低下", text)
        text = re.compile(u"^Ph陽性ALL$", re.I).sub(u"Ph陽性急性リンパ性白血病", text)
        text = re.compile(u"^Ph+ALL$", re.I).sub(u"Ph陽性急性リンパ性白血病", text)
        text = re.compile(u"^SpO2/低下$", re.I).sub(u"SpO2/低下", text)
        text = re.compile(u"^T-LGL_leukemia$", re.I).sub(u"T-LGL白血病", text)
        text = re.compile(u"^TNF_receptor-associated_periodic_syndrome$", re.I).sub(u"TNF_受容体関連の周期的症候群", text)
        text = re.compile(u"^TRAb陰性バセドウ病$", re.I).sub(u"TRAb陰性バセドウ病", text)
        text = re.compile(u"^T-lymphoblasticリンパ腫$", re.I).sub(u"T-リンパ芽球性リンパ腫", text)
        text = re.compile(u"^VIPoma$", re.I).sub(u"VIP産生腫瘍", text)
        text = re.compile(u"^Arnold-Chiari奇形1型$", re.I).sub(u"アーノルド・キアリ奇形1型", text)
        text = re.compile(u"^Eisenmenger症候群$", re.I).sub(u"アイゼンメンゲル症候群", text)
        text = re.compile(u"^Avellis症候群$", re.I).sub(u"アヴェリス症候群", text)
        text = re.compile(u"^Azacitidine$", re.I).sub(u"アザシチジン", text)
        text = re.compile(u"^Acinetobacter敗血症$", re.I).sub(u"アシネトバクター敗血症", text)
        text = re.compile(u"^Adams-Stokes発作$", re.I).sub(u"アダムス・ストークス発作", text)
        text = re.compile(u"^upside_down_stomach$", re.I).sub(u"アップサイドダウン・ストマック", text)
        text = re.compile(u"^Upshaw-Schulman症候群$", re.I).sub(u"アップショー・シュールマン症候群", text)
        text = re.compile(u"^upfront_combination_therapy$", re.I).sub(u"アップフロントコンビネーション・セラピー", text)
        text = re.compile(u"^Addison病$", re.I).sub(u"アジソン病", text)
        text = re.compile(u"^anastrozole副作用$", re.I).sub(u"アナストロゾール副作用", text)
        text = re.compile(u"^Alagille症候群$", re.I).sub(u"アラジール症候群", text)
        text = re.compile(u"^Salmonella_arizonae菌血症$", re.I).sub(u"アリゾナ菌血症", text)
        text = re.compile(u"^Alcohol_induced_pseudo_Cushing&#039;s_syndrome$", re.I).sub(u"アルコール誘発性偽性クッシング症候群", text)
        text = re.compile(u"^Alstr.m症候群$", re.I).sub(u"アルストレム症候群", text)
        text = re.compile(u"^aldosteronoma$", re.I).sub(u"アルデステロン産生腺腫", text)
        text = re.compile(u"^tPA合併症$", re.I).sub(u"アルテプラーゼ合併症", text)
        text = re.compile(u"^Alport症候群$", re.I).sub(u"アルポート症候群", text)
        text = re.compile(u"^Alport症候群遺伝子異常$", re.I).sub(u"アルポート症候群遺伝子異常", text)
        text = re.compile(u"^Angelman症候群$", re.I).sub(u"アンジェルマン症候群", text)
        text = re.compile(u"^Anthracycline$", re.I).sub(u"アンスラサイクリン", text)
        text = re.compile(u"^amphetamine中毒$", re.I).sub(u"アンフェタミン中毒", text)
        text = re.compile(u"^itraconazole副作用$", re.I).sub(u"イトラコナゾール副作用", text)
        text = re.compile(u"^imatinib併用寛解導入療法副作用$", re.I).sub(u"イマチニブ併用寛解導入療法副作用", text)
        text = re.compile(u"^Immunotactoid_glomerulopathy$", re.I).sub(u"イムノタクトイド糸球体症", text)
        text = re.compile(u"^IFNα+ribavirin併用療法副作用$", re.I).sub(u"インターフェロンα+リバビリン併用療法副作用", text)
        text = re.compile(u"^IFN-α2b副作用・リバビリン副作用$", re.I).sub(u"インターフェロンα2b副作用・リバビリン副作用", text)
        text = re.compile(u"^Valsalva洞破裂$", re.I).sub(u"バルサルバ洞破裂", text)
        text = re.compile(u"^Waldenstr.m&#039;s_macroglobulinemia$", re.I).sub(u"ワルデンストレームマクログロブリン血症", text)
        text = re.compile(u"^Villaret症候群$", re.I).sub(u"ヴィラレ症候群", text)
        text = re.compile(u"^Williams-Campbell_症候群$", re.I).sub(u"ウィリアムズ・キャンベル症候群", text)
        text = re.compile(u"^Williams-Beuren_syndrome$", re.I).sub(u"ウィリアムズ・ビューレン症候群", text)
        text = re.compile(u"^Werner症候群$", re.I).sub(u"ウェルナー症候群", text)
        text = re.compile(u"^Wenckebach型房室ブロック$", re.I).sub(u"ウェンケバッハ型房室ブロック", text)
        text = re.compile(u"^Waterhouse-Fridrichsen症候群$", re.I).sub(u"ウォーターハウス・フリードリヒセン症候群", text)
        text = re.compile(u"^Waterhouse-Friderichsen症候群$", re.I).sub(u"ウォーターハウス・フリードリヒセン症候群", text)
        text = re.compile(u"^Waterhouse-Friderichsen_症候群$", re.I).sub(u"ウォーターハウス・フリードリヒセン症候群", text)
        text = re.compile(u"^Wolfram症候群$", re.I).sub(u"ウォルフラム症候群", text)
        text = re.compile(u"^Ehlers-Danlos症候群$", re.I).sub(u"エーラス・ダンロス症候群", text)
        text = re.compile(u"^escitalopram副作用$", re.I).sub(u"エスシタロプラム副作用", text)
        text = re.compile(u"^Edwardsiella_tarda腸炎$", re.I).sub(u"エドワージエラ・タルダ腸炎", text)
        text = re.compile(u"^Edwardsiella_tarda敗血症$", re.I).sub(u"エドワージエラ・タルダ敗血症", text)
        text = re.compile(u"^Epstein-Barr_Virus感染症$", re.I).sub(u"EBウイルス感染症", text)
        text = re.compile(u"^EBV-associated_T_NK_lymphoproliferative_desease$", re.I).sub(u"EBウイルス関連のT/NKリンパ増殖性疾患", text)
        text = re.compile(u"^Epstein-Barr_Virus脳炎$", re.I).sub(u"EBウイルス脳炎", text)
        text = re.compile(u"^Ebstein奇形$", re.I).sub(u"エブスタイン奇形", text)
        text = re.compile(u"^Emery-Dreifuss型筋ジストロフィー$", re.I).sub(u"エメリ・ドレフュス型筋ジストロフィー", text)
        text = re.compile(u"^Elizabethkingia_meningoseptica感染症$", re.I).sub(u"エリザベトキンギア・メニンゴセプティカ感染症", text)
        text = re.compile(u"^Eltrombopag副作用$", re.I).sub(u"エルトロンボパグ副作用", text)
        text = re.compile(u"^elthrombopag副作用$", re.I).sub(u"エルトロンボパグ副作用", text)
        text = re.compile(u"^electrical_storm$", re.I).sub(u"エレクトリカルストーム", text)
        text = re.compile(u"^Aeromonas_hydrophilia感染症$", re.I).sub(u"エロモナス・ハイドロフィラ感染症", text)
        text = re.compile(u"^Aeromonas腸炎$", re.I).sub(u"エロモナス腸炎", text)
        text = re.compile(u"^Enterococcus_durans菌血症$", re.I).sub(u"エンテロコッカス・デューランス菌血症", text)
        text = re.compile(u"^Enterobacter_aerogenes菌血症$", re.I).sub(u"エンテロバクター・エロゲネス菌血症", text)
        text = re.compile(u"^Empty_Sella$", re.I).sub(u"エンプティ・セラ", text)
        text = re.compile(u"^empty_sella_syndrome$", re.I).sub(u"エンプティ・セラ症候群", text)
        text = re.compile(u"^Empty_sella症候群$", re.I).sub(u"エンプティ・セラ症候群", text)
        text = re.compile(u"^oxaliplatin副作用$", re.I).sub(u"オキサリプラチン副作用", text)
        text = re.compile(u"^Opalski症候群$", re.I).sub(u"オパルスキ症候群", text)
        text = re.compile(u"^from_original$", re.I).sub(u"オリジナルより", text)
        text = re.compile(u"^Ortner症候群$", re.I).sub(u"オルトナー症候群", text)
        text = re.compile(u"^オルメサルタンによるLi排泄障害$", re.I).sub(u"オルメサルタンによるLi排泄障害", text)
        text = re.compile(u"^Carney複合$", re.I).sub(u"カーニー複合", text)
        text = re.compile(u"^Cowden病$", re.I).sub(u"カウデン病", text)
        text = re.compile(u"^Kasabach_meritt症候群$", re.I).sub(u"カサバッハ・メリット症候群", text)
        text = re.compile(u"^Kasabach-Merritt症候群$", re.I).sub(u"カサバッハ・メリット症候群", text)
        text = re.compile(u"^Catheter_Ablation合併症$", re.I).sub(u"カテーテルアブレーション合併症", text)
        text = re.compile(u"^Caplan症候群$", re.I).sub(u"カプラン症候群", text)
        text = re.compile(u"^Garcin症候群$", re.I).sub(u"ガルサン症候群", text)
        text = re.compile(u"^Ca/低下$", re.I).sub(u"カルシウム/低下", text)
        text = re.compile(u"^Calcium-alkali症候群$", re.I).sub(u"カルシウム-アルカリ症候群", text)
        text = re.compile(u"^Ca過剰摂取$", re.I).sub(u"カルシウム過剰摂取", text)
        text = re.compile(u"^Ca製剤副作用$", re.I).sub(u"カルシウム製剤副作用", text)
        text = re.compile(u"^Ca拮抗薬副作用$", re.I).sub(u"カルシウム拮抗薬副作用", text)
        text = re.compile(u"^Calciphylaxis$", re.I).sub(u"カルシフィラキシー", text)
        text = re.compile(u"^Kartagener症候群$", re.I).sub(u"カルタゲナー症候群", text)
        text = re.compile(u"^Kallmann症候群$", re.I).sub(u"カルマン症候群", text)
        text = re.compile(u"^Caroli病$", re.I).sub(u"カロリー病", text)
        text = re.compile(u"^M.kansasii症$", re.I).sub(u"カンサシ症", text)
        text = re.compile(u"^ganciclovir副作用$", re.I).sub(u"ガンシクロビル副作用", text)
        text = re.compile(u"^Candida_ALBicans感染症$", re.I).sub(u"カンジダ・アルビカンス感染症", text)
        text = re.compile(u"^Candida_guilliermondii敗血症$", re.I).sub(u"カンジダ・ギリエルモンジィ敗血症", text)
        text = re.compile(u"^Campylobacter_jejuni感染$", re.I).sub(u"カンピロバクター・ジェジュニ感染", text)
        text = re.compile(u"^Campylobacter_fetus菌血症$", re.I).sub(u"カンピロバクターフィータス菌血症", text)
        text = re.compile(u"^Campylobacter感染症$", re.I).sub(u"カンピロバクター感染症", text)
        text = re.compile(u"^cap_polyposis$", re.I).sub(u"キャップ・ポリープ", text)
        text = re.compile(u"^Capnocytophagacanimorsus感染症$", re.I).sub(u"カプノサイトファーガ・カニモルサス感染症", text)
        text = re.compile(u"^Capnocytophaga_canimorsus敗血症$", re.I).sub(u"キャプノサイトファーガ・カニモルサス敗血症", text)
        text = re.compile(u"^Cameron病変$", re.I).sub(u"キャメロン病変", text)
        text = re.compile(u"^Chilaiditi症候群$", re.I).sub(u"キライジチ症候群", text)
        text = re.compile(u"^Guillan-Barre症候群$", re.I).sub(u"ギラン・バレー症候群", text)
        text = re.compile(u"^Guillain-Barr._syndrome$", re.I).sub(u"ギラン・バレー症候群", text)
        text = re.compile(u"^Guillain-Barr.症候群$", re.I).sub(u"ギラン・バレー症候群", text)
        text = re.compile(u"^Guillain_Barre_Syndrome_Variant$", re.I).sub(u"ギラン・バレー症候群変種", text)
        text = re.compile(u"^Kounis症候群$", re.I).sub(u"クーニス症候群", text)
        text = re.compile(u"^Coombs陰性自己免疫性溶血性貧血$", re.I).sub(u"クームス陰性自己免疫性溶血性貧血", text)
        text = re.compile(u"^Cushing徴候$", re.I).sub(u"クッシング徴候", text)
        text = re.compile(u"^Goodpasture症候群$", re.I).sub(u"グッドパスチャー症候群", text)
        text = re.compile(u"^Goodpasture's_disease$", re.I).sub(u"グッドパスチャー病", text)
        text = re.compile(u"^Good症候群$", re.I).sub(u"グッド症候群", text)
        text = re.compile(u"^crowned_dens_syndrome$", re.I).sub(u"Crowned_dens症候群", text)
        text = re.compile(u"^Chlamydia_pneumoniae感染$", re.I).sub(u"クラジミア肺炎感染", text)
        text = re.compile(u"^Klippel-Weber症候群$", re.I).sub(u"クリッペル・ウェーバー症候群", text)
        text = re.compile(u"^Klippel-Trenaunay-Weber症候群$", re.I).sub(u"クリッペル・トレノーネイ・ウェーバー症候群", text)
        text = re.compile(u"^Klippel-Trenaunay症候群$", re.I).sub(u"クリッペル・トレノーネイ・ウェーバー症候群", text)
        text = re.compile(u"^Klippel_Trenaunay症候群$", re.I).sub(u"クリッペル・トレノーネイ・ウェーバー症候群", text)
        text = re.compile(u"^Klippel-Feil症候群$", re.I).sub(u"クリッペル・フェイユ症候群", text)
        text = re.compile(u"^Klippel-Feil症候群3型$", re.I).sub(u"クリッペル・フェイユ症候群3型", text)
        text = re.compile(u"^Krukenberg腫瘍$", re.I).sub(u"クルーケンベルク腫瘍", text)
        text = re.compile(u"^Graves'病$", re.I).sub(u"グレーブス病", text)
        text = re.compile(u"^Klebsiella_pneumoniaeによる敗血症$", re.I).sub(u"クレブシエラ・ニューモニエによる敗血症", text)
        text = re.compile(u"^Klebsiella感染$", re.I).sub(u"クレブシエラ感染", text)
        text = re.compile(u"^Klebsiella_Pneumonia感染症$", re.I).sub(u"クレブシエラ肺炎桿菌感染症", text)
        text = re.compile(u"^Klebsiella_peumoniae感染症$", re.I).sub(u"クレブシエラ肺炎桿菌感染症", text)
        text = re.compile(u"^Creutzfeldt_Jacob病$", re.I).sub(u"クロイツフェルト・ヤコブ病", text)
        text = re.compile(u"^Crow-Fukase症候群$", re.I).sub(u"クロウ・深瀬症候群", text)
        text = re.compile(u"^Crow-深瀬症候群$", re.I).sub(u"クロウ・深瀬症候群", text)
        text = re.compile(u"^C.difficile関連腸炎$", re.I).sub(u"クロストリジウム・ディフィシル関連腸炎", text)
        text = re.compile(u"^Clostridium_difficilecolitis$", re.I).sub(u"クロストリジウム・ディフィシル腸炎", text)
        text = re.compile(u"^Clostridium_difficile感染$", re.I).sub(u"クロストリジウム・ディフィシレ菌感染", text)
        text = re.compile(u"^Cronkhite-Canada症候群$", re.I).sub(u"クロンカイト・カナダ症候群", text)
        text = re.compile(u"^kwashiorkor型栄養障害$", re.I).sub(u"クワシオルコル型栄養障害", text)
        text = re.compile(u"^Gemcitabine・S1併用療法副作用$", re.I).sub(u"ゲムシタビン・S1併用療法副作用", text)
        text = re.compile(u"^Gerstmann-Str.ussler-Scheinker病$", re.I).sub(u"ゲルストマン・ストロイスラー・シャインカー病", text)
        text = re.compile(u"^Gerstmann症候群$", re.I).sub(u"ゲルストマン症候群", text)
        text = re.compile(u"^Coagulase-negative_staphylococciカテーテル関連血流感染症$", re.I).sub(u"コアグラーゼ陰性ブドウ球菌カテーテル関連血流感染症", text)
        text = re.compile(u"^Cogan症候群$", re.I).sub(u"コーガン症候群", text)
        text = re.compile(u"^Gorlin症候群$", re.I).sub(u"ゴーリン症候群", text)
        text = re.compile(u"^Coxiellaburnetii感染症$", re.I).sub(u"コクシエラバーネッティ感染症", text)
        text = re.compile(u"^Kocuria_kristinae敗血症$", re.I).sub(u"コクリアクリスティナエ敗血症", text)
        text = re.compile(u"^Cockayne症候群$", re.I).sub(u"コケイン症候群", text)
        text = re.compile(u"^gonadotropin単独欠損症$", re.I).sub(u"ゴナドトロピン単独欠損症", text)
        text = re.compile(u"^Kommerell憩室$", re.I).sub(u"コメレル憩室", text)
        text = re.compile(u"^collgenous_colitis$", re.I).sub(u"コラーゲン大腸炎", text)
        text = re.compile(u"^collagenous_colitis$", re.I).sub(u"コラゲナウス・コライティス", text)
        text = re.compile(u"^Cortisol_Binding_Globulin異常症$", re.I).sub(u"コルチゾール結合グロブリン異常症", text)
        text = re.compile(u"^cyclosporin_A$", re.I).sub(u"サイクロスポリンA", text)
        text = re.compile(u"^Cypherステント留置後$", re.I).sub(u"サイファーステント留置後", text)
        text = re.compile(u"^subclinical_クッシング症候群$", re.I).sub(u"サブクリニカルクッシング症候群", text)
        text = re.compile(u"^Salmonella_enteritidis敗血症$", re.I).sub(u"サルモネラエンテリティディス敗血症", text)
        text = re.compile(u"^Zieve症候群$", re.I).sub(u"ジーブ症候群", text)
        text = re.compile(u"^Zieve's_syndrome$", re.I).sub(u"ジーブ症候群", text)
        text = re.compile(u"^Zieve_Syndrome$", re.I).sub(u"ジーブ症候群", text)
        text = re.compile(u"^Sj.gren症候群$", re.I).sub(u"シェーグレン症候群", text)
        text = re.compile(u"^Sjoegren症候群$", re.I).sub(u"シェーグレン症候群", text)
        text = re.compile(u"^Schonlein-Henoch紫斑病$", re.I).sub(u"シェーンライン・ヘノッホ紫斑病", text)
        text = re.compile(u"^Sch.nlein-Henoch紫斑病$", re.I).sub(u"シェーンライン・ヘノッホ紫斑病", text)
        text = re.compile(u"^Sister_MaryJoseph&#039;snodule$", re.I).sub(u"シスター・メアリー・ジョセフの小結節", text)
        text = re.compile(u"^Sister_Mary_Joseph結節$", re.I).sub(u"シスター・メアリー・ジョセフ結節", text)
        text = re.compile(u"^sick_day$", re.I).sub(u"シックデイ", text)
        text = re.compile(u"^Scimitar症候群$", re.I).sub(u"シミター症候群", text)
        text = re.compile(u"^imeprevir併用PEG-IFN・Ribavirin療法$", re.I).sub(u"シメプレビル併用ペグインターフェロン・リバビリン療法", text)
        text = re.compile(u"^Shy-Drager症候群$", re.I).sub(u"シャイ・ドレーガー症候群", text)
        text = re.compile(u"^shaggy_aorta症候群$", re.I).sub(u"シャギー大動脈症候群", text)
        text = re.compile(u"^Schmidt症候群$", re.I).sub(u"シュミット症候群", text)
        text = re.compile(u"^Schloffer腫瘍$", re.I).sub(u"シュロッフェル腫瘍", text)
        text = re.compile(u"^Schwannoma$", re.I).sub(u"シュワン腫", text)
        text = re.compile(u"^Gilbert症候群$", re.I).sub(u"ジルベール症候群", text)
        text = re.compile(u"^Sweet病$", re.I).sub(u"スウィート病", text)
        text = re.compile(u"^Stewart-Treves症候群$", re.I).sub(u"スチュアート・トレーヴス症候群", text)
        text = re.compile(u"^Still病$", re.I).sub(u"スティル病", text)
        text = re.compile(u"^Steven_Johnson_syndrome$", re.I).sub(u"スティーブンス・ジョンソン症候群", text)
        text = re.compile(u"^Stevens-Johnson症候群$", re.I).sub(u"スティーブンス・ジョンソン症候群", text)
        text = re.compile(u"^stiff-man症候群$", re.I).sub(u"スティッフパーソン症候群", text)
        text = re.compile(u"^Stage_I_EA$", re.I).sub(u"ステージ1早期抗原", text)
        text = re.compile(u"^stress_cardiomyopathy$", re.I).sub(u"ストレス心筋症", text)
        text = re.compile(u"^S.intermedius感染症$", re.I).sub(u"ストレプトコッカス・インターメディウス感染症", text)
        text = re.compile(u"^Str.gallolyticus_ssp_pasteurianas敗血症$", re.I).sub(u"ストレプトコッカス・ガロリティカス亜種パスツリア敗血症", text)
        text = re.compile(u"^Streptococcus_dysgalactiae_subsp._equisimilis菌血症$", re.I).sub(u"ストレプトコッカス・ディスガラクティエ亜種エクイシミリス菌血症", text)
        text = re.compile(u"^Streptococcus_bovis感染$", re.I).sub(u"ストレプトコッカス・ボビス感染", text)
        text = re.compile(u"^Streptococcus_mitis敗血症$", re.I).sub(u"ストレプトコッカス・ミチス敗血症", text)
        text = re.compile(u"^sunitinib$", re.I).sub(u"スニチニブ", text)
        text = re.compile(u"^Sneddon症候群$", re.I).sub(u"スネドン症候群", text)
        text = re.compile(u"^Spur_cell_anemia$", re.I).sub(u"スプールセル貧血", text)
        text = re.compile(u"^Swyer-James症候群$", re.I).sub(u"スワイヤー・ジェームス症候群", text)
        text = re.compile(u"^therapy-relatedMDS$", re.I).sub(u"治療関連骨髄異形成症候群", text)
        text = re.compile(u"^Celecoxib$", re.I).sub(u"セレコキシブ", text)
        text = re.compile(u"^seroconversion$", re.I).sub(u"セロコンバージョン", text)
        text = re.compile(u"^Other_iatrogenic_Immunodeficiency-associated_lymphoproliferative_disorders$", re.I).sub(u"その他医発性免疫不全関連のリンパ増殖性疾患", text)
        text = re.compile(u"^Zollinger-Ellison症候群$", re.I).sub(u"ゾリンジャー・エリソン症候群", text)
        text = re.compile(u"^Turner症候群$", re.I).sub(u"ターナー症候群", text)
        text = re.compile(u"^Dasatinib内服$", re.I).sub(u"ダサチニブ内服", text)
        text = re.compile(u"^double_gap_acidosis$", re.I).sub(u"ダブルギャップ・アシドーシス", text)
        text = re.compile(u"^double_hit_リンパ腫$", re.I).sub(u"ダブルヒットリンパ腫", text)
        text = re.compile(u"^Anabolic_Steroid副作用$", re.I).sub(u"タンパク質同化ステロイド副作用", text)
        text = re.compile(u"^Tigecycline副作用$", re.I).sub(u"チゲサイクリン副作用", text)
        text = re.compile(u"^Churg_Strauss症候群$", re.I).sub(u"チャーグ・ストラウス症候群", text)
        text = re.compile(u"^Churg-strauss_症候群$", re.I).sub(u"チャーグ・ストラウス症候群", text)
        text = re.compile(u"^Child-Pugh分類C$", re.I).sub(u"チャイルド・ピュー分類C", text)
        text = re.compile(u"^Zenker憩室$", re.I).sub(u"ツェンカー憩室", text)
        text = re.compile(u"^DiGeorge症候群$", re.I).sub(u"ディジョージ症候群", text)
        text = re.compile(u"^de_novo_B型肝炎$", re.I).sub(u"デノボB型肝炎", text)
        text = re.compile(u"^de_novoB型肝炎$", re.I).sub(u"デノボB型肝炎", text)
        text = re.compile(u"^denovoB型急性肝炎$", re.I).sub(u"デノボB型急性肝炎", text)
        text = re.compile(u"^de_novo肝炎$", re.I).sub(u"デノボ肝炎", text)
        text = re.compile(u"^Dieulafoy潰瘍$", re.I).sub(u"デュラフォイ潰瘍", text)
        text = re.compile(u"^Dieulafoy潰瘍@小腸$", re.I).sub(u"デュラフォイ潰瘍@小腸", text)
        text = re.compile(u"^telmisartan副作用$", re.I).sub(u"テルミサルタン作用", text)
        text = re.compile(u"^Doege-Potter症候群$", re.I).sub(u"ドージ・ポッター症候群", text)
        text = re.compile(u"^Trichosporon_asahii菌血症$", re.I).sub(u"トリコスポロンアサヒ菌血症", text)
        text = re.compile(u"^trisomy_8陽性非MDS$", re.I).sub(u"トリソミー8陽性非骨髄異形成症候群", text)
        text = re.compile(u"^triple-hit_リンパ腫$", re.I).sub(u"トリプルヒットリンパ腫", text)
        text = re.compile(u"^TripleHitリンパ腫$", re.I).sub(u"トリプルヒットリンパ腫", text)
        text = re.compile(u"^Torsades_de_pointes$", re.I).sub(u"トルサード・ド・ポワント", text)
        text = re.compile(u"^Torsade_de_pointes$", re.I).sub(u"トルサード・ド・ポワント", text)
        text = re.compile(u"^Dressler症候群$", re.I).sub(u"ドレスラー症候群", text)
        text = re.compile(u"^Tolosa-Hunt症候群$", re.I).sub(u"トロサ・ハント症候群", text)
        text = re.compile(u"^Nutcracker現象$", re.I).sub(u"ナットクラッカー現象", text)
        text = re.compile(u"^Nutcracker症候群$", re.I).sub(u"ナットクラッカー症候群", text)
        text = re.compile(u"^Na/低下$", re.I).sub(u"ナトリウム/低下", text)
        text = re.compile(u"^Na喪失性腎症$", re.I).sub(u"ナトリウム喪失性腎症", text)
        text = re.compile(u"^Pneumocystis_jirovecii感染$", re.I).sub(u"ニューモシスチス・ジロベシ感染", text)
        text = re.compile(u"^Pneumocystis_jiroveci肺炎$", re.I).sub(u"ニューモシスチス・ジロベシ肺炎", text)
        text = re.compile(u"^Nilotinib$", re.I).sub(u"ニロチニブ", text)
        text = re.compile(u"^nilotinib副作用$", re.I).sub(u"ニロチニブ副作用", text)
        text = re.compile(u"^Noonan症候群$", re.I).sub(u"ヌーナン症候群", text)
        text = re.compile(u"^Nocardia_asteroides感染$", re.I).sub(u"ノカルジア・アステロイデス感染", text)
        text = re.compile(u"^Nocardia_farcinica脳膿瘍$", re.I).sub(u"ノカルジア・ファルシニカ脳膿瘍", text)
        text = re.compile(u"^Burkitt_リンパ腫$", re.I).sub(u"バーキットリンパ腫", text)
        text = re.compile(u"^Burkittリンパ腫$", re.I).sub(u"バーキットリンパ腫", text)
        text = re.compile(u"^Parkin遺伝子変異$", re.I).sub(u"パーキン遺伝子変異", text)
        text = re.compile(u"^Bartter症候群$", re.I).sub(u"バーター症候群", text)
        text = re.compile(u"^Birt-Hogg-Dub.症候群$", re.I).sub(u"バート・ホッグ・デューベ症候群", text)
        text = re.compile(u"^Vernet症候群$", re.I).sub(u"バーネット症候群", text)
        text = re.compile(u"^Heyde症候群$", re.I).sub(u"ハイド症候群", text)
        text = re.compile(u"^Bacteroides_fragilis感染症$", re.I).sub(u"バクテロイデスフラジリス感染症", text)
        text = re.compile(u"^Bazin硬結性紅斑$", re.I).sub(u"バザン性紅斑", text)
        text = re.compile(u"^Paget_Schroetter_syndrome$", re.I).sub(u"パジェット・シュレッター症候群", text)
        text = re.compile(u"^Paget-Schroetter症候群$", re.I).sub(u"パジェット・シュレッター症候群", text)
        text = re.compile(u"^Pasteurella_Multocida髄膜炎$", re.I).sub(u"パスツレラ・ムルトシダ髄膜炎", text)
        text = re.compile(u"^Pasteurella_multocida感染症$", re.I).sub(u"パスツレラムルトシダ感染症", text)
        text = re.compile(u"^pasteurella肺炎$", re.I).sub(u"パスツレラ肺炎", text)
        text = re.compile(u"^Basex症候群$", re.I).sub(u"バセックス症候群", text)
        text = re.compile(u"^Basedow眼症$", re.I).sub(u"バセドー眼症", text)
        text = re.compile(u"^Basedow氏病$", re.I).sub(u"バセドー氏病", text)
        text = re.compile(u"^Hamman症候群$", re.I).sub(u"ハマン症候群", text)
        text = re.compile(u"^Balint症候群$", re.I).sub(u"バリント症候群", text)
        text = re.compile(u"^Bardet-Biedl症候群$", re.I).sub(u"バルデー・ビードル症候群", text)
        text = re.compile(u"^parvovirus_B19感染症$", re.I).sub(u"パルボウィルスB19感染症", text)
        text = re.compile(u"^Paroxetine副作用$", re.I).sub(u"パロキセチン副作用", text)
        text = re.compile(u"^Pancoast症候群$", re.I).sub(u"パンコースト症候群", text)
        text = re.compile(u"^Hunter症候群$", re.I).sub(u"ハンター症候群", text)
        text = re.compile(u"^Hunter舌炎$", re.I).sub(u"ハンター舌炎", text)
        text = re.compile(u"^van_der_Hoeve症候群$", re.I).sub(u"バンデルヘーベ症候群", text)
        text = re.compile(u"^Piehler変法術後$", re.I).sub(u"ピーラー変法術後", text)
        text = re.compile(u"^Pisa症候群$", re.I).sub(u"ピサ症候群", text)
        text = re.compile(u"^VitB12欠乏$", re.I).sub(u"ビタミンB12欠乏", text)
        text = re.compile(u"^Vit.B1欠乏$", re.I).sub(u"ビタミンB1欠乏", text)
        text = re.compile(u"^Vit.D産生$", re.I).sub(u"ビタミンD産生", text)
        text = re.compile(u"^VitD製剤副作用$", re.I).sub(u"ビタミンD製剤副作用", text)
        text = re.compile(u"^Pickwick症候群$", re.I).sub(u"ピックウィック症候群", text)
        text = re.compile(u"^hCG産生絨毛癌$", re.I).sub(u"ヒト柔毛膜性ゴナドトロピン産生絨毛癌", text)
        text = re.compile(u"^hANP$", re.I).sub(u"ヒト心房性ナトリウム利尿ペプチド", text)
        text = re.compile(u"^hANP副作用$", re.I).sub(u"ヒト心房性ナトリウム利尿ペプチド副作用", text)
        text = re.compile(u"^Vibrio_vulnificus感染$", re.I).sub(u"ビブリオ・バルニフィカス感染", text)
        text = re.compile(u"^Vibrio_vulnificus感染症$", re.I).sub(u"ビブリオ・バルニフィカス感染症", text)
        text = re.compile(u"^Vibrio_vulnificus敗血症$", re.I).sub(u"ビブリオ・バルニフィカス敗血症", text)
        text = re.compile(u"^Piperacillin_Tazobactam副作用$", re.I).sub(u"ピペラシリン・タゾバクタム副作用", text)
        text = re.compile(u"^Diffuse_Large_BCellリンパ腫$", re.I).sub(u"びまん性大細胞型B細胞リンパ腫", text)
        text = re.compile(u"^diffuse_large_B_cell_リンパ腫$", re.I).sub(u"びまん性大細胞型B細胞リンパ腫", text)
        text = re.compile(u"^diffuselargeBcell_リンパ腫$", re.I).sub(u"びまん性大細胞型B細胞性リンパ腫", text)
        text = re.compile(u"^H.pylori除菌$", re.I).sub(u"ピロリ菌除菌", text)
        text = re.compile(u"^Bing-Neel症候群$", re.I).sub(u"ビング・ニール症候群", text)
        text = re.compile(u"^Fahr病$", re.I).sub(u"ファール病", text)
        text = re.compile(u"^Fallot四徴症$", re.I).sub(u"ファロー四徴症", text)
        text = re.compile(u"^Fanconi_症候群$", re.I).sub(u"ファンコニー症候群", text)
        text = re.compile(u"^Fitz-Hugh-Curtis$", re.I).sub(u"フィッツ・ヒュー・カーティス症候群", text)
        text = re.compile(u"^Fitz-Hugh-Curtis_syndrome$", re.I).sub(u"フィッツ・ヒュー・カーティス症候群", text)
        text = re.compile(u"^Fits_Hugh_Curtis症候群$", re.I).sub(u"フィッツ・ヒュー・カーティス症候群", text)
        text = re.compile(u"^Felty症候群$", re.I).sub(u"フェルティ症候群", text)
        text = re.compile(u"^focus不明の大腸菌感染症$", re.I).sub(u"フォーカス不明の大腸菌感染症", text)
        text = re.compile(u"^Vogt-小柳-原田病$", re.I).sub(u"フォークト・小柳・原田病", text)
        text = re.compile(u"^von_Willebrand病$", re.I).sub(u"フォン・ウィルブランド病", text)
        text = re.compile(u"^von_Hippel_Lindau病$", re.I).sub(u"フォンヒッペル・リンダウ病", text)
        text = re.compile(u"^von_Recklinghausen_neurofibromatosis$", re.I).sub(u"フォンレックリングハウゼン神経線維腫", text)
        text = re.compile(u"^von_Recklinghausen病$", re.I).sub(u"フォンレックリンクハウゼン病", text)
        text = re.compile(u"^vRD合併GIST$", re.I).sub(u"フォンレックリンクハウゼン病合併消化管間質腫瘍", text)
        text = re.compile(u"^Fusobacterium_varium感染$", re.I).sub(u"フソバクテリウムバリウム感染", text)
        text = re.compile(u"^Brown-S.quard症候群$", re.I).sub(u"ブラウン・セカール症候群", text)
        text = re.compile(u"^Brown-Sequard症候群$", re.I).sub(u"ブラウン・セカール症候群", text)
        text = re.compile(u"^plus_minus_lid症候群$", re.I).sub(u"プラスマイナスリッド症候群", text)
        text = re.compile(u"^Prada-Willi症候群$", re.I).sub(u"プラダ—・ウィリ症候群", text)
        text = re.compile(u"^Prader-Wiili症候群$", re.I).sub(u"プラダ—・ウィリ症候群", text)
        text = re.compile(u"^Platypnea_orthodeoxia_syndrome$", re.I).sub(u"プラネプチア・オルソデオキシア症候群", text)
        text = re.compile(u"^Pralidoxime使用後$", re.I).sub(u"プラリドキシム使用後", text)
        text = re.compile(u"^Plummer_Vinson症候群$", re.I).sub(u"プランマー・ビンソン症候群", text)
        text = re.compile(u"^Plummer病$", re.I).sub(u"プランマ—病", text)
        text = re.compile(u"^Brittle型1型糖尿病合併妊娠$", re.I).sub(u"ブリットル1型糖尿病合併妊娠", text)
        text = re.compile(u"^Brugada型心電図$", re.I).sub(u"ブルガダ型心電図", text)
        text = re.compile(u"^Brugada症候群$", re.I).sub(u"ブルガダ症候群", text)
        text = re.compile(u"^Brugada症候群様症状$", re.I).sub(u"ブルガダ症候群様症状", text)
        text = re.compile(u"^Prevotella_Melaninogenica菌血症$", re.I).sub(u"プレボテラ・メラニノジェニカ菌血症", text)
        text = re.compile(u"^proteinS欠乏症$", re.I).sub(u"プロテインS欠乏症", text)
        text = re.compile(u"^プロテインS欠乏症Type1$", re.I).sub(u"プロテインS欠乏症1型", text)
        text = re.compile(u"^Heerfordt症候群$", re.I).sub(u"ヘールフォルト症候群", text)
        text = re.compile(u"^PegIFN・RBV療法$", re.I).sub(u"ペグインターフェロン・RBV療法", text)
        text = re.compile(u"^Peg-IFNα-2a$", re.I).sub(u"ペグインターフェロンα-2a", text)
        text = re.compile(u"^PEG-interferonα-2a副作用$", re.I).sub(u"ペグインターフェロンα-2a副作用", text)
        text = re.compile(u"^PEG-IFNα-2a副作用$", re.I).sub(u"ペグインターフェロンα-2a副作用", text)
        text = re.compile(u"^PEG-IFNα2b+リバビリン$", re.I).sub(u"ペグインターフェロンα2b+リバビリン", text)
        text = re.compile(u"^peginterferonα-2b+ribavirin副作用$", re.I).sub(u"ペグインターフェロンα-2b+リバビリン副作用", text)
        text = re.compile(u"^ベタメタゾン/d-マレイン酸クロルフェニラミン配合錠副作用$", re.I).sub(u"ベタメタゾン/d-マレイン酸クロルフェニラミン配合錠副作用", text)
        text = re.compile(u"^Becker型筋ジストロフィー$", re.I).sub(u"ベッカー型筋ジストロフィー", text)
        text = re.compile(u"^Henoch-Schoenlein紫斑病$", re.I).sub(u"ヘノッホ・シェーンライン紫斑病", text)
        text = re.compile(u"^Henoch-Sch.nlein紫斑病$", re.I).sub(u"ヘノッホ・シェーンライン紫斑病", text)
        text = re.compile(u"^Henoch-Sch.enlein紫斑病$", re.I).sub(u"ヘノッホ・シェーンライン紫斑病", text)
        text = re.compile(u"^Henoch-Sch.enlein_Purpura$", re.I).sub(u"ヘノッホ・シェーンライン紫斑病", text)
        text = re.compile(u"^ヘパリン-induced_thrombocytopenia$", re.I).sub(u"ヘパリン誘発性血小板減少症", text)
        text = re.compile(u"^HbA1c/上昇$", re.I).sub(u"ヘモグロビンA1c /上昇", text)
        text = re.compile(u"^HbA1c偽高値$", re.I).sub(u"ヘモグロビンA1c偽高値", text)
        text = re.compile(u"^Hemosuccus_Pancreaticus$", re.I).sub(u"ヘモサッカス膵炎による大小十二指腸乳頭からの出血", text)
        text = re.compile(u"^Helicobacter.cinaedi感染症$", re.I).sub(u"ヘリコバクター・シネディ感染症", text)
        text = re.compile(u"^Helicobacter_cinaedi感染症$", re.I).sub(u"ヘリコバクター・シネディ感染症", text)
        text = re.compile(u"^H.cinaedi菌血症$", re.I).sub(u"ヘリコバクター・シネディ菌血症", text)
        text = re.compile(u"^Helicobacter_cinaedi敗血症$", re.I).sub(u"ヘリコバクター・シネディ敗血症", text)
        text = re.compile(u"^H.cinaedi敗血症$", re.I).sub(u"ヘリコバクター・シネディ敗血症", text)
        text = re.compile(u"^Helicobacter_Pyroli胃炎$", re.I).sub(u"ヘリコバクター・ピロリ胃炎", text)
        text = re.compile(u"^Hermansky-Pudlak症候群$", re.I).sub(u"ヘルマンスキー・パドラック症候群", text)
        text = re.compile(u"^Hermansky_Pudlak_Syndrome$", re.I).sub(u"ヘルマンスキー・パドラック症候群", text)
        text = re.compile(u"^Bell麻痺$", re.I).sub(u"ベル麻痺", text)
        text = re.compile(u"^Bornholm_disease$", re.I).sub(u"ボーンホルム病", text)
        text = re.compile(u"^post_staphylococcal_infection_Henoch-_Sch.nlein紫斑病$", re.I).sub(u"ポストブドウ球菌感染症 ヘノッホ・シェーンライン紫斑病", text)
        text = re.compile(u"^phosphoglyceratekinase欠損症$", re.I).sub(u"ホスホグリセレートキナーゼ欠損症", text)
        text = re.compile(u"^Horner徴候$", re.I).sub(u"ホルネル徴候", text)
        text = re.compile(u"^Madelung病$", re.I).sub(u"マーデルング病", text)
        text = re.compile(u"^Mycobacterium_peregrinum感染$", re.I).sub(u"マイコバクテリウム・ペレグリヌム感染", text)
        text = re.compile(u"^Mycobacterium_avium感染症$", re.I).sub(u"マイコバクテリウムアビウム感染症", text)
        text = re.compile(u"^Mycobacterium_avium胸膜炎$", re.I).sub(u"マイコバクテリウムアビウム胸膜炎", text)
        text = re.compile(u"^Mycobacterium_fortuitum皮膚感染症$", re.I).sub(u"マイコバクテリウム‐フォーチュイタム皮膚感染症", text)
        text = re.compile(u"^マクロCK_type_1$", re.I).sub(u"マクロCK1型", text)
        text = re.compile(u"^McCune-ALBright症候群$", re.I).sub(u"マッキューン・オルブライト症候群", text)
        text = re.compile(u"^Muckle-Wells症候群$", re.I).sub(u"マックル・ウェルズ症候群", text)
        text = re.compile(u"^Malassezia_furfur菌血症$", re.I).sub(u"マラセチア・ファーファー菌血症", text)
        text = re.compile(u"^Marie-Bamberger症候群$", re.I).sub(u"マリー・バンベルガー症候群", text)
        text = re.compile(u"^Marine-Lenhart症候群$", re.I).sub(u"マリン・レンハート症候群", text)
        text = re.compile(u"^marchiafava-bignami症候群$", re.I).sub(u"マルキアファーヴァ・ビニャミi症候群", text)
        text = re.compile(u"^Marfan症候群$", re.I).sub(u"マルファン症候群", text)
        text = re.compile(u"^Mallory-Weiss症候群$", re.I).sub(u"マロリー・ワイス症候群", text)
        text = re.compile(u"^Myoadenylate_deaminase欠損症$", re.I).sub(u"ミオアデニル酸デアミナーゼ欠損症", text)
        text = re.compile(u"^myohemoglobinuria$", re.I).sub(u"ミオヘモグロビン血症", text)
        text = re.compile(u"^Mikulicz病$", re.I).sub(u"ミクリッツ病", text)
        text = re.compile(u"^Miller_フィッシャー症候群$", re.I).sub(u"ミラー・フィッシャー症候群", text)
        text = re.compile(u"^Miller-フィッシャー症候群$", re.I).sub(u"ミラー・フィッシャー症候群", text)
        text = re.compile(u"^May-Thurner症候群$", re.I).sub(u"メイ・ターナー症候群", text)
        text = re.compile(u"^Meigs症候群$", re.I).sub(u"メイグス症候群", text)
        text = re.compile(u"^methicillin-resistant_Staphylococcus_aureus肝膿瘍$", re.I).sub(u"メシチリン耐性黄色ブドウ球菌肝膿瘍", text)
        text = re.compile(u"^Metabolic_Syndrome$", re.I).sub(u"メタボリック症候群", text)
        text = re.compile(u"^Methicillin-resistant_Staphylococcus_epidermidis菌血症$", re.I).sub(u"メチシリン耐性表皮ブドウ球菌", text)
        text = re.compile(u"^Meckel憩室炎$", re.I).sub(u"メッケル憩室炎", text)
        text = re.compile(u"^Methotrexate関連リンパ増殖性疾患$", re.I).sub(u"メトトレキサート関連リンパ増殖性疾患", text)
        text = re.compile(u"^Mogamulizuma副作用$", re.I).sub(u"モガムリズマ副作用", text)
        text = re.compile(u"^Mounier_Kuhn症候群$", re.I).sub(u"モニエール・クーン症候群", text)
        text = re.compile(u"^Mollaret髄膜炎$", re.I).sub(u"モラレ髄膜炎", text)
        text = re.compile(u"^Jarisch-Herxheimer反応$", re.I).sub(u"ヤーリッシュ・ヘルクスハイマー反応", text)
        text = re.compile(u"^Reye症候群$", re.I).sub(u"ライ症候群", text)
        text = re.compile(u"^Ladd靭帯形成$", re.I).sub(u"ラッド靭帯形成", text)
        text = re.compile(u"^Ramsey_Hunt症候群$", re.I).sub(u"ラムゼー・ハント症候群", text)
        text = re.compile(u"^Ramsay_Hunt症候群$", re.I).sub(u"ラムゼー・ハント症候群", text)
        text = re.compile(u"^Laron症候群$", re.I).sub(u"ラロン症候群", text)
        text = re.compile(u"^Lansoprazole・NSAIDs副作用$", re.I).sub(u"ランソプラゾール・非ステロイド性抗炎症薬副作用", text)
        text = re.compile(u"^Rendu-Osler-Weber病$", re.I).sub(u"ランデュ・オスラー・ウェーバー病", text)
        text = re.compile(u"^Lambert-Eaton筋無力症候群$", re.I).sub(u"ランバート・イートン筋無力症候群", text)
        text = re.compile(u"^Lambert-Eaton筋無力症症候群$", re.I).sub(u"ランバート・イートン筋無力症候群", text)
        text = re.compile(u"^Lambert-Eaton症候群$", re.I).sub(u"ランバート・イートン筋無力症候群", text)
        text = re.compile(u"^Li-Fraumeni症候群$", re.I).sub(u"リー・フラウメニ症候群", text)
        text = re.compile(u"^rheumatoid_血管炎$", re.I).sub(u"リウマチ性血管炎", text)
        text = re.compile(u"^Liddle症候群$", re.I).sub(u"リドル症候群", text)
        text = re.compile(u"^Richter症候群$", re.I).sub(u"リヒター症候群", text)
        text = re.compile(u"^Libman-Sacks心内膜炎$", re.I).sub(u"リブマン・サックス心内膜炎", text)
        text = re.compile(u"^lipodystrophy$", re.I).sub(u"リポジストロフィー", text)
        text = re.compile(u"^Lynch症候群$", re.I).sub(u"リンチ症候群", text)
        text = re.compile(u"^Lymphoplasmacytic_リンパ腫$", re.I).sub(u"リンパ形質細胞性リンパ腫", text)
        text = re.compile(u"^リンパ腫tosis_cerebri$", re.I).sub(u"大脳リンパ腫瘍", text)
        text = re.compile(u"^リンパ腫toid_granulomatosis$", re.I).sub(u"リンパ腫様肉芽腫症", text)
        text = re.compile(u"^Roux-en-Y再建後総胆管結石症$", re.I).sub(u"ルー・ワイ再建後総胆管結石症", text)
        text = re.compile(u"^Lupus_cardiomyopathy$", re.I).sub(u"ループス心筋症", text)
        text = re.compile(u"^Leriche症候群$", re.I).sub(u"ルリッシュ症候群", text)
        text = re.compile(u"^Raeder症候群$", re.I).sub(u"レーダー症候群", text)
        text = re.compile(u"^L.fgren症候群$", re.I).sub(u"ロフグレン症候群", text)
        text = re.compile(u"^L.ffler症候群$", re.I).sub(u"レフラー症候群", text)
        text = re.compile(u"^L.ffler心内膜心筋炎$", re.I).sub(u"レフレル心内膜心筋炎", text)
        text = re.compile(u"^Lemirre症候群$", re.I).sub(u"レミエール症候群", text)
        text = re.compile(u"^Streptococcal_毒素性ショック症候群$", re.I).sub(u"レンサ球菌毒素性ショック症候群", text)
        text = re.compile(u"^Lemmel症候群$", re.I).sub(u"レンメル症候群", text)
        text = re.compile(u"^Rowell's症候群$", re.I).sub(u"ロウェル症候群", text)
        text = re.compile(u"^Rosai-Dorfman病様病変$", re.I).sub(u"ロザイ・ドルフマン病様病変", text)
        text = re.compile(u"^Rothia_mucilaginosa肺炎$", re.I).sub(u"ロシアムチラギノーザ肺炎", text)
        text = re.compile(u"^Lofgren症候群$", re.I).sub(u"ロフグレン症候群", text)
        text = re.compile(u"^Weil病$", re.I).sub(u"ワイル病", text)
        text = re.compile(u"^Waldenstr.m_macroglobulin血症$", re.I).sub(u"ワルデンストレームマクログロブリン血症", text)
        text = re.compile(u"^Waldenstrom_macrogulobulinemia$", re.I).sub(u"ワルデンストレームマクログロブリン血症", text)
        text = re.compile(u"^Wallenberg症候群$", re.I).sub(u"ワレンベルグ症候群", text)
        text = re.compile(u"^subclinical_クッシング病$", re.I).sub(u"サブクリニカルクッシング病", text)
        text = re.compile(u"^Malignant_T細胞リンパ腫$", re.I).sub(u"悪性T細胞リンパ腫", text)
        text = re.compile(u"^Malignantリンパ腫$", re.I).sub(u"悪性リンパ腫", text)
        text = re.compile(u"^悪性腫瘍による高Ca血症$", re.I).sub(u"悪性腫瘍に伴う高カルシウム血症", text)
        text = re.compile(u"^humoral_hypercalcemia_of悪性腫瘍$", re.I).sub(u"悪性腫瘍に伴う高カルシウム血症", text)
        text = re.compile(u"^humoral_hypercalcemia_of_悪性腫瘍$", re.I).sub(u"悪性腫瘍に伴う高カルシウム血症", text)
        text = re.compile(u"^Remitting_Seronegative_Symmetrical_Synovitis_with_Pitting_Edema$", re.I).sub(u"圧痕性浮腫を伴う血清反応陰性の寛解性対称性滑膜炎", text)
        text = re.compile(u"^biclonal_gammopathy_of_undetermined_significance$", re.I).sub(u"意義不明の2クローン性高ガンマグロブリン血症", text)
        text = re.compile(u"^Monoclonal_gammopathy_of_undeterminedsignificance$", re.I).sub(u"意義不明の単クローン性高ガンマグロブリン血症", text)
        text = re.compile(u"^Ectpoic_ACTH症候群$", re.I).sub(u"異所性ACTH症候群", text)
        text = re.compile(u"^移植後再発IgA腎症$", re.I).sub(u"移植後再発IgA腎症", text)
        text = re.compile(u"^migratingcranialneuropathy$", re.I).sub(u"移動性脳神経障害", text)
        text = re.compile(u"^胃PEComa$", re.I).sub(u"胃の血管周囲類上皮細胞腫瘍", text)
        text = re.compile(u"^胃体部癌cT4aN3M1_Stage_IV$", re.I).sub(u"胃体部癌cT4aN3M1ステージ4", text)
        text = re.compile(u"^Transientaplastic_crisis$", re.I).sub(u"一過性骨髄無形成クリーゼ", text)
        text = re.compile(u"^HaNDL$", re.I).sub(u"一過性頭痛および脳脊髄液リンパ球増加症による神経学的障害", text)
        text = re.compile(u"^acute_ophthalmoparesis_without_ataxia$", re.I).sub(u"運動失調を伴わない急性眼麻痺", text)
        text = re.compile(u"^Cast_Nephropathy$", re.I).sub(u"円柱形成性尿細管障害", text)
        text = re.compile(u"^inflammatory_myoglandular_polyp$", re.I).sub(u"炎症性筋線維性ポリープ", text)
        text = re.compile(u"^yellow_nail症候群$", re.I).sub(u"黄色爪症候群", text)
        text = re.compile(u"^Yellow_nail_syndrome$", re.I).sub(u"黄色爪症候群", text)
        text = re.compile(u"^下垂体empty_sella$", re.I).sub(u"下垂体エンプティ・セラ", text)
        text = re.compile(u"^下垂体gonadotropinoma内転移$", re.I).sub(u"下垂体ゴナドトロピン内転移", text)
        text = re.compile(u"^Streptococcus_pyogenes感染$", re.I).sub(u"化膿性連鎖球菌感染", text)
        text = re.compile(u"^Age-relatedEBV-associated_B_cell_lymphoproliferative_disorder$", re.I).sub(u"加齢変化性EBV関連B型細胞リンパ増殖性疾患", text)
        text = re.compile(u"^reversible_posterior_leukoencepalopathy_syndrome$", re.I).sub(u"可逆性後白質脳症", text)
        text = re.compile(u"^brainstem_variant_of_可逆性後部白質脳症症候群$", re.I).sub(u"可逆性後部白質脳症の脳幹変種", text)
        text = re.compile(u"^reversible_cerebral_vasoconstriction_syndrome$", re.I).sub(u"可逆性脳血管攣縮症候群", text)
        text = re.compile(u"^Posterior_Reversible_Encephalopathy_Syndroe$", re.I).sub(u"可逆性白質脳症", text)
        text = re.compile(u"^posterior_reversible_encephalopathy_syndrome$", re.I).sub(u"可逆性白質脳症", text)
        text = re.compile(u"^Posteriorreversibleencephalopathy_syndrome$", re.I).sub(u"可逆性白質脳症", text)
        text = re.compile(u"^家族性高Lp血症$", re.I).sub(u"家族性高Lp血症", text)
        text = re.compile(u"^Hypersensitivity_Syndrome$", re.I).sub(u"過敏症症候群", text)
        text = re.compile(u"^Blastic_NK-cell_リンパ腫$", re.I).sub(u"芽球性NK細胞リンパ腫", text)
        text = re.compile(u"^blastic_NK-cell_リンパ腫_leukemia$", re.I).sub(u"芽球性NK細胞リンパ腫白血病", text)
        text = re.compile(u"^blasticNKcell_leukemia・リンパ腫$", re.I).sub(u"芽球性NK細胞性白血病・リンパ腫", text)
        text = re.compile(u"^Blastic_Plasmacytoid_Dendritic_Cell_Neoplasm$", re.I).sub(u"芽球性形質細胞様樹状細胞腫瘍", text)
        text = re.compile(u"^核酸アナログ製剤・Peg-IFNα-2a$", re.I).sub(u"核酸アナログ製剤・ペグインターフェロンα-2a", text)
        text = re.compile(u"^活性型CaSR異常症$", re.I).sub(u"活性型カルシウム感受性受容体異常症", text)
        text = re.compile(u"^活性型ビタミンD製剤副作用・乳酸Ca副作用$", re.I).sub(u"活性型ビタミンD製剤副作用・乳酸カルシウム副作用", text)
        text = re.compile(u"^septic_shock$", re.I).sub(u"感染性ショック", text)
        text = re.compile(u"^breakthrough_肝炎$", re.I).sub(u"breakthrough_hepatitis", text)
        text = re.compile(u"^肝性IgA腎症$", re.I).sub(u"肝性IgA腎症", text)
        text = re.compile(u"^肝転移・S53cm単発$", re.I).sub(u"肝転移・S53cm単発", text)
        text = re.compile(u"^肝Reactive_lymphoid_hyperplasia$", re.I).sub(u"肝反応性リンパ組織増生", text)
        text = re.compile(u"^Hepatosplenic_γδ_T細胞リンパ腫$", re.I).sub(u"肝脾γδT細胞リンパ腫", text)
        text = re.compile(u"^眼窩marginal_zone_B-cell_リンパ腫$", re.I).sub(u"眼窩辺縁帯b細胞リンパ腫", text)
        text = re.compile(u"^paradoxical_response$", re.I).sub(u"奇異反応", text)
        text = re.compile(u"^Tracheal_web$", re.I).sub(u"気管支 web", text)
        text = re.compile(u"^Hungry_Bone_Syndrome$", re.I).sub(u"飢餓骨症候群", text)
        text = re.compile(u"^偽Bartter症候群$", re.I).sub(u"偽性バーター症候群", text)
        text = re.compile(u"^Pseudo-クッシング症候群$", re.I).sub(u"偽性クッシング症候群", text)
        text = re.compile(u"^偽性Bartter症候群$", re.I).sub(u"偽性バーター症候群", text)
        text = re.compile(u"^偽性Batter症候群$", re.I).sub(u"偽性バーター症候群", text)
        text = re.compile(u"^Pseudo-pseudo-Meigs症候群$", re.I).sub(u"偽性メイグス症候群", text)
        text = re.compile(u"^pseudo-Meigs症候群$", re.I).sub(u"偽性メイグス症候群", text)
        text = re.compile(u"^pseudo_renal_failure$", re.I).sub(u"偽性腎不全", text)
        text = re.compile(u"^pseudo-renal_failure$", re.I).sub(u"偽性腎不全", text)
        text = re.compile(u"^偽性副甲状腺機能低下症type2$", re.I).sub(u"偽性副甲状腺機能低下症2型", text)
        text = re.compile(u"^偽性副甲状腺機能低下症Ib型$", re.I).sub(u"偽性副甲状腺機能低下症Ib型", text)
        text = re.compile(u"^Acute_akinesia$", re.I).sub(u"急性アキネジア", text)
        text = re.compile(u"^急性graft_versus_host_disease$", re.I).sub(u"急性移植片対宿主病", text)
        text = re.compile(u"^acute_motor_sensory_axonal_neuropathy$", re.I).sub(u"急性運動感覚性軸索型ニューロパチー", text)
        text = re.compile(u"^AML_M4Eo$", re.I).sub(u"急性骨髄性白血病M4Eo", text)
        text = re.compile(u"^biphenotypic_acute_leukemia$", re.I).sub(u"急性混合型白血病", text)
        text = re.compile(u"^Acute_undifferentiated_leukemia$", re.I).sub(u"急性未分化白血病", text)
        text = re.compile(u"^infusion_reaction$", re.I).sub(u"急性輸液反応", text)
        text = re.compile(u"^megakaryoblast増加$", re.I).sub(u"巨核芽細胞増加", text)
        text = re.compile(u"^interface_肝炎$", re.I).sub(u"境界性肝炎", text)
        text = re.compile(u"^胸腺腫type_B2$", re.I).sub(u"胸腺腫B2型", text)
        text = re.compile(u"^local_osteolytichypercalcemia$", re.I).sub(u"局所溶骨性高カルシウム血症", text)
        text = re.compile(u"^Metallic_implant-associated_リンパ腫$", re.I).sub(u"金属製インプラント関連リンパ腫", text)
        text = re.compile(u"^HFrEF$", re.I).sub(u"駆出率が低下した心不全", text)
        text = re.compile(u"^plasmablasticリンパ腫$", re.I).sub(u"形質芽球性リンパ腫", text)
        text = re.compile(u"^crowned_dens症候群$", re.I).sub(u"Crowned_dens症候群", text)
        text = re.compile(u"^nodular_histiocytic_hyperplasia$", re.I).sub(u"結節性組織球過形成", text)
        text = re.compile(u"^hemangiopericytoma$", re.I).sub(u"血管外皮腫", text)
        text = re.compile(u"^asian_variant_of_血管内リンパ腫$", re.I).sub(u"血管内リンパ腫のアジア変種", text)
        text = re.compile(u"^intravasucular_large_B_cell_リンパ腫$", re.I).sub(u"血管内大型細胞B細胞リンパ腫", text)
        text = re.compile(u"^intravascular_large_B_cell_リンパ腫$", re.I).sub(u"血管内大細胞型B細胞リンパ腫", text)
        text = re.compile(u"^asian_variantofintravascular_large_B-cell_リンパ腫$", re.I).sub(u"血管内大細胞型B細胞リンパ腫のアジア変種", text)
        text = re.compile(u"^Angioimmunoblastic_T細胞リンパ腫$", re.I).sub(u"血管免疫芽細胞性T細胞リンパ腫", text)
        text = re.compile(u"^AngioimmunoblasticT細胞リンパ腫$", re.I).sub(u"血管免疫芽細胞性T細胞リンパ腫", text)
        text = re.compile(u"^angioimmunoblastic_T_cell_リンパ腫$", re.I).sub(u"血管免疫芽細胞性T細胞リンパ腫", text)
        text = re.compile(u"^PaIgG/上昇$", re.I).sub(u"血小板関連IgG/上昇", text)
        text = re.compile(u"^myeloid_neoplasms_associated_with_PDGFRα_rearrangement$", re.I).sub(u"血小板由来成長因子受容体αの再配列に関連する骨髄腫", text)
        text = re.compile(u"^血清Ca/低下$", re.I).sub(u"血清カルシウム/低下", text)
        text = re.compile(u"^MicroscopicPolyangiits$", re.I).sub(u"顕微鏡的多発血管炎", text)
        text = re.compile(u"^microscopic_colitis$", re.I).sub(u"顕微鏡的大腸炎", text)
        text = re.compile(u"^Primary_Effusion_リンパ腫_Like_リンパ腫$", re.I).sub(u"原発性体液性リンパ腫様リンパ腫", text)
        text = re.compile(u"^Primary_Effusion_リンパ腫-Like_リンパ腫$", re.I).sub(u"原発性体液性リンパ腫様リンパ腫", text)
        text = re.compile(u"^PrimarycutaneousCD30-positive_T-cell_lymphoproliferative_disorder$", re.I).sub(u"原発性皮膚CD30陽性T細胞型リンパ増殖性疾患", text)
        text = re.compile(u"^Primarycutaneousびまん性大細胞型B細胞リンパ腫,_leg_type$", re.I).sub(u"原発性皮膚びまん性大細胞型B細胞リンパ腫、脚型", text)
        text = re.compile(u"^Primary_effusion_リンパ腫$", re.I).sub(u"原発性滲出液リンパ腫", text)
        text = re.compile(u"^Primaryeffusionリンパ腫$", re.I).sub(u"原発性滲出液リンパ腫", text)
        text = re.compile(u"^PEL-like_リンパ腫$", re.I).sub(u"原発性滲出性リンパ腫様リンパ腫", text)
        text = re.compile(u"^solid-psudopapillary_neoplasm$", re.I).sub(u"固形疑似乳頭性腫瘍", text)
        text = re.compile(u"^Solitary_fibrous_tumor_of_the_pleura$", re.I).sub(u"孤在性胸膜線維腫", text)
        text = re.compile(u"^solitary_fibroustumor$", re.I).sub(u"孤在性線維性腫瘍", text)
        text = re.compile(u"^後天性von_Willebrand病$", re.I).sub(u"後天性フォン・ウェイブランド病", text)
        text = re.compile(u"^後天性免疫不全症候群_related_リンパ腫$", re.I).sub(u"後天性免疫不全症候群関連リンパ腫", text)
        text = re.compile(u"^eosinophilic_granulomatosis_with_polyangitis$", re.I).sub(u"好酸球性多発血管炎性肉芽腫症", text)
        text = re.compile(u"^diffuse_fasciitis_without_eosinophilia$", re.I).sub(u"好酸球増加症を伴わないびまん性筋膜炎", text)
        text = re.compile(u"^Hypereosinophilic_syndrome$", re.I).sub(u"好酸球増加症候群", text)
        text = re.compile(u"^抗MuSK抗体陽性重症筋無力症$", re.I).sub(u"抗MuSK抗体陽性重症筋無力症", text)
        text = re.compile(u"^抗アミノアシルtRNA抗体症候群$", re.I).sub(u"抗アミノアシルtRNA抗体症候群", text)
        text = re.compile(u"^抗アミノアシルt-RNA合成酵素抗体症候群$", re.I).sub(u"抗アミノアシルtRNA抗体症候群", text)
        text = re.compile(u"^anti-androgen_withdrawalsyndrome$", re.I).sub(u"抗アンドロゲン退薬症候群", text)
        text = re.compile(u"^抗結核療法paradoxicalreaction$", re.I).sub(u"抗結核療法奇異反応", text)
        text = re.compile(u"^aggressive_NK-cell_leukemia$", re.I).sub(u"攻撃性NK細胞白血病", text)
        text = re.compile(u"^euthyroid_Graves'_ophthalmopathy$", re.I).sub(u"甲状腺機能正常性グレーブス眼症", text)
        text = re.compile(u"^Euthyroid_Grave&#039;s$", re.I).sub(u"甲状腺機能正常性バセドウ病", text)
        text = re.compile(u"^Euthyroid_Orbital_Myositis$", re.I).sub(u"甲状腺機能正常性眼窩筋炎", text)
        text = re.compile(u"^Hypothyroid_Graves'_disease$", re.I).sub(u"甲状腺機能低下性グレーブス病", text)
        text = re.compile(u"^高Ca血症性副甲状腺クリーゼ$", re.I).sub(u"高Ca血症性副甲状腺クリーゼ", text)
        text = re.compile(u"^高Cl性代謝性アシドーシス$", re.I).sub(u"高Cl性代謝性アシドーシス", text)
        text = re.compile(u"^高IgE症候群$", re.I).sub(u"高IgE症候群", text)
        text = re.compile(u"^高IgG4症候群$", re.I).sub(u"高IgG4症候群", text)
        text = re.compile(u"^高IgM症候群$", re.I).sub(u"高IgM症候群", text)
        text = re.compile(u"^高Lp血症$", re.I).sub(u"高Lp血症", text)
        text = re.compile(u"^高Ca血症$", re.I).sub(u"高カルシウム血症", text)
        text = re.compile(u"^Humoral_Hypercalcemia$", re.I).sub(u"体液性高カルシウム血症", text)
        text = re.compile(u"^高Ca尿症$", re.I).sub(u"高カルシウム尿症", text)
        text = re.compile(u"^高Cl性アシドーシス$", re.I).sub(u"高クロール性アシドーシス", text)
        text = re.compile(u"^高Na血症$", re.I).sub(u"高ナトリウム血症", text)
        text = re.compile(u"^高酸素親和性異常Hb症$", re.I).sub(u"高酸素親和性異常Hb症", text)
        text = re.compile(u"^高iPTH血症$", re.I).sub(u"高副甲状腺ホルモン血症", text)
        text = re.compile(u"^骨Paget病$", re.I).sub(u"骨パジェット病", text)
        text = re.compile(u"^骨格筋型極長鎖アシルCoA脱水素酵素欠損症$", re.I).sub(u"骨格筋型極長鎖アシルCoA脱水素酵素欠損症", text)
        text = re.compile(u"^MDS5q-syndrome$", re.I).sub(u"骨髄異形成症候群 5q-症候群", text)
        text = re.compile(u"^Acute_myeloid_leukemia_with_myelodysplasia-related_changes$", re.I).sub(u"骨髄形成異常関連の変化を伴う急性骨髄性白血病", text)
        text = re.compile(u"^myeloma_cast_nephropathy$", re.I).sub(u"骨髄腫尿円柱腎障害", text)
        text = re.compile(u"^Left_main_trunk_compression_syndrome$", re.I).sub(u"左冠動脈主幹部圧迫症候群", text)
        text = re.compile(u"^subclavian_steal_syndrome$", re.I).sub(u"鎖骨下動脈盗血流症候群", text)
        text = re.compile(u"^refeedingsyndrome$", re.I).sub(u"再栄養症候群", text)
        text = re.compile(u"^refeeding_syndrome$", re.I).sub(u"再栄養症候群", text)
        text = re.compile(u"^再発lymphoplasmacytic_リンパ腫$", re.I).sub(u"再発リンパ形質細胞性リンパ腫", text)
        text = re.compile(u"^再発Mantle_cell_リンパ腫$", re.I).sub(u"再発外套細胞リンパ腫", text)
        text = re.compile(u"^bacterial_translocation$", re.I).sub(u"細菌転移", text)
        text = re.compile(u"^cytotoxicT細胞リンパ腫$", re.I).sub(u"細胞傷害性T細胞リンパ腫", text)
        text = re.compile(u"^cytotoxicT細胞リンパ腫再発$", re.I).sub(u"細胞傷害性T細胞リンパ腫再発", text)
        text = re.compile(u"^酸化Mg副作用$", re.I).sub(u"酸化マグネシウム副作用", text)
        text = re.compile(u"^lipomatous_pseudohypertrophy_of_the_pancreas$", re.I).sub(u"脂肪腺性の偽性膵臓肥大", text)
        text = re.compile(u"^lipolysis$", re.I).sub(u"脂肪分解", text)
        text = re.compile(u"^NMO_spectrum_disorder$", re.I).sub(u"視神経脊髄炎スペクトラム疾患", text)
        text = re.compile(u"^Persistent_hyperインスリンemic_hypoglycemia$", re.I).sub(u"持続性高インスリン性低血糖症", text)
        text = re.compile(u"^Interstitial_Pneumonia_with_Autoimmune_Features$", re.I).sub(u"自己免疫性特徴を伴う間質性肺炎", text)
        text = re.compile(u"^Ketosis-prone_type_2_diabetes$", re.I).sub(u"ケトーシスで始まる2型糖尿病", text)
        text = re.compile(u"^Ketosis-prone_type2_diabetes$", re.I).sub(u"ケトーシスで始まる2型糖尿病", text)
        text = re.compile(u"^maturity-onset_diabetes_of_the_young$", re.I).sub(u"若年発症成人型糖尿病", text)
        text = re.compile(u"^primaryspinalリンパ腫$", re.I).sub(u"主脊髄リンパ腫", text)
        text = re.compile(u"^paraneoplastic_synd$", re.I).sub(u"腫瘍随伴症候群", text)
        text = re.compile(u"^tumor_induced_acute_pancreatitis$", re.I).sub(u"腫瘍性急性膵炎", text)
        text = re.compile(u"^malignant_osteoclasticgiantcell_tumor_of_duodenum$", re.I).sub(u"十二指腸悪性骨腫瘍", text)
        text = re.compile(u"^十二指腸Gangliocytic_Paraganglioma$", re.I).sub(u"十二指腸神経節細胞性傍神経節腫", text)
        text = re.compile(u"^pure_autonomic_failure$", re.I).sub(u"純粋自律神経失調症", text)
        text = re.compile(u"^smalllymphocyticリンパ腫$", re.I).sub(u"小リンパ球リンパ腫", text)
        text = re.compile(u"^paraimmunoblastic_variant_of_smalllymphocyticリンパ腫・慢性リンパ性白血病$", re.I).sub(u"小リンパ球性リンパ腫の偽性免疫芽球性変種・慢性リンパ性白血病", text)
        text = re.compile(u"^小腸angiodysplasia$", re.I).sub(u"小腸血管形成異常", text)
        text = re.compile(u"^gastrointestinal_stromal_tumor$", re.I).sub(u"消化管間質腫瘍", text)
        text = re.compile(u"^消化管間質腫瘍@胃・Littoral_cell_angioma@脾$", re.I).sub(u"消化管間質腫瘍@胃・沿岸細胞血管腫@脾", text)
        text = re.compile(u"^食道Web$", re.I).sub(u"食道Web", text)
        text = re.compile(u"^aggressive_large_granular_lymphocytic_leukemia$", re.I).sub(u"侵攻性大顆粒リンパ球性白血病", text)
        text = re.compile(u"^invasive_Klebsiella_pneumonia_syndrome$", re.I).sub(u"侵入クレブシエラ肺炎桿菌症候群", text)
        text = re.compile(u"^Beer_Potomania$", re.I).sub(u"心因性ビール多飲症", text)
        text = re.compile(u"^神経Sweet病$", re.I).sub(u"神経スウィート病", text)
        text = re.compile(u"^神経Beh.et病$", re.I).sub(u"神経ベーチェット病", text)
        text = re.compile(u"^Neuralgic_Amyotrophy$", re.I).sub(u"神経痛性筋萎縮", text)
        text = re.compile(u"^Neuroendorine_tumor$", re.I).sub(u"神経内分泌腫瘍", text)
        text = re.compile(u"^glioblastoma$", re.I).sub(u"神経膠芽腫", text)
        text = re.compile(u"^sarcomatoid_renal_cell_carcinoma$", re.I).sub(u"腎明細胞癌", text)
        text = re.compile(u"^probable_毒素性ショック症候群$", re.I).sub(u"推定毒素性ショック症候群", text)
        text = re.compile(u"^Varicella-Zoster_Virus再帰感染$", re.I).sub(u"水痘帯状疱疹ウイルス再帰感染", text)
        text = re.compile(u"^herpes_zoster_encephalitis$", re.I).sub(u"水痘帯状疱疹ウイルス脳炎", text)
        text = re.compile(u"^sleep_apnea_syndrome$", re.I).sub(u"睡眠時無呼吸症候群", text)
        text = re.compile(u"^GnRHアナログ副作用$", re.I).sub(u"性腺刺激ホルモン放出ホルモンアナログ副作用", text)
        text = re.compile(u"^adult_T_cellleukemia_リンパ腫$", re.I).sub(u"成人T細胞白血病リンパ腫", text)
        text = re.compile(u"^成人型still病$", re.I).sub(u"成人型スティル病", text)
        text = re.compile(u"^Mature_B_cell_neoplasm$", re.I).sub(u"成人性B型細胞腫瘍", text)
        text = re.compile(u"^Adult_respiratory_distress_syndrome$", re.I).sub(u"成人性呼吸促迫症候群", text)
        text = re.compile(u"^Blue_Toe症候群$", re.I).sub(u"青趾症候群", text)
        text = re.compile(u"^Blue_toe_sndrome$", re.I).sub(u"青趾症候群", text)
        text = re.compile(u"^Silent_corticotroph_andsomatotroph腺腫$", re.I).sub(u"静止副腎皮質刺激ホルモン分泌細胞アンドソマトトロフ腺腫", text)
        text = re.compile(u"^veno-occlusive_disease$", re.I).sub(u"静脈閉塞性疾患", text)
        text = re.compile(u"^Calcified_amorphous_tumor$", re.I).sub(u"石灰化無形腫瘍", text)
        text = re.compile(u"^Pure_erythroid_leukemia$", re.I).sub(u"赤血球系白血病", text)
        text = re.compile(u"^pure_red_cell_aplasia$", re.I).sub(u"赤血球糸無形成症;", text)
        text = re.compile(u"^Extranodal_marginalzone_B-cell_リンパ腫$", re.I).sub(u"節外性辺縁帯B細胞リンパ腫", text)
        text = re.compile(u"^Intravascular_large_B-cell_リンパ腫$", re.I).sub(u"節外性辺縁帯B細胞リンパ腫", text)
        text = re.compile(u"^Acromegalic_Cardiomyopathy$", re.I).sub(u"先端巨大症型心筋症", text)
        text = re.compile(u"^潜在性IgA沈着$", re.I).sub(u"潜在性免疫グロブリンA沈着", text)
        text = re.compile(u"^Fibrolipomatous_Hamartoma$", re.I).sub(u"線維平滑筋腫過誤腫", text)
        text = re.compile(u"^腺腫tous_goiter$", re.I).sub(u"腺腫性甲状腺腫", text)
        text = re.compile(u"^選択的IgA欠損症$", re.I).sub(u"選択的IgA欠損症", text)
        text = re.compile(u"^選択的IgG2欠損症$", re.I).sub(u"選択的IgG2欠損症", text)
        text = re.compile(u"^pre-クッシング症候群$", re.I).sub(u"プレクリニカルクッシング症候群", text)
        text = re.compile(u"^precursor_T-lymphoblasticleukemia$", re.I).sub(u"前駆Tリンパ芽球性白血病", text)
        text = re.compile(u"^preclinical_クッシング症候群$", re.I).sub(u"プレクリニカルクッシング症候群", text)
        text = re.compile(u"^全身性IgG4関連疾患$", re.I).sub(u"全身性IgG4関連疾患", text)
        text = re.compile(u"^Systemic_Cappillary_Leak_Syndrome$", re.I).sub(u"全身性毛細血管漏出症候群", text)
        text = re.compile(u"^Systemic_capillary_leak_syndrome$", re.I).sub(u"全身性毛細血管漏出症候群", text)
        text = re.compile(u"^AML_with_multilineage_dysplasia$", re.I).sub(u"多系列異形成を伴う急性骨髄性白血病", text)
        text = re.compile(u"^Polyglandular_Autoimmune_Syndrome_TypeIII$", re.I).sub(u"多腺性自己免疫症候群3型", text)
        text = re.compile(u"^Polyglandular_autoimmune_type_3$", re.I).sub(u"多腺性自己免疫性症候群3型", text)
        text = re.compile(u"^Multicentric_Castleman's_Disease$", re.I).sub(u"多中心性キャッスルマン病", text)
        text = re.compile(u"^Multicentric_キャッスルマン病$", re.I).sub(u"多中心性キャッスルマン病", text)
        text = re.compile(u"^Multicentric_Castleman&#039;s_Disease$", re.I).sub(u"多中心性キャッスルマン病", text)
        text = re.compile(u"^Polycystic_ovary_syndrome$", re.I).sub(u"多嚢胞性卵巣症候群", text)
        text = re.compile(u"^polyangitis_overlap_syndrome$", re.I).sub(u"多発血管炎オーバーラップ症候群", text)
        text = re.compile(u"^Granulomatosis_with_Polyangitis$", re.I).sub(u"多発血管炎性肉芽腫症", text)
        text = re.compile(u"^granulomatosis_with_polyangiitis$", re.I).sub(u"多発血管炎性肉芽腫症", text)
        text = re.compile(u"^多発性内分泌腫瘍2a型$", re.I).sub(u"多発性内分泌腫瘍2a型", text)
        text = re.compile(u"^MEN_type_1$", re.I).sub(u"多発性内分泌腺腫症1型", text)
        text = re.compile(u"^大腿骨原発diffuse_large_B_cellリンパ腫$", re.I).sub(u"大腿骨原発びまん性大型B細胞リンパ腫", text)
        text = re.compile(u"^大腸mucosal_polyp$", re.I).sub(u"大腸粘膜ポリープ", text)
        text = re.compile(u"^Large_GranularLymphocytic_Leukemia$", re.I).sub(u"大顆粒リンパ球性白血病", text)
        text = re.compile(u"^large_granular_lymphocyte白血病$", re.I).sub(u"大顆粒リンパ球白血病", text)
        text = re.compile(u"^protein_calorie_malnutrition$", re.I).sub(u"蛋白・カロリー栄養失調症", text)
        text = re.compile(u"^Septo-Optic-Dysplasia$", re.I).sub(u"中隔視神経異形成症", text)
        text = re.compile(u"^Primary_angitis_of_the_Central_nervous_system$", re.I).sub(u"中枢神経限局性血管炎", text)
        text = re.compile(u"^EnteropathytypeT_cell_リンパ腫$", re.I).sub(u"腸疾患T型細胞リンパ腫", text)
        text = re.compile(u"^Painfull_sensory_neuropathy$", re.I).sub(u"痛覚神経症", text)
        text = re.compile(u"^低Ca尿性高Ca血症$", re.I).sub(u"低カルシウム尿性高カルシウム血症", text)
        text = re.compile(u"^低K・低Mg$", re.I).sub(u"低カリウム・低マグネシウム", text)
        text = re.compile(u"^低Ca血症$", re.I).sub(u"低カルシウム血症", text)
        text = re.compile(u"^低Cl血症$", re.I).sub(u"低クロール血症", text)
        text = re.compile(u"^低ナトリウム血症・低カリウム血症・低Cl血症$", re.I).sub(u"低ナトリウム血症・低カリウム血症・低クロール血症", text)
        text = re.compile(u"^Poorlydifferentiatedhepatocellular_carcinoma$", re.I).sub(u"低分化肝細胞癌", text)
        text = re.compile(u"^Electrolyte_Depletion_Syndrome$", re.I).sub(u"電解質低下症候群", text)
        text = re.compile(u"^Diabetic_lipemia$", re.I).sub(u"糖尿病性脂肪血症", text)
        text = re.compile(u"^diabetic_polyneuropathy$", re.I).sub(u"糖尿病性多発ニューロパチー", text)
        text = re.compile(u"^糖尿病性hemichorea-hemiballism$", re.I).sub(u"糖尿病性半側舞踏病・片側バリズム", text)
        text = re.compile(u"^flail_arm症候群$", re.I).sub(u"動揺腕症候群", text)
        text = re.compile(u"^Cu欠乏$", re.I).sub(u"銅欠乏", text)
        text = re.compile(u"^Cryptogenic_organizing_pneumonia$", re.I).sub(u"特発性器質化肺炎", text)
        text = re.compile(u"^Boerhaave_syndrome$", re.I).sub(u"特発性食道破裂", text)
        text = re.compile(u"^Toxic_Shock_Like_Syndrome$", re.I).sub(u"毒素性ショック様症候群", text)
        text = re.compile(u"^Isolated_body_lateropulsion$", re.I).sub(u"Isolated_body_lateropulsion", text)
        text = re.compile(u"^cryptogenicHCC$", re.I).sub(u"潜在性肝細胞癌", text)
        text = re.compile(u"^Idiopathic_primary_bent_spine_syndrome$", re.I).sub(u"Idiopathic_primary_bent_spine_syndrome", text)
        text = re.compile(u"^二次性IgA腎症$", re.I).sub(u"二次性IgA腎症", text)
        text = re.compile(u"^二次性Budd-chiari症候群$", re.I).sub(u"二次性バッド・キアリ症候群", text)
        text = re.compile(u"^乳房外Paget病$", re.I).sub(u"乳房外パジェット病", text)
        text = re.compile(u"^Tubulointerstitial_nephritis-uveitis_syndrome$", re.I).sub(u"尿細管間質性腎炎・ぶどう膜炎症候群", text)
        text = re.compile(u"^cystic_pituitary_腺腫$", re.I).sub(u"嚢胞性下垂体腺腫", text)
        text = re.compile(u"^Cranial_neuropathy$", re.I).sub(u"脳神経障害", text)
        text = re.compile(u"^pyothorax-associated_リンパ腫$", re.I).sub(u"膿胸関連リンパ腫", text)
        text = re.compile(u"^肺M._abscessus症$", re.I).sub(u"肺マイコバクテリウム・アブセサス症", text)
        text = re.compile(u"^肺Mycobacterium_shinjukuense感染症$", re.I).sub(u"肺マイコバクテリウム・シンジュクエンス感染症", text)
        text = re.compile(u"^Klebsiella_pneumoniae感染症$", re.I).sub(u"肺炎かん菌感染症", text)
        text = re.compile(u"^C.pneumoniae肺炎$", re.I).sub(u"肺炎クラミジア肺炎", text)
        text = re.compile(u"^pulmonarytumor血栓性微小血管症$", re.I).sub(u"肺腫瘍血栓性微小血管症", text)
        text = re.compile(u"^Pulmonary_tumor_血栓性微小血管症$", re.I).sub(u"肺腫瘍血栓性微小血管症", text)
        text = re.compile(u"^pulmonary_abscess$", re.I).sub(u"肺膿瘍", text)
        text = re.compile(u"^Purewhitecellaplasia$", re.I).sub(u"白血球形成不全", text)
        text = re.compile(u"^pure_white_cell_aplasia$", re.I).sub(u"白血球形成不全", text)
        text = re.compile(u"^leukostasis$", re.I).sub(u"白血球停滞", text)
        text = re.compile(u"^hemichorea$", re.I).sub(u"片側舞踏病", text)
        text = re.compile(u"^hemichorea-hemiballism症候群$", re.I).sub(u"片側舞踏病・片側バリズム症候群", text)
        text = re.compile(u"^Burned-out_先端巨大症$", re.I).sub(u"疲労無力性先端巨大症", text)
        text = re.compile(u"^Nonalcoholic_steato肝炎$", re.I).sub(u"非アルコール性脂肪肝炎", text)
        text = re.compile(u"^NSAIDs関連腎症$", re.I).sub(u"非ステロイド性抗炎症薬関連腎症", text)
        text = re.compile(u"^NSAIDs潰瘍$", re.I).sub(u"非ステロイド性抗炎症性薬潰瘍", text)
        text = re.compile(u"^NSAIDs内服歴$", re.I).sub(u"非ステロイド性抗炎症薬内服歴", text)
        text = re.compile(u"^NSAIDs副作用$", re.I).sub(u"非ステロイド性抗炎症薬副作用", text)
        text = re.compile(u"^NSAIDs誘発性髄膜炎$", re.I).sub(u"非ステロイド性抗炎症薬誘発性髄膜炎", text)
        text = re.compile(u"^Non-Hodgkin_びまん性大細胞型B細胞リンパ腫$", re.I).sub(u"非ホジキンリンパ腫 びまん性大細胞型B細胞リンパ腫", text)
        text = re.compile(u"^非肝硬変性Portal-systemic_encephalopathy$", re.I).sub(u"非肝硬変性門脈体循環性脳障害", text)
        text = re.compile(u"^非持続性wide_QRS_regular頻拍$", re.I).sub(u"非持続性wideQRS規則的頻拍", text)
        text = re.compile(u"^aHUS$", re.I).sub(u"非典型溶血性尿毒症症候群", text)
        text = re.compile(u"^Nonepisodic_angioedema_with_eosinophilia$", re.I).sub(u"非突発的好酸球性血管浮腫", text)
        text = re.compile(u"^Micronodular_pneumocytes_hyperplasia$", re.I).sub(u"微小結節型肺細胞過形成", text)
        text = re.compile(u"^microangiopathic_hemolytic_anemia$", re.I).sub(u"微小血管症性溶血性貧血", text)
        text = re.compile(u"^pauci-immune型半月体形成性腎炎$", re.I).sub(u"微量免疫型半月体形成性腎炎", text)
        text = re.compile(u"^overwhelming_postsplenectomy_infection_syndrome$", re.I).sub(u"脾臓摘出後感染症候群", text)
        text = re.compile(u"^不全型Ramsay-Hunt症候群$", re.I).sub(u"不全型ラムゼー・ハント症候群", text)
        text = re.compile(u"^不全型Ramsay_Hunt症候群$", re.I).sub(u"不全型ラムゼー・ハント症候群", text)
        text = re.compile(u"^PTHrP産生精巣原発びまん性大型B細胞リンパ腫$", re.I).sub(u"副甲状腺ホルモン関連タンパク質産生精巣原発びまん性大型B細胞リンパ腫", text)
        text = re.compile(u"^PTHrP産生腫瘍$", re.I).sub(u"副甲状腺ホルモン関連ペプチド産生腫瘍", text)
        text = re.compile(u"^副腎black_腺腫$", re.I).sub(u"副腎黒色腺腫", text)
        text = re.compile(u"^副腎性Preclinical_クッシング症候群$", re.I).sub(u"副腎性プレクリニカルクッシング症候群", text)
        text = re.compile(u"^composite_リンパ腫$", re.I).sub(u"複合リンパ腫", text)
        text = re.compile(u"^Branch_Atheromatous_Disease$", re.I).sub(u"分岐部動脈硬化症", text)
        text = re.compile(u"^marginalzone_B-cell_リンパ腫$", re.I).sub(u"辺縁帯B細胞リンパ腫", text)
        text = re.compile(u"^濾胞リンパ腫_with_marginal_zone_differentiation$", re.I).sub(u"辺縁帯に分化を伴う濾胞リンパ腫", text)
        text = re.compile(u"^paravalvular_leakage$", re.I).sub(u"弁周囲漏出", text)
        text = re.compile(u"^Maternally_inherited_diabetes_and_deafness$", re.I).sub(u"母胎遺伝性糖尿病および難聴", text)
        text = re.compile(u"^spindle_cellsarcoma$", re.I).sub(u"紡錘細胞肉腫", text)
        text = re.compile(u"^Peripheral_T細胞リンパ腫$", re.I).sub(u"末梢T細胞リンパ腫", text)
        text = re.compile(u"^Acromegalic_heart$", re.I).sub(u"末端肥大性心臓", text)
        text = re.compile(u"^慢性Chagas病$", re.I).sub(u"慢性シャーガス病", text)
        text = re.compile(u"^慢性graft_versus_host_disease$", re.I).sub(u"慢性移植片対宿主病", text)
        text = re.compile(u"^chronic_expanding_hematoma$", re.I).sub(u"慢性拡張型血腫", text)
        text = re.compile(u"^CML_lymphnodALBlast_crisis$", re.I).sub(u"慢性骨髄性白血病_リンパ節急性転化", text)
        text = re.compile(u"^chronic_idiopathic_axonalpolyneuropathy$", re.I).sub(u"慢性突発性軸索型ニューロパチー", text)
        text = re.compile(u"^chronic_播種性血管内凝固症候群$", re.I).sub(u"慢性播種性血管内凝固症候群", text)
        text = re.compile(u"^Anaplastic_large_cell_リンパ腫$", re.I).sub(u"未分化大細胞型リンパ腫", text)
        text = re.compile(u"^pulselessVT$", re.I).sub(u"脈欠損心室性頻拍", text)
        text = re.compile(u"^Acute_renal_failure_with_severeLoinpain_and_Patchy_renal_ischemia_after_anaerobic_Exercise$", re.I).sub(u"無酸素運動後における激しい腰腹痛を伴う急性腎不全と斑状腎虚血", text)
        text = re.compile(u"^Zoster_sine_herpete$", re.I).sub(u"無疱疹性帯状疱疹", text)
        text = re.compile(u"^immune-complex型半月体形成性糸球体腎炎$", re.I).sub(u"免疫複合体型半月体形成性糸球体腎炎", text)
        text = re.compile(u"^great_imitator$", re.I).sub(u"模倣の名人", text)
        text = re.compile(u"^Blind_loop_syndrome$", re.I).sub(u"盲管症候群", text)
        text = re.compile(u"^drug-induced_hypersensitivity_syndrome$", re.I).sub(u"薬剤性過敏症症候群", text)
        text = re.compile(u"^drug_induced_hypersensitivity_syndrome$", re.I).sub(u"薬剤性過敏症症候群", text)
        text = re.compile(u"^HairyB_cell_lymphoproliferative_disorder$", re.I).sub(u"有毛B細胞型リンパ腫疾患", text)
        text = re.compile(u"^hairy_cell_leukemia$", re.I).sub(u"有毛状細胞性白血病", text)
        text = re.compile(u"^HCL_Japanese_variant$", re.I).sub(u"有毛状細胞性白血病日本変種_", text)
        text = re.compile(u"^Hairy_cell_leukemia_variant$", re.I).sub(u"有毛状細胞性白血病変種", text)
        text = re.compile(u"^EBV-positive_T-cell_lymphoproliferative_disorders_of_childhood$", re.I).sub(u"幼年期EBV陽性T細胞リンパ増殖性疾患", text)
        text = re.compile(u"^volume_overload$", re.I).sub(u"volume_overload", text)
        text = re.compile(u"^Tumefactive_MS$", re.I).sub(u"隆起性MS", text)
        text = re.compile(u"^Benign_lymphoepithelial_cyst$", re.I).sub(u"良性リンパ上皮性嚢胞", text)
        text = re.compile(u"^Benign_Tremulous_Parkinsonism$", re.I).sub(u"良性腫瘍パーキンソン症候群", text)
        text = re.compile(u"^clinically_筋萎縮性側索硬化症$", re.I).sub(u"筋萎縮性側索硬化症", text)
        text = re.compile(u"^Clinically_mild_encephalitis・encephalopathy_with_a_reversible_spleniallesion$", re.I).sub(u"可逆性脳梁膨大部病変を有する軽症脳炎脳症", text)
        text = re.compile(u"^clinically_amyopathicdermatomyositis$", re.I).sub(u"非ミオパチー性皮膚筋炎", text)
        text = re.compile(u"^clinical_amyopatic_dermatomyositis$", re.I).sub(u"非ミオパチー性皮膚筋炎", text)
        text = re.compile(u"^Senile_EBV_associated_B-Cell_lymphoproliferative_disorder$", re.I).sub(u"老人性エブスタイン・バーウィルス関連のB細胞リンパ腫疾患", text)
        text = re.compile(u"^mTOR阻害薬副作用$", re.I).sub(u"哺乳類ラパマイシン標的タンパク質阻害薬副作用", text)
        text = re.compile(u"^Olfactory_neuroblastoma$", re.I).sub(u"嗅神経芽細胞腫", text)
        text = re.compile(u"^splenic_marginal_zone_リンパ腫$", re.I).sub(u"脾臓周辺帯リンパ腫", text)
        text = re.compile(u"^膀胱原発Burkitt-likeDiffuse_large_Bcell_リンパ腫$", re.I).sub(u"膀胱原発バーキット様びまん性大型B細胞リンパ腫", text)
        text = re.compile(u"^膵Solid_pseudopapillary_neoplasm$", re.I).sub(u"膵固形偽性乳頭腫瘍", text)
        text = re.compile(u"^膵Solid-pseudopapillary_neoplasm$", re.I).sub(u"膵固形偽性乳頭腫瘍", text)
        text = re.compile(u"^膵体部インスリンoma$", re.I).sub(u"膵体部インスリン腫", text)
        text = re.compile(u"^nonislet-cell_tumor_hypoglycemia$", re.I).sub(u"膵島細胞腫瘍に由来しない低血糖症", text)
        text = re.compile(u"^Non-isletcell_tumor_hypoglycemia$", re.I).sub(u"膵島細胞腫瘍に由来しない低血糖症", text)
        text = re.compile(u"^Crowned-dens症候群$", re.I).sub(u"Crowned_dens症候群", text)
        text = re.compile(u"^numb_chin_syndrome$", re.I).sub(u"頤しびれ症候群", text)
        text = re.compile(u"^numb_chin症候群$", re.I).sub(u"頤しびれ症候群", text)
        text = re.compile(u"^#NAME?$", re.I).sub(u"#NAME?", text)
        text = re.compile(u"^LGL$", re.I).sub(u"顆粒リンパ球", text)
        text = re.compile(u"^IPMT$", re.I).sub(u"膵管内乳頭状粘液腫瘍", text)
        text = re.compile(u"^AGD$", re.I).sub(u"嗜銀顆粒性認知症", text)
        text = re.compile(u"^MALT$", re.I).sub(u"両側副腎原発非ホジキンリンパ腫", text)
        text = re.compile(u"^BHL$", re.I).sub(u"両側肺門リンパ節腫大", text)
        text = re.compile(u"^PFO$", re.I).sub(u"卵円孔開存", text)
        text = re.compile(u"^PSAGN$", re.I).sub(u"溶連菌感染後急性糸球体腎炎", text)
        text = re.compile(u"^HUS$", re.I).sub(u"溶血性尿毒素症候群", text)
        text = re.compile(u"^HUS$", re.I).sub(u"溶血性尿毒症症候群", text)
        text = re.compile(u"^TRALI$", re.I).sub(u"輸血後急性肺障害", text)
        text = re.compile(u"^DES$", re.I).sub(u"薬剤溶出性ステント", text)
        text = re.compile(u"^CYPHER$", re.I).sub(u"薬剤溶出ステント", text)
        text = re.compile(u"^DIHS$", re.I).sub(u"薬剤性過敏症症候群", text)
        text = re.compile(u"^DLST$", re.I).sub(u"薬剤リンパ球刺激試験", text)
        text = re.compile(u"^ITP$", re.I).sub(u"免疫性血小板減少症", text)
        text = re.compile(u"^IRIS$", re.I).sub(u"免疫再構築症候群", text)
        text = re.compile(u"^IVIG$", re.I).sub(u"免疫グロブリン大量療法_", text)
        text = re.compile(u"^IVIg$", re.I).sub(u"免疫グロブリン大量療法", text)
        text = re.compile(u"^IVIg$", re.I).sub(u"免疫グロブリン大量静注療法", text)
        text = re.compile(u"^IVIg$", re.I).sub(u"免疫グロブリン静注療法", text)
        text = re.compile(u"^LCDD$", re.I).sub(u"免疫グロブリンL鎖沈着症", text)
        text = re.compile(u"^PEA$", re.I).sub(u"無脈性電気活動", text)
        text = re.compile(u"^COPD$", re.I).sub(u"慢性閉塞性肺疾患", text)
        text = re.compile(u"^CKD$", re.I).sub(u"慢性腎臓病", text)
        text = re.compile(u"^CMML$", re.I).sub(u"慢性骨髄単球性白血病", text)
        text = re.compile(u"^CMMoL$", re.I).sub(u"慢性骨髄単球性白血病", text)
        text = re.compile(u"^CML$", re.I).sub(u"慢性骨髄性白血病", text)
        text = re.compile(u"^CEL$", re.I).sub(u"慢性好酸球性白血病", text)
        text = re.compile(u"^CTEPH$", re.I).sub(u"慢性血栓塞栓性肺高血圧症", text)
        text = re.compile(u"^CAEBV$", re.I).sub(u"慢性活動性EBV感染症", text)
        text = re.compile(u"^CIDP$", re.I).sub(u"慢性炎症性脱髄性多発神経炎", text)
        text = re.compile(u"^GVHD$", re.I).sub(u"慢性移植片対宿主病", text)
        text = re.compile(u"^CLL$", re.I).sub(u"慢性リンパ性白血病", text)
        text = re.compile(u"^MPGN$", re.I).sub(u"膜性増殖性腎炎", text)
        text = re.compile(u"^MPGN$", re.I).sub(u"膜性増殖性糸球体腎炎", text)
        text = re.compile(u"^PNS$", re.I).sub(u"傍腫瘍神経症候群", text)
        text = re.compile(u"^DCA$", re.I).sub(u"方向性冠動脈アテレクトミー", text)
        text = re.compile(u"^HOCM$", re.I).sub(u"閉塞性肥大型心筋症", text)
        text = re.compile(u"^CRPS$", re.I).sub(u"複合性局所疼痛症候群", text)
        text = re.compile(u"^AVS$", re.I).sub(u"副腎静脈サンプリング", text)
        text = re.compile(u"^PSE$", re.I).sub(u"部分的脾動脈塞栓術", text)
        text = re.compile(u"^MCNS$", re.I).sub(u"微小変化型ネフローゼ症候群", text)
        text = re.compile(u"^NOMI$", re.I).sub(u"非閉塞性腸管虚血症", text)
        text = re.compile(u"^NOMI$", re.I).sub(u"非閉塞性腸管虚血", text)
        text = re.compile(u"^LRPN$", re.I).sub(u"非糖尿病性腰部根神経叢炎", text)
        text = re.compile(u"^aHUS$", re.I).sub(u"非典型溶血性尿毒症症候群", text)
        text = re.compile(u"^NPPV$", re.I).sub(u"非侵襲的陽圧換気療法", text)
        text = re.compile(u"^NIV$", re.I).sub(u"非侵襲的陽圧換気", text)
        text = re.compile(u"^NPPV$", re.I).sub(u"非侵襲的陽圧換気", text)
        text = re.compile(u"^NBTE$", re.I).sub(u"非細菌性血栓性心内膜炎", text)
        text = re.compile(u"^NTM$", re.I).sub(u"非結核性抗酸菌症", text)
        text = re.compile(u"^NSAIDs$", re.I).sub(u"非ステロイド性抗炎症薬", text)
        text = re.compile(u"^NASH$", re.I).sub(u"非アルコール性脂肪性肝炎", text)
        text = re.compile(u"^NASH$", re.I).sub(u"非アルコール性脂肪肝炎", text)
        text = re.compile(u"^EPS$", re.I).sub(u"被嚢性腹膜硬化症", text)
        text = re.compile(u"^CPAN$", re.I).sub(u"皮膚型結節性多発動脈炎", text)
        text = re.compile(u"^PNH$", re.I).sub(u"発作性夜間血色素尿症", text)
        text = re.compile(u"^PAF$", re.I).sub(u"発作性心房細動", text)
        text = re.compile(u"^PNH$", re.I).sub(u"発作性血色素尿症", text)
        text = re.compile(u"^LCAP$", re.I).sub(u"白血球除去療法", text)
        text = re.compile(u"^PAH$", re.I).sub(u"肺動脈性肺高血圧症", text)
        text = re.compile(u"^PTE$", re.I).sub(u"肺血栓塞栓症", text)
        text = re.compile(u"^PSSP$", re.I).sub(u"肺炎球菌", text)
        text = re.compile(u"^DIC$", re.I).sub(u"播種性血管内凝固症候群", text)
        text = re.compile(u"^RTA$", re.I).sub(u"尿細管性アシドーシス", text)
        text = re.compile(u"^DFPP$", re.I).sub(u"二重濾過血漿交換", text)
        text = re.compile(u"^TTP$", re.I).sub(u"難治性血栓性血小板減少性紫斑病", text)
        text = re.compile(u"^EMR$", re.I).sub(u"内視鏡的粘膜切除術", text)
        text = re.compile(u"^ESD$", re.I).sub(u"内視鏡的粘膜下層剥離術", text)
        text = re.compile(u"^EVL$", re.I).sub(u"内視鏡的静脈瘤結紮術", text)
        text = re.compile(u"^EVL$", re.I).sub(u"内視鏡的食道静脈瘤結紮術", text)
        text = re.compile(u"^EIS$", re.I).sub(u"内視鏡的硬化療法", text)
        text = re.compile(u"^EVL$", re.I).sub(u"内視鏡的結紮術", text)
        text = re.compile(u"^ENBD$", re.I).sub(u"内視鏡的経鼻胆管ドレナージ", text)
        text = re.compile(u"^ERCP$", re.I).sub(u"内視鏡的逆行性膵胆管造影", text)
        text = re.compile(u"^TSS$", re.I).sub(u"毒素性ショック症候群", text)
        text = re.compile(u"^TSS$", re.I).sub(u"毒素ショック症候群", text)
        text = re.compile(u"^IPAH$", re.I).sub(u"特発性肺動脈性肺高血圧症", text)
        text = re.compile(u"^IPF$", re.I).sub(u"特発性肺線維症", text)
        text = re.compile(u"^HES$", re.I).sub(u"特発性好酸球増多症候群", text)
        text = re.compile(u"^HES$", re.I).sub(u"特発性好酸球増多症", text)
        text = re.compile(u"^ITP$", re.I).sub(u"特発性血小板減少性紫斑病", text)
        text = re.compile(u"^COP$", re.I).sub(u"特発性器質化肺炎", text)
        text = re.compile(u"^IHA$", re.I).sub(u"特発性アルドステロン症", text)
        text = re.compile(u"^CTA$", re.I).sub(u"動脈造影下CTスキャン", text)
        text = re.compile(u"^DWI$", re.I).sub(u"頭部MRI拡散強調画像", text)
        text = re.compile(u"^DKA$", re.I).sub(u"糖尿病性ケトアシドーシス", text)
        text = re.compile(u"^DKA$", re.I).sub(u"糖尿病ケトアシドーシス", text)
        text = re.compile(u"^EPS$", re.I).sub(u"電気生理検査", text)
        text = re.compile(u"^UC$", re.I).sub(u"潰瘍性大腸炎", text)
        text = re.compile(u"^UIP$", re.I).sub(u"通常型間質性肺炎", text)
        text = re.compile(u"^EUS-FNA$", re.I).sub(u"超音波内視鏡下穿刺吸引細胞診", text)
        text = re.compile(u"^EBUS-TBNA$", re.I).sub(u"超音波気管支鏡ガイド下針生検", text)
        text = re.compile(u"^IVIG$", re.I).sub(u"大量γグロブリン療法", text)
        text = re.compile(u"^IABP$", re.I).sub(u"大動脈内バルーンパンピング", text)
        text = re.compile(u"^LCNEC$", re.I).sub(u"大細胞神経内分泌癌", text)
        text = re.compile(u"^JDS$", re.I).sub(u"台", text)
        text = re.compile(u"^ECMO$", re.I).sub(u"体外式膜型人工肺", text)
        text = re.compile(u"^POTS$", re.I).sub(u"体位性頻脈症候群", text)
        text = re.compile(u"^MEN1$", re.I).sub(u"多発性内分泌腺腫症1型", text)
        text = re.compile(u"^MOF$", re.I).sub(u"多臓器不全", text)
        text = re.compile(u"^multiphasic_ADEM$", re.I).sub(u"多相性急性散在性脳脊髄炎", text)
        text = re.compile(u"^APS$", re.I).sub(u"多腺性自己免疫症候群", text)
        text = re.compile(u"^CHOP$", re.I).sub(u"多剤併用化学療法", text)
        text = re.compile(u"^FSGS$", re.I).sub(u"巣状分節性糸球体硬化症", text)
        text = re.compile(u"^FSGS$", re.I).sub(u"巣状糸球体硬化症", text)
        text = re.compile(u"^SSc$", re.I).sub(u"全身性強皮症", text)
        text = re.compile(u"^SIRS$", re.I).sub(u"全身性炎症反応症候群", text)
        text = re.compile(u"^SLE$", re.I).sub(u"全身性エリトマトーデス", text)
        text = re.compile(u"^SLE$", re.I).sub(u"全身性エリテマトーデス", text)
        text = re.compile(u"^SACI$", re.I).sub(u"選択的動脈内カルシウム注入試験", text)
        text = re.compile(u"^ASVS$", re.I).sub(u"選択的カルシウム動注後肝静脈サンプリング", text)
        text = re.compile(u"^PRCA$", re.I).sub(u"赤芽球癆", text)
        text = re.compile(u"^VTE$", re.I).sub(u"静脈血栓塞栓症", text)
        text = re.compile(u"^ARDS$", re.I).sub(u"成人呼吸窮迫症候群", text)
        text = re.compile(u"^ATL$", re.I).sub(u"成人T細胞白血病", text)
        text = re.compile(u"^ATL$", re.I).sub(u"成人T細胞リンパ腫", text)
        text = re.compile(u"^SAS$", re.I).sub(u"睡眠時無呼吸症候群_", text)
        text = re.compile(u"^SAS$", re.I).sub(u"睡眠時無呼吸症候群", text)
        text = re.compile(u"^PVE$", re.I).sub(u"人工弁心内膜炎", text)
        text = re.compile(u"^PML$", re.I).sub(u"進行性多巣性白質脳症", text)
        text = re.compile(u"^PSP$", re.I).sub(u"進行性核上性麻痺", text)
        text = re.compile(u"^NET$", re.I).sub(u"神経内分泌腫瘍", text)
        text = re.compile(u"^NPE$", re.I).sub(u"神経原性肺水腫", text)
        text = re.compile(u"^DVT$", re.I).sub(u"深部静脈血栓症", text)
        text = re.compile(u"^FFP$", re.I).sub(u"新鮮凍結血漿", text)
        text = re.compile(u"^EPS$", re.I).sub(u"心臓電気生理検査", text)
        text = re.compile(u"^UCG$", re.I).sub(u"心臓超音波検査", text)
        text = re.compile(u"^CRT$", re.I).sub(u"心臓再同期療法_", text)
        text = re.compile(u"^CTR$%$", re.I).sub(u"心拡大", text)
        text = re.compile(u"^ICD$", re.I).sub(u"植え込み型除細動器", text)
        text = re.compile(u"^ADPKD$", re.I).sub(u"常染色体優性多発性嚢胞腎", text)
        text = re.compile(u"^SMA$", re.I).sub(u"上腸間膜動脈", text)
        text = re.compile(u"^GIST$", re.I).sub(u"消化管間質腫瘍", text)
        text = re.compile(u"^SCLC$", re.I).sub(u"小細胞肺癌", text)
        text = re.compile(u"^PSD$", re.I).sub(u"周期性同期性放電", text)
        text = re.compile(u"^PNP$", re.I).sub(u"腫瘍随伴性天疱瘡", text)
        text = re.compile(u"^CEA$", re.I).sub(u"腫瘍マーカー", text)
        text = re.compile(u"^AIP$", re.I).sub(u"自己免疫性膵炎", text)
        text = re.compile(u"^AIHA$", re.I).sub(u"自己免疫性溶血性貧血", text)
        text = re.compile(u"^AITD$", re.I).sub(u"自己免疫性甲状腺疾患", text)
        text = re.compile(u"^AIH$", re.I).sub(u"自己免疫性肝炎", text)
        text = re.compile(u"^CHDF$", re.I).sub(u"持続的血液濾過透析", text)
        text = re.compile(u"^CGM$", re.I).sub(u"持続血糖測定モニター", text)
        text = re.compile(u"^CGM$", re.I).sub(u"持続血糖測定", text)
        text = re.compile(u"^NMO$", re.I).sub(u"視神経脊髄炎", text)
        text = re.compile(u"^HOT$", re.I).sub(u"在宅酸素療法", text)
        text = re.compile(u"^RPE$", re.I).sub(u"再膨張性肺水腫", text)
        text = re.compile(u"^ARVC$", re.I).sub(u"催不整脈性右室心筋症", text)
        text = re.compile(u"^LAD$", re.I).sub(u"左前下行枝", text)
        text = re.compile(u"^LVG$", re.I).sub(u"左室造影", text)
        text = re.compile(u"^LMT$", re.I).sub(u"左冠動脈主幹部", text)
        text = re.compile(u"^MCTD$", re.I).sub(u"混合性結合組織病", text)
        text = re.compile(u"^MDS$", re.I).sub(u"骨髄異形成症候群", text)
        text = re.compile(u"^RAEB-2$", re.I).sub(u"骨髄異形成症候群", text)
        text = re.compile(u"^HHS$", re.I).sub(u"高浸透圧高血糖症候群", text)
        text = re.compile(u"^HHS$", re.I).sub(u"高血糖高浸透圧症候群", text)
        text = re.compile(u"^MRHE$", re.I).sub(u"鉱質コルチコイド反応性低ナトリウム血症", text)
        text = re.compile(u"^SIADH$", re.I).sub(u"抗利尿ホルモン不適合分泌症候群", text)
        text = re.compile(u"^CTRX$", re.I).sub(u"抗生剤", text)
        text = re.compile(u"^ANCA$", re.I).sub(u"抗好中球細胞質抗体", text)
        text = re.compile(u"^SBT/ABPC$", re.I).sub(u"抗菌薬", text)
        text = re.compile(u"^ART$", re.I).sub(u"抗レトロウイルス治療", text)
        text = re.compile(u"^APS$", re.I).sub(u"抗リン脂質抗体症候群", text)
        text = re.compile(u"^HES$", re.I).sub(u"好酸球増多症候群", text)
        text = re.compile(u"^HES$", re.I).sub(u"好酸球増加症候群", text)
        text = re.compile(u"^EGPA$", re.I).sub(u"好酸球性多発血管炎肉芽腫症", text)
        text = re.compile(u"^EGPA$", re.I).sub(u"好酸球性多発血管炎性肉芽腫症", text)
        text = re.compile(u"^OCT$", re.I).sub(u"光干渉断層法", text)
        text = re.compile(u"^AIDS$", re.I).sub(u"後天性免疫不全症候群", text)
        text = re.compile(u"^後天性第VIII因子欠乏症$", re.I).sub(u"後天性血友病", text)
        text = re.compile(u"^OPLL$", re.I).sub(u"後縦靭帯骨化症", text)
        text = re.compile(u"^PEL$", re.I).sub(u"原発性滲出性リンパ腫primary_effusion_lymphoma", text)
        text = re.compile(u"^CVID$", re.I).sub(u"原発性免疫不全症候群", text)
        text = re.compile(u"^PHPT$", re.I).sub(u"原発性副甲状腺機能亢進症", text)
        text = re.compile(u"^PBC$", re.I).sub(u"原発性胆汁性肝硬変症", text)
        text = re.compile(u"^PBC$", re.I).sub(u"原発性胆汁性肝硬変", text)
        text = re.compile(u"^PSC$", re.I).sub(u"原発性硬化性胆管炎", text)
        text = re.compile(u"^MPA$", re.I).sub(u"顕微鏡的多発血管炎", text)
        text = re.compile(u"^PE$", re.I).sub(u"血漿交換療法", text)
        text = re.compile(u"^PEX$", re.I).sub(u"血漿交換", text)
        text = re.compile(u"^TMA$", re.I).sub(u"血栓性微小血管障害症", text)
        text = re.compile(u"^TMA$", re.I).sub(u"血栓性微小血管障害", text)
        text = re.compile(u"^TTP$", re.I).sub(u"血栓性血小板減少性紫斑病", text)
        text = re.compile(u"^HLH$", re.I).sub(u"血球貪食症候群", text)
        text = re.compile(u"^AITL$", re.I).sub(u"血管免疫芽球性T細胞リンパ腫", text)
        text = re.compile(u"^IVUS$", re.I).sub(u"血管内超音波", text)
        text = re.compile(u"^IVL$", re.I).sub(u"血管内大細胞型B細胞リンパ腫", text)
        text = re.compile(u"^IVL$", re.I).sub(u"血管内悪性リンパ腫", text)
        text = re.compile(u"^IVL$", re.I).sub(u"血管内リンパ腫", text)
        text = re.compile(u"^GPA$", re.I).sub(u"血管炎性肉芽腫症", text)
        text = re.compile(u"^PAN$", re.I).sub(u"結節性多発動脈炎", text)
        text = re.compile(u"^MERS$", re.I).sub(u"軽症脳炎脳症", text)
        text = re.compile(u"^PTMC$", re.I).sub(u"経皮的僧帽弁交連切開術", text)
        text = re.compile(u"^PTRA$", re.I).sub(u"経皮的腎動脈形成術", text)
        text = re.compile(u"^PCPS$", re.I).sub(u"経皮的心肺補助法", text)
        text = re.compile(u"^PCPS$", re.I).sub(u"経皮的心肺補助装置", text)
        text = re.compile(u"^PCI$", re.I).sub(u"経皮的冠動脈形成術", text)
        text = re.compile(u"^PCI$", re.I).sub(u"経皮的冠動脈ステント留置術", text)
        text = re.compile(u"^PCI$", re.I).sub(u"経皮的冠動脈インターベンション", text)
        text = re.compile(u"^RFA$", re.I).sub(u"経皮的ラジオ波焼灼術", text)
        text = re.compile(u"^PTAD$", re.I).sub(u"経皮経肝膿瘍ドレナージ", text)
        text = re.compile(u"^PTO$", re.I).sub(u"経皮経肝的静脈瘤塞栓術", text)
        text = re.compile(u"^PTGBD$", re.I).sub(u"経皮経肝胆嚢ドレナージ", text)
        text = re.compile(u"^TEE$", re.I).sub(u"経食道心エコー", text)
        text = re.compile(u"^TTE$", re.I).sub(u"経胸壁心臓超音波検査", text)
        text = re.compile(u"^TBLB$", re.I).sub(u"経気管支肺生検", text)
        text = re.compile(u"^TAE$", re.I).sub(u"経カテーテル的動脈塞栓術", text)
        text = re.compile(u"^MG$", re.I).sub(u"筋無力症", text)
        text = re.compile(u"^ALS$", re.I).sub(u"筋萎縮性側索硬化症", text)
        text = re.compile(u"^CPM$", re.I).sub(u"橋中心髄鞘崩壊症", text)
        text = re.compile(u"^SSc$", re.I).sub(u"強皮症", text)
        text = re.compile(u"^GCA$", re.I).sub(u"巨細胞性動脈炎", text)
        text = re.compile(u"^RPGN$", re.I).sub(u"急速進行性糸球体腎炎", text)
        text = re.compile(u"^APTE$", re.I).sub(u"急性肺血栓塞栓症", text)
        text = re.compile(u"^AFBN$", re.I).sub(u"急性巣状細菌性腎炎", text)
        text = re.compile(u"^APL$", re.I).sub(u"急性前骨髄球性白血病", text)
        text = re.compile(u"^ARF$", re.I).sub(u"急性腎不全", text)
        text = re.compile(u"^AKI$", re.I).sub(u"急性腎障害", text)
        text = re.compile(u"^AMI$", re.I).sub(u"急性心筋梗塞", text)
        text = re.compile(u"^ADEM$", re.I).sub(u"急性散在性脳脊髄炎", text)
        text = re.compile(u"^AML$", re.I).sub(u"急性骨髄性白血病", text)
        text = re.compile(u"^AEP$", re.I).sub(u"急性好酸球性肺炎", text)
        text = re.compile(u"^ARDS$", re.I).sub(u"急性呼吸促迫症候群", text)
        text = re.compile(u"^ARDS$", re.I).sub(u"急性呼吸窮迫症候群", text)
        text = re.compile(u"^ACS$", re.I).sub(u"急性冠症候群", text)
        text = re.compile(u"^ALL$", re.I).sub(u"急性リンパ性白血病", text)
        text = re.compile(u"^CPFE$", re.I).sub(u"気腫合併肺線維症", text)
        text = re.compile(u"^BALF$", re.I).sub(u"気管支肺胞洗浄液", text)
        text = re.compile(u"^BAL$", re.I).sub(u"気管支肺胞洗浄", text)
        text = re.compile(u"^BAE$", re.I).sub(u"気管支動脈塞栓術_", text)
        text = re.compile(u"^PCPS$", re.I).sub(u"機械的補助循環", text)
        text = re.compile(u"^ILD$", re.I).sub(u"間質性肺炎", text)
        text = re.compile(u"^SOL$", re.I).sub(u"肝内占拠性病変", text)
        text = re.compile(u"^TACE$", re.I).sub(u"肝動脈塞栓術", text)
        text = re.compile(u"^TACE$", re.I).sub(u"肝動脈化学塞栓療法", text)
        text = re.compile(u"^TACE$", re.I).sub(u"肝動脈化学塞栓術", text)
        text = re.compile(u"^HCC$", re.I).sub(u"肝細胞癌", text)
        text = re.compile(u"^SPIDDM$", re.I).sub(u"緩徐進行1型糖尿病", text)
        text = re.compile(u"^IE$", re.I).sub(u"感染性心内膜炎", text)
        text = re.compile(u"^CAD$", re.I).sub(u"寒冷凝集素症", text)
        text = re.compile(u"^CAG$", re.I).sub(u"冠動脈造影検査", text)
        text = re.compile(u"^CAG$", re.I).sub(u"冠動脈造影", text)
        text = re.compile(u"^PCI$", re.I).sub(u"冠動脈形成術", text)
        text = re.compile(u"^CABG$", re.I).sub(u"冠動脈バイパス術", text)
        text = re.compile(u"^DCM$", re.I).sub(u"拡張型心筋症", text)
        text = re.compile(u"^DWI$", re.I).sub(u"拡散強調画像", text)
        text = re.compile(u"^SPG4$", re.I).sub(u"家族性痙性対麻痺", text)
        text = re.compile(u"^FMF$", re.I).sub(u"家族性地中海熱", text)
        text = re.compile(u"^PRES$", re.I).sub(u"可逆性白質脳症", text)
        text = re.compile(u"^PRES$", re.I).sub(u"可逆性後頭葉白質脳症", text)
        text = re.compile(u"^BEP療法$", re.I).sub(u"化学療法", text)
        text = re.compile(u"^IVCF$", re.I).sub(u"下大静脈フィルター", text)
        text = re.compile(u"^MSSA$", re.I).sub(u"黄色ブドウ球菌", text)
        text = re.compile(u"^TGA$", re.I).sub(u"一過性全健忘", text)
        text = re.compile(u"^HNPCC$", re.I).sub(u"遺伝性非ポリポーシス大腸癌", text)
        text = re.compile(u"^HHT$", re.I).sub(u"遺伝性出血性毛細血管拡張症", text)
        text = re.compile(u"^HAE$", re.I).sub(u"遺伝性血管性浮腫", text)
        text = re.compile(u"^GAVE$", re.I).sub(u"胃前庭部毛細血管拡張症", text)
        text = re.compile(u"^GERD$", re.I).sub(u"胃食道逆流症", text)
        text = re.compile(u"^PTLD$", re.I).sub(u"移植後リンパ増殖性疾患", text)
        text = re.compile(u"^JCS$$", re.I).sub(u"意識障害", text)
        text = re.compile(u"^JCS_II-10$", re.I).sub(u"意識障害", text)
        text = re.compile(u"^SAT$", re.I).sub(u"亜急性甲状腺炎", text)
        text = re.compile(u"^LVFX$", re.I).sub(u"レボフロキサシン", text)
        text = re.compile(u"^PRA$", re.I).sub(u"レニン活性", text)
        text = re.compile(u"^WHO-V型$", re.I).sub(u"ループス腎炎", text)
        text = re.compile(u"^LPL$", re.I).sub(u"リンパ形質細胞性リンパ腫", text)
        text = re.compile(u"^DLST$", re.I).sub(u"リンパ球幼若化試験", text)
        text = re.compile(u"^DLST$", re.I).sub(u"リンパ球刺激試験", text)
        text = re.compile(u"^PMR$", re.I).sub(u"リウマチ性多発筋痛症", text)
        text = re.compile(u"^RFA$", re.I).sub(u"ラジオ波焼灼療法", text)
        text = re.compile(u"^MEPM$", re.I).sub(u"メロペネム", text)
        text = re.compile(u"^MTX$", re.I).sub(u"メトトレキセート", text)
        text = re.compile(u"^MTX$", re.I).sub(u"メトトレキサート", text)
        text = re.compile(u"^MRSE$", re.I).sub(u"メチシリン耐性表皮ブドウ球菌", text)
        text = re.compile(u"^MSSA$", re.I).sub(u"メチシリン感受性黄色ブドウ球菌", text)
        text = re.compile(u"^MTX$", re.I).sub(u"メソトレキセート", text)
        text = re.compile(u"^MTX$", re.I).sub(u"メソトレキサート", text)
        text = re.compile(u"^MELAS$", re.I).sub(u"ミトコンドリア病", text)
        text = re.compile(u"^MELAS$", re.I).sub(u"ミトコンドリア脳筋症", text)
        text = re.compile(u"^MMF$", re.I).sub(u"ミコフェノール酸モフェチル", text)
        text = re.compile(u"^HIT$", re.I).sub(u"ヘパリン起因性血小板減少症", text)
        text = re.compile(u"^HSP$", re.I).sub(u"ヘノッホ・シェーンライン紫斑病", text)
        text = re.compile(u"^PTU$", re.I).sub(u"プロピルチオウラシル", text)
        text = re.compile(u"^PPI$", re.I).sub(u"プロトンポンプ阻害薬", text)
        text = re.compile(u"^PSL$", re.I).sub(u"プレドニン", text)
        text = re.compile(u"^PSL$", re.I).sub(u"プレドニゾロン", text)
        text = re.compile(u"^PSL$", re.I).sub(u"プレドニゾロン", text)
        text = re.compile(u"^PZA$", re.I).sub(u"ピラジナミド", text)
        text = re.compile(u"^DPB$", re.I).sub(u"びまん性汎細気管支炎", text)
        text = re.compile(u"^DAD$", re.I).sub(u"びまん性肺胞障害", text)
        text = re.compile(u"^DLBCL$", re.I).sub(u"びまん性大細胞性B細胞性リンパ腫", text)
        text = re.compile(u"^DLBCL$", re.I).sub(u"びまん性大細胞性B細胞リンパ腫", text)
        text = re.compile(u"^DLBCL$", re.I).sub(u"びまん性大細胞型リンパ腫", text)
        text = re.compile(u"^DLBCL$", re.I).sub(u"びまん性大細胞型B細胞性リンパ腫", text)
        text = re.compile(u"^DLBCL$", re.I).sub(u"びまん性大細胞型B細胞リンパ腫", text)
        text = re.compile(u"^VB12$", re.I).sub(u"ビタミンB12", text)
        text = re.compile(u"^VCM$", re.I).sub(u"バンコマイシン", text)
        text = re.compile(u"^BRTO$", re.I).sub(u"バルーン閉塞下逆行性経静脈的塞栓術", text)
        text = re.compile(u"^B-RTO$", re.I).sub(u"バルーン下逆行性経静脈的塞栓術", text)
        text = re.compile(u"^PCP$", re.I).sub(u"ニューモシスティス肺炎", text)
        text = re.compile(u"^PCP$", re.I).sub(u"ニューモシスチス肺炎", text)
        text = re.compile(u"^TCZ$", re.I).sub(u"トシリズマブ", text)
        text = re.compile(u"^TSS$", re.I).sub(u"トキシックショック症候群", text)
        text = re.compile(u"^TEIC$", re.I).sub(u"テイコプラニン", text)
        text = re.compile(u"^CSS$", re.I).sub(u"チャーグストラウス症候群", text)
        text = re.compile(u"^MMI$", re.I).sub(u"チアマゾール", text)
        text = re.compile(u"^TTC$", re.I).sub(u"たこつぼ型心筋症", text)
        text = re.compile(u"^TAC$", re.I).sub(u"タクロリムス", text)
        text = re.compile(u"^AOSD$", re.I).sub(u"スティル病", text)
        text = re.compile(u"^HSP$", re.I).sub(u"シェーンラインヘノッホ紫斑病", text)
        text = re.compile(u"^SjS$", re.I).sub(u"シェーグレン症候群", text)
        text = re.compile(u"^SASP$", re.I).sub(u"サラゾスルファピリジン", text)
        text = re.compile(u"^ATG-G$", re.I).sub(u"サイモグロブリン", text)
        text = re.compile(u"^CMV$", re.I).sub(u"サイトメガロウイルス", text)
        text = re.compile(u"^CCE$", re.I).sub(u"コレステロール結晶塞栓症", text)
        text = re.compile(u"^CJD$", re.I).sub(u"クロイツフェルト・ヤコブ病", text)
        text = re.compile(u"^CAM$", re.I).sub(u"クラリスロマイシン", text)
        text = re.compile(u"^GBS$", re.I).sub(u"ギランバレー症候群", text)
        text = re.compile(u"^GBS$", re.I).sub(u"ギラン・バレー症候群", text)
        text = re.compile(u"^GCV$", re.I).sub(u"ガンシクロビル", text)
        text = re.compile(u"^CBZ$", re.I).sub(u"カルバマゼピン", text)
        text = re.compile(u"^OPCA$", re.I).sub(u"オリーブ・橋・小脳萎縮症", text)
        text = re.compile(u"^PMX$", re.I).sub(u"エンドトキシン吸着療法", text)
        text = re.compile(u"^PMX-DHP$", re.I).sub(u"エンドトキシン吸着療法", text)
        text = re.compile(u"^ETN$", re.I).sub(u"エタネルセプト", text)
        text = re.compile(u"^UDCA$", re.I).sub(u"ウルソデオキシコール酸", text)
        text = re.compile(u"^CHF$", re.I).sub(u"うっ血性心不全", text)
        text = re.compile(u"^SVR$", re.I).sub(u"ウイルス学的著効", text)
        text = re.compile(u"^IFX$", re.I).sub(u"インフリキシマブ", text)
        text = re.compile(u"^IFN$", re.I).sub(u"インターフェロン", text)
        text = re.compile(u"^IAS$", re.I).sub(u"インスリン自己免疫症候群", text)
        text = re.compile(u"^CSII$", re.I).sub(u"インスリン持続皮下注入療法", text)
        text = re.compile(u"^ITCZ$", re.I).sub(u"イトラコナゾール", text)
        text = re.compile(u"^ACE-I$", re.I).sub(u"アンギオテンシン変換酵素阻害薬", text)
        text = re.compile(u"^ARB$", re.I).sub(u"アンギオテンシン2受容体拮抗薬", text)
        text = re.compile(u"^AGA$", re.I).sub(u"アレルギー性肉芽腫性血管炎", text)
        text = re.compile(u"^ABPM$", re.I).sub(u"アレルギー性気管支肺真菌症", text)
        text = re.compile(u"^ABPA$", re.I).sub(u"アレルギー性気管支肺アスペルギルス症", text)
        text = re.compile(u"^APA$", re.I).sub(u"アルドステロン産生腺腫", text)
        text = re.compile(u"^APC$", re.I).sub(u"アルゴンプラズマ凝固法", text)
        text = re.compile(u"^AKA$", re.I).sub(u"アルコール性ケトアシドーシス", text)
        text = re.compile(u"^AMD$", re.I).sub(u"アミオダロン", text)
        text = re.compile(u"^ADA$", re.I).sub(u"アダリムマブ", text)
        text = re.compile(u"^AZM$", re.I).sub(u"アジスロマイシン", text)
        text = re.compile(u"^IVIg$", re.I).sub(u"γグロブリン大量療法", text)
        text = re.compile(u"^IVIg$", re.I).sub(u"γ-グロブリン静注療法", text)
        text = re.compile(u"^ICL$", re.I).sub(u"Tリンパ球減少症", text)
        text = re.compile(u"^TACE$", re.I).sub(u"transcatheter_arterial_chemoembolization", text)
        text = re.compile(u"^TSLS$", re.I).sub(u"Toxic_shock-like_syndrome", text)
        text = re.compile(u"^TSS$", re.I).sub(u"Toxic_Shock_Syndrome_", text)
        text = re.compile(u"^TSS$", re.I).sub(u"Toxic_Shock_Syndrome", text)
        text = re.compile(u"^TEN$", re.I).sub(u"toxic_epidermal_necrolysis", text)
        text = re.compile(u"^TdP$", re.I).sub(u"torsades_de_pointes", text)
        text = re.compile(u"^MMI$", re.I).sub(u"Thiamazole", text)
        text = re.compile(u"^STSS$", re.I).sub(u"Streptococcal_toxic_shock_syndrome", text)
        text = re.compile(u"^SPS$", re.I).sub(u"stiff-person症候群", text)
        text = re.compile(u"^SJS$", re.I).sub(u"Stevens-Johnson症候群", text)
        text = re.compile(u"^MSSA$", re.I).sub(u"Staphylococcus_aureus", text)
        text = re.compile(u"^SAM$", re.I).sub(u"segmental_arterial_mediolysis", text)
        text = re.compile(u"^RTX$", re.I).sub(u"Rituximab", text)
        text = re.compile(u"^RPLS$", re.I).sub(u"Reversible_Posterior_Leukoencephalopathy_syndrome", text)
        text = re.compile(u"^RS3PE$", re.I).sub(u"Remitting_Seronegative_Symmetrical_Synovitis_with_Pitting_Edema", text)
        text = re.compile(u"^PMM$", re.I).sub(u"pure_motor_monoparesis", text)
        text = re.compile(u"^PTTM$", re.I).sub(u"Pulmonary_tumor_thrombotic_microangiopathy_", text)
        text = re.compile(u"^PTTM$", re.I).sub(u"pulmonary_tumor_thrombotic_microangiopathy", text)
        text = re.compile(u"^INR$", re.I).sub(u"PT", text)
        text = re.compile(u"^PTU$", re.I).sub(u"Propylthiouracil", text)
        text = re.compile(u"^PEL$", re.I).sub(u"Primary_effusion_lymphoma", text)
        text = re.compile(u"^PSL$", re.I).sub(u"prednisolone", text)
        text = re.compile(u"^PWS$", re.I).sub(u"Prader-Willi症候群", text)
        text = re.compile(u"^PRES$", re.I).sub(u"posterior_reversible_encephalopathy_syndrome_", text)
        text = re.compile(u"^PRES$", re.I).sub(u"posterior_reversible_encephalopathy_syndrome", text)
        text = re.compile(u"^PAU$", re.I).sub(u"Penetrating_Atherosclerotic_Ulcer", text)
        text = re.compile(u"^MTX-LPD$", re.I).sub(u"MTX関連リンパ増殖性疾患", text)
        text = re.compile(u"^RAEB-2$", re.I).sub(u"MDS", text)
        text = re.compile(u"^LYG$", re.I).sub(u"lymphomatoid_granulomatosis", text)
        text = re.compile(u"^LCA$", re.I).sub(u"Littoral_cell_angioma", text)
        text = re.compile(u"^LCDD$", re.I).sub(u"Light_Chain_Deposition_Disease", text)
        text = re.compile(u"^LPZ$", re.I).sub(u"lansoprazole", text)
        text = re.compile(u"^IVL$", re.I).sub(u"Intravasucular_large_Bcell_Lymphoma", text)
        text = re.compile(u"^IVL$", re.I).sub(u"Intravascular_Lymphoma", text)
        text = re.compile(u"^IVL$", re.I).sub(u"intravascular_large_B-cell_lymphoma", text)
        text = re.compile(u"^IVR$", re.I).sub(u"interventional_radiology", text)
        text = re.compile(u"^IgG$-RD$", re.I).sub(u"IgG$関連疾患", text)
        text = re.compile(u"^HSP$", re.I).sub(u"Henoch-Sch.nlein紫斑病", text)
        text = re.compile(u"^NGSP$", re.I).sub(u"HbA1c", text)
        text = re.compile(u"^GBS$", re.I).sub(u"Guillain-Barr.症候群", text)
        text = re.compile(u"^GBS$", re.I).sub(u"Guillain-Barre症候群", text)
        text = re.compile(u"^GPA$", re.I).sub(u"granulomatosis_with_polyangiitis", text)
        text = re.compile(u"^GEM$", re.I).sub(u"Gemcitabine", text)
        text = re.compile(u"^GIST$", re.I).sub(u"gastrointestinal_stromal_tumor", text)
        text = re.compile(u"^to1$", re.I).sub(u"from1", text)
        text = re.compile(u"^EGIST$", re.I).sub(u"extragastrointestinal_stromal_tumor_", text)
        text = re.compile(u"^EBV$", re.I).sub(u"Epstein-Barr_virus", text)
        text = re.compile(u"^VCA法$", re.I).sub(u"EB-IgG抗体", text)
        text = re.compile(u"^DLBCL$", re.I).sub(u"diffuse_large_B-cell_lymphoma_", text)
        text = re.compile(u"^DLBCL$", re.I).sub(u"diffuse_large_B-cell_lymphoma", text)
        text = re.compile(u"^DLBCL$", re.I).sub(u"Diffuse_Large_B_cell_lymphoma", text)
        text = re.compile(u"^CDS$", re.I).sub(u"Crowned_dens_syndrome", text)
        text = re.compile(u"^CADM$", re.I).sub(u"clinically_amyopathic_dermatomyositis", text)
        text = re.compile(u"^CJ$", re.I).sub(u"Campylobacter_jejuni_", text)
        text = re.compile(u"^HBV$", re.I).sub(u"B型肝炎ウイルス", text)
        text = re.compile(u"^AAV$", re.I).sub(u"ANCA関連血管炎", text)
        text = re.compile(u"^SIADH$", re.I).sub(u"ADH分泌不適合症候群", text)
        text = re.compile(u"^SIADH$", re.I).sub(u"ADH不適合分泌症候群", text)
        text = re.compile(u"^AIMAH$", re.I).sub(u"ACTH非依存性大結節性副腎皮質過形成", text)
        text = re.compile(u"^IAD$", re.I).sub(u"ACTH単独欠損症", text)
        text = re.compile(u"^ABPM$", re.I).sub(u"24時間自由行動下血圧測定", text)
        text = re.compile(u"^SPIDDM$", re.I).sub(u"1型糖尿病", text)
        text = re.compile(u"^SFTS$", re.I).sub(u"重症熱性血小板減少症候群", text)
        text = re.compile(u"^RCVS$", re.I).sub(u"可逆性脳血管攣縮症候群", text)
        text = re.compile(u"^Acromegalic_myopathy_and_arthropathy$", re.I).sub(u"先端巨大性筋原性疾患および関節疾患", text)
        text = re.compile(u"^acute_biphenotypic_leukemia$", re.I).sub(u"急性白血病(二重表現型)", text)
        text = re.compile(u"^adult_T-cellleukemia_リンパ腫$", re.I).sub(u"成人T細胞白血病リンパ腫", text)
        text = re.compile(u"^aggressiveリンパ腫$", re.I).sub(u"中悪性度リンパ腫", text)
        text = re.compile(u"^Agrressive_NK-cell_leukemia$", re.I).sub(u"アグレッシブNK(ナチュラルキラー)細胞白血病", text)
        text = re.compile(u"^Asian_variant_of_intravascular_large_B-cell_リンパ腫$", re.I).sub(u"アジア変異型血管内大型B細胞リンパ腫", text)
        text = re.compile(u"^Bence_Jones型骨髄腫$", re.I).sub(u"ベンスジョーンズ型骨髄腫", text)
        text = re.compile(u"^Bickerstaff脳幹脳炎合併$", re.I).sub(u"ビッカースタッフ脳幹脳炎合併", text)
        text = re.compile(u"^breakthrough_hepatitis$", re.I).sub(u"ブレークスルー肝炎", text)
        text = re.compile(u"^B型肝炎ウイルスのreactivation$", re.I).sub(u"B型肝炎再燃", text)
        text = re.compile(u"^Capnocytophaga_gingivalis肺炎$", re.I).sub(u"キャプノサイトファガ・ジンジバリウス肺炎", text)
        text = re.compile(u"^Carney_complex$", re.I).sub(u"カーニー複合", text)
        text = re.compile(u"^Castleman's_disease$", re.I).sub(u"キャッスルマン病", text)
        text = re.compile(u"^Catastrophic_anti-phospholipid_syndrome$", re.I).sub(u"破滅的抗リン脂質症候群", text)
        text = re.compile(u"^CD20陰性Plasmablastic_リンパ腫$", re.I).sub(u"CD20陰性形質芽細胞リンパ種", text)
        text = re.compile(u"^chronic_lymphocytic_inflammation_with_pontineperivascularenhancement_responsive_to_steroids$", re.I).sub(u"クリッパーズ症候群", text)
        text = re.compile(u"^Churg-Strauss_Syndrome$", re.I).sub(u"好酸球性多発血管炎性肉芽腫症", text)
        text = re.compile(u"^congenital_myopathy_with_type1fiber_predominance$", re.I).sub(u"先天性ミオパチータイプ1繊維優位型", text)
        text = re.compile(u"^Creutzfeldt_Jakob病$", re.I).sub(u"クロイツフェルト・ヤコブ病", text)
        text = re.compile(u"^critical_illness_polyneuropathy、ギランバレー症候群$", re.I).sub(u"重篤疾患多発ニューロパチー、ギランバレー症候群", text)
        text = re.compile(u"^Crowned_dens症候群$", re.I).sub(u"頸性偽通風", text)
        text = re.compile(u"^diffuse_large_Bcell_リンパ腫$", re.I).sub(u"びまん性大細胞型B細胞性リンパ腫", text)
        text = re.compile(u"^DiffuselargeB-cell_リンパ腫$", re.I).sub(u"びまん性大細胞型B細胞性リンパ腫", text)
        text = re.compile(u"^Duchenne型筋ジストロフィー$", re.I).sub(u"デュシェンヌ型筋ジストロフィー", text)
        text = re.compile(u"^eculizumab副作用$", re.I).sub(u"エクリズマブ副作用", text)
        text = re.compile(u"^EnteropathytypeT細胞リンパ腫$", re.I).sub(u"腸管原発T細胞性リンパ腫", text)
        text = re.compile(u"^Ewing肉腫$", re.I).sub(u"ユーイング肉腫", text)
        text = re.compile(u"^Extragonadal_germ_cell_cancer_syndrome$", re.I).sub(u"性腺外胚細胞ガン症候群", text)
        text = re.compile(u"^extranodal_NK_T細胞リンパ腫$", re.I).sub(u"節外性NK T細胞リンパ腫", text)
        text = re.compile(u"^ferroportin_disease$", re.I).sub(u"フェロポーチン病", text)
        text = re.compile(u"^fingolimod副作用$", re.I).sub(u"フィンゴリモド副作用", text)
        text = re.compile(u"^Forestier病$", re.I).sub(u"フォレスティエ病", text)
        text = re.compile(u"^Furosemido副作用$", re.I).sub(u"フロセミド副作用", text)
        text = re.compile(u"^ganglioglioma$", re.I).sub(u"神経節細胞膠腫", text)
        text = re.compile(u"^Glimepiride副作用$", re.I).sub(u"グリメピリド副作用", text)
        text = re.compile(u"^GluRε2抗体陽性辺縁系脳炎$", re.I).sub(u"抗グルタミン酸受容体抗体陽性辺縁系脳炎", text)
        text = re.compile(u"^glycogenic_hepatopathy$", re.I).sub(u"グリコジェニック・ヘパトパシー", text)
        text = re.compile(u"^Guillain-_Barr.症候群$", re.I).sub(u"ギランバレー症候群", text)
        text = re.compile(u"^H._pylori感染症$", re.I).sub(u"ヘリコバクター・ピロリ感染症", text)
        text = re.compile(u"^Helicobacter_pylori感染$", re.I).sub(u"ヘリコバクター・ピロリ感染", text)
        text = re.compile(u"^Hemophagocytic_syndrome$", re.I).sub(u"血球貪食症候群", text)
        text = re.compile(u"^Histiocytic_sarcoma$", re.I).sub(u"組織球性肉腫", text)
        text = re.compile(u"^Hodgkin-like_ATLL$", re.I).sub(u"Hodgkin-like成人T細胞白血病", text)
        text = re.compile(u"^Hungtington病$", re.I).sub(u"ハンチントン病", text)
        text = re.compile(u"^Hyper_Sensitivity_Syndrom$", re.I).sub(u"過敏症症候群", text)
        text = re.compile(u"^hypertensive_brainstem_encephalopathy$", re.I).sub(u"高血圧性脳幹脳症", text)
        text = re.compile(u"^hypokalemic_myopathy$", re.I).sub(u"低カリウム血性ミオパチー", text)
        text = re.compile(u"^ICU_Acquired_Weakness合併$", re.I).sub(u"ICU発症筋力低下合併", text)
        text = re.compile(u"^Idiopathic_pleuroparenchymal_fibroelastosis$", re.I).sub(u"IPPFE", text)
        text = re.compile(u"^Idiopathic_primary_bent_spine_syndrome$", re.I).sub(u"特発性カンプトコーミア", text)
        text = re.compile(u"^IgD_myeloma$", re.I).sub(u"IgD型骨髄腫", text)
        text = re.compile(u"^IgG_H鎖Fcフラグメント病$", re.I).sub(u"IgG型H鎖Fcフラグメント病", text)
        text = re.compile(u"^indolent_myeloma$", re.I).sub(u"無痛性骨髄腫", text)
        text = re.compile(u"^Infliximab副作用$", re.I).sub(u"インフリキシマブ副作用", text)
        text = re.compile(u"^influenza$", re.I).sub(u"インフルエンザ", text)
        text = re.compile(u"^Intaravascular_リンパ腫$", re.I).sub(u"血管内リンパ腫", text)
        text = re.compile(u"^Intravascular_large_Bcell_リンパ腫$", re.I).sub(u"血管内大細胞型B細胞性リンパ腫", text)
        text = re.compile(u"^intravascular_malignant_リンパ腫tosis$", re.I).sub(u"血管内悪性リンパ腫症", text)
        text = re.compile(u"^intravasucular_large_B-cell_リンパ腫$", re.I).sub(u"血管内大細胞型B細胞性リンパ腫", text)
        text = re.compile(u"^Isolated_body_lateropulsion$", re.I).sub(u"延髄外側症候群", text)
        text = re.compile(u"^Klebsiella_pneumoniae菌血症$", re.I).sub(u"クレブシエラ・ニューモニエ菌血症", text)
        text = re.compile(u"^Large_B-cell_リンパ腫@胸壁$", re.I).sub(u"大細胞型B細胞性リンパ腫@胸壁", text)
        text = re.compile(u"^lateropulsion$", re.I).sub(u"側方突進", text)
        text = re.compile(u"^Legionella肺炎$", re.I).sub(u"レジオネラ肺炎", text)
        text = re.compile(u"^Leukoerythroblastosis$", re.I).sub(u"白赤芽球症", text)
        text = re.compile(u"^Listeria_monocytogenesis髄膜炎$", re.I).sub(u"リステリア・モノサイトゲネス感染症髄膜炎", text)
        text = re.compile(u"^Lupus_anticoagulant_hypoprothrombinemia_syndrome$", re.I).sub(u"ループスアンチコアグラント陽性・低プロトロンビン血症", text)
        text = re.compile(u"^LV_non_compaction$", re.I).sub(u"左室緻密化障害", text)
        text = re.compile(u"^Malignant_リンパ腫$", re.I).sub(u"悪性リンパ腫", text)
        text = re.compile(u"^mantle_cell_リンパ腫$", re.I).sub(u"外套細胞リンパ腫", text)
        text = re.compile(u"^Marchiafava-Bignami病$", re.I).sub(u"マルキファーバ・ビニャーミ病", text)
        text = re.compile(u"^Marginalzone_リンパ腫$", re.I).sub(u"辺縁体リンパ腫", text)
        text = re.compile(u"^MDSovertAML$", re.I).sub(u"骨髄異形性症候群発症急性骨髄白血病", text)
        text = re.compile(u"^mild_encephalitis_encephalopathy_with_a_reversible_splenial_lesion$", re.I).sub(u"可逆性の脳梁膨大部病変を伴う軽脳炎症・脳症", text)
        text = re.compile(u"^mineralcorticoid_responsive_hyponatremia_of_the_elderly$", re.I).sub(u"老人性鉱質コルチコイド反応性低Na血症", text)
        text = re.compile(u"^Mixed_cellularity_classical_Hodgkin_リンパ腫$", re.I).sub(u"混合細胞型ホジキンリンパ腫", text)
        text = re.compile(u"^MonoMAC症候群$", re.I).sub(u"MonoMAC症候群", text)
        text = re.compile(u"^Myeloid/NK前駆細胞性急性白血病$", re.I).sub(u"ミエロイドNK細胞性前駆細胞性急性白血病", text)
        text = re.compile(u"^Myeloid・NK_cell_precursor_acute_leukemia$", re.I).sub(u"ミエロイドNK細胞性前駆細胞性急性白血病", text)
        text = re.compile(u"^nesidioblastosis$", re.I).sub(u"びまん性膵ラ氏島細胞増殖症", text)
        text = re.compile(u"^ornithine_transcarbamylase欠損症$", re.I).sub(u"オルニチントランスカルバミラーゼ欠損症", text)
        text = re.compile(u"^Osler-Weber-Rendu病$", re.I).sub(u"オスラー・ウェーバー・ランデュ病", text)
        text = re.compile(u"^overwhelming_postsplenectomy_infection$", re.I).sub(u"脾臓摘出後重症感染症", text)
        text = re.compile(u"^paramalignant_effusion$", re.I).sub(u"疑似悪性胸水", text)
        text = re.compile(u"^PEComa$", re.I).sub(u"血管周囲類上皮細胞腫瘍", text)
        text = re.compile(u"^PEG-interferonα2a副作用$", re.I).sub(u"ペグインターフェロンα2a副作用", text)
        text = re.compile(u"^peginterferonα2b+ribavirin副作用$", re.I).sub(u"ペグインターフェロンα2b及びリバビリン", text)
        text = re.compile(u"^plasma_cell_dyscrasia$", re.I).sub(u"プラズマ細胞増殖症", text)
        text = re.compile(u"^Plasmablastic_リンパ腫$", re.I).sub(u"形質芽球性リンパ腫", text)
        text = re.compile(u"^post-infectious_glomerulonephritis$", re.I).sub(u"感染後糸球体腎炎", text)
        text = re.compile(u"^Pretibial_myxedema$", re.I).sub(u"前脛骨粘液水腫", text)
        text = re.compile(u"^Pre-播種性血管内凝固症候群$", re.I).sub(u"前播種性血管内凝固症候群", text)
        text = re.compile(u"^Primaryアミロイドーシス$", re.I).sub(u"原発性アミロイド症", text)
        text = re.compile(u"^Protein-energy_malnutrition$", re.I).sub(u"タンパク質エネルギー栄養障害", text)
        text = re.compile(u"^pseudoangiosarcomatous_carcinoma$", re.I).sub(u"外陰部腺様扁平上皮癌", text)
        text = re.compile(u"^Pulmonary_tumor_thrombotic_microangiopathy_$", re.I).sub(u"微小肺動脈腫瘍塞栓", text)
        text = re.compile(u"^pulseless_electrical_activity$", re.I).sub(u"無脈性電気活動", text)
        text = re.compile(u"^Radiation-related_heart_disease$", re.I).sub(u"放射性誘発性心疾患", text)
        text = re.compile(u"^Refeeding症候群$", re.I).sub(u"リフィーディング症候群", text)
        text = re.compile(u"^Remitting_Seronegative_Symmetrical_Synovitis_with_Pitting_Edema$", re.I).sub(u"RS3PE症候群", text)
        text = re.compile(u"^Renal_Salt_Wasting$", re.I).sub(u"腎塩類喪失症", text)
        text = re.compile(u"^Reversible_Posterior_Leukoencepalopathysyndrome$", re.I).sub(u"可逆性後頭葉白質脳症", text)
        text = re.compile(u"^S._maltophilia出血性肺炎$", re.I).sub(u"ステノトロホモナス・マルトフィリア出血性肺炎", text)
        text = re.compile(u"^segmental_arterial_mediolysis$", re.I).sub(u"動脈中膜壊死", text)
        text = re.compile(u"^septic_pulmonary_emboli$", re.I).sub(u"敗血症性肺塞栓", text)
        text = re.compile(u"^septic_pulmonary_embolism$", re.I).sub(u"敗血症性肺塞栓症", text)
        text = re.compile(u"^Sj.gren症候群合併$", re.I).sub(u"シェーグレン症候群合併", text)
        text = re.compile(u"^Spironolactone副作用$", re.I).sub(u"スピロノラクトン副作用", text)
        text = re.compile(u"^Subcutaneous_panniculitis-like_T細胞リンパ腫$", re.I).sub(u"皮下蜂巣織炎様T細胞リンパ腫", text)
        text = re.compile(u"^sunitinib副作用$", re.I).sub(u"スニチニブ副作用", text)
        text = re.compile(u"^Sweet病様皮疹$", re.I).sub(u"スウィート病様皮疹", text)
        text = re.compile(u"^systemic_sclerosis_sine_scleroderma$", re.I).sub(u"皮膚硬化を伴わない全身性強皮症", text)
        text = re.compile(u"^systemicIgG4-related_plasmacytic_syndrome$", re.I).sub(u"全身性IgG4関連形質細胞症候群", text)
        text = re.compile(u"^T_NK-cell_リンパ腫$", re.I).sub(u"ナチュラルキラーT細胞リンパ腫", text)
        text = re.compile(u"^T-cell/histiocyte_rich_large_B-cell_リンパ腫$", re.I).sub(u"T細胞/組織球に富む大型B細胞リンパ腫", text)
        text = re.compile(u"^Tcell_リンパ腫$", re.I).sub(u"T細胞リンパ腫", text)
        text = re.compile(u"^Triamteren副作用$", re.I).sub(u"トリアムテレン副作用", text)
        text = re.compile(u"^Tubulointerstitial_Nephritis_with_Uveitis$", re.I).sub(u"急性尿細管質性腎炎", text)
        text = re.compile(u"^Virchow-Robin腔$", re.I).sub(u"ウィルヒョー・ロバン腔", text)
        text = re.compile(u"^volume_overload$", re.I).sub(u"体液過剰", text)
        text = re.compile(u"^Y.enterocolitica感染$", re.I).sub(u"エルシニア・エンテロコリティカ感染", text)
        text = re.compile(u"^肝多発性solitary_fibrous_tumor$", re.I).sub(u"肝多発性孤立性線維性腫瘍", text)
        text = re.compile(u"^肝転移・S53cm単発$", re.I).sub(u"肝転移・S53cm単発", text)
        text = re.compile(u"^肝門部paraganglioma$", re.I).sub(u"肝門部傍神経節腫", text)
        text = re.compile(u"^急性骨髄性白血病_with_multilineage_dysplasia$", re.I).sub(u"多血球系異形成を伴う急性骨髄性白血病", text)
        text = re.compile(u"^骨髄原発composite_リンパ腫$", re.I).sub(u"骨髄原発混合リンパ腫", text)
        text = re.compile(u"^骨髄原発smalllymphocyticリンパ腫$", re.I).sub(u"骨髄原発小リンパ球性リンパ腫", text)
        text = re.compile(u"^食道Web$", re.I).sub(u"食堂狭窄", text)
        text = re.compile(u"^肺Actinomyces$", re.I).sub(u"肺放線菌", text)
        text = re.compile(u"^非持続性wideQRS規則的頻拍$", re.I).sub(u"非持続性ワイドQRS規則的頻拍", text)
        text = re.compile(u"^Sj_gren症候群$", re.I).sub(u"シェーグレン症候群", text)
        text = re.compile(u"^Fusobacterium_varium感染症$", re.I).sub(u"フソバクテリウム-バリウム", text)
        text = re.compile(u"^polymicrobial_bacteremia$", re.I).sub(u"複数菌菌血症", text)
        text = re.compile(u"^Mycobacterium_tuberculosisによる感染性肺嚢胞$", re.I).sub(u"結核菌による感染性肺ほう胞", text)
        text = re.compile(u"^Pneumocystis_jirovecii感染症$", re.I).sub(u"ニューモシスチス肺炎感染症", text)
        text = re.compile(u"^Stiff_person_syndrome$", re.I).sub(u"スティッフパーソン症候群", text)
        text = re.compile(u"^Guillain-Barr症候群$", re.I).sub(u"ギランバレー症候群", text)
        text = re.compile(u"^2次性Composite_リンパ腫$", re.I).sub(u"2次性複合リンパ腫", text)
        text = re.compile(u"^骨髄異形成症候群5q-syndrome$", re.I).sub(u"骨髄異形成症候群5q-症候群", text)
        text = re.compile(u"^Guillain-_Barr症候群$", re.I).sub(u"ギランバレー症候群", text)
        text = re.compile(u"^大腿骨原発diffuse_large_B-cellリンパ腫$", re.I).sub(u"大腿骨原発びまん性大細胞型B細胞性リンパ腫", text)
        text = re.compile(u"^L_ffler心内膜心筋炎$", re.I).sub(u"レフラー心内膜心筋炎", text)
        text = re.compile(u"^Streptococcus_pyogenes感染症$", re.I).sub(u"A群溶血性レンサ球菌感染症", text)
        text = re.compile(u"^Mycobacterium_peregrinum感染症$", re.I).sub(u"マイコバクテリウム・ペレグリナム感染症", text)
        text = re.compile(u"^senileEBV-associated_lymphoproliferative_disorder_polymorphic_variant$", re.I).sub(u"加齢性EBウィルス関連リンパ増殖性疾患一塩基多型変異体", text)
        text = re.compile(u"^Guillain_Barr症候群合併$", re.I).sub(u"ギランバレー症候群合併", text)
        text = re.compile(u"^Gerstmann-Str_ussler-Scheinker病$", re.I).sub(u"ゲルストマン・ストロイスラー・シャインカー病", text)
        text = re.compile(u"^ゲルストマン・ストロイスラー・シャインカー病$", re.I).sub(u"胃体部癌cT4aN3M1Stage_IV", text)
        text = re.compile(u"^胃体部癌cT4aN3M1Stage_IV$", re.I).sub(u"胃体部癌cT4aN3M1ステージ4", text)
        text = re.compile(u"^Clostridium_difficile感染症$", re.I).sub(u"クロストリジウム・ディフィシル感染症", text)
        text = re.compile(u"^気管web$", re.I).sub(u"気管支狭窄", text)
        text = re.compile(u"^Henoch-Sch_enlein_Purpura$", re.I).sub(u"ヘノッホ・シェーンライン紫斑病", text)
        text = re.compile(u"^Varicella-Zoster_Virus再帰感染症$", re.I).sub(u"水痘帯状疱疹ウィルス再帰感染症", text)
        text = re.compile(u"^消化管間質腫瘍@胃@脾&消化管間質腫瘍@Littoral_cell_angioma@脾$", re.I).sub(u"消化管間質腫瘍@胃@脾&消化管間質腫瘍@沿岸細胞血管腫@脾", text)
        text = re.compile(u"^Sj_gren症候群合併$", re.I).sub(u"シェーグレン症候群合併", text)
        text = re.compile(u"^シェーグレン症候群合併$", re.I).sub(u"神経Beh_et病", text)
        text = re.compile(u"^神経Beh_et病$", re.I).sub(u"神経ベーチェット病", text)
        text = re.compile(u"^Stanford_B型急性大動脈解離$", re.I).sub(u"スタンフォードB型急性大動脈解離", text)
        text = re.compile(u"^アミオダロン-induced-thyrotoxicosis$", re.I).sub(u"アミオダロン誘発性甲状腺中毒症", text)
        text = re.compile(u"^L_ffler症候群$", re.I).sub(u"レフラー症候群", text)
        text = re.compile(u"^Brown-S_quard症候群$", re.I).sub(u"ブラウン・セカール症候群", text)
        text = re.compile(u"^Alstr_m症候群$", re.I).sub(u"アルストローム症候群", text)
        text = re.compile(u"^リンパ形質細胞性リンパ腫・Waldenstronマクログロブリン血症$", re.I).sub(u"リンパ形質細胞性リンパ腫・ワルデンストレームマクログロブリン血症", text)
        text = re.compile(u"^Streptococcus_bovis感染症$", re.I).sub(u"ストレプトコッカスボビス感染症", text)
        text = re.compile(u"^Malignantリンパ腫,B-cell_type$", re.I).sub(u"悪性リンパ腫、B細胞性", text)
        text = re.compile(u"^neuro-psychiatric_全身性エリテマトーデス$", re.I).sub(u"精神神経性全身性エリテマトーデス", text)
        text = re.compile(u"^platypnea-orthodeoxia_syndrome$", re.I).sub(u"プラプチネア、オルソデオキシア症候群", text)
        text = re.compile(u"^Pulmonaryhyalinizinggranuloma$", re.I).sub(u"Pulmonary hyalinizing granuloma", text)
        text = re.compile(u"^Rendu-Osler-Weber症候群$", re.I).sub(u"ランデュ・オスラー・ウェーバー症候群", text)
        text = re.compile(u"^ランデュ・オスラー・ウェーバー症候群$", re.I).sub(u"Valsalva洞動脈瘤破裂", text)
        text = re.compile(u"^Valsalva洞動脈瘤破裂$", re.I).sub(u"バルサルバ洞動脈瘤破裂", text)
        text = re.compile(u"^Protein_C欠損症$", re.I).sub(u"プロテインC欠損症", text)
        text = re.compile(u"^Budd-Chiari症候群$", re.I).sub(u"バッド・キアリ症候群", text)
        text = re.compile(u"^May_Thurner症候群$", re.I).sub(u"メイ・ターナー症候群", text)
        text = re.compile(u"^Idiopathic_chylopericardium$", re.I).sub(u"特発性乳糜心膜症", text)
        text = re.compile(u"^mitochondria遺伝子3243変異$", re.I).sub(u"ミトコンドリア遺伝子3243変異", text)
        text = re.compile(u"^ミトコンドリア遺伝子3243変異$", re.I).sub(u"VTストーム", text)
        text = re.compile(u"^bevacizumab副作用$", re.I).sub(u"ベバシズマブ副作用", text)
        text = re.compile(u"^Nocardia_farcinica感染症$", re.I).sub(u"ノカルジア・ファルシニカ感染症", text)
        text = re.compile(u"^血管型Ehlers-Danlos症候群$", re.I).sub(u"血管型エーラス・ダンロス症候群", text)
        text = re.compile(u"^Wallenberg症候群合併$", re.I).sub(u"ワレンベルグ症候群合併", text)
        text = re.compile(u"^Campylobacter_jejuni腸炎$", re.I).sub(u"カンピロバクター・ジェジュニ腸炎", text)
        text = re.compile(u"^Strawberry_pickers&#039;_palsy$", re.I).sub(u"ストロベリーピッカー麻痺", text)
        text = re.compile(u"^Mallory-Weiss症候群合併$", re.I).sub(u"マロリー・ワイス症候群合併", text)
        text = re.compile(u"^Rheumatoidleptomeningitis$", re.I).sub(u"リウマチ性軟脳膜炎", text)
        text = re.compile(u"^Wernicke_Korsakoff症候群$", re.I).sub(u"ウェルニッケ・コルサコフ症候群", text)
        text = re.compile(u"^Birt-Hogg-Dub症候群$", re.I).sub(u"バート・ホッグ・デュべ症候群", text)
        text = re.compile(u"^腸管型Behcet_disease$", re.I).sub(u"腸管型ベーチェット病", text)
        text = re.compile(u"^trisomy8陽性myelodysplastic_syndromes$", re.I).sub(u"トリソミー8陽性骨髄異形性症候群", text)
        text = re.compile(u"^peribiliary_cysts$", re.I).sub(u"胆管周囲嚢胞", text)
        text = re.compile(u"^Mixed_acinar-endocrine_carcinoma$", re.I).sub(u"混合型内分泌腺房癌", text)
        text = re.compile(u"^Edwardsiella_tarda肺炎$", re.I).sub(u"エドワジェラ・タルダ肺炎", text)
        text = re.compile(u"^Helicobacter_cinaedi菌血症$", re.I).sub(u"ヘリコバクター・シネディ菌血症", text)
        text = re.compile(u"^Corynebacterium_urealyticum尿路感染症$", re.I).sub(u"コリネバクテリウム・ウレアリティクム尿路感染症", text)
        text = re.compile(u"^Re-feeding症候群$", re.I).sub(u"リフィーディング症候群", text)
        text = re.compile(u"^Marchiafava_Bignami病$", re.I).sub(u"マルキアファーバ・ビニャーミ病", text)
        text = re.compile(u"^rt-PA療法副作用$", re.I).sub(u"rt-PA療法副作用", text)
        text = re.compile(u"^Sturge-Weber症候群$", re.I).sub(u"スタージ・ウェーバー症候群", text)
        text = re.compile(u"^Menetrier病$", re.I).sub(u"メネトリエ病", text)
        text = re.compile(u"^Hepatic_pseudoリンパ腫$", re.I).sub(u"肝臓偽リンパ腫", text)
        text = re.compile(u"^Granulocyte_Colony_Stimulating_Factor_産生腫瘍$", re.I).sub(u"顆粒球コロニー刺激因子産生腫瘍", text)
        text = re.compile(u"^Valsalva洞動脈瘤$", re.I).sub(u"バルサルバ洞動脈瘤", text)
        text = re.compile(u"^膵Solid_pseudopapillaryneoplasm$", re.I).sub(u"膵臓固形仮性乳頭腫瘍", text)
        text = re.compile(u"^Collet-Sicard症候群$", re.I).sub(u"コレー・シカール症候群", text)
        text = re.compile(u"^大腸diffuse_large_B_cell_リンパ腫$", re.I).sub(u"大腸びまん性大細胞型B細胞性リンパ腫", text)
        text = re.compile(u"^Systemic_lupuserythematous$", re.I).sub(u"全身性エリテマトーデス", text)
        text = re.compile(u"^VTstorm$", re.I).sub(u"VTstorm", text)
        text = re.compile(u"^Groove膵癌$", re.I).sub(u"Groove膵癌", text)
        text = re.compile(u"^Waldenstr_m&#039;s_macroglobulinemia$", re.I).sub(u"ワルデンシュトレームマクログロブリン血症", text)
        text = re.compile(u"^Nocardia_asteroides感染症$", re.I).sub(u"ノカルジア・アステロイデス感染症", text)
        text = re.compile(u"^Supragastric_Belch$", re.I).sub(u"胃に由来しないげっぷ", text)
        text = re.compile(u"^Moraxella_catarrhalis感染症$", re.I).sub(u"モラクセラ・カタラーリス感染症", text)
        text = re.compile(u"^ペニシリナーゼ非産生S.aureusによる胸骨骨髄炎$", re.I).sub(u"ペニシリナーゼ非産生黄色ブドウ球菌による胸骨骨髄炎", text)
        text = re.compile(u"^trisomy8陽性非骨髄異形成症候群$", re.I).sub(u"トリソミー8陽性非骨髄異形成症候群", text)
        text = re.compile(u"^Ketosis-prone_type2diabetes$", re.I).sub(u"Ketosis-prone_type2diabetes", text)
        text = re.compile(u"^Guillain-Barr_syndrome$", re.I).sub(u"ギラン・バレー症候群", text)
        text = re.compile(u"^Good症候群合併赤芽球癆$", re.I).sub(u"グッド症候群合併赤芽球癆", text)
        text = re.compile(u"^骨髄異形成症候群_overt_leukemia$", re.I).sub(u"骨髄異形成症候群から発症した白血病", text)
        text = re.compile(u"^Henoch-Sch_enlein紫斑病$", re.I).sub(u"ヘノッホ・シェーンライン紫斑病", text)
        text = re.compile(u"^Senile_EBウイルス_associated_B-cell_lymphoproliferative_disorder$", re.I).sub(u"老人性EBウィルス関連のB細胞リンパ腫疾患", text)
        text = re.compile(u"^post_staphylococcal_infection_Henoch-_Sch_nlein紫斑病$", re.I).sub(u"ブドウ球菌感染症後 ヘノッホ・シェーンライン紫斑病", text)
        text = re.compile(u"^プロテインC異常症type2$", re.I).sub(u"プロテインC異常症2型", text)
        text = re.compile(u"^マクロCK_type1$", re.I).sub(u"マクロCK1型", text)
        text = re.compile(u"^L_fgren症候群$", re.I).sub(u"ロフグレン症候群", text)
        text = re.compile(u"^Sarcoid_myopathy$", re.I).sub(u"サルコイドミオパチー", text)
        text = re.compile(u"^脾原発_histiocytic_sarcoma$", re.I).sub(u"脾原発組織球性肉腫", text)
        text = re.compile(u"^Mature_B-cell_neoplasm$", re.I).sub(u"成熟B細胞腫瘍", text)
        text = re.compile(u"^Mikulicz症候群$", re.I).sub(u"ミクリッツ症候群", text)
        text = re.compile(u"^Age-relatedEBV-associated_B-cell_lymphoproliferative_disorder$", re.I).sub(u"加齢変化性EBV関連B型細胞リンパ増殖性疾患", text)
        text = re.compile(u"^reverseseroconversion$", re.I).sub(u"Reverse_Seroconversion", text)
        text = re.compile(u"^Henoch-Sch_nlein紫斑病$", re.I).sub(u"ヘノッホ・シェーンライン紫斑病", text)
        text = re.compile(u"^若年性parkinsonism$", re.I).sub(u"若年性パーキンソン症", text)
        text = re.compile(u"^Subcutaneouspanniculitis-likeT-cellリンパ腫$", re.I).sub(u"皮下脂肪織炎様T細胞リンパ腫", text)
        text = re.compile(u"^T-cell/histiocyte_rich_large_B-cell_リンパ腫$", re.I).sub(u"T細胞/高組織球性大型B細胞リンパ腫", text)
        text = re.compile(u"^T_blastic_crisis$", re.I).sub(u"T芽球性クリーゼ", text)
        text = re.compile(u"^B型肝炎ウイルス_reverse_seroconversion$", re.I).sub(u"B型肝炎ウイルス回復セロコンバージョン", text)
        text = re.compile(u"^Polyglandular_autoimmune_type3$", re.I).sub(u"多腺性自己免疫性症候群3型", text)
        text = re.compile(u"^IgGλ型monoclonalgammopathy$", re.I).sub(u"IgG_λ型単クローン性免疫グロブリン血症", text)
        text = re.compile(u"^Sjorgren症候群$", re.I).sub(u"シェーグレン症候群", text)
        text = re.compile(u"^Bacillus_cereus敗血症$", re.I).sub(u"バチルス・セレウス敗血症", text)
        text = re.compile(u"^VitB12欠乏症$", re.I).sub(u"ビタミンB12欠乏症", text)
        text = re.compile(u"^EBウイルスーpositive_T-cell_lymphoproliferative_disorders_of_childhood$", re.I).sub(u"EBウイルスー幼年性陽性T細胞型リンパ増殖性疾患", text)
        text = re.compile(u"^Klebsiella感染症$", re.I).sub(u"クレブシエラ感染症", text)
        text = re.compile(u"^Rathke嚢胞内出血$", re.I).sub(u"ラトケ嚢胞内出血", text)
        text = re.compile(u"^直腸mucosa-associated_lymphoid_tissue_リンパ腫$", re.I).sub(u"直腸粘膜内リンパ組織性リンパ腫", text)
        text = re.compile(u"^Campylobacterjejuni菌血症$", re.I).sub(u"カンピロバクター・ジェジュニ菌血症", text)
        text = re.compile(u"^Vit.B1欠乏症$", re.I).sub(u"ビタミンB1欠乏症", text)
        text = re.compile(u"^Chlamydia_pneumoniae感染症$", re.I).sub(u"クラミジア肺炎病原体感染症", text)
        text = re.compile(u"^Ph染色体陽性acute_biphenotypic_leukemia$", re.I).sub(u"Ph染色体陽性急性混合白血病", text)
        text = re.compile(u"^Klebsiella_pneumoniae髄膜脳炎$", re.I).sub(u"クレブシエラ肺炎病原体髄膜脳炎", text)
        text = re.compile(u"^Sch_nlein-Henoch紫斑病$", re.I).sub(u"シェーンライン・ヘノッホ紫斑病", text)
        text = re.compile(u"^Hodgkin_リンパ腫$", re.I).sub(u"ホジキンリンパ腫", text)
        text = re.compile(u"^Multicentric_CastlemanDisease$", re.I).sub(u"多中心性キャッスルマン病", text)
        text = re.compile(u"^結節性硬化型Hodgikinリンパ腫$", re.I).sub(u"結節性硬化型ホジキンリンパ腫", text)
        text = re.compile(u"^Y.enterocolitica感染症$", re.I).sub(u"エルシニア・エンテロコリチカ菌感染症", text)
        text = re.compile(u"^慢性骨髄性白血病_lymphnodalblast_crisis$", re.I).sub(u"慢性骨髄性白血病_リンパ節急性転化", text)
        text = re.compile(u"^Xanthogranuloma$", re.I).sub(u"黄色肉芽腫", text)
        text = re.compile(u"^Munchausen症候群$", re.I).sub(u"ミュンヒハウゼン症候群", text)
        text = re.compile(u"^原発性胆汁性肝硬変症-自己免疫性肝炎_overlap_syndrome$", re.I).sub(u"原発性胆汁性肝硬変症-自己免疫性肝炎オーバーラップ症候群", text)
        text = re.compile(u"^HTLV-1associated_myelopathy$", re.I).sub(u"HTLV-1関連脊髄症", text)
        text = re.compile(u"^Chronic_Lymphocytic_Inflammation_with_Pontine_Perivascular_Enhancement_Responsive_toSteroids$", re.I).sub(u"ステロイド反応による脳橋血管周囲拡張の慢性リンパ球性炎症", text)
        text = re.compile(u"^aceruloplasminemia$", re.I).sub(u"無セルロプラスミン血症", text)
        text = re.compile(u"^核酸アナログ製剤・Peg-IFNα2a$", re.I).sub(u"核酸アナログ製剤・ペグインターフェロンα2a", text)
        text = re.compile(u"^Peg-IFNα2a$", re.I).sub(u"ペグインターフェロンα2a", text)
        text = re.compile(u"^MEN_type1$", re.I).sub(u"多発性内分泌腺腫症1型", text)
        text = re.compile(u"^HairyB-cell_lymphoproliferative_disorder$", re.I).sub(u"有毛B細胞型リンパ腫疾患", text)
        text = re.compile(u"^Hepatosplenicγδ_T細胞リンパ腫$", re.I).sub(u"肝脾γδT細胞リンパ腫", text)
        text = re.compile(u"^Vit.D欠乏症$", re.I).sub(u"ビタミンD欠乏症", text)
        text = re.compile(u"^Waldenstr_m_macroglobulin血症$", re.I).sub(u"ワルデンシュトレームマクログロブリン血症", text)
        text = re.compile(u"^Littoral_cell_angioma@脾$", re.I).sub(u"堤防細胞血管腫@脾", text)


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
            if not judge_cython:
                text_new=self.replace_by_hidemaru(text_new)

            else:
                text_new=replacement.replace_by_hidemaru(text_new)

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

        response=FormatText(**kwargs).main(
            path_input=kwargs['path_input'],
            path_output=kwargs['path_output'],
            path_blacklist=kwargs['path_blacklist'],
            judge_cython=kwargs['cython']
        )

    elif kwargs['keyword']:
        # 2.単語のテストをする場合

        for keyword in kwargs['keyword'].split(','):

            text_modified=FormatText(**kwargs).replace_by_regx(
                text=keyword
            )

            text_modified=FormatText(**kwargs).replace_by_hidemaru(
                text=text_modified
            )

            if u"＆" in text_modified:
                text_modified = text_modified.split(u"＆")

            print('%s => %s' %(keyword,text_modified))
