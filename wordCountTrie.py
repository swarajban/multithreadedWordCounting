__author__ = 'swaraj'

import argparse
import os
import math
import string
from multiprocessing import Process, Lock
from stringTrie import StringTrie

def main():
	# Parse command line arguments
	parser = argparse.ArgumentParser(description='Word frequency in text file')
	parser.add_argument('-t', '--textFile', help='Input text file', required=True)
	parser.add_argument('-o', '--outputFile', help='Output text file', required=True)
	args = vars(parser.parse_args())

	path = os.getcwd()
	trieRoot = path + "/trieRoot"


	inputFilePath = args['textFile']
	# Creates 4 files called partaa, partab, partac, and partad of equal length
	splitInputFile(inputFilePath)

	# spawn 4 processes that read in files, create tries, and write to disk when they hit X nodes
	diskWriteLock = Lock()
	p1 = Process(target=trieWorker, args=('partaa', trieRoot, diskWriteLock))
	p2 = Process(target=trieWorker, args=('partab', trieRoot, diskWriteLock))
	p3 = Process(target=trieWorker, args=('partac', trieRoot, diskWriteLock))
	p4 = Process(target=trieWorker, args=('partad', trieRoot, diskWriteLock))

	allProcesses = [p1, p2, p3, p4]
	for proc in allProcesses:
		proc.start()

	for proc in allProcesses:
		proc.join()


	# Traverse Trie on disk and output file
	outFilePath = args['outputFile']
	outFile = open(outFilePath, 'a')
	diskTrieToWordCount(trieRoot, outFile)
	outFile.close()

	print "done"

def trieWorker(inputChunkPath, rootPath, lck):
	trie = StringTrie()
	with open(inputChunkPath, 'r') as inputChunk:
		for line in inputChunk:
			line = line.strip()
			# Remove punctuation (http://stackoverflow.com/questions/265960/best-way-to-strip-punctuation-from-a-string-in-python)
			line = line.translate(string.maketrans("",""), string.punctuation)
			line = line.lower()
			words = line.split()
			for word in words:
				trie.addString(word)

			# Once Trie reaches certain number of nodes, write it to disk and create new one
			if trie.numNodes > 1000:
				lck.acquire()
				print "writing to dask before hand"
				trie.writeToDisk(rootPath)
				lck.release()
				trie = StringTrie()
	lck.acquire()
	trie.writeToDisk(rootPath)
	lck.release()


# Creates 4 files called partaa, partab, partac, and partad of equal length
def splitInputFile(inputFilePath):
	numLines = getNumInputFileLines(inputFilePath)
	chunkLength = int(math.ceil(numLines / 4.0))
	os.system('split -l ' + str(chunkLength) + ' ' + inputFilePath + ' part')



def getNumInputFileLines(inputFilePath):
	count = 0
	with open(inputFilePath, 'r') as inputFile:
		for line in inputFile:
			count += 1
	return count



def diskTrieToWordCount(rootPath, outFile):
	for root, dirs, files in os.walk(rootPath):
		for fileName in files:
			filePath = os.path.join(root, fileName)
			word = getWordFromPath(rootPath, filePath)
			wordFrequency = str(getFrequencyFromFile(filePath))
			outFile.write(word + "\t" + wordFrequency + "\n")



def getWordFromPath(rootPath, filePath):
	endIndex = len(rootPath) + 1
	wordPath = filePath[endIndex:-4]
	word = wordPath.replace("/", "")
	return word

def getFrequencyFromFile(filePath):
	with open(filePath) as f:
		return len(f.read())


if __name__ == "__main__":
	main()