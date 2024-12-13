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

    # with pdfplumber.open(io.BytesIO(file)) as pdf:
    with pdfplumber.open(file) as pdf:
        try:
            for page in pdf.pages:
                text_with_boxes = page.extract_text_simple()
                Name_and_address =  text_with_boxes.split("8.IGM/EGM NO & DT -- INDEX")[0].split("EF METHOD")[1].strip()

                Name = Name_and_address.split("5.PAGE")[0].replace("M/S","").strip()
                Address = Name_and_address.split("7.BANK CODE")[1].split("\n")
                Address = " ".join(Address[-2:]).replace("  ", " ").split(' 1 ')[0].strip()

                Invoice_no = text_with_boxes.split("TRANSPORT")[1].split()[0].strip().split('/')
                Invoice_no_1 = Invoice_no[-1].replace("202","2")
                Invoice_no[-1] = Invoice_no_1
                Invoice_no = "/".join(Invoice_no)

                Importer_name = text_with_boxes.split("INDEX\nDT")[1].split("11.DECLARANT")[0]
                Importer_name = Importer_name.strip()

                # Importer_name_and_addr = text_with_boxes.split("INDEX\nDT")[1].split("14.NTN")[0]
                # Importer_name_and_addr = Importer_name_and_addr.split("\n")
                # Importer_name_and_addr = [x if "12." not in x else "" for x in Importer_name_and_addr]
                # Importer_name_and_addr = [x if "CARGO LINKERS" not in x else "" for x in Importer_name_and_addr]
                #
                # for i in range(len(Importer_name_and_addr)):
                #     if "" in Importer_name_and_addr:
                #         Importer_name_and_addr.remove("")
                # if Importer_name_and_addr[-2] != Importer_name_and_addr[0]:
                #     Importer_name_and_addr = Importer_name_and_addr[0].split("11.DECLARANT")[0].strip() + " " + Importer_name_and_addr[-2].strip() + " " + Importer_name_and_addr[-1].strip()
                # else:
                #     Importer_name_and_addr = Importer_name_and_addr[0].split("11.DECLARANT")[0].strip() + " " + Importer_name_and_addr[-1].strip()
                # Importer_name_and_addr = Importer_name_and_addr.replace(". ", ".").split("TEL")[0].strip()

                Place_of_Delivery = text_with_boxes.split("DELIVERY TERMS")[1].split("31.NUMBER")[0].split("-")[0].strip().lower()
                Place_of_Delivery = Place_of_Delivery.split()
                Place_of_Delivery_list = set_list_order_preserved(Place_of_Delivery)
                if len(Place_of_Delivery_list) > 2:
                    Place_of_Delivery_list = Place_of_Delivery[1:-1]
                Place_of_Delivery = " ".join(Place_of_Delivery_list)

                Gross_WT = float(text_with_boxes.split("OSS WT")[1].split("35.GENERAL")[0].split("\n")[1].split()[-2].replace(",",""))
                Net_WT = float(text_with_boxes.split("NET WT")[1].split("36.IN")[0].replace("MT", "").strip().replace(",",""))

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

                GD_file_data_dict = {"Invoice_no":Invoice_no,"Name":Name,"Address":Address,"Place_of_Delivery":Place_of_Delivery,"Gross_WT":Gross_WT,"Net_WT":Net_WT,"Value":Value,"Country":Country,"No_of_packages":No_of_packages, "Importer_name_and_addr":Importer_name, "No_of_units_1": No_of_units_1, "No_of_units_2": No_of_units_2}

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

    Invoice_no = "" if Invoice_df.iloc[7, 1] in [None, "None"] else Invoice_df.iloc[7, 1]
    Invoice_no = Invoice_no.replace("/202", "/2")

    Name = "" if Invoice_df.iloc[70, 9] in [None, "None"] else Invoice_df.iloc[70, 9]
    Name = Name.replace("FOR:", "").strip()

    Importer_name_and_addr = "" if Invoice_df.iloc[8, 1] in [None, "None"] else Invoice_df.iloc[8, 1]
    Importer_name_and_addr = Importer_name_and_addr.strip()

    Place_of_Delivery_full = "" if Invoice_df.iloc[12, 2] in [None, "None"] else Invoice_df.iloc[12, 2]
    Place_of_Delivery_full = Place_of_Delivery_full.strip()
    Place_of_Delivery = Place_of_Delivery_full.split("-")[0]
    Place_of_Delivery = Place_of_Delivery.strip()

    Gross_WT = 0 if Invoice_df.iloc[64, 4] in [None, "None"] else Invoice_df.iloc[64, 4]
    Gross_WT = float(Gross_WT)/1000

    Net_WT = 0 if Invoice_df.iloc[63, 4] in [None, "None"] else Invoice_df.iloc[63, 4]
    Net_WT = float(Net_WT)/1000

    No_of_packages_list = Invoice_df.iloc[16: 59, 2].tolist()
    No_of_packages = ""
    for i in No_of_packages_list[::-1]:
        if type(i) == type(1) and i != 0:
            No_of_packages = i
            break

    Value = "" if Invoice_df.iloc[60, 11] in [None, "None"] else Invoice_df.iloc[60, 11]
    Value = float(Value)
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

    Name = "" if Invoice_df.iloc[107, 9] in [None, "None"] else Invoice_df.iloc[107, 9]
    Name = Name.replace("For", "").strip()

    Importer_name = "" if Invoice_df.iloc[18, 2] in [None, "None"] else Invoice_df.iloc[18, 2]
    Importer_name = Importer_name.strip()
    # Importer_address = "" if Invoice_df.iloc[14, 2] in [None, "None"] else Invoice_df.iloc[14, 2]
    # Importer_address = Importer_address.strip()
    #
    # Importer_name_and_addr = Importer_name + " " + Importer_address

    Place_of_Delivery = "" if Invoice_df.iloc[21, 2] in [None, "None"] else Invoice_df.iloc[21, 2]
    Place_of_Delivery_full = Place_of_Delivery.replace(","," -").strip()
    Place_of_Delivery = Place_of_Delivery_full.split("-")[0]
    Place_of_Delivery = Place_of_Delivery.strip()

    Gross_WT = "" if Invoice_df.iloc[95, 10] in [None, "None"] else Invoice_df.iloc[95, 10]
    Gross_WT = float(Gross_WT) / 1000

    Net_WT = "" if Invoice_df.iloc[95, 9] in [None, "None"] else Invoice_df.iloc[95, 9]
    Net_WT = float(Net_WT) / 1000

    No_of_packages = "" if Invoice_df.iloc[95, 3] in [None, "None"] else Invoice_df.iloc[95, 3]

    Value = "" if Invoice_df.iloc[95, 12] in [None, "None"] else Invoice_df.iloc[95, 12]
    Value = math.floor(Value)

    No_of_units_1 = ""
    No_of_units_2 = ""

    Country = Place_of_Delivery_full.split("-")[-1].strip()

    Invoice_file_data_dict = {"Invoice_no": Invoice_no, "Name": Name,
                              "Place_of_Delivery": Place_of_Delivery,
                              "Gross_WT": Gross_WT, "Net_WT": Net_WT, "Value": Value, "Country": Country,
                              "No_of_packages": No_of_packages, "Importer_name_and_addr": Importer_name,
                              "No_of_units_1": No_of_units_1, "No_of_units_2": No_of_units_2}

    return Invoice_file_data_dict


