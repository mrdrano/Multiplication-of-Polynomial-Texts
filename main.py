#poly = "(A+2*B^2)(B+3*C^3)(2*A+B+C)"
poly = input("please input the polynomials: ")
to_list = list(poly)                    # transform the string to the list to benefit the operation

# (X+2*Y)(2*X^2-Y^2+Z), (2*X+3*Y+4*Z)(XY^2+X^2Y+Z^2), (A+2*B^2)(B+3*C^3)(2*A+B+C)
while (1):                              # Start by removing left "("
    if("(" in to_list):
        to_list.remove("(")
    else:
        break

to_str = "".join(to_list)               # then again to put the remaining in a string to do operation
#print(to_str.split(")")[:-1])

def checker(poly):  # check the number of operands
    count_add = poly.count("+")
    count_minus = poly.count("-")             # to find how many + and - in the sub-polys and then return

    if ("-" not in poly and count_add == 1):  # single + or - in the string
        key1 = poly.split("+")
        key1[1] = f"+"+key1[1]
        return key1

    if ("+" not in poly and count_minus == 1):
        key1 = poly.split("-")
        key1[1] = f"-"+key1[1]
        return key1

    if ("+" in poly and "-" in poly):  # simultaneously, + or - in the string
        add = poly.find("+")
        minus = poly.find("-")

        one = []
        two = []
        three = []

        if (count_add > 0 and count_minus > 0):
            if (add > minus):       # add is behind  - +
                one.append(poly[:minus])
                two.append(poly[minus:add])
                three.append(poly[add:])

                key2 = one + two + three
                return (key2)

            if(add < minus):        # minus is behind + -
                one.append(poly[:add])
                two.append(poly[add:minus])
                three.append(poly[minus:])

                key2 = one + two + three
                return key2
    all = []
    if (count_add == 2 and count_minus == 0):
        kkk = poly.split("+")
        all.append(kkk[0])

        for each in kkk[1:]:
            each = f"+" + each
            all.append(each)
        return all

    if(count_minus == 2 and count_add == 0):
        kkk = poly.split("-")
        all.append(kkk[0])

        for each in poly.split("-")[1:]:
            each = f"-" + each
            all.append(each)
        return all

def signal_processor(unprocessed):
    nxx = []                                    # ['X2*X^2', 'X-Y^2', 'X+Z', '+2*Y2*X^2', '+2*Y-Y^2', '+2*Y+Z']
    for each in unprocessed:                    # nxx is a list used to store the items after the (+-) operation -> (+,+) = + , etc.
        if ("+" not in each and "-" not in each):
            nxx.append(each)                    # in this segment funcitonm, just focus on the unprocessed poly
                                                # to follow positive, negative in math way => (-,-) -> + etc.
        if (each.count("-") == 1 and "+" not in each):
            each = each.replace("-", "")        #then return
            each = f"-" + each
            nxx.append(each)

        if (each.count("+") == 1 and "-" not in each):
            each = each.replace("+", "")
            each = f"+" + each
            nxx.append(each)

        if ("+" in each and "-" in each):
            each = each.replace("+", "")
            each = each.replace("-", "")
            each = f"-" + each
            nxx.append(each)

        if (each.count("+") == 2):
            each = each.replace("+", "")
            each = each.replace("+", "")
            each = f"+" + each
            nxx.append(each)

        if (each.count("-") == 2):
            each = each.replace("-", "")
            each = each.replace("-", "")
            each = f"-" + each
            nxx.append(each)
    return (nxx)


