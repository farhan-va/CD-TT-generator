import base64
from tkinter import *
from datetime import datetime

win = Tk()
win.title("CD TT Filename Generator")
win.geometry('600x800')
win.configure(bg='#a5e8e5')

iconimgdata = b'iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAYAAABw4pVUAAAABmJLR0QA/wD/A' \
              b'P+gvaeTAAACt0lEQVR4nO3cPWsUURjF8fPMnZckIEQUVHxBVBACMX2qye6C2A' \
              b'QsFC1iZymWfoTU+QIWIoIKCnbq7s5W1n4LSwtBEmH32qgka2ZZZGbuWef8usB' \
              b'k7pP8c3dmZyGAiIiIiIiIiIiIyD+wqk+42d/3VZ+zSp96S5X/zFWKQg8gRykI' \
              b'GQUhE4ceoGndbnH4Gjcaj3FrNNraDzbQlLbvkDyO7WWeFzR/mG0PAu/9dhz7p' \
              b'4CnuPtqfRAA8N52Op1iL/QcgIL8YWaPOp3iSeg5FOQQM+z2eqOHQWeo+oTzvl' \
              b'M/uZdVvfSxnr36fuTrnTsZfhx8hp98K/uWsfd2fzjMX9c+3DFat0PMHNLsBsx' \
              b'Wyg5xZnje6w1vNjnXb60LAgBmCdKlDZgtlRzhU++jN53OYLPRwdDSIABglv2K' \
              b'kpYc4VfMonfdbn+tyblaGwQAzJaRZOswc2WHnALchzwvLjc1U6uDAEAUnUCSr' \
              b'mPGr+J8HONjt9s/08g8TSzCLnKrSLM1lN10eo9rgHuf58Vq7bPUvcCiiNxpJN' \
              b'n1WYdsOIe3eV6U3QlUM0edJ180zp1FnFyZdUjuHF7UOYOCTImTS3DxxVmH3K5' \
              b'zfQU5RpJehYvPBVmb5nOApkw/SikzmVzAve0vNU/zN+2QElEU5uMRBSGjIGT+' \
              b'+2vIg7ulT3UpaYeQURAyCkJGQcjQX9TnfSM3L/aLvHYIGQUhoyBk6K8h7K/5V' \
              b'dMOIaMgZBSEjIKQURAyCkKG/rZXj04kKAUhoyBk6K8h7K/5VdMOIaMgZBSEjI' \
              b'KQURAy9HdZeqcuQSkIGQUhQ38NYX/Nr5p2CBkFIaMgZBSEjIKQURAyCkJGQcg' \
              b'oCBkFIRPs0cnXxwehlp7b8m7za2qHkFEQMgpCRkHIKAgZ+g+oQhoMthr/t3La' \
              b'IWQUhIyCiIiIiIiIiIjIovgJU6xfatsMxgsAAAAASUVORK5CYII='

img = base64.b64decode(iconimgdata)
photo = PhotoImage(data=img)
win.iconphoto(False, photo)

