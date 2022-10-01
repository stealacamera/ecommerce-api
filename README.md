# Ecommerce API
> REST API to store and keep track of categories, products, user carts, orders/sales.


## API endpoints
<sub>*Uses JWT authentication.  
Methods in italic are only accessible by users.  
Methods in bold are only accessible by admins.*</sub>

### User endpoints 
`http://localhost:5000/account/`
| Endpoint  | HTTP methods | Description |
| --- | --- | --- |
| `register/` | `POST` |
| `change-password/` | *`POST`* | Updates password & blacklists current refresh token |
| `change-address/` | *`PUT` `PATCH`* | Updates user address info (city, street address, zip code) |
| `token-refresh/` | `POST` |
| `login/` | *`POST`* | Enter username & password to log in |
| `logout/` | *`POST`* | Blacklists current refresh token |
| `profile/` | *`GET` `POST`* | Get logged-in user's profile; Change username |
| `profile/<slug:username>/` | `GET` | Get the specified user's profile |

### Product endpoints
`http://localhost:5000/`
| Endpoint  | HTTP methods | Description |
| --- | --- | --- |
| `category/` | `GET` **`POST`** | Returns list of categories |
| `category/<pk>/` | `GET` **`PUT` `PATCH` `DELETE`** |
| ` ` | `GET` *`POST`* | Returns list of products |
| `<pk>/` | `GET` *`PUT` `PATCH` `DELETE`* |
| `<int:product_pk>/reviews/` | `GET` *`POST`* | Returns reviews for the specified product |
| `<int:product_pk>/reviews/<int:pk>/` | `GET` *`PUT` `PATCH` `DELETE`* |

### Cart endpoints
`http://localhost:5000/cart/`
| Endpoint  | HTTP methods | Description |
| --- | --- | --- |
| ` ` | *`GET`* | Returns user cart items |
| `<int:pk>/` | *`GET` `PUT` `PATCH` `DELETE`* |
| `add/<int:product_pk>/` | *`POST`* | Add specified product to user's cart |

### Order endpoints
`http://localhost:5000/orders/`
| Endpoint  | HTTP methods | Description |
| --- | --- | --- |
| `checkout/` | *`POST`* | Turns cart items to orders, deleting the existing cart |
| `history/` | *`GET`* | Returns the user's placed orders |
| `sales/` | *`GET`* | Returns the user's sales/shop orders |
| `sales/<int:pk>/` | *`GET` `PUT` `PATCH` `DELETE`* |
