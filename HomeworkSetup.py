import time
import calendar
import re

# All whitespace to be stripped from beginning and end of a line
TO_STRIP = ' .()[]\n'

# Class of latex document to create
DOCUMENT_CLASS = 'article'

#list of all latex packages to include
PACKAGE_LIST = ['amsmath',   # For advanced latex math
                'amsfonts'  # For black-board fonts for field symbols
               ]

# Style setup for latex document
TEXT_SIZE = '12pt'
LINE_SPACING = '16pt'

# Regular expressions to recognize enumerations for lists, sorted by importance
ENUMERATION_STYLES = [r'^[0-9]+$',    # Numeric Indexing (1. 27. 100. etc)
                      r'^[a-z]$',     # Alphabetized Indexing (a. q. z. etc)
                      r'^[IVX]+$'     # Roman Numeral Indexing (I. IV. XI. etc)
                     ]





def read_and_strip_line(file_to_read):
    ''' reads line from a file and returns it with whitespace stripped '''

    return file_to_read.readline().strip(TO_STRIP)

def get_formatted_time(current_time):
    ''' Returns a Formatted latex date string using a time.struct_time '''

    # Example String: '15 November 2013'
    return '%i %s %i' %(current_time.tm_mday,
                        calendar.month_name[current_time.tm_mon],
                        current_time.tm_year)





def write_packages(my_file, packages):
    ''' Writes all required latex packages to the latex document '''

    for latex_package in packages:
        my_file.write('\usepackage{%s}\n' %(latex_package))

    my_file.write('\n')

def write_personal_info(input_file, output_file):
    ''' Writes personal info to the latex file, read from input file '''

    # Read author and date from the first two lines in the input file
    title, author = [read_and_strip_line(input_file) for x in range(0, 2)]

    # Output title, author and date settings to the latex document
    output_file.write('\\title{%s}\n' %(title))
    output_file.write('\\author{%s}\n' %(author))
    output_file.write('\\date{%s}\n\n' %get_formatted_time(time.localtime()))

def write_enumerations(input_file, output_file, enumeration_styles):
    ''' Writes enumerations for required lists to a latex document '''

    output_file.write('\t\\begin{enumerate}\n\n')

    last_style = 2

    for line in [input_line.strip(TO_STRIP) for input_line in input_file]:
        has_broken = False

        for style_number, indexing_style in enumerate(enumeration_styles, 2):
            if re.match(indexing_style, line):
                print line, indexing_style

                if style_number < last_style:
                    output_file.write('%s\\end{enumerate}\n\n' %('\t' * style_number))

                elif style_number > last_style:
                    output_file.write('%s\\begin{enumerate}\n\n' %('\t' * last_style))

                output_file.write('%s\\item %% %s\n\n' %('\t' * style_number, line))
                last_style = style_number

                has_broken = True
                break

        if not has_broken:
            raise Exception('%s is not a legal enumeration' %(line))

    output_file.write('\t\\end{enumerate}\n\n')





def format_latex_document(output_file_name):
    ''' Formats latex file for homework, with itemized lists based on input '''

    # Open the input and output files for reading and writing
    input_file = open('input.txt', 'r')
    output_file = open(output_file_name, 'w')

    # Write document class and line-spacing settings to the latex document
    output_file.write('\documentclass[%s]{%s}\n\n' %(TEXT_SIZE, DOCUMENT_CLASS))
    output_file.write('\setlength{\\baselineskip}{%s}\n\n' %(LINE_SPACING))

    # Write out all packages in PACKAGE_LIST to the latex document
    write_packages(output_file, PACKAGE_LIST)

    # Write personal info to file
    write_personal_info(input_file, output_file)

    # Write the begin document header
    output_file.write('\\begin{document}\n\n')

    # Write the make title command
    output_file.write('\\maketitle\n\n')

    # Write the list settings defined in the input_file
    write_enumerations(input_file, output_file, ENUMERATION_STYLES)

    # Finish the document with the end document header
    output_file.write('\\end{document}')

format_latex_document(raw_input("Output File Name: "))