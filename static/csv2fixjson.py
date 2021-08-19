#!/home/lich/Workspace/djWeb/bin/python
import argparse
import json

def main():
  parser = argparse.ArgumentParser(description='csv to fixture json')
  parser.add_argument('-csv', dest='csv_file', required=True, help='input csv file')
  parser.add_argument('-o', dest='out_dir', required=False, default='.', help='output dir')
  args = parser.parse_args()
  csv_file = args.csv_file
  out_dir = args.out_dir

  out_list = []
  print("Parsing {}".format(csv_file))
  with open(csv_file,'r') as fh:
    model = "region.Region"
    pk = 1
    for line in fh:
      temp_dict = {}
      temp_dict['model'] = model
      temp_dict['pk'] = pk
      temp_dict['fields'] = {}
      province,city,county,longitude,latitude,zipCode = line.split(',')
      temp_dict['fields']["country"] = "中国"
      temp_dict['fields']["province"] = province
      temp_dict['fields']["city"] = city
      temp_dict['fields']["county"] = county
      temp_dict['fields']["longitude"] = float(longitude)
      temp_dict['fields']["latitude"] = float(latitude)
      temp_dict['fields']["zip_code"] = zipCode.strip()
      out_list.append(temp_dict)
      pk += 1

  out_json = out_dir + '/region.json'
  print("Writing out {}".format(out_json))
  with open(out_json, 'w') as fout:
    json.dump(out_list, fout ,ensure_ascii=False)

if __name__=="__main__":
  main()
