import csv
import random
import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from string import Template

MY_ADDRESS = 'mail@gmail.com'
PASSWORD = 'pwd'


class Bcolors:
    HEADER = '\033[94m'
    OKGREEN = '\033[92m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    ENDC = '\033[0m'


def read_csv(ponchos_file):
    """
    lecture de la liste des participants
    """
    invites = []
    print(Bcolors.HEADER + "Lecture des participants..." + Bcolors.ENDC, end=" ")
    with open(file=ponchos_file, mode='r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')  # <-- Tu peux choisir ton délimiteur ici
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
            else:
                invites += [Poncho(row[0], row[1], row[2])]
                line_count += 1
    print(Bcolors.OKGREEN + "Lecture terminée." + Bcolors.ENDC, end=" ")
    print("Il y a {guests} participants.".format(guests=line_count - 1))
    return invites


class Poncho:
    """Un Poncho"""

    def __init__(self, prenom, mail, avoid):
        self.prenom = prenom
        self.mail = mail
        if avoid == "":
            self.avoid = []
        else:
            self.avoid = avoid.split(';')
        self.avoid.append(self.prenom)
        self.priority = len(self.avoid)

    def show(self):
        print("========================")
        print("Prenom   : " + self.prenom)
        print("Mail     : " + self.mail)
        print("À éviter : ", end="")
        print(self.avoid)
        print("Priorité : " + str(self.priority))
        print("")
        return


def searchPonchoByName(plist, prenom):
    for poncho in plist:
        if poncho.prenom == prenom:
            return poncho
    raise ModuleNotFoundError("Le Poncho que vous recherchez (" + prenom + ") n'a pas été trouvé")


def insertionSort(arr):
    print(Bcolors.HEADER + "Début du tri..." + Bcolors.ENDC, end=" ")
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and key.priority < arr[j].priority:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    print(Bcolors.OKGREEN + "Tri terminé." + Bcolors.ENDC)
    arr.reverse()
    return arr


def tirage(plist):
    """
    Prend une liste triée de participants en fonction de leur priorité
    :param plist: une liste de Ponchos
    :return: l'arrangement des cadeaux
    """
    print(Bcolors.HEADER + "Début du tirage..." + Bcolors.ENDC, end=" ")
    # liste des secret santa restants (copy)
    pereNoels = plist.copy()
    # liste des gosses restants (copy)
    enfants = plist.copy()
    # arrangement
    arr = []
    for pere_noel in pereNoels:
        rd_enfant = pere_noel
        choices = 0
        while rd_enfant.prenom in pere_noel.avoid and choices < 50:
            rd_enfant = random.choice(enfants)
            choices += 1
        if choices >= 50:
            raise RuntimeError('Pas réussi à trouver un enfant pour ' + pere_noel.prenom)
        arr += [[pere_noel, rd_enfant]]
        enfants.remove(rd_enfant)
    print(Bcolors.OKGREEN + "Tirage terminé." + Bcolors.ENDC)
    return arr


def show_arrangement(arr, show):
    monHash = "#########"
    for a in arr:
        if show:
            print(a[0].prenom + " va offrir un cadeau à " + a[1].prenom)
        else:
            print(monHash + " va offrir un cadeau à " + monHash)


def send(arr):
    print(Bcolors.HEADER + "Début de l'envoi..." + Bcolors.ENDC, end=" ")
    smtp = smtplib.SMTP(host='smtp.gmail.com', port=587)
    smtp.starttls()
    smtp.login(MY_ADDRESS, PASSWORD)

    def read_template(filename):
        """
        Returns a Template object comprising the contents of the
        file specified by filename.
        """
        with open(filename, 'r', encoding='utf-8') as template_file:
            template_file_content = template_file.read()
        return Template(template_file_content)

    def addImageToHtml(img):
        fp = open('/home/antoine/Documents/Ponchokado/images/' + img + '.png', 'rb')
        messageImage = MIMEImage(fp.read())
        fp.close()
        messageImage.add_header('Content-ID', '<' + img + '>')
        return messageImage

    for a in arr:
        strFrom = MY_ADDRESS
        strTo = a[0].mail
        html_template = read_template('/home/antoine/Documents/Ponchokado/mail2020.html')

        # Create the root message and fill in the from, to, and subject headers
        msgRoot = MIMEMultipart('related')
        msgRoot['Subject'] = '[PONCHO] TIRAGE CADEAU DE NOËL'
        msgRoot['From'] = strFrom
        msgRoot['To'] = strTo
        msgRoot.preamble = 'This is a multi-part message in MIME format.'

        # Encapsulate the plain and HTML versions of the message body in an
        # 'alternative' part, so message agents can decide which they want to display.
        msgAlternative = MIMEMultipart('alternative')
        msgRoot.attach(msgAlternative)

        msgText = MIMEText(
            'Alternative Plain text. Si tu vois ça, c\'est que y a eu pun problème quelque part.' +
            ' Essaie de lire ce mail depuis ton pc stp (et envoie moi un mp pour m\'en informer)')
        msgAlternative.attach(msgText)

        # We reference the image in the IMG SRC attribute by the ID we give it below
        html = html_template.substitute(ENFANT=a[1].prenom)
        msgText = MIMEText(html, 'html')
        msgAlternative.attach(msgText)

        for i in ["content-bottom", "content-top", "header-top_nostripes", "snow-background", "Merry_Christmas"]:
            msgImage = addImageToHtml(i)
            msgRoot.attach(msgImage)

        # Send the email (this example assumes SMTP authentication is required)
        smtp.send_message(from_addr=strFrom, to_addrs=strTo, msg=msgRoot)
    smtp.quit()
    print(Bcolors.OKGREEN + "Envoi terminé." + Bcolors.ENDC)


if __name__ == '__main__':
    ponchos_list = read_csv("ponchos.csv")
    ponchos_list = insertionSort(ponchos_list)

    arrangement = tirage(ponchos_list)

    show_arrangement(arrangement, True)

    arr_test = [[searchPonchoByName(ponchos_list, "Antoine"), searchPonchoByName(ponchos_list, "Orlane")]]

    send(arr_test)
