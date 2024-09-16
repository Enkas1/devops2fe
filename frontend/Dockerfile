# Använd Nginx som basbild
FROM nginx:alpine

# Kopiera din anpassade Nginx-konfigurationsfil
COPY nginx.conf /etc/nginx/nginx.conf

# Kopiera statiska filer och HTML-filer till Nginx's standardwebbrot
COPY ./static /usr/share/nginx/html/static
COPY ./templates /usr/share/nginx/html/templates

# Exponera port 80 för HTTP
EXPOSE 80

# Starta Nginx i förgrunden
CMD ["nginx", "-g", "daemon off;"]
