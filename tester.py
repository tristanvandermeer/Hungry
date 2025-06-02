# Counting
total = 0
math_total = 0
pdf_total = 0
doc_total = 0
with open("file_links.txt", "r") as file:
    for line in file:
        total += 1
        if "math"  in line.lower():
            math_total += 1
        
    


print(f"TOTAL IS: {total}")
print(f"MATH TOTAL IS: {math_total}")

# Wow ! 2332