
from django.http import HttpResponse
from django.shortcuts import render
from .models import Product

import numpy as np
import pandas as pd

def homepage(request):
    return render(request, 'home.html',
    {'key':7})

def count(request):
    fulltext = request.GET['fulltext']

    print("fulltext= ", fulltext)

    def dfc(text: str):
        """
        Given a text,
        returns the frequency of the words in the text in a dataframe
        THAT ARE BIGGER THAN 1
        """
        #Splitting the text into a list
        wordlist = text.split()
        worddictionary = {}

        #Creating the wordlist dictionary
        for word in wordlist:
            if word in worddictionary:
                #Increase
                worddictionary[word] += 1
            else:
                #add to the dictionary
                worddictionary[word] = 1

        #Converting worddictionary into a dataframe
        df = pd.DataFrame.from_dict(worddictionary, orient='index')
        #Resetting index to a numerical one for ease of use
        df = df.reset_index()
        #Renaming the old string-valued index
        df = df.rename(columns={'index':'word'})
        #Defining two functions (over empty variables) to replace commas and dots
        remover = lambda x: x.replace(',','')
        remover2 = lambda x: x.replace('.','')
        #Using ( too many lines) to apply the functions
        df['word'] = df['word'].apply(remover)
        df['word'] = df['word'].apply(remover2)
        #Row-wise Subselection and assignment to remove words with a frequency smaller than 2
        df = df[df[0] > 2]
        #Renaming word frequncy
        df = df.rename(columns={0:'Frequency'})

        return df

    df = dfc(fulltext)
    print("This is the dataframe \n", df)


    return render(request, 'count.html', {'fulltext':fulltext, 'dataframe':df},  )
