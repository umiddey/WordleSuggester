#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import numpy as np

class WordleSuggester:
    
    def __init__(self):
        
        pass
 
    
    def prefilter_words(self):    
        with open('E:/Projects/Wordle finder/all_words.txt') as f:
            all_words = f.readlines()
        filtered_words = [re.sub('[^a-zA-Z0-9]+', '', i) for i in all_words] # Removing special characters
        five_letter_words = [word for word in filtered_words if len(word) == 5] # Keeping only 5 letter words
        five_letter_words_low  = pd.DataFrame([i.lower() for i in five_letter_words], columns = ['words']) # Setting all words to lower case
        five_letter_words_low.drop_duplicates(inplace = True) # Dropping duplicates, if any
        
        return five_letter_words_low
        
    def position_known_potential(self, five_letter_words_low):   
        
        
        # if letter position known
        print('Are position(s) of any letter(s) known: Input Y or N:')
        position_indicator = input().lower()
        temp_letter = ''
        temp_position = 0
        
        if position_indicator == 'n':
            return pd.DataFrame()
        else:
            position_indicator = 1
            known_count = 0
            position_tracker = []
            letter_tracker = []

            while position_indicator != 0:
                print('Enter number of positions for which letters are known: ')
                known_count = int(input())

                letter_position = 1
                if known_count == 0:
                    print('Can not have 0 known positions!')
                    break
                else:
                
                    while known_count != 0:
                        print(f'Enter position number of known letter number {letter_position}:')
                        temp_position = int(input()) - 1 
                        position_tracker.append(temp_position)
                        print('Enter known letter:')   
                        temp_letter = input()
                        letter_tracker.append(temp_letter)
                        known_count -= 1

                        letter_position += 1


                position_indicator -= 1
                
                poten_word = pd.DataFrame(columns=['words'])

                for word in five_letter_words_low['words']:
                    for i, letter in enumerate(letter_tracker):
                        if word[position_tracker[i]] == letter_tracker[i]:
                            temp = pd.DataFrame([word], columns = ['words'])
                            poten_word = poten_word.append(temp)


                poten_word = poten_word[poten_word['words'].isin(poten_word['words'].value_counts()[poten_word['words'].value_counts() == len(letter_tracker)].index)]
                poten_word.drop_duplicates(inplace = True)
                
        return poten_word
    
    def position_unknown_potential(self, five_letter_words_low):
        
        
        print('Are there letters with unknown positions: Input Y or N:')
        unk_position_indicator = input().lower()
        temp_unk_letter = ''

        if unk_position_indicator == 'n':
            return pd.DataFrame()
        else:
            unk_position_indicator = 1
            unknown_count = 0
            unk_letter_tracker = []

            while unk_position_indicator != 0:
                print('Number of letters with position unknown:')
                unknown_count = int(input())
                if unknown_count == 0:
                    print('Can not have 0 unknown letters!')
                    break
                else:
                    letter_number = 1
                    while unknown_count != 0:
                        print(f'Enter unknown letter {letter_number}')
                        temp_unk_letter = input()
                        if temp_unk_letter in temp_letter:
                            print('This letter is known')
                            continue
                        else:
                            unk_letter_tracker.append(temp_unk_letter)
                            letter_number += 1

                            unknown_count -= 1

                unk_position_indicator -= 1
                
                #for unknown positions

        unk_poten_word = pd.DataFrame()
        for unk_letter in unk_letter_tracker:
            temp = five_letter_words_low[five_letter_words_low['words'].str.contains(unk_letter)]
            unk_poten_word = unk_poten_word.append(temp)

        unk_poten_word = unk_poten_word[unk_poten_word['words'].isin(unk_poten_word['words'].value_counts()[unk_poten_word['words'].value_counts() == len(unk_letter_tracker)].index)]
        unk_poten_word.drop_duplicates(inplace = True)
                
        return unk_poten_word
    
    def run_suggester(self):
        
        five_letter_words_low = self.prefilter_words()
        position_known = self.position_known_potential(five_letter_words_low)
        position_unknown = self.position_unknown_potential(five_letter_words_low)
        
        print(position_known)
        print(position_unknown)
        if position_known.empty:
            return position_unknown
        elif position_unknown.empty:
            return position_known
        else: 
            potential_words = pd.DataFrame(poten_word.append(unk_poten_word), columns = ['words'])
            return potential_words[potential_words.duplicated()]

    
    

