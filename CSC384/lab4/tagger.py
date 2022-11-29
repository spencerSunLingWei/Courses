# The tagger.py starter code for CSC384 A4.
# Currently reads in the names of the training files, test file and output file,
# and calls the tagger (which you need to implement)
import os
import sys
import numpy as np

I = np.zeros(76, dtype=float)       # initial probability
T = np.zeros((76,76), dtype=float)  # transition matrix   
M = None                            # emission matrix
E = []                              # a sequnce of observations
E_lst = []
tag_index_dic = {}                  # S -> a set hidden state
index_tag_dic = {}

word_lst = []
tag_lst = []
sentence_lst = []
sentence_lst_tag = []
M_index_dic = {}

cornor_end_set = ('"', "'", ')', ']', '}')  #for initial probability

def tag(training_list, test_file, output_file):
    global I, T, M, E
    # Tag the words from the untagged input file and write them into the output file.
    # Doesn't do much else beyond that yet.
    # print("Tagging the file.")

    # to word_lst, tag_lst, tag_index_dic, index_tag_dic
    for training_file in training_list:
        with open(training_file) as f:
            lines = f.readlines()
            for line in lines:

                # split tag and word
                line_split = line.split(" : ")
                word = line_split[0]
                if line_split[1].find("\n") != -1:
                    tag = line_split[1][:line_split[1].find("\n")]
                else:
                    tag = line_split[1]

                # link tag && index
                tag_index = -1
                if tag not in tag_index_dic:
                    if "-" in tag: # Ambiguity Tag
                        tag_split = tag.split("-")
                        
                        if tag_split[0] > tag_split[1]:
                            new_tag = tag_split[1] + "-" + tag_split[0]
                            if new_tag not in tag_index_dic:
                                tag_index_dic[new_tag] = len(tag_index_dic)
                                index_tag_dic[len(tag_index_dic)-1] = new_tag
                        else:
                            tag_index_dic[tag] = len(tag_index_dic)
                            index_tag_dic[len(tag_index_dic)-1] = tag
                    else:
                        tag_index_dic[tag] = len(tag_index_dic)
                        index_tag_dic[len(tag_index_dic)-1] = tag

                word_lst.append(word)
                tag_lst.append(tag)

    # to sentence_lst
    each_sentence, each_sentence_tag, shuangyinhao_cnt, is_next_end = [], [], 0, False
    for i in range(0, len(word_lst)):
        word = word_lst[i]
        tag = tag_lst[i]
        
        if word == '"':     
            shuangyinhao_cnt += 1

        if is_next_end:     
            is_next_end = False
            continue

        each_sentence.append(word)
        each_sentence_tag.append(tag)

        if word in [".", "?", "!"]:
            if i+1 < len(word_lst) and word_lst[i+1] in cornor_end_set:
                if word_lst[i+1] == '"' and shuangyinhao_cnt%2 == 0:    
                    is_next_end = False # i is end of the sentence
                else:                                                   
                    is_next_end = True # i+1 is end of the sentence
            else:               
                is_next_end = False # i is end of the sentence
        
            if is_next_end:     
                each_sentence.append(word_lst[i+1])
                each_sentence_tag.append(tag_lst[i+1])

            # print(" ".join(each_sentence)) # debug
            sentence_lst.append(each_sentence)
            sentence_lst_tag.append(each_sentence_tag)
            each_sentence = []
            each_sentence_tag = []
    
    # print(len(sentence_lst)) # debug

    # construct HMM
    M = np.zeros((76,len(set(word_lst))), dtype=float) # emission matrix
    for i in range(0, len(sentence_lst)):
        word = sentence_lst[i][0]
        tag = sentence_lst_tag[i][0]

        # initial probability
        if tag not in tag_index_dic:
            new_tag = tag.split("-")[1] + "-" + tag.split("-")[0]
            tag_index = tag_index_dic[new_tag]
        else:
            tag_index = tag_index_dic[tag]
        I[tag_index] += 1

        # emission matrix
        if word in M_index_dic:
            word_index = M_index_dic[word]     
        else:
            word_index = len(M_index_dic)
            M_index_dic[word] = word_index
        M[tag_index][word_index] += 1

        for j in range(1, len(sentence_lst[i])):
            word = sentence_lst[i][j]
            tag = sentence_lst_tag[i][j]
            pre_word = sentence_lst[i][j-1]
            pre_tag = sentence_lst_tag[i][j-1]

            # transition matrix
            if tag not in tag_index_dic:
                new_tag = tag.split("-")[1] + "-" + tag.split("-")[0]
                tag_index = tag_index_dic[new_tag]
            else:
                tag_index = tag_index_dic[tag]
            
            if pre_tag not in tag_index_dic:
                pre_new_tag = pre_tag.split("-")[1] + "-" + pre_tag.split("-")[0]
                pre_tag_index = tag_index_dic[pre_new_tag]
            else:
                pre_tag_index = tag_index_dic[pre_tag]

            T[pre_tag_index][tag_index] += 1

            # emission matrix
            if word in M_index_dic:
                word_index = M_index_dic[word]     
            else:
                word_index = len(M_index_dic)
                M_index_dic[word] = word_index
            M[tag_index][word_index] += 1

    # # Normalization
    I = I / np.linalg.norm(I)

    for i in range(0, len(T)):
        sum = np.sum(T[i])
        if sum != 0:
            T[i] /= sum
        sumM = np.sum(M[i])
        if sumM != 0:
            M[i] /= sumM
    
    # new_M = M.T
    # for i in range(0, len(new_M)):
    #     sumM = np.sum(new_M[i])
    #     if sumM != 0:
    #         new_M[i] /= sumM
    
    # M = new_M.T

    # construct Viterbi
    # S -> tag_index_dic.keys
    # E -> all words need to label
    temm = np.sum(M, axis=1)[:, None]
    if np.sum(temm) != 0:
        temm /= np.sum(temm)

    with open(test_file) as f:
        lines = f.readlines()
        for line in lines:
            if line.find("\n") != -1:
                line = line[:line.find("\n")]
            E.append(line)
                    
            if line not in M_index_dic:
                M_index_dic[line] = len(M_index_dic)
                M = np.append(M, temm, axis = 1)

    # break input test file to sentence / word
    each_sentence, shuangyinhao_cnt, is_next_end = [], 0, False
    for i in range(0, len(E)):
        word = E[i]
        
        if word == '"':     
            shuangyinhao_cnt += 1

        if is_next_end:     
            is_next_end = False
            continue

        each_sentence.append(word)

        if word in [".", "?", "!"]:
            if i+1 < len(E) and E[i+1] in cornor_end_set:
                if E[i+1] == '"' and shuangyinhao_cnt%2 == 0:    
                    is_next_end = False # i is end of the sentence
                else:                                                   
                    is_next_end = True # i+1 is end of the sentence
            else:               
                is_next_end = False # i is end of the sentence
        
            if is_next_end:     
                each_sentence.append(E[i+1])
                each_sentence_tag.append(E[i+1])

            # print(" ".join(each_sentence)) # debug
            E_lst.append(each_sentence)
            each_sentence = []

    # viterbi algorithm
    # print("Start Viterbi")
    final_word = []
    final_tag = []
    for each_E in E_lst:
        final_sub_word, final_sub_tag = viterbi(each_E)
        final_word.extend(final_sub_word)
        final_tag.extend(final_sub_tag)
    
    # write output path to file
    with open(output_file, 'w') as f:
        for i in range(0,len(final_word)):
            if i < len(final_word)-1:
                f.write(final_word[i] + " : " + final_tag[i] + "\n")
            else:
                f.write(final_word[i] + " : " + final_tag[i])

