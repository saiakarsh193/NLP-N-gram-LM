# NLP N-gram Language Model  

Implementing N-Gram Language Model for NLP Assignment 1.  
Smoothing is done using various methods like Laplace, Witten-Bell and Kneser-Ney.  

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
and it will give the probability of the sentence calculated using the ngram table made from the corpus and the smoothing technique.  

Uncomment this line to log the perplexity values for test and train set  
```python
# uncomment this line to log the perplexity values for train and test set
# lm.log("") # the parameter is LM id value for naming the file
```  

## References  
- [Dan Jurafsky](https://www.youtube.com/playlist?list=PLLssT5z_DsK8HbD2sPcUIDfQ7zmBarMYv)
- [Stanford Docs](https://nlp.stanford.edu/~wcmac/papers/20050421-smoothing-tutorial.pdf)
- [Heidelberg University](https://www.cl.uni-heidelberg.de/courses/ss15/smt/scribe6.pdf)
- [Harvard University](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/tr-10-98.pdf?from=https%3A%2F%2Fresearch.microsoft.com%2F%7Ejoshuago%2Ftr-10-98.pdf)