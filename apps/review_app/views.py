# -*- coding: utf-8 -*-
from __future__ import unicode_literals


from django.shortcuts import render,redirect
from .models import User,Book,Review
from django.contrib import messages


def index(request):

	return render(request,'review_app/index.html')

def register(request):

	response=User.objects.register(

		request.POST['username'],
		request.POST['email'],
		request.POST['password'],
		request.POST['conf_password']

			)
	print response
	if response['valid']:
		request.session['user_id']=response['user'].id
		return redirect('/success')

	else:
		for error_message in response['errors']:
			messages.add_message(request,messages.ERROR,error_message)
		return redirect('/')


def login(request):

	response=User.objects.login(

		request.POST['email'],
		request.POST['password']

			)
	print response
	if response['valid']:
		request.session['user_id']=response['user'].id
		return redirect('/success')

	else:
		for error_message in response['errors']:
			messages.add_message(request,messages.ERROR,error_message)
		return redirect('/')

def success(request):
	if 'user_id' not in request.session:
		return redirect('/')

	all_books=Book.objects.all()
	current_reviews=[]
	for review in Review.objects.all().order_by('-created_at')[:3]:
		current_reviews.append({
			'title':review.book.title,
			'rating':review.rating,
			'review':review.review,
			'reviewer':review.user.username,
			'stars':"★"*int(review.rating)+"☆"*(5-int(review.rating)),
			'user_id':review.user.id,
			'book_id':review.book.id

			})
		all_books=all_books.exclude(id=review.book.id)

	context={
		'all_books':all_books,
		'user':User.objects.get(id=request.session['user_id']),
		'current_reviews':current_reviews
		
	}

	return render(request,'review_app/success.html',context)

	
def my_book(request,id):
	
	return render(request,'review_app/new_book.html',{'id':id})

def add_book(request,id):

	user=User.objects.get(id=id)
	response=Book.objects.bookCheck(
		request.POST['title'],
		request.POST['author'],
		user
	)
	

	if response["valid"]:

		response_2=Review.objects.reviewCheck(

			user,
			response['book'],
			request.POST['review'],
			int(request.POST['rating']),

		)

		if response_2["valid"]:
			return redirect('/success')
		else:
			for error_message in response_2['errors']:
				messages.add_message(request,messages.ERROR,error_message)
			return redirect ('/my_book/'+str(id))


	else:
		for error_message in response['errors']:
			messages.add_message(request,messages.ERROR,error_message)
		return redirect ('/my_book/'+str(id))


def book_info(request,id):
	context = {

		'this_book':Review.objects.filter(book_id=id),
		'book':Book.objects.get(id=id)
	}

	return render(request,'review_app/book_info.html',context)

def add_review(request, id):

	if request.POST['review']=='':
		messages.add_message(request,messages.ERROR,'Review field cannot be blank')
	else:
		book = Book.objects.get(id=id)
		user=User.objects.get(id=request.session['user_id'])

		reviews=Review.objects.create(user=user,book=book,review=request.POST['review'],rating=int(request.POST['rating']))
	return redirect('/book_info/'+str(id))


def user_info(request,id):

	context={
	'users':User.objects.get(id=id),
	'your_reviews':Review.objects.filter(user_id=id)
	
		}
	print context
	return render(request,'review_app/user_info.html',context)

def delete(request,id):

	Review.objects.get(id=id).delete()

	return redirect('/success')

def logout(request):
	request.session.clear()

	return redirect('/')
