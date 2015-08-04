import requests
import string
from PIL import Image
import os
import sys
import shutil
import glob

#go register one at bing.com/developers
key = "ZqtAKVnXJJGyM7VxyTJrGvfTIRljKZTC5dGf49NrkSs"

#inspired by BingSearchAPI
class BingSearch():
	bing_api = "https://api.datamarket.azure.com/Data.ashx/Bing/Search/v1/Composite?"

	def __init__(self,key):
		self.key = key

	def replace_symbols(self, request):
		request = string.replace(request, "'", '%27')
		request = string.replace(request, '"', '%27')
		request = string.replace(request, '+', '%2b')
		request = string.replace(request, ' ', '%20')
		request = string.replace(request, ':', '%3a')
		return request

	def search(self, sources, query, params):
		request =  'Sources="' + sources    + '"'
		request += '&Query="'  + str(query) + '"'
		for key,value in params.iteritems():
			request += '&' + key + '=' + str(value) 
		request = self.bing_api + self.replace_symbols(request)
		return requests.get(request, auth=(self.key, self.key))

#your list of things to get images for
people = ['barack obama','michelle obama','neil degrasse tyson','dr martin luther king jr','aliko dangote','malcolm x','james baldwin','james mickens','oprah winfrey','clarence ellis','zora neal hurston','muhammad ali','jimi hendrix','rosa parks','mae jemison','colin powell','bb king','david blackwell','langston hughes','chris rock','common','dave chappelle','michael jordan','roland fryer','jackie robinson','richard pryor','madam c j walker','maya angelou','web dubois','alain locke','duke ellington','huey p newton','denzel washing','will smith','marvin gaye','bill withers','prince roger nelson','henry louis gates jr','frederick douglas','alexander pushkin','alexandre dumas','thomas alexander dumas','nina simone','etta james','vicente guerrero','sylvester james gates','dr daniel hale williams','guion s bluford','marie joseph angelique','toussaint louverture','patrice lumumba','nat turner','jean jacques dessalines','dutty boukman','aime cesaire','chokwe lumumba','assata shakur','angela davis','q tip','etheridge knight','charles mingus','beyonce','serena williams','sade','john coltrane','barkley l hendricks','sun ra','ornette coleman','gil scott heron','alicia keys','de la soul','jean michel basquiat','amiri baraka','bass reeves','bayard rustin','saul williams','bill t jones','fela','frantzfanon','spike lee','muddy waters','slick rick','michael johnson','usain bolt','dan haskett','jackie ormes','floyd norman','earnie barnes','wole soyinka','leopold senghor','junot diaz','ben okri','amilcar cabral','nelson mandela','miriam makeba','toni morisson','cheikh anta diop','john ogbu','mo ibrahim','mansa musa','queen idia','pele','didier drogba','hakeem olajuwon','nina simone','whitney houston','marcus garvey','jack johnson','octavia butler','josephine baker','dwayne mcduffie','david banner','quincy jones','charles hamilton houston','oliver hill','thurgood marshall','ruth simmons','mary mcleod bethune','sojourner truth','leymah gbowee','wilma rudolph','ruby bridges','hiram revels','joseph rainey','alice waker','harriet tubman','phillis wheatly','nick cave','henry ossawa tanner','thomas sowell','bayanard rustin','benjamin zephaniah','bayard rustin','ta nehisi coates','miles davis','kwame ture','fred hampton']
images = []
count = len(people)
for idx,person in enumerate(people):
	query_string = person
	bing = BingSearch(key)
	params = {'ImageFilters':'"Face:Portrait+Size:Medium"',
			  '$format': 'json',
			  '$top': 1,
			  '$skip': 0}
	image = bing.search('image',query_string,params).json()
	print 'getting image for %s, %s of %s' % (person,idx,count) 
	im_url = image[u'd'][u'results'][0][u'Image'][0][u'Thumbnail'][u'MediaUrl']
	person_slug = person.replace(' ','-')
	images.append({
		'person':person_slug,
		'url':im_url})
	#print im_url
	response = requests.get(im_url,stream=True)
	with open(person_slug+'.jpg','wb') as out_file:
		shutil.copyfileobj(response.raw,out_file)

#these dimensions are optimized for 135 images. adjust accordingly if you have more or less.
image_files = []
for file in glob.glob("*.jpg"):
    image_files.append(file)
count = 0
size = 100,100
new_im = Image.new('RGB', (2754,510))
for i in xrange(0,2700,102):
	for j in xrange(0,500,102):
		print 'pasting image %s of %s' % (count,len(image_files))
		im = Image.open(image_files[count])
		
		#im.thumbnail(size)
		im = im.resize(size)
		new_im.paste(im, (i,j))

		count += 1

new_im.save("collage.jpg", "JPEG")
