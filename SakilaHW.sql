SELECT actor.first_name AS "First Name", actor.last_name AS "Last Name" 
FROM actor
JOIN film_actor ON actor.actor_id = film_actor.actor_id AND film_actor.film_id=1;

SELECT category.name AS "Category", COUNT(*) AS "Count"
FROM category
JOIN film_category ON category.category_id = film_category.category_id
GROUP BY film_category.category_id;

SELECT film.rating AS "Rating", AVG(film.rental_duration) AS "Average Rental Length"
FROM film
GROUP BY film.rating;

SELECT customer.first_name AS "First Name", customer.last_name AS "Last Name", COUNT(*) AS "Num Rentals"
FROM customer
JOIN rental ON customer.customer_id = rental.customer_id
GROUP BY customer.customer_id;

SELECT store.store_id, COUNT(rental.staff_id) AS "Num Rentals"
FROM store
JOIN rental ON store.store_id = rental.staff_id
GROUP BY store.store_id
ORDER BY "Num Rentals" DESC
LIMIT 1;

SELECT category.name AS "Category", COUNT(rental.rental_id) AS "Num Rentals"
FROM rental
JOIN inventory ON rental.inventory_id = inventory.inventory_id
JOIN film_category ON inventory.film_id = film_category.film_id
JOIN category ON category.category_id = film_category.category_id
GROUP BY category.name
ORDER BY "Num Rentals" DESC
LIMIT 1;

SELECT category.name AS "Category", AVG(film.rental_rate) AS "Average Rental Cost"
FROM film
JOIN film_category ON film.film_id = film_category.film_id
JOIN category ON film_category.category_id = category.category_id
GROUP BY category.category_id;

SELECT film.title AS "Film", MAX(rental.rental_date) AS "Last Rental Date"
FROM rental
JOIN inventory ON rental.inventory_id = inventory.inventory_id
JOIN film ON inventory.film_id = film.film_id
GROUP BY film.film_id;

SELECT customer.first_name AS "First Name", customer.last_name AS "Last Name", SUM(payment.amount) AS "Total Spending"
FROM customer
JOIN payment ON customer.customer_id = payment.customer_id
GROUP BY payment.customer_id;

SELECT language.name AS "Language", AVG(film.length) AS "Average Film Length"
FROM language
JOIN film ON language.language_id = film.language_id
GROUP BY language.name;