def coefficient(res_signals):                 # find in the unprocessed poly that the coeficient is in front of "*"
    coff = []                                 # and to combine them (multiply them) to the new coefficient
    residual = []
    for aaa in res_signals:
        if ("*" not in aaa):
            one = 1
            coff.append(one)
            residual.append(aaa)

        if (aaa.count("*") == 1):

            place1 = aaa.find("*")
            cof1 = ""
            for nn in aaa[:place1]:
                if (nn.isdigit()):
                    cof1 += nn

            residual1 = cof1 + "*"
            aaa = aaa.replace(residual1, "")
            cof1 = int(cof1)
            coff.append(cof1)
            residual.append(aaa)

        if (aaa.count("*") == 2):

            place1 = aaa.find("*")
            place2 = aaa[place1 + 1:].find("*")
            place2 += (place1 + 1)

            cof1 = ""
            cof2 = ""
            for nn in aaa[:place1]:
                if (nn.isdigit()):
                    cof1 += str(nn)

            residual1 = cof1 + "*"
            cof1 = int(cof1)

            for nn_next in aaa[place1 + 1:place2]:
                if (nn_next.isdigit()):
                    cof2 += str(nn_next)

            residual2 = cof2 + "*"
            aaa = aaa.replace(residual1, "")
            aaa = aaa.replace(residual2, "")

            cof2 = int(cof2)
            cof_sum = cof1 * cof2

            residual.append(aaa)
            coff.append(cof_sum)

    return coff, residual                                    # separate the poly(residual) and coefficient

def signs_and_res_items_after(res_coefficient, res_items):
    signs = []
    res_items_after = []                                     # this focus on signs of each poly's item
                                                             # by creating a list to store each sign (+ or -)
    for each in res_items:
        if ("+" not in each and "-" not in each):
            signs.append("+")
            res_items_after.append(each)

        if ("-" in each and "+" not in each):
            signs.append("-")
            each = each.replace("-", "")
            res_items_after.append(each)

        if ("+" in each and "-" not in each):
            signs.append("+")
            each = each.replace("+", "")
            res_items_after.append(each)

    return signs, res_items_after

# a2 = ['XXY^2', 'XX^2Y', 'XZ^2', 'YXY^2', 'YX^2Y', 'YZ^2', 'ZXY^2', 'ZX^2Y', 'ZZ^2']

def round_up(res_coefficient, aaa_items, aaa_signs):
    combined = []                                            # since haven't deal with same x/y/z (or A/B/C)
    fin = []                                                 # here is the operaiton, and also delete the repetitive x/y/z (or A/B/C)
                                                             # to the power
    for each in aaa_items:
        if ("^" in each and each.count("^") == 1):
            position = each.find("^")

            item = each[position - 1]
            power = int(each[position + 1])
            delete = each[position - 1:position + 2]
            fin.append(delete)  # save B^C

            each_new = each.replace(delete, "")

            combined.append(each_new)  # save -> A(B^C)
                                        #  ['XX^2', '-XY^2', '+XZ', '+YX^2', '-YY^2', '+YZ']

    nnew = []
    for i in range(len(combined)):
        if (len(combined[i]) == 2):
            if (combined[i][0] == combined[i][1]):
                ppow = 2
                bbase = f"{combined[i][0]}^{ppow}"
                nnew.append(bbase)

            else:
                nnew.append(combined[i])
        else:
            nnew.append(combined[i])

    # print(nnew)     # center on nnew and fin's opertion

    return fin, combined, nnew

def combination(fin, nnew):
    raw_final = []

    for i in range(len(fin)):
        wwe = str(nnew[i]) + str(fin[i])
        raw_final.append(wwe)

    return raw_final

def the_final(raw_final):           # start to combine all the materials above mentioned and operated

    ddos = []
    for each in raw_final:

        up = each.find("^")
        target = each[up - 1]
        power = int(each[up + 1])

        search = each[:up - 1] + each[up + 2:]

        if (target in search):
            power += 1
            search = search.replace(target, "")
            search = search + f"{target}^{power}"

            ddos.append(search)

        else:
            ddos.append(each)

    return ddos

def retrace(ddos, raw):

    fic = []
    for i in range(len(raw)):
        if ("^" in raw[i]):
            fic.append(1)
        else:
            fic.append(0)

    lastt = []  # fic =  [1, 1, 0, 1, 1, 0]

    h = 0  # raw =  ['XX^2', '-XY^2', '+XZ', '+YX^2', '-YY^2', '+YZ']
    for i in range(len(fic)):  # ddos = ['X^3', '-XY^2', '+YX^2', '-Y^3']  0-3
        if (fic[i] == 1):
            lastt.append(ddos[h])
            h += 1

        if (fic[i] == 0):
            lastt.append(raw[i])

    return lastt

