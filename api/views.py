from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Account, Stock, OwnStock
from rest_framework.authtoken.models import Token
from .serializers import AccountSerializer, RegistrationSerializer, StockSerializer, OwnStockSerializer, myHistorySerializer


# Create your views here.
@api_view(["POST"])
def register(request):
    serializer = RegistrationSerializer(data = request.data)
    if serializer.is_valid():
        account = serializer.save()
        token = Token.objects.get(user=account).key
        data = {
            'response': "Successfully registered a new user.",
            'email': account.email,
            'username': account.username,
            'token': token,
            'first_name': account.first_name,
            'last_name': account.last_name,
        }
    else:
        data = serializer.errors
    return Response(data)

@api_view(["POST"])
@permission_classes((IsAuthenticated,))
def stockTransaction(request):
    user = request.user
    stock = Stock(user=user)
    serializer = StockSerializer(stock,data=request.data)
    account = Account.objects.get(username=user.username)
    money = (float(account.money))
    total = float(request.data['price']) * (request.data['quantity'])
    total = "{:.2f}".format(total)
    total= float(total)
    check = OwnStock.objects.filter(user=user, symbol=request.data['symbol'])
    if request.data['type'] == "Buy":
        if check:
            ownStock = OwnStock.objects.get(user=user, symbol=request.data['symbol'])
            newTotal = float(ownStock.total) + total 
            newTotal = "{:.2f}".format(newTotal)
            newTotal= float(newTotal)
            ownSerializer = OwnStockSerializer(ownStock,data={"symbol":request.data['symbol'], "quantity": 
            request.data['quantity'] + ownStock.quantity,'total': newTotal})
            if ownSerializer.is_valid():
                ownSerializer.save()
        else:
            ownStock = OwnStock(user=user)
            ownSerializer = OwnStockSerializer(ownStock,data={"symbol":request.data['symbol'], "quantity": request.data['quantity'],
            'total': total})
            if ownSerializer.is_valid():
                ownSerializer.save()
    else:
        if check:
            ownStock = OwnStock.objects.get(user=user, symbol=request.data['symbol'])
            newTotal = float(ownStock.total) - total 
            newTotal = "{:.2f}".format(newTotal)
            newTotal= float(newTotal)
            ownSerializer = OwnStockSerializer(ownStock,data={"symbol":request.data['symbol'], "quantity": 
            ownStock.quantity -request.data['quantity'],'total': newTotal})
            if request.data['quantity'] > ownStock.quantity:
                return Response({'response': "You are trying to sell more than you own."})
            if ownSerializer.is_valid():
                print('YES')
                ownSerializer.save()
        else:
            return Response({'response': "You do not own this stock."})

    checkStock = OwnStock.objects.get(user=user, symbol=request.data['symbol'])
    if checkStock.quantity == 0:
        checkStock.delete()

    if serializer.is_valid():
        serializer.save()
        if request.data['type'] == "Buy":
            account.money = money - total
            account.save()
        else:
            account.money = money + total
            account.save()
        return Response(serializer.data)
    return Response(serializer.errors)

@api_view(["GET"])
@permission_classes((IsAuthenticated,))
def getStockHistory(request):
    user = request.user
    history = Stock.objects.filter(user=user)
    serializer = myHistorySerializer(history, many=True)

    return Response(serializer.data)

@api_view(["GET"])
@permission_classes((IsAuthenticated,))
def getMyStock(request):
    user = request.user
    myStocks = OwnStock.objects.filter(user=user)
    serializer = OwnStockSerializer(myStocks, many=True)

    return Response(serializer.data)

@api_view(["GET"])
@permission_classes((IsAuthenticated,))
def getAccount(request):
    user = request.user
    account = Account.objects.get(username=user.username)
    serializer = AccountSerializer(account, many=False)
    return Response(serializer.data)
