#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
This module generated the docinfo xml file from a text file 
formatted using asciidoc format.
The resulting file will contain only the following tags:
 - rehistory     => tag for revision history table
 - copyright     => tag that will contain the name of 
                    the copyright's owner and the date of the copyright
 - legalnotice   => tag that will display the legal notice information

Command-line usage: docinfo_generator.py [-h] asciidoc_input_file_name

[NOTE]
This module is normally compatible python 2.6.6 (and later) 
and python 3.2.3 (other versions of python3 not tested but should work).

IMPORTANT: None of the following blocks are mandatory.

Revision history rules for an optimal docinfo generation (revinfo tag)
----------------------------------------------------------------------

To extract the revision history data, 
put it in a comment block (more than 3 "/").

Begin the block with one line only containing ":revinfo:"

Then for each revision history item is like this:

  * a block begins with a "v" followed by the version nbr (only digits and ".")
  * followed by a ","
  * followed optionally by the author's initials or name followed by a ","
  * followed by the date of the modification
  * followed by a ":"
  * Then a bunch of lines for the comments over the remark

*Do NOT put a blank line between the blocks.*

The revision history ends with either:

  * a blank line
  * a comment line (a line beginning by more than 3 "/")
  * a new block header (a line beginning by a ":something:"

Copyright rules for optimal docinfo generation (copyright tag)
--------------------------------------------------------------

To avoid any conflict with the asciidoc format, 
put the copyright in a comment block.

Begin the block with a line beginning with the ":copyright:" tag.
Then write the date followed by comma (",") and the company or author's name.
You can use multiple lines for this block, 
but the best practice is to put all in one line.


Legal notice rules for optimal docinfo generation (legalnotice tag)
-------------------------------------------------------------------

To avoid any conflict with the asciidoc format, 
put the legalnotice block in a comment block.

Begin the block with a line beginning with the ":legalnotice:" tag.
Then write each paragraph that you want beginning them by 
a dot (".") as the very first character of the line.
You can use multiple lines for each paragraph, 
but each new paragraph must begin with a dot.
Don't separate paragraph by a blank line!

Example of correctly interpreted block:
---------------------------------------

//////
:copyright:2013,Joseph HERLANT
:revinfo:
v1.2, Joseph HERLANT, 2013-02-22:
 These are my notes for 1.2 revision
 And a bunch of other informations
v1.1, 2013-01-03:
 this is a test for v1.1
 You will notice that there is no author here...
v1.0.1, Jojo, 2013-01-01: All in one line sample. All comment is on one line!
v1.0, JHE, 2013-01-02:
 Creation
 2nd line of modification remark...
:legalnotice:
.This is the first paragraph
of the legal notice.
. This is the second one!
. The next one
last but not least! :)
//////


After running this script to generate the XML file, generate
the HTML document using: 
`a2x -a docinfo -fxhtml <asciidoc file name>`
Or the PDF document using:
`a2x -a docinfo -fpdf <asciidoc file name>`


[NOTE]
As I am a beginner in python and in the development world,
don't hesitate to send me the errors I could have made
or the optimizations I could do.
If you wish this script to be extended to include stuffs you would need,
don't hesitate to send me also a mail.