def retrace_or_not(ddos, listtt):    # to determine whether to retrace in the above def retrace_or_not
    flag = 0                         # because some polys are just simple multiplication
    for each in listtt:

        if ("^" in each):
            flag = 0
        else:
            flag = 1
            break

    if (flag == 1):
        return retrace(ddos, listtt)

    else:
        return ddos

def outcome(coefficient, signed_items):
    watch1 = []

    for i in range(len(coefficient)):

        if (i == 0):
            if (coefficient[i] == 1):
                watch1.append(signed_items[i])

            else:
                signed_items[i] = f"{coefficient[i]}*{signed_items[i]}"
                watch1.append(signed_items[i])

        if (i > 1):
            if (coefficient[i] == 1):
                watch1.append(signed_items[i])
            else:
                signed_items[i] = signed_items[i][:1] + f"{coefficient[i]}*" + signed_items[i][1:]
                watch1.append(signed_items[i])

    return watch1

items = len(to_str.split(")")[:-1])                         # to determine whether the poly has two or three items to be multiplied
                                                            # two -> items == 2 ; three -> items == 3
if(items == 2):
    first = to_str.split(")")[:-1][0]                       # First : find the left and right sub-poly
    second = to_str.split(")")[:-1][1]

    def multiplication_in2(first, second):
        unprocessed_result = []
        left = checker(first)
        right = checker(second)

        for i in left:                                     # this is for each element to be corresponded to each in the right,
            for j in right:                                # then go into the processing function in (1. signal processing ; 2. coefficient processing)
                unprocessed_result.append(i+j)

        sign1 = signal_processor(unprocessed_result)
        coff1 = coefficient(sign1)[0]
        a1 = coefficient(sign1)[1]

        aaa_signs1 = signs_and_res_items_after(coff1, a1)[0]
        aaa_items1 = signs_and_res_items_after(coff1, a1)[1]

        b1 = round_up(coff1, a1, aaa_signs1)
        c1 = combination(b1[0], b1[2])
        d1 = the_final(c1)
        e1 = retrace_or_not(d1,a1)
        f1 = outcome(coff1,e1)

        for f_sub in f1:
            print(f_sub, end="")

    multiplication_in2(first,second)

