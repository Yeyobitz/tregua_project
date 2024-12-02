from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ContactForm
from django.core.mail import send_mail

def nuestra_historia(request):
    return render(request, 'core/nuestra_historia.html')

def contacto(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Send email
            send_mail(
                f"Contacto: {form.cleaned_data['asunto']}",
                f"Mensaje de {form.cleaned_data['nombre']} ({form.cleaned_data['email']}):\n\n{form.cleaned_data['mensaje']}",
                form.cleaned_data['email'],
                ['your-email@tregua.com'],
                fail_silently=False,
            )
            messages.success(request, 'Mensaje enviado correctamente')
            return redirect('core:contacto')
    else:
        form = ContactForm()
    
    return render(request, 'core/contacto.html', {'form': form})

