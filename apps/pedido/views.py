from django.shortcuts import render

#Crear Pedido
def CrearPedido (request):
    if request.method == 'POST':
        pedido_form = PedidoForm(request.POST)
        if pedido_form.is_valid():
            pedido_form.save()
            return ListarPedido(request)
    else:
        pedido_form = PedidoForm()
    return render(request, 'pedido/crear_pedido.html',{'pedido_form':pedido_form})
