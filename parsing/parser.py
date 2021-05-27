from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

from parsing.header import Header

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/documents.readonly']

# The ID of a sample document.
DOCUMENT_ID = '1RCalk-b8xGGT1D1QlKlJEYW0M_Esap56JWa3kNuDx7M'


def get_credentials():
    """Shows basic usage of the Docs API.
    Prints the title of a sample document.
    """
    credentials = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        credentials = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            credentials = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(credentials.to_json())
    return credentials


def read_paragraph_element(element):
    """Returns the text in the given ParagraphElement.

        Args:
            element: a ParagraphElement from a Google Doc.
    """
    text_run = element.get('textRun')
    if not text_run:
        return ''
    return text_run.get('content')


def get_headings():
    credentials = get_credentials()
    service = build('docs', 'v1', credentials=credentials)
    # Retrieve the documents contents from the Docs service.
    document = service.documents().get(documentId=DOCUMENT_ID).execute()
    headings = []
    content = document.get('body').get('content')
    for value in content:
        if paragraph_style(value) == 'HEADING_1':
            header = Header()
            header.name = get_name(value)
            header.links = find_links(value)
            headings.append(header)
    for header in headings:
        find_subheadings(header, content, 'HEADING_1')
    return headings


def get_name(element):
    if 'paragraph' in element:
        elements = element.get('paragraph').get('elements')
        for elem in elements:
            if 'textRun' in elem:
                text_run = elem.get('textRun')
                return text_run.get('content')


def find_subheadings(parent_header, content, style):
    flag = 0
    subheaders = []
    for value in content:
        if flag == 1:
            if paragraph_style(value) == style:
                break
            if paragraph_style(value) == next_paragraph_style(style):
                subheader = Header()
                subheader.name = get_name(value)
                subheader.links = find_links(value)
                subheaders.append(subheader)
                find_subheadings(subheader, content, next_paragraph_style(style))
        elif get_name(value) == parent_header.name:
            flag = 1
    parent_header.subheaders = subheaders


def find_links(element):
    links = []
    if 'paragraph' in element:
        elements = element.get('paragraph').get('elements')
        for elem in elements:
            if 'textRun' in elem:
                text_run = elem.get('textRun')
                if 'textStyle' in text_run:
                    text_style = text_run.get('textStyle')
                    if 'link' in text_style:
                        links.append(text_style.get('link').get('url'))
    return links


def next_paragraph_style(style):
    if style == 'HEADING_1':
        return 'HEADING_2'
    if style == 'HEADING_2':
        return 'HEADING_3'
    if style == 'HEADING_3':
        return 'HEADING_4'
    if style == 'HEADING_4':
        return 'HEADING_5'
    if style == 'HEADING_5':
        return 'HEADING_6'
    if style == 'HEADING_6':
        return ''


def paragraph_style(element):
    if 'paragraph' in element:
        paragraph = element.get('paragraph')
        if 'paragraphStyle' in paragraph:
            style = paragraph.get('paragraphStyle')
            if 'namedStyleType' in style:
                return style.get('namedStyleType')


if __name__ == '__main__':
    heads = get_headings()
    for head in heads:
        print(str(head))
