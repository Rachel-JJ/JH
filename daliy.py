import xlrd
from MySQL_write import config, eachRow
from MySQL_write import w_toexl
from MySQL_write.config import single,multi
from openpyxl import Workbook,load_workbook

def read_exl_process(path,index):
    dic1={}
    process={}
    data=xlrd.open_workbook(path)

    #if there are multiple sheets, change the index num
    table=data.sheet_by_index(index)
    for calNum in range(table.ncols):
        colume=table.col_values(calNum)
        dic1[colume[0]]=colume[1:]

    b=dic1['employee']
    a=len(b)
    c=0
    for i in range(a):
        if a>=1 and i<a-1 and b[i]!=b[i+1] or i==a-1:
            d={}
            for j in dic1.keys():
                if j!='employee':
                    d[j]=dic1[j][c:i+1]
            process[b[i]]=d
            c=i+1
        else:
            process[b[i]]=dic1
    if len(process.keys())==1:
        process[process.keys()[0]].pop('employee')
    return process, table.name

# the consumation of produce in kgs(克数，层数，盒数)
def product_used_meterial(process, level):
    #separate
    trans_num = {48:0,50:0,52:0, 55:0, 57:0,58:0,60:0, 64:0,65:0,68:0,70:0,75:0}
    total_num = {48: 0, 50: 0, 52: 0, 55: 0, 57: 0, 58: 0, 60: 0, 64:0,65: 0, 68: 0, 70: 0,75:0}

    #sum up
    # total_num=0
    # to=0

    consumed_kg = {}
    #calculate the use of meter and kg
    for i in range(len(process['weight'])):
        if process['level'][i] in level:
            now =process['page_num'][i]/1000 * process['numOfBox'][i] * (process['specification'][i]/241)

            # total_num += now
            # to+=process['numOfBox'][i]

            total_num[process['weight'][i]] += process['numOfBox'][i]
            trans_num[process['weight'][i]] += now

            conf=config.names[process['weight'][i]][process['layer'][i]]
            for j in range(3):
                temp_k = conf[j] * now
                if process['weight'][i] not in consumed_kg.keys():
                    consumed_kg[process['weight'][i]] = [0, 0, 0]
                    consumed_kg[process['weight'][i]][j] += round(temp_k,2)

                elif process['weight'][i] in consumed_kg.keys():
                    consumed_kg[process['weight'][i]][j]+= round(temp_k,2)
    return consumed_kg, trans_num, total_num


# the mesurement of raw material usage - meter
def real_used_meterial(raw,trans_num, kg_):
    #一层的不需要算中和下
    total=0
    usage_kg={}
    total_mid=0
    total_bottom=0
    for k in trans_num.keys():
        if k in multi:
            total+=trans_num[k]
    for j in kg_.keys():
        total_mid+=kg_[j][1]
        total_bottom+=kg_[j][2]

    if total_mid==0: total_mid=1
    if total_bottom==0: total_bottom=1
    for i in range(len(raw['weight'])):
        if raw['weight'][i] in multi:
            if raw['weight'][i] not in usage_kg.keys():
                usage_kg[raw['weight'][i]]=[0,0,0]

            usage_kg[raw['weight'][i]][0] += round(raw['up_kg'][i], 2)
            usage_kg[raw['weight'][i]][1] =round((sum(raw['mid_kg']))*kg_[raw['weight'][i]][1]/total_mid,2)
            usage_kg[raw['weight'][i]][2] = round(sum(raw['bottom_kg']) *kg_[raw['weight'][i]][2]/total_bottom, 2)

        elif raw['weight'][i] in single:
            if raw['weight'][i] not in usage_kg.keys():
                usage_kg[raw['weight'][i]]=[0,0,0]
            usage_kg[raw['weight'][i]][0] += round(raw['up_kg'][i], 2)
            usage_kg[raw['weight'][i]][1] = 0
            usage_kg[raw['weight'][i]][2] = 0
    return usage_kg


if __name__== '__main__':
    p_path='/Users/jiaqili/Desktop/嘉禾/六月_生产.xlsx'
    r_path='/Users/jiaqili/Desktop/嘉禾/六月_原纸.xlsx'
    each_path='/Users/jiaqili/desktop/嘉禾/六月_每行.xlsx'


    wb = xlrd.open_workbook(p_path)
    sNum = wb.nsheets

    wb1 = xlrd.open_workbook(each_path)
    sNum1 = wb1.nsheets

    print(sNum,sNum1)
    # for k in range(sNum):
    if sNum>sNum1:
        k=sNum-1
    # if k==11:
    # # r=[3,16]
    # # r = [6, 7, 8, 9, 10]
    # # for k in r:
        process, s_name=read_exl_process(p_path,k)
        raw, r_name= read_exl_process(r_path,k)
        if s_name==r_name:
            print('everything is fine, sheet name is:',s_name)
        else:
            print('not the same sheet, something wrong, process sheet name:{}, raw sheet name{}', format(s_name, r_name))
            print('not the same sheet, something wrong, process sheet name: %s, raw sheet name: %s'
                  %(s_name, r_name))

        print('生产keys',process.keys())
        print('原材料keys',raw.keys())

        for i in process.keys():
            if i !='':
                print('员工',i)
                print(process[i])
                print(raw[i])

                x,y,p=eachRow.product_eachRow(process[i], ['A', 'B'])
                in_kg,trans_num,total_num=product_used_meterial(process[i],['A','B'])
                in_kg_B, trans_num_B,total_num_B = product_used_meterial(process[i], ['C'])
                print('kg',in_kg,in_kg_B)

                r_inKg= real_used_meterial(raw[i],trans_num, in_kg)
                print('r_kg',r_inKg)

                eachRow.more_Specific_used(in_kg, r_inKg, p, process[i]['weight'], s_name, i, x, y)

                diff={}
                for j in in_kg.keys():
                    diff[j]=[0,0,0]
                    for k in range(3):
                        if j in in_kg_B.keys():
                            diff[j][k]+=round(r_inKg[j][k]-in_kg[j][k] -in_kg_B[j][k],2)
                        else:
                            diff[j][k]+= round(r_inKg[j][k] - in_kg[j][k], 2)

                print('diff',diff)
                w_toexl.write_toxl(i, r_inKg, diff,trans_num,total_num,s_name)
