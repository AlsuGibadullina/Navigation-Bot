class Header:
    name = ''
    links = []
    subheaders = []

    def __str__(self) -> str:
        text = self.name + 'links:\n'
        for link in self.links:
            text += link + ' '
        text += 'subheads:\n'
        for sub in self.subheaders:
            text += ' ' + str(sub)

        return text
