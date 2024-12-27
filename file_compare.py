import pdfplumber
import pandas as pd
import io
import math

def set_list_order_preserved(input_list):
    result = []
    for item in input_list:
        item = item.replace(",", "").replace("'","").replace(".","").replace(" ","")
        if item not in result:
            result.append(item)
    return result


def extract_data_from_GD_file(file):

    with pdfplumber.open(io.BytesIO(file)) as pdf:
    # with pdfplumber.open(file) as pdf:
        try:
            for page in pdf.pages:
                text_with_boxes = page.extract_text_simple()
                Name_and_address =  text_with_boxes.split("8.IGM/EGM NO & DT -- INDEX")[0].split("EF METHOD")[1].strip()

                Name = Name_and_address.split("5.PAGE")[0].replace("M/S","").strip()
                Address = Name_and_address.split("7.BANK CODE")[1].split("\n")
                Address = " ".join(Address[-2:]).replace("  ", " ").split(' 1 ')[0].strip()

                position = text_with_boxes.find("AFU")
                if position < 1 :
                    Invoice_no = text_with_boxes.split("TRANSPORT")[1].split()[0].strip().split('/')
                    Invoice_no_1 = Invoice_no[-1].replace("202","2")
                    Invoice_no[-1] = Invoice_no_1
                    Invoice_no = "/".join(Invoice_no)

                else:
                    Invoice_no = text_with_boxes.split("INV#")[1].split()[0].strip().split('/')
                    Invoice_no_1 = Invoice_no[-1].replace("202", "2")
                    Invoice_no[-1] = Invoice_no_1
                    Invoice_no = "/".join(Invoice_no)


                # Importer_name = text_with_boxes.split("INDEX\nDT")[1].split("11.DECLARANT")[0]
                # Importer_name = Importer_name.strip()

                Importer_name_and_addr = text_with_boxes.split("INDEX\nDT")[1].split("14.NTN")[0]
                Importer_name_and_addr = Importer_name_and_addr.split("\n")
                Importer_name_and_addr = [x if "12." not in x else "" for x in Importer_name_and_addr]
                Importer_name_and_addr = [x if "CARGO LINKERS" not in x else "" for x in Importer_name_and_addr]

                for i in range(len(Importer_name_and_addr)):
                    if "" in Importer_name_and_addr:
                        Importer_name_and_addr.remove("")
                if Importer_name_and_addr[-2] != Importer_name_and_addr[0]:
                    Importer_name_and_addr = Importer_name_and_addr[0].split("11.DECLARANT")[0].strip() + " " + Importer_name_and_addr[-2].strip() + " " + Importer_name_and_addr[-1].strip()
                else:
                    Importer_name_and_addr = Importer_name_and_addr[0].split("11.DECLARANT")[0].strip() + " " + Importer_name_and_addr[-1].strip()
                Importer_name_and_addr = Importer_name_and_addr.replace(". ", ".").split("TEL")[0].strip()


                Place_of_Delivery = text_with_boxes.split("DELIVERY TERMS")[1].split("31.NUMBER")[0].split("-")[0].strip().lower()
                Place_of_Delivery = Place_of_Delivery.split()
                ind_element = Place_of_Delivery[0].replace(',','')
                Place_of_Delivery__ = Place_of_Delivery[1:]
                Place_of_Delivery__ = list(map(lambda x:x.replace(',','') , Place_of_Delivery__))
                ind_City = Place_of_Delivery__.index(ind_element)
                ind_City = ind_City + 1
                Port_of_Discharge = Place_of_Delivery[:ind_City]
                Place_of_Delivery = Place_of_Delivery[ind_City:]


                # Place_of_Delivery_list = set_list_order_preserved(Place_of_Delivery)
                # if len(Place_of_Delivery_list) > 2:
                #     Place_of_Delivery_list = Place_of_Delivery[1:-1]
                Place_of_Delivery = " ".join(Place_of_Delivery)
                Port_of_Discharge = " ".join(Port_of_Discharge)

                Gross_WT = float(text_with_boxes.split("OSS WT")[1].split("35.GENERAL")[0].split("\n")[1].split()[-2].replace(",","").replace("KG", ""))
                Net_WT = float(text_with_boxes.split("NET WT")[1].split("36.IN")[0].replace("MT", "").strip().replace(",","").replace("KG", ""))

                Value = float(text_with_boxes.split("19.LC/DD NO.")[0].split()[-1].strip())
                try:
                    Value_1 = float(text_with_boxes.split("19.LC/DD NO.")[0].split()[-1].strip())
                    Value_2 = float(text_with_boxes.split("21.CURRENCY")[0].split("IT EXMP")[-1].split()[-1].strip())
                    Value = Value_1 + Value_2
                except:
                    pass

                Value = math.floor(Value)

                Country = text_with_boxes.split("BL/AWB")[0].split("20.COUNTRY OF DESTINATION")[1].strip().split("M ")
                Country = Country[0] if len(Country) < 2 else Country[1]
                No_of_packages = float(text_with_boxes.split("Volume M3")[1].split()[0].strip())

                No_of_units = text_with_boxes.split("Pakistan")
                No_of_units_1 = float(No_of_units[0].split()[-1])
                No_of_units_2 = ""

                if len(No_of_units) > 2:
                    No_of_units_2 = float(No_of_units[1].split()[-1])

                GD_file_data_dict = {"Invoice_no":Invoice_no,"Name":Name,"Address":Address,"Place_of_Delivery":Place_of_Delivery,"Gross_WT":Gross_WT,"Net_WT":Net_WT,"Value":Value,"Country":Country,"No_of_packages":No_of_packages, "Importer_name_and_addr":Importer_name_and_addr, "No_of_units_1": No_of_units_1, "No_of_units_2": No_of_units_2}

                return GD_file_data_dict

        except Exception as e:
            print(f"Error processing file: {e}")


