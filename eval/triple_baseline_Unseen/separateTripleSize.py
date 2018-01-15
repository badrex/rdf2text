import xml.etree.ElementTree as Et
import xml.etree.cElementTree as ET
import sys
import getopt



def separateUnseen(filePath,size):
    """
    this function separate unseen dataset according to triple size
    :param filePath: the directory for unseen dataset file
    :param size: the current size of triple we want to separate from unseen dataset 
    return
    """
    context = ET.iterparse(filePath, events=('end', ))
    # create xml file to put extracted triples in it
    filename = format("unseenTriple"+size+".xml")
    with open(filename, 'wb') as f:
        f.write(b"<benchmark>\n")
        f.write(b" <entries>\n")
        for event, elem in context:
           if elem.tag == 'entry':
               tsize = elem.get('size')
               if tsize==size:
                   f.write(ET.tostring(elem))
        f.write(b" </entries>\n")
        f.write(b"</benchmark>\n")


def main(argv):
    usage = 'usage:\npython3 separateTripleSize.py -i <data-directory> -s size' \
           '\ndata-directory is the directory where the whole xml of unseen dataset is'\
      '\n size, the size of triple' 
    try:
        opts, args = getopt.getopt(argv, 'i:s:', ['inputdir=', 'size='])
    except getopt.GetoptError:
        print(usage)
        sys.exit(2)
    input_data = False
    for opt, arg in opts:
        if opt in ('-i', '--inputdir'):
            inputdir= arg
            input_data = True
        elif opt in ('-s', '--size'):
            size=arg
            input_data = True
        else:
            print(usage)
            sys.exit()
    if not input_data:
        print(usage)
        sys.exit(2)
    print('Input directory is', inputdir)
    print('The cuurent size of triple is', size)
    separateUnseen(inputdir,size)

if __name__ == "__main__":
    main(sys.argv[1:])
