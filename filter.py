import fnmatch
lst = ['this','is','just','a','test']
filtered = fnmatch.filter(lst, 'th?s')
print(filtered)