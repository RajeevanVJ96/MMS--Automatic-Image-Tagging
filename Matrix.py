import csv
import heapq
import pandas as pd
import math
import copy
from pprint import pprint

tags = {}                                    # stores the co occurrence matrix
photos_with_tags = {}                        # stores all the photos and their tags as a list
tags_photos = {}                             # stores all the tags and the no of images they are tagged in
idf_tags = {}                                # stores all the tags with their co occurrence values*idf values

# opening the tags.csv to add them to a dictionary using a csv reader to read the file line by line
# with each line, a new tag is added and a second for loop loops through the tags dictionary to add
# all the tags to each dictionary value of the tags so each tag has a dictionary hold all the tags
# as the key with values being the number of co occurrences.

with open('tags.csv', 'rb') as csvfile:
    reader = csv.reader(csvfile)
    for i in reader:
        tags[i[0]] = {}
    for i in tags:
        for j in tags:
            values = tags.get(i)
            values[j] = 0
    csvfile.close()

# opening the photos_tag.csv file to add all the photos to a dictionary along with their tags in a list as their value.
# the first loop adds the images to the dictionary and the conditional is used to eliminate duplicate additions. The
# second file opening and for loops are used to add the tags for each image to a list and add them as the photo's value
# in the dictionary.
	
with open('photos_tags.csv', 'rb') as csvfile:
    reader = csv.reader(csvfile)
    for i in reader:
        if i[0] not in photos_with_tags:
            photos_with_tags[i[0]] = []
    csvfile.close()

with open('photos_tags.csv', 'rb') as csvfile:
    reader = csv.reader(csvfile)
    for i in reader:
        x = photos_with_tags.get(i[0])
        if i[1] not in x:
            x.append(i[1])
    csvfile.close()

with open('tags.csv', 'rb') as csvfile:
    reader = csv.reader(csvfile)
    for i in reader:
        tags_photos[i[0]] = i[1]
    csvfile.close()

# x = tags.get('red')
# x['red']+=1


def create_matrix():
    for i in tags:                                                # loop through tags dictionary
        for j in photos_with_tags:                                # loop through dictionary with pics and their list
            x = photos_with_tags.get(j)                           # of tags. get the current photo's list of tags
            if i in x:                                            # check if tag exists for the current pic
                for k in x:                                       # if so loop through the list
                    if k != i:                                    # if the current index is not equal to the tag then
                        y = tags.get(i)                           # find tag in current tags dictionary of tags and add
                        y[k] += 1                                 # 1 to its value
    data = pd.DataFrame(tags)
    data.to_csv("matrix.csv")

# returns the top 5 recommended tags for a given tag


def top_5(name):
    x = tags.get(name)                                            # get the co occurrence for the required tag
    y = heapq.nlargest(5, x, key=x.get)                           # get the top 5 tag co occurring tags and puts them in
    for i in y:                                                   # a list set to var y. The for loop loops through this
        print "%s: %d" % (i, x.get(i))                            # list and prints out the tag and co occurrence.


# calculate the idf value for a tag given the tag and the total number images
# in a collection. The idf value is then multipled by the co occurrence value
# for each of the tags in the given tag's dictionary.


def tfidf(tag, images):
    idf_tags = copy.deepcopy(tags)                                # create a copy of the tags dictionary
    tag_in_question = idf_tags.get(tag)                           # get the dictionary of tags for the current tag
    for i in tag_in_question:                                     # in question from the new dictionary and loop
        images_tagged = tags_photos.get(i)                        # get the number of images the current tag in loop
        idf_value = math.log(images / int(images_tagged))         # appears in and calculate the idf value using above
        tag_in_question[i] *= idf_value                           # value and total images. Then multiply the current
    top5 = heapq.nlargest(5, tag_in_question, key=tag_in_question.get)  # tag's value in the copied dictionary by the
    for j in top5:                                                # idf  value. get the top 5 tags and store in list
        print "%s :%.3f" % (j, tag_in_question.get(j))            # and loop through list and print

create_matrix()                                                   # function call to create the co occurrence matrix
print "Task 2"
print "Water:"
top_5('water')                                                    # calling the top5 function for each of the tags
print "People:"
top_5('people')
print "London:"
top_5('london')

print "Task 3"
print "Water"
tfidf('water', 10000)                                             # calling the tfidf value on all the tags
print "People"
tfidf('people', 10000)
print "London"
tfidf('london', 10000)