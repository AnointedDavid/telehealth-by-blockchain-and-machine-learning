from django.urls import path

from . import views

urlpatterns = [path("index.html", views.index, name="index"),
	       path('Login.html', views.Login, name="Login"), 
	       path('Register.html', views.Register, name="Register"),
	       path('Signup', views.Signup, name="Signup"),
	       path('UserLogin', views.UserLogin, name="UserLogin"),
	       path('AddPatientCondition.html', views.AddPatientCondition, name="AddPatientCondition"),
	       path('AddPatientConditionAction', views.AddPatientConditionAction, name="AddPatientConditionAction"),
	       path('Predict.html', views.Predict, name="Predict"),
	       path('PredictAction', views.PredictAction, name="PredictAction"),
]