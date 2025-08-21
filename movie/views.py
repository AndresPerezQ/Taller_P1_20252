from django.shortcuts import render
from django.http import HttpResponse
import matplotlib.pyplot as plt
import matplotlib
import io
import urllib, base64

from .models import Movie
# Create your views here.

def home(request):
    ##return HttpResponse('<h1> Welcome to the Home Page </h1>')
    ##return render (request, 'home.html')
    ## return render(request, 'home.html', {'name': 'Andrés Pérez Quinchía :D'})
    searchTerm = request.GET.get('searchMovie')
    if searchTerm:
        movies = Movie.objects.filter(title__icontains=searchTerm)
    else:
        movies = Movie.objects.all()
    return render(request, 'home.html', {'searchTerm': searchTerm, 'movies': movies})

def about(request):
    ##return HttpResponse('<h1> About Page by Andrés Pérez Quinchía <h1>')
    return render(request, 'about.html')

def signup(request):
    email = request.POST.get('email')
    return render(request, 'signup.html', {'email': email})

def statistics_view(request):
    matplotlib.use('Agg')
    # Obtener todas las películas
    all_movies = Movie.objects.all()
    
    # ===== GRÁFICA 1: Películas por año =====
    movie_counts_by_year = {}
    for movie in all_movies:
        year = movie.year if movie.year else "None"
        if year in movie_counts_by_year:
            movie_counts_by_year[year] += 1
        else:
            movie_counts_by_year[year] = 1

    # Crear la gráfica de años
    plt.figure(figsize=(10, 5))
    bar_positions = range(len(movie_counts_by_year))
    plt.bar(bar_positions, movie_counts_by_year.values(), width=0.5, align='center')
    plt.title('Movies per Year')
    plt.xlabel('Year')
    plt.ylabel('Number of movies')
    plt.xticks(bar_positions, movie_counts_by_year.keys(), rotation=90)
    plt.subplots_adjust(bottom=0.3)
    
    # Guardar la gráfica de años
    buffer_year = io.BytesIO()
    plt.savefig(buffer_year, format='png')
    buffer_year.seek(0)
    plt.close()
    
    # Convertir a base64
    image_png_year = buffer_year.getvalue()
    buffer_year.close()
    graphic_year = base64.b64encode(image_png_year).decode('utf-8')
    
    # ===== GRÁFICA 2: Películas por género =====
    movie_counts_by_genre = {}
    for movie in all_movies:
        if movie.genre:
            # Manejar múltiples géneros separados por comas
            genres = [genre.strip() for genre in str(movie.genre).split(',')]
            for genre in genres:
                if genre:
                    if genre in movie_counts_by_genre:
                        movie_counts_by_genre[genre] += 1
                    else:
                        movie_counts_by_genre[genre] = 1
        else:
            no_genre = "No Genre"
            movie_counts_by_genre[no_genre] = movie_counts_by_genre.get(no_genre, 0) + 1

    # Crear la gráfica de géneros
    plt.figure(figsize=(10, 5))
    bar_positions_genre = range(len(movie_counts_by_genre))
    plt.bar(bar_positions_genre, movie_counts_by_genre.values(), width=0.5, align='center', color='orange')
    plt.title('Movies per Genre')
    plt.xlabel('Genre')
    plt.ylabel('Number of movies')
    plt.xticks(bar_positions_genre, movie_counts_by_genre.keys(), rotation=45, ha='right')
    plt.subplots_adjust(bottom=0.3)
    
    # Guardar la gráfica de géneros
    buffer_genre = io.BytesIO()
    plt.savefig(buffer_genre, format='png')
    buffer_genre.seek(0)
    plt.close()
    
    # Convertir a base64
    image_png_genre = buffer_genre.getvalue()
    buffer_genre.close()
    graphic_genre = base64.b64encode(image_png_genre).decode('utf-8')
    
    # Renderizar la plantilla con ambas gráficas
    return render(request, 'statistics.html', {
        'graphic': graphic_year,  # Mantiene compatibilidad con template existente
        'graphic_genre': graphic_genre  # Nueva gráfica
    })