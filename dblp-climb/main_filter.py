import os


key_word = [
    ["word", "spot"],
    ["scene", "text"],
    ["text", "spot"]
]

s_paper_list = []
res_paper_list = []
key_w_set = set([])

pps = os.listdir("./scene-ocr-target")
for paper_folder in pps:
    cf_files = os.listdir("./scene-ocr-target/"+paper_folder)
    for cf_file in cf_files:
        f = open(
            "./scene-ocr-target/"+paper_folder+"/"+cf_file,
            "rt",
            encoding="utf8"
        )
        cl = f.readlines()
        f.close()
        cl = [l.strip() for l in cl]
        f_length = len(cl)
        i = 0
        while i < f_length:
            ccl = cl[i]
            if ccl.startswith("[") and ccl.endswith("]"):
                i += 2
                current_s_paper = {
                    "key": ccl,
                    "doi-link": cl[i],
                    "conf_jr": paper_folder
                }
                s_paper_list.append(current_s_paper)
            else:
                i += 1
for paper in s_paper_list:
    key_string = paper["key"]
    l_ks = key_string.lower()

    for k_rule in key_word:
        match_count = 0
        for k in k_rule:
            if k in l_ks:
                match_count += 1
        if match_count == len(k_rule):
            if key_string in key_w_set:
                pass
            else:
                res_paper_list.append(paper)

f = open(
    "./res_filter.md",
    "wt",
    encoding="utf8"
)
print("done, " + str(len(res_paper_list)))
for res_p in res_paper_list:
    f.write(res_p["key"] + "\n")
    f.write(res_p["doi-link"] + "\n")
    f.write(res_p["conf_jr"] + "\n")
    f.write("-----------------------------" + "\n")
f.close()