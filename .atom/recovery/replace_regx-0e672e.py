def replace_by_regx(ds):
    ds = self.replace_side_effects(ds)

    ds.replace(u"【正：(.*?)】", u"\\1", regex=True, inplace=True)

    # ds = self.exclude_brackets(ds)
    ds = self.exclude_stars(ds)

    ds.replace(u"h;", u"H:", inplace=True)
    ds.replace(u"Ｈ；", u"Ｈ：", inplace=True)
    ds.replace(u"／高値", u"／上昇", inplace=True)
    ds.replace(u"／低値", u"／低下", inplace=True)
    ds.replace(u"】", u"］", inplace=True)
    ds.replace(u"【", u"［", inplace=True)
    ds.replace(u"〔", u"［", inplace=True)
    ds.replace(u"〕", u"］", inplace=True)
    ds.replace(u"([＠＝／・：])[^［]*［解釈：", u"", inplace=True, regex=True)
    ds.replace(u"血液＝", u"", inplace=True)
    ds.replace(u"血清＝", u"", inplace=True)
    ds.replace(u"尿＝", u"尿", inplace=True)
    ds.replace(u"\n　", u"\n", inplace=True)
    ds.replace(u".*［解釈：([^］]*)].*", u"\1", inplace=True, regex=True)
    ds.replace(u".*［解釈：([^］]*)］.*", u"\1", inplace=True, regex=True)
    ds.replace(u"／／", u"／", inplace=True)
    ds.replace(u"　／", u"／", inplace=True)
    ds.replace(u"^wbc/", u"白血球/", inplace=True)
    ds.replace(u"^plt/", u"血小板/", inplace=True)
    ds.replace(u"^rbc/", u"赤血球/", inplace=True)
    ds.replace(u"^hb/", u"赤血球/", inplace=True)
    ds.replace(u"^hb/", u"赤血球/", inplace=True)
    ds.replace(u"^ht/", u"赤血球/", inplace=True)
    ds.replace(u"^got/", u"AST/", inplace=True)
    ds.replace(u"^gpt/", u"ALT/", inplace=True)
    ds.replace(u"^tp/", u"蛋白/", inplace=True)
    ds.replace(u"^cre/", u"クレアチニン/", inplace=True)
    ds.replace(u"^cr/", u"クレアチニン/", inplace=True)
    ds.replace(u"^neutro/", u"好中球/", inplace=True)
    ds.replace(u"^lymph/", u"リンパ球/", inplace=True)
    ds.replace(u"^k/", u"カリウム/", inplace=True)
    ds.replace(u"^na/", u"ナトリウム/", inplace=True)
    ds.replace(u"ＡＦＰ／高値", u"ＡＦＰ／上昇", inplace=True)
    ds.replace(u"ＡＮＡ／上昇", u"ＡＮＡ／陽性", inplace=True)
    ds.replace(u"ＣＲＰ／高値", u"ＣＲＰ／上昇", inplace=True)
    ds.replace(u"Ｃ−ペプチド／低下", u"Ｃペプチド／低下", inplace=True)
    ds.replace(u"Ｄ−ダイマ−／上昇", u"Ｄダイマ−／上昇", inplace=True)
    ds.replace(u"ＦＧＦ−２３／上昇", u"ＦＧＦ２３／上昇", inplace=True)
    ds.replace(u"Ｆ−Ｔ３／上昇", u"ＦＴ３／上昇", inplace=True)
    ds.replace(u"Ｆ−Ｔ４／上昇", u"ＦＴ４／上昇", inplace=True)
    ds.replace(u"Ｆ−Ｔ４／低下", u"ＦＴ４／低下", inplace=True)
    ds.replace(u"ＨｂＡ１ｃ／高値", u"ＨｂＡ１ｃ／上昇", inplace=True)
    ds.replace(u"ＨＢｓ−Ａｂ／陰性", u"ＨＢｓＡｂ／陰性", inplace=True)
    ds.replace(u"ＨＢｓ−Ａｇ／陽性", u"ＨＢｓＡｇ／陽性", inplace=True)
    ds.replace(u"ＨＣＯ３／低下", u"ＨＣＯ３−／低下", inplace=True)
    ds.replace(u"ＨＣＶＡｂ／陰性", u"ＨＣＶ抗体／陰性", inplace=True)
    ds.replace(u"ＨＣＶ−Ａｂ／陰性", u"ＨＣＶ抗体／陰性", inplace=True)
    ds.replace(u"ＨＤＬ−Ｃ／低下", u"ＨＤＬ／低下", inplace=True)
    ds.replace(u"ＩＧＦ−１／上昇", u"ＩＧＦ−Ｉ／上昇", inplace=True)
    ds.replace(u"ＩＧＦ−１／低下", u"ＩＧＦ−Ｉ／低下", inplace=True)
    ds.replace(u"ｉｎｔａｃｔ＿ＰＴＨ／上昇", u"ｉｎｔａｃｔＰＴＨ／上昇",
               inplace=True)
    ds.replace(u"ｉｎｔａｃｔ＿ＰＴＨ／正常", u"ｉｎｔａｃｔＰＴＨ／正常",
               inplace=True)
    ds.replace(u"ｉｎｔａｃｔ＿ＰＴＨ／低下", u"ｉｎｔａｃｔＰＴＨ／低下",
               inplace=True)
    ds.replace(u"ＩＮＴＡＣＴ−ＰＴＨ／上昇", u"ｉｎｔａｃｔＰＴＨ／上昇",
               inplace=True)
    ds.replace(u"ＬＤ／上昇", u"ＬＤＨ／上昇", inplace=True)
    ds.replace(u"ＰＩＶＫＡ−２／上昇", u"ＰＩＶＫＡ−ＩＩ／上昇", inplace=True)
    ds.replace(u"Ｔ．Ｂｉｌ／上昇", u"Ｔ−ｂｉｌ／上昇", inplace=True)
    ds.replace(u"Ｔ−ｃｈｏｌ／上昇", u"Ｔ−Ｃｈｏ／上昇", inplace=True)
    ds.replace(u"Ｔｇ−Ａｂ／上昇", u"ＴｇＡｂ／上昇", inplace=True)
    ds.replace(u"ＴＰＯＡｂ／上昇", u"ＴＰＯＡｂ／陽性", inplace=True)
    ds.replace(u"ＴＲＡｂ／上昇", u"ＴＲＡｂ／陽性", inplace=True)
    ds.replace(u"γ−Ｇ蛋白／上昇", u"γＧ蛋白／上昇", inplace=True)
    ds.replace(u"γ−Ｇ蛋白／正常", u"γＧ蛋白／正常", inplace=True)
    ds.replace(u"フェリチン値／上昇", u"フェリチン／上昇", inplace=True)
    ds.replace(u"レニン活性／低下", u"レニン／低下", inplace=True)
    ds.replace(u"意識レベル／低下", u"意識／低下", inplace=True)
    ds.replace(u"異形リンパ球／陽性", u"異型リンパ球／陽性", inplace=True)
    ds.replace(u"炎症／上昇", u"炎症反応／上昇", inplace=True)
    ds.replace(u"炎症所見／陰性", u"炎症反応／陰性", inplace=True)
    ds.replace(u"炎症所見／上昇", u"炎症反応／上昇", inplace=True)
    ds.replace(u"炎症反応／陽性", u"炎症反応／上昇", inplace=True)
    ds.replace(u"芽球／上昇", u"芽球／陽性", inplace=True)
    ds.replace(u"血液ガス分析＝ＨＣＯ３／低下", u"血液ガス＝ＨＣＯ３−／低下",
               inplace=True)
    ds.replace(u"血液ガス分析＝ｐＨ／低下", u"血液ガス＝ｐＨ／低下", inplace=True)
    ds.replace(u"血液ガス分析＝ｐＯ２／低下", u"血液ガス＝ＰａＣＯ２／低下",
               inplace=True)
    ds.replace(u"血小板／低下", u"血小板／減少", inplace=True)
    ds.replace(u"血小板数／正常", u"血小板／正常", inplace=True)
    ds.replace(u"血小板数／低下", u"血小板／低下", inplace=True)
    ds.replace(u"血清ＡＣＥ／上昇", u"ＡＣＥ／上昇", inplace=True)
    ds.replace(u"血清ＩｇＧ４／上昇", u"ＩｇＧ４／上昇", inplace=True)
    ds.replace(u"血清ＩＬ−６／上昇", u"ＩＬ−６／上昇", inplace=True)
    ds.replace(u"血清Ｋ／低下", u"Ｋ／低下", inplace=True)
    ds.replace(u"血清Ｍ蛋白／陽性", u"Ｍ蛋白／陽性", inplace=True)
    ds.replace(u"血清Ｎａ／正常", u"Ｎａ／正常", inplace=True)
    ds.replace(u"血清アミラ−ゼ／上昇", u"アミラ−ゼ／上昇", inplace=True)
    ds.replace(u"血清アルブミン／低下", u"アルブミン／低下", inplace=True)
    ds.replace(u"血清クレアチニン／上昇", u"クレアチニン／上昇", inplace=True)
    ds.replace(u"血清クレアチニン／正常", u"クレアチニン／正常", inplace=True)
    ds.replace(u"血清抗糖脂質抗体／陽性", u"抗糖脂質抗体／陽性", inplace=True)
    ds.replace(u"血清浸透圧／上昇", u"浸透圧／上昇", inplace=True)
    ds.replace(u"血清浸透圧／低下", u"浸透圧／低下", inplace=True)
    ds.replace(u"血清銅／低下", u"銅／低下", inplace=True)
    ds.replace(u"血中ＣＫ値／上昇", u"ＣＫ／上昇", inplace=True)
    ds.replace(u"血中ＣＰＲ／低下", u"ＣＰＲ／低下", inplace=True)
    ds.replace(u"血中Ｃペプチド／上昇", u"Ｃペプチド／上昇", inplace=True)
    ds.replace(u"血中Ｃペプチド／低下", u"Ｃペプチド／低下", inplace=True)
    ds.replace(u"血中インスリン／上昇", u"インスリン／上昇", inplace=True)
    ds.replace(u"血中総ケトン／上昇", u"総ケトン／上昇", inplace=True)
    ds.replace(u"血糖／上昇", u"血糖／高値", inplace=True)
    ds.replace(u"血糖値／上昇", u"血糖／高値", inplace=True)
    ds.replace(u"血糖値／低下", u"血糖／低下", inplace=True)
    ds.replace(u"好酸球数／上昇", u"好酸球／上昇", inplace=True)
    ds.replace(u"抗ＤＮＡ抗体／上昇", u"抗ＤＮＡ抗体／陽性", inplace=True)
    ds.replace(u"抗ｄｓ−ＤＮＡ抗体／陽性", u"抗ｄｓＤＮＡ抗体／陽性", inplace=True)
    ds.replace(u"抗ＧＡＤ抗体／上昇", u"抗ＧＡＤ抗体／陽性", inplace=True)
    ds.replace(u"抗ＲＮＰ抗体／上昇", u"抗ＲＮＰ抗体／陽性", inplace=True)
    ds.replace(u"抗ＳＳ−Ａ／Ｒｏ抗体", u"抗ＳＳＡ抗体／Ｒｏ抗体", inplace=True)
    ds.replace(u"抗ＳＳ−Ａ抗体／陽性", u"抗ＳＳＡ抗体／陽性", inplace=True)
    ds.replace(u"抗ＳＳ−Ｂ抗体／陰性", u"抗ＳＳＢ抗体／陰性", inplace=True)
    ds.replace(u"抗ＳＳ−Ｂ抗体／陽性", u"抗ＳＳＢ抗体／陽性", inplace=True)
    ds.replace(u"抗Ｔｇ抗体／上昇", u"抗Ｔｇ抗体／陽性", inplace=True)
    ds.replace(u"抗ＴＰＯ抗体／上昇", u"抗ＴＰＯ抗体／陽性", inplace=True)
    ds.replace(u"抗アセチルコリン受容体抗体／上昇",
               u"抗アセチルコリン受容体抗体／陽性", inplace=True)
    ds.replace(u"抗核抗体／上昇", u"抗核抗体／陽性", inplace=True)
    ds.replace(u"心拍／正常", u"心拍数／正常", inplace=True)
    ds.replace(u"神経学的異常所見／陰性", u"神経学的異常／陰性", inplace=True)
    ds.replace(u"神経学的所見／正常", u"神経所見／正常", inplace=True)
    ds.replace(u"神経症状／陰性", u"神経所見／陰性", inplace=True)
    ds.replace(u"神経伝導検査／正常", u"神経伝導速度／正常", inplace=True)
    ds.replace(u"随時血糖値／上昇", u"随時血糖／上昇", inplace=True)
    ds.replace(u"髄液＝細胞／上昇", u"髄液＝細胞数／上昇", inplace=True)
    ds.replace(u"髄液検査／正常", u"髄液／正常", inplace=True)
    ds.replace(u"髄液検査＝ＩＬ−６／上昇", u"髄液＝ＩＬ−６／上昇", inplace=True)
    ds.replace(u"髄液検査＝細胞数／上昇", u"髄液＝細胞数／上昇", inplace=True)
    ds.replace(u"髄液検査＝細胞数／正常", u"髄液＝細胞数／正常", inplace=True)
    ds.replace(u"髄液検査＝総蛋白／上昇", u"髄液＝総蛋白／上昇", inplace=True)
    ds.replace(u"髄液検査＝単核球／上昇", u"髄液＝単核球／上昇", inplace=True)
    ds.replace(u"髄液検査＝蛋白／上昇", u"髄液＝蛋白／上昇", inplace=True)
    ds.replace(u"髄液検査＝糖／正常", u"髄液＝糖／正常", inplace=True)
    ds.replace(u"髄液検査＝糖／低下", u"髄液＝糖／低下", inplace=True)
    ds.replace(u"髄液細胞数／上昇", u"髄液＝細胞数／上昇", inplace=True)
    ds.replace(u"髄液細胞数／正常", u"髄液＝細胞数／正常", inplace=True)
    ds.replace(u"髄液所見／正常", u"髄液／正常", inplace=True)
    ds.replace(u"髄液所見＝蛋白／上昇", u"髄液＝蛋白／上昇", inplace=True)
    ds.replace(u"髄液蛋白／上昇", u"髄液＝蛋白／上昇", inplace=True)
    ds.replace(u"髄液蛋白／正常", u"髄液＝蛋白／正常", inplace=True)
    ds.replace(u"髄膜刺激症状／陰性", u"髄膜刺激徴候／陰性", inplace=True)
    ds.replace(u"髄膜刺激症状／陽性", u"髄膜刺激徴候／陽性", inplace=True)
    ds.replace(u"髄膜刺激兆候／陰性", u"髄膜刺激徴候／陰性", inplace=True)
    ds.replace(u"染色体／正常", u"染色体分析／正常", inplace=True)
    ds.replace(u"蛋白尿／上昇", u"蛋白尿／陽性", inplace=True)
    ds.replace(u"尿ケトン／陰性", u"尿ケトン体／陰性", inplace=True)
    ds.replace(u"尿ケトン／陽性", u"尿ケトン体／陽性", inplace=True)
    ds.replace(u"尿検査＝ケトン／陽性", u"尿＝ケトン／陽性", inplace=True)
    ds.replace(u"尿中赤血球／上昇", u"尿中赤血球／陽性", inplace=True)
    ds.replace(u"尿中白血球／上昇", u"尿中白血球／陽性", inplace=True)
    ds.replace(u"白血球／低下", u"白血球／減少", inplace=True)
    ds.replace(u"白血球数／上昇", u"白血球／上昇", inplace=True)
    ds.replace(u"白血球数／正常", u"白血球／正常", inplace=True)
    ds.replace(u"白血球数／低下", u"白血球／減少", inplace=True)
    ds.replace(u"腹水ＡＤＡ／上昇", u"腹水＝ＡＤＡ／上昇", inplace=True)
    ds.replace(u"腹部ＣＴ検査／正常", u"腹部ＣＴ／正常", inplace=True)
    ds.replace(u"末梢血＝異型リンパ球／陽性", u"異型リンパ球／陽性", inplace=True)
    ds.replace(u"末梢血＝芽球／陽性", u"芽球／陽性", inplace=True)
    ds.replace(u"末梢血好酸球／上昇", u"好酸球／上昇", inplace=True)
    ds.replace(u"網赤血球／低下", u"網状赤血球／低下", inplace=True)

    # ds = self.expand_dot(ds)
    return ds


