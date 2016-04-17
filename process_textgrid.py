#!/usr/local/bin/python2.7
# -*- coding: utf-8 -*-

import codecs, re, sys, argparse, string, operator

from mohawk_word import mohawk_word
from glob import glob
from os import makedirs
from os.path import exists
from subprocess import call

reload(sys)
sys.setdefaultencoding("utf-8")

UTF8Writer = codecs.getwriter('utf8')
sys.stdout = UTF8Writer(sys.stdout)


class Mohawk_word(object):
	text = None
	xmin = None
	xmax = None
	
	def __init__(self, text, xmin, xmax):
        	self.text = text
		self.xmin = xmin
		self.xmax = xmax 
	

def make_segment_file(filename, recording):
#	print "the filename is: " + filename
#	print filename.split(".")
	print "did we get here too"
	segment_prefix = filename.split(".")[0] + "_"
#	print "segment_prefix is: " + segment_prefix
	text_ret = ""	

	utf8 = True
        tiernum = "1"
	if utf8 == True:
        	with codecs.open(filename, 'r', 'utf-8') as f:
                	myList = f.readlines()
	f.close()

        size = len(myList)

        tierstring = "item [" + tiernum + "]:"

	word_list = []
        for x in myList:
		if "xmin" in x:
                        xmin = x.rpartition('= ')[2].rstrip()
                if "xmax" in x:
                        xmax = x.rpartition('= ')[2].rstrip()
                if "text" in x:
                        just_text = re.findall(r'"([^"]*)"', x)
                        if just_text[0] != "":
                                text_ret += just_text[0] + " "
				word_list.append(Mohawk_word(just_text[0], xmin, xmax))
	utterance_array = []
        utterance_xmin = 0
        utterance_xmax = 0

	print "did we get here last?"

	fo = open(filename + ".segment", "wb")
	f1 = open(filename + ".text", "wb")
	for idx, obj in enumerate(word_list):
		if (idx + 1) < len(word_list):
			if (float(word_list[idx + 1].xmin) - float(word_list[idx].xmax)) < .420:
				utterance_xmin = word_list[idx].xmin
				#print "text is: " + str(word_list[idx].text) + " next word text is: " + str(word_list[idx + 1].text) + " difference is: " + str(float(word_list[idx + 1].xmin) - float(word_list[idx].xmax))
				utterance_array.append(word_list[idx].text)
			else:
				utterance_array.append(word_list[idx].text)
				utterance_xmax = word_list[idx].xmax
				print "begin time: " + str(utterance_xmin) + " utterance max: " + str(utterance_xmax) + " utterance array: " + str(utterance_array)
				utterance = " ".join(utterance_array)
				print utterance
				xmin = "%.2f" % float(utterance_xmin)
				xmin_ = xmin.split(".")
				xmin_ = xmin_[0] + "_" + xmin_[1]
				
                                xmax = "%.2f" % float(utterance_xmax)
                                xmax_ = xmax.split(".")
                                xmax_ = xmax_[0] + "_" + xmax_[1]
				#fo.write(segment_prefix + xmin_ + "-" + xmax_ + " " + recording + " " + str(xmax) + " " + str(xmin) + "\n")
				fo.write(segment_prefix + xmin_ + "-" + xmax_ + " " + recording + " " + str(xmin) + " " + str(xmax) + "\n")
				print segment_prefix + xmin_ + "-" + xmax_ + " " + utterance + "\n"
				f1.write(segment_prefix + xmin_ + "-" + xmax_ + " " + utterance + "\n")
				del utterance_array[:]
	
	fo.close()
	f1.close()
	return

def ortho_to_arp(mohawk_orth):

        mohawk_arp = mohawk_orth
	
	mohawk_arp = re.sub(r"'", ur"’", mohawk_arp)
	mohawk_arp = re.sub(r"’", ur"’", mohawk_arp)
	#removing all the down stress TODO: fix this
	mohawk_arp = re.sub(ur"’", ur"GS ", mohawk_arp)
	mohawk_arp = re.sub(ur"È", ur"E", mohawk_arp)
	mohawk_arp = re.sub(ur"Ì", ur"I", mohawk_arp)
	mohawk_arp = re.sub(ur"Ò", ur"O", mohawk_arp)
	mohawk_arp = re.sub(ur"À", ur"A", mohawk_arp)


	#should check if the word has the following patterns, EY 
	mohawk_arp = re.sub(ur"EY", ur"E Y", mohawk_arp)

	#print "the beginning mohawk_arp is: " + mohawk_arp
        mohawk_arp = re.sub(ur":", ur" ", mohawk_arp)
        mohawk_arp = re.sub(ur"(O|Ó|E|É)N(I|Í|O|Ó|ON|ÓN|A|Á|E|É|EN|ÉN)", ur"\1N \2", mohawk_arp)
        #mohawk_arp = re.sub(ur"(o|Ó|e|É)n(t|k|ts|s|n|r|w|y|h|’)", ur"\1N \2", mohawk_arp)
        #print "the mohawk_arp after is: " + mohawk_arp
        mohawk_arp = re.sub(ur"K(I|Í|O|Ó|ON|ÓN|A|Á|E|É|EN|ÉN)", ur"G \1", mohawk_arp)
        mohawk_arp = re.sub(ur"K", ur"K ", mohawk_arp)
