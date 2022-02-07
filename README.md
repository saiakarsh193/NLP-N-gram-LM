# NLP N-gram Language Model  

Implementing N-Gram Language Model for NLP Assignment 1.  
Tokenization is done using custom regular expressions and the code can be found in `tokenizer.py`.  
Smoothing is done using various methods like Laplace, Witten-Bell and Kneser-Ney which is in `language_model.py`.  

## Running the code  

```bash
python language_model.py <n_gram_value> <smooth_type> <path_to_corpus>
```

where,  
`<n_gram_value>` is the n gram value the language model will use  
`<smooth_type>` is the smooth type to be used, it can be `l` or `laplace`, `w` or `witten-bell`, `k` or `kneser-ney`  
`<path_to_corpus>` is the path to the corpus file  

It will give a prompt where you need to enter a sentence,  
```bash
input sentence: <sentence>
```  
and it will give the probability of the sentence calculated using the ngram table made from the corpus and the smoothing technique specified.  

**Uncomment** this line to log the perplexity values for train and test set  
```python
# uncomment this line to log the perplexity values for train and test set
# lm.log("") # the parameter is LM id value for naming the file
```  
where the parameter given is used to name the files accordingly like `<rollnumber>_LM_<parameter>_test-perplexity.txt`.  
The log files are created in a new directory `logs/`.  

## Tokenization  
- Urls (`https://example.com`) are replaced with `<URL>` tag.  
- Hashtags (`#trending`) are replaced with `<HASHTAG>` tag.  
- Mentions (`@userid`) are replaced with `<MENTION>` tag.  
- Actions (`\*coughs\*`) are replaced with `<ACTION>` tag.  
- Phone numbers (`+123-456-789-000`) are replaced with `<PHONE>` tag.  
- Emoticons (`:-D`) are replaced with `<EMOTICON>` tag.  
- Currencies and prices (`$123,456.000`) are replaced with `<CURRENCY>` tag.  
- Percentages (`94%`) are replaced with `<PERCENTAGE>` tag.  
- Dates (`12-11-21`) are replaced with `<DATE>` tag.  
- Abbreviations (`lmao`) are replaced with `<ABBREVIATION>` tag.  
- Repeating periods (`....`) are replaced with `,`.  
- Repeating characters are converted to a single character (`!!!` -> `!`).  
- Alphabets occuring more than two times are removed (`Soooo` -> `So`).

## References  
- [Dan Jurafsky and Chris Manning, Stanford](https://www.youtube.com/playlist?list=PLLssT5z_DsK8HbD2sPcUIDfQ7zmBarMYv)
- [Stanford University](https://nlp.stanford.edu/~wcmac/papers/20050421-smoothing-tutorial.pdf)
- [Heidelberg University](https://www.cl.uni-heidelberg.de/courses/ss15/smt/scribe6.pdf)
- [Harvard University](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/tr-10-98.pdf?from=https%3A%2F%2Fresearch.microsoft.com%2F%7Ejoshuago%2Ftr-10-98.pdf)