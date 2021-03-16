# Starter testing
- [Primary README.md file](./README.md)
- [View Website](https://https://starter-sourdough.herokuapp.com/.herokuapp.com/)

## Table of Contents
1. [Validators](#validators)
2. [User Stories](#testing-user-stories)
     - [First Time User Goals](#first-time-user-goals)
     - [Returning User Goals](#returning-user-goals)
     - [Member Goals](#returning-user-goals)
     - [Premium Member Goals](#premium-member-goals)
     - [Admin](#admin-goals)
3. [Manual Testing](#manual-testing)
   - [Devices & Browsers](#devices-tested-on)
   - [User Testing](#testing)
   - [Testing Features](#testing-interactive-elements)
4. [Bugs](#bugs)

## Validators
- HTML: [W3C Markup Validator](https://validator.w3.org/)
  - The use of Django templating in the html results in a number of errors in each file, all have been reviewed and deemed acceptable.

- CSS: [W3C CSS Validator](https://jigsaw.w3.org/css-validator/)

- JavaScript: [JSHint](https://jshint.com/)

- Python:
  - [PEP8](http://pep8online.com/)
  - [Gitpod](https://gitpod.io/)

## Testing User stories
### First Time User Goals
#### As a first time user, I want to: 
1. Easily understand the purpose of the website and the services it offers
    -  As user's first enter the site, the use of strong imagery suggest the nature of the site.
    - The logo in the header clearly states the company name and mission: 
    ![Logo](./static/images/readme-images/testing/logo.png)
    - Each aspect of the website is represented on the homepage; shopping, recipes and membership. This gives the user an immediate sense of what the site offers. 

2. Be able to navigate intuitively through the site
    - 


## Manual Testing 
### Devices & Browsers

- The Website was tested on Google Chrome, Firefox, Microsoft Edge and Safari browsers.

- The website was tested on a variety of devices including; Desktop, Laptop, iPad mini, iPhone 7, iPhone 8, iPhoneX, Nokia E30 and Galaxy S20.

- It was also viewed on all devices and orientations available in Chrome DevTools.

### User Testing

- Friends and family members viewed the site and provided feedback on bugs and UX issues.

### Testing Features / Interactive Elements

#### Elements of every page

| Element              | Expected behaviour | Tested On             | Confirmed 
| -------------------- | ------------------ | -----------    | ----------
| Shop Link            | Trigger shop options dropdown| click          | yes
| Main Navigation Links| Takes user to specified page  | click          | yes
| Home Logo            | Takes user to homepage | click          | yes
| Search Icon          | Trigger search dropdown      | click          | yes
| Account Icon         | Trigger account options dropdown | click | yes
| Account Options | Change options depending on user | login | yes
| Basket Icon | Takes user to basket | click | yes
| Hover Features | Change background or colour | hover | yes
| Mobile Nav | Main nav collapses in to burger nav on mobile views | collapse | yes 
| Promo Banner | Takes user to premium page | click  | yes 
| Toasts | Appear when certain actions are taken | carrying out said actions | yes 
| Footer | Featured at the bottom of each page | inspection | yes 


#### Homepage

| Element              | Expected behaviour | Tested On      | Confirmed 
| -------------------- | ------------------ | -----------    | ----------
| Ingredients Image | Takes user to shop filtered by ingredients | click | yes
| Tools Image | Takes user to shop filtered by tools | click | yes
| Featured Recipe | Populated by 'featured' recipe | changing from true / false in admin | yes
| Featured Recipe | Takes user to recipe | click | yes
| Membership Promo Poster | Takes user to premium page | click | yes 
| Featured Products | Populated by 'featured' products | changing from true / false in admin | yes
| Featured Products | Takes user to specified product | click | yes


#### Shop/Products

| Element              | Expected behaviour | Tested On      | Confirmed 
| -------------------- | ------------------ | -----------    | ----------
| Subtitle | Changes depending on where you arrived from; shop or tools | click | yes
| Product Count | Displays product count of specified filter | click / inspection | yes
| Sort Options | Change product display depening on chosen option | click | yes


#### Product Details

| Element              | Expected behaviour | Tested On      | Confirmed 
| -------------------- | ------------------ | -----------    | ----------
| Plus/Minus Buttons | Increases/reduced amount of product to be added | click / add | yes
| 