def viterbi(E):
    output_word_lst = []
    output_tag_lst = []

    prob = np.zeros((len(E), 76), dtype=float)
    prev = np.full((len(E), 76), "", dtype='<U1')

    # Determine values for time step 0
    for tag in tag_index_dic:
        tag_index = tag_index_dic[tag]
        
        word = E[0]
        if word in M_index_dic:             word_index = M_index_dic[word]
        else:                               print("ERROR!!! test word not in training word, no emission value")

        prob[0][tag_index] = I[tag_index] * M[tag_index][word_index]
        prev[0][tag_index] = None
            
    # Normilization
    sum = np.sum(prob[0])
    if sum != 0:
        prob[0] /= sum

    # For time steps 1 to length(E)-1, find each current state's most likely prior state x.
    for t in range(1, len(E)):  # time stamp
        word = E[t]              # current word -> e_t
        if word in M_index_dic:         word_index = M_index_dic[word]
        else:                           print("ERROR!!! test word not in training word, no emission value")

        for tag in tag_index_dic:  # if current word is current tag -> S_t
            tag_index = int(tag_index_dic[tag])
            word_index = int(word_index)

            x = np.argmax(prob[t-1, :] * T[:, tag_index].T * M[tag_index, word_index])
            prob[t, tag_index] = prob[t-1, x] * T[x, tag_index] * M[tag_index, word_index]
            prev[t, tag_index] = x

        # Normilization
        sum = np.sum(prob[t])
        if sum != 0:
            prob[t] /= sum

    max_prob_index_lst = np.argmax(prob, axis=1) 
    for i in range(0, len(E)): # for each word in each sentence
        max_pro_index = max_prob_index_lst[i]
        word = E[i]
        tag = index_tag_dic[max_pro_index]

        output_word_lst.append(word)
        output_tag_lst.append(tag)

    return output_word_lst, output_tag_lst

if __name__ == '__main__':
    # Run the tagger function.
    print("Starting the tagging process.")

    # Tagger expects the input call: "python3 tagger.py -d <training files> -t <test file> -o <output file>"
    parameters = sys.argv
    training_list = parameters[parameters.index("-d")+1:parameters.index("-t")]
    test_file = parameters[parameters.index("-t")+1]
    output_file = parameters[parameters.index("-o")+1]
    # print("Training files: " + str(training_list))
    # print("Test file: " + test_file)
    # print("Output file: " + output_file)

    # Start the training and tagging operation.
    tag (training_list, test_file, output_file)