def Akhtar_Invoice(file):
    Invoice_df = pd.read_excel(file)
    Invoice_df = Invoice_df.fillna('')
    Invoice_no = "" if Invoice_df.iloc[19, 10] in [None, "None"] else Invoice_df.iloc[19, 10]

    Name = "Akhtar Textile Industries (Pvt) LTD"

    Importer_name = "" if Invoice_df.iloc[15, 4] in [None, "None"] else Invoice_df.iloc[15, 4]
    Importer_name = Importer_name.strip()
    Importer_address_1 = "" if Invoice_df.iloc[16, 4].strip() in [None, "None"] else Invoice_df.iloc[16, 4].strip()
    Importer_address_1 = Importer_address_1.strip()
    Importer_address_2 = "" if Invoice_df.iloc[17, 4].strip() in [None, "None"] else Invoice_df.iloc[17, 4].strip()
    Importer_address_2 = Importer_address_2.strip()

    Importer_name_and_addr = Importer_name + " " + Importer_address_1.strip() + " " + Importer_address_2.strip()

    Place_of_Delivery = "" if Invoice_df.iloc[22, 4] in [None, "None"] else Invoice_df.iloc[22, 4]
    Place_of_Delivery = Place_of_Delivery.replace(",","").strip()

    Gross_WT = 0 if Invoice_df.iloc[9, 10] in [None, "None", ""] else Invoice_df.iloc[95, 10]
    Gross_WT = float(Gross_WT) / 1000

    Net_WT = 0 if Invoice_df.iloc[95, 9] in [None, "None", ""] else Invoice_df.iloc[95, 9]
    Net_WT = float(Net_WT) / 1000

    No_of_packages = "" if Invoice_df.iloc[97, 4] in [None, "None"] else Invoice_df.iloc[97, 4]

    Value = 0 if Invoice_df.iloc[97, 11] in [None, "None", ""] else Invoice_df.iloc[97, 11]
    Value = math.floor(Value)

    No_of_units_1 = ""
    No_of_units_2 = ""

    Country = Importer_name_and_addr.split(",")[-1].strip() if Importer_name != "LEVI STRAUSS & CO." else "United States"

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

    Gross_WT = "" if Invoice_df.iloc[62, 34] in [None, "None"] else Invoice_df.iloc[62, 34]
    Gross_WT = float(Gross_WT) / 1000

    Net_WT = "" if Invoice_df.iloc[62, 37] in [None, "None"] else Invoice_df.iloc[62, 37]
    Net_WT = float(Net_WT) / 1000

    No_of_packages = "" if Invoice_df.iloc[62, 22] in [None, "None"] else Invoice_df.iloc[62, 22]

    Value = "" if Invoice_df.iloc[63, 41] in [None, "None"] else Invoice_df.iloc[63, 41]
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
    # Importer_addr = "" if Invoice_df.iloc[15, 7] in [None, "None"] else Invoice_df.iloc[15, 7]
    # Importer_name_and_addr = Importer_name.strip() + " " + Importer_addr.strip()
    Importer_name = Importer_name.strip()

    Place_of_Delivery = "" if Invoice_df.iloc[11, 4] in [None, "None"] else Invoice_df.iloc[11, 4]
    Place_of_Delivery_full = Place_of_Delivery.replace(","," -").strip()
    Place_of_Delivery = Place_of_Delivery.split("-")[0]
    Place_of_Delivery = Place_of_Delivery.strip()

    Gross_WT = "" if Invoice_df.iloc[66, 0] in [None, "None"] else Invoice_df.iloc[66, 0]
    Gross_WT = float(Gross_WT) / 1000

    Net_WT = "" if Invoice_df.iloc[66, 2] in [None, "None"] else Invoice_df.iloc[66, 2]
    Net_WT = float(Net_WT) / 1000

    No_of_packages = "" if Invoice_df.iloc[59, 26] in [None, "None"] else Invoice_df.iloc[59, 26]

    Value = "" if Invoice_df.iloc[59, 40] in [None, "None"] else Invoice_df.iloc[59, 40]
    Value = math.floor(Value)

    No_of_units_1 = ""
    No_of_units_2 = ""

    Country = Place_of_Delivery_full.split("-")[-1].strip()

    Invoice_file_data_dict = {"Invoice_no": Invoice_no, "Name": Name,
                              "Place_of_Delivery": Place_of_Delivery,
                              "Gross_WT": Gross_WT, "Net_WT": Net_WT, "Value": Value, "Country": Country,
                              "No_of_packages": No_of_packages, "Importer_name_and_addr": Importer_name,
                              "No_of_units_1": No_of_units_1, "No_of_units_2": No_of_units_2}

    return Invoice_file_data_dict


