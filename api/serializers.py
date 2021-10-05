from rest_framework import serializers 
from .models import OwnStock, Stock, Account

class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type':'password'}, write_only = True)
    class Meta:
        model = Account
        fields = ['username', 'email', 'password', 'password2', 'first_name', 'last_name']
        extra_kwargs = {
            'password' : {'write_only': True}
        }
    
    def save(self):
        user = Account(
            email=self.validated_data['email'],
            username= self.validated_data['username'],
            first_name = self.validated_data['first_name'],
            last_name = self.validated_data['last_name']
        )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2: 
            raise serializers.ValidationError({'password': 'Passwords must match'})
        user.set_password(password)
        user.save() 
        return user

class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = ['symbol', 'quantity', 'price', 'type']

class myHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = ['symbol', 'quantity', 'price', 'type', 'date']

class OwnStockSerializer(serializers.ModelSerializer):
    class Meta:
        model = OwnStock
        fields = ['symbol', 'quantity', 'total']

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['money', 'email', 'first_name', 'last_name']