def Ali_Murtaza_Invoice(file):
    # file = file.read()
    with pdfplumber.open(file) as pdf:
        try:
            for page in pdf.pages:

                text_with_boxes = page.extract_text_simple()

                Name = text_with_boxes.split("EXP")[0].replace("INVOICE NO:", "").replace(".","").strip()
                Invoice_no = text_with_boxes.split("\n")[1].split()[0].strip()
                Address = text_with_boxes.split("\n")[1].split("ISSUE #")[0]
                Address = Address.replace(Address.split()[0], "").strip()

                Importer_name_and_addr = text_with_boxes.split("against L/c No.")[0].split("for account & risk of M/s:")[1].split("\n")
                for i in range(len(Importer_name_and_addr)):
                    if "" in Importer_name_and_addr:
                        Importer_name_and_addr.remove("")

                Importer_name_and_addr_1 = Importer_name_and_addr[0].split("  ")
                Importer_name_and_addr_1 = list(map(lambda x: x.strip(), Importer_name_and_addr_1))
                Importer_name_and_addr_1 = [" " if x == ""  else x for x in Importer_name_and_addr_1]
                Importer_name_and_addr = "".join(Importer_name_and_addr_1).strip() + " " + Importer_name_and_addr[1].strip()
                Importer_name_and_addr = Importer_name_and_addr.replace(". ", ".").replace("  ", " ")

                Place_of_Delivery = text_with_boxes.split("for account & risk of")[0].split("TO")[-1].strip()

                Gross_WT = float(text_with_boxes.split("Gross Weight")[1].split("KGS Net Weight")[0].strip().replace(",",""))/1000

                Net_WT = float(text_with_boxes.split("Marks & Nos")[0].split("Net Weight (Kgs)")[1].strip().replace(",",""))/1000

                Value = float(text_with_boxes.split("ONLY) PIECES")[0].split("$")[-1].split('\n')[0].strip().replace(" ","").replace(",",""))

                Country = text_with_boxes.split("Opening/through")[1].split()[0].strip()
                No_of_packages = float(text_with_boxes.split("PRICE AMOUNT")[1].split("CARTONS")[0].strip())

                No_of_units = text_with_boxes.split("PIECES USD USD")[1].split("\n")
                No_of_units_1 = float(No_of_units[5].split("$")[-3].split()[-1].replace(",","").strip())
                No_of_units_2 = ""

                if len(No_of_units) > 2:

                    No_of_units_2 = float(No_of_units[6].split("$")[-3].split()[-1].replace(",","").strip())

                Invoice_file_data_dict = {"Invoice_no": Invoice_no,"Name": Name, "Address": Address, "Place_of_Delivery": Place_of_Delivery,
                                     "Gross_WT": Gross_WT, "Net_WT": Net_WT, "Value": Value, "Country": Country,
                                     "No_of_packages": No_of_packages, "Importer_name_and_addr":Importer_name_and_addr, "No_of_units_1":No_of_units_1, "No_of_units_2":No_of_units_2}

                return Invoice_file_data_dict

        except Exception as e:
            print(f"Error processing file: {e}")


