# Wrote by cloud (http://www.madpowah.org - @madpowah)
import sys
import pandas as pd
import argparse
import requests

class Launcher():

    def __init__(self) -> None: 
        pd.set_option("display.max_rows", None)
        # URL de la liste : https://planet4589.org/space/gcat/tsv/launch/launch.tsv 
        fd = pd.read_csv('launch.tsv',sep='\t', on_bad_lines='skip', encoding_errors='ignore')
        # On filtre pour n'avoir que les tirs orbitaux
        fd = fd.dropna(subset=['Launch_Code'])
        fd = fd[fd['Launch_Code' ].str.contains(r'^O.*')]
        # On supprime les colonnes qui ne vont pas nous servir
        fd = fd.drop(['Variant', 'Ascent_Site', 'Ascent_Pad', 'LTCite', 'Cite', 'Notes', 'Apoflag','Apogee', 'Range', 'RangeFlag', 'Dest', 'Group', 'FlightCode', 'Platform'], axis=1)
        fd['Launch_Date'] = pd.to_datetime(fd['Launch_JD'], origin='julian', unit='D').astype('datetime64[s]')
        fd = fd.drop(['Launch_JD'], axis=1)

        self.vols = fd

    # Lanceurs différents
    def listLauncher(self):
        nbuniq = pd.unique(self.vols['LV_Type'].sort_values())

        return nbuniq

    # Liste des opérateurs / agences
    def listOperators(self):
        nbuniq = pd.unique(self.vols['Agency'].sort_values())

        return nbuniq

    # Liste des échecs
    def filter_fail(self):
        # On check les echecs partiels
        fd1 = self.vols[self.vols['Launch_Code'].str.len() > 2]
        # On check les echecs complets
        fd2 = self.vols[self.vols['Launch_Code'] == 'OF']
        # On concatène les 2 et on trie par date
        fd = pd.concat([fd1, fd2])
        fd = fd.sort_values(by=['Launch_Date'])

        self.vols = fd

    def getLaunch(self):
        return self.vols

    # Retourne les 10 derniers lancements
    def getLast(self, nb):
        self.vols = self.vols.sort_values(by=['Launch_Date'], ascending=True)[len(self.vols)-nb:len(self.vols)]

    # Filtre par operateurs
    def filter_operator(self, listOperator):
        tmp = []
        # On les met en majuscule 
        for o in listOperator:
            tmp.append(o.upper())
        self.vols = self.vols[self.vols['Agency'].isin(tmp)]

    # Filtre par mission
    def filter_mission(self, mission):
        self.vols = self.vols[self.vols['Mission'].str.upper().str.contains(str.upper(mission))]

    # Filtre par lanceur
    def filter_launcher(self, launcher):
        # On met en capitalize() pour respecter le DF
        self.vols = self.vols[self.vols['LV_Type'].str.upper().str.contains(str.upper(launcher))]

    # Filtre par année
    def filter_year(self, listYears):
        self.vols = self.vols[pd.DatetimeIndex(self.vols['Launch_Date']).year.isin(listYears)]


def main():
    parser = argparse.ArgumentParser(description='Search in the launch history')
    parser.add_argument('--update', '-u', action='store_const', const=1,
                    help='Update the launch list')
    parser.add_argument('--last', action='store', type=int,
                    help='Print the n last results according the filters')
    parser.add_argument('--list_launchers', '-ll', action='store_const', const=1,
                    help='Return the list of launchers')
    parser.add_argument('--list_operators', '-lo', action='store_const', const=1,
                    help='Return the list of operators')
    parser.add_argument('--operator', '-o', action='store', nargs='*',
                    help='Filter on a list of operators')
    parser.add_argument('--mission', '-m', action='store', nargs='*',
                    help='Filter on a mission')
    parser.add_argument('--launcher', '-l', action='store', nargs='*',
                    help='Filter on a launcher')
    parser.add_argument('--year', '-y', action='store', nargs='*', type=int,
                    help='Filter on a list of years')
    parser.add_argument('--fail', '-f', action='store_const', const=1,
                    help='Print all failures according to the operator and rocket chosen')

    args = parser.parse_args()

    # Si --update
    if args.update:
        sys.stdout.write('Launcher Database Updating .... ')
        sys.stdout.flush()
        req = requests.get('https://planet4589.org/space/gcat/tsv/launch/launch.tsv', verify=False)
        with open("launch.tsv", 'w') as file:
            file.write(req.text)
            file.close()
            print('OK')
            exit()

    # On crée l'instance de Launcher()
    launch = Launcher()



    # Si filtre sur Agency (--operator)
    if args.operator:
        launch.filter_operator(args.operator)

    # Si filtre sur le lanceur (--launcher)
    if args.launcher:
        launch.filter_launcher(' '.join(args.launcher))

    # Si filtre sur la Mission (--mission)
    if args.mission:
        launch.filter_mission(' '.join(args.mission))

    # Si filtre sur les échecs (--fail)
    if args.fail:
        launch.filter_fail()

    # Si filtre sur les années (--year)
    if args.year:
        launch.filter_year(args.year)

    # Si demande de lister les lanceurs
    if args.list_launchers:
        list = launch.listLauncher()
        print(', '.join(list))
        exit()

    # Si demande de lister les opérateurs
    if args.list_operators:
        list = launch.listOperators()
        print(', '.join(list))
        exit()

    # Si --last on affiche les 10 derniers lancements
    if args.last:
        launch.getLast(args.last)
    
    print(launch.getLaunch().to_string(index=False))
    print('Number of results : ' + str(len(launch.getLaunch())))


if __name__ == '__main__':
    main()