#	print "mohawk: " + str(mohawk_arp)
        mohawk_arp = re.sub(ur"T(I|Í|O|Ó|[ON]|[ÓN]|A|Á|E|É|EN|ÉN)", ur"D \1", mohawk_arp)
        mohawk_arp = re.sub(ur"TS", ur"JH ", mohawk_arp)
        mohawk_arp = re.sub(ur"T", ur"T ", mohawk_arp)
        mohawk_arp = re.sub(ur"^S(I|Í|O|Ó|ON|ÓN|A|Á|E|É|EN|ÉN)", ur"Z \1", mohawk_arp)
        mohawk_arp = re.sub(ur"(I|Í|O|Ó|ON|ÓN|A|Á|E|É|EN|ÉN)S(I|Í|O|Ó|ON|ÓN|A|Á|E|É|EN|ÉN)", ur"\1Z \2", mohawk_arp)
	#print "mohawk1: " + str(mohawk_arp)

	mohawk_arp = re.sub(ur'A', ur"AA0 ", mohawk_arp)
	mohawk_arp = re.sub(ur"Í", ur"IY1 ", mohawk_arp)
        mohawk_arp = re.sub(ur"ÓN", ur"UW1 ", mohawk_arp)
        mohawk_arp = re.sub(ur"Á", ur"AA1 ", mohawk_arp)
	#print 'after the A: ' + mohawk_arp
	#mohawk_arp = re.sub(ur'(?<!A,A)(A1?)', ur"AA ", mohawk_arp)
	#print 'again after the A1: ' + mohawk_arp
        mohawk_arp = re.sub(ur"ÉN", ur"AH1 ", mohawk_arp)
#	mohawk_arp = re.sub(ur"E(?!H|N)", ur"EH ", mohawk_arp)
        mohawk_arp = re.sub(ur"ÉH", ur"EY1 H", mohawk_arp)
        mohawk_arp = re.sub(ur"EH", ur"EY0 H ", mohawk_arp)
        mohawk_arp = re.sub(ur"É", ur"EH1 ", mohawk_arp)
	#print "mohawk2: " + str(mohawk_arp) 

        mohawk_arp = re.sub(ur"(?<!I|E)(Y1?)", ur"Y ", mohawk_arp)
	mohawk_arp = re.sub(ur"I(?!Y)", ur"IY0 " , mohawk_arp)
	#mohawk_arp = re.sub(ur"Y(?!1)", ur"Y ", mohawk_arp)
	mohawk_arp = re.sub(ur"Y(?!1|0)", ur"Y ", mohawk_arp)
        mohawk_arp = re.sub(ur"ON", ur"UW0 ", mohawk_arp)
        mohawk_arp = re.sub(ur"ÓN", ur"UW1 ", mohawk_arp)
        #mohawk_arp = re.sub(ur"A", ur"AA ", mohawk_arp)
        mohawk_arp = re.sub(ur"EN", ur"AH0 ", mohawk_arp)
        mohawk_arp = re.sub(ur"E(?!H|Y)", ur"EH0 ", mohawk_arp)
        #print "mohawk3.5: " + str(mohawk_arp)
	#mohawk_arp = re.sub(ur"’", ur"GS ", mohawk_arp)
	#print "mohawk3: " + str(mohawk_arp) 

        mohawk_arp = re.sub(ur"S", ur"S ", mohawk_arp)
        mohawk_arp = re.sub(ur"R", ur"R ", mohawk_arp)
        mohawk_arp = re.sub(ur'([^U])W(1?)', ur'\1W\2 ', mohawk_arp)
	#print "after the negative look behind: " + mohawk_arp
	mohawk_arp = re.sub(ur'O(T|K|TS|S|N|R|W|Y|H|’|G|JH)', ur'O \1', mohawk_arp)
	#print "after the negative look behind behind: " + mohawk_arp 
	mohawk_arp = re.sub(ur'O', ur'OW0 ', mohawk_arp)
	mohawk_arp = re.sub(ur"W([A-Z])", ur"W \1", mohawk_arp)
        #mohawk_arp = re.sub(ur"Y", ur"Y ", mohawk_arp)
        mohawk_arp = re.sub(ur"(?<!E|A)H", ur"H ", mohawk_arp)
        mohawk_arp = re.sub(ur"N", ur"N ", mohawk_arp)
	mohawk_arp = re.sub(ur"AA AA", ur"AA0", mohawk_arp)
	mohawk_arp = re.sub(ur" H ", ur" HH ", mohawk_arp)
	mohawk_arp = re.sub(ur"  ", ur" ", mohawk_arp)
        mohawk_arp = mohawk_arp.rstrip()
	#print "mohawk4_last: " + str(mohawk_arp)

        return mohawk_arp