def Siddiqsons_Invoice(file):
    Invoice_df = pd.read_excel(file)
    Invoice_df = Invoice_df.fillna('')

    Invoice_ind = Invoice_df[Invoice_df.apply(lambda row: row.astype(str).str.contains('INV/DO# ').any(), axis=1)]
    Invoice_no = Invoice_ind.iloc[0][1] if Invoice_ind.iloc[0][1] is not None else ''
    Invoice_no = Invoice_no.replace("/202", "/2")

    Name = "SIDDIQSONS LIMITED"
    # Name = Invoice_df.apply(lambda row: row.astype(str).str.contains('FOR: ').any(), axis=1)
    # Name = Invoice_df[Name].stack().index
    # Name = Name.iloc[0][11] if Name.iloc[0][11] is not None else ''

    # Importer_name_and_addr = "" if Invoice_df.iloc[8, 1] in [None, "None"] else Invoice_df.iloc[8, 1]
    Importer_name_and_addr = Invoice_df[Invoice_df.apply(lambda row: row.astype(str).str.contains('BUYER:').any(), axis=1)]
    Importer_name_and_addr = Importer_name_and_addr.iloc[0][1] if Importer_name_and_addr.iloc[0][1] is not None else ''
    Importer_name_and_addr = Importer_name_and_addr.strip()

    # Place_of_Delivery_full = "" if Invoice_df.iloc[12, 2] in [None, "None"] else Invoice_df.iloc[12, 2]
    Place_of_Delivery_full = Invoice_df[Invoice_df.apply(lambda row: row.astype(str).str.contains('KARACHI TO').any(), axis=1)]
    Place_of_Delivery_full = Place_of_Delivery_full.iloc[0][2]
    Place_of_Delivery = Place_of_Delivery_full.split("-")[0]
    Place_of_Delivery = Place_of_Delivery.strip()

    # Gross_WT = 0 if Invoice_df.iloc[64, 4] in [None, "None"] else Invoice_df.iloc[64, 4]
    Gross_WT = Invoice_df[Invoice_df.apply(lambda row: row.astype(str).str.contains('TOTAL GROSS WEIGHT').any(), axis=1)]
    Gross_WT = Gross_WT.iloc[0][3] if Gross_WT.iloc[0][3] not in [None, ''] else Gross_WT.iloc[0][4]
    Gross_WT = float(Gross_WT)/1000

    # Net_WT = 0 if Invoice_df.iloc[63, 4] in [None, "None"] else Invoice_df.iloc[63, 4]
    Net_WT = Invoice_df[Invoice_df.apply(lambda row: row.astype(str).str.contains('TOTAL NET WEIGHT').any(), axis=1)]
    Net_WT = Net_WT.iloc[0][3] if Net_WT.iloc[0][3] not in [None, ''] else Net_WT.iloc[0][4]
    Net_WT = float(Net_WT)/1000

    # No_of_packages_list = Invoice_df.iloc[16: 59, 2].tolist()
    No_of_packages_list = Invoice_df.apply(lambda column: column.astype(str).str.contains('NO. OF').any(), axis=1)
    No_of_packages_list = No_of_packages_list.tolist()
    package_ind = No_of_packages_list.index(True) if No_of_packages_list.index(True) is not None else ""
    i = package_ind + 1
    No_of_packages = 0
    while True:
        num_of_Package = Invoice_df.iloc[i][2]
        if num_of_Package not in ["", None, 'None', 0]:
            try:
                num_of_Package = int(num_of_Package)
                No_of_packages = num_of_Package
            except:
                break
        i+=1

    # No_of_packages = ""
    # for i in No_of_packages_list[::-1]:
    #     if type(i) == type(1) and i != 0:
    #         No_of_packages = i
    #         break

    # Value = 0 if Invoice_df.iloc[60, 11] in [None, "None"] else Invoice_df.iloc[60, 11]

    Value=0
    try:
        Value_df = Invoice_df[Invoice_df.apply(lambda row: row.astype(str).str.contains('VALUE').any(), axis=1)]
        # Value = Value.iloc[0][3] if Value.iloc[0][3] is not None else 0
        for ind in range(5):
            value= Value_df.iloc[0][-ind]
            if value != "":
                try:
                    Value= float(value)
                except:
                    break

    except:
        Value_df = Invoice_df[Invoice_df.apply(lambda row: row.astype(str).str.contains('Value').any(), axis=1)]
        for ind in range(5):
            value= Value_df.iloc[0][-ind]
            if value != "":
                try:
                    Value= float(value)
                except:
                    break

    Value = math.floor(Value)

    No_of_units_1 = ""
    No_of_units_2 = ""

    Country = Place_of_Delivery_full.split("-")[-1].strip() if Place_of_Delivery_full.split("-")[-1].strip() != "MOROCCOW" else "MOROCCO"

    Invoice_file_data_dict = {"Invoice_no": Invoice_no, "Name": Name,
                              "Place_of_Delivery": Place_of_Delivery,
                              "Gross_WT": Gross_WT, "Net_WT": Net_WT, "Value": Value, "Country": Country,
                              "No_of_packages": No_of_packages, "Importer_name_and_addr": Importer_name_and_addr,
                              "No_of_units_1": No_of_units_1, "No_of_units_2": No_of_units_2}

    return Invoice_file_data_dict

