#!/usr/bin/env python3

'''
Atempt to create a mistune-jira renderer
'''

import mistune
import re

class MistuneJiraRenderer(mistune.Renderer):

    '''
    MistuneJiraRenderer
    '''

    def get_block(self, text):

        '''
        Not sure what this is for
        '''

        return "Get Block: {}".format(text)

    def newline(self):

        return "\\"

    def text(self, text):

        return text

    def linebreak(self):

        return "\\"

    def hrule(self):

        return "\n----"

    def header(self, text, level, raw=None):

        return "\nh{}. {}\n".format(level, text)


    def list(self, body, ordered=True):

        '''
        Do Lists But There's no List Stuff Here

        Because Lists are always "inline" in Jira
        '''

        return body

    def list_item(self, text, ordered=False):

        '''
        I don't think list_item sends the "ordered" falg
        '''

        if ordered is True:
            token = "#"
        else:
            token = "*"

        return "{} {}\n".format(token, text)

    def paragraph(self, text):

        return "\n{}\n".format(text)

    def block_code(self, code, lang):

        '''
        Block Code
        '''

        replacemes = {"python3" : "python", "sh" : "bash"}

        parsed_lang = replacemes.get(str(lang).lower(), str(lang).lower())

        if parsed_lang not in ("actionscript", "ada", "applescript", "bash", "c",
                             "c#", "c++", "css", "erlang", "go", "groovy",
                             "haskell", "html", "javascript", "json", "lua",
                             "nyan", "objc", "perl", "php", "python", "r",
                             "ruby", "scala", "sql", "swift", "visualbasic",
                             "xml", "yaml"):
            parsed_lang = ""
        else:
            parsed_lang = ":{}".format(parsed_lang)

        block_code_return = '''\n{{code{}}}
{}
{{code}}\n'''.format(parsed_lang, code)

        return block_code_return


    def block_quote(self, text):

        block_quote_text ='''{{quote}}
{}
{{quote}}'''.format(text)

        return block_quote_text

    def emphasis(self, text):

        return "_{}_".format(text)

    def double_emphasis(self, text):

        return "*{}*".format(text)

    def strikethrough(self, text):

        return "-{}-".format(text)

    def codespan(self, text):

        """
        Rendering Inline Text, not really supported in Jira.
        """

        return "{{{{{}}}}}".format(text)


    def link(self, link, title, text, image=False):

        '''
        Format Links Properly
        '''

        if title is not None:
            titletext = "{}|".format(text)
        else:
            titletext = ""

        link_text = "[{}|{}]".format(titletext, text)

        if image is True:
            # Different Format
            link_text = "!{}!".format(link)

        return link_text

    def autolink(self, link, is_email=False):

        if is_email is True:
            email="mailto:"
        else:
            email=""

        autolink=" [{}{}] ".format(email, link)

        return autolink

    def image(self, src, title, text):

        '''
        Image Links
        '''

        return "!{}!".format(src)

    def table(self, header, body):

        '''
        Attempt a Table Creation
        '''

        table_text = "\n{}{}\n".format(header, body)

        return table_text


    def table_row(self, content):

        this_row = "|{}\n".format("|".join(content.split(";;")))

        #print(this_row)


        return this_row

    def table_cell(self, content, **flags):

        '''
        Jira tables are different so I'm overlosding ;; to signify the end of a column
        I'll use split later to split them back up.
        '''

        if flags.get("header", True):
            cell="|{}|;;".format(content)
        else:
            cell="{};;".format(content)

        return cell
