#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import re
import argparse
import flickrapi

from apiconfig import APIConfig



class RelatedTags():

	# Public
	tag = None
	getphotocount = False

	# Private
	_flickr = None
	_apiconfig = None


# ------------------------------------------------------------------------
	def __init__(self, apiconfig):

		# Get API configuration
		self._apiconfig = apiconfig

		# Prepare Flickr API
		self._flickr = flickrapi.FlickrAPI(
			api_key = self._apiconfig.key,
			secret  = self._apiconfig.secret,
			format  = 'etree'
			)


# ------------------------------------------------------------------------
	def Run(self):

		def sortByTag(item):
			return item[0]

		def sortByPhotoCount(item):
			return item[1]

		# Call Flickr - Get related tags
		print("Searching related tag for: {0}".format(self.tag))
		flickr_response = self._flickr.tags.getrelated(
			tag=self.tag
			)

		# Read all tags from response
		rel_tags=[]
		for r in flickr_response.find('tags').findall('tag'):
			rel_tags.append(r.text)

		print("Found {0} related tags:".format(len(rel_tags)))

		# Check user response
		_related_tags=[]
		if self.getphotocount:

			print "Requesting photo count for each tag..."

			# For each tag look how many photos are available
			for rel_tag in rel_tags:

				# Init
				photo_count=0

				# Search photos with the tag
				flickr_response = self._flickr.photos.search(
					tags=rel_tag,
					sort='relevace',
					per_page=1,
					page=1
					)

				# Read photo count
				photo_count = int(flickr_response.find('photos').attrib['total'])

				# Add tuple to list
				_related_tags.append( (rel_tag, photo_count) )

		# Sort tuple-list and print them
		if self.getphotocount:
			#for t in sorted(_related_tags, reverse=True, key=sortByPhotoCount):
			#	#print("%s [%d]" % ('{0: <15}'.format(t[0]), t[1]))
			#	print(" {0: <15}: {1: >10,d}".format(t[0], t[1], grouping=True))
			num_tags = len(rel_tags)
			num_cols = 2
			num_rows = int(num_tags / num_cols)+1
			sorted_tags = sorted(_related_tags, reverse=True, key=sortByPhotoCount)
			col_width = max(len(t) for t in rel_tags) + 2
			for i in range(num_rows):
				for j in range(num_cols):
					if i + j*num_rows < num_tags:
						print("- {0: <{2}}: {1: >10,d}   ".format(
							sorted_tags[i+j*num_rows][0],
							sorted_tags[i+j*num_rows][1],
							col_width)),
				print

		else:
			num_tags = len(rel_tags)
			num_cols = 3
			num_rows = int(num_tags / num_cols)+1
			sorted_tags = sorted(rel_tags, key=sortByTag)
			col_width = max(len(t) for t in rel_tags) + 2
			#print("num_tags={}, num_cols={}, num_rows={}".format(num_tags, num_cols, num_rows))
			for i in range(num_rows):
				for j in range(num_cols):
					if i + j*num_rows < num_tags:
						print("- {0: <{1}}".format(
							sorted_tags[i+j*num_rows],
							col_width)),
				print



# ========================================================================
if __name__ == '__main__':

	# Load API config
	apiconfig = APIConfig()

	# Create parser for arguments
	parser = argparse.ArgumentParser(description="Flickr getRelated TAG")

	# Add arguments to parser
	parser.add_argument('--tag',
		required=True,
		action='store',
		help="Search tags related to TAG")
	parser.add_argument('--getphotocount',
		required=False,
		action='store_true',
		default=False,
		help='Get the number of photo for each related tag')

	# Parse arguments
	args = parser.parse_args()

	# Create RelatedTag()
	rt = RelatedTags(apiconfig)

	# Pass the tag to RelatedTag()
	rt.tag = args.tag
	rt.getphotocount = args.getphotocount

	# Run
	rt.Run()



# === VIM modeline ===
# :set modeline
# :e [reload buffer]
# vim: tabstop=4 shiftwidth=4 noexpandtab
# eof
