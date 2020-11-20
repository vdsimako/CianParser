from bs4 import BeautifulSoup
import requests
import csv


# class="_93444fe79c--list--HEGFW"
# TODO place cyti on hostname?
url = 'https://fryazino.cian.ru/cat.php?deal_type=sale&engine_version=2&offer_type=flat&p={}&region=5038&room1=1&room2=1'

def parsePage(url, pageNum):
	result = requests.get(url.format(pageNum))
	resultList = []
	result = requests.get(url)
	soup = BeautifulSoup(result.content, 'html.parser')

	# offerList = soup.select('[data-name="CardComponent"]')
	offerList = soup.select('._93444fe79c--cont--1Ddh2')

	for offer in offerList:
		resultRow = []
		href = offer.select_one('._93444fe79c--link--39cNw').get('href')
		offreId = href.split("/")[-2]
		resultRow.append(offreId)
		resultRow.append(href)
		resultRow.append(offer.select_one('[data-mark="OfferTitle"]').text)
		offerSubtitle = ''
		if not offer.select_one('[data-mark="OfferSubtitle"]') is None:
			offerSubtitle = offer.select_one('[data-mark="OfferSubtitle"]').text
		resultRow.append(offerSubtitle)
		resultRow.append(offer.select_one('[data-mark="MainPrice"]').text)

		address = [element.text for element in offer.select('[data-name="GeoLabel"]') ]

		address = ','.join(address)
		resultRow.append(address)
		resultList.append(resultRow)
	return resultList

def writeToFile(dataList):
	with open('result.csv', 'a', encoding='utf8') as f:
		for row in dataList:
			writer = csv.writer(f)
			writer.writerow(row)

page = 1
pageCount = 1
while page <= pageCount:

	rowList = parsePage(url, page)

	if rowList == -1:
		break

	writeToFile(rowList)
	print(page)
	page += 1