def Compare_files(GD_file_path, Invoice_path, Title):
    try:
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

        Name = GD_file_data["Name"].lower() == Invoice_data["Name"].lower()
        # Address =GD_file_data["Address"].lower() == Invoice_data["Address"].lower()

        # Importer_name_and_addr = GD_file_data["Importer_name_and_addr"].lower() == Invoice_data["Importer_name_and_addr"].lower()
        Place_of_Delivery = GD_file_data["Place_of_Delivery"].lower() == Invoice_data["Place_of_Delivery"].lower()

        Gross_WT = round(GD_file_data["Gross_WT"], 3) == round(Invoice_data["Gross_WT"], 3)

        Net_WT =round(GD_file_data["Net_WT"], 3) == round(Invoice_data["Net_WT"] , 3)

        Value = GD_file_data["Value"] == Invoice_data["Value"]

        Country = GD_file_data["Country"].lower() == Invoice_data["Country"].lower()
        No_of_packages = GD_file_data["No_of_packages"] == Invoice_data["No_of_packages"]

        # No_of_units_1 = GD_file_data["No_of_units_1"] == Invoice_data["No_of_units_1"]
        # No_of_units_2 = GD_file_data["No_of_units_2"] == Invoice_data["No_of_units_2"]

        matched = {"Invoice_no": Invoice_no, "Name": Name, "Place_of_delivery": Place_of_Delivery,
                                         "Gross_wt": Gross_WT, "Net_wt": Net_WT, "Value": Value, "Country": Country,
                                         "No_of_packages": No_of_packages}

        return matched
    except Exception as e:
        print(e)
        return {f"error: {e}"}