def onCopyClick():
    blankFlag = False
    invalidFlag = False
    if foreignCur.get() == "SR":
        SRFlag = True
    else:
        SRFlag = False
    if ttNum.get() == "":
        blankFlag = True
    cdttStr = cdtt + company.get() + ttNum.get() + " "
    # checking for division for SQCC only
    if company.get() == "SQCC":
        if div.get() == "None":
            blankFlag = True
        else:
            cdttStr += div.get() + " "
    cdttStr += "SR "
    # amount formatting
    amountStr = ""
    foreignAmountStr = ""
    # Root if
    if amount.get() == "":
        blankFlag = True
    else:
        # for foreignCur != "SR", process foreign part
        if not SRFlag:
            if foreignCur.get() == "Other":
                if otherCur.get() == "":
                    blankFlag = True
                if any(c.isdigit() for c in otherCur.get()):
                    invalidFlag = True
                    invalidData('Other currency')
            if foreignAmount.get() == "" or frex.get() == "":
                blankFlag = True
            else:
                if any(c.isalpha() for c in foreignAmount.get()):
                    invalidFlag = True
                    invalidData('Foreign Amount')
                if any(c.isalpha() for c in frex.get()):
                    invalidFlag = True
                    invalidData('Frex')
                else:
                    # validate and add foreign amount
                    if paymentType.get() == "Outgoing":
                        if foreignAmount.get()[0] != '-':
                            foreignAmountStr += '-'
                    foreignAmountStr += '{:,.2f}'.format(float(foreignAmount.get().replace(",", "")))
        # validate and add amount
        if any(c.isalpha() for c in amount.get()):
            invalidFlag = True
            invalidData('Amount')
        else:
            if paymentType.get() == "Outgoing":
                if amount.get()[0] != '-':
                    amountStr += '-'
            amountStr += '{:,.2f}'.format(float(amount.get().replace(",", "")))
            cdttStr += amountStr + " "
    # JV, client and our doc codes
    if jvNum.get() == "" or transactee.get() == "" or clientDocCode.get() == "" or ourDocCode.get() == "":
        blankFlag = True
    cdttStr += jvNum.get().replace("/","-") + ' - '
    # Transactee status
    if paymentType.get() == "Outgoing":
        cdttStr += "Vendor payable to "
    else:
        cdttStr += "Customer receivable from "
    cdttStr += transactee.get() + ' - ' + clientDoc.get() + " " + clientDocCode.get() + " " + ourDoc.get() + " " + ourDocCode.get() + " "
    # Foreign part
    if not SRFlag:
        if foreignCur.get() == "Other":
            cdttStr += otherCur.get().upper() + " "
        else:
            cdttStr += foreignCur.get() + " "
        cdttStr += foreignAmountStr + " " + frex.get() + " "
    # Purpose
    if purpose.get() == "":
        blankFlag = True
    cdttStr += purpose.get() + " "
    # date validation and correction
    dateStr = date.get()
    if dateStr == "":
        blankFlag = True
    else:
        try:
            dateObj = datetime.strptime(dateStr, "%d-%m-%Y")
            cdttStr += dateStr
        except ValueError:
            try:
                dateObj = datetime.strptime(dateStr, "%d/%m/%Y")
                dateFormatted = dateObj.strftime("%d-%m-%Y")
                cdttStr += dateFormatted
            except ValueError:
                invalidFlag = True
                invalidData('Date')
    # static length check
    if len(cdttStr) <= 255:
        if blankFlag:
            fieldLeftBlank()
        elif not invalidFlag:
            clipCopy(cdttStr)
    else:
        lengthOverflow()
    win.after(5000, clearLabel)


def onResetClick():
    company.set(companyList[0])
    div.set(None)
    ttNumEntry.delete(0, END)
    amountEntry.delete(0, END)
    paymentType.set(paymentTypeList[0])
    jvNumEntry.delete(0, END)
    amountEntry.delete(0, END)
    transacteeEntry.delete(0, END)
    otherCurEntry.delete(0, END)
    clientDoc.set(clientDocList[0])
    ourDoc.set(ourDocList[0])
    clientDocCodeEntry.delete(0, END)
    ourDocCodeEntry.delete(0, END)
    foreignCur.set(foreignCurList[0])
    foreignAmountEntry.delete(0, END)
    frexEntry.delete(0, END)
    purposeEntry.delete(0, END)
    dateEntry.delete(0, END)
    outputDisplayText.delete("1.0", END)
    ttNumEntry.focus_set()
    win.after(5000, clearLabel)
    resetLabel.configure(text="All fields cleared!")


def boxClear(event):
    event.widget.delete(0, "end")
    return None


def clipCopy(copyStr):
    win.clipboard_clear()
    win.clipboard_append(copyStr)
    win.update()
    outputLabel.configure(text="Generated and copied!", fg="dark green")
    outputDisplayText.insert(END, copyStr)


