# Starter

![Home Responsive](./static/images/readme-images/responsive/home-responsive.png)
## Milestone Project 4: Full Stack Frameworks with Django - Code Institute

[Deployed Version](https://starter-sourdough.herokuapp.com/)

As one of the more difficult trends of the UK lockdown, Starter is an e-commerce website that aims to simplify the processes involved in baking with sourdough. The website offers recipes and useful tools of the trade (available for purchase). A number of free recipes are provided, with paid membership required for access to premium recipes.

**Please use the following card number for test purposes:**
4242 4242 4242 4242

## Table of Contents

1. <details><summary>UX</summary>

   - [User Stories](#user-stories)

     - [First Time User Goals](#first-time-user-goals)
     - [Returning User Goals](#returning-user-goals)
     - [Member Goals](#returning-user-goals)
     - [Premium Member Goals](#premium-member-goals)
     - [Admin](#admin-goals)

   - [Design](#design)
     - [Colour Scheme](#colour-scheme)
     - [Typography](#typography)
     - [Imagery](#imagery)
     - [Icons](#icons)
     - [Layout](#layout)
     - [Styling](#styling)
     - [Wireframes](#wireframes)
         </details>

2. <details><summary>Features</summary>

   - [Existing Features](#existing-features)

     - [Elements on every page](#elements-on-every-page)
     - [Shop](#shop)
     - [Product Details](#product-details)
     - [Basket](#basket)
     - [Product Checkout](#product-checkout)
     - [Recipes](#recipes)
     - [Recipe](#recipe)
     - [Premium](#premium)
     - [Premium Checkout](#premium-checkout)
     - [Stripe Premium Checkout](#stripe-premium-checkout)
     - [User Account](#user-acccount)
     - [Premium Settings](#premium-settings)
     - [Allauth Pages](#allauth-pages)
     - [Confirmation Emails](#allauth-pages)

   - [Features Left to Implement](#features-left-to-implement)
     </details>

3. <details><summary>Information Architecture
   </summary>

   - [Database Choice](#database-choice)

   - [Collections Data Structure](#collections-data-structure)

   </details>

4. <details><summary>Technologies Used
   </summary>

   - [Languages](#languages)

   - [Frameworks, Libraries & Programs Used](#frameworks,-libraries-&-programs-used)

   </details>

5. <details><summary>Testing
   </summary>

   - [testing.md](./testing.md)

   </details>

6. <details><summary>Deployment
   </summary>

   - [Requirements](#requirements)

   - [Making a Local Clone on Gitpod](#making-a-local-clone-on-gitpod)

   - [Heroku Deployment](#heroku-deployment)

   </details>

7. <details><summary>Credits
   </summary>

   - [Content](#content)

   - [Media](#media)

   - [Code](#code)

   - [Acknowledgements](#acknowledgements)
   </details>


# UX

## User Stories

### First Time User Goals 
#### As a first time user, I want to: 

1. Easily understand the purpose of the website and the services it offers
2. Be able to navigate intuitively through the site


### Returning User Goals
#### As a returning, I want to:

1. Browse all products and recipes
2. Browse via product category
3. Search for product and/or recipe by name or description
4. Easily see what I've searched for and the search results
5. As a Returning User, I want to easily select the colour and quantity of a product
6. View items in my basket to be purchased
7. Be able to adjust the quantity of individual items in my basket 
8. See an order confirmation after checkout
9. Receive an email confirmation after checkout
10. Easily find how to become a member
11. Learn about becoming a premium member


### Member Goals
#### As a member, I want to:

1. Easily login and logout
2. Receive an email confirmation upon registering
3. Recover my password in case I forget it
4. Save/update my shipping information
5. View my order history


### Premium Member Goals
#### As a premium member, I want to:

1. View premium content 
2. See when new premium content is added
3. View which subscription service is enabled
4. Easily cancel a subscription service
5. View my next subscription payment date


### Admin Goals
#### As admin, I want to:

1. Add a product
2. Edit/update a product
3. Delete a product
4. Add a recipe 
5. Edit/update a recipe 
6. Delete a recipe
7. Ensure all subscriptions payments are up to date


## Design

The overall design is clean and simple, reflecting the the purpose of the website. 

### Colour Scheme

![Colour Scheme](./static/images/readme-images/colour-scheme.png)

- Colour was used minimullay in order to not detract from the content.
- Bootstrap colours were used on icons in toasts to signal different responses:
    - Success = BS Success
    - Info = BS Info
    - Error = BS Danger
    - Warning = BS Warning 


### Typography

- 'Special Elite' was used for headings and titles as well as the main logo. This type-writer like font was chosen to give the impression of a story or a book. 
- 'Knewave' was used to promote premium content to make it look like a poster.
- 'IBM Plex Sans' was used for all other text. It was chosen for it's readability. 
- A range of font sizes and weights were used to denote importance.
- All fonts had Sans Serif as the back-up font. 


### Imagery
**Bootstrap's 'img-fluid' class was used on the majority of images to ensure responsivity.**

#### Product Images
All product imagery is sized at 640 x 640px based on [this](https://store.magenest.com/blog/ecommerce-product-image/#:~:text=or%20just%20larger.-,Medium%20size%3A%20Product%20pages,or%20800%20x%20800%20image.) Magenest article.

#### Recipe Images
All recipes images are sized at 1200 x 800px based on [this](https://wordpress.org/support/topic/ideal-recipe-picture-size/#:~:text=So%20to%20answer%20the%20size,access%20to%20the%20larger%20images.) Wordpress forum. 

#### Illustrations
![Illustrations](./static/images/readme-images/illustrations.png)
Illustrations were taken from the above Adobe stock image and used throughout the website, complimenting the title/logo font by creating the impression of a story or book. 


#### Membership promo
![Membership Promo](./static/images/member-promo.png)
The membership promo was created in the image of a poster to grab the user's attention and direct them to the premium membership page. 

#### No Image
![No image](./static/images/noimage.png)

The 'No Image' image is used in the event that an image is not uploaded for a product or recipe. 

### Icons
Icons are used throughout the site to provide the user with visual cues and create a more interesting aesthetic.

- Chevron icons are used throughout, to indicate directional links.
- Social media icons are clearly positioned to the left of the footer and are constantly available to the user. Dead links are used as the social media pages to exist at present.
- A crown icon is used when to denote premium membership. 

### Layout
- [Bootstrap's Grid System](https://getbootstrap.com/docs/5.0/layout/grid/) was used throughout to created the layout and make it responsive.

### Styling
- [Bootstrap](https://getbootstrap.com/) was used in conjunction with custom spacing and colours to provide much of the styling for the site. This includes all **buttons**, **cards** and **nav bars**.
- [Django Crispy Forms](https://django-crispy-forms.readthedocs.io/) was used to automatically style form elements.
- [Stripe Elements](https://stripe.com/docs/stripe-js) was used to style the product checkout.
- [Stripe Checkout](https://stripe.com/docs/payments/checkout) was used for the subscription/premium membership checkout. 

### Wireframes

- [Homepage](./static/images/readme-images/wireframes/Homepage.png)

- [Shop](./static/images/readme-images/wireframes/Shop.png)

- [Product Details](./static/images/readme-images/wireframes/Product-Details.png)

- [Shopping Basket](./static/images/readme-images/wireframes/Shopping-Basket.png)

- [Product Checkout](./static/images/readme-images/wireframes/Checkout.png)

- [Recipes](./static/images/readme-images/wireframes/Recipes.png)

- [Recipe Details](./static/images/readme-images/wireframes/Recipe-Details.png)

- [Premium](./static/images/readme-images/wireframes/Premium.png)

- [Premium Basket](./static/images/readme-images/wireframes/Premium-Basket.png)

- [Account](./static/images/readme-images/wireframes/Account.png)


# Features

## Existing Features

### Elements on every page

![Nav](./static/images/readme-images/nav.png)
#### Navbar
- The main navigation to the left of the bar shows the main website pages avaible to everyone.
- The icon links to the right represent other key features of the site. 
- Active classes are added to active page to show the user what page they are currently on.
- Account options differ depending on user: 
    - Not logged in:
        - Sign In 
        - Sign Up
    - Logged in:
        - Account 
        - Sign Out
    - Admin/Superuser:
        - Product Management 
        - Recipe Management
        - Update Premium Memberships
        - Account
        - Sign In 
        - Sign Out
    - Django/Python checks whether a user is logged in or not with `if request.user.is_authenticated` and whether the user is a Superuser with `if request.user.is_superuser ` to display the correct navigation to the user. 

- Mobile Nav 
![Nav Mobile](./static/images/readme-images/nav-mobile.png)
    - The main navigation and account collapse in to a burger nav icon.
    - The subheading of the logo is dropped.

- Dropdowns
![Nav Dropdown](./static/images/readme-images/nav-dropdown.png)
![Mobile Dropdown](./static/images/readme-images/mobile-dropdown.png)
    - Dropdowns were used to reserve space. 
    - The background is solid white to prevent any background interference.

#### Promo Banner
![Promo banner](./static/images/readme-images/promo-banner.png)
- The promo banner is placed at the top of the screen to immediately alert the user of promotions. 
- The banner is removed on mobile views to reserve space.

#### Toasts
![Toasts](./static/images/readme-images/toasts.png)
- Bootstrap toasts are used to provide feedback to the user for certain actions, e.g. adding/removing a product, signing in/out. 
- The toast also provides a running summary of the user's shopping basket and link to proceed. 

#### Footer 
![Nav Mobile](./static/images/readme-images/footer.png)
- To reflect the nature of the website, the footer only contains the bare necessities; social links and contact email.

### Homepage
![Home Responsive](./static/images/readme-images/responsive/home-responsive.png)

- The homepage immediately directs the user to shop for either ingredients or tools. Clicking either will take the user to their specified shopping category.


![Homepage](./static/images/readme-images/home/homepage-2.png)
![Homepage](./static/images/readme-images/home/homepage-3.png)

- Both the Product and Recipe modal contain a boolean field called 'featured' 

- The home app uses python to filter recipes/products by 'featured' which are passed in to a Django template and sliced to display the correct amount for the layout: 

    - `for recipe in featured_recipes|slice:":1"`
    - `for product in featured_products|slice:":4"`

- This option allows superusers to customise their homepage by ticking the featured checkbox when creating or editing a product/recipe. 

- To the left, a promotional poster is displayed to encourage the user to become a member. Clicking navigates user to the premium purchase options. 

#### Promo Poster
- The Promo Poster was created to alert the user to the website's premium membership. 


### Shop / Products Page

![Shop Responsive](./static/images/readme-images/responsive/shop-responsive.png)

#### Products
- Bootstrap cards were used to display product information
- If user's arrived on the shop page via the 'all' navigation all products will be visable.
- If user's arrived on the shop page via the 'tools' or 'ingredients' the products will be filtered by their respective category with the category name displayed e.g:

![Shop Filter](./static/images/readme-images/products/shop-filter.png)

#### Product Count

- Logic to display product count of selected filter: `{{ products|length }}`

#### Sort Options
![Sort options](./static/images/readme-images/products/sort-options.png)

- User's are able to sort products by a number of options to make shopping easier. 

### Product Details Page
![Product Details](./static/images/readme-images/responsive/product-details-responsive.png)

#### Buttons
![Product Details Buttons](./static/images/readme-images/products/product-details-buttons.png)

- The quantity buttons use javascript to overlay the default plus/minus buttons to fit with the style of the website.

- The Add to Basket uses python/django to add the specified quantity of the specified product to the shopping basket. If successful, a success toast is triggered with a summary of the shopping basket and the items are stored in the session. 

- Edit/delete buttons are visable if the user is a Superuser: `if request.user.is_superuser `. 

- Clicking delete triggers a defensive modal:
![Delete modal](./static/images/readme-images/products/delete-product-modal.png)

#### Inventory / Stock
Python logic is used to prevent the user from adding products to their basket that are out of stock or exceed the amount of inventory currently in stock. 

- If a product has 0 Inventory, the 'Add to Basket' button is disable and a message is displayed. 
![Out of stock](./static/images/readme-images/products/no-stock.png)

- If a product exce the amount of inventory currently in stock a toast is displayed and the product is not added to the basket. 
![Exceeds Amount Toast](./static/images/readme-images/products/inventory-exceed.png)


### Shopping Basket

#### Empty Shopping Basket 
![Empty Shopping Basket ](./static/images/readme-images/shopping-basket/empty-basket.png)

#### Shopping Basket with Contents
![Empty Shopping Basket ](./static/images/readme-images/shopping-basket/basket.png)
- The information is laid out in clear way to allow user's to review for proceeding.

#### Product Controls
- The user is able to update the quantity of the item or remove the item before proceeding to checkout. 

#### Total 
- Keeps a running total of all products and shipping. 
- If the total amounts to less than the free shipping threshold a message is displayed to inform the user of how much more they have to spend to qualify for free shipping.

#### Directional Buttons
- The 'Continue to Secure Checkout' is the most prominent button on the page to direct the user to the checkout.
- The keep shopping button takes the user back to products.

### Product Checkout
![Checkout](./static/images/readme-images/product-checkout/checkout.png)

#### Product Details
- The user is displayed a summary of what they are about to purchase for final review.

#### The Form
- The form combines stripe elements with crispy forms to provide the logic and styling. 
- Contact Information: 
    - If the user is annonymous, they are prompted to sign / in or register to save their contact information. This will be related to the user's profile. 
    - If the user is logged in ( `if user.is_authenticated` ) a checkbox to save shipping information is visable:
    ![Save Shipping](./static/images/readme-images/product-checkout/save-shipping.png)
    - If ticked the shipping information is then save on the user's profile. This time saving feature makes user's more likely to proceed with a purchase in the future. 
    - If a required field is left empty the user is alerted and prevented from proceeding:
    ![Required Field](./static/images/readme-images/product-checkout/required-field.png)

- Payment Information:
    - Stripe is used to handle payments
    - The user is informed of invalid payment information with the alerts from Stripe:
    ![Invalid Payment](./static/images/readme-images/product-checkout/invalid-payment.png)

- Completing payment  
    - The complete payment button sends the entered information and triggers a loading screen: 
    ![Loading Screen](./static/images/readme-images/product-checkout/loading-screen.png)
    - The loading screen informs that their request is being handled and therefor prevents refereshing or any other interuption that may effect the payment process.


### Product Checkout Success
![Product Checkout Success](./static/images/readme-images/product-checkout/product-checkout-success.png)
- Provides user's with a summary of their order and informs them that an email has been sent to their account as assurance. 

### Recipes
![Recipes Responsive](./static/images/readme-images/responsive/recipes-responsive.png)

#### Subtitle 
- Python/Django checks if profile has membership attached with `if profile.membership`
- If the user is not logged in or does not have a membership they are encouraged to become a premium in order to access premium content: 
![Recipes Subtitle](./static/images/readme-images/recipes/recipes-subtitle-1.png)
- If the user has a membership: 
![Recipes Subtitle](./static/images/readme-images/recipes/recipes-subtitle-2.png)

#### Recipe Cards
- The recipe cards feature a large photo, recipe title and a free or premium tag.
- Having both free and premium content shows the user the quality of the recipes making them more likely to want to access the premium content.
- Python/Django checks if the recipe is premium with `if recipe.premium` and displays the correct tag accordingly:
![Free Content](./static/images/readme-images/recipes/free-content1.png)
![Premium Content](./static/images/readme-images/recipes/premium-content1.png)


### Recipe Details
![Recipe Details](./static/images/readme-images/responsive/recipe-details-responsive.png)

- Python/Django handels whether a user has premium membership to access premium recipes: `  if request.user.userprofile.membership`

#### Bootstrap Accordian
- A Bootstrap accordian is used to show/hide subsections of the recipe. 
- Ingredients are rendered using a bootstrap table for clarity. 

#### Buttons
- Edit/delete buttons are visable if the user is a Superuser: `if request.user.is_superuser `. 

### Premium
![Premium](./static/images/readme-images/responsive/premium-responsive.png)
- The premium page provides users of information of what is included with premium membership and how to cancel once purchased, for assurance. 

#### Payment Options
- Bootstrap images cards are used to display the two payemnt options.
- The cars are of one whole image split in to two for visual impact and continuity. 
- Overlayed text is white and has a text-shadow to ensure readability.
- Clicking on either takes the user to checkout with specified option.

#### Promotional Offer
- The promotional offer displayed in the banner is repeated below the payment options as a reminder to users before proceeding. 

### Premium Basket/Checkout
![Premium Basket/Checkout](./static/images/readme-images/premium/premium-basket.png)
- The user must have profile, to which the membership will be attached, to access this page. 
- If the user is not logged in / does not have a profile they will be redirected to the Sign In page: 
![Sign In Redirect](./static/images/readme-images/premium-signin.png)
- If the user already has a membership they will be redirected to their account:
![Account Redirect](./static/images/readme-images/premium/account-redirect.png)
- The premium basket mirrors the shopping basket for continuity.
- The information is laid out in clear way to allow user's to review for proceeding.
- The user is informed that promo codes can be entered at the next stage. 
- A back button is provided in case the user wants to change payment option. 

### Stripe Premium Checkout
![ Stripe Premium Checkout](./static/images/readme-images/premium/premium-checkout.png)
- [Stripe Checkout](https://stripe.com/docs/billing/subscriptions/checkout) is used to render information and handle payment of subscriptions. 
- If the user goes clicks the back arrow they are re-directed to the transaction cancelled page to reassure them that they will not be charged: 
![Transaction Cancelled](./static/images/readme-images/premium/transaction-cancelled.png)
- Stripe creates the subscription `stripe.checkout.Session.create`.

### Premium Checkout Success
![Premium Checkout Success](./static/images/readme-images/premium/premium-success.png)
- If the transaction is successful, the membership will be attached to their account and the user will be able to see the changes immediately. 
- Successful payment is confirmed by the checkout success page. 

### Account 
#### Account Details
- If the user has previously purchased something and ticked the [Save Shipping Details](#the-form) checkbox at checkout this form will be populated with the saved information.
- Users can update this information to populate the contact information on the [Product Checkout](#product-checkout) page.

#### Premium Membership
- If a user does not have a membership:
![Account Non-Member](./static/images/readme-images/account/account-nonmember.png)

- If a user has membership:
![Account Member](./static/images/readme-images/account/account-member.png)
- Python/Django inserts the most recently added recipe.
- The settings button takes the user to their membership settings. 

#### Order History 
- Displays user's order history in a Bootstrap table.
- Clicking the order number takes the user to the specified order summary, that mirrors that of the [Product Checkout Success](#product-checkout-success) page, with an altered message:
![Order Sumamry](./static/images/readme-images/account/order-summary.png)

### Premium Settings
(#product-checkout-success) page, with an altered message:
![Premium Settings](./static/images/readme-images/premium/premium-settings.png)
- This page retrieves information from the user's specific Stripe Subscription `stripe.Subscription.retrieve(request.user.userprofile.stripe_subscription_id)` and renders it to the display.
- The Cancel Membership triggers a defensive modal:
![Cancel Modal](./static/images/readme-images/premium/premium-modal.png)
- If cancelled, the Stripe Subscription information is altered to stop taking payments and end of the next billing period and the following page is now displayed using `{% if cancel_at_period_end %}`:
![Premium Cancelled](./static/images/readme-images/premium/membership-cancelled.png)

### Product Management 
![Product Management](./static/images/readme-images/products/product-management.png)
- The Product management page can only be accessed by superusers, if a non superuser attempts to access the page `if not request.user.is_superuser` they are redirected back to the homepage with the following message:
![Product Management](./static/images/readme-images/products/non-storeowner-message.png)

#### The Form
- Allows superusers to add a product 
- All required fields are labelled with *




### Recipe Management

### Update Premium Memberships

### Allauth Pages

### Confirmation Emails