def replace_side_effects(ds):
    ds.replace(u"［副作用］", u"[副作用]", inplace=True)
    ds.replace(u"【副作用】", u"[副作用]", inplace=True)
    ds.replace(u"〔副作用〕", u"[副作用]", inplace=True)
    ds.replace(u"（副作用）", u"[副作用]", inplace=True)
    ds.replace(u"\(副作用\)", u"[副作用]", inplace=True)
    ds.replace(u"^\[副作用\](.*)", u"[副作用]\\1[副作用]",
               inplace=True, regex=True)
    ds.replace(u"\[副作用\]", u"副作用")
    return ds


def exclude_stars(ds):
    ds.replace(u"＠", u"@", inplace=True)
    ds.replace(u"：", u":", inplace=True)
    ds.replace(u"／", u"/", inplace=True)
    ds.replace(u"＝", u"=", inplace=True)
    ds.replace(u"＊", u"*", inplace=True)
    ds.replace(u"@", u"＆@＆", inplace=True)
    ds.replace(u":", u"＆:＆", inplace=True)
    ds.replace(u"/", u"＆/＆", inplace=True)
    ds.replace(u"=", u"＆=＆", inplace=True)
    ds.replace(u"・", u"＆・＆", inplace=True)
    ds = ds.str.split(u"＆")
    ds = ds.apply(find_n_del_stars)
    return ds


