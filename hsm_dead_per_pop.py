import numpy as np
import csv
from ast import literal_eval
from datetime import datetime
import pandas as pd
import subprocess
import sys
import argparse


args = sys.argv


class DataProcessing:
	def __init__(self, csv_path, start='2020/1/16', end='2021/5/12', threshold='1000000'):
		self.csv_path = csv_path
		self.start = start
		self.end = end
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

		self.infected_perday_dict = {}
		self.death_perday_dict = {}

		for i, pref in enumerate(self.prefecture):
			pref_indices = np.where(np.array(df.loc[:, '都道府県コード']) == i + 1)
			date_list = np.array(df.loc[pref_indices, '日付'])
			infected_perday = np.array(df.loc[pref_indices, '各地の感染者数_1日ごとの発表数'])
			death_perday = np.array(df.loc[pref_indices, '各地の死者数_1日ごとの発表数'])

			start_idx = np.argwhere(date_list == start)[0, 0]
			end_idx = np.argwhere(date_list == end)[0, 0]
			infected_perday = np.sum(infected_perday[start_idx:end_idx+1])
			death_perday = np.sum(death_perday[start_idx:end_idx+1])

			self.infected_perday_dict[pref] = infected_perday
			self.death_perday_dict[pref] = death_perday

	def txt_output(self):
		with open('./coronaData.txt', 'w') as f:
			number = str(len(self.prefecture)) + ' ' + '#' + str(self.start) + '-' + str(self.end)
			f.write(number + '\n')
			for i, pref in enumerate(self.prefecture):
				line = '#' + str(i) +': ' + str(self.pop[i]) + ' ' + str(self.death_perday_dict[pref]) + ' ' + '#-' + str(i+1) + pref
				f.write(line + '\n')

	def hsm_program(self):
		proc = subprocess.run('./hsm coronaData.txt {} -p'.format(self.threshold), shell=True)

		mylist = subprocess.Popen(
			'./hsm coronaData.txt {} -p'.format(self.threshold), 
			stdout=subprocess.PIPE, 
			shell=True).stdout.readlines()
		print(mylist[4])

	
	def call(self, start_date, end_date):
		pass


if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('--start', type=str, default='2020/1/16')
	parser.add_argument('--end', type=str, default='2021/6/30')
	parser.add_argument('--threshold', type=str, default='10000000')
	args = parser.parse_args()
	
	print(args, '\n')

	dp = DataProcessing(
        csv_path='./nhk_news_covid19_prefectures_daily_data.csv',
        start=args.start, end=args.end, threshold=args.threshold)
	dp.txt_output()
	dp.hsm_program()