# Invoice = 'C:\\Users\\admin\\Downloads\\INVOICE ALI MURTAZA.pdf'
# Invoice = 'C:\\Users\\admin\\Downloads\\INVOCIE PROLINE 644.xls'
# Invoice = 'C:\\Users\\admin\\Downloads\\INVOCIE LIBERTY 1068.xlsx'
Invoice = 'C:\\Users\\admin\\Downloads\\INVOICE INDIGO 1316.xlsx'
# Invoice = 'C:\\Users\\admin\\Downloads\\INVOCIE SIDDIQSONS 0517.xlsx'
# GD_file = 'C:\\Users\\admin\\Downloads\\differentpartygdandinv\\GD FORNT PAGE SIDDIQSONS 517.pdf'
# GD_file = 'C:\\Users\\admin\\Downloads\\differentpartygdandinv\\GD FRONT PAGE ALI MURTAZA 1816.pdf'
# GD_file = 'C:\\Users\\admin\\Downloads\\differentpartygdandinv\\GD FORNT PAGE AKHTAR 1586B.pdf'
GD_file = 'C:\\Users\\admin\\Downloads\\differentpartygdandinv\\GD FORNT PAGE INDIGO 1316.pdf'
# GD_file = 'C:\\Users\\admin\\Downloads\\differentpartygdandinv\\GD FORNT PAGE LIB 1068.pdf'
# GD_file = 'C:\\Users\\admin\\Downloads\\differentpartygdandinv\\GD FRONT PAGE PROLINE 644.pdf'
# GD_file = 'C:\\Users\\admin\\Downloads\\ALI MURTAZA GD.pdf'

if __name__ == "__main__":
    try:
        matched= Compare_files(Invoice_path=Invoice, GD_file_path=GD_file, Title="Indigo")
        print(matched)
    except Exception as e:
        print(e)

