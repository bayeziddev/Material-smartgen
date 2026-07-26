import markdown2

class MarkdownConverter:
    def __init__(self):
        self.extras = [
            "fenced-code-blocks",
            "tables",
            "header-ids",
            "toc",
            "metadata",
            "code-friendly",
            "task_list"
        ]

    def convert(self, text):
        return markdown2.markdown(text, extras=self.extras)