import bibtexparser
import argparse
import bibengine
import pandas as pd


def parse_bibtex_entry(entry):
	return bibengine.QueryEntry(entry['doi'])


def read_conference(conferencebib):
	with open(conferencebib) as bibtex_file:
		bib_database = bibtexparser.load(bibtex_file)
	return bib_database.entries


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Analze Conference.')
	parser.add_argument('-c', '--conf', action='store', dest='conferences',
                    type=str, nargs='*', default=["asplos", "ccs", "isca", "pact", "pldi", "ppopp"],
                    help='set the conference to analyze')
	parser.add_argument('-y', '--years', action='store', dest='years',
                    type=int, nargs='*', default=[2016, 2017, 2018, 2019, 2020],
                    help='set the year of the conference to parse')
	args = parser.parse_args()
	pddata = dict()

	engine = bibengine.BibTexEngine()
	pddata['Years'] = args.years
	paper_cnt_list, ml_paper_list = [], []
	for year in args.years:
		# total number of accepted papers in top-tier conferences
		total_paper_cnts = 0
		ml_related_paper_cnts = 0
		for conference in args.conferences:
			bib_entries = read_conference(f"./conferences/{conference}/{conference}{year}.bib")
			for bibentry in bib_entries:
				qe = parse_bibtex_entry(bibentry)
				result = engine.query(qe)
				if result:
					ml_related_paper_cnts += 1
			total_paper_cnts += len(bib_entries)
		paper_cnt_list += [total_paper_cnts]
		ml_paper_list += [ml_related_paper_cnts]
	pddata['Papers'] = paper_cnt_list
	pddata['ML Related Papers'] = ml_paper_list
	df = pd.DataFrame(data=pddata)
	print(df)