def lengthOverflow():
    outputLabel.configure(
        text="Max length of 255 characters exceeded!", fg="red")


def fieldLeftBlank():
    outputLabel.configure(text="Required field(s) left blank!", fg="red")


def invalidData(fieldName):
    outputLabel.configure(text="Invalid data in '" +
                          fieldName + "' field!", fg="red")


def clearLabel():
    outputLabel.configure(text="")
    resetLabel.configure(text="")


cdtt = "CD TT "
# Main frame
mainFrame = Frame(win, padx = 7, pady=7, bg='#a5e8e5')
mainFrame.place(relx=0.5, rely=0.5, anchor=CENTER)
# Inputs frame
inputsFrame = Frame(mainFrame, padx=7, pady=7, bg='#a5e8e5')
inputsFrame.grid(row=0,column=0)
# Header
headerLabel = Label(win, text="CD TT Filename Generator", font=(
    "Consolas", 18), bg='#a5e8e5', fg="dark blue", padx=10, pady=15)
headerLabel.place(relx=0.5, anchor=N)
# Footer
footerLabel = Label(
    win, text="Made by Farhan Arshad\nVersion 0.3.1", bg='#a5e8e5', fg="grey", padx=7, pady=7)
footerLabel.place(relx=1, rely=1, anchor=SE)
# Company
company = StringVar()
companyLabel = Label(inputsFrame, text="Company: ", bg='#a5e8e5')
companyLabel.grid(row=0, column=0, sticky=E)
companyList = [
    "AR", "BA", "SQSS", "SQCC"
]
company.set(companyList[0])
companyRbuttons = []
companyRbuttonsFrame = Frame(inputsFrame, bg='#a5e8e5')
companyRbuttonsFrame.grid(row=0, column=1, sticky=W)
buttonListIndex = 0
for text in companyList:
    companyRbuttons.append(Radiobutton(
        companyRbuttonsFrame, text=text, variable=company, value=text, bg='#a5e8e5'))
    companyRbuttons[buttonListIndex].grid(
        row=0, column=buttonListIndex, sticky=W, padx=3)
    buttonListIndex += 1
# SQCC division
div = StringVar()
divLabel = Label(inputsFrame, text="Division: ", pady=7, bg='#a5e8e5')
divLabel.grid(row=1, column=0, sticky=E)
divList = [
    "WH", "FS", "IT", "ST", "TY"
]
div.set(None)
divRbuttons = []
divRbuttonsFrame = Frame(inputsFrame, bg='#a5e8e5')
divRbuttonsFrame.grid(row=1, column=1, sticky=W)
buttonListIndex = 0
for text in divList:
    divRbuttons.append(Radiobutton(
        divRbuttonsFrame, text=text, variable=div, value=text, bg='#a5e8e5'))
    divRbuttons[buttonListIndex].grid(
        row=1, column=buttonListIndex, sticky=W, padx=3)
    buttonListIndex += 1
# TT Code
ttNum = StringVar()
ttNumLabel = Label(inputsFrame, text="TT Code: ", bg='#a5e8e5')
ttNumLabel.grid(row=2, column=0, sticky=E)
ttNumEntry = Entry(inputsFrame, textvariable=ttNum, width=50)
ttNumEntry.grid(row=2, column=1, pady=3)
# Amount
amount = StringVar()
amountLabel = Label(inputsFrame, text="Amount in SR: ", bg='#a5e8e5')
amountLabel.grid(row=3, column=0, sticky=E)
amountEntry = Entry(inputsFrame, textvariable=amount, width=50)
amountEntry.grid(row=3, column=1, pady=3)
# Payment type
paymentType = StringVar()
paymentTypeLabel = Label(inputsFrame, text="Payment type: ", pady=7, bg='#a5e8e5')
paymentTypeLabel.grid(row=4, column=0, sticky=E)
paymentTypeList = [
    "Outgoing", "Incoming"
]
paymentType.set(paymentTypeList[0])
paymentTypeRbuttons = []
paymentTypeRbuttonsFrame = Frame(inputsFrame, bg='#a5e8e5')
paymentTypeRbuttonsFrame.grid(row=4, column=1, sticky=W)
buttonListIndex = 0
for text in paymentTypeList:
    paymentTypeRbuttons.append(Radiobutton(
        paymentTypeRbuttonsFrame, text=text, variable=paymentType, value=text, bg='#a5e8e5'))
    paymentTypeRbuttons[buttonListIndex].grid(
        row=4, column=buttonListIndex, sticky=W, padx=3)
    buttonListIndex += 1