def Indigo_Invoice(file):
    Invoice_df = pd.read_excel(file)
    Invoice_df = Invoice_df.fillna('')

    Invoice_no = "" if Invoice_df.iloc[18, 10] in [None, "None"] else Invoice_df.iloc[18, 10]

    Name = "Indigo Textile (Pvt) Ltd."
    # Name = "" if Invoice_df.iloc[107, 9] in [None, "None"] else Invoice_df.iloc[107, 9]
    # Name = Name.replace("For", "").strip()
    Name = Name.strip()

    Importer_name_and_addr_1 = "" if Invoice_df.iloc[14, 2] in [None, "None"] else Invoice_df.iloc[14, 2]
    Importer_name_and_addr_1 = Importer_name_and_addr_1.strip()

    Importer_name_and_addr_2 = "" if Invoice_df.iloc[15, 2] in [None, "None"] else Invoice_df.iloc[15, 2]
    Importer_name_and_addr_2 = Importer_name_and_addr_2.strip()

    Importer_name_and_addr_3 = "" if Invoice_df.iloc[16, 2] in [None, "None"] else Invoice_df.iloc[16, 2]
    Importer_name_and_addr_3 = Importer_name_and_addr_3.strip()

    Importer_name_and_addr_4 = "" if Invoice_df.iloc[17, 2] in [None, "None"] else Invoice_df.iloc[17, 2]
    Importer_name_and_addr_4 = Importer_name_and_addr_4.strip()


    # Importer_address = "" if Invoice_df.iloc[14, 2] in [None, "None"] else Invoice_df.iloc[14, 2]
    # Importer_address = Importer_address.strip()
    #
    Importer_name_and_addr = Importer_name_and_addr_1.strip() + " " + Importer_name_and_addr_2.strip() + " " + Importer_name_and_addr_3.strip() + " " + Importer_name_and_addr_4.strip()

    Place_of_Delivery = "" if Invoice_df.iloc[21, 2] in [None, "None"] else Invoice_df.iloc[21, 2]
    Place_of_Delivery_full = Place_of_Delivery.replace(","," -").strip()
    Place_of_Delivery = Place_of_Delivery_full.split("-")[0]
    Place_of_Delivery = Place_of_Delivery.strip()

    # Gross_WT = "" if Invoice_df.iloc[95, 10] in [None, "None"] else Invoice_df.iloc[95, 10]
    Gross_WT_ind = Invoice_df.apply(lambda row: row.astype(str).str.contains('For Indigo.').any(), axis=1)
    Gross_WT_ind = Gross_WT_ind.tolist()
    Gross_WT_ind = Gross_WT_ind.index(True)

    # Gross_WT = Invoice_df.apply(lambda row: row.astype(str).str.contains('For Indigo Textile (Pvt) Ltd.').any(), axis=1)
    Gross_WT = 0
    Net_WT = 0
    No_of_packages = 0
    Value = 0
    for row in range(25,Gross_WT_ind):
        try:
            Gross_WT_ = Invoice_df.iloc[row][10]
            Net_WT_ = Invoice_df.iloc[row][9]
            No_of_packages_ = Invoice_df.iloc[row][3]
            Value_ = Invoice_df.iloc[row][12]
            if Gross_WT_ not in ['', None]:
                Gross_WT = int(Gross_WT_)
            if Net_WT_ not in ['', None]:
                Net_WT = int(Net_WT_)
            if No_of_packages_ not in ['', None]:
                No_of_packages = int(No_of_packages_)
            if Value_ not in ['', None]:
                Value = int(Value_)
        except:
            pass

    Gross_WT = float(Gross_WT) / 1000

    # Net_WT = "" if Invoice_df.iloc[95, 9] in [None, "None"] else Invoice_df.iloc[95, 9]
    Net_WT = float(Net_WT) / 1000

    # No_of_packages = "" if Invoice_df.iloc[95, 3] in [None, "None"] else Invoice_df.iloc[95, 3]

    # Value = "" if Invoice_df.iloc[95, 12] in [None, "None"] else Invoice_df.iloc[95, 12]
    Value = math.floor(Value)

    No_of_units_1 = ""
    No_of_units_2 = ""

    Country = Place_of_Delivery_full.split("-")[-1].strip()

    Invoice_file_data_dict = {"Invoice_no": Invoice_no, "Name": Name,
                              "Place_of_Delivery": Place_of_Delivery,
                              "Gross_WT": Gross_WT, "Net_WT": Net_WT, "Value": Value, "Country": Country,
                              "No_of_packages": No_of_packages, "Importer_name_and_addr": Importer_name_and_addr,
                              "No_of_units_1": No_of_units_1, "No_of_units_2": No_of_units_2}

    return Invoice_file_data_dict


