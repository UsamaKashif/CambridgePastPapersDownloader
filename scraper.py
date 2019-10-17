import requests
from bs4 import BeautifulSoup


# main menu
def mainMenu():
    print("Choose from the following options:")
    print("1:Cambridge AS & A Level ")
    print("2:Cambridge Olevel")
    print("3:Cambridge IGCSE")
    print("")

    repeat = True
    while repeat:
        choice = str(input("Enter 1/2/3 to choose the above options: "))
        if choice >= "1" and choice <= "3":
            repeat = False
        else:
            repeat = True

    if choice == "1":
        source = requests.get("https://papers.gceguide.com/A%20Levels/")
    elif choice == "2":
        source = requests.get("https://papers.gceguide.com/O%20Levels/")
    elif choice == "3":
        source = requests.get("https://papers.gceguide.com/IGCSE/")

    return source


def subjectSelection (source):
    repeat = True
    while repeat:
        syllabusCode = str(input(("Enter the 4-digit syllabus code. (5040): "))) #entered by the user 
        allNum = 0
        if len(syllabusCode)==4:
            for i in syllabusCode:
                if i >= "0" and i<="9":
                    allNum += 1
        
        if allNum == 4:
            repeat = False
        else:
            print("please enter 4-digit code: ")

    soup = BeautifulSoup(source.content, "html.parser")
    syllabusCodes = soup.find_all("tr", class_="dir")
    for c in syllabusCodes:
        code = c.a.get("href")
        code = code[code.index("(")+1:-1]
        if ("(") in code:
            code = code[code.index("(")+1:]
        if code == syllabusCode:
            return c.a.get("href")
    return ("No such syllabus code")



def yearValidation(year):
    allNums = 0
    if (len(year)==4):
        for i in year:
            if (i>="0" and i<="9"):
                allNums +=1
    if allNums == 4:
        return True
    else:
        return False
         

def quesPapers(link):
    r = requests.get(link)
    soup = BeautifulSoup(r.content, "html.parser")
    Questions = []
    questions = soup.find_all("tr", class_="file")
    for i in questions:
        if "qp" in i.td.a.text:
            Questions.append(i.td.a)

    return Questions


def Ms (link):
    r = requests.get(link)
    soup = BeautifulSoup(r.content, "html.parser")
    ms = []
    m = soup.find_all("tr", class_="file")
    for i in m:
        if "ms" in i.td.a.text:
            ms.append(i.td.a)
    return ms


def Choice(choice,final_url):
    print("!: single paper")
    print("2: multiple papers")
    print("")
    repeat = True
    while repeat:
        ans = str(input("Enter your choice: "))
        if len(ans)==1 and (ans>="1"and ans<="2"):
            repeat = False

    print("")
    repeat = True
    while repeat:
        paperNum = str(input("Enter the number of paper you want to download, eg.1/2/3/4..: "))
        if len(paperNum)==1 and (paperNum>="1" and paperNum<="9"):
            repeat = False

    print("")
    correct = True
    while correct:
        if ans == "1":
            correct = False
            papers = []
            year = str(input("Enter the year: "))
            while yearValidation(year)==False:
                year = str(input("Enter the year: "))
            year = year[2:]
            if choice == "1":
                select = quesPapers(final_url)
            elif choice == "2":
                select = Ms(final_url)
            for q in select:
                if year == q.text[6:8]:
                    if paperNum == q.get("href")[-6]:
                        papers.append(q.get("href")) 
            return papers
        elif ans == "2":
            correct = False
            year1 = str(input("Enter the starting year: "))
            while yearValidation(year1)==False:
                year1 = str(input("Enter the starting year: "))
            year2 = str(input("Enter the ending year: "))
            while yearValidation(year2)==False:
                year2 = str(input("Enter the ending year: "))
            year1 = year1[2:]
            year2 = year2[2:]
            papers = []
            year = year1
            if choice == "1":
                select = quesPapers(final_url)
            elif choice == "2":
                select = Ms(final_url)
            if int(year1) < int(year2):
                while int(year) <= int(year2):
                    for q in select:
                        if year in q.text[6:8]:
                            if paperNum == q.get("href")[-6]:
                                papers.append(q.get("href"))
                    year = str(int(year)+1)
            return papers


def paperSelection(source,code):
    base_url = source.url
    code = code.replace(" ","%20")
    final_url = str(base_url) + str(code)

    # print (final_url)

    print("Please Select From The Following Options: ")
    print("1:Question Paper")
    print("2:Marking Scheme")
    print("")


    repeat = True
    while repeat:
        choice = str(input("Enter Your Choice: "))
        if len(choice)==1 and (choice>="1" and choice<="2"):
            repeat = False
    
    return Choice(choice,final_url)
        


def createDir(code):
    import os
    dirName = code 
    if not os.path.exists("Downloads"):
        os.mkdir("Downloads")
        print ('Directory Downloads created')
    else:
        print ('Directory Downloads already exists')
    try:
        # Create target Directory
        os.mkdir(f'Downloads/{str(dirName)}')
        print("")
        print("Directory " , dirName ,  " Created.............................") 
    except FileExistsError:
        print("")
        print("Directory " , dirName ,  " already exists...........................")


def downloadPapers(papers,source,code):
    base_url = source.url
    semi_final_url = base_url + code.replace(" ", "%20")
    dirname = code
    # print (semi_final_url)

    createDir(dirname) #create a folder
    print ("")
    print ("Downloading.............")
    for p in papers:
        final_url = semi_final_url +"/"+ p
        # print(final_url)
        r = requests.get(final_url)
        with open(f'Downloads/{dirname}/{p}' , "wb") as f:
            f.write(r.content)



def main():
    loop = "y"

    while loop[0] == "y":

        x = mainMenu()
        y = subjectSelection(x)
        while y == "No such syllabus code":
            print("")
            print ("No such syllabus code -- enter again: ")
            y = subjectSelection(x)

        z = paperSelection(x,y)
    
        downloadPapers(z,x,y)

        # print(z)
        print("")
        print("")
        print ("-----------------------------------------------------------------------------------")

        print ("")

        if z == []:
            print ("Sorry No Papers Found")
            print ("Try Again...")
        else:
            print("Past papers downloaded...")
            print("ENJOY!!")

        loop = input("Do you want to download more: ").lower()

    input("press any key to exit... ")


if __name__ == "__main__":
    main()
