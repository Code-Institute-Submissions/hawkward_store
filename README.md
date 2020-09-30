# Hawkward Store
## An animal e-commerce webpage. 

This is my fourth and final Milestone Project! The purpouse of the webpage is a animal store which has 2 highlights!
The first beeing subscription system where the customer gets sent the newest item added to the store each month. And the second beeing a giftcard system that incentivises the customer to return to the store and to purchase more and more products from my webpage! Every 7th item of the same product is automatically for free and you don't have to pay for it. 

This project includes interactivity, database management, data manipulation, payment system, and ease of use. It is easy to navigate, easy to understand and has been testet by several people before publishing.

The project is deployed to heroku under:
## [Hawkward-Store](https://hawkward-store.herokuapp.com/)

## Table of Contents

1. **[UX](#UX)**

    * **[Wireframes and user Stories](#wireframes)**

2. **[Features](#features)**

   * **[Existing Features](#existing-features)**
        * **[Navigation](#navigation)**
        * **[Sidebar](#Sidebar)**
        * **[Store](#Store)**
        * **[Giftcard](#Giftcard)**
        * **[Queries](#Queries)**
        * **[Users](#Users)**
        * **[Admin](#Subscription)**
        * **[Authentication](#Subscription)**
        * **[Checkout](#Checkout)**
        * **[Subscription](#Subscription)**
   * **[Future Features](#future-features)**

3. **[Technologies Used](#technologies-used)**

   * **[Languages](#languages)**
   * **[Libraries](#libraries)**
   * **[API](#api)**
   * **[Tools](#tools)**
   * **[Hosting](#hosting)**
   
4. **[Testing](#testing)**

5. **[Deployment](#deployment)**

6. **[Credits](#credits)**


## Wireframes for the project

<p>To view all wireframes and user stories created please go to the wireframes folder</p>
<p>Because of time constraints i haven't given creating a lot of wireframes priority and I also deviated quiet a bit from my original design</p>

## Features

### Existing Features
#### Navigation   
  * For users to the site who are not logged in:    
    1. Expand to show sidebar
    2. Profile    
    3. Login
    4. Register
    5. Shopping Bag
  * For users who are logged in: 
    1. Expand to show sidebar
    2. Profile    
    3. My Profile
    4. Logout
    5. Shopping Bag
  * For admin/moderator: 
    1. Expand to show sidebar
    2. Admin Tab    
    3. Profile
    4. Product Management
    5. My Profile
    6. Logout
    7. Shopping Bag
  * The navbar is collapsed into a burger icon on small screens. The options remain the same, but they are instead accessed using a side navigation element which can be accessed through 'burger' icon at the top right.
#### Sidebar
  * This is the same for all users:
    1. Logo
    2. Searchbar for queries in the database
    3. Page information
    4. Showing all Products
    5. Showing newest Products added
    6. Showing all Products related to Dogs
      * Submenu:
        1. Food
        2. Toys
        3. Other
    7. Showing all Products related to Cats
      * Submenu:
        1. Food
        2. Toys
        3. Other
    8. Showing all Products that have the Giftcard system enabled
    9. Showing all other Products not related to any of the links
    10. Setting up a subscription


#### Store
* The overall intent and usage of the webpage:
  * The store is an animals store and has a specific customer base.
  * I want to sell only animal, or animal related, products and have animals and nature as a theme of the store.
  * As an inspiration to this I used a local animal store from where I live, I also used got the explicit allowance to  use their products/data to create this store. Not all Products have been added since I had to add them manually.

#### Giftcard
  * This is a Feature to incentivise customers to use our Page!
    * The main goal is to make people login/create an account and as a reward some items(specifically food items) will be for free for every 7th purchase
    * My implementation of the giftcard system was to give every Product a Boolean attribute and storing that.
    * I then retrieve this attribute before checkout and also check if the logged in user has a giftcard for that particular product already. If not I create one.
    * I add the products to this giftcard and check if there are 7 or more products on it. If there are I add a session item that stores free products and substract 7 from the counter. I do this for as long as the counter is above 7.
    * I then continue to the checkout process that checks if there are free items in the session. If so it substracts the product price from the total for every product and quantity of that product in the free item session.
    * If the checkout succeeds nothing more is done else then deleting the free item session.
    * If checkout fails I use the free item session to recreate the old giftcard, save that and then delete the free item session.
    * The whole intent of this is to incentivise people to become return customers and to create an account. Only if you buy 7 items of the same product and you have a logged in account, will you be able to utilize this feature.
#### Queries
* Beeing able to search the entire webpage:
  * The goal of a searchbar is to be able to quickly find and check for items that are in the store.
  * This is achieved by sending a post to the products method and retrieving the values sent. I then check the database for all items containing either part of the search in category, name or description.
  * It then returns to the products view and only shows the items that were found in the database.

#### Users
* Creating a user specific profile and having access to your profile page
  * The intent of this is to create a userprofile that stores your information for an easier checkout process.
  * This is only used to prefill forms on the webpage.
  * When paying for your items in the shopping bag you have the option to save the information and when this is done it will save all the information to the userprofile. It is connected to your user login.
  * I first wanted to add the giftcard to the userprofile but ran into trouble iterating through it since i am creating a giftcard for every product and for every user. I therefore decided to create giftcards seperately.
  * You can also access all your orders through your profile page and see all Giftcards that have been created.
  * Here you can also set up or delete subscriptions.

#### Admin
* Creating a product management system that superusers can use.
  * This was created in order to implement CRUD operations for Products, Categories and animals.
  * This was one of the first things I created in order to create, retreive, update and delete items from the Store.
  * Since I had no fixtures I had this quite high on my priority list in order to test be able to test: queries, retreiving products, adding them to the shopping bag, changing quantities and so on.
  * It is a simple page that from the start was not ment to be accesible for any user and therefore is quiet simple.
  * I have not found any issues regarding this feature.

#### Authentication
* Creating and logging in to accounts.
  * I used the standard Allauth authentication system and changed the templates a bit.
  * I added both Facebook and Google social login. Both through the integrated Admin site of Django.
  * Other than that it is base Allauth

### Before we continue to the payment functionality of the page:
  * I have had time constraints during this project and would've liked to implement this way better than it is.
  * I also struggled a lot with Stripe and intents and webhooks.
  * This resulted in me not beeing able to implement correct webhook usage, creating customers and adding them to the userprofile, updating payment information, retreiving your invoices from stripe and so on.
  * There are a lot more features I wanted to implement in regards to payment and know now that I would've done a better job with more time and my understanding of it now after having struggled with it for so long.
  * During the end of the project I started to understand the Stripe API better and see now that I could've done a lot more.


#### Checkout
* Beeing able to buy products from the store.
  * I first created a shopping bag context and a shopping bag session in order to store all the products to the shopping bag.
  * I then check for giftcard products.
  * You can then continue to the checkout page which prompts a checkout form. This form checks if there is a userprofile asociated to your account and if so prefills the form for you. If not then you can log in in order to save your information and create a userprofile.
  * After that you can continue to the payment page and have to enter your card details.  
  * If you use a non 3dsecure card everything works and you will be redirected to the 3dsecure page. If authentication succeeds you are redirected to the payment success template and a order confirmation is sent to the given email as well as the shopping bag deleted.
  * If authentication fails the order is deleted, you will not reveive an email and you will be redirected to the error template that tells you the error message and also gives you the option to return to the store. The shopping bag will not be deleted.

  * #### KNOWN BUGS:
    * The first time you try to pay and the app talks to stripe the redirect doesn't wait long enough and stripe has no time to respond. It therefore sometimes throws out an 500 error. 
    * When adding only one giftcard item to the shopping cart and this item beeing for free stripe renders an error cause the amount of payment is 0. I noticed this error 1 hour before having to deliver the project and couldn't fix  the issue anymore.
    * My thought of how to fix these bugs:
      * Check in the payment-method view if the amount = 0 and if so check if the shopping bag only contains giftcard products. If so confirm the order without using stripe.
      * Create an await function in order to wait for stripe to reply before redirecting to the next page.

#### Subscription
* A subscription service where you can sign up and reveive the last item added to the store for free!
  * The intent again is to make customers return to my store and to incentivise the use of specifically MY STORE,
  * When you set up the subscription you choose a plan (monthly or yearly), You have to be logged in in order to subscribe.
  * You then have to insert you payment information. and will be redirected to the either a 3dsecure, payment success or payment error template.
  * If payment succeeds a stripe customer and a stripe subscription is created as well as a subscription in my own databse with account name, and subscription id.
  * if the payment fails the subscription is not created and nothing is stored in my database. You will be redirected to the payment error template and reveive a message about what went wrong.
  * You can either delete or create a subscription but you cannot update your payment information.
  * #### KNOWN BUG:
    * Paying with a card that is not 3dsecure sometimes throws out an error that then prevents the creation of a subscription in my own database but which handles a payment in stripe. It only handles the payment and does not create a subscription. Paying with a 3dsecure card does not create this error.
     * I have no idea why this happens since it works with 3dsecure cards.

### Future Features
  * I wanted to implement a Newsletter system.
  * Updating payment information for both subscription and normal checkout.
  * Adding the stripe customer to the userprofile database including invoices subscriptions and so on.
  * Sending mails in case of an unexpected webhook error so that the store owner is notified if something is wrong with stripe.
  * Pagination
  * Making the website "prettier", seem more modern,
  * Adding more javascript functionality and implementing await functions that wait for stripe to answer.
  * Adding a webhook system for stripe.
  * Adding a facebook bubble system so that customers can contact the store owner over facebook.
  * Adding a contact us form that sends an email to the store owner/webpage host.

## Technologies Used

### Languages
*   HTML  
*   CSS
*   JavaScript
*   Python3

### Libraries
* Google Fonts
* Font Awesome
* Bootstrap
* Jquery
* Django with several sublibraries
* Postgres

### API
* Google Mail
* Facebook
* AWS S3
* Stripe

### Tools
* Visual Studio Code
* Git
* GitHub
* AdobeXD
* autopep8

### Hosting
* Heroku
* AWS S3

## Testing
Most of the testing was manual testing during the development and having the webpage and code already posted so that friends, family and coworkers could review the code and give feedback during development.

Several people have tested how the page displays on different devices, registered their own accounts, added their reviews, edited and deleted and given feedback to the general UX design of the page.

If you'd like to test the page yourself feel free to browse as a guest or create a user!

### Validation Services
I tested my code with the following validation services:
* W3C Markup Validation  
* W3C CSS validation
* JSHint

On my local machine i used the standard validation and autocorrect of:
* VScode
* Werkzeug
* autopep8

### Responsiveness
Since my project was hosted almost immideately and i constantly had people looked at my progress i got a lot of feedback in regards to responsiveness and I also addressed all the issues that were brought up.

Throughout the project I used chrome developer tools continuously and have constantly been checking weird css mistakes and responsiveness.

### Devices Used
These are the devices used throughout the testing/development:
* Samsung Galaxy S8 – Android 8.0
* OnePlus 6T - OxygenOS, Android 10
* Apple Macbook Air - Safari browser
* Apple iPhone 6,7 &8S - Safari Browser
* iPad Mini - Safari Browser
* Desktop - Chrome v.74
* Desktop - Firefox v.67
* OnePlus 6T - OxygenOS, Android 10
* Samsung Galaxy S8 – Android 8.0

### Browsers Used
These are the browsers used throughout the testing/development:
    Chrome
    Firefox
    Microsoft Edge

## Features Testing
### I wanted to implement automatic testing in the code but unfortunately haven't had the time to do so. Only manual testing has been done. Everything has been tested by several people and i also have given my superuser access to friends and family in order to test the webpage as thoroughly as possible.

#### Navigation:
  * Navigation has been tested by clicking on all links, trying to reacreate routing errors (django noramlly tells you if you have a view or url missing)
  * Spamming links, going back and forth from one page to another. Trying to recreate posting errors when going to a form submit and then reloading the page. Realoading pages when Stripe is sending intents or tries to make a payment.
  * changing to responsive view to see if links or other important parts disapear/show up incorrectly.
  * testing the return to top button.
  * Checking that all the links are present on all pages.
  I ran into several issues specifically while reloading posts or trying to break stripe while reloading during payment and so on. I therefore created a specific error template that all errors link to and spit out a error message.

#### Sidebar:
  * the same as Navigation testing but also trying to send weird requests in the search query, trying to get to the subscription page when already subscribed.
  I specifically added the requirement to login for subscription and forced to check if you already have a subscription before creating one because of this testing. This helped me narrow down some issues related to subscription payments.

#### Store:
  * There was a lot of testing involved during the development of the store, shopping bag and payment system specifically.
  * We tried to add and remove items from shopping bag, checkout and then return to shopping bag, change quantity of bag items, add different items and going back and forth between pages while doing so, Testing that all the products render correctly in the store, testing all the card sizing, clearing sessions, resizing to responsive mode.
  * Found issues:
    * There was an issue where when you changed the amount of items in the shopping bag and added items it would add them several times because of a accidental loop in the change_amount method. Also written up in a commit.
    * several times product cards rendered wrong and I had to rewrite css for them.
    * Forms were showing up wrong in the start and didn't show errors. I then added Error handling and form-control.

#### Giftcard
  * We tested that giftcards were created and updated correctly, didn't duplicate, returned to their previous state after any error during payment occurs, only are created for logged in users, create counters for free products, free products session is deleted in case of error during payment, that the counters count down correctly while above 7.
  * Found issues:
    * giftcards were saved but during payment error weren't recreated, I fixed this by recreating the original calculation for free items and saving that when an error occurs. After that the free item session is deleted.
    * had several issues where giftcards were suddenly duplicated while i was creating them. Added a filter to check if a giftcard exists before creating one. 
    * Had a massive issue where when someone went to checkout an item the first time and hadn't created any giftcard yet, and at the same time purchased more than 7 it would not add to the free items session and therefore not substract the amount from the total checkout. Fixed this by implementing the counter calculation also during the creation of a giftcard.

#### Queries
  * We tested this searching for all kinds of things but very few errors have been found.
  * Django is really good at telling you when you are iterating through something that can't be iterated or are searching for something that doesn't exist. Therefore a lot of errors that came up were immideatly noticed and fixed.

#### Users
  * Tested that the autofilling works in checkout, tested that you can update and create a userprofile. Tested that it gets deleted when the associated user is deleted. Tested that it requires forms to be valid before saving.
  * Had some issues adding users to the userprofile because i searched wrong for the user and wasn't comfortable with models at that time. Took a lot of the model structure from the code institute project listed below and noticed no issues while testing.

#### Admin
  * **Reading**
    Checking all the possibilities of the browse tab kind of made sure that everything was read as intended and didn't spit out any errors.
  * **Creating**
    Several people and me ensured that everything can be created and that it throws no errors. In fact one of my friends had so much fun with playing with the site that he added a lot of the products for the Store.    
    * Had an issue where animals were stored in the categories model but quickly noticed this when i wanted to add an product to an animal. The problem was in the form code since it used the wrong model as a base and the names of the model lines are the same.

  * **Updating**
    Several people and me ensured that everything that is to edit was editable and didn't throw out any errors by adding numbers, signs, weird letters and so on and it seemed to work nice.

  * **Deleting**
    * Deleting products from page, order, shopping bag, user and so on was tested a lot and quiet thoroughly mostly because of so much data that has been added and modified during the building of the webpage. I therefore had to delete a lot of stuff in order to be able clear the clutter.

#### Authentication
  * The authentication system hasn't been tested much in general mostly because it comes from a already good library (allauth). I tested a lot the social media login but that either worked or it didn't so it was quiet clear to find issues and errors and fix them. 

#### Checkout, subscription and payment:
  * Checkout was tested a lot!, Tried refreshing the page while paying, paied with different testing cards from stripe, tried invalid orders and subscription, webhook handling, error handling, trying to catch all errors,

  * There is still a lot to be done here! I hadn't understood webhook handling before 1 day off submission and from that point on it was to late to implement. I struggled a lot trying to setup a subscription service and also beeing able to retreive it and delete it again. I haven't figured out how to handle responses from stripe in order to wait for an answer before redirecting and also HttpResponses were new to me. In general this needs still a lot of work and I at least think that I am managing to catch all the errors and showing them to the user as well as not commiting the payment, order and subscription when an error occurs. There are also still some errors that I don't understand like the subscription error that comes only when a non 3dsecure card is used. 

  * I think this still needs a lot of work but at the same time I tested enough in order to catch all the errors and present them to the user. As well as not commiting either payment or storing data in the database during an error.

  * #### KNOWN BUGS:
  * Checkout
    * The first time you try to pay and the app talks to stripe the redirect doesn't wait long enough and stripe has no time to respond. It therefore sometimes throws out an 500 error. 
    * When adding only one giftcard item to the shopping cart and this item beeing for free stripe renders an error cause the amount of payment is 0. I noticed this error 1 hour before having to deliver the project and couldn't fix  the issue anymore.
    * My thought of how to fix these bugs:
      * Check in the payment-method view if the amount = 0 and if so check if the shopping bag only contains giftcard products. If so confirm the order without using stripe.
      * Create an await function in order to wait for stripe to reply before redirecting to the next page.
  
  * #### KNOWN BUGS:
  * Subscription
    * Paying with a card that is not 3dsecure sometimes throws out an error that then prevents the creation of a subscription in my own database but which handles a payment in stripe. It only handles the payment and does not create a subscription. Paying with a 3dsecure card does not create this error.
     * I have no idea why this happens since it works with 3dsecure cards.

## Deployment
### Deployment To Heroku
 * I followed the heroku and django guide on how to deploy my page. 
 * I set up a requirements.txt, Procfile and commited to github.
 * Added heroku to my git cli
 * Logged in to heroku and set collect static to 1
 * Set up a postgres database in heroku.
 * migrated everything to the postgres database.
 * pushed to heroku.
 * set up a AWS S3 bucket with public policies (here I followed a code institute guide quiet thoroughly)
 * Set up my static and media url, and root and connected S3 to django and heroku.
 * removed collect static from heroku and pushed.
 * i then added my media files to a media folder i created in S3.

### Link to the deployed page:
* https://hawkward-store.herokuapp.com/

## Credits
Pictures taken from:
  * hawk logo: https://wallpaperscraft.com/download/hawk_bird_funny_179892/1680x1050
  * background image: https://pixabay.com/photos/wood-floor-backdrop-background-1866667/

Code taken from:
  * sidebar: https://colorlib.com/wp/bootstrap-sidebar/
  * Checkout layout and idea: https://getbootstrap.com/docs/4.0/examples/checkout/
  * color scheme: http://www.flatuicolorpicker.com/
  * A lot of inspiration and ideas as well as model and databse structuring from:
    https://github.com/ckz8780/boutique_ado_v1


### Tutorials
* https://www.youtube.com/watch?v=oZwyA9lUwRk&ab_channel=DennisIvy
* https://www.youtube.com/watch?v=tkQafmnBKqk&list=PLlM3i4cwc8zDBTisCexry-FPoGhHO2uE_&index=3&ab_channel=DjangoLessons

### Acknowledgements
* Special thanks to friends, family and coworkers for helping me during development, testing and giving me ideas and implementations that i could use to create this project.
* https://github.com/stephyraju/spiceworld/blob/master/README.md I used this project as a guideline for my README.md