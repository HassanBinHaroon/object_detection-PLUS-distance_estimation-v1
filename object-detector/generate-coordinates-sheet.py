from pathlib import Path
import xlsxwriter


category_label = ['empty', 'person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus', 'train', 'truck', 'boat', 'traffic light', 'fire hydrant', 'stop sign', 'parking meter']

def listToString(lst):
    """ convert from 2D list to string """
    listToStr = ''
    for lst1 in lst:
        print(lst1)
        listToStr=f"({lst1[0]},{lst1[1]})\n"
        # listToStr = listToStr+' '.join([str(elem) for elem in lst1])+'\n'
    return str(listToStr)
    

sum=0
def extract_data_from_labels(folder_path):
    """ 
        [return dictionary of dictionary of list]

        key1 -> frame  : number of frame (1 or 2 ...)
        key2 -> obj    : category id     (car or person ....)

        dict={
             "1":{
               "1":[[0.2 0.5],[0.4 0.4]]
             }
        }
        
        the frame 2 has 2 persons(category_id=1) on upper left corner (0.2,0.5) , (0.4,0.4)
    
    """
    global sum
    sum=0
    from collections import defaultdict

    data_dict = {}
    files = Path(folder_path).glob('*')

    for file in files:
      with open(file) as f:
            filename=file.name.split('.')[0]
            frame=filename.split('_')[-1]
            sum=max(sum,int(frame))

            lines = f.readlines()
            data_dict[frame]=defaultdict(list)

            for obj in lines:                    # obj:  cls_id x_center y_center width hight
                lst=list(obj.split(" "))
                lst=list(map(float,lst))

                data_dict[frame][int(lst[0])].append(lst[1:3])

    return data_dict


def export_excel_sheet(data_dict):
    workbook = xlsxwriter.Workbook('Detected_Objects_Coordinates.xlsx') # name of the Excel sheet
    worksheet = workbook.add_worksheet()


     #initialize
    for i in range(0,sum+2,1):
      for y in range(14):
        if y== 0:worksheet.write(i,y,i)
        else :worksheet.write(i,y,"--")

    # write the header
    for i in range(14):
      if i==0:
          worksheet.write(0,i,"frame")
      else:
          worksheet.write(0,i,category_label[i])


    # Write the data
    for frame,value1 in data_dict.items():
          index_with_data={}                     # In each row I will store the data in some columns and the rest I will store underscore

          for obj,value2 in value1.items() :
              listoflist=value2
              index_with_data[int(obj)+1]=listToString(listoflist)
          
          for i in range(0,14):
              if i==0:
                worksheet.write(int(frame)+1,i,int(frame)+1)
                continue    
              if i in index_with_data.keys():worksheet.write(int(frame)+1,i,index_with_data[i])    
      
    workbook.close()


path=f"/content/Graduation-Project/object-detector/runs/detect/exp/labels"
data=extract_data_from_labels(path)
export_excel_sheet(data)
