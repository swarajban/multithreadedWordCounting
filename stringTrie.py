__author__ = 'swaraj'

from collections import deque
import os

class StringTrie:
	def __init__(self):
		self.numNodes = 0
		self.root = TrieNode("", None)

	def addString(self, newString):
		currNode = self.root
		for character in newString:
			if character not in currNode.children:
				newNode = TrieNode(character, currNode)
				currNode.children[character] = newNode
				self.numNodes += 1

			currNode = currNode.children[character]

		currNode.count += 1

	def writeToDisk(self, rootPath):
		openSet = deque([(self.root, rootPath)])
		while len(openSet) > 0:
			currNode, currPath = openSet.popleft()
			StringTrie.makeDirectoryRecursive(currPath)
			if currNode.count != 0:
				endFile = open(currPath + '/end', 'a')
				for i in range(currNode.count):
					endFile.write('1')
				endFile.close()

			for character, childNode in currNode.children.iteritems():
				openSet.append((childNode, currPath + '/' + character))


	@staticmethod
	def makeDirectoryRecursive(path):
		if not os.path.exists(path):
			os.makedirs(path)




class TrieNode:
	def __init__(self, character, parent):
		self.count = 0
		self.character = character
		self.children = {}
		self.parent = parent