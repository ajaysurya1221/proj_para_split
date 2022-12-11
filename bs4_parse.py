from bs4 import BeautifulSoup
from pprint import pprint 
import re
from os import listdir
from os.path import isfile, join
import cssutils
import json
import pprint

def parse_html(html_filename, obj_id):
    final_list = []

    with open(html_filename, encoding='utf-8') as fp:
        soup = BeautifulSoup(fp, "html5lib")


        selectors = {}

        for styles in soup.select('style'):
            css = cssutils.parseString(styles.encode_contents())
            for rule in css:
                if rule.type == rule.STYLE_RULE:
                    style = rule.selectorText
                    selectors[style] = {}
                    for item in rule.style:
                        propertyname = item.name
                        value = item.value
                        selectors[style][propertyname] = value
        # print(selectors)
        classes_to_avoid = []
        for key, value in selectors.items():
            fontsize_str = value
            if 'font-size' in value:
                font_size = fontsize_str['font-size']
                font_size_int = int(float(font_size.replace("pt", "")))
                if font_size_int < 7:
                    new_key = key.replace('.', '')
                    classes_to_avoid.append(new_key)
        # print(classes_to_avoid)

        #remove all span tags
        for span_tag in soup.findAll("span"):
            span_tag.decompose()

        for tag in soup.findAll("p"):
            if tag.findChildren():
                for inside_tag in tag.findAll(True):
                    class_name = inside_tag.get("class")
                    if class_name != None:
                            # print(class_name[0])
                            # print(classes_to_avoid)
                            if class_name[0] in classes_to_avoid:
                                inside_tag.decompose()
                                print("true")
            else:
            # print(tag)
                class_name = tag.get("class")
                if class_name != None:
                        # print(class_name[0])
                        # print(classes_to_avoid)
                        if class_name[0] in classes_to_avoid:
                            tag.decompose()
                            print("true")


        full_para = ""
        for tag_to_check in soup.find_all('p'):

            if tag_to_check.find_parent("li"):
                break
            text_to_check = tag_to_check.get_text()
            # if text_to_check == None:
            #     continue
            text_to_check = text_to_check.strip()
            if (text_to_check).lower() == "leave granted" or (text_to_check).lower() == "leavegranted" or (text_to_check).lower() == "1. leave granted" or (text_to_check).lower() == "1.leave granted" or (text_to_check).lower() == "leave granted.":
                full_para += text_to_check + "\n\n"
                break
        
        # print(full_para)
        for li in soup.select("li"):
            # para_number = li['data-list-text']
            if li.find_parent("li"):
                continue
            flag = 0
            for para in li.select("p"):
                # print(para.previous_sibling)
                if para.previous_sibling == None:
                    para_parent = para.parent
                    if not para.find_parent("td") or not para.find_parent("tr"):
                        print(para_parent)
                    # print(para_parent)
                        para_counter = para_parent['data-list-text']
                    # print(para_counter)
                        para_txt = "\n\n" + para_counter + " "
                        flag = 1
                if para.find_parent("td") or para.find_parent("tr"):
                    continue
                if flag == 0:
                    para_txt = para.get_text().replace("¶", "")
                if flag == 1:
                    para_txt += para.get_text().replace("¶", "")
                    flag = 0
                para_txt = para_txt.strip()
                if not para_txt.endswith("vs.") or not para_txt.endswith("v.") or not para_txt.endswith("V.") or not para_txt.endswith("VS."):
                    if para_txt.endswith(".") or para_txt.endswith(":") or para_txt.endswith(";") or para_txt.endswith('"') or para_txt.endswith("'") or para_txt.endswith("-") or para_txt.endswith("?") or para_txt.endswith('”'):
                        full_para += para_txt + "\n\n"
                    else:
                        full_para += para_txt + " "
                else:
                    full_para += para_txt + " "

            # txtfile.write(full_para)
            if full_para != "":
                split_para = full_para.split("\n\n")
                # print(split_para)
                for ind_para in split_para:
                    temp_append = ind_para.strip()
                    if len(temp_append) != 0:
                        final_list.append({"type":"text","paragraph":temp_append,"original_document_id":obj_id})
                full_para = ""
                        # print("--------------------------------")
                    # json_file.append({"type":"text","paragraph":full_para,"original_document_id":obj_id})
            # txtfile.write("\n" + "--sep--" + "\n")
            if li.find("table"):
                tables = li.find_all("table")
                for table in tables:
                    # txtfile.write("--table--"+ "\n")
                    final_list.append({"type":"html","paragraph":str(table),"original_document_id":obj_id})
                    # txtfile.write("--table_end--" + "\n")
        reversed_end = []
        for p in reversed(soup.find_all()):
            if p.find_parent('li') or p.find_parent('ol'):
                break
            reversed_end.append(" ".join(p.text.split()))
        if reversed_end!=[]:
            for final_end in reversed(reversed_end):
                full_para = final_end.strip()
                if full_para == "":
                    continue
                final_list.append({"type":"text","paragraph":full_para,"original_document_id":obj_id})
                # txtfile.write("--sep--" + "\n")

    return final_list


def get_split(filename, obj_id):
    # filename = "sup_del_htmls/17.pdf.html"
    # obj_id = "6390846595228b5787e84de3"
    list_res = parse_html(filename, obj_id)
    json_object = json.dumps(list_res, indent=2)
    
    return json_object