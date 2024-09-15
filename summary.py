from pypdf import PdfReader
from openai import OpenAI

# open ai stuff
key = ""
client = OpenAI(api_key=key)

reader = PdfReader("Discrete Mathematics and Its Applications.pdf")
# number_of_pages = len(reader.pages)
# page = reader.pages[0]
# text = page.extract_text()

tableEnd = 0
tableStart = 0 
tableStart = int(input("Enter the page the page that the Table of Contents starts at: ")) - 1
tableEnd = int(input("Enter the page the page that the Table of Contents ends at: ")) - 1

textBuffer = ""

for i in range(tableStart, tableEnd + 1):
  page = reader.pages[i]
  text = page.extract_text()
  textBuffer += text + '[ENDOFPAGE]'


test = '''
"The Foundations: Logic and Proofs"[SPLIT]1
"Basic Structures: Sets, Functions, Sequences, Sums, and Matrices"[SPLIT]121
"Algorithms"[SPLIT]201
"Number Theory and Cryptography"[SPLIT]251
"Induction and Recursion"[SPLIT]331
"Counting"[SPLIT]405
"Discrete Probability"[SPLIT]469
"Advanced Counting Techniques"[SPLIT]527
"Relations"[SPLIT]599
'''


tablePrompt = '''You are provided with a string containing the text of a textbook, which includes a table of contents. Pages in the string are delimited by the token '[ENDOFPAGE]'. Your task is to extract each chapter title along with its starting page number, and return them as a list of strings. Each string should follow this format:

"<Chapter Title>"[SPLIT]<Starting Page Number>\n

Ensure that you exclude the chapter number and return only the list of strings in the specified format.

Text:'''


def parseTableOfContents():
  completion = client.chat.completions.create(
  model="gpt-4o-mini",
  messages=[
    {"role": "system", "content": tablePrompt},
    {"role": "user", "content": textBuffer},
  ]
  )
  #print(completion.choices[0].message.content)
  formatChapters(completion.choices[0].message.content)

# After formatting the chapters are in a 2d arr [["chapter",pageNum]...]
chaptersArr = []
def formatChapters(chapters):
  chapters = chapters.split("\n")
  for item in chapters:
     if len(item.split("[SPLIT]")) == 2:  
            chapterTitle = item.split("[SPLIT]")[0].strip().strip('"').strip("'")
            pageNum = item.split("[SPLIT]")[1].strip().strip('"')    
            chaptersArr.append([chapterTitle, pageNum])
  # add if statement to check if its chill to index the next page bc it might not be bc theres no more ch
  getChaperInfo(chaptersArr[0][0],chaptersArr[0][1], chaptersArr[1][1])



def getChaperInfo(Title, chStart, chEnd):
  # print("!!!!",Title,chStart,chEnd)
  chapterStart = int(chStart.replace(",","")) - 1
  chapterEnd = int(chEnd.replace(",",""))
  textBuffer = ""

  for i in range(chapterStart, chapterEnd):
    page = reader.pages[i]
    text = page.extract_text()
    textBuffer += text
  getImportantSentences(textBuffer)

chapterSummaryPrompt = """You are tasked with summarizing a specific chapter and its subsections from a textbook. The summary should serve as a refresher for someone who has already read the material. Return only a list of concise yet content-packed strings that highlight the most important ideas and key concepts from the chapter. Focus on:

Key equations, formulas, or algorithms.
Major theories, theorems, or principles.
Fundamental concepts crucial for intuitive understanding of the subject.
Definitions of essential terms.
Significant examples, reactions, or applications that reinforce understanding.
Each string should be dense with information, clearly conveying core ideas, theories, or formulas. Ensure the concepts are succinctly described while containing enough detail to capture the essence of the material. Only return a list of strings, without any additional explanation or formatting."""


def getImportantSentences(chaperText):
  completion = client.chat.completions.create(
  model="gpt-4o-mini",
  messages=[
    {"role": "system", "content": chapterSummaryPrompt},
    {"role": "user", "content": chaperText},
  ]
  )
  print(completion.choices[0].message.content)

parseTableOfContents()