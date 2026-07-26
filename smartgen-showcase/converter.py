import markdown2

class MarkdownConverter:
    def __init__(self):
        # Enable common extras for documentation
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
        """Convert markdown text to HTML."""
        return markdown2.markdown(text, extras=self.extras)
