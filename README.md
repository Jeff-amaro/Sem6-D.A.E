# Semana 6


Curso : Desarrollo de Aplicaciones Empresariales. 


El proyecto es un portal de noticias construido con Django: lista de portada,
detalle de cada noticia y listado por categoría, con imágenes destacadas,
hojas de estilos, panel de administración personalizado y pruebas.


Capturas

Portada


<img width="943" height="862" alt="image" src="https://github.com/user-attachments/assets/2884dd9e-1871-4db4-abaa-649aae4ff0bc" />


Detalles


<img width="957" height="862" alt="image" src="https://github.com/user-attachments/assets/1c280060-f820-4128-ba98-2139928085bd" />


Categoria


<img width="941" height="862" alt="image" src="https://github.com/user-attachments/assets/0b3aa1bd-fe04-4ece-a9ae-dec32c27b8ec" />


Admin


<img width="953" height="862" alt="image" src="https://github.com/user-attachments/assets/c6c6ad4a-5481-4ed2-a71f-8f113ce168e1" />


# Conclusiones


- El uso de base.html y del fragmento _article_card.html permitió reutilizar el código HTML en las tres páginas del portal, evitando repeticiones y facilitando su mantenimiento. Esto demuestra la aplicación del principio DRY de Django.
- La creación de los modelos Article, Category y Author, junto con sus relaciones y migraciones, permitió organizar correctamente los datos. Asimismo, el uso de nombres de rutas y de {% url %} facilitó la navegación interna y el mantenimiento del portal.
- La configuración de archivos estáticos y multimedia permitió aplicar los estilos CSS y mostrar las imágenes correctamente. Las pruebas realizadas confirmaron que los recursos se cargaban de manera adecuada durante el desarrollo.
- Las pruebas demostraron que Django escapa automáticamente las etiquetas HTML potencialmente peligrosas, ayudando a prevenir ataques XSS. Además, el cumplimiento de PEP 8 y la ausencia de credenciales escritas directamente en settings.py contribuyeron a mejorar la calidad y seguridad del proyecto.