if(items == 3):                                       # in this section, all the operation is the same as in those functions
                                                      # but since after getting the unprocessed poly, there will probably be
    first = to_str.split(")")[:-1][0]                 # 3 corfficient or 2, 1 etc, it's a bit tought to apply in the same function
    second = to_str.split(")")[:-1][1]                # so I do it in each line using loops
    third = to_str.split(")")[:-1][2]                 # most importantly, finding the coeffiecient and power of each variable A,B,C
                                                      # and combine the same variable together
    first_split = first.split("+")
    second_split = second.split("+")
    third_split = third.split("+")

    step_one = []
    for a in first_split:
        for b in second_split:
            for c in third_split:
                step_one.append(a+b+c)

    res1 = []

    for each in step_one:
        if (each == step_one[0]):

            star = each.find("*")
            coff = int(each[star - 1])
            item = each[star + 1]
            delete = each[star - 1:star + 2]

            each = each.replace(delete, "")
            again = each
            if (each[0] == item):
                power = 2
                each = each.replace(each[0], "")
                each = f"{coff}*{item}^{power}{each}"
                res1.append(each)

            if (each[1] == item):
                power = 2
                each = each.replace(each[1], "")
                each = f"{coff}*{item}^{power}{each}"
                res1.append(each)

    for each in step_one[1:]:
        if (each.count("*") == 0):
            if (each[0] == each[1]):
                rep = each[0]
                each = each.replace(each[0], "")
                each = f"{each}{rep}^2"
                res1.append(each)

            if (each[1] == each[2]):

                rep = each[1]
                each = each.replace(each[1], "")
                each = f"{each}{rep}^2"
                res1.append(each)

            else:
               res1.append(each)

        if (each.count("*") == 1):

            position = each.find("*")

            if (position == (len(each) - 2)):  # AB2*A

                coefficient = each[position - 1]
                target = each[position + 1]
                delete = each[position - 1:position + 2]
                each = each.replace(delete, "")

                for ee in each:
                    if (ee == target):
                        power = 2
                        break
                each = each.replace(ee, "")
                each = f"{coefficient}*{target}^2{each}"
                res1.append(each)

            if (position != (len(each) - 2)):  # 'A 3*C^3 B', 'A 3*C^3 C', ' 2*B^2 BB',  2*B^2 BC

                coefficient = each[position - 1]
                target = each[position + 1]

                upp = each.find("^")
                power = each[upp + 1]
                delete = each[position - 1:position + 4]
                each = each.replace(delete, "")  # AB AC BB BC

                num = 0
                for ee in each:
                    if (ee == target):
                        num += 1

                if (num == 0):
                    each = f"{coefficient}*{each}{target}^{power}"
                    res1.append(each)

                if (num == 1):
                    power = int(power) + num
                    each = each.replace(target, "")
                    each = f"{coefficient}*{target}^{power}{each}"
                    res1.append(each)

                if (num == 2):
                    power = int(power) + num
                    each = ""
                    each = f"{coefficient}*{target}^{power}"
                    res1.append(each)

        if (each.count("*") == 2):  # A 3*C^32*A   2*B^2 B 2*A '2*B^23*C^3B', '2*B^23*C^3C'
            star1 = each.find("*")
            star2 = each[star1 + 1:].find("*") + star1 + 1
            target1 = each[star1 + 1]
            target2 = each[star2 + 1]
            coff1 = int(each[star1 - 1])
            coff2 = int(each[star2 - 1])

            if (target2 == each[-1] and len(each) == star2 + 2):
                delete1 = each[star1 - 1:star1 + 4]
                delete2 = each[star2 - 1:star2 + 2]

                pow1 = int(each[star1 + 3])
                pow2 = 1
                each = each.replace(delete1, "")
                each = each.replace(delete2, "")

                if (each == target1):
                    pow1 += 1
                    coff = coff1 * coff2
                    new = f"{coff}*{target1}^{pow1}{target2}"
                    res1.append(new)
                if (each == target2):
                    pow2 += 1
                    coff = coff1 * coff2
                    new = f"{coff}*{target1}^{pow1}{target2}^{pow2}"
                    res1.append(new)

            else:
                delete1 = each[star1 - 1:star1 + 4]  # '2*B^23*C^3  B', '2*B^23*C^3  C'
                delete2 = each[star2 - 1:star2 + 4]
                pow1 = int(each[star1 + 3])
                pow2 = int(each[star2 + 3])
                each = each.replace(delete1, "")
                each = each.replace(delete2, "")

                if (each == target1):
                    pow1 += 1
                    coff = coff1 * coff2
                    new = f"{coff}*{target1}^{pow1}{target2}^{pow2}"
                    res1.append(new)

                if (each == target2):
                    pow2 += 1
                    coff = coff1 * coff2
                    new = f"{coff}*{target1}^{pow1}{target2}^{pow2}"
                    res1.append(new)

        if (each.count("*") == 3):
            star1 = each.find("*")
            star2 = each[star1 + 1:].find("*") + star1 + 1
            star3 = each[star2 + 1:].find("*") + star2 + 1

            coff1 = int(each[star1 - 1])
            coff2 = int(each[star2 - 1])
            coff3 = int(each[star3 - 1])
            coff = coff1 * coff2 * coff3

            delete1 = each[star1 - 1:star1 + 1]
            delete2 = each[star2 - 1:star2 + 1]
            delete3 = each[star3 - 1:star3 + 1]

            each = each.replace(delete1, "")
            each = each.replace(delete2, "")
            each = each.replace(delete3, "")

            each = f"{coff}*{each}"
            res1.append(each)

    #print(res1)
    res2 = []
    for i in range(len(res1)):
        if(i==0):
            res2.append(res1[i])
        else:
            res1[i] = res1[i][:0]+"+"+res1[i][0:]
            res2.append(res1[i])

    for each in res2:
        print(each,end="")



