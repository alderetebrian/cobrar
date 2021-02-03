from django.shortcuts import render
import requests

# Create your views here.
def home(request):
    api_precio = requests.get("https://www.dolarsi.com/api/api.php?type=valoresprincipales").json()
    oficial_compra = api_precio[0]['casa']['compra']
    oficial_compra = oficial_compra.replace(',', '.')

    oficial_venta = api_precio[0]['casa']['venta']
    oficial_venta = oficial_venta.replace(',', '.')
    
    blue_compra = api_precio[1]['casa']['compra']
    blue_compra = blue_compra.replace(',', '.')

    blue_venta = api_precio[1]['casa']['venta']
    blue_venta = blue_venta.replace(',', '.')

    context = {'oficial_compra': oficial_compra, 'oficial_venta': oficial_venta, 'blue_compra': blue_compra, 'blue_venta': blue_venta}

    if request.method == 'POST':
        cobrar = request.POST
        por_dia = float(cobrar['monto_ganar']) / float(cobrar['dias_trabajar'])
        por_hora = float(por_dia) / float(cobrar['horas_dias'])
        dolares_hora = float(por_hora) / float(oficial_compra)
        en_oficial = float(por_dia) / float(oficial_compra)
        en_blue = float(por_dia) / float(blue_compra)

        resultado = {'por_dia': por_dia, 'por_hora': por_hora, 'dolares_hora': dolares_hora, 'en_oficial': en_oficial, 'en_blue': en_blue}
        return render(request, 'cobrar/index.html', {'dolar_hoy': context, 'cobrar': cobrar, 'resultado': resultado})
    return render(request, 'cobrar/index.html', {'dolar_hoy': context})