def expand_dot(ds, dot_pat):
    text = re.sub(r"([ァ-ヴ]+?)・([ァ-ヴ]+?)", r"\1■\2", text)
    # A1・A2・A3
    if re.match(self.dot_pat[0], text):
        text = text.replace(u"・", u"＆")
    # A1=B1/C1@D1・A2=B2/C2@D2・A3=B3/C3@D3
    elif re.match(self.dot_pat[1], text):
        text = text.replace(u"・", u"＆")
    # A1=B1@D1・A2=B2@D2・A3=B3@D3
    elif re.match(self.dot_pat[2], text):
        text = text.replace(u"・", u"＆")
    # A1=B1/C1・A2=B2/C2・A3=B3/C3
    elif re.match(self.dot_pat[3], text):
        text = text.replace(u"・", u"＆")
    # B1@D1・B2@D2・B3@D3
    elif re.match(self.dot_pat[4], text):
        text = text.replace(u"・", u"＆")
    # B1/C1・B2/C2・B3/C3
    elif re.match(self.dot_pat[5], text):
        text = text.replace(u"・", u"＆")
    # A=B1@C1・B2@C2
    elif re.match(self.dot_pat[6], text):
        text = self.product_text(text, eq=True)
    # A=B1/C1・B2/C2
    elif re.match(self.dot_pat[7], text):
        text = self.product_text(text, eq=True)
    # A1・A2・A3=B/C@D
    elif re.match(self.dot_pat[8], text):
        text = self.product_text(text, eq=True)
    # A1・A2・A3=B@D
    elif re.match(self.dot_pat[9], text):
        text = self.product_text(text, at=True, sl=True, eq=True)
    # A1・A2・A3=B/C
    elif re.match(self.dot_pat[10], text):
        text = self.product_text(text, at=True, eq=True)
    # A1・A2・A3=B
    elif re.match(self.dot_pat[11], text):
        text = self.product_text(text, eq=True)
    # B1・B2・B3@D
    elif re.match(self.dot_pat[12], text):
        text = self.product_text(text, at=True)
    # B1・B2・B3/C
    elif re.match(self.dot_pat[13], text):
        text = self.product_text(text, sl=True)
    # A=B1・B2・B3/C@D
    elif re.match(self.dot_pat[14], text):
        text = self.product_text(text, at=True, sl=True, eq=True)
    # A=B1・B2・B3@D
    elif re.match(self.dot_pat[15], text):
        text = self.product_text(text, at=True, eq=True)
    # A=B1・B2・B3/C
    elif re.match(self.dot_pat[16], text):
        text = self.product_text(text, sl=True, eq=True)
    # A=D1・D2・D3
    elif re.match(self.dot_pat[17], text):
        text = self.product_text(text, eq=True)
    # A=B/C@D1・D2・D3
    elif re.match(self.dot_pat[18], text):
        text = self.product_text(text, at=True)
    # A=B@D1・D2・D3
    elif re.match(self.dot_pat[19], text):
        text = self.product_text(text, at=True)
    # B@D1・D2・D3
    elif re.match(self.dot_pat[20], text):
        text = self.product_text(text, at=True)
    # B1・B2/C@D
    elif re.match(self.dot_pat[21], text):
        text = self.product_text(text, at=True, sl=True)
    # B/C@D1・D2・D3
    elif re.match(self.dot_pat[22], text):
        text = self.product_text(text, at=True)
    # H:A1・A2・A3
    elif re.match(self.dot_pat[23], text):
        text = self.product_text(text, cl=True)
    # H:A1・A2・A3@C
    elif re.match(self.dot_pat[24], text):
        text = self.product_text(text, at=True, cl=True)
    # H:A1・A2・A3/C
    elif re.match(self.dot_pat[25], text):
        text = self.product_text(text, sl=True, cl=True)
    # H:A@C1・C2
    elif re.match(self.dot_pat[26], text):
        text = self.product_text(text, at=True, cl=True)
    # A1・A2・A3=B/C@D1・D2・D3
    elif re.match(self.dot_pat[27], text):
        text = self.product_text(text, at=True, eq=True)
    # A1・A2・A3=B1・B2・B3/C@D
    elif re.match(self.dot_pat[28], text):
        text = self.product_text(text, at=True, sl=True, eq=True)
    # A=B1・B2・B3/C@D1・D2・D3
    elif re.match(self.dot_pat[29], text):
        text = self.product_text(text, at=True, eq=True)
    # A1・A2=B1・B2@C
    elif re.match(self.dot_pat[30], text):
        text = self.product_text(text, at=True, eq=True)
    # A1・A2=B1・B2
    elif re.match(self.dot_pat[31], text):
        text = self.product_text(text, eq=True)
    # A1・A2=B1@C1・C2
    elif re.match(self.dot_pat[32], text):
        text = self.product_text(text, at=True, eq=True)
    # A=B1・B2@C1・C2
    elif re.match(self.dot_pat[33], text):
        text = self.product_text(text, at=True, eq=True)
    # A1・A2=B1・B2/C
    elif re.match(self.dot_pat[34], text):
        text = self.product_text(text, at=True, sl=True, eq=True)
    # B1・B2/C@D1・D2
    elif re.match(self.dot_pat[35], text):
        text = self.product_text(text, at=True, sl=True, eq=True)
    # A1・A2@B1・B2
    elif re.match(self.dot_pat[36], text):
        text = self.product_text(text, at=True)

    text = re.sub(u"■", u"・", text)
    return text


