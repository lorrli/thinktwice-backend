from fuzzywuzzy import fuzz
import re

def calculate_material_composition(product_details):
    material_type = ['recycled', 'organic']
    all_materials = ['polyester', 'acrylic', 'wool', 'cashmere', 'viscose', 'nylon', 'tencel', 'hemp', 'cotton',
                     'denim', 'linen', 'modal', 'faux fur', 'fleece', 'leather', 'lyocell', 'elastane', 'spandex']
    plastic_materials = ['polyester', 'acrylic', 'nylon', 'fleece', 'elastane', 'spandex']
    percentage = '%'
    return_list = []
    reduced_details = []

    # check for organic and recycled materials
    for detail in product_details:
        for m_type in material_type:
            if (fuzz.partial_ratio(m_type, detail)) > 95:
                reduced_details.append(detail)
                return_list.append(
                    {'material_type': m_type})

        if reduced_details:
            for index, detail in enumerate(reduced_details):
                for material in all_materials:
                    if (fuzz.partial_ratio(material, detail)) > 95:
                        return_list[index]['material'] = material
                        if (fuzz.partial_ratio(percentage, detail)) > 95:
                            return_list[index]['percent'] = int(re.search("(\d+)%", detail).group()[:-1])

    # check for plastic materials
    for index, detail in enumerate(product_details):
        for material in plastic_materials:
            if (fuzz.partial_ratio(material, detail)) > 95 and (fuzz.partial_ratio(percentage, detail)) == 100:
                plastic_object = {'material_type': 'plastic',
                                  'material': material, 'percent': -1}
                
                try: 
                    for m_type in material_type: 
                        plastic_percent = int(
                        re.search("(\d+)", (re.search("(\d+)% " + m_type + " " + material, detail).group())).group())    
                        print(plastic_percent)
                        print(m_type + " " + material)
                except: 
                    plastic_percent = None

                if not (plastic_percent):
                    try:
                        plastic_percent = int(
                            re.search("(\d+)", (re.search("(\d+)% " + material, detail).group())).group())
                    except:
                        plastic_percent = int(
                            re.search("(\d+)%", detail).group()[:-1])
                print(material, ' and da ', plastic_percent)
                plastic_object['percent'] = plastic_percent
                return_list.append(plastic_object)

    # data cleansing of list of dicts
    incomplete_indices = []
    for index, item in enumerate(return_list):
        if ('percent' not in item) or ('material' not in item) or ('material_type' not in item):
            incomplete_indices.append(index)
    if incomplete_indices:
        for index in incomplete_indices:
            return_list.pop(index)
    
    seen = set()
    clean_return_list = []
    for d in return_list:
        t = tuple(d.items())
        if t not in seen:
            seen.add(t)
            clean_return_list.append(d)

    return clean_return_list