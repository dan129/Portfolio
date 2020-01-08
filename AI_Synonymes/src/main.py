# -*- coding: utf-8 -*-
import sys
import entrainement
import recherche
import clustering
import traceback
import knn

def main():
    try:
        nbArgv = len(sys.argv)
        
        for arg in sys.argv:
            # Entrainement
            if arg == '-e':
                if nbArgv < 8:
                    raise Exception('Message d\'erreur: nombre d\'arguments incorrect.')

                taille = None
                encodage = None
                chemins = None

                for i in range(nbArgv):
                    if sys.argv[i] == '-t':
                        taille = sys.argv[i + 1]
                    elif sys.argv[i] == '--enc':
                        encodage = sys.argv[i + 1]
                    elif sys.argv[i] == '--chemin':
                        chemins = []
                        compteur = 1
                        
                        while i + compteur < nbArgv and sys.argv[i + compteur][0] != "-":
                            chemins.append(sys.argv[i + compteur])
                            compteur += 1
                            
                if taille is None or encodage is None or chemins is None:
                    raise Exception('Message d\'erreur: il manque des arguments pour effectuer l\'enregistrement.')

                entrainement.Entrainement(int(taille), encodage, chemins)

                return 0

            # Recherche
            elif arg == '-r':
                if nbArgv != 4:
                    raise Exception('Message d\'erreur: nombre d\'arguments incorrect.')

                taille = None

                for i in range(nbArgv):
                    if sys.argv[i] == '-t':
                        taille = sys.argv[i + 1]

                if taille is None:
                    raise Exception('Message d\'erreur: il manque des arguments pour effectuer la recherche.')

                recherche.Recherche(int(taille))

                return 0
            
            # Clustering
            elif arg == '-c':
                if nbArgv < 8:
                    raise Exception('Message d\'erreur: nombre d\'arguments incorrect.')

                taille = None
                nbResultats = None
                nbCentroides = None
                mots = None
                chemin = None

                for i in range(len(sys.argv)):
                    if sys.argv[i] == '-t':
                        taille = int(sys.argv[i + 1])
                    elif sys.argv[i] == '-n':
                        nbResultats = int(sys.argv[i + 1])
                    elif sys.argv[i] == '--nc':
                        nbCentroides = int(sys.argv[i + 1])
                    elif sys.argv[i] == '--mots':
                        mots = []
                        compteur = 1
                        
                        while i + compteur < nbArgv and sys.argv[i + compteur][0] != "-":
                            mots.append(sys.argv[i + compteur])
                            compteur += 1
                            
                        mots[0] = mots[0][1:]
                        mots[-1] = mots[-1][:-1]
                    elif sys.argv[i] == '>':
                        chemin = sys.argv[i + 1]

                if taille is None or nbResultats is None or (nbCentroides is None and  mots is None):
                    raise Exception('Message d\'erreur: il manque des arguments pour effectuer l\'enregistrement.')
                elif nbCentroides is not None and mots is not None:
                    raise Exception('Message d\'erreur: seul un type de centroide peut être testé à la fois.')

                clustering.Clustering(taille, nbResultats, nbCentroides, mots, chemin)

                return 0
            
            # KNN
            # -knn = Indique que l'on veut appliquer le KNN.
            # -t = Taille de la fenêtre.
            # -k = Nombre de mots au tour pris en compte.
            # --mots = Mots sur les quels on désire un résultat.
            # Example:
            # -knn -t5 -k 5 --mots 'Banane Maison Manger'
            elif arg == '-knn':
                if nbArgv < 10:
                    raise Exception('Message d\'erreur: nombre d\'arguments incorrect.')

                taille = None
                encodage = None
                kMots = None
                mots = None

                for i in range(len(sys.argv)):
                    if sys.argv[i] == '-t':
                        taille = int(sys.argv[i + 1])
                    elif sys.argv[i] == '-k':
                        kMots = int(sys.argv[i + 1])
                    elif sys.argv[i] == '--enc':
                        encodage = sys.argv[i + 1]
                    elif sys.argv[i] == '--mots':
                        mots = []
                        compteur = 1
                        
                        while i + compteur < nbArgv and sys.argv[i + compteur][0] != "-":
                            mots.append(sys.argv[i + compteur])
                            compteur += 1
                            
                        mots[0] = mots[0][1:]
                        mots[-1] = mots[-1][:-1]

                if taille is None or kMots is None or encodage is None or mots is None:
                    raise Exception('Message d\'erreur: il manque des arguments pour effectuer KNN.')

                knn.KNN(taille, kMots, encodage, mots)

                return 0

        raise Exception('Message d\'erreur: aucun argument pour l\'entrainement ou la recherche.')
    
    except Exception as e:
        print(traceback.format_exc())
        return 1

if __name__ == '__main__':
    sys.exit(main())