def Akhtar_Invoice(file):
    Invoice_df = pd.read_excel(file)
    Invoice_df = Invoice_df.fillna('')
    Invoice_no_ind = Invoice_df.apply(lambda row: row.astype(str).str.contains('Invoice of').any(), axis=1)
    Invoice_no_ind = Invoice_no_ind.tolist()
    Invoice_no_ind = Invoice_no_ind.index(True)

    Invoice_no = "" if Invoice_df.iloc[Invoice_no_ind, 10] in [None, "None"] else Invoice_df.iloc[Invoice_no_ind, 10]

    Name = "Akhtar Textile Industries (Pvt) LTD"

    Importer_detail_ind = Invoice_df.apply(lambda row: row.astype(str).str.contains('Messrs').any(), axis=1)
    Importer_detail_ind = Importer_detail_ind.tolist()
    Importer_detail_ind = Importer_detail_ind.index(True)

    des_ind = Invoice_df.apply(lambda row: row.astype(str).str.contains('From KARACHI to').any(), axis=1)
    des_ind = des_ind.tolist()
    des_ind = des_ind.index(True)


    Importer_name = "" if Invoice_df.iloc[Importer_detail_ind, 4] in [None, "None"] else Invoice_df.iloc[Importer_detail_ind, 4]
    Importer_name = Importer_name.strip()
    Importer_address_1 = "" if Invoice_df.iloc[Importer_detail_ind +1, 4].strip() in [None, "None"] else Invoice_df.iloc[Importer_detail_ind +1, 4].strip()
    Importer_address_1 = Importer_address_1.strip()
    Importer_address_2 = "" if Invoice_df.iloc[Importer_detail_ind +2, 4].strip() in [None, "None"] else Invoice_df.iloc[Importer_detail_ind +2, 4].strip()
    Importer_address_2 = Importer_address_2.strip()
    Importer_address_3 = "" if Invoice_df.iloc[Importer_detail_ind +3, 4].strip() in [None, "None"] else Invoice_df.iloc[Importer_detail_ind +3, 4].strip()
    Importer_address_3 = Importer_address_3.strip()

    Importer_name_and_addr = Importer_name + " " + Importer_address_1.strip() + " " + Importer_address_2.strip() + " " + Importer_address_3.strip()
    Importer_name_and_addr = Importer_name_and_addr.strip()

    Place_of_Delivery_ = "" if Invoice_df.iloc[des_ind, 4] in [None, "None"] else Invoice_df.iloc[des_ind, 4]
    Place_of_Delivery = Place_of_Delivery_.replace(",", "").strip()

    pcs_ind = Invoice_df.apply(lambda row: row.astype(str).str.contains('UNDER REBATE CLAIM VIDE').any(), axis=1)
    pcs_ind = pcs_ind.tolist()
    pcs_ind = pcs_ind.index(True)

    Gross_WT = 0 if Invoice_df.iloc[9, 10] in [None, "None", ""] else Invoice_df.iloc[95, 10]
    Gross_WT = float(Gross_WT) / 1000

    Net_WT = 0 if Invoice_df.iloc[9, 9] in [None, "None", ""] else Invoice_df.iloc[9, 9]
    Net_WT = float(Net_WT) / 1000

    No_of_packages = "" if Invoice_df.iloc[pcs_ind-1, 4] in [None, "None"] else Invoice_df.iloc[pcs_ind-1, 4]

    Value = 0 if Invoice_df.iloc[pcs_ind-1, 11] in [None, "None", ""] else Invoice_df.iloc[pcs_ind-1, 11]
    Value = math.floor(Value)

    No_of_units_1 = ""
    No_of_units_2 = ""

    Country = Place_of_Delivery_.split(" ")[1] if len(Place_of_Delivery_.split(" ")) > 1 else ""
    Country = "United States" if len(Country) == 2 and Country != "UK" else Country
    # Country = Importer_name_and_addr.split(",")[-1].strip() if Importer_name != "LEVI STRAUSS & CO." else "United States"

    Invoice_file_data_dict = {"Invoice_no": Invoice_no, "Name": Name,
                              "Place_of_Delivery": Place_of_Delivery,
                              "Gross_WT": Gross_WT, "Net_WT": Net_WT, "Value": Value, "Country": Country,
                              "No_of_packages": No_of_packages, "Importer_name_and_addr": Importer_name_and_addr,
                              "No_of_units_1": No_of_units_1, "No_of_units_2": No_of_units_2}

    return Invoice_file_data_dict


def Liberty_Invoice(file):
    Invoice_df = pd.read_excel(file)
    Invoice_df = Invoice_df.fillna('')
    Invoice_no = "" if Invoice_df.iloc[13, 7] in [None, "None"] else Invoice_df.iloc[13, 7]
    Invoice_no = Invoice_no.replace(":", "-")

    Name = "" if Invoice_df.iloc[0, 3] in [None, "None"] else Invoice_df.iloc[0, 3]

    Importer_name_and_addr = "" if Invoice_df.iloc[16, 7] in [None, "None"] else Invoice_df.iloc[16, 7]
    Importer_name_and_addr = Importer_name_and_addr.replace("\n"," ").split("TEL")[0]
    Importer_name_and_addr = Importer_name_and_addr.strip()

    Place_of_Delivery = "" if Invoice_df.iloc[23, 7] in [None, "None"] else Invoice_df.iloc[23, 7]
    Place_of_Delivery_full = Place_of_Delivery.replace(","," -").strip()
    Place_of_Delivery = Place_of_Delivery_full.split("-")[0]
    Place_of_Delivery = Place_of_Delivery.strip()

    Invoice_total_ind = Invoice_df.apply(lambda row: row.astype(str).str.contains('Invoice Total').any(), axis=1)
    Invoice_total_ind = Invoice_total_ind.tolist()
    Invoice_total_ind = Invoice_total_ind.index(True)

    # Gross_WT = "" if Invoice_df.iloc[62, 34] in [None, "None"] else Invoice_df.iloc[62, 34]
    Gross_WT = "" if Invoice_df.iloc[Invoice_total_ind, 34] in [None, "None"] else Invoice_df.iloc[Invoice_total_ind, 34]
    Gross_WT = float(Gross_WT) / 1000

    Net_WT = "" if Invoice_df.iloc[Invoice_total_ind, 37] in [None, "None"] else Invoice_df.iloc[Invoice_total_ind, 37]
    Net_WT = float(Net_WT) / 1000


    No_of_packages = "" if Invoice_df.iloc[Invoice_total_ind, 22] in [None, "None"] else Invoice_df.iloc[Invoice_total_ind, 22]

    Value = "" if Invoice_df.iloc[Invoice_total_ind +1, 41] in [None, "None"] else Invoice_df.iloc[Invoice_total_ind +1, 41]
    Value = math.floor(Value)

    No_of_units_1 = ""
    No_of_units_2 = ""

    Country = Place_of_Delivery_full.split("-")[-1].strip() if Place_of_Delivery_full.split("-")[-1].strip() !="U.S.A" and Place_of_Delivery_full.split("-")[-1].strip() != "USA" else "United States"

    Invoice_file_data_dict = {"Invoice_no": Invoice_no, "Name": Name,
                              "Place_of_Delivery": Place_of_Delivery,
                              "Gross_WT": Gross_WT, "Net_WT": Net_WT, "Value": Value, "Country": Country,
                              "No_of_packages": No_of_packages, "Importer_name_and_addr": Importer_name_and_addr,
                              "No_of_units_1": No_of_units_1, "No_of_units_2": No_of_units_2}

    return Invoice_file_data_dict


