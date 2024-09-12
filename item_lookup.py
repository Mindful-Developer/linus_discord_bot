import csv


def lookup_item(item, tier):
    matching_items = []
    with open("items.csv", "r") as f:
        reader = csv.reader(f)
        for row in reader:
            if item.lower() in row[1].lower() and "T" + str(tier)[0] in row[0] and "ARTEFACT" not in row[0]:
                matching_items.append(row[0])
    return matching_items

def get_item_name(item):
    with open("items.csv", "r") as f:
        reader = csv.reader(f)
        for row in reader:
            if item == row[0]:
                return row[1]


if __name__ == "__main__":
    print(lookup_item("bear paws", 4.4))
    print(get_item_name("T4_ARTEFACT_2H_DUALAXE_KEEPER"))