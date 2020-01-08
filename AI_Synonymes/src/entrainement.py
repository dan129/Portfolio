# -*- coding: utf-8 -*-
import re
import connexion

class Entrainement:
	def __init__(self, taille, encodage, listeChemins):
		sousFenetre = taille // 2
		connexionBD = connexion.Connexion()

		print('Chargement des données de la base de données...')
		connexionBD.ouvrirConnexion()
		dictBD = connexionBD.telechargementDictionnaire()
		coocBD = connexionBD.telechargementCoocurrences(taille)

		print('Lecture du texte et traitement des données...')
		for chemin in listeChemins:
			listeNouveauxMots, texteEnMots = self.lectureDuTexte(chemin, encodage, dictBD)
		dictNouvellesCooc = self.remplirCoocurences(texteEnMots, dictBD, sousFenetre)

		print('Sauvegarde des données dans la base de données...')
		connexionBD.remplirDictionnaire(listeNouveauxMots)
		connexionBD.updateBD(coocBD, dictNouvellesCooc, taille)
		connexionBD.fermerConnexion()

		print('Sauvegarde terminée.')

	def lectureDuTexte(self, chemin, encodage, dictBD):
		# Lire les textes
		fichier = open(chemin, 'r', encoding = encodage)
		texte = fichier.read()
		fichier.close()
		texte = texte.lower()

		# Ajouter les mots dans le dictonnaire
		texteEnMots = re.findall('\w+', texte)
		listeNouveauxMots = []
		
		for mot in texteEnMots:
			if mot not in dictBD:
				listeNouveauxMots.append((len(dictBD), mot))
				dictBD[mot] = len(dictBD)
		
		return listeNouveauxMots, texteEnMots

	def remplirCoocurences(self, texteEnMots, dictBD, sousFenetre):
		dictNouvellesCooc = {}
		
		for i in range(len(texteEnMots)):
			idMot = dictBD[texteEnMots[i]]

			for j in range(1, sousFenetre + 1):
				if i - j >= 0:
					idCoocurrence = dictBD[texteEnMots[i - j]]

					if (idMot, idCoocurrence) not in dictNouvellesCooc:
						dictNouvellesCooc[(idMot, idCoocurrence)] = 1
					else:
						dictNouvellesCooc[(idMot, idCoocurrence)] += 1

				if i + j < len(texteEnMots):
					idCoocurrence = dictBD[texteEnMots[i + j]]

					if (idMot, idCoocurrence) not in dictNouvellesCooc:
						dictNouvellesCooc[(idMot, idCoocurrence)] = 1
					else:
						dictNouvellesCooc[(idMot, idCoocurrence)] += 1
		
		return dictNouvellesCooc

if __name__ == '__main__':
	print('Dans Entraînement')