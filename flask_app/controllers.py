import os
import sys

from .models import HomophonesGroup

# Needed to execute this package as a script
sys.path.append(os.path.join(os.path.dirname(__file__), os.path.pardir))


def define_limit_offset(request):
	""" Define limit and offset variables from request.args """

	if request.args:
		try:
			limit = int(request.args['limit'])
			offset = int(request.args['offset'])
		except:
			# Default limit and offset
			limit = 12
			offset = 0
	else:
		# Default limit and offset
		limit = 12
		offset = 0

	return (limit, offset)


def get_current_browse_page_homophones(homophonesGroupCollection, limit, offset):
	""" Return list of homophones to be shown at the browse page, the latter determined by the limit and offset. """

	nthDocument = find_nth_document(homophonesGroupCollection, offset)
	nthID = nthDocument['_id']
	documentsAfterNthDocument = homophonesGroupCollection.find(
		{'_id': {'$gte': nthID}}).limit(limit)
	homophones = list(map(lambda x: x['homophones'], documentsAfterNthDocument))

	return homophones


def define_pagination_variables(limit, offset, homophonesGroupCollection):
	""" Define previous URL, next URL, total number of pages and current page based
	on the limit and offset. """

	if offset - limit < 0:
		prevURL = None
	else:
		prevURL = f'/p/?limit={limit}&offset={offset - limit}'

	totalDocuments = homophonesGroupCollection.count_documents({})
	if offset + limit >= totalDocuments:
		nextURL = None
	else:
		nextURL = f'/p/?limit={limit}&offset={offset + limit}'

	totalPages = (totalDocuments // limit) + 1
	currentPage = (offset // limit) + 1

	return (prevURL, nextURL, totalPages, currentPage)


def find_one_random_document(homophonesGroupCollection):
	""" Return random document from database """

	cursor = homophonesGroupCollection.aggregate([
		{ "$sample": { "size": 1 } }
	])

	return list(cursor)[0]


def find_nth_document(homophonesGroupCollection, n):
	""" Return nth document from database (insertion order). """

	return homophonesGroupCollection.find_one(skip=n)


def create_homophones_list(homophonesCollection, query="", random=False):
	""" Return Homophone object with queried word (if applicable) and its homophones.

		Optional keyword arguments:

		`random`: will use a random homophone as starting point
		if set to `True`.
	"""

	homophonesList = []

	if random:
		homophone = find_one_random_document(homophonesCollection)
		# print(homophone)
	else:
		homophone = homophonesCollection.find_one({"word": query.strip()})
		if homophone is None:
			return None

	# Create list querying all homophones
	homophonesList.append(homophone)
	# print(homophone)
	for otherHomophone in homophone['pronunciations']['homophones']:
		try:
			# print(f"Querying {otherHomophone.strip()}...")
			wordQueryResult = homophonesCollection.find_one(
				{"word": otherHomophone})
			# print(f"query: {wordQueryResult}")
		except TypeError:  # If the query return None
			wordQueryResult = None

		# If didn't find in the database, proceed to next iteration
		if not wordQueryResult:
			continue

		homophonesList.append(wordQueryResult)

	homophones = HomophonesGroup(homophonesList)

	return homophones
