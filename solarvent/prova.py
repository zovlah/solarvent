'''
Created on 15. 5. 2017.

@author: zovlah
'''
def trailing_zeroes(broj):
    s = str(broj)
#    s.rstrip('0') if '.' in s else s
    if '.' in s:
        s = s.rstrip('0')
        
    if s.endswith('.'):
        s = s[:-1]
    
    return s

print trailing_zeroes(100.0)
print trailing_zeroes(34.8000)
print trailing_zeroes(100.0800)
print trailing_zeroes(100)
