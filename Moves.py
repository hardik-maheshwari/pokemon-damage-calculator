import csv

input_filename = "./data/all_moves.csv"
output_filename = "./data/gen3.csv"

column_headings = [
    "Name",
    "Type",
    "Category",
    "Effect",
    "Power",
    "Accuracy",
    "Probability",
    "Generation",
]


with open(input_filename, encoding="utf-8") as input_file:
    with open(output_filename, "w", encoding="utf-8", newline="") as output_file:

        writer = csv.writer(output_file,delimiter="|")
        reader = csv.reader(input_file,delimiter=",")
        writer.writerow(column_headings)
        input_file.readline()

        for row in reader:

            (
                name,
                pokemon_type,
                category,
                effect,
                power,
                acc,
                pp,
                tm,
                probability,
                generation,
            ) = row

            if int(generation) > 3:
                continue

            if category != "Status":

                if pokemon_type in {
                    "Normal",
                    "Fighting",
                    "Flying",
                    "Ground",
                    "Rock",
                    "Bug",
                    "Ghost",
                    "Steel",
                    "Poison",
                }:
                    category = "Physical"

                else:
                    category = "Special"

            ans = [
                (
                    name,
                    pokemon_type,
                    category,
                    effect,
                    power,
                    acc,
                    probability,
                    generation,
                )
            ]

            writer.writerows(ans)


# reader = csv.reader(open("Gen3_temp.csv", "r", encoding="utf-8"), delimiter=",")
# writer = csv.writer(open("Gen3.csv", "w", encoding="utf-8", newline=""), delimiter="|")
# writer.writerows(reader)
