class Header:
    name = ''
    links = []
    subheaders = []

    def get_name(self):
        return self.name

    def get_links(self):
        return self.links

    def get_subheaders(self):
        return self.subheaders

    def __str__(self) -> str:
        text = self.name + '\nlinks:\n'
        for link in self.links:
            text += link + '\n'
        text += 'subheads:\n'
        for sub in self.subheaders:
            text += ' ' + str(sub)

        return text