def read_parse_dict(lexicon_file):
	lex_key_value = {}
	with open(lexicon_file) as f:
		for line in f:
			line_split_by_space = line.split()
			key = line_split_by_space[0]
			#value = line_split_by_space[1:]
			value = " ".join(line_split_by_space[1:])
			lex_key_value[key] = value	
			#print "key: " + str(key) + " the value is: " + str(value)
	return lex_key_value

#def extract_textgrid(filEName, utf8, tiernum):
def extract_textgrid(filename, dictionary):
#def extract_textgrid():
	asr_dict = {}
	utf8 = True
	tiernum = "1"
#	filEName = "./sose.TextGrid"

	text_ret = ""

        if utf8 == False:
                with codecs.open(filename, 'r', 'utf-16') as f:
#                       print "are we in the loops"
                        myList = f.readlines()
        elif utf8 == True:
                with codecs.open(filename, 'r', 'utf-8') as f:
                        myList = f.readlines()

        f.close()

        size = len(myList)

        tierstring = "item [" + tiernum + "]:"

#        print "tierstring is: " + tierstring

        for x in myList:
		#print "the x: " + x
#		xmin = ""
#		xmax = ""
		if "xmin" in x:
			xmin = x.rpartition('= ')[2]
#			print "xmin: " + xmin
		if "xmax" in x:
			xmax = x.rpartition('= ')[2]
                if "text" in x:
                   #    print "text was found."
                        just_text = re.findall(r'"([^"]*)"', x)
			#print just_text
                        if just_text[0] != "":
				text_ret += just_text[0] + " "
	#			print "xmin: " + xmin + " xmax: " + xmax + " text: " + just_text[0]
				#print "text_ret: " + str(text_ret)
                                #print "the text is: " + str(just_text[0])
                		mohawk_arp = ortho_to_arp(just_text[0])
				#print "Mohawk orth: " + str(just_text[0]) + " type: " + str(type(just_text[0])) + "\t\tMohawk arp: " + str(mohawk_arp)
				asr_dict[just_text[0]] = mohawk_arp

		if tierstring in x:
			tierindex = myList.index(x)
                   #    print "\t\t the tierindex: " + str(tierindex)
        
        for y in range (tierindex, size):
#               print "\t\t\t the y: " + str(y)
                if "text" in myList[y]:
                        textindex = y
#                        print "\t\t\t\t textindex: " + str(textindex)
                        break;
        
        textline = myList[textindex]
 
#       print "the textline is: " + str(textline)
        
        tmp = re.search('\"(.+?)\"', textline)
	if tmp:
                text = tmp.group(1)
#               print "in the if tmp: loop and text is: " + text
#        print "we are going to return: " + text

#	print "trying to print the text: " + text_ret
	text_ret = text_ret.rstrip()
#	print asr_dict
#	sorted_asr_dict = sorted(asr_dict.items(), key=operator.itemgetter(0))
	#print sorted_asr_dict[0]
	#print sorted_asr_dict

	fo = open(dictionary + ".updated", "wb")
	if dictionary:
		lexicon_dict = read_parse_dict(dictionary)
#		print lexicon_dict
		combine_dict = dict(lexicon_dict)
                combine_dict.update(asr_dict)
		sorted_asr_dict = sorted(combine_dict.items(), key=operator.itemgetter(0))
		for value, key_list in sorted_asr_dict:
			fo.write(value + " " + key_list + "\n");
    			#print value, key_list
	fo.close()
	print
	print "created file: " + dictionary + ".updated that combined the vocab from the textGrid: " + filename + " and the existing lexicon: " + dictionary
        print
	#return text_ret
	return

def utt2spk(segment_file, speaker):

	fo = open(segment_file + ".utt2spk", "wb")

	with open(segment_file) as f:
                for line in f:
                        line_split_by_space = line.split()
                        utterance = line_split_by_space[0]
			fo.write(utterance + " " + speaker + "\n")                        

	fo.close()

	print
	print "create file: " + segment_file + ".utt2spk with speaker: " + speaker
	print
	return

def main(argv):

	parser = argparse.ArgumentParser(description='Process the textgrids')
	parser.add_argument('-file_name','--file_name', help='file_name', required=False)
	parser.add_argument('-lexicon', help='lexicon file', required=False)
	parser.add_argument('-transcript', help='output transcript file', action='store_true')
	parser.add_argument('-segment', help='create the segment file', required=False)
	parser.add_argument('-speaker', help='speaker of file', required=False)
	parser.add_argument('-recording', help='recording to tie the segment file to', required=False)
	args = parser.parse_args()
    	argsdict = vars(args)
	speaker = argsdict['speaker']
	recording = argsdict['recording']
	segment = argsdict['segment']
	dictionary = argsdict['lexicon']
	transcript = argsdict['transcript']
	filename = argsdict['file_name']


	if speaker:
                utt2spk(segment, speaker)
	if segment:
		print "we are getting here?"
		# in here the segment and text files are created note the segment file is the TextGrid file in this instance it's used kind of as a flag, don't do this at home kids you are better than this
		make_segment_file(segment, recording)	
	elif lexicon:
		# in here the lexicon is updated with new vocab from a textGrid
		trans = extract_textgrid(filename, lexicon)

if __name__ == "__main__":
	main(sys.argv[1:])
