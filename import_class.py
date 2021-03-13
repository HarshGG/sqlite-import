import sqlite3
import json
import csv
import xml

class import_class:

    def import_file(self, filename):
        split=filename.split(".")
        if split[1]=="csv":
            self.import_csv(self, filename)
        elif split[1]=="json":
            self.import_json(self, filename)
        elif split[1]=="xml":
            self.import_xml(self, filename)

    def import_csv(self, filename):
        count=0
        conn = sqlite3.connect('data.sqlite')
        catagories = []
        csv_file = csv.reader(open(filename))
        csv_dict_file = csv.DictReader(open(filename))
        for row in csv_file:
            count += 1
            if count>2:
                break
            if count == 1:
                catagories = row
            elif count == 2:
                tabExists = conn.execute("SELECT count(*) FROM sqlite_master WHERE type='table' AND name='" + filename[0:filename.index(".")]+"';")
                result = tabExists.fetchone()[0]
                if(result==0):
                    s = "CREATE TABLE "+filename[0:filename.index(".")] + \
                        " (id INTEGER NOT NULL, "
                    for index in range(0, len(catagories)):
                        i = catagories[index]
                        if row[index].isnumeric() and len(row[index]) <= 6:
                            s += i+" INTEGER "
                        elif "." in row[index]:
                            s += i+" REAL"
                        else:
                            s += i+" TEXT"

                        if index != len(catagories)-1:
                            s += ", "
                        else:
                            s += ', PRIMARY KEY("id" AUTOINCREMENT))'
                    #print(s)
                    conn.execute(s)
                else:
                    conn.execute("DELETE FROM " + filename[0:filename.index(".")])
        for row in csv_dict_file:
            t = "INSERT INTO "+filename[0:filename.index(".")]+" ("
            for index in range(0, len(catagories)):
                i = catagories[index]
                t += i

                if index != len(catagories)-1:
                    t += ", "
                else:
                    t += ")"

            t += " VALUES ("
            for index in range(0, len(catagories)):
                i = catagories[index]
                if(isinstance(row[i], str)):
                    t += '"' + row[i] + '"'
                else:
                    t+= str(row[i])
                if index != len(catagories)-1:
                    t += ", "
                else:
                    t += ");"

                #print(catagories)
            #print(t)
            conn.execute(t)

    def import_json(self, filename):
        _conn = sqlite3.connect('data.sqlite')

        #START CODE TO CHECK IF TABLE EXISTS OR NOT, AND IF NOT THEN DELETE
        tabExists = _conn.execute("SELECT count(*) FROM sqlite_master WHERE type='table' AND name='" + filename[0:filename.index(".")]+"';")
        result = tabExists.fetchone()[0]
        #print(result)
        with open(filename,encoding='UTF-8') as json_file:
            data = json.load(json_file)
            #print(data)
            if(result==0):
                keys = data[0].keys()
                s = "CREATE TABLE "+filename[0:filename.index(".")]+" (id INTEGER NOT NULL, "
                for key in keys:
                    if key.isnumeric() and len(key)<=6:
                        s+= key+ " INTEGER,"
                    elif "." in key:
                        s+=key+" REAL,"
                    else:
                        s+=key+" TEXT,"
                s+= 'PRIMARY KEY("id" AUTOINCREMENT))'
                #print(s)
                _conn.execute(s)
            else:
                _conn.execute("DELETE FROM " + filename[0:filename.index(".")])
            #END CODE TO CHECK IF TABLE EXISTS OR NOT, AND IF NOT THEN DELETE

            #FIRST PART OF INSERTING STATEMENT COMMAND
            keys = data[0].keys()
            initText = "INSERT INTO " + filename[0:filename.index(".")] +"("
            for key in keys:
                initText+=key+","
            initText = initText[0:len(initText)-1]
            initText+=') '

            #INSERTING ALL VALUES
            toExecute = ''
            count = 0
            for row in data:
                toExecute = ''
                count+=1
                toExecute+=initText + " VALUES( "

                for key in keys:
                    if(isinstance(row[key],str)):
                        toExecute+='"' + str(row[key]) + '",'
                    else:
                        toExecute+=str(row[key])+","
                
                toExecute = toExecute[0:len(toExecute)-1]
                toExecute+=");"
                #print(toExecute + " -- " + str(count))
                _conn.execute(toExecute)
        #python runner.py cars.json



    def import_xml(self, filename):
        import xml.etree.ElementTree as ET 
        tree = ET.parse(filename)
        root = tree.getroot()
        catagories=[]
        conn = sqlite3.connect('data.sqlite')
        tabExists = conn.execute("SELECT count(*) FROM sqlite_master WHERE type='table' AND name='" + filename[0:filename.index(".")]+"';")
        result = tabExists.fetchone()[0]
        if(result==0):
            s = "CREATE TABLE "+filename[0:filename.index(".")] + \
                " (id INT NOT NULL"

            for elem in root.iter():
                cata = str(elem)[str(elem).index("'")+1:str(elem).rindex("'")]
                if not cata in catagories:
                    catagories.append(cata)

            #print(catagories)

            count=0

            for st in root.findall('./record'):
                count+=1
                if count==1:
                    for index in range(0, len(catagories)):
                        i = catagories[index]
                        if st.find(i) is not None and st.find(i).text.isnumeric() and len(st.find(i).text) <= 6:
                            s += i+" INTEGER "
                        if st.find(i) is not None and "." in st.find(i).text:
                            s += i+" REAL"
                        else:
                            s += i+" TEXT"
                        if index != len(catagories)-1:
                            s += ", "
                        else:
                            s += 'PRIMARY KEY("id" AUTOINCREMENT))'

                    print(s)
                    conn.execute(s)

            for cta in catagories:
                t = "INSERT INTO "+filename[0:filename.index(".")]+" ("
                for index in range(0, len(catagories)):
                    i = catagories[index]
                    t+=i
                    if index != len(catagories)-1:
                        t += ", "
                    else:
                        t += ")"

                t += " VALUES ("
                for index in range(0, len(catagories)):
                    i = catagories[index]
                    if st.find(i) is not None:
                        if(isinstance(t,str)):
                            t += '"' + st.find(i).text + '"'
                        else:
                            t+=st.find(i).text
                        if index != len(catagories)-1:
                            t += ", "
                        else:
                            t += ");"

                #print(t)
                conn.execute(t)


