from datetime import datetime

class DataMixin():
    products = None
    slides = None
    feedbacks = None 
    extra_context = {}
    year = datetime.today().year
    title = None

    def __init__(self):
        self.extra_context['year'] = self.year
        if self.products:
            self.extra_context['products'] = self.products
        if self.slides:
            self.extra_context['slides'] = self.slides
        if self.feedbacks:
            self.extra_context['feedbacks'] = self.feedbacks
        if self.title:
            self.extra_context['title'] = self.title 
                  
    def get_mixin_context(self, context, **kwargs):
        context.update(kwargs)
        return context