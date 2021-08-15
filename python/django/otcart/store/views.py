
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    View
)

# Product List View
class ProductsListView(ListView):

    template_name = 'products_list.html'

    context_object_name = 'products'
    #model = Product

    #paginate_by = 6


    def get_queryset(self, *args, **kwargs):
        
        return None

# Product Detail View
class ProductDetailView(ListView):

    template_name = 'product_detail.html'

    context_object_name = 'product'

    def get_queryset(self, *args, **kwargs):
        
        return None

