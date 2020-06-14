from MySQL_write.config import names
from MySQL_write.w_toexl import write_eachRow

def product_eachRow(process, level):
    x=[]
    y=[]
    z=[]
    for i in range(len(process['weight'])):
        if process['level'][i] in level:
            now = process['page_num'][i]/1000 * process['numOfBox'][i] * (process['specification'][i]/241)
            x.append(now)
            y.append(process['numOfBox'][i])
            conf=names[process['weight'][i]][process['layer'][i]]
            temp=[]
            for j in range(3):
                temp_k = conf[j] * now
                temp.append(round(temp_k,2))
            z.append(temp)
    return x,y,z

def more_Specific_used(kg,r_kg,p,w,SN,n,x,y):
    each_row=[]
    for i in range(len(w)):
        temp=[]
        for j in range(3):
            if kg[w[i]][j]==0:
                temp.append(r_kg[w[i]][j]*0)
            else:
                temp.append(r_kg[w[i]][j]*(p[i][j]/kg[w[i]][j]))
        each_row.append(temp)
    return write_eachRow(SN, n, each_row,x,y)



