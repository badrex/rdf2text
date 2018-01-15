import xml.etree.ElementTree as Et
import xml.etree.cElementTree as ET
import sys
import getopt


def separateUnseen(filePath,catgory):
    """
    this function separate unseen dataset according to category name
    :param filePath: the directory for unseen dataset file
    :param catgory: the current name of catgory we want to separate unseen dataset according to
    return
    """
    context = ET.iterparse(filePath, events=('end', ))
    # create xml file to put extracted triples in it
    filename = format("unseen"+catgory+".xml")
    with open(filename, 'wb') as f:
        f.write(b"<benchmark>\n")
        f.write(b" <entries>\n")
        for event, elem in context:
           if elem.tag == 'entry':
               cg = elem.get('category')
               if cg==catgory:
                   f.write(ET.tostring(elem))
        f.write(b" </entries>\n")
        f.write(b"</benchmark>\n")


def main(argv):
    usage = 'usage:\npython3 separateCategory.py -i <data-directory> -c category' \
           '\ndata-directory is the directory where the whole xml of unseen dataset is'\
      '\n category, the name of category' 
    try:
        opts, args = getopt.getopt(argv, 'i:c:', ['inputdir=', 'category='])
    except getopt.GetoptError:
        print(usage)
        sys.exit(2)
    input_data = False
    for opt, arg in opts:
        if opt in ('-i', '--inputdir'):
            inputdir= arg
            input_data = True
        elif opt in ('-c', '--category'):
            catg=arg
            input_data = True
        else:
            print(usage)
            sys.exit()
    if not input_data:
        print(usage)
        sys.exit(2)
    print('Input directory is', inputdir)
    print('The cuurent name of category is', catg)
    separateUnseen(inputdir,catg)

if __name__ == "__main__":
    main(sys.argv[1:])