def find_n_del_stars(text):
    for i, s in enumerate(text):
        if s.find(u"*") > -1:
            part_tuple = s.rpartition(u"*")
            text[i] = part_tuple[2]
    text = u"".join(text)
    return text


def define_dot_pattern():
    dot_pat = []
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
    dot_pat.append(re.compile(pat_00 + r"$"))
    # A1=B1/C1@D1・A2=B2/C2@D2・A3=B3/C3@D3
    dot_pat.append(re.compile(pat_01 + r"(・" + pat_01 + r")+$"))
    # A1=B1@D1・A2=B2@D2・A3=B3@D3
    dot_pat.append(re.compile(pat_02 + r"(・" + pat_02 + r")+$"))
    # A1=B1/C1・A2=B2/C2・A3=B3/C3
    dot_pat.append(re.compile(pat_03 + r"(・" + pat_03 + r")+$"))
    # B1@D1・B2@D2・B3@D3
    dot_pat.append(re.compile(pat_04 + r"(・" + pat_04 + r")+$"))
    # B1/C1・B2/C2・B3/C3
    dot_pat.append(re.compile(pat_05 + r"(・" + pat_05 + r")+$"))

    # A=B1@C1・B2@C2
    dot_pat.append(re.compile(pat_07 + pat_04 + r"(・" + pat_04 + r")+$"))
    # A=B1/C1・B2/C2
    dot_pat.append(re.compile(pat_07 + pat_05 + r"(・" + pat_05 + r")+$"))
    # A1・A2・A3=B/C@D
    dot_pat.append(re.compile(pat_00 + pat_01 + r"$"))
    # A1・A2・A3=B@D
    dot_pat.append(re.compile(pat_00 + pat_02 + r"$"))
    # A1・A2・A3=B/C
    dot_pat.append(re.compile(pat_00 + pat_03 + r"$"))
    # A1・A2・A3=B
    dot_pat.append(re.compile(pat_00 + pat_07 + r"$"))
    # B1・B2・B3@D
    dot_pat.append(re.compile(pat_00 + pat_04 + r"$"))
    # B1・B2・B3/C
    dot_pat.append(re.compile(pat_00 + pat_05 + r"$"))
    # A=B1・B2・B3/C@D
    dot_pat.append(re.compile(pat_07 + pat_00 + pat_06 + r"$"))
    # A=B1・B2・B3@D
    dot_pat.append(re.compile(pat_07 + pat_00 + pat_04 + r"$"))
    # A=B1・B2・B3/C
    dot_pat.append(re.compile(pat_07 + pat_00 + pat_05 + r"$"))
    # A=D1・D2・D3
    dot_pat.append(re.compile(pat_07 + pat_00 + r"$"))
    # A=B/C@D1・D2・D3
    dot_pat.append(re.compile(pat_01 + pat_00 + r"$"))
    # A=B@D1・D2・D3
    dot_pat.append(re.compile(pat_02 + pat_00 + r"$"))
    # B@D1・D2・D3
    dot_pat.append(re.compile(pat_04 + pat_00 + r"$"))
    # B1・B2/C@D
    dot_pat.append(re.compile(pat_00 + pat_06 + r"$"))
    # B/C@D1・D2・D3
    dot_pat.append(re.compile(pat_06 + pat_00 + r"$"))
    # H:A1・A2・A3
    dot_pat.append(re.compile(pat_08 + pat_00 + r"$"))
    # H:A1・A2・A3@C
    dot_pat.append(re.compile(pat_08 + pat_00 + pat_04 + r"$"))
    # H:A1・A2・A3/C
    dot_pat.append(re.compile(pat_08 + pat_00 + pat_05 + r"$"))
    # H:A@C1・C2
    dot_pat.append(re.compile(pat_08 + pat_04 + pat_00 + r"$"))
    # A1・A2・A3=B/C@D1・D2・D3
    dot_pat.append(re.compile(pat_00 + pat_01 + pat_00 + r"$"))
    # A1・A2・A3=B1・B2・B3/C@D
    dot_pat.append(re.compile(pat_00 + pat_07 + pat_00 + pat_06 + r"$"))
    # A=B1・B2・B3/C@D1・D2・D3
    dot_pat.append(re.compile(pat_07 + pat_00 + pat_06 + pat_00 + r"$"))
    # A1・A2=B1・B2@C
    dot_pat.append(re.compile(pat_00 + pat_07 + pat_00 + pat_04 + r"$"))
    # A1・A2=B1・B2
    dot_pat.append(re.compile(pat_00 + pat_07 + pat_00 + r"$"))
    # A1・A2=B1@C1・C2
    dot_pat.append(re.compile(pat_00 + pat_02 + pat_00 + r"$"))
    # A=B1・B2@C1・C2
    dot_pat.append(re.compile(pat_07 + pat_00 + pat_04 + pat_00 + r"$"))
    # A1・A2=B1・B2/C
    dot_pat.append(re.compile(pat_00 + pat_07 + pat_00 + pat_05 + r"$"))
    # B1・B2/C@D1・D2
    dot_pat.append(re.compile(pat_00 + pat_06 + pat_00 + r"$"))
    # A1・A2@B1・B2
    dot_pat.append(re.compile(pat_00 + pat_04 + pat_00 + r"$"))

    return dot_pat


def product_text(text, at=False, sl=False, eq=False, cl=False):
    if at:
        text = re.sub(u"@", u"＆@＆", text)
    if sl:
        text = re.sub(u"/", u"＆/＆", text)
    if eq:
        text = re.sub(u"=", u"＆=＆", text)
    if cl:
        if re.match(u"H:|PH:|FH:", text):
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