'''

import sys, argparse, re
from os import path

__author__     = "Joseph HERLANT"
__copyright__  = "Copyright 2013, Joseph HERLANT"
__credits__    = ["Joseph HERLANT"]
__license__    = "GNU GPL"
__version__    = "1.0.2"
__maintainer__ = "Joseph HERLANT"
__email__      = "herlantj@gmail.com"
__status__     = "Production"
__website__    = "https://github.com/aerostitch/asciidoc-tools"

VERBOSE = 0

class Docinfoitem(object):
    ''' This is an abstract class from what each class used to 
        generate xml groups will inherit.
    '''
    def __init__(self):
        ''' As it is an abstract class, it cannot be implemented directly. '''
        print "This is an abstract class. It has not to be implemented"
        raise
    
    def gen_xml_from_self(self, line_indent = '', ordered_list = []):
        ''' Generates xml structure from current object using: 
            - The top-level object xml tag will have the name of the class
            - Each sub objects xml tag will have the name of a member and its value

        WARNING: This will work only on non complex objects (only str, list of str, or numeric members)
        
        Input parameter:
           - line_indent is either one or more tab, whitespace or alike
           - ordered_list is the list of the elements you want to print in the order you want to.
               This is used in order to validated DTD that are sensitive to the xml tags order
               and for filtering.
        Returns:
            - An xml-formatted string
        '''
        # Cleaning up given indentation
        if not re.match(r"^\s*$", line_indent):
            line_indent = ""

        # Initializing given list if not already done
        if ordered_list == []:
##            print(self.__dict__)
            ordered_list = self.__dict__.keys()
            
        _result = ""
        _result += "\n"+ line_indent +"<"+ self.__class__.__name__ +">"
        for k in ordered_list:
            # For each member of the class, transform it to an xml tag if exists
            if k in self.__dict__.keys():
                if(type( self.__dict__[k] ) == list):
                    for list_item in self.__dict__[k]:
                        _result += "\n"+ line_indent +"\t<"+ k +">"
                        _result += "<![CDATA["+ list_item +"]]></"+ k +">"
                else:
                    _result += "\n"+ line_indent +"\t<"+ k +">"
                    _result += "<![CDATA["+ self.__dict__[k] +"]]></"+ k +">"
            else:
                print("WARNING: given key named \""+ k + "\" does not exists.")
        _result += "\n"+ line_indent +"</"+ self.__class__.__name__ +">"
        return _result
    

class legalnotice(Docinfoitem):
    ''' Subclass containing legal notice data for the legalnotice tag.
    Inherits from Docinfoitem abstract class.
    '''
    def __init__(self):
        ''' Class constructor... Initializing inner variables
        Input parameter: Nothing
        Returns: Nothing
        '''
        # Each item of a simpara is a paragraph in the end
        self.simpara = []


class copyright(Docinfoitem):
    ''' Subclass containing copyright data for the copyright tag.
    Inherits from Docinfoitem abstract class.
    '''
    def __init__(self):
        ''' Class constructor... Initializing inner variables
        Input parameter: Nothing
        Returns: Nothing
        '''
        self.year = "1970"
        self.holder = ""


class revision(Docinfoitem):
    ''' Subclass containing revision data for the revhistory tag.
    Inherits from Docinfoitem abstract class.
    '''
    def __init__(self):
        ''' Class constructor... Initializing inner variables
        Input parameter: Nothing
        Returns: Nothing
        '''
        self.revnumber = "0"
        self.date = "0000-00-00"
        self.authorinitials = ""
        self.revremark = ""


    
class docinfo:
    ''' A class that will handle docinfo data '''
    def __init__(self):
        ''' Class constructor... Initializing inner variables
        Input parameter: Nothing
        Returns: Nothing
        '''
        self.copyright = copyright()
        self.legalnotice = legalnotice()
        self.revhistory = []


    def gen_docinfo_filename(self, text_file_name):
        ''' Generates the output xml file for the docinfo module
        based on the file name
        Input parameter:
            text_file_name: name of the file to use as a base
        Returns:
            The name of the xml file to use with the docinfo norms
        '''
        return path.splitext(text_file_name)[0] + '-docinfo.xml'


    def get_revinfo_block(self, filecontent):
        ''' Extracts the revinfo block from the content of the text
        Input parameter:
            filecontent: Content of the text file in a string
        Returns: Nothing
        '''

        # This is how to find the beginning of the block
        strpattern_start_tag = r'.*^:revinfo:\s*\n'
        # This is how to find the revinfo items as one piece
        str_pattern_block = r'(^[v][0-9\.]+[,][^:]+:[^\n]*(?:\n[^:][^\n]+)*?)+' 
        # This is the end of the block (means a line begining by ///
        # or :something: or one blank line)
        str_pattern_end_of_block = r'\n(?:\:\w+\:|/{3,}|\s*\n)'
        # These 3 blocks form a global pattern
        str_pattern_global = strpattern_start_tag + str_pattern_block
        str_pattern_global += str_pattern_end_of_block
        revinfo = re.compile(str_pattern_global, 
		flags=re.MULTILINE|re.UNICODE|re.IGNORECASE|re.DOTALL)
        if revinfo.match(filecontent, re.MULTILINE) is None:
            if VERBOSE > 0: print("No revInfo tag found")
        else:
            # If pattern matches, process data
            revinfo_data = revinfo.search(filecontent).groups(0)[0]
            self.get_revision_items(revinfo_data)


    def get_revision_items(self, revinfo_block):
        ''' Extracts each revision history item from a revinfo block
        and populate the revhistory self table with the items found
        Input parameter:
            revinfo_block: A revision history block extracted from a file content
        Returns: nothing
        '''

        # First part retrieves the revision items in an array of hashtables
        str_pattern_rev = r"^v(?P<revision>[0-9\.]*)[,](?P<modifier>[^,]+[,])?"\
		r"(?P<daterev>[^\:]*)[:](?P<remarks>.*).*"
        rev = re.compile(str_pattern_rev, flags=re.UNICODE|re.IGNORECASE)
        global_rem = []
        current_rem = {}
        for item in revinfo_block.split('\n'):
            if rev.match(item) is None:
##                print("This is a remark line...")
                current_rem['remarks'] += item + "\n"
            else:
                if 'revision' in current_rem.keys():
                    global_rem.append(current_rem)
                current_rem = rev.search(item).groupdict()
        global_rem.append(current_rem)

        # Second part transforms the array of hash in an array of revision objs
        for remitem in global_rem:
            cur_rev = revision()
            cur_rev.revnumber = remitem['revision'].strip()
            cur_rev.date = remitem['daterev'].strip()
            if remitem['modifier'] is None:
                cur_rev.authorinitials = ""
            else:
                cur_rev.authorinitials = remitem['modifier'].strip().strip(',')
            cur_rev.revremark = remitem['remarks'].strip()
##            print cur_rev.gen_xml_from_self('\t')
            self.revhistory.append(cur_rev)
##        print global_rem


    def get_copyright_content(self, filecontent):
        ''' Extracts the copyright block from the content of the text
        Input parameter:
            filecontent: Content of the text file in a string
        Returns: Nothing
        '''
        # This is how to find the beginning of the block
        strpattern_start_tag = r'.*^:copyright:\s*\n*'
        # This is how to find the data as one piece
        str_pattern_block_content = '(?P<date>[^,]*)[,](?P<holder>.*?)' 
        # This is the end of the block (means a line begining by /// 
	# or :something: or one blank line)
        str_pattern_end_of_block = r'\n(?:\:\w+\:|/{3,}|\s*\n)'
        # These 3 blocks form a global pattern
        str_pattern_global = strpattern_start_tag + str_pattern_block_content
        str_pattern_global += str_pattern_end_of_block
        regexinfo = re.compile(str_pattern_global, 
		flags=re.MULTILINE|re.UNICODE|re.IGNORECASE|re.DOTALL)
        if regexinfo.match(filecontent, re.MULTILINE) is None:
            if VERBOSE > 0: print("No copyright tag found")
        else:
            # If pattern matches, process data
##            print(regexinfo.search(filecontent).groupdict())
            tmp_dict = regexinfo.search(filecontent).groupdict()
            self.copyright.year = tmp_dict['date'].strip()
            self.copyright.holder = tmp_dict['holder'].strip()
            del(tmp_dict)

    def get_legalnotice_content(self, filecontent):
        ''' Extracts the legal notice block from the content of the text
        Input parameter:
            filecontent: Content of the text file in a string
        Returns: Nothing
        '''
        # This is how to find the beginning of the block
        strpattern_start_tag = r'.*^:legalnotice:\s*\n*'
        # This is how to find the data as one piece
        str_pattern_block_content = r'(?P<simparas>^\..*?)' 
        # This is the end of the block (means a line begining by /// 
	# or :something: or one blank line)
        str_pattern_end_of_block = r'\n(?:\:\w+\:|/{3,}|\s*\n)'
        # These 3 blocks form a global pattern
        str_pattern_global = strpattern_start_tag + str_pattern_block_content
        str_pattern_global += str_pattern_end_of_block
        regexinfo = re.compile(str_pattern_global, 
		flags=re.MULTILINE|re.UNICODE|re.IGNORECASE|re.DOTALL)
        if regexinfo.match(filecontent, re.MULTILINE) is None:
            if VERBOSE > 0: print("No legal notice tag found")
        else:
            # If pattern matches, process data
            ## print(regexinfo.search(filecontent).groupdict())
            tmp_dict = regexinfo.search(filecontent).groupdict()
            ## print(tmp_dict['simparas'].strip().split("\n."))
            for tmp_item in tmp_dict['simparas'].strip().split("\n."):
                ## print(tmp_item.lstrip('.').strip())
                self.legalnotice.simpara.append(tmp_item.lstrip('.').strip())
            del(tmp_dict)

    def gen_xml_from_self(self, line_indent = ''):
        ''' Generates the xml structure from the current object
        Input parameter:
           line_indent is either one or more tab, whitespace or alike
        Returns:
            An xml-formatted string
        '''
        
        if not re.match(r'^\s*$', line_indent):
            line_indent = ""
        _result = ""

        if self.copyright.holder:
            # Generating copyright tag
            _result += "\n"+ self.copyright.gen_xml_from_self(line_indent, 
		['year','holder'])
        
        if self.legalnotice.simpara:
            # generating legalnotice tag
            _result += "\n"+ self.legalnotice.gen_xml_from_self(line_indent)

 
        if self.revhistory:
            # Generating revision history tags
            _result += "\n"+ line_indent +"<revhistory>"
            revision_items_list = ['revnumber', 'date', 'authorinitials',
		'revremark']
            for revitem in self.revhistory:
                _result += "\n"+ revitem.gen_xml_from_self(line_indent + '\t', 
			revision_items_list)
            _result += "\n"+ line_indent +"</revhistory>"
            _result += "\n"

        return _result
    
    def parse_document(self, doc_content):
        ''' Call the several methods used for parsing file
	Input parameter:
	    doc_content is the content of the document to be parsed
	'''
        self.get_revinfo_block(doc_content)
        self.get_copyright_content(doc_content)
        self.get_legalnotice_content(doc_content)


def usage():
    ''' Prints docinfo documentation '''
    print(" ***************** How to use this tool ****************** ")
    print(__doc__)
    print(" ********************************************************* ")



def main():
    ''' Main function '''
    global VERBOSE
    # Initializing the file name container.
    input_filename = ''
    
    # Checking command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', action='count', 
	help='Prints out more information during the processing status.')
    parser.add_argument('-o', '--output', action='store', 
	help='Output filename')
    parser.add_argument('asciidoc_input_file_name', 
	help='Asciidoc input file name.')
    args = parser.parse_args()
    VERBOSE = args.verbose # To be able to enable multiple levels of verbosity
    # if(args.usage): usage()
    input_filename = args.asciidoc_input_file_name
    output_filename = args.output
    del(args)

    # Proceed if file exists
    if(len(input_filename) > 0 and path.isfile(input_filename)):
        # Retrieving the data from the asciidoc text file
        ## input_filename = 'samples/test_asciidoc.txt'
        file1 = open(input_filename, 'r')
        str_in = file1.read()
        file1.close()
        del(file1)
        if(VERBOSE > 0):
            print("[INFO] File found.")
        file1 = open(input_filename, 'r')
        str_in = file1.read()
        file1.close()
        del(file1)
        
        if(VERBOSE > 0):
            print("[INFO] Parsing document content.")
        # This does it globally and print the table of hashtables to the screen.
        doc_item = docinfo()
        doc_item.parse_document(str_in)
        
        if(VERBOSE > 0):
            print("[INFO] Begining XML file generation.")
        # writing output to the target file name
        if output_filename == None:
            output_filename = doc_item.gen_docinfo_filename(input_filename)
        out_f = open(output_filename, 'w')
        out_f.write(doc_item.gen_xml_from_self(''))
        out_f.close()
        if(VERBOSE > 0):
            print("[INFO] End of XML file generation.")
    else:
        print("[ERROR] No correct file name provided.")
        if(VERBOSE > 0):
            usage()
            print("[ERROR] No correct file name provided.")
        sys.exit(2)


if __name__ == '__main__':
    main()
    #run tests if called from command-line
##    print("# Usage explanations")
##    usage()
    
##    print("# ************** Unit tests... To be done. **************")
##    print("# Testing the 'revision' class:")
##    rev_item = revision()
##    print("# A non customized revhistory class item")
##    print rev_item.gen_xml_from_self('\t')



    # This is to check whether the generated xml conforms to the docbook's DTD
    #===========================================================================
    # import libxml2
    # dtd="""<!ELEMENT foo EMPTY>"""
    # # instance=doc_item.gen_xml_from_self('')
    # dtd = libxml2.parseDTD("-//OASIS//DTD DocBook XML V4//EN",None)
    # ctxt = libxml2.newValidCtxt()
    # doc = libxml2.parseDoc(instance)
    # ret = doc.validateDtd(ctxt, dtd)
    # if ret != 1:
    #     print("error doing DTD validation")
    # else:
    #     print("Generated XML has a valid DTD!")

    # doc.freeDoc()
    # dtd.freeDtd()
    # del dtd
    # del ctxt
    #===========================================================================
    # pass
