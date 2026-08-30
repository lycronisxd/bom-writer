import tkinter as tk
from tkinter.filedialog import askdirectory, askopenfile, askopenfilename

import datetime
import os

date = datetime.datetime.now()
d = date.strftime("%d")
m = date.strftime("%m")
y = date.strftime("%Y")
dmy = "{0}-{1}-{2}".format(d, m, y)

def menu():
    menu_choice = str(input("""
welcome to the bill of materials writer
by yours truly, andrei acatalinei

what would you like to do?

1) create a new bill of materials
2) convert existing bill of materials to markdown table
3) exit the program

"""))
    
    if menu_choice == "1":
        bomcreator()
    elif menu_choice == "2":
        mdconverter()
    elif menu_choice == "3":
        exit()
    else:
        print("invalid option selected - retry")
        menu()

def bomcreator():
    global bom_filename
    name = str(input("""
enter the name of your project:

"""))
    if len(name) < 1:
        print("project name must be at least 1 character - retry.")
        bomcreator()
    
    pathloop_condition = True
    while pathloop_condition == True:
        print("""
select the path of the folder to save the bill of materials
""")
        root = tk.Tk()
        root.withdraw()
        root.attributes("-topmost", True)
        path = askdirectory()
        root.destroy()
        path_conf = str(input(f"""
are you sure '{path}' is the correct path? (y/n)

"""))
        
        if path_conf == "Y" or path_conf == "y":
            pathloop_condition = False
            if os.path.exists(f"{path}"):
                bom_filename = f"{path}\{name}-bom-{dmy}.csv"
                try:
                    create_bom_file = open(bom_filename, "x")
                except FileExistsError:
                    print("a file with this name already exists. restarting the program")
                    menu()
                with open(bom_filename, 'a') as bomcsv:
                    bomcsv.write("item no.,part no.,part name,qty.,supplier,unit cost,total cost,notes,\n")
                    bomcsv.close()
                    partadder()
            else:
                print("path not found - re-enter the path.")
        else:
            print("re-enter the path.")

def partadder():
    part_no = 0
    type_number = 0
    
    partloop_condition = True
    
    while partloop_condition == True:
        newpart = str(input("""
would you like to add a new part to the bom? (y/n)

"""))
        if newpart == "Y" or newpart == "y":
            part_no += 1
            part_no_str = str(part_no)
            
            typeloop_condition = True
            while typeloop_condition == True:
                type_choice = str(input("""
what type of part would you like to add?

1) pcb/components
2) 3d printed parts
3) mounting hardware
4) other

"""))
                if type_choice == "1":
                    type_prefix = "PCB"
                    typeloop_condition = False
                elif type_choice == "2":
                    type_prefix = "3DP"
                    typeloop_condition = False
                elif type_choice == "3":
                    type_prefix = "MNT"
                    typeloop_condition = False
                elif type_choice == "4":
                    type_prefix = str(input("""
enter a 3 character suffix for the type of part to add:

"""))
                    type_prefix = type_prefix.upper()
                    if len(type_prefix) != 3:
                        print("invalid number of characters - retry.")
                        typeloop_condition = True
                    else:
                        typeloop_condition = False
                else:
                    print("invalid option - retry.")
                    typeloop_condition = True
            
            type_number += 1
            type_number_str = f"{type_number:03}"
            part_type = f"{type_prefix}-{type_number_str}"
                
            nameloop_condition = True
            while nameloop_condition == True:
                part_name = str(input("""
enter the name of the new part:

"""))
                if len(part_name) < 1:
                    print("part name must be at least 1 character - retry.")
                    nameloop_condition = True
                else:
                    nameloop_condition = False
            
            qtyloop_condition = True
            while qtyloop_condition == True:
                try:
                    part_qty = int(input("""
enter the quantity/amount of the new part needed:

"""))
                except ValueError:
                    print("invalid quantity entered - retry.")
                    continue
                part_qty_str = str(part_qty)
                if part_qty < 1:
                    print("part quantity must be at least 1 - retry.")
                    qtyloop_condition = True
                else:
                    qtyloop_condition = False
            
            supplierloop_condition = True
            while supplierloop_condition == True:
                part_supplier = str(input("""
enter the supplier of the new part:

"""))
                if len(part_supplier) < 1:
                    print("part supplier must be at least 1 character - retry.")
                    supplierloop_condition = True
                else:
                    supplierloop_condition = False
            
            totalloop_condition = True
            while totalloop_condition == True:
                try:
                    part_total = float(input("""
enter the total cost of the new part:

$"""))
                except ValueError:
                    print("invalid price entered - retry.")
                    continue
                if part_total < 0:
                    print("part total must be at least $0.00 - retry.")
                    totalloop_condition = True
                else:
                    totalloop_condition = False
            
            part_unit = float(part_total / part_qty)
            
            part_notes = str(input("""
enter your notes for the new part if you have any:

"""))
            
            part_info = f"{part_no_str}, {part_type}, {part_name}, {part_qty_str}, {part_supplier}, ${part_unit:.2f}, ${part_total:.2f}, {part_notes}"
            print(part_info)
            
            with open(bom_filename, 'a') as bomcsv:
                bomcsv.write(f"{part_info},\n")
                bomcsv.close()
            
        elif newpart == "N" or newpart == "n":
            partloop_condition = False
            print("thank you for using bom writer!")
            menu()
        else:
            print("invalid option - retry.")
            partloop_condition = True

def mdconverter():
    print("""
select the path of your bill of materials
""")
    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)
    bom_filename = askopenfilename()
    root.destroy()
    with open(bom_filename, 'r') as bomcsv:
        csv_unparsed = bomcsv.read()
        csv_unparsed = csv_unparsed.replace("\n", "")
        csv_parsed = csv_unparsed.split(",")
        
        print(csv_parsed)
        
        extrarows = int((len(csv_parsed)-1)/8)-1
        
        mdstring = f"|{csv_parsed[0]}|{csv_parsed[1]}|{csv_parsed[2]}|{csv_parsed[3]}|{csv_parsed[4]}|{csv_parsed[5]}|{csv_parsed[6]}|{csv_parsed[7]}|\n|--------|--------|---------|----|--------|---------|----------|-----|\n"
        
        rowadd_counter = 1
        while rowadd_counter <= 2:
            row_no = mdstring.count("\n")
            print(mdstring)
            print(row_no)
            int1 = 0 + (8*(row_no-1))
            int2 = 1 + (8*(row_no-1))
            int3 = 2 + (8*(row_no-1))
            int4 = 3 + (8*(row_no-1))
            int5 = 4 + (8*(row_no-1))
            int6 = 5 + (8*(row_no-1))
            int7 = 6 + (8*(row_no-1))
            int8 = 7 + (8*(row_no-1))
            
            
            mdstring = mdstring + f"|{csv_parsed[int1]}|{csv_parsed[int2]}|{csv_parsed[int3]}|{csv_parsed[int4]}|{csv_parsed[int5]}|{csv_parsed[int6]}|{csv_parsed[int7]}|{csv_parsed[int8]}|\n"
            rowadd_counter += 1
        print("""
select a path to save your converted bill of materials to:
""")
    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)
    md_filepath = askdirectory()
    root.destroy()
    
    newbom_name = bom_filename.rsplit("/")
    last_item = len(newbom_name)-1
    newbom_name = md_filepath + "/" + str(newbom_name[last_item]).replace(".csv", "") + "-converted.md"
        
    open(newbom_name, 'x')
    with open(newbom_name, 'w') as bommd:
        bommd.write(mdstring)
        print("conversion successful!")
        bommd.close()
    menu()

menu()
