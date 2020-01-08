# -*- coding: utf-8 -*-
import numpy as np
import operator

class AnalyseVectorielle():
    def __init__(self):
        self.listeStopWords = ['a', 'à', 'â', 'abord', 'afin', 'ah', 'ai', 'aie', 'ainsi', 'allaient', 'allo', 'allô', 'allons', 'alors', 'après', 'assez', 'attendu', 'au', 'aucun', 'aucune', 'aucuns', 'aujourd', 'aujourd\'hui', 'auquel', 'aura', 'auront', 'aussi', 'autre', 'autres', 'aux', 'auxquelles', 'auxquels', 'avaient', 'avais', 'avait', 'avant', 'avec', 'avoir', 'ayant', 'b', 'bah', 'beaucoup', 'bien', 'bigre', 'bon', 'boum', 'bravo', 'brrr', 'c', 'ça', 'car', 'ce', 'ceci', 'cela', 'celle', 'celle-ci', 'celle-là', 'celles', 'celles-ci', 'celles-là', 'celui', 'celui-ci', 'celui-là', 'cent', 'cependant', 'certain', 'certaine', 'certaines', 'certains', 'certes', 'ces', 'cet', 'cette', 'ceux', 'ceux-ci', 'ceux-là', 'chacun', 'chaque', 'cher', 'chère', 'chères', 'chers', 'chez', 'chiche', 'chut', 'ci', 'cinq', 'cinquantaine', 'cinquante', 'cinquantième', 'cinquième', 'clac', 'clic', 'combien', 'comme', 'comment', 'compris', 'concernant', 'contre', 'couic', 'crac', 'd', 'da', 'dans', 'de', 'debout', 'début', 'dedans', 'dehors', 'delà', 'depuis', 'derrière', 'des', 'dès', 'désormais', 'desquelles', 'desquels', 'dessous', 'dessus', 'deux', 'deuxième', 'deuxièmement', 'devant', 'devers', 'devra', 'devrait', 'différent', 'différente', 'différentes', 'différents', 'dire', 'divers', 'diverse', 'diverses', 'dix', 'dix-huit', 'dixième', 'dix-neuf', 'dix-sept', 'doit', 'doivent', 'donc', 'dont', 'dos', 'douze', 'douzième', 'dring', 'droite', 'du', 'duquel', 'durant', 'e', 'effet', 'eh', 'elle', 'elle-même', 'elles', 'elles-mêmes', 'en', 'encore', 'entre', 'envers', 'environ', 'es', 'ès', 'essai', 'est', 'et', 'étaient', 'étais', 'était', 'etant' 'étant', 'état', 'etc', 'été', 'étions', 'etre', 'être', 'eu', 'euh', 'eux', 'eux-mêmes', 'excepté', 'f', 'façon', 'fais', 'faisaient', 'faisant', 'fait', 'faites', 'feront', 'fi', 'flac', 'floc', 'fois', 'font', 'force', 'g', 'gens', 'h', 'ha', 'haut', 'hé', 'hein', 'hélas', 'hem', 'hep', 'hi', 'ho', 'holà', 'hop', 'hormis', 'hors', 'hou', 'houp', 'hue', 'hui', 'huit', 'huitième', 'hum', 'hurrah', 'i', 'ici', 'il', 'ils', 'importe', 'j', 'je', 'jusqu', 'jusque', 'juste', 'k', 'l', 'la', 'là', 'laquelle', 'las', 'le', 'lequel', 'les', 'lès', 'lesquelles', 'lesquels', 'leur', 'leurs', 'longtemps', 'lorsque', 'lui', 'lui-même', 'm', 'ma', 'maint', 'maintenant', 'mais', 'malgré', 'me', 'même', 'mêmes', 'merci', 'mes', 'mien', 'mienne', 'miennes', 'miens', 'mille', 'mince', 'mine', 'moi', 'moi-même', 'moins', 'mon', 'mot', 'moyennant', 'n', 'na', 'ne', 'néanmoins', 'neuf', 'neuvième', 'ni', 'nombreuses', 'nombreux', 'nommés', 'non', 'nos', 'notre', 'nôtre', 'nôtres', 'nous', 'nous-mêmes', 'nouveaux', 'nul', 'o', 'ô', 'o|', 'oh', 'ohé', 'olé', 'ollé', 'on', 'ont', 'onze', 'onzième', 'ore', 'ou', 'où', 'ouf', 'ouias', 'oust', 'ouste', 'outre', 'p', 'paf', 'pan', 'par', 'parce', 'parmi', 'parole', 'partant', 'particulier', 'particulière', 'particulièrement', 'pas', 'passé', 'pendant', 'personne', 'personnes', 'peu', 'peut', 'peuvent', 'peux', 'pff', 'pfft', 'pfut', 'pièce', 'pif', 'plein', 'plouf', 'plupart', 'plus', 'plusieurs', 'plutôt', 'pouah', 'pour' 'pourquoi', 'premier', 'première', 'premièrement', 'près', 'proche', 'psitt', 'puisque', 'q', 'qu', 'quand', 'quant', 'quanta', 'quant-à-soi', 'quarante', 'quatorze', 'quatre', 'quatre-vingt', 'quatrième', 'quatrièmement', 'que', 'quel', 'quelconque', 'quelle', 'quelles', 'quelque', 'quelques', 'quelqu\'un', 'quels' 'qui', 'quiconque', 'quinze', 'quoi', 'quoique', 'r', 'revoici', 'revoilà', 'rien', 's', 'sa', 'sacrebleu', 'sans', 'sapristi', 'sauf', 'se', 'seize', 'selon', 'sept', 'septième', 'sera', 'seront', 'ses', 'seulement', 'si', 'sien', 'sienne', 'siennes', 'siens', 'sinon', 'six', 'sixième', 'soi', 'soi-même', 'soit', 'soixante', 'son', 'sont', 'sous', 'soyez', 'stop', 'suis', 'suivant', 'sujet', 'sur', 'surtout', 't', 'ta', 'tac', 'tandis', 'tant', 'te', 'té', 'tel', 'telle', 'tellement', 'telles', 'tels', 'tenant', 'tes', 'tic', 'tien', 'tienne', 'tiennes', 'tiens', 'toc', 'toi', 'toi-même', 'ton', 'touchant', 'toujours', 'tous', 'tout', 'toute', 'toutes', 'treize', 'trente', 'très', 'trois', 'troisième', 'troisièmement', 'trop', 'tsoin', 'tsouin', 'tu', 'u', 'un', 'une', 'unes', 'uns', 'v', 'va' 'vais', 'valeur', 'vas', 'vé', 'vers', 'via', 'vif', 'vifs', 'vingt', 'vivat', 'vive' 'vives', 'vlan', 'voici', 'voie', 'voient', 'voilà', 'vont', 'vos', 'votre', 'vôtre', 'vôtres', 'vous', 'vous-mêmes', 'vu', 'w', 'x', 'y', 'z', 'zut']

    def calcul(self, methodeChoisie, dictionnaireMots, dictionnaireCoocurrences, synonyme):
        listeScore = []
        score = 0
        matriceVecteurs = np.zeros((len(dictionnaireMots), len(dictionnaireMots)))

        for coocurencesKeys, frequencee in dictionnaireCoocurrences.items():
            matriceVecteurs[coocurencesKeys[0]][coocurencesKeys[1]] = frequencee

        for mot, index in dictionnaireMots.items():
            if mot not in self.listeStopWords and mot != synonyme:
                vecteurRangeeMot = matriceVecteurs[dictionnaireMots[synonyme]]
                vecteurRangeeIteration = matriceVecteurs[index]

                if methodeChoisie == 0:
                    score=np.dot(vecteurRangeeMot, vecteurRangeeIteration)
                elif methodeChoisie == 1:
                    score=np.sum(np.power(np.subtract(vecteurRangeeMot, vecteurRangeeIteration), 2))
                elif methodeChoisie == 2:
                    score=np.sum(np.absolute(np.subtract(vecteurRangeeMot, vecteurRangeeIteration)))

                listeScore.append((score, mot))

        if methodeChoisie == 0:
            listeScore.sort(key = operator.itemgetter(0), reverse = True)
        elif methodeChoisie == 1 or methodeChoisie == 2:
            listeScore.sort(key = operator.itemgetter(0), reverse = False)

        return listeScore

    def calculCluster(self, dictionnaireMots, matriceVecteurs, centroides, anciensClusters):
        nouveauxClusters = [{} for centroide in centroides]
        changements = 0

        for mot, index in dictionnaireMots.items():
            scores = [np.sum((np.subtract(centroide, matriceVecteurs[index]) ** 2)) for centroide in centroides]
            iCentroide = scores.index(min(scores))
            nouveauxClusters[iCentroide][mot] = matriceVecteurs[index]
            
            if mot not in anciensClusters[iCentroide]:
                changements += 1

        return nouveauxClusters, changements
    
if __name__ == '__main__':
    print('Dans Analyse Vectorielle')
