# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import re
import bcrypt



EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9+-._]+@[a-zA-Z0-9+-._]+\.[a-zA-Z]+$')


class UserManager(models.Manager):
	def register(self,username,email,password,conf_password):

		response={
			'valid':True,
			'errors':[],
			'user':None
		}
		#for username
		if len(username)<1:
			response['errors'].append('Username is required')
		elif len(username)<2:
			response['errors'].append('Username must be greater than 2 characters or more')
			#for email
		if len(email)<1:
			response['errors'].append('Email is required')
		elif not EMAIL_REGEX.match(email):
			response['errors'].append('Invalid Email')
		else:
			email_list=User.objects.filter(email=email.lower())
			if len (email_list)>0:
				response['errors'].append('Email already exist')
		
			#for password
		if len(password)<1:
			response['errors'].append('Password is required')
		elif len(password)<8:
			response['errors'].append(' Password must be greater than 8 characters or more')

			#for conf password
		if len(conf_password)<1:
			response['errors'].append('Please confirm the password')
		if conf_password != password:
			response['errors'].append('Confirm password must match password')

		if len(response['errors'])>0:
			response['valid']=False

		else:
			user=User.objects.create(
				username=username,
				email=email.lower(),
				password=bcrypt.hashpw(password.encode(),bcrypt.gensalt())

			)
			response['user']=user

		return response


	def login(self,email,password):

		response={
			'valid':True,
			'errors':[],
			'user':None
		}
		#for email
		if len(email)<1:
			response['errors'].append('Email is required')
		elif not EMAIL_REGEX.match(email):
			response['errors'].append('Email is required')
		else:
			email_list=User.objects.filter(email=email.lower())
			if len (email_list)==0:
				response['errors'].append('Email doesnot exist')
		#for password
		if len(password)<1:
			response['errors'].append('Password is required')
		elif len(password)<8:
			response['errors'].append(' Password must be greater than 8 characters or more')

		if len(response['errors'])==0:
			hashed_pw = email_list[0].password
			if bcrypt.checkpw(password.encode(),hashed_pw.encode()):
				response['user']=email_list[0]
			else:
				response['errors'].append('Incorrect Password')

		if len(response['errors'])>0:
			response['valid']=False

		return response

class BookManager(models.Manager):
	def bookCheck(self,title,author,uploaded_by):
		response={
			'valid':True,
			'errors':[],
			'book':None
		}
		
		# #for book title
		if len(title)<1:
			response['errors'].append('Title is required')

		# #for author
		if len(author)<1:
			response['errors'].append('Author name is required')

		if len(response['errors'])>0:
			response['valid']=False

		else:
			book=Book.objects.create(
				title=title,
				author=author,
				uploaded_by=uploaded_by
				
			)

			response['book']=book

		return response

		

class ReviewManager(models.Manager):
	def reviewCheck(self,user,book,review,rating):
		response={
			'valid':True,
			'errors':[],
			'review':None
		}

		#for reviews
		if len(review)<1:
			response['errors'].append('Please give some review')

		if len(response['errors'])>0:
			response['valid']=False

		else:
			my_review=Review.objects.create(
				user=user,
				book=book,
				review=review,
				rating=rating
				
			)

			response['review']=my_review

		return response


class User(models.Model):
	username= models.CharField(max_length=255)
	email=models.CharField(max_length=255)
	password=models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	objects=UserManager()

	def __repr__(self):
		return "<User object: {} {} {}>".format(self.username, self.email, self.password)


class Book(models.Model):
	title=models.CharField(max_length=255)
	author=models.CharField(max_length=255)
	uploaded_by=models.ForeignKey(User,related_name="uploaded_related")
	created_at=models.DateTimeField(auto_now_add=True)
	updated_at=models.DateTimeField(auto_now=True)
	objects=BookManager()
	
	def __repr__(self):
		return "<Book object: {} {} {}>".format(self.title, self.author, self.uploaded_by)


class Review(models.Model):
	user=models.ForeignKey(User,related_name='user_review')
	book=models.ForeignKey(Book,related_name='book_review')
	review=models.TextField(max_length=1000)
	rating=models.IntegerField()
	created_at=models.DateTimeField(auto_now_add=True)
	updated_at=models.DateTimeField(auto_now=True)
	objects=ReviewManager()

	def __repr__(self):
		return "<Review object: {} {} {}>".format(self.user, self.book, self.review)


