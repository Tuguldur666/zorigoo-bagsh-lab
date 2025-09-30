from django.contrib import admin
from .models import Category, Product

# Welcome to the coolest admin setup on the block! 😎
# Where slugs magically appear like unicorns from your names! 🦄✨

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        'slug': ('category_name',)  # Watch this slug grow up from the category_name! 🌱➡️🌳
    }

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        'slug': ('product_name',)  # Slug alert! Product names turning into slugs faster than you can say "Django rocks!" 🤘🐌
    }

# Now go ahead and enjoy watching those slugs fill themselves in like magic! 🎩🐇✨
