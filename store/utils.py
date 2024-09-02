from datetime import datetime

class DataMixin():
    extra_context = {}
    year = datetime.today().year
    title = None

    def __init__(self):
        self.extra_context['year'] = self.year
        if self.title:
            self.extra_context['title'] = self.title 
                  
    def get_mixin_context(self, context, **kwargs):
        context.update(kwargs)
        return context
