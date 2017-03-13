key=["k1","k2","k3","k4","k5","k6","k7"]
value=[1,2,3,4,5]
result={}

print('keys: ', key)
print('values: ', value)

if len(key)<=len(value):
    for i in range(0,len(key)):
        result[key[i]]=value[i]

else :
    for i in range(0,len(value)):
        result[key[i]] = value[i]
    for i in range(len(value),len(key)):
        result[key[i]] = 'None'
print('Result dic: ', result)