def Proline_Invoice(file):
    Invoice_df = pd.read_excel(file)
    Invoice_df = Invoice_df.fillna('')
    Invoice_no = "" if Invoice_df.iloc[6, 4] in [None, "None"] else Invoice_df.iloc[6, 4]
    Invoice_no = Invoice_no.replace("/202", "/2")

    # Name = Invoice_df.columns.tolist()[0]
    Name = "PROLINE (PRIVATE) LIMITED"

    Importer_name = "" if Invoice_df.iloc[13, 4] in [None, "None"] else Invoice_df.iloc[13, 4]
    Importer_name = Importer_name.strip()
    Importer_addr = "" if Invoice_df.iloc[15, 4] in [None, "None"] else Invoice_df.iloc[15, 4]
    Importer_addr = Importer_addr.strip()
    Importer_name_and_addr = Importer_name.strip() + " " + Importer_addr.strip()


    Place_of_Delivery = "" if Invoice_df.iloc[11, 4] in [None, "None"] else Invoice_df.iloc[11, 4]
    Place_of_Delivery_full = Place_of_Delivery.replace(","," -").strip()
    Place_of_Delivery = Place_of_Delivery.split("-")[0]
    Place_of_Delivery = Place_of_Delivery.strip()

    Gross_WT_ = Invoice_df.apply(lambda row: row.astype(str).str.contains('GROSS WEIGHT').any(), axis=1)
    Gross_WT_ = Gross_WT_.tolist()
    Gross_WT_ind = Gross_WT_.index(True)
    Gross_WT= 0
    Net_WT= 0
    for row in range(Gross_WT_ind+1, Gross_WT_ind+10):
        try:
            Gross_WT_ = Invoice_df.iloc[row, 0]
            Net_WT_ = Invoice_df.iloc[row, 2]
            if Gross_WT_ not in ['', None]:
                Gross_WT= float(Gross_WT_)
            if Net_WT_ not in ['', None]:
                Net_WT = float(Net_WT_)
        except:
            break
    Gross_WT = float(Gross_WT) / 1000

    # Net_WT = "" if Invoice_df.iloc[Gross_WT_ind+1, 2] in [None, "None"] else Invoice_df.iloc[Gross_WT_ind+1, 2]
    Net_WT = float(Net_WT) / 1000

    No_of_packages = Invoice_df.apply(lambda row: row.astype(str).str.contains('TOTAL U.S. DOLLAR').any(), axis=1)
    No_of_packages = No_of_packages.tolist()
    No_of_packages_ind = No_of_packages.index(True) +1
    No_of_packages = "" if Invoice_df.iloc[No_of_packages_ind, 26] in [None, "None"] else Invoice_df.iloc[No_of_packages_ind, 26]

    # Value = "" if Invoice_df.iloc[59, 40] in [None, "None"] else Invoice_df.iloc[59, 40]
    Value = "" if Invoice_df.iloc[No_of_packages_ind, 40] in [None, "None"] else Invoice_df.iloc[No_of_packages_ind, 40]
    Value = Value if type(Value) == type(2) or type(Value) == type(2.2) else Invoice_df.iloc[No_of_packages_ind, 41]
    Value = math.floor(Value)

    No_of_units_1 = ""
    No_of_units_2 = ""

    Country = Place_of_Delivery_full.split("-")[-1].strip()

    Invoice_file_data_dict = {"Invoice_no": Invoice_no, "Name": Name,
                              "Place_of_Delivery": Place_of_Delivery,
                              "Gross_WT": Gross_WT, "Net_WT": Net_WT, "Value": Value, "Country": Country,
                              "No_of_packages": No_of_packages, "Importer_name_and_addr": Importer_name_and_addr,
                              "No_of_units_1": No_of_units_1, "No_of_units_2": No_of_units_2}

    return Invoice_file_data_dict


