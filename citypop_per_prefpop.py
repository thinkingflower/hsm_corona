import numpy as np
import csv
from ast import literal_eval
from datetime import datetime
import pandas as pd
import subprocess
import sys
import argparse


''' ================
都会の方が多いと思いきや，田舎の方が第一都市に集中している．
 -43熊本県 -33岡山県 -46鹿児島県 -9栃木県 -38愛媛県 -44大分県 -17石川県 -16富山県 -42長崎県 -15新潟県 -45宮崎県 -10群馬県 -29奈良県 -7福島県 -25滋賀県 -24三重県 -5秋田県 -3岩手県 -2青森県 -22静岡県 -35山口県 -6山形県 -21岐阜県 -20長野県 -12千葉県 -8茨城県
================'''

args = sys.argv

class DataProcessing:
	def __init__(self, threshold):
		self.threshold = threshold
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

		self.citypop = np.array([
			'1,966,416','279,133','294,047','1,088,669','308,482','250,998','342,897',
			'270,289','520,189','369,733','1,295,607','977,247','9,555,919','3,740,172',
			'800,582','417,332','465,325','263,529','189,589','372,304','402,537','794,025',
			'2,320,361','310,750','341,488','1,468,980','2,725,006','1,527,407','355,350',
			'357,868','190,090','204,428','721,329','1,199,252','259,855','256,698','419,696',
			'510,963','331,414','1,579,450','234,342','416,419','739,556','478,113','398,841','597,193','318,270'
		])

		self.city_pops_dict = {key: val for key, val in zip(self.prefecture, self.citypop)}

	def txt_output(self):
		with open('./citypopData.txt', 'w') as f:
			number = str(len(self.prefecture)) + ' ' + '#' + 'pref_pops & city_pops'
			f.write(number + '\n')
			for i, pref in enumerate(self.prefecture):
				line = '#' + str(i) +': ' + str(self.pop[i]) + ' ' + str(self.city_pops_dict[pref]) + ' ' + '#-' + str(i+1) + pref
				f.write(line + '\n')

	def hsm_program(self):
		proc = subprocess.run('../HotSpotMiner1.72/hsm citypopData.txt {} -p'.format(self.threshold), shell=True)

		mylist = subprocess.Popen(
			'../HotSpotMiner1.72/hsm citypopData.txt {} -p'.format(self.threshold), 
			stdout=subprocess.PIPE, 
			shell=True).stdout.readlines()
		print(mylist[4])


if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('--threshold', type=str, default='10000000')
	args = parser.parse_args()
	print(args, '\n')

	dp = DataProcessing(threshold=args.threshold)
	dp.txt_output()
	dp.hsm_program()