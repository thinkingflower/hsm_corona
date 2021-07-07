import numpy as np
import csv
from ast import literal_eval
from datetime import datetime
import pandas as pd
import subprocess
import sys
import argparse

'''
2020年都道府県別交通事故発生状況"https://www.e-stat.go.jp/stat-search/files?page=1&layout=datalist&toukei=00130002&tstat=000001027458&cycle=7&year=20200&month=0"
 -8茨城県 -9栃木県 -45宮崎県 -17石川県 -40福岡県 -33岡山県 -46鹿児島県 -10群馬県 -23愛知県 -28兵庫県 -6山形県 -7福島県 -27大阪府 -43熊本県 -42長崎県 -24三重県 -25滋賀県 -12千葉県 -47沖縄県 -29奈良県 -35山口県 -44大分県 -2青森県 -38愛媛県 -34広島県 -14神奈川県 -4宮城県 -16富山県 -26京都府 -3岩手県 -1北海道 -15新潟県 -5秋田県 -11埼玉県 -22静岡県 -20長野県 -13東京都 -21岐阜県
'''
args = sys.argv


class DataProcessing:
	def __init__(self, csv_path, threshold='1000000'):
		self.csv_path = csv_path
		self.threshold = threshold
		df = pd.read_csv(filepath_or_buffer=csv_path)

		self.prefecture = np.array([
			'北海道','青森県','岩手県','宮城県','秋田県','山形県','福島県','茨城県','栃木県','群馬県',
			'埼玉県','千葉県','東京都','神奈川県','新潟県','富山県','石川県','福井県','山梨県',
			'長野県','岐阜県','静岡県','愛知県','三重県','滋賀県','京都府','大阪府','兵庫県',
			'奈良県','和歌山県','鳥取県','島根県','岡山県','広島県','山口県','徳島県','香川県',
			'愛媛県','高知県','福岡県','佐賀県','長崎県','熊本県','大分県','宮崎県','鹿児島県','沖縄県'])

		self.pop = np.array([
			'5,382,000', '1,308,000', '1,280,000', '2,334,000', '1,023,000',
			'1,124,000', '1,914,000', '2,917,000', '1,974,000', '1,973,000',
			'7,267,000', '6,223,000', '13,515,000', '9,126,000', '2,304,000',
			'1,066,000', '1,154,000', '787,000', '835,000', '2,099,000', 
			'2,032,000', '3,700,000', '7,483,000', '1,816,000', '1,413,000', 
			'2,610,000', '8,839,000', '5,535,000', '1,364,000', '964,000', 
			'573,000', '694,000', '1,922,000', '2,844,000', '1,405,000', 
			'756,000', '976,000', '1,385,000', '728,000', '5,102,000', '833,000',
			'1,377,000', '1,786,000', '1,166,000', '1,104,000', '1,648,000', '1,434,000'
		])

		self.accidents = np.array(df.loc[:, '件'])
		self.accidents_dict = {key: val for key, val in zip(self.prefecture, self.accidents)}

	def txt_output(self):
		with open('./trafficAccs.txt', 'w') as f:
			number = str(len(self.prefecture)) + ' ' + '#' + 'populations&trafficAccidents'
			f.write(number + '\n')
			for i, pref in enumerate(self.prefecture):
				line = '#' + str(i) +': ' + str(self.pop[i]) + ' ' + str(self.accidents_dict[pref]) + ' ' + '#-' + str(i+1) + pref
				f.write(line + '\n')

	def hsm_program(self):
		proc = subprocess.run('../HotSpotMiner1.72/hsm trafficAccs.txt {} -p'.format(self.threshold), shell=True)

		mylist = subprocess.Popen(
			'../HotSpotMiner1.72/hsm trafficAccs.txt {} -p'.format(self.threshold), 
			stdout=subprocess.PIPE, 
			shell=True).stdout.readlines()
		print(mylist[4])


if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('--threshold', type=str, default='10000000')
	args = parser.parse_args()
	print(args, '\n')

	dp = DataProcessing(
        csv_path='./trafficAccident.csv', threshold=args.threshold)
	dp.txt_output()
	dp.hsm_program()