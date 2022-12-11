from pymongo import MongoClient
from bson.objectid import ObjectId
import requests
import json
from pdf_cleaner import cleaner
from adobe_script import pdf_to_html
from bs4_parse import get_split
import os, shutil

def send_alert(message):
    url = "https://chat.googleapis.com/v1/spaces/AAAAWhLAa-U/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=uYG59110a5c0akF7hOydZznG_bsvdJs-vBJnQoQlkH8%3D"
    payload = json.dumps({
    "text": message
    })
    headers = {
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)
    print(response.status_code)



def clear_folder(folder):
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))


if __name__ == "__main__":
    client = MongoClient("mongodb://172.105.253.134:37268") #mongodb://localhost:37268
    db=client['vs-court-agent']
    collection = db['JudgementsTest']
    # collection2 = db['ParaCollection']
    documents = collection.find({"courtKey": "supremecourt", "paragraphSplitStatus": { "$exists" : False }, "errorStatus":{ "$exists" : False }})
    flag = "supreme"
    for i in documents:
        obj_id = str(i["_id"])
        try:
            counter = counter + 1
            try:
                line = i["cloudData"]["cloudLink"]
            except:
                collection.find_one_and_update({"_id":ObjectId(obj_id)},{"$set":{"CloudLink":False}})
                continue
            line=line.strip()
            response = requests.get(line)
            with open("pdfs/" +"1"+".pdf", 'wb') as f:
                f.write(response.content)
            # start = time.process_time()
            # model_output = inference(PipelineModel, "1.pdf", spark)
            original_filename = "pdfs/" +"1"+".pdf"
            if flag == "supreme":
                cleaned_pdf_filename =  cleaner(original_filename)
                if cleaned_pdf_filename == "nodata":
                    # collection.find_one_and_update({"_id":ObjectId(obj_id)},{"$set":{"paragraphSplitStatus":False, "errorStatus":True}})
                    continue
            else:
                cleaned_pdf_filename = original_filename
                if cleaned_pdf_filename == "nodata":
                    # collection.find_one_and_update({"_id":ObjectId(obj_id)},{"$set":{"paragraphSplitStatus":False, "errorStatus":True}})
                    continue
            
            html_filename = pdf_to_html(cleaned_pdf_filename)

            split_data = get_split(html_filename, obj_id)
            print(split_data)
            with open(str(i["_id"])+".json", "w") as outfile:
                outfile.write(split_data)
        except Exception as e:
            print(str(e)) 


        #     #......your code here


        #     clear_folder("htmls/")
        #     clear_folder("pdfs/")

        #     if split_data == {}:
        #         collection.find_one_and_update({"_id":ObjectId(obj_id)},{"$set":{"paragraphSplitStatus":False, "errorStatus":True}})
        #         continue
        #     collection.find_one_and_update({"_id":ObjectId(obj_id)} , { "$set": { 'paragraphs': split_data ,'paragraphSplitStatus':True} })
        #     if counter%1000==0:
        #         send_alert("completed status :"+str(counter))
        # except Exception as e:
        #     obj_id = str(i["_id"])
        #     if "cloudLink" in i["cloudData"].keys():
        #         line = i["cloudData"]["cloudLink"]
        #         send_alert("Some error occured :"+str(e) + "--Object_id: " + obj_id + "--pdf_link: " + line)
        #     else:
        #         send_alert("Some error occured :"+str(e) + "--Object_id: " + obj_id)
        #     collection.find_one_and_update({"_id":ObjectId(obj_id)},{"$set":{"paragraphSplitStatus":False, "errorStatus":True}})
        #     pass
    
    