multithreadedWordCounting
=========================

Solving the following code challenge:  
Counting  
You have a 100GB text file and a Linux box with 4GB of RAM and 4 cores. 
Write a program/script that outputs a file listing the frequency of all words
in the file (e.g., a TSV file with two columns &lt;word, frequency>). Note 
that the set of words in the file may not fit in memory.

- Usage: python wordCountTrie.py --textFile lines.txt --outputFile wordFrequency.txt
	- Description: This solution uses the trie data structure and multiple python threads to accomplish the word count task. The steps are as follows:
		1) Split the input file into 4 equal chunks
		2) Spawn 4 python processes that each do the following:
			- Read each file, line-by-line, and word-by-word
			- For each word, insert the word into a Trie in memory
			- After each line is read, determine if we have added too many nodes to the trie in memory
			- If we have, write the trie out to disk using a special directory structure
			- At the end of the file, write the trie out to disk one last time
		3) Wait for all processes to finish working on their own chunk
		4) Traverse the directory structure to find all word frequencies and output to file
	- Assumptions
		- Text file is broken into lines where each line is reasonably small and can be read into memory safely
		- Disk drive has large amount of space
	- External Libraries Used
		- Multiprocessesing library from python
		- Unix split tool to split file into chunks