def Compare_files(GD_file_path, Invoice_path, Title):
    try:
        not_matched = {}
        gd_data = {}
        invoice_data = {}
        Invoice_data = {}
        GD_file_data = extract_data_from_GD_file(GD_file_path)
        # if Title == "Ali Murtaza":
        #     Invoice_data = Ali_Murtaza_Invoice(Invoice_path)
        if Title == "Siddiqsons":
            Invoice_data = Siddiqsons_Invoice(Invoice_path)
        if Title == "Indigo":
            Invoice_data = Indigo_Invoice(Invoice_path)
        if Title == "Akhtar":
            Invoice_data = Akhtar_Invoice(Invoice_path)
        if Title == "Liberty":
            Invoice_data = Liberty_Invoice(Invoice_path)
        if Title == "Proline":
            Invoice_data = Proline_Invoice(Invoice_path)

        Invoice_no = GD_file_data["Invoice_no"] == Invoice_data["Invoice_no"]
        if not Invoice_no:
            gd_data.update({"Invoice_no": GD_file_data["Invoice_no"]})
            invoice_data.update({"Invoice_no": Invoice_data["Invoice_no"]})

        Name = GD_file_data["Name"].lower() == Invoice_data["Name"].lower()
        if not Name:
            gd_data.update({"Name": GD_file_data["Name"]})
            invoice_data.update({"Name": Invoice_data["Name"]})
        # Address =GD_file_data["Address"].lower() == Invoice_data["Address"].lower()

        Importer_name_and_addr = GD_file_data["Importer_name_and_addr"].lower().replace(',','') == Invoice_data["Importer_name_and_addr"].lower().replace(',','')
        if not Importer_name_and_addr:
            Importer_name_and_addr = GD_file_data["Importer_name_and_addr"].replace(" ","").replace(",","").replace(".","").lower() == Invoice_data["Importer_name_and_addr"].replace(" ","").replace(",","").replace(".","").lower()
            if not Importer_name_and_addr:
                gd_data.update({"Importer_name_and_addr": GD_file_data["Importer_name_and_addr"]})
                invoice_data.update({"Importer_name_and_addr": Invoice_data["Importer_name_and_addr"]})

        Place_of_Delivery = GD_file_data["Place_of_Delivery"].lower().replace(',','') == Invoice_data["Place_of_Delivery"].lower().replace(',','')
        if not Place_of_Delivery:
            Place_of_Delivery = GD_file_data["Place_of_Delivery"].lower() in Invoice_data["Place_of_Delivery"].lower().split(" ")
            if not Place_of_Delivery:
                gd_data.update({"Place_of_Delivery": GD_file_data["Place_of_Delivery"]})
                invoice_data.update({"Place_of_Delivery": Invoice_data["Place_of_Delivery"]})


        Gross_WT = round(GD_file_data["Gross_WT"], 3) == round(Invoice_data["Gross_WT"], 3)
        if not Gross_WT:
            gd_data.update({"Gross_WT": GD_file_data["Gross_WT"]})
            invoice_data.update({"Gross_WT": Invoice_data["Gross_WT"]})

        Net_WT =round(GD_file_data["Net_WT"], 3) == round(Invoice_data["Net_WT"] , 3)
        if not Net_WT:
            gd_data.update({"Net_WT": GD_file_data["Net_WT"]})
            invoice_data.update({"Net_WT": Invoice_data["Net_WT"]})

        Value = GD_file_data["Value"] == Invoice_data["Value"]
        if not Value:
            gd_data.update({"Value": GD_file_data["Value"]})
            invoice_data.update({"Value": Invoice_data["Value"]})


        Country = GD_file_data["Country"].lower() == Invoice_data["Country"].lower()
        if not Country:
            gd_data.update({"Country": GD_file_data["Country"]})
            invoice_data.update({"Country": Invoice_data["Country"]})


        No_of_packages = GD_file_data["No_of_packages"] == Invoice_data["No_of_packages"]
        if not No_of_packages:
            gd_data.update({"No_of_packages": GD_file_data["No_of_packages"]})
            invoice_data.update({"No_of_packages": Invoice_data["No_of_packages"]})



        # No_of_units_1 = GD_file_data["No_of_units_1"] == Invoice_data["No_of_units_1"]
        # No_of_units_2 = GD_file_data["No_of_units_2"] == Invoice_data["No_of_units_2"]

        matched = {"Invoice_no": Invoice_no, "Name": Name, "Place_of_delivery": Place_of_Delivery,
                                         "Gross_wt": Gross_WT, "Net_wt": Net_WT, "Value": Value, "Country": Country,
                                         "No_of_packages": No_of_packages, "Importer_name_and_addr"" ": Importer_name_and_addr}

        # gd_data = {"Name": GD_file_data["Name"], "Place_of_delivery": GD_file_data["Place_of_Delivery"],
        #                                  "Gross_wt": round(GD_file_data["Gross_WT"], 3), "Net_wt": round(GD_file_data["Net_WT"], 3), "Value": GD_file_data["Value"], "Country": GD_file_data["Country"],
        #                                  "No_of_packages": GD_file_data["No_of_packages"], "Importer_name_and_addr"" ": GD_file_data["Importer_name_and_addr"]}
        #
        # invoice_data = {"Invoice_no": Invoice_data["Invoice_no"], "Name": Invoice_data["Name"], "Place_of_delivery": Invoice_data["Place_of_Delivery"],
        #                                  "Gross_wt": round(Invoice_data["Gross_WT"], 3), "Net_wt": round(Invoice_data["Net_WT"], 3), "Value": Invoice_data["Value"], "Country": Invoice_data["Country"],
        #                                  "No_of_packages": Invoice_data["No_of_packages"], "Importer_name_and_addr"" ": Invoice_data["Importer_name_and_addr"]}

        not_matched.update({"gd_data":gd_data, "invoice_data": invoice_data})

        return {"matched":matched, "not_matched": not_matched}
    except Exception as e:
        print(e)
        return {f"error: {e}"}