# JV no.
jvNum = StringVar()
jvNumLabel = Label(inputsFrame, text="JV No.: ", bg='#a5e8e5')
jvNumLabel.grid(row=5, column=0, sticky=E)
jvNumEntry = Entry(inputsFrame, textvariable=jvNum, width=50)
jvNumEntry.grid(row=5, column=1, pady=3)
# Transactee
transactee = StringVar()
transacteeLabel = Label(inputsFrame, text="Vendor/Customer: ", bg='#a5e8e5')
transacteeLabel.grid(row=6, column=0, sticky=E)
transacteeEntry = Entry(inputsFrame, textvariable=transactee, width=50)
transacteeEntry.grid(row=6, column=1, pady=3)
# Client doc
clientDoc = StringVar()
clientDocLabel = Label(inputsFrame, text="Client doc.: ", pady=7, bg='#a5e8e5')
clientDocLabel.grid(row=7, column=0, sticky=E)
clientDocList = [
    "Inv", "PO", "Qtn", "Ac"
]
clientDoc.set(clientDocList[0])
clientDocRbuttons = []
clientDocRbuttonsFrame = Frame(inputsFrame, bg='#a5e8e5')
clientDocRbuttonsFrame.grid(row=7, column=1, sticky=W)
buttonListIndex = 0
for text in clientDocList:
    clientDocRbuttons.append(Radiobutton(
        clientDocRbuttonsFrame, text=text, variable=clientDoc, value=text, bg='#a5e8e5'))
    clientDocRbuttons[buttonListIndex].grid(
        row=7, column=buttonListIndex, sticky=W, padx=3)
    buttonListIndex += 1
# Client doc code
clientDocCode = StringVar()
clientDocCodeLabel = Label(inputsFrame, text="Client doc. no.: ", bg='#a5e8e5')
clientDocCodeLabel.grid(row=8, column=0, sticky=E)
clientDocCodeEntry = Entry(inputsFrame, textvariable=clientDocCode, width=50)
clientDocCodeEntry.grid(row=8, column=1, pady=3)
# Our doc
ourDoc = StringVar()
ourDocLabel = Label(inputsFrame, text="Our doc.: ", pady=7, bg='#a5e8e5')
ourDocLabel.grid(row=9, column=0, sticky=E)
ourDocList = [
    "PO", "RFQ", "SO", "Srv"
]
ourDoc.set(ourDocList[0])
ourDocRbuttons = []
ourDocRbuttonsFrame = Frame(inputsFrame, bg='#a5e8e5')
ourDocRbuttonsFrame.grid(row=9, column=1, sticky=W)
buttonListIndex = 0
for text in ourDocList:
    ourDocRbuttons.append(Radiobutton(
        ourDocRbuttonsFrame, text=text, variable=ourDoc, value=text, bg='#a5e8e5'))
    ourDocRbuttons[buttonListIndex].grid(
        row=9, column=buttonListIndex, sticky=W, padx=3)
    buttonListIndex += 1
