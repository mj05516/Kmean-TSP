import random
# temp = "124, 123, 121, 117, 116, 103, 91, 93, 74, 21, 18, 22, 10, 12, 27, 31, 49, 55, 50, 42, 30, 32, 35, 44, 54, 52, 53, 37, 24, 26, 33, 57, 28, 29, 51, 61, 67, 107, 118, 120, 115, 112, 110, 108, 48, 46, 43, 47, 70, 83, 79, 81, 77, 68, 66, 73, 84, 100, 64, 45, 39, 40, 56, 41, 38, 58, 92, 95, 97, 105, 106, 96, 88, 9, 3, 5, 15, 19, 34, 60, 72, 69, 75, 78, 102"
# temp = temp.split()

# print(len(temp))
t = [9, 10, 15, 19, 27, 45, 33, 70, 7, 3, 5, 12, 47, 67, 73, 97, 105, 117, 116, 93, 79, 61, 51, 68, 84, 100, 110, 115, 112, 95, 92, 77, 66, 56, 46, 38, 31, 29, 22, 28, 26, 17, 21, 18, 37, 39, 34, 40, 43, 52, 53, 60, 72, 69, 24, 48, 41, 44, 42, 49, 55, 50, 54, 58, 57, 74, 75, 78, 88, 96, 106, 107, 108, 83, 81, 64, 35, 32, 30, 124, 123, 120, 103, 91, 102]
t2 = [52, 55, 50, 42, 31, 15, 5, 9, 10, 12, 27, 22, 57, 70, 100, 110, 115, 117, 116, 108, 107, 66, 37, 39, 43, 44, 49, 54, 51, 61, 81, 83, 88, 84, 68, 77, 103, 102, 91, 72, 17, 26, 24, 21, 18, 69, 96, 93, 95, 97, 60, 33, 28, 29, 45, 79, 92, 106, 105, 120, 124, 123, 112, 73, 56, 53, 46, 41, 35, 30, 19, 32, 47, 75, 78, 74, 64, 67, 58, 48, 38, 40, 34, 7, 3]
t3 = [102, 92, 83, 103, 81, 79, 77, 70, 64, 12, 10, 9, 5, 15, 19, 32, 30, 31, 35, 37, 27, 29, 22, 24, 26, 60, 72, 74, 96, 105, 106, 107, 108, 73, 58, 40, 47, 51, 45, 69, 75, 97, 110, 115, 120, 124, 123, 67, 66, 68, 84, 117, 116, 112, 100, 55, 50, 42, 54, 53, 43, 34, 39, 41, 38, 49, 44, 48, 46, 52, 56, 61, 88, 95, 93, 91, 78, 21, 18, 28, 57, 33, 17, 7, 3]
# find unique values in temp
t3 = t+t2+t3
print(len(t3))
unique_values = set(t3)
print(len(unique_values))

# lst = [1,2,3,4,5,6,7,8,9]
# lst2 = [10]

# print(lst+lst2)

# def crossover(self, seq1: list, seq2: list) -> list:
#         """
#         This method will perform crossover on the parents and return the child. It selects a random range and selects a sublist from the parents
#         and merges them.
#         We have eliminated the possibility of wrong chromosomes. 
#         """
#         bound1 = random.randint(0, len(seq1)-1)
#         bound2 = random.randint(bound1, len(seq1)-1)

#         child = seq1[bound1:bound2]
#         from_parent_2a = seq2[0:bound1]
#         from_parent_2b = seq2[bound2:len(seq2)]

#         for i in range(len(from_parent_2b)):
#             if from_parent_2b[i] in child:
#                 from_parent_2b[i] = seq1[bound2+i]
#         for i in range(len(from_parent_2a)-1,-1,-1):
#             if from_parent_2a[i] in child and from_parent_2a[i] not in from_parent_2b:
#                 from_parent_2a[i] = seq1[i-bound1]
        
#         child = from_parent_2a + child + from_parent_2b

#         for i in range(len(child)):
#             if child.count(child[i]) > 1:
#                 if seq1[i] not in child:
#                     child[i] = seq1[i]
#                 elif seq2[i] not in child:
#                     child[i] = seq2[i]
#                 else:
#                     child[i] = [x for x in seq1 if x not in child][0]
        
#         # check if the child is valid
#         for each in child:
#             assert child.count(each) == 1

#         return child