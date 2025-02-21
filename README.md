[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/2Fvl11oK)
Objective
Your task is to implement a hash table in Python using a list as the underlying data structure. Your hash table will store words and count how many times each word appears in a given dataset. The competition will evaluate the efficiency of your implementation based on collisions, memory usage, and lookup efficiency.

How the Competition Works
Each student/team will receive a list of words. Your hash table must:

Store each word in the dataset, keeping track of how many times it appears.
Allow word lookups to quickly retrieve the count of a given word.
Handle collisions using any method of your choice.
You have learned chaining, but you are free to implement other methods.
At the end of the competition, your implementation will be scored based on the following criteria:

Scoring System
Metric	Explanation	Scoring Method
Buckets Used (Lower is Better)	The total number of buckets used in your hash table, including those in chains. More efficient use of memory results in a lower score.	1 point per bucket used
Collisions (Lower is Better)	Every time two words land in the same bucket, a collision occurs. Fewer collisions mean a better hash function distribution.	1 point per collision
Lookup Efficiency (Lower is Better)	The number of steps needed to find a word in the hash table. If a bucket contains multiple items, more comparisons are needed.	1 point per lookup step
Final Score Calculation
The team with the lowest total score wins:
Final Score=buckets used+collisions+lookup inefficiency

Required Functions
Your hash table implementation must include the following functions:

words_in(word_list) -> (num_buckets, collisions)

Inserts all words from word_list into your hash table.
Returns:
The number of buckets used in the table.
The total number of collisions encountered.
lookup_word_count(word) -> (word_count, lookups)

Searches for word in the hash table.
Returns:
The count of the word in the dataset.
The number of lookups (steps taken to find the word).
