import shared.up

# excluded:
# ASIANetwork Exchange: back-issues bundled as single files does strange things to stats
# Journal of Embodied Research: no articles yet. Video journal.
# Le foucaldien: only launched in September
# Pynchon Notes: An archived journal
# Digital Medievalist: only launched in September

olh_journals = ['https://olh.openlibhums.org/jms/index.php/up/oai/',
                'https://www.pynchon.net/jms/index.php/up/oai/',
                'https://19.bbk.ac.uk/jms/index.php/up/oai/',
                'http://journal.eahn.org/jms/index.php/up/oai/',
                'http://c21.openlibhums.org/jms/index.php/up/oai/',
                'http://www.comicsgrid.com/jms/index.php/up/oai/',
                'http://www.glossa-journal.org/jms/index.php/up/oai/',
                'http://poetry.openlibhums.org/jms/index.php/up/oai/',
                'https://jpl.letras.ulisboa.pt/jms/index.php/up/oai/',
                'http://www.journal-labphon.org/jms/index.php/up/oai/',
                'http://marvell.openlibhums.org/jms/index.php/up/oai/',
                'http://www.mamsie.bbk.ac.uk/jms/index.php/up/oai/',
                'http://www.asianetworkexchange.org/jms/index.php/up/oai/',
                'https://journal.digitalmedievalist.org/jms/index.php/up/oai/',
                'https://foucaldien.net/jms/index.php/up/oai/',
                'https://pynchonnotes.openlibhums.org/jms/index.php/up/oai/']

def main():
    for journal in olh_journals:
        jrnl = shared.up.parse_OAI(journal)
        print('{0}: {1}. Average: {2}'.format(journal, jrnl, str(sum(jrnl)/len(jrnl))))

if __name__ == "__main__":
    main()