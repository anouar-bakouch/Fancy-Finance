# BudgetView REST API 

import pickle
from django.shortcuts import get_object_or_404, render
from BudgetPRed.serializers import BudgetSerializer, TokenPairSerializer, TokenRefreshSerializer, TokenVerifySerializer, UserSerializer
from BudgetPRed.models import Budget, User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser


def index(request):
    # return index.html in templates folder
    return render(request, 'index.html')

# budgets 

class AddBudgetView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        serializer = BudgetSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            budget_saved = serializer.save()
            return Response(
                {"success": f"Budget '{budget_saved.IDEIMPST}' created successfully"},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ListBudgetView(APIView):
    def get(self, request):
        budgets = Budget.objects.all()
        serializer = BudgetSerializer(budgets, many=True)
        return Response({"budgets": serializer.data})


class UpdateBudgetView(APIView):
    def put(self, request, pk):
        saved_budget = get_object_or_404(Budget.objects.all(), pk=pk)
        data = request.data.get('budget')
        serializer = BudgetSerializer(instance=saved_budget, data=data, partial=True)
        if serializer.is_valid(raise_exception=True):
            budget_saved = serializer.save()
        return Response({
            "success": "Budget '{}' updated successfully".format(budget_saved.IDEIMPST)
        })
    
class DeleteBudgetView(APIView):
    def delete(self, request, pk):
        # Get object with this pk
        budget = get_object_or_404(Budget.objects.all(), pk=pk)
        budget.delete()
        return Response({
            "message": "Budget with id `{}` has been deleted.".format(pk)
        }, status=204)
    
class GetBudgetView(APIView):
    def get(self, request, pk):
        # Get object with this pk
        budget = get_object_or_404(Budget.objects.all(), pk=pk)
        serializer = BudgetSerializer(budget)
        return Response({"budget": serializer.data})

class PredictBudgetView(APIView):

    # the post must accept the IDEIMPST and return the prediction 
    def post(self, request, pk):
        # Get object with this pk
        budget = get_object_or_404(Budget.objects.all(), pk=pk)
        serializer = BudgetSerializer(budget)
        # load the model from disk
        filename = 'BudgetPRed/MLPrediction/finalized_model.sav'
        loaded_model = pickle.load(open(filename, 'rb'))
        # predict the budget
        prediction = loaded_model.predict([serializer.data])
        return Response({"prediction": prediction})
    
class ListUserView(APIView):

    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response({"users": serializer.data})

class GetUserView(APIView):
    def get(self, request, pk):
        # Get object with this pk
        user = get_object_or_404(User.objects.all(), pk=pk)
        serializer = UserSerializer(user)
        return Response({"user": serializer.data})
    
class signUpView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            return Response({"success": "User '{}' created successfully".format(user.id)}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class signInView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = User.objects.filter(username=username, password=password).first()
        if user is None:
            return Response({"error": "Wrong username or password"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"success": "User '{}' signed in successfully".format(user.id)}, status=status.HTTP_200_OK)
        

class UpdateUserView(APIView):
    def put(self, request, pk):
        saved_user = get_object_or_404(User.objects.all(), pk=pk)
        data = request.data.get('user')
        serializer = UserSerializer(instance=saved_user, data=data, partial=True)
        if serializer.is_valid(raise_exception=True):
            user_saved = serializer.save()
        return Response({
            "success": "User '{}' updated successfully".format(user_saved.id)
        })
    
class DeleteUserView(APIView):
    def delete(self, request, pk):
        # Get object with this pk
        user = get_object_or_404(User.objects.all(), pk=pk)
        user.delete()
        return Response({
            "message": "User with id `{}` has been deleted.".format(pk)
        }, status=204)
    
class GetUserInfoView(APIView):
    def get(self, request, pk):
        # Get object with this pk
        user = get_object_or_404(User.objects.all(), pk=pk)
        serializer = UserSerializer(user)
        return Response({"user": serializer.data})


class TokenPairObtainView (APIView):
    def post(self, request):
        serializer = TokenPairSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)
    
class TokenRefreshView (APIView):
    def post(self, request):
        serializer = TokenRefreshSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)
    
class TokenVerifyView (APIView):
    def post(self, request):
        serializer = TokenVerifySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)
    
