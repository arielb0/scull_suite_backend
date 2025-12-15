# Scull Suite Backend

## Description

Scull Suite Backend is a project that show programming skills developing 
applications that reside on server and exposes an REST API.

## Applications

- **Users:** Web application to manage accounts. It uses permissions to decide who access or
modify account data.

- **Recipes:** Web applications to manage cook recipes. It uses authentication and permissions
to decide who access or modify recipes entities.

## Key Learnings

- Design and manage a data persistence layer using an ORM.
- Best practices to organize backend code using a layered architecture, separation of concerns and modular design.
- Deploy a production-ready application, separating the application server from HTTP handling.
- Design, document and expose RESTful API endpoints.
- Apply JWT-based authentication in stateless API.
- Manage sensitive information using environment variables.

## Technology Stack

- PostgreSQL
- Python
- Django
- DRF
- djangorestframework_simplejwt
- djoser
- Gunicorn
- Nginx
- GNU/Linux (Debian)
- Visual Studio Code

## Architecture

- **urls:** Routing layer. Associate (mapping) a viewsets with a URL.

- **views (viewsets):** Orchestration layer. Manage HTTP request, apply 
authentication, permissions, business logic and return a HTTP response.

- **services**: Business layer. Define the logic of application, like 
uses cases, business rules and complex validations. On small applications is 
optionally.

- **serializers:**: Presentation layer. Transform JSON data to Python objects 
and vice versa, validate inputs and format output.

- **models:**: Persistence layer. Define data schema, relations, queries 
and interact with database using Django Object Relational Management (ORM).

## Deployment (Production)

The service runs on GNU/Linux environment, using PostgreSQL as database to
persist data, Nginx as HTTP server to serve static content and 
Gunicorn as application server to translate HTTP request and responses 
to Python based application, like Django/DRF.


## Technical decisions

- **PostgreSQL:** It offer strong data integrity and consistency, 
mature ecosystem, advanced features and is open source. Other 
alternatives considered are MariaDB, that offer fewer features 
and MongoDB but PostgreSQL was chosen because it offer good balance 
between performance, features and resource consumption. The trade-off 
are higher operational complexity compared to simpler engines and 
require more careful tuning high-performance scenarios.

- **Python:** This programming language offer high productivity and 
readability, excellent database integration with PostgreSQL and support
for ML and AI libraries. It is ideal for small teams or solo 
developers that need rapid prototyping and development, reducing 
boilerplate. Other alternatives considered was Java and JavaScript, 
but this languages do not offer a mature AI/ML ecosystem and do not
 allow on rapid prototyping. The trade-off is slower runtime
compared with compiled languages.

- **Django:** Chosen because it has structured and maintainable architecture, 
follow batteries-included philosophy, allow rapid development,
maintainability, offer large community and ecosystem. Other alternatives 
are Flask and FastAPI, but the philosophies of these frameworks are better 
for more custom projects. The trade-off are that Django is more heavier
that Flask or FastAPI for small projects. Also, it not offer fully support for 
async projects.

- **DRF:** It is the natural option, if you choose Django to expose REST API.
Offer seamless integration with Django. It simplifies API development, through serializers, 
viewsets and routers, to expose CRUD endpoints with minimal code. Built-in
support for JWT, token authentication, permissions and browseable API. Other 
alternatives are Vanilla Django with manual JSON views, Flask or FastAPI, 
but requires learning new frameworks or are less seamless with Django. 
The trade-off of DRF is add extra layer of abstraction over Django views.

- **Nginx:** Offer high performance, scalability, without consume excessive resources.
Is a good option to serve static files, caching them and apply SSL certificates. Allow
future horizontal scaling with minimal configuration. Also has a great documentation. Other
alternatives are Apache HTTP Server and Caddy/Lighttpd, but are heavier for concurrent connections
and has smaller community for production grade Python applications.

- **Gunicorn:** Great compatibility with Python/Django is simple, reliable, works 
seamlessly with Nginx and is scalable. Other alternatives considered was uWSGI, but has
stepper learning curve and Daphne / Hypercorn, but this server is more useful for async workloads.
The trade-off is Gunicorn is not optimized for async workloads and require careful tuning of workers
numbers based on traffic and resources.

- **JSON Web Token (JWT):** Chosen to implement authentication on project. 
. Other alternatives are traditional cookies sessions, OAuth2, but JWT
offer more simplicity, is fully compatible with SPA clients and offer horizontal 
scalability. The trade-off are the storage of tokens and how to expire them.

- **English:** The document is aimed at international developers 
and recruiters and English is the de facto language for communication 
in the industry.

## Improvements

On more complex applications, separate business logic on "services" 
module. This technical choice allow deacoplate views, serializers 
and logic.