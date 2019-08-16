import json

if __name__ == "__main__":
    data = json.load(open("final_4.json"))
    # print(data)
    for info in data.values():
        filename = info["filename"]
        text_name = "./txts/" + "gt_" + filename.replace("jpg", "txt")
        # print(info)
        if len(info["regions"]) == 0:
            continue
        f = open(text_name, "w", encoding="utf-8")
        for poly in info["regions"]:
            print(poly)
            if poly is not None and poly["shape_attributes"]["name"] == "polygon":
                # print(poly["shape_attributes"])
                print("#######")
                polygon = []
                for x, y in zip(poly["shape_attributes"]["all_points_x"], poly["shape_attributes"]["all_points_y"]):
                    polygon.append(str(x))
                    polygon.append(str(y))
                if len(polygon) == 8:
                    f.write(",".join(polygon))
                    f.write(",###\n")
            else:
                print(poly)
        f.close()
