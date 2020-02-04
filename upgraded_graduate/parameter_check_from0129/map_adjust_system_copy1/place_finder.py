f = open('ネジ座標写真アナパ.txt')
data1 = f.read()  # ファイル終端まで全て読んだデータを返す
f.close()
lines1 = data1.split('\n') # 改行で区切る(改行文字そのものは戻り値のデータには含まれない)
print(type(lines1))
for line in lines1:
    datas = 
print()
