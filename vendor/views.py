from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from accounts.forms import UserProfileForm
from django.contrib import messages
from accounts.models import UserProfile
from django.contrib.auth.decorators import login_required, user_passes_test
from menu.forms import CategoryForm, FoodItemForm
from django.template.defaultfilters import slugify

from vendor.models import Vendor
from .forms import VendorForm
from accounts.views import check_role_restaurant
from menu.models import Category, FoodItem
# Create your views here.


def get_vendor(request):
    vendor = Vendor.objects.get(user=request.user)
    return vendor


@login_required(login_url='login')
@user_passes_test(check_role_restaurant)
def vprofile(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    vendor = get_object_or_404(Vendor, user=request.user)

    if request.method == 'POST':
        profile_form = UserProfileForm(
            request.POST, request.FILES, instance=profile)
        vendor_form = VendorForm(request.POST, request.FILES, instance=vendor)
        if profile_form.is_valid() and vendor_form.is_valid():
            profile_form.save()
            vendor_form.save()
            messages.success(request, 'Settings updated.')
            return redirect('vprofile')
        else:
            print(profile_form.errors)
            print(vendor_form.errors)
    else:
        profile_form = UserProfileForm(instance=profile)
        vendor_form = VendorForm(instance=vendor)

    context = {
        'profile_form': profile_form,
        'vendor_form': vendor_form,
        'profile': profile,
        'vendor': vendor,
    }
    return render(request, 'vendor/vprofile.html', context)


@login_required(login_url='login')
@user_passes_test(check_role_restaurant)
def menu_builder(request):
    vendor = get_vendor(request)
    categories = Category.objects.filter(vendor=vendor)
    context = {
        "categories": categories
    }
    return render(request, 'vendor/menu_builder.html', context)


@login_required(login_url='login')
@user_passes_test(check_role_restaurant)
def foodCategory(request, pk=None):
    vendor = get_vendor(request)
    category = get_object_or_404(Category, pk=pk)
    foodItems = FoodItem.objects.filter(vendor=vendor, category_name=category)
    context = {
        "foodItems": foodItems,
        "category": category,
    }

    return render(request, 'vendor/foodCategory.html', context)

@login_required(login_url='login')
@user_passes_test(check_role_restaurant)
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category_name = form.cleaned_data['category_name']
            category = form.save(commit=False)
            category.vendor = get_vendor(request)

            category.slug = slugify(category_name)
            form.save()
            messages.success(request, 'Category added successfully!')
            return redirect('menu_builder')
        else:
            print(form.errors)

    else:
        form = CategoryForm()
        context = {
            'form': form,
        }
        return render(request, 'vendor/add_category.html', context)

@login_required(login_url='login')
@user_passes_test(check_role_restaurant)
def edit_category(request, pk=None):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            category_name = form.cleaned_data['category_name']
            category = form.save(commit=False)
            category.vendor = get_vendor(request)

            category.save()  # here the category id will be generated
            category.slug = slugify(category_name) + \
                '-'+str(category.id)  # chicken-15
            category.save()
            messages.success(request, 'Category Updated Successfully!')
            return redirect('menu_builder')
        else:
            print(form.errors)

    else:
        form = CategoryForm(instance=category)
        context = {
            'form': form,
            'category': category,
        }
        return render(request, 'vendor/edit_category.html', context)

@login_required(login_url='login')
@user_passes_test(check_role_restaurant)
def delete_category(request, pk=None):
    category = get_object_or_404(Category, pk=pk)
    category.delete()
    messages.success(request, 'Category Deleted Successfully!')
    return redirect('menu_builder')

@login_required(login_url='login')
@user_passes_test(check_role_restaurant)
def add_food(request):
    if request.method == 'POST':
        form = FoodItemForm(request.POST, request.FILES)
        if form.is_valid():
            food_title = form.cleaned_data['food_title']
            food = form.save(commit=False)
            food.vendor = get_vendor(request)

            # here the category id will be generated
            food.slug = slugify(food_title)
            form.save()
            messages.success(request, 'Food item added successfully!')
            return redirect('foodCategory', food.category_name.id)
        else:
            print(form.errors)

    else:
        form = FoodItemForm()
        form.fields['category_name'].queryset = Category.objects.filter(vendor=get_vendor(request))
        context = {
            'form': form,
        }
        return render(request, 'vendor/add_food.html', context)


def edit_food(request, pk=None):
    food = get_object_or_404(FoodItem, pk=pk)
    if request.method == 'POST':
        form = FoodItemForm(request.POST, request.FILES,  instance=food)
        if form.is_valid():
            food_title = form.cleaned_data['food_title']
            food = form.save(commit=False)
            food.vendor = get_vendor(request)
            food.slug = slugify(food_title) 
            food.save()
            messages.success(request, 'Food Updated Successfully!')
            return redirect('foodCategory', food.category_name.id)
        else:
            print(form.errors)

    else:
        form = FoodItemForm(instance=food)
        form.fields['category_name'].queryset = Category.objects.filter(vendor=get_vendor(request))
        context = {
            'form': form,
            'food': food,
        }
        return render(request, 'vendor/edit_food.html', context)
    

@login_required(login_url='login')
@user_passes_test(check_role_restaurant)
def delete_food(request, pk=None):
    food = get_object_or_404(FoodItem, pk=pk)
    food.delete()
    messages.success(request, 'Food Item Deleted Successfully!')
    return redirect('foodCategory', food.category_name.id)
