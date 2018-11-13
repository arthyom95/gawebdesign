import sys
from random import randint
import random
from operator import itemgetter
def generatePopulation(populationSize, preBodyText, bodyText, populationGenotypeMatrix):
	if(len(populationGenotypeMatrix) == 0):		
		populationGenotypeMatrix = generateInitialGenotypeMatrix(populationSize)
	
	for i in range(1,populationSize):	
		numberString = str(i)		
		f = open(numberString + ".html", 'w')	
		
		#number of rows, columns per row, boostrap breakpoint, title size, subtitle size, size of margin, individual fitness
		genotypeArray = populationGenotypeMatrix[i-1]		
		message = generatePageFromGenotype(genotypeArray, preBodyText, bodyText, numberString)
		f.write(message)
		
		print("Page "+numberString+" generated.")	
		f.close()	
	return populationGenotypeMatrix

def generateInitialGenotypeMatrix(populationSize):
	w, h = 7, populationSize;	
	populationGenotypeMatrix = [[0 for x in range(w)] for y in range(h)]
	
	for i in range(1,populationSize):
		bootstrapColumns = [1,2,3,4,6,12]
		#number of rows, columns per row, boostrap breakpoint, title size, subtitle size, size of margin, individual fitness
		genotypeArray = [randint(1,9),bootstrapColumns[randint(0,5)], randint(1,4), str(randint(1,3)), str(randint(4,6)), str(randint(0,200)), 0]
		populationGenotypeMatrix[i-1] = genotypeArray
	
	return populationGenotypeMatrix
	
def generatePageFromGenotype(genotypeArray, preBodyText, bodyText, pageNumber):
		
	noOfRows = genotypeArray[0]
	columnsPerRow = genotypeArray[1]
	boostrapBreakpoint = genotypeArray[2]
	titleSize = genotypeArray[3]
	subTitleSize = genotypeArray[4]
	sizeOfMargin = genotypeArray[5]
	
	if boostrapBreakpoint == 1:
		breakpoint = "sm"
	elif boostrapBreakpoint == 2:
		breakpoint = "md"
	elif boostrapBreakpoint == 3:
		breakpoint = "lg"
	elif boostrapBreakpoint == 4:
		breakpoint = "xl"
		
	page = preBodyText
	page = page + """
			<body style ="margin:"""+sizeOfMargin+"""px">
				<div class="container">			
					<main role="main">
						<div style ="padding:1rem 2rem" class="jumbotron">
							<h"""+titleSize+""" class="display-3">GA Web Design page """+pageNumber+"""</h"""+titleSize+""">
							<p class="lead">"""+bodyText+"""</p>					
						</div>
	"""				
	
	if breakpoint == "":
		fullCol = "\"col-" + str(int(12/columnsPerRow)) + "\""
	else:
		fullCol = "\"col-" + breakpoint+"-" + str(int(12/columnsPerRow)) + "\""	
		
	column = """
				<div class="""+fullCol+"""">
					<h"""+subTitleSize+""">Subheading</h"""+subTitleSize+""">
					<p class="lead">"""+bodyText+	"""</p>					
				</div>
			 """
	
	for i in range(0, noOfRows):
		page = page + """
			<div class="row marketing">
		"""
		for j in range(0, columnsPerRow):
			page = page + column
		page = page + """
			</div>
		"""	
			
	page = page + """
					</main>
				</div>
			</body>
		</html>
	"""	
	return page
	
def crossoverGenotype(genotypeArray1, genotypeArray2, crossoverRate):
	for i in range(0, len(genotypeArray1) - 1):
		if random.uniform(0.0, 1.0) < crossoverRate/10:
			temp = genotypeArray1[i]
			genotypeArray1[i] = genotypeArray2[i]
			genotypeArray2[i] = temp
			
def mutateGenotypeArray(genotypeArray, mutationChance):
	for i in range(0, len(genotypeArray) - 1):
		if random.uniform(0.0, 1.0) < mutationChance/10:
			genotypeArray[i] = generateNewGeneValue(i);
	return genotypeArray				
	
def generateNewGeneValue(geneIndex):
	geneValue = None
	if geneIndex == 0:
		geneValue = randint(1,9)
	elif geneIndex == 1:
		bootstrapColumns = [1,2,3,4,6,12]
		geneValue = bootstrapColumns[randint(0,5)]
	elif geneIndex == 2:
		geneValue = randint(1,5)
	elif geneIndex == 3:
		geneValue = str(randint(1,6))
	elif geneIndex == 4:
		geneValue = str(randint(1,6))
	elif geneIndex == 5:
		geneValue = str(randint(0,200))
		
	return geneValue
	
def evolve(genotypeMatrix, preBodyText, bodyText, offspring):	
	sorted(genotypeMatrix, key=itemgetter(6))
	for i in range (0, offspring):
		crossoverGenotype(genotypeMatrix[i], genotypeMatrix[i+1], 5)
			
	for i in range(0, len(genotypeMatrix)):
		genotypeMatrix[i] = mutateGenotypeArray(genotypeMatrix[i], 1)
	
	genotypeMatrix = generatePopulation(len(genotypeMatrix), preBodyText, bodyText, genotypeMatrix)
	return genotypeMatrix

HEAD ="""
	<head>
		<meta charset="utf-8">
		<meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
		<link rel="stylesheet" href="css/bootstrap.min.css" >	
		<script src="js/jquery-3.2.1.min.js"></script>
		<script src="js/popper.js"></script>
		<script src="js/bootstrap.min.js"></script>
	</head>
"""	
PREBODYTEXT = """ <!doctype html><html>""" + HEAD

LOREMIPSUM = """Lorem ipsum dolor sit amet, consectetur adipiscing elit. Pellentesque lobortis odio ut odio fringilla, ac fermentum diam vehicula. Vestibulum efficitur elit accumsan sapien hendrerit, et porttitor ante interdum. Etiam euismod rhoncus porta. Etiam ac nisi nec sem sollicitudin lacinia."""

######
#MAIN#
######
if len(sys.argv) == 3:
	try:
		populationsize = int(sys.argv[1])
		generationsNo = int(sys.argv[2])
	except ValueError:
		print ("Usage: " + sys.argv[0] + " <size of initial population><number of generations>")
		print ("<size of initial population> - must be an integer")
		print ("<number of generations> - must be an integer")
		sys.exit (1)
elif len(sys.argv) == 1:
	populationsize = 5
	generationsNo = 3
elif len(sys.argv) > 3:
	print ("Usage: " + sys.argv[0] + " <size of initial population><number of generations>")
	sys.exit(1)
	
populationGenotypeMatrix = []
populationGenotypeMatrix = generatePopulation(populationsize + 1,PREBODYTEXT,LOREMIPSUM, populationGenotypeMatrix)
input("Initial population generated. Press Enter to continue...")

generation = 1
while generation < generationsNo:
	for i in range(1,populationsize + 1):
		numberString = str(i)
		rating = input("Please assign a rating between 1 and 5 for web page "+numberString+".html ")
		while not rating in ('1', '2', '3', '4', '5'):
			rating = input("Please assign a rating between 1 and 5 for web page "+numberString+".html ")
		populationGenotypeMatrix[i-1][6] = int(rating)
		print(populationGenotypeMatrix[i-1])

	populationGenotypeMatrix = evolve(populationGenotypeMatrix, PREBODYTEXT, LOREMIPSUM, 2)
	input("New population generated! ")	
	generation = generation + 1
	
print("Specified number of generations"+str(generationsNo)+" evolved. Exiting...")
sys.exit(0)
		