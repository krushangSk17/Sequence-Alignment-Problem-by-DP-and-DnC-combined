# ********* IMPORT LIBRARIES ********* 

import sys  # System library to taken command line input
import time # Time library to check the runtime 
import psutil # Process and System utility library to check the memory consumed 
# import basic # Calling the basic algorithm 

# missCost = MissMatchCost 

missCost = {
    'A': {'A' : 0 ,   'C' : 110, 'G' : 48,  'T' : 94},
    'C': {'A' : 110 , 'C' : 0,   'G' : 118, 'T' : 48},
    'G': {'A' : 48 ,  'C' : 118, 'G' : 0,   'T' : 110},
    'T': {'A' : 94 ,  'C' : 48,  'G' : 110, 'T' : 0}
}

gapCost = 30

# ******** String Generator : STARTS ********

def strgenerate(strings, numbers):
    s1 = strings[0]
    s2 = strings[1]

    # s_m = StringMaker
    s_m_1 = numbers[0]
    s_m_2 = numbers[1]

    for i in range(len(s_m_1)):
        s1 = s1[:s_m_1[i]+1] + s1 + s1[s_m_1[i]+1:]

    for j in range(len(s_m_2)):
        s2 = s2[:s_m_2[j]+1] + s2 + s2[s_m_2[j]+1:]

    return s1,s2

# ******** String Generator : ENDS ********

#############################################

def SolveDp(s1,s2):
    s1_len = len(s1)
    s2_len = len(s2)

    DP = [[0 for _ in range(s1_len + 1)] for _ in range(s2_len + 1)]

    for j in range(s1_len + 1):
        DP[0][j] = gapCost * j
    for i in range(s2_len + 1):
        DP[i][0] = gapCost * i

    for i in range(1, s2_len + 1):
        for j in range(1, s1_len + 1):
            DP[i][j] = min(DP[i - 1][j] + gapCost,
                           DP[i][j - 1] + gapCost,
                           DP[i - 1][j - 1] + missCost[s1[j - 1]][s2[i - 1]])

    # print(DP[s2_len][s1_len])

    s1_point = s1_len
    s2_point = s2_len

    ms1 = ''
    ms2 = ''

    while(s1_point > 0 and s2_point > 0):
        if(DP[s2_point-1][s1_point-1] + missCost[s1[s1_point-1]][s2[s2_point-1]] == DP[s2_point][s1_point]):
            ms1 = s1[s1_point-1] + ms1
            ms2 = s2[s2_point- 1] + ms2
            s1_point -= 1
            s2_point -= 1
        elif(DP[s2_point-1][s1_point] + gapCost == DP[s2_point][s1_point]):
            ms1 = '_' + ms1
            ms2 = s2[s2_point - 1] + ms2
            s2_point-=1
        else:
            ms2 = '_' + ms2
            ms1 = s1[s1_point - 1] + ms1
            s1_point -= 1

    if(s1_point == 0 and s2_point > 0):
        while(s2_point>0):
            ms1 = '_' + ms1
            ms2 = s2[s2_point - 1] + ms2
            s2_point -= 1

    if(s2_point == 0 and s1_point > 0):
        while(s1_point>0):
            ms2 = '_' + ms2
            ms1 = s1[s1_point - 1] + ms1
            s1_point -= 1


    return (DP,ms1,ms2)
#############################################

# ******** Space Efficient Function : STARTS ********

def findTwo(s1,s2):
    s1_len = len(s1)
    s2_len = len(s2)

    DP = [[0 for _ in range(s1_len+1)] for _ in range(2)]

    for j in range(s1_len+1):
        DP[0][j] = gapCost*j

    for i in range(1,s2_len+1):
        DP[1][0] = i*gapCost
        for j in range(1,s1_len+1):
            DP[1][j] = min(DP[0][j] + gapCost,
                           DP[1][j-1] + gapCost,
                           DP[0][j-1] + missCost[s1[j-1]][s2[i-1]])

        for i in range(0,s1_len):
            DP[0][i] = DP[1][i]

    return DP[-1]

# ******** Space Efficient Function : ENDS ********

# ******** Divide and Conquer Function : STARTS ********

def SolveDC(s1,s2):

    s1_len = len(s1)
    s2_len = len(s2)

    if(s1_len <= 2 or s2_len <= 2):
        return SolveDp(s1,s2)[1:]

    s2_left = s2[:s2_len//2]
    s2_right = s2[s2_len//2:]

    minsum = 10**14
    splitpoint = 10**14

    dp_left = findTwo(s1,s2_left)
    dp_right = findTwo(s1[::-1],s2_right[::-1])[::-1]
    
    for i in range(len(dp_right)):
        s = dp_left[i]+dp_right[i]
        if(s<=minsum):
            minsum = s
            splitpoint = i
    
    s1_left = s1[:splitpoint]
    s1_right = s1[splitpoint:]

    (s1_left_out,s2_left_out) = SolveDC(s1_left,s2_left)
    (s1_right_out,s2_right_out) = SolveDC(s1_right,s2_right)

    return (s1_left_out + s1_right_out, s2_left_out + s2_right_out)

# ******** Divide and Conquer Function : ENDS ********


# ******** INPUT DATA : STARTS ********

input_file = sys.argv[1]    # Taking input file from command line arguments
output_file = sys.argv[2]   # Taking output file from command line arguments

infile = open(input_file, 'r')  # Reading the input file in read mode

input_data = infile.read().split('\n')  # Reading the whole data from the input file

strings = []
numbers = [[],[]]

for iter in input_data:
    if(iter.isalpha()):
        strings.append(iter)
    if(iter.isnumeric()):
        if(len(strings) == 1):
            numbers[0].append(int(iter))
        else:
            numbers[1].append(int(iter))

# ******** INPUT DATA : ENDS ********

# ******** String Generator function call ********

s1,s2 = strgenerate(strings,numbers)

##################################################################################
##################################################################################
##################################################################################
##################################################################################
##################################################################################
##################################################################################
##################################################################################


# print('main inputs : s1 :: ',s1)
# print('main inputs : s2 :: ',s2)

# ******** Calculating time and memory : START ********

start_time = time.time() 
process = psutil.Process()

# ******** Calling SolveDC function ********

output = []
for i in SolveDC(s1,s2):
    output.append(i)
    # print(i)
# print(output)

# for test purpose
# print('sequence matching cost ne sequence cost :::: ',basic.SolveDp(output[0],output[1])[0][-1][-1])

# print('sequence matching cost optimal :::: ',findTwo(s1,s2)[-1])
# print('True output ::: ')
# basic.SolveDp(s1,s2)[1:]

end_time = time.time()
time_taken = (end_time - start_time)*1000

memory_info = process.memory_info()
memory_consumed = int(memory_info.rss/1024)

# ******** Calculating time and memory : END ********

# ******** OUTPUT DATA : START ********

outfile = open(output_file,"w")

outfile.write(str(findTwo(s1,s2)[-1])+'\n')
outfile.write(output[0]+'\n')
outfile.write(output[1]+'\n')
outfile.write(str(time_taken)+'\n')
outfile.write(str(memory_consumed))

outfile.close()
infile.close()

# ******** OUTPUT DATA : ENDS ********