# Our doc code
ourDocCode = StringVar()
ourDocCodeLabel = Label(inputsFrame, text="Our doc. no.: ", bg='#a5e8e5')
ourDocCodeLabel.grid(row=10, column=0, sticky=E)
ourDocCodeEntry = Entry(inputsFrame, textvariable=ourDocCode, width=50)
ourDocCodeEntry.grid(row=10, column=1, pady=3)
# Foreign currency
foreignCur = StringVar()
foreignCurLabel = Label(inputsFrame, text="Foreign Currency: ", pady=7, bg='#a5e8e5')
foreignCurLabel.grid(row=11, column=0, sticky=E)
foreignCurList = [
    "SR" ,"USD", "GBP", "AED", "INR", "Other"
]
foreignCur.set(foreignCurList[0])
foreignCurRbuttons = []
foreignCurRbuttonsFrame = Frame(inputsFrame, bg='#a5e8e5')
foreignCurRbuttonsFrame.grid(row=11, column=1, sticky=W)
buttonListIndex = 0
for text in foreignCurList:
    foreignCurRbuttons.append(Radiobutton(
        foreignCurRbuttonsFrame, text=text, variable=foreignCur, value=text, bg='#a5e8e5'))
    foreignCurRbuttons[buttonListIndex].grid(
        row=11, column=buttonListIndex, sticky=W, padx=3)
    buttonListIndex += 1
# Other cur
otherCur = StringVar()
otherCurLabel = Label(inputsFrame, text="If other, specify: ", bg='#a5e8e5')
otherCurLabel.grid(row=12, column=0, sticky=E)
otherCurEntry = Entry(inputsFrame, textvariable=otherCur, width=50)
otherCurEntry.grid(row=12, column=1, pady=3)
# Foreign amount
foreignAmount = StringVar()
foreignAmountLabel = Label(inputsFrame, text="Foreign Amount: ", bg='#a5e8e5')
foreignAmountLabel.grid(row=13, column=0, sticky=E)
foreignAmountEntry = Entry(inputsFrame, textvariable=foreignAmount, width=50)
foreignAmountEntry.grid(row=13, column=1, pady=3)
# Frex
frex = StringVar()
frexLabel = Label(inputsFrame, text="Frex: ", bg='#a5e8e5')
frexLabel.grid(row=14, column=0, sticky=E)
frexEntry = Entry(inputsFrame, textvariable=frex, width=50)
frexEntry.grid(row=14, column=1, pady=3)
# Purpose
purpose = StringVar()
purposeLabel = Label(inputsFrame, text="Purpose: ", bg='#a5e8e5')
purposeLabel.grid(row=15, column=0, sticky=E)
purposeEntry = Entry(inputsFrame, textvariable=purpose, width=50)
purposeEntry.grid(row=15, column=1, pady=3)
# Date
date = StringVar()
dateLabel = Label(inputsFrame, text="Date (DD-MM-YYYY): ", bg='#a5e8e5')
dateLabel.grid(row=16, column=0, sticky=E)
dateEntry = Entry(inputsFrame, textvariable=date, width=50)
dateEntry.grid(row=16, column=1, pady=3)
# Execution button
copyButton = Button(
    inputsFrame, text="Generate and copy to clipboard", command=onCopyClick, bg='white')
copyButton.grid(row=17, column=0, pady=10)
# Result indicator
outputLabel = Label(inputsFrame, text="", pady=10, bg='#a5e8e5')
outputLabel.grid(row=17, column=1)
# Reset button
resetButton = Button(inputsFrame, text="Reset fields",
                     command=onResetClick, bg='white')
resetButton.grid(row=18, column=1, pady=5)
# Reset indicator
resetLabel = Label(inputsFrame, text="", pady=5, bg='#a5e8e5')
resetLabel.grid(row=18, column=0)
# Output display
outputDisplayLabel = Label(mainFrame, text = "File name: ", bg = '#a5e8e5')
outputDisplayLabel.grid(row = 1, column = 0, sticky = W, padx=56)
outputDisplayText = Text(mainFrame, height = 3, width = 50)
outputDisplayText.grid(row = 2, column = 0)
# Cursor focus
ttNumEntry.focus_set()

win.mainloop()