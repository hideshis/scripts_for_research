from xml.etree import ElementTree

XMLFILE = 'df_httpclient5-5.0-alpha2-SNAPSHOT.xml'

tree = ElementTree.parse(XMLFILE)
root = tree.getroot()
print root.tag
