import json
import requests


KEYWORDS = ["Machine Learning", "Neural Network", "CNN", "RNN", "LSTM", "Deep Learning"]

class QueryEntry(object):
	"""docstring for QueryEntry"""
	def __init__(self, doi):
		super(QueryEntry, self).__init__()
		self.doi = doi

class BibTexObject(object):
	"""docstring for BibTexObject"""
	def __init__(self, title, author_list, keywords, abstract):
		super(BibTexObject, self).__init__()
		self.title = title
		self.authors = author_list
		self.keywords = keywords
		self.abstract = abstract
		

class BibTexEngine(object):
	"""docstring for BibTexEngine"""
	def __init__(self):
		super(BibTexEngine, self).__init__()

	def query(self, queryObj):
		bibtex = dict()
		print(f"query from https://dl.acm.org/doi/{queryObj.doi} ... ")
		r = requests.get(f'https://dl.acm.org/doi/{queryObj.doi}')
		r = requests.post('https://dl.acm.org/action/exportCiteProcCitation', data={
			'dois': queryObj.doi,
			'targetFile': 'custom-bibtex',
			'format': 'bibTex'
		})

		j = json.loads(r.text)
		kvs = list(j['items'][0].items())[0][1]

		if 'title' not in bibtex and 'title' in kvs:
			bibtex['title'] = kvs['title']

		for k in ['original-date', 'issued']:
			if k in kvs:
				date = kvs[k]
				ds = map(str, date['date-parts'][0])
				bibtex['date'] = '/'.join(ds)
				break
		if 'author' in kvs:
			l = []
			for a in kvs['author']:
				name = ''
				if 'given' in a:
					name += a['given']
				if 'family' in a:
					if name:
						name += ' '
					name += a['family']
				l.append(name)
			bibtex['authors'] = l
		if 'keyword' in kvs:
			bibtex['keyword'] = kvs['keyword'].split(", ")
		if 'abstract' in kvs:
			bibtex['abstract'] = kvs['abstract']
		if 'keyword' in kvs and 'abstract' in kvs:
			bibObj = BibTexObject(bibtex['title'], bibtex['authors'], bibtex['keyword'], bibtex['abstract'])
		elif 'keyword' in kvs:
			bibObj = BibTexObject(bibtex['title'], bibtex['authors'], bibtex['keyword'], '')
		elif 'abstract' in kvs:
			bibObj = BibTexObject(bibtex['title'], bibtex['authors'], [], bibtex['abstract'])
		else:
			bibObj = BibTexObject(bibtex['title'], bibtex['authors'], [], '')
		return bibObj

	def toBibObj(self, bibentry):
		if 'keywords' in bibentry and 'abstract' in bibentry:
			bibObj = BibTexObject(bibentry['title'], bibentry['author'], bibentry['keywords'], bibentry['abstract'])
		elif 'keywords' in bibentry:
			bibObj = BibTexObject(bibentry['title'], bibentry['author'], bibentry['keywords'], '')
		elif 'abstract' in bibentry:
			bibObj = BibTexObject(bibentry['title'], bibentry['author'], [], bibentry['abstract'])
		else:
			bibObj = BibTexObject(bibentry['title'], bibentry['author'], [], '')
		return bibObj


	def findKeyword(self, bibObj, keywords=KEYWORDS):
		for kw in keywords:
			if kw.lower() in bibObj.keywords:
				return True
			elif kw.lower() in bibObj.abstract:
				return True
		return False