# Invoice = 'C:\\Users\\USER\\Downloads\\Copy of CUSTOM INVOICE 1691-C.xlsx'
# Invoice = 'C:\\Users\\admin\\Downloads\\INVOICE ALI MURTAZA.pdf'
# Invoice = 'C:\\Users\\admin\\Downloads\\INVOIE AKHTAR 1586-B.xlsx'
# Invoice = 'C:\\Users\\admin\\Downloads\\INVOCIE PROLINE 644.xls'
# Invoice = 'C:\\Users\\admin\\Downloads\\INVOCIE LIBERTY 1068.xlsx'
# Invoice = 'C:\\Users\\admin\\Downloads\\INVOICE INDIGO 1316.xlsx'
# Invoice = 'C:\\Users\\admin\\Downloads\\INVOCIE SIDDIQSONS 0517.xlsx'
# GD_file = 'C:\\Users\\admin\\Downloads\\differentpartygdandinv\\GD FORNT PAGE SIDDIQSONS 517.pdf'
# GD_file = 'C:\\Users\\admin\\Downloads\\differentpartygdandinv\\GD FRONT PAGE ALI MURTAZA 1816.pdf'
# GD_file = 'C:\\Users\\admin\\Downloads\\differentpartygdandinv\\GD FORNT PAGE AKHTAR 1586B.pdf'
# GD_file = 'C:\\Users\\admin\\Downloads\\differentpartygdandinv\\GD FORNT PAGE INDIGO 1316.pdf'
# GD_file = 'C:\\Users\\admin\\Downloads\\differentpartygdandinv\\GD FORNT PAGE LIB 1068.pdf'
# GD_file = 'C:\\Users\\admin\\Downloads\\differentpartygdandinv\\GD FRONT PAGE PROLINE 644.pdf'
# GD_file = 'C:\\Users\\admin\\Downloads\\GD-Invoices\\FORN PAGE GD SIDDIQONS.pdf'
# GD_file = 'C:\\Users\\admin\\Downloads\\GD-Invoices\\FRONT PAGE GD INDIGO.pdf'
# GD_file = 'C:\\Users\\admin\\Downloads\\GD-Invoices\\FORNT PAGE GD PROLINE.pdf'
# GD_file = 'C:\\Users\\admin\\Downloads\\GD-Invoices\\FRONT PAGE GD LIBERTY.pdf'
# GD_file = 'C:\\Users\\admin\\Downloads\\GD-Invoices\\FORNT PAGE GD AKHTAR.pdf'
# Invoice = 'C:\\Users\\admin\\Downloads\\GD-Invoices\\INVOICE SIDDIQSONS.xlsx'
# Invoice = 'C:\\Users\\admin\\Downloads\\GD-Invoices\\INVOICE AKHTAR EXCEL.xlsx'
# Invoice = 'C:\\Users\\admin\\Downloads\\GD-Invoices\\INVOICE INDIGO EXCEL.xlsx'
# Invoice = 'C:\\Users\\admin\\Downloads\\GD-Invoices\\INVOICE EXCEL PROLINE.xls'
# Invoice = 'C:\\Users\\admin\\Downloads\\GD-Invoices\\INVOICE LIBERTY EXCEL.xlsx'
# GD_file = 'C:\\Users\\admin\\Downloads\\ALI MURTAZA GD.pdf'
# GD_file = 'C:\\Users\\USER\\Downloads\\FRONT PAGE.pdf'
#
# if __name__ == "__main__":
#     try:
#         matched= Compare_files(Invoice_path=Invoice, GD_file_path=GD_file, Title="Akhtar")
#         print(matched)
#     except Exception as e:
#         print(e)
#
