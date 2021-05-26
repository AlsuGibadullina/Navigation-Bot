from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

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


def read_structural_elements(elements):
    """Recurses through a list of Structural Elements to read a document's text where text may be
        in nested elements.

        Args:
            elements: a list of Structural Elements.
    """
    text = ''
    for value in elements:
        if 'paragraph' in value:
            elements = value.get('paragraph').get('elements')
            for elem in elements:
                text += read_paragraph_element(elem)
        elif 'table' in value:
            # The text in table cells are in nested Structural Elements and tables may be
            # nested.
            table = value.get('table')
            for row in table.get('tableRows'):
                cells = row.get('tableCells')
                for cell in cells:
                    text += read_structural_elements(cell.get('content'))
        elif 'tableOfContents' in value:
            # The text in the TOC is also in a Structural Element.
            toc = value.get('tableOfContents')
            text += read_structural_elements(toc.get('content'))
    return text


def main():
    credentials = get_credentials()
    service = build('docs', 'v1', credentials=credentials)
    # Retrieve the documents contents from the Docs service.
    document = service.documents().get(documentId=DOCUMENT_ID).execute()
    content = document.get('body').get('content')
    value1 = find_paragraph(content, 'HEADING_1')
    value2 = []
    for value in content:
        if value in value1:
            value2 = find_paragraph(content, 'HEADING_2')
    for elem in value1:
        if 'paragraph' in elem:
            ph = elem.get('paragraph').get('elements')
            for e in ph:
                print(read_paragraph_element(e))


def find_paragraph(content, style):
    values1 = []
    for value in content:
        if paragraph_style(value) == style:
            values1.append(value)
    return values1


def paragraph_style(element):
    if 'paragraph' in element:
        paragraph = element.get('paragraph')
        if 'paragraphStyle' in paragraph:
            style = paragraph.get('paragraphStyle')
            if 'namedStyleType' in style:
                return style.get('namedStyleType')


if __name__ == '__main__':
    main()
