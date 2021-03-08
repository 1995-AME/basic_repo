from django.urls import path     
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
	path('', views.index),
	path('add', views.add_user),
	path('create_user',views.create_user),
	path('gallery',views.gallery),
	path('profile', views.profile),
	path('profile/<int:user_id>', views.user_profile),
	path('login',views.user_login),
	path('edit/<int:user_id>', views.edit),
	path('profile_image',views.upload_image),
	path('profile_image2',views.upload_image_gallery),
	path('delete/<int:image_id>',views.delete_image),
	path('delete2/<int:image_id>',views.delete_image2),
	path('messages', views.messages),
	path('donor_mess', views.donor_mess),
	path('email/<int:user_id>',views.send_email),
	path('contact/<int:user_id>',views.contact),
	# path('create_message',views.create_message),
	path('charities',views.charities),
	path('logout', views.logout),
]



if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
