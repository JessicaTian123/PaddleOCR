import copy
import json
filename = './inference_results/system_results.txt'
# 读取文件中的数据
Data = []
with open(filename, encoding='utf-8') as inputData:
    for line in inputData:
        try:
            Data.append(json.loads(line.rstrip('\n')))
        except ValueError:
            print("Skipping invalid line {0}".format(repr(line)))

lines: object = Data[0]
inputData.close()
# 解决中文文本中含有 ';'的情况
for items in lines:
    if(items['transcription'][-1:] == '；'):
        strr = items['transcription']
        strr = strr[:-1] + ';'
        items['transcription'] = strr
# lines = items
list_1 = []
count = 0
index = 0
num = 25
str_1 = ''
str_2 = ''
j = count + 1
# 遍历每一行语句
# while(count + 1 < len(lines)):
#     j = count + 1
#     position_i = lines[count]['points']
#     position_j = lines[j]['points']
#     # 两行语句横纵坐标中点
#     h_i = (position_i[1][1] + position_i[2][1]) / 2
#     h_j = (position_j[1][1] + position_j[2][1]) / 2
#     r_i = (position_i[0][0] + position_i[1][0]) / 2
#     r_j = (position_j[0][0] + position_j[1][0]) / 2
#     if(abs(r_i-r_j) < 10 and (h_j - h_i) < num):
#         while (lines[count]['transcription'][-1:] != ';') and (count + 1 < len(lines)):
#             # 当在多行中间遇到Yes或No时
#             if(lines[j]['transcription'] == 'Y' or lines[j]['transcription'] == 'N' or lines[j]['transcription'] == 'Yes' or lines[j]['transcription'] == 'No'):
#                 list_1.insert(index, lines[count])
#                 index = index + 1
#                 j = count + 2
#             else:
#                 str_1 = lines[count]['transcription'] + lines[j]['transcription']
#                 lines[count]['transcription'] = str_1
#                 #             重新计算位置
#                 i = lines[count]['points'][0][0] + lines[count]['points'][1][0] - lines[count]['points'][0][0] + lines[j]['points'][1][0] - lines[j]['points'][0][0]
#                 lines[count]['points'][1][0] = i
#                 m = lines[count]['points'][3][0] + lines[count]['points'][2][0] - lines[count]['points'][3][0] + lines[j]['points'][2][0] - lines[j]['points'][3][0]
#                 lines[count]['points'][2][0] = m
#                 #             将合并后的字典插入列表中
#                 #             list_1.insert(index, copy.deepcopy(lines[j]))
#                 #             index = index + 1
#                 j = j + 1
#                 if (lines[count]['transcription'][-1:] == ';' and count + 1 < len(lines)):
#                     list_1.insert(index, copy.deepcopy(lines[count]))
#                     index = index + 1
#                     count = count + 1
#                     break
#     elif(lines[count]['transcription'] == 'Y' or lines[count]['transcription'] == 'N' or lines[count]['transcription'] == 'Yes' or lines[count]['transcription'] == 'No'):
#         list_1.insert(index, lines[count])
#         index = index + 1
#         count = count + 1
#     elif (lines[count]['transcription'] == 'NO;'):
#         count = count + 1
#     else:
#         list_1.insert(index, lines[count])
#         index = index + 1
#         count = count + 1
while(count + 1 < len(lines)):
    # j = count + 1
    position_i = lines[count]['points']
    position_j = lines[j]['points']
    p_i = (position_i[1][1] + position_i[2][1])/2
    p_j = (position_j[1][1] + position_j[2][1])/2
    # 当前为yes或No
    if lines[count]['transcription'] == 'Y' or lines[count]['transcription'] == 'N' or lines[count]['transcription'] == 'Yes' or lines[count]['transcription'] == 'No':
        list_1.insert(index, lines[count])
        index = index + 1
        count = count + 1
        j = count + 1
    #     两行间距大于20判断为不是一个框中
    elif((p_j - p_i)>num):
        list_1.insert(index, lines[count])
        index = index + 1
        count = count + 1
        j = count + 1
    #     两行在一个框中
    else:
        if (lines[count]['transcription'][-1:] == ';'):
            list_1.insert(index, lines[count])
            index = index + 1
            count = count + 1
            j = count + 1
        else:
            while(count + 1 < len(lines)):
                # 当在多行中间遇到Yes或No时
                if (lines[j]['transcription'] == 'Y' or lines[j]['transcription'] == 'N' or lines[j]['transcription'] == 'Yes' or lines[j]['transcription'] == 'No'):
                    list_1.insert(index, lines[j])
                    index = index + 1
                    j = count + 2
                    continue
                else:
                    str_1 = lines[count]['transcription'] + lines[j]['transcription']
                    lines[count]['transcription'] = str_1
                    #  重新计算位置
                    i = lines[count]['points'][0][0] + lines[count]['points'][1][0] - lines[count]['points'][0][0] + lines[j]['points'][1][0] - lines[j]['points'][0][0]
                    lines[count]['points'][1][0] = i
                    m = lines[count]['points'][3][0] + lines[count]['points'][2][0] - lines[count]['points'][3][0] + lines[j]['points'][2][0] - lines[j]['points'][3][0]
                    lines[count]['points'][2][0] = m
                    j = j + 1
                    if (lines[count]['transcription'][-1:] == ';' and count + 1 < len(lines)):
                        list_1.insert(index, lines[count])
                        index = index + 1
                        count = j
                        j = count + 1
                        break
# 将'结束语句添加进list_1'
list_1.insert(index, lines[count])
s = ''
for item in list_1:
    s = s + str(item) +'\n'
print(s)
# print(list_1[0])
# for item in list_1:
#     print(item)
with open('./inference_results/deal_results.txt', 'w', encoding='utf-8') as f:
    